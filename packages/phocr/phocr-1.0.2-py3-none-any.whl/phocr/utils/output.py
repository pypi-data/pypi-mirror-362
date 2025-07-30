from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union

import numpy as np

from .logger import Logger
from .to_markdown import ToMarkdown
from .utils import save_img
from .vis_res import VisRes

logger = Logger(logger_name=__name__).get_log()


@dataclass
class PHOCROutput:
    img: Optional[np.ndarray] = None
    boxes: Optional[np.ndarray] = None
    txts: Optional[Tuple[str]] = None
    scores: Optional[Tuple[float]] = None
    elapse_list: List[Union[float, None]] = field(default_factory=list)
    elapse: float = field(init=False)
    lang_type: Optional[str] = None

    def __post_init__(self):
        self.elapse = sum(v for v in self.elapse_list if isinstance(v, float))

    def __len__(self):
        if self.txts is None:
            return 0
        return len(self.txts)

    def to_json(self):
        pass

    def to_markdown(self) -> str:
        return ToMarkdown.to(self.boxes, self.txts)

    def vis(self, save_path: Optional[str] = None, font_path: Optional[str] = None):
        if self.img is None or self.boxes is None:
            logger.warning("No image or boxes to visualize.")
            return

        vis = VisRes()
        vis_img = vis(
            self.img,
            self.boxes,
            self.txts,
            self.scores,
            font_path=font_path,
            lang_type=self.lang_type,
        )

        if save_path is not None:
            save_img(save_path, vis_img)
            logger.info("Visualization saved as %s", save_path)
        return vis_img
