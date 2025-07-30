# Writer: LauNT - 07/2025 - akaOCR Team

import os
import numpy as np
import math
import cv2

from akaocr.common import create_predictor
from akaocr.common import build_post_process


SUPPORTED_LANG = ['eng']
work_dir = os.path.dirname(os.path.realpath(__file__))


class Recognitor:
    def __init__(self, model_path=None, 
                vocab_path=None, 
                use_space_char=True,
                batch_sizes=32,
                model_shape=None, 
                max_wh_ratio=None,
                device='cpu'):

        # init parameters
        self.rec_image_shape = model_shape
        self.max_wh_ratio = max_wh_ratio
        self.model_path = model_path
        self.vocab_path = vocab_path
        self.use_space_char = use_space_char
        self.rec_batch_num = batch_sizes
        self.predictor, self.input_tensor, self.output_tensors = create_predictor(
            model_path=self.update_path(model_path), device=device)

        # for post-processing
        postprocess_params = {
            'name': 'CTCLabelDecode',
            "character_dict_path": self.vocab_path,
            "use_space_char": self.use_space_char
        }
        self.postprocess_op = build_post_process(postprocess_params)

    @staticmethod
    def update_path(model_path):
        # Update model path if model_path is not exist

        if not model_path or not os.path.exists(model_path):
            model_path = os.path.join(work_dir, '../data/model.onnx')

        return model_path

    def __call__(self, img_list):
        """Text recognition pipeline (supported for English)
        Args:
            org_img_list (list): list of images
        Returns:
            list(tuple): (text, text confidence)
        """
        # calculate the aspect ratio of all text bars
        img_num = len(img_list)
        width_list = []
        for img in img_list:
            width_list.append(img.shape[1] / float(img.shape[0]))

        # sorting can speed up the recognition process
        indices = np.argsort(np.array(width_list))
        rec_res = [['', 0.0]] * img_num
        batch_num = self.rec_batch_num
        _, img_h, img_w = self.rec_image_shape[:3]

        for beg_img_no in range(0, img_num, batch_num):
            end_img_no = min(img_num, beg_img_no + batch_num)
            norm_img_batch = []
            max_wh_ratio = img_w / img_h

            # calculate max_wh_ratio of batch
            for ino in range(beg_img_no, end_img_no):
                h, w = img_list[indices[ino]].shape[0:2]
                wh_ratio = w * 1.0 / h
                max_wh_ratio = max(max_wh_ratio, wh_ratio)

            # update max_ratio
            if self.max_wh_ratio is not None:
                max_wh_ratio = min(10, self.max_wh_ratio)

            # create a batch of images
            for ino in range(beg_img_no, end_img_no):
                norm_img = self.resize_image(
                    img_list[indices[ino]],
                    self.rec_image_shape,
                    max_wh_ratio)
                norm_img = norm_img[np.newaxis, :]
                norm_img_batch.append(norm_img)
               
            norm_img_batch = np.concatenate(norm_img_batch)
            norm_img_batch = norm_img_batch.copy()

            # infder with batch
            input_dict = {}
            input_dict[self.input_tensor.name] = norm_img_batch
            outputs = self.predictor.run(self.output_tensors, input_dict)
            preds = outputs[0]
                
            rec_result = self.postprocess_op(preds)
            for rno in range(len(rec_result)):
                rec_res[indices[beg_img_no + rno]] = rec_result[rno]

        return rec_res
    
    @staticmethod
    def resize_image(image, image_shape, max_ratio):
        """Resize image without distortion

        Args:
            image (array): color image, read by opencv
            image_shape (list): desired image shape
            max_ratio (float)): max ratio in a batch of images

        Returns:
            array: resized image
        """
        h, w = image.shape[0], image.shape[1]
        img_c, img_h, img_w = image_shape
        current_ratio = w * 1.0 / h

        # get resized width
        img_w = int(img_h * max_ratio)
        if math.ceil(img_h * current_ratio) > img_w: resized_w = img_w
        else: resized_w = int(math.ceil(img_h * current_ratio))
        
        # resize image
        resized_image = cv2.resize(image, (resized_w, img_h))
        resized_image = resized_image.astype('float32')

        # normalize image
        resized_image = resized_image.transpose((2, 0, 1))/255
        resized_image -= 0.5
        resized_image /= 0.5
        padding_im = np.zeros((img_c, img_h, img_w), dtype=np.float32)
        padding_im[:, :, :resized_w] = resized_image

        return padding_im
