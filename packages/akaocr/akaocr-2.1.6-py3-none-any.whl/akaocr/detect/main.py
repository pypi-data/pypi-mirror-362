# Writer: LauNT - 07/2025 - akaOCR Team

import traceback, os
from akaocr.detect.center.engines import Detector

work_dir = os.path.dirname(os.path.realpath(__file__))


class BoxEngine:
    def __init__(self, model_path=None, 
                 side_len=960, 
                 conf_thres=0.5, 
                 mask_thes=0.4,
                 unclip_ratio=2.0,
                 max_candidates=1000,
                 device='cpu'):
        # Init some parameters

        self.text_detector = Detector(
            model_path, side_len, 
            conf_thres, mask_thes, 
            unclip_ratio, 
            max_candidates, device)

    def __call__(self, image):
        # Text Detection Pipeline
        
        det_res = None
        try:
            det_res = self.text_detector(image)
        except Exception:
            print(traceback.format_exc())

        return det_res
