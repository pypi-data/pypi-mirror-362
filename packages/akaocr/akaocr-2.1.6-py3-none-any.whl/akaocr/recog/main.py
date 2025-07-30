# Writer: LauNT - 07/2025 - akaOCR Team

import traceback
from akaocr.recog.center import Recognitor


class TextEngine:
    def __init__(self, model_path=None,
                vocab_path=None, 
                use_space_char=True,
                batch_sizes=32,
                model_shape=[3, 48, 320],
                max_wh_ratio=None,
                device='cpu') -> None:
        
        self.text_recognizer = Recognitor(
            model_path, vocab_path, 
            use_space_char, batch_sizes, model_shape, 
            max_wh_ratio, device)

    def __call__(self, image):
        # Text recogntion pipeline

        rec_res = None
        try:
            if isinstance(image, list):
                rec_res = self.text_recognizer(image)
            else:    
                rec_res = self.text_recognizer([image])
        except Exception:
            print(traceback.format_exc())

        return rec_res
