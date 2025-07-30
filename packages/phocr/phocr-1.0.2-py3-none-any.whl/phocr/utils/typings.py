from enum import Enum


class LangDet(Enum):
    CH = "ch"
    EN = "en"
    MULTI = "multi"


class LangCls(Enum):
    CH = "ch"


class LangRec(Enum):
    CH = "ch"
    EN = "en"
    JP = "jp"
    KO = "ko"
    RU = "ru"


class OCRVersion(Enum):
    PPOCRV4 = "PP-OCRv4"
    PPOCRV5 = "PP-OCRv5"
    PH_OCRV1 = "PH-OCRv1"


class EngineType(Enum):
    ONNXRUNTIME = "onnxruntime"
    # OPENVINO = "openvino"
    # PADDLE = "paddle"
    # TORCH = "torch"


class ModelType(Enum):
    MOBILE = "mobile"
    SERVER = "server"
    NONE = "none"


class TaskType(Enum):
    DET = "det"
    CLS = "cls"
    REC = "rec"
