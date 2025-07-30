# Writer: LauNT - 07/2025 - akaOCR Team

import traceback
from akaocr.rotate.center import Classifier


class ClsEngine:
    def __init__(self, model_path=None, conf_thres=0.75, device='cpu') -> None:
        self.text_rotator = Classifier(model_path, conf_thres, device)

    def __call__(self, image) -> tuple:
        # Get rotation angle of cropped text image or images

        rot_res = None
        try:
            if isinstance(image, list):
                rot_res = self.text_rotator(image)
            else:    
                rot_res = self.text_rotator([image])
        except Exception:
            print(traceback.format_exc())

        return rot_res
