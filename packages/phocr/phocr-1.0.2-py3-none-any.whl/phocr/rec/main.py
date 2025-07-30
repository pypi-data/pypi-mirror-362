import time
from collections import defaultdict
from typing import Any, Dict, List, Tuple

import cv2
import numpy as np

from phocr.inference_engine.base import get_engine
from ..utils.onnx_helper import ORTSeq2Seq

from ..utils import Logger, batched
from .typings import TextRecInput, TextRecOutput

logger = Logger(logger_name=__name__).get_log()


class Preprocess:
    def __init__(self, cfg: Dict[str, Any]):
        self.image_height = cfg.get('rec_img_height', 32)
        self.min_width = cfg.get('rec_min_width', 40)
        self.channels = cfg.get('rec_channels', 1)
        self.downsample_rate = cfg.get('rec_downsample_rate', 4)
        self.max_img_side = cfg.get('rec_max_img_side', 800)

    def _pad_image_to_width(self, img: np.ndarray, max_width: int) -> np.ndarray:
        """Pad image to match maximum width in batch."""
        height, width, channels = img.shape
        padding_width = max_width - width
        padding = np.zeros((height, padding_width, channels))
        return np.concatenate([img, padding], axis=1)

    def _resize_image(
        self,
        img: np.ndarray,
        target_height: int,
        min_width: int,
        max_width: int,
        is_grayscale: bool,
        downsample_rate: int,
    ) -> np.ndarray:
        """Resize image with proper padding and aspect ratio preservation."""
        assert (
            min_width % downsample_rate == 0 and max_width % downsample_rate == 0
        ), 'min_width and max_width must be multiple of downsample_rate'

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape
        if is_grayscale:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            channels = 1

        content_height = target_height
        content_width = max(int(width * content_height / height), 1)
        total_width = int(np.ceil(content_width / downsample_rate) * downsample_rate)
        content_width += total_width - content_width

        if min_width <= total_width <= max_width:
            canvas = np.zeros((target_height, total_width, channels))
            resized_img = cv2.resize(img, (content_width, content_height))
            if is_grayscale:
                resized_img = np.expand_dims(resized_img, -1)
            canvas[:, :content_width] = resized_img

        elif total_width < min_width:
            total_width = min_width
            canvas = np.zeros((target_height, total_width, channels))
            resized_img = cv2.resize(img, (content_width, content_height))
            if is_grayscale:
                resized_img = np.expand_dims(resized_img, -1)
            canvas[:, :content_width] = resized_img
        else:
            total_width = max_width
            canvas = np.zeros((target_height, total_width, channels))
            content_width = total_width
            content_height = int(content_width / width * height)
            resized_img = cv2.resize(img, (content_width, content_height))
            if is_grayscale:
                resized_img = np.expand_dims(resized_img, -1)

            start_y = (target_height - content_height) // 2
            canvas[start_y : start_y + content_height, :] = resized_img

        return canvas.astype('uint8')

    def _preprocess_batch(
        self,
        images: List[np.ndarray],
        resize_height: int,
        resize_min_width: int,
        channels: int,
        downsample_rate: int,
        resize_max_width: int,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess recognition batch with proper image resizing and padding."""
        assert channels in [1, 3], 'channels must be 1 or 3. Gray or BGR'

        processed_images = []
        image_shapes = []
        max_width = 0
        is_grayscale = channels == 1
        for img in images:
            resized_img = self._resize_image(
                img,
                target_height=resize_height,
                min_width=resize_min_width,
                max_width=resize_max_width,
                is_grayscale=is_grayscale,
                downsample_rate=downsample_rate,
            )
            processed_images.append(resized_img / 255.0)
            image_shapes.append((resized_img.shape[0], resized_img.shape[1]))
            max_width = max(max_width, resized_img.shape[1])

        padded_images = np.array([self._pad_image_to_width(im, max_width) for im in processed_images], dtype=np.float32)
        image_shapes = np.asarray(image_shapes, np.int32)
        padded_images = np.transpose(padded_images, [0, 3, 1, 2])

        return padded_images, image_shapes

    def __call__(self, images: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """Main preprocessing method for text recognition."""
        return self._preprocess_batch(
            images,
            self.image_height,
            self.min_width,
            self.channels,
            self.downsample_rate,
            self.max_img_side,
        )


class Postprocess:
    def __init__(self, cfg: Dict[str, Any]):
        self.chars = cfg['charset']
        self.eos_id = self.chars.index("[EOS]")

    def __call__(self, outputs: np.ndarray) -> List[str]:
        results = []
        for output_indices, output_log_probs in zip(*outputs):
            max_idx = np.argmax(output_log_probs)
            output_indices = output_indices[max_idx]
            output_log_probs = output_log_probs[max_idx]
            decoded_chars = [self.chars[int(idx)] for idx in output_indices]
            if self.eos_id in output_indices:
                selected_idx = np.where(output_indices == self.eos_id)[0][0]
            else:
                selected_idx = len(decoded_chars)
            text = "".join(decoded_chars[:selected_idx])
            score = self._convert_score(output_log_probs)
            results.append((text, score))
        return results

    def _convert_score(self, score: np.ndarray) -> float:
        return float(np.exp(score))


class ImageSegmenter:
    def __init__(self):
        self.stride = 1
        self.window_size = 3
        self.unit = 800
        self.h = 32
        self.n = 100

    def _get_patches(self, img: np.ndarray) -> List[np.ndarray]:
        h, w, _ = img.shape
        resized_w = int(w * self.h / h)
        if resized_w <= self.unit:
            return [img]

        resized_im = cv2.resize(img, (resized_w, self.h))
        gray_im = cv2.cvtColor(resized_im, cv2.COLOR_BGR2GRAY)
        norm_gray_im = cv2.normalize(gray_im, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

        seg_width = self.unit - self.n
        if seg_width >= resized_w:
            return [img]

        patch_points = [0]
        s = self.window_size // 2
        e = self.window_size - s
        for start in range(seg_width, resized_w, seg_width):
            end = min(start + self.n, resized_w)
            interval_stds = [
                (x, np.std(norm_gray_im[:, x - s : x + e])) for x in range(start, end - self.window_size, self.stride)
            ]
            if not interval_stds:
                patch_points.append(resized_w)
                break
            min_std_x = min(interval_stds, key=lambda x: x[1])[0]
            if resized_w - min_std_x < 50:
                patch_points.append(resized_w)
                break
            else:
                patch_points.append(min_std_x)

        if not patch_points or patch_points[-1] < resized_w:
            patch_points.append(resized_w)

        patches = [resized_im[:, start:end, :] for start, end in zip(patch_points, patch_points[1:])]

        return patches

    def __call__(self, image_list: List[np.ndarray]) -> Tuple[List[int], List[np.ndarray]]:
        segments = [(i, patch) for i, img in enumerate(image_list) for patch in self._get_patches(img)]
        return list(zip(*segments)) if segments else (tuple(), tuple())

    def postprocess(self, groups: List[int], rec_res: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        group_dict = defaultdict(list)
        for group_id, (text, score) in zip(groups, rec_res):
            group_dict[group_id].append((text, score))
        merged_result = []
        for group_id in sorted(group_dict.keys()):
            texts, scores = zip(*group_dict[group_id])
            if any(self.is_chinese(t) for t in texts):
                merged_text = ''.join(texts)
            else:
                merged_text = ' '.join(texts)
            avg_score = sum(scores) / len(scores)
            merged_result.append((merged_text, avg_score))

        return merged_result

    @staticmethod
    def is_chinese(label: str) -> bool:
        for char in label:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False


class TextRecognizer:
    def __init__(self, cfg: Dict[str, Any]):
        # self.session = get_engine(cfg.engine_type)(cfg)
        self.session = ORTSeq2Seq(cfg)
        cfg['charset'] = self.session.vocab
        self.use_beam_search = cfg.get('use_beam_search', False)

        self.preprocess = Preprocess(cfg)
        self.postprocess = Postprocess(cfg)
        self.segmenter = ImageSegmenter()

        self.rec_batch_num = cfg.rec_batch_num
        self.rec_image_shape = cfg.rec_img_shape

    def __call__(self, args: TextRecInput) -> TextRecOutput:
        img_list = [args.img] if isinstance(args.img, np.ndarray) else args.img
        groups, img_list = self.segmenter(img_list)

        width_list = [img.shape[1] / float(img.shape[0]) for img in img_list]

        indices = np.argsort(np.array(width_list))
        rec_res = [("", 0.0)] * len(img_list)

        elapse = 0
        for mini_batch_ids in batched(indices, self.rec_batch_num):
            imgs = [img_list[i] for i in mini_batch_ids]
            images, image_shape = self.preprocess(imgs)
            start_time = time.perf_counter()
            outputs = self.session.run([images, image_shape], beam_size=1 if not self.use_beam_search else 5)
            elapse += time.perf_counter() - start_time
            post_res = self.postprocess(outputs)
            logger.info(f"post_res: {post_res}")

            for i, j in enumerate(mini_batch_ids):
                rec_res[j] = post_res[i]

        if groups:
            rec_res = self.segmenter.postprocess(groups, rec_res)

        txts, scores = list(zip(*rec_res))

        return TextRecOutput(
            imgs=imgs,
            txts=txts,
            scores=scores,
            elapse=elapse,
        )

    def load_charset(self, charset_path: str) -> List[str]:
        with open(charset_path) as f:
            chars = ['[PAD]', '[EOS]', '[UNK]', ' '] + [line.strip() for line in f if line.strip() != '']
        return chars
