import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import onnx
import onnxruntime as ort
from omegaconf import OmegaConf

from ..inference_engine.onnxruntime.provider_config import ProviderConfig
from .download_file import DownloadFile, DownloadFileInput
from .logger import Logger

MODEL_URL_PATH = Path(__file__).resolve().parent.parent / "default_models.yaml"
DEFAULT_MODEL_PATH = Path(__file__).resolve().parent.parent / "models"


class KVCache:
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.cache = {}
        self.view = {}

    def alloc(self, name, batchxbeam, max_seq_len):
        try:
            import torch

            self.device = torch.device("cuda", self.device_id)
        except:
            self.device = None

        if self.device is None:
            return

        """allocate a tensor on cuda"""
        # shape: (12, batchxbeam, 6, max_len, 2 * 64)
        shape = (12, batchxbeam, 6, max_seq_len, 2 * 64)
        tensor = torch.empty(shape, dtype=torch.float32, device=self.device)
        self.cache[name] = {
            "tensor": tensor,
            "shape": shape,
        }

    def has_name(self, name):
        return name in self.view

    def alloc_view(self, buffer_name, name, batchxbeam, seq_len):
        """allocate a view of a tensor on cuda"""
        if buffer_name not in self.cache:
            return

        buffer_shape = self.cache[buffer_name]["shape"]
        assert buffer_shape[3] >= seq_len
        assert buffer_shape[1] >= batchxbeam
        self.view[name] = {
            "tensor": self.cache[buffer_name]["tensor"][:, :batchxbeam, :, :seq_len, :],
            "shape": (buffer_shape[0], batchxbeam, buffer_shape[2], seq_len, buffer_shape[4]),
        }

    def clear_view(self):
        self.view = {}

    def bind_input(self, io_binding, name):
        io_binding.bind_input(
            name=name,
            device_type='cuda',
            device_id=0,
            element_type=1,
            shape=self.view[name]["shape"],
            buffer_ptr=self.view[name]["tensor"].data_ptr(),
        )

    def bind_output(self, io_binding, name):
        io_binding.bind_output(
            name=name,
            device_type='cuda',
            device_id=0,
            element_type=1,
            shape=self.view[name]["shape"],
            buffer_ptr=self.view[name]["tensor"].data_ptr(),
        )

    def get_tensor(self, name):
        return self.cache[name]["tensor"]


ort.set_default_logger_severity(3)


def numpy_obj_to_dtype(arr: np.ndarray):
    dtype_map = {
        np.dtype('float32'): 1,
        np.dtype('uint8'): 2,
        np.dtype('int8'): 3,
        np.dtype('uint16'): 4,
        np.dtype('int16'): 5,
        np.dtype('int32'): 6,
        np.dtype('int64'): 7,
        np.dtype('bool'): 9,
        np.dtype('float64'): 11,
    }
    np_dtype = arr.dtype
    if np_dtype in dtype_map:
        return dtype_map[np_dtype]
    else:
        raise TypeError(f"Unsupported dtype: {np_dtype} ({type(np_dtype)})")


def inspect_ortvalue(ov):
    print("OrtValue Info:")
    print("  Shape      :", ov.shape())
    print("  DType      :", ov.data_type())
    print("  Device     :", ov.device_name())
    print("  Data Ptr   :", hex(ov.data_ptr()))
    print("  Is Tensor? :", ov.is_tensor())


def sequence_mask_np(lengths, max_len=None):
    lengths = np.asarray(lengths)
    batch_size = lengths.shape[0]
    max_len = max_len or lengths.max()
    mask = np.arange(max_len)[None, :] < lengths[:, None]
    return np.expand_dims(mask, axis=1)


# def log_softmax(x, axis=-1):
#     e = np.exp(x - np.max(x, axis=axis, keepdims=True))
#     return np.log(e / np.sum(e, axis=axis, keepdims=True))


def log_softmax(x, axis=-1):
    x_max = np.max(x, axis=axis, keepdims=True)
    x_shifted = x - x_max
    log_sum_exp = np.log(np.sum(np.exp(x_shifted), axis=axis, keepdims=True))
    return x_shifted - log_sum_exp


def gather_nd(params: np.ndarray, indices: np.ndarray) -> np.ndarray:
    indices = indices.T.astype(np.int64)
    ndim, M = indices.shape
    idx = np.zeros(M, dtype=np.int64)
    m = 1
    for i in range(ndim - 1, -1, -1):
        idx += indices[i] * m
        m *= params.shape[i]

    tail_shape = params.shape[ndim:]
    flat = params.reshape(-1, *tail_shape)

    return flat[idx]


def gather_tree_numpy(values, parents):
    """
    values: shape [time, batch*beam, ...] or [time, beam]
    parents: shape [time, batch*beam] or [time, beam]
    """
    time, BxK = parents.shape
    # Assumme batch = BxK / beam_size
    beam = BxK  # treat as single-beam for each batch element
    res = np.zeros_like(values)
    res[-1] = values[-1]
    for b in range(BxK):
        parent = parents[-1, b]
        for t in range(time - 2, -1, -1):
            res[t, b] = values[t, parent]
            parent = parents[t, parent]
    return res


def finalize(beam_size, output_ids, parent_ids, out_seq_lens, end_id, max_seq_len=None):
    BxK = out_seq_lens.shape[0]
    B = BxK // beam_size

    # 1. reshape lengths to (B, beam)
    seq_lens = out_seq_lens.reshape(B, beam_size)
    max_lens = np.max(seq_lens, axis=1)  # shape [B]

    # 2. set max_time
    T = max_seq_len if max_seq_len is not None else int(max_lens.max())

    # 3. reshape outputs and parents to [time, batch, beam]
    output_ids = output_ids[: T * B * beam_size].reshape(T, B, beam_size)
    parent_ids = parent_ids[: T * B * beam_size].reshape(T, B, beam_size)

    # 4. gather_tree for each batch-element
    ids = np.zeros_like(output_ids)
    for b in range(B):
        vals = output_ids[:, b, :]  # [T, beam]
        pars = parent_ids[:, b, :]
        traced = gather_tree_numpy(vals, pars)
        ids[:, b, :] = traced

    # 5. swap to [batch, beam, time]
    ids = np.transpose(ids, (1, 2, 0))

    # 6. count length (EOS token before)
    eos_mask = ids == end_id
    # find the first EOS position, if no EOS, return T
    lengths = np.where(eos_mask.any(-1), eos_mask.argmax(-1), T)
    return ids, lengths


def topk(a, k, axis=-1, largest=True, sorted=True):
    if largest:
        indices = np.argpartition(-a, kth=k - 1, axis=axis)
    else:
        indices = np.argpartition(a, kth=k - 1, axis=axis)

    topk_indices = np.take(indices, np.arange(k), axis=axis)
    topk_values = np.take_along_axis(a, topk_indices, axis=axis)

    if sorted:
        sort_order = np.argsort(-topk_values if largest else topk_values, axis=axis)
        topk_values = np.take_along_axis(topk_values, sort_order, axis=axis)
        topk_indices = np.take_along_axis(topk_indices, sort_order, axis=axis)

    return topk_values, topk_indices


class ORTSeq2Seq(object):
    """
    This class is used to run the encoder and decoder of the vision2seq model
    """

    def __init__(self, cfg: Dict[str, Any]):
        self.logger = Logger(logger_name=__name__).get_log()

        encoder_path = cfg.get("encoder_model_path", None)
        decoder_path = cfg.get("decoder_model_path", None)
        if not encoder_path or not decoder_path:
            model_info = OmegaConf.load(MODEL_URL_PATH)
            key = f"{cfg.engine_type.value}.{cfg.ocr_version.value}.{cfg.task_type.value}.{cfg.lang_type.value}"
            model_info = OmegaConf.select(model_info, key)

            encoder_info = {
                'url': model_info.encoder_model_dir,
                'path': DEFAULT_MODEL_PATH / Path(model_info.encoder_model_dir).name,
                'sha256': model_info.encoder_SHA256,
            }
            decoder_info = {
                'url': model_info.decoder_model_dir,
                'path': DEFAULT_MODEL_PATH / Path(model_info.decoder_model_dir).name,
                'sha256': model_info.decoder_SHA256,
            }

            for model_type, info in [('encoder', encoder_info), ('decoder', decoder_info)]:
                download_params = DownloadFileInput(
                    file_url=info['url'], sha256=info['sha256'], save_path=info['path'], logger=self.logger
                )
                DownloadFile.run(download_params)
                self.logger.info(f"Downloaded {model_type} model to {info['path']}")

            encoder_path = encoder_info['path']
            decoder_path = decoder_info['path']

        if not Path(encoder_path).exists():
            raise FileNotFoundError(f"Encoder model not found: {encoder_path}")
        if not Path(decoder_path).exists():
            raise FileNotFoundError(f"Decoder model not found: {decoder_path}")

        use_io_binding = cfg.get("use_io_binding", True)
        device = cfg.get("device", 'cuda')
        use_cache = cfg.get("use_cache", False)

        # provider_cfg = ProviderConfig(engine_cfg=cfg.engine_cfg)
        # providers = provider_cfg.get_ep_list()
        # provider_cfg.verify_providers(providers)
        provider = 'CPUExecutionProvider' if device == 'cpu' else 'CUDAExecutionProvider'
        self.logger.info(f"Providers: {provider}")

        self.encoder_session = ort.InferenceSession(encoder_path, providers=[provider])
        self.encoder_io_binding = ort.IOBinding(self.encoder_session)
        self.decoder_session = ort.InferenceSession(decoder_path, providers=[provider])
        self.decoder_io_binding = ort.IOBinding(self.decoder_session)
        self.use_io_binding = use_io_binding
        self.device = device
        self.encoder_sign = {
            'input_names': [inp.name for inp in self.encoder_session.get_inputs()],
            'output_names': [inp.name for inp in self.encoder_session.get_outputs()],
        }
        self.decoder_sign = {
            'input_names': [inp.name for inp in self.decoder_session.get_inputs()],
            'output_names': [inp.name for inp in self.decoder_session.get_outputs()],
        }

        self.vocab = self._load_vocab(decoder_path)
        self.vocab_size = len(self.vocab)
        self.end_id = self.vocab.index('[EOS]')
        self.kv_cache = None
        if use_cache:
            self.kv_cache = KVCache()
            self.kv_cache.alloc('kvs_buffer', 32 * 5, 210)

    def _load_vocab(self, decoder_path):
        model = onnx.load(decoder_path)
        vocab_json = None
        for prop in model.metadata_props:
            if prop.key == "vocab":
                vocab_json = prop.value
                break

        if vocab_json is None:
            raise ValueError("No 'vocab' field found in ONNX metadata.")

        return json.loads(vocab_json)

    def batch_decode(self, outputs):
        texts = []
        for j in range(outputs.shape[0]):
            text = ""
            for i in range(outputs.shape[2]):
                if outputs[j][0][i] in [0, 1]:  # EOS, PAD
                    break
                if outputs[j][0][i] == 2:  # UNK
                    continue
                text += self.vocab[outputs[j][0][i]]
            texts.append(text)
        return texts

    def clear_io_binding(self):
        self.encoder_io_binding.clear_binding_inputs()
        self.encoder_io_binding.clear_binding_outputs()
        self.decoder_io_binding.clear_binding_inputs()
        self.decoder_io_binding.clear_binding_outputs()

    def _bind_io_for_encoder(self, inputs: Dict[str, np.ndarray]):
        # clear io binding
        # bind inputs
        for inp in self.encoder_session.get_inputs():
            name = inp.name
            assert name in inputs
            arr = inputs[name]
            self.encoder_io_binding.bind_input(
                name=name,
                device_type='cpu',
                device_id=0,
                element_type=numpy_obj_to_dtype(arr),
                shape=arr.shape,
                buffer_ptr=arr.ctypes.data,
            )

        # bind outputs (cpu or gpu)
        output_name0 = self.encoder_sign['output_names'][0]
        self.encoder_io_binding.bind_output(name=output_name0, device_type=self.device, element_type=1)

    def _bind_io_for_decoder(self, inputs: Dict[str, Any], cache=None):
        # clear io binding
        # bind inputs
        for inp in self.decoder_session.get_inputs():
            name = inp.name
            assert name in inputs
            arr = inputs[name]
            # arr type is np.ndarray or OrtValue
            if isinstance(arr, np.ndarray):
                self.decoder_io_binding.bind_input(
                    name=name,
                    device_type='cpu',
                    device_id=0,
                    element_type=numpy_obj_to_dtype(arr),
                    shape=arr.shape,
                    buffer_ptr=arr.ctypes.data,
                )
            else:
                self.decoder_io_binding.bind_ortvalue_input(name, arr)

        # logits (on cpu), self_attn_kvs (on cpu or gpu)
        # scores (bb, 1, k), new_word_ids (bb, 1, k), merged_self_attn_kvs
        output_names = self.decoder_sign['output_names']
        self.decoder_io_binding.bind_output(name=output_names[0], device_type='cpu', element_type=1)

        self.decoder_io_binding.bind_output(name=output_names[1], device_type='cpu', element_type=1)

        # bingind with cache
        if cache is not None:
            assert cache.has_name(output_names[2])
            cache.bind_output(self.decoder_io_binding, output_names[2])
        else:
            self.decoder_io_binding.bind_output(name=output_names[2], device_type=self.device, element_type=1)

    def forward_encoder(self, inputs: List[np.ndarray]):
        encoder_inputs = {}
        for k, v in zip(self.encoder_sign['input_names'], inputs):
            encoder_inputs[k] = v

        if self.use_io_binding:
            self._bind_io_for_encoder(encoder_inputs)
            self.encoder_session.run_with_iobinding(self.encoder_io_binding)
            encoder_outputs = self.encoder_io_binding.get_outputs()
        else:
            output_names = self.encoder_sign['output_names']
            encoder_outputs = self.encoder_session.run(output_names, encoder_inputs)
        return encoder_outputs

    def forward_decoder(self, inputs: List[Any], cache=None):
        # words_ids, cross_attn_kvs, self_attn_kvs, src_mask_pad, beam_indices
        decoder_inputs = {}
        for k, v in zip(self.decoder_sign['input_names'], inputs):
            decoder_inputs[k] = v

        if self.use_io_binding:
            self._bind_io_for_decoder(decoder_inputs, cache)
            self.decoder_session.run_with_iobinding(self.decoder_io_binding)
            decoder_outputs = self.decoder_io_binding.get_outputs()
            decoder_outputs = (decoder_outputs[0].numpy(), decoder_outputs[1].numpy(), decoder_outputs[2])
        else:
            output_names = self.decoder_sign['output_names']
            decoder_outputs = self.decoder_session.run(output_names, decoder_inputs)
        return decoder_outputs

    def greedy_search(self, images: np.ndarray, images_shape: np.ndarray):
        encoder_outputs = self.forward_encoder([images, images_shape])
        cross_attn_kvs = encoder_outputs[0]
        batch_size = images.shape[0]
        max_len = images.shape[3] // 4
        memory_sequence_length = images_shape[:, 1] // 4

        # init
        words_ids = np.zeros(batch_size, dtype=np.int64).reshape((1, batch_size, 1))
        self_attn_kvs = np.zeros((12, batch_size, 6, 0, 2 * 64), dtype=np.float32)
        src_mask_pad = sequence_mask_np(memory_sequence_length, max_len)
        beam_indices = np.arange(batch_size, dtype=np.int64)

        # loop condition and variables
        extra_decode_length = 10
        max_seq_len = max_len + extra_decode_length
        output_scores = np.zeros([max_seq_len, batch_size], dtype=np.float32)
        output_ids = np.zeros([max_seq_len, batch_size], dtype=np.int64)
        finished = np.zeros((batch_size,), dtype=np.bool_)
        sequence_lengths = np.zeros((batch_size,), dtype=np.int64)
        cum_log_probs = np.zeros((batch_size,), dtype=np.float32)
        seq_len = -1

        for step in range(max_seq_len):
            if finished.all():
                break

            outputs = self.forward_decoder([words_ids, cross_attn_kvs, self_attn_kvs, src_mask_pad, beam_indices])

            topk_scores, ids, merged_self_attn_kvs = outputs
            idx = np.argsort(-topk_scores.reshape(batch_size, -1), axis=-1)[:, :1]
            curr_scores = np.take_along_axis(topk_scores.reshape(batch_size, -1), idx, axis=-1)
            curr_words_ids = np.take_along_axis(ids.reshape(batch_size, -1), idx, axis=-1)

            sequence_lengths = np.where(finished, sequence_lengths, sequence_lengths + 1)
            cum_log_probs = np.where(finished, cum_log_probs, cum_log_probs + curr_scores.reshape(-1))

            finished = np.bitwise_or(finished, curr_words_ids.reshape(-1) == 1)
            output_ids[step, :] = curr_words_ids.reshape(-1)
            output_scores[step, :] = curr_scores.reshape(-1)

            words_ids = curr_words_ids.reshape((1, -1, 1))
            self_attn_kvs = merged_self_attn_kvs
            seq_len += 1

        output_ids = output_ids[: seq_len + 1, :]
        output_scores = output_scores[: seq_len + 1, :]
        beams = np.transpose(output_ids, (1, 0)).reshape(batch_size, 1, -1)
        avg_log_probs = cum_log_probs.reshape(-1) / sequence_lengths.reshape(-1)
        avg_log_probs = avg_log_probs.reshape(-1, 1)
        # scores = np.transpose(output_scores, (1, 0)).reshape(batch_size, 1, -1)
        return beams, avg_log_probs

    def beam_search(self, images: np.ndarray, images_shape: np.ndarray, beam_size: int = 5):
        encoder_outputs = self.forward_encoder([images, images_shape])
        # cross_attn_kvs: (12, B, 6, src_len, 2 * 64)
        cross_attn_kvs = encoder_outputs[0]
        batch_size = images.shape[0]
        max_len = images.shape[3] // 4
        memory_sequence_length = images_shape[:, 1] // 4
        # (B, 1, src_len)
        src_mask_pad = sequence_mask_np(memory_sequence_length, max_len)

        # init
        batchxbeam = batch_size * beam_size
        if self.device == 'cuda':
            src_mask_pad = ort.OrtValue.ortvalue_from_numpy(src_mask_pad, device_type='cuda', device_id=0)

        words_ids = np.zeros(batchxbeam, dtype=np.int64).reshape((1, batchxbeam, 1))
        self_attn_kvs = np.zeros((12, batchxbeam, 6, 0, 2 * 64), dtype=np.float32)
        beam_indices = np.arange(batchxbeam, dtype=np.int64)
        vocab_size = self.vocab_size
        end_id = self.end_id

        # loop condition and variables
        extra_decode_length = 10
        max_seq_len = max_len + extra_decode_length

        cum_log_probs = np.full((batchxbeam,), -np.inf)
        cum_log_probs[::beam_size] = 0
        finished = np.zeros((batchxbeam,), dtype=np.bool_)
        parent_ids = np.zeros((max_seq_len, batchxbeam), dtype=np.int64)
        output_ids = np.zeros((max_seq_len, batchxbeam), dtype=np.int64)
        sequence_lengths = np.zeros((batchxbeam,), dtype=np.int64)
        offset = (np.arange(beam_size) * vocab_size).reshape(1, beam_size, 1)
        batch_index = np.repeat(np.arange(batch_size), beam_size).reshape(-1, 1)
        seq_len = -1

        kv_cache = self.kv_cache
        if kv_cache is not None:
            kv_cache.clear_view()

        for step in range(max_seq_len):
            if finished.all():
                break

            if kv_cache is not None:
                kv_cache.alloc_view('kvs_buffer', 'merged_self_attn_kvs', batchxbeam, step + 1)

            outputs = self.forward_decoder(
                [words_ids, cross_attn_kvs, self_attn_kvs, src_mask_pad, beam_indices], kv_cache
            )

            topk_scores, ids, merged_self_attn_kvs = outputs
            topk_scores[finished, 0, :] = [0, -100, -100, -100, -100]
            ids[finished, 0, :] = [1, 2, 2, 2, 2]

            scores = topk_scores.reshape(-1, beam_size) + cum_log_probs.reshape(-1, 1)

            scores = scores.reshape(batch_size, -1)
            ids = ids.reshape(batch_size, beam_size, -1)

            ids = ids + offset
            ids = ids.reshape(-1, beam_size * beam_size)
            _, final_ids = topk(scores, beam_size)

            final_ids = final_ids.reshape(-1, 1)
            index = np.concatenate([batch_index, final_ids], axis=1)
            sample_ids = gather_nd(ids, index)
            sample_ids = sample_ids.reshape(-1)

            # [batch_size * beam_size]
            word_ids = sample_ids % vocab_size
            beam_ids = sample_ids // vocab_size

            batch_pos = np.arange(batchxbeam) // beam_size
            beam_indices = batch_pos * beam_size + beam_ids
            sequence_lengths = np.where(finished, sequence_lengths, sequence_lengths + 1)
            next_cum_log_probs = gather_nd(scores, index)

            finished = finished[beam_indices]
            sequence_lengths = sequence_lengths[beam_indices]
            parent_ids[step, :] = beam_ids
            output_ids[step, :] = word_ids

            cum_log_probs = np.where(finished, cum_log_probs, next_cum_log_probs)
            finished = np.bitwise_or(finished, np.equal(word_ids, end_id))

            # update status for next search
            words_ids = word_ids.reshape((1, -1, 1))
            self_attn_kvs = merged_self_attn_kvs
            beam_indices = beam_indices.reshape(-1)
            seq_len += 1

        # breakpoint()
        parent_ids = parent_ids[: seq_len + 1, :]
        output_ids = output_ids[: seq_len + 1, :]
        beams, lengths = finalize(beam_size, output_ids, parent_ids, sequence_lengths, end_id)
        # best_beams = beams[:, 0, :]
        # best_lengths = lengths[:, 0]
        # best_probs = cum_log_probs.reshape(-1, beam_size)[:, 0]
        avg_log_probs = cum_log_probs.reshape(-1) / (lengths + 1).reshape(-1)
        avg_log_probs = avg_log_probs.reshape(-1, beam_size)

        return beams, avg_log_probs

    def run(self, inputs: List[np.ndarray], beam_size: int = 5):
        if beam_size and beam_size > 1:
            return self.beam_search(inputs[0], inputs[1], beam_size)
        else:
            return self.greedy_search(inputs[0], inputs[1])
