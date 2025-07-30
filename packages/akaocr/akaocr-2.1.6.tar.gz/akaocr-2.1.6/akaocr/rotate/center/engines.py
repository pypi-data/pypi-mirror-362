# Writer: LauNT - 07/2025 - akaOCR Team

import numpy as np
import math
import cv2, os

from akaocr.common import create_predictor
from akaocr.common import build_post_process

work_dir = os.path.dirname(os.path.realpath(__file__))


class Classifier:
    def __init__(self, model_path=None, conf_thres=0.75, device='cpu'):
        # Initialize some parameters
        
        self.cls_image_shape = [3, 48, 192]
        self.cls_batch_num = 32
        self.cls_thresh = conf_thres
        self.postprocess_op = build_post_process(
            {'name': 'ClsPostProcess', 'label_list': ['0', '180']})

        self.predictor, self.input_tensor, self.output_tensors = create_predictor(
            model_path=self.update_path(model_path), device=device)

    @staticmethod
    def resize_image(image, img_c, img_h, img_w):
        # Resize image without distortion
        
        h = image.shape[0]; w = image.shape[1]
        ratio = w / float(h)
        if math.ceil(img_h * ratio) > img_w:
            resized_w = img_w
        else:
            resized_w = int(math.ceil(img_h * ratio))
        resized_image = cv2.resize(image, (resized_w, img_h))
        resized_image = resized_image.astype('float32')
        resized_image = resized_image.transpose((2, 0, 1)) / 255
        resized_image -= 0.5
        resized_image /= 0.5
        padding_im = np.zeros((img_c, img_h, img_w), dtype=np.float32)
        padding_im[:, :, 0:resized_w] = resized_image

        return padding_im
    
    @staticmethod
    def update_path(model_path):
        # Update model path if model_path is not exist

        if not model_path or not os.path.exists(model_path):
            model_path = os.path.join(work_dir, '../data/model.onnx')

        return model_path

    def __call__(self, img_list):
        # calculate the aspect ratio of all text bars
        img_num = len(img_list)
        width_list = np.array([img.shape[1] / float(img.shape[0]) for img in img_list])

        # sorting can speed up the classification process
        indices = np.argsort(width_list)
        cls_res = [['', 0.0]] * img_num
        batch_num = self.cls_batch_num

        for beg_img_no in range(0, img_num, batch_num):
            end_img_no = min(img_num, beg_img_no + batch_num)
            norm_img_batch = []

            # create a batch of images
            for ino in range(beg_img_no, end_img_no):
                norm_img = self.resize_image(img_list[indices[ino]], *self.cls_image_shape)
                norm_img_batch.append(norm_img[np.newaxis, :])

            norm_img_batch = np.concatenate(norm_img_batch)
            norm_img_batch = norm_img_batch.copy()

            # infer with batch
            input_dict = {self.input_tensor.name: norm_img_batch}
            outputs = self.predictor.run(self.output_tensors, input_dict)
            preds = outputs[0]

            cls_result = self.postprocess_op(preds)
            for rno in range(len(cls_result)):
                cls_res[indices[beg_img_no + rno]] = cls_result[rno]

        return cls_res
