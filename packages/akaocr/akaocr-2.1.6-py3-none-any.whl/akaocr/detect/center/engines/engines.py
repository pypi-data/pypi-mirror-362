# Writer: LauNT - 07/2025 - akaOCR Team

import numpy as np
import os

from akaocr.detect.center.data import create_operators
from akaocr.detect.center.data import transform
from concurrent.futures import ThreadPoolExecutor

from akaocr.common import create_predictor
from akaocr.common import build_post_process

work_dir = os.path.dirname(os.path.realpath(__file__))


class Detector:
    def __init__(self, model_path=None, 
                 side_len=960, 
                 conf_thres=0.5, 
                 mask_thes=0.4,
                 unclip_ratio=2.0,
                 max_candidates=1000,
                 device='cpu'):
        # Initialize parameters
        self.conf_thres = conf_thres
        self.output_tensors = None

        # build pre-processing operations
        pre_process_list = [
            {'DetResize': {'limit_side_len': side_len, 'limit_type': 'min'}}, 
            {'NormalizeImage': {'std': [0.229, 0.224, 0.225], 
                                'mean': [0.485, 0.456, 0.406], 
                                'scale': '1./255.', 'order': 'hwc'}},
            {'ToCHWImage': None}, 
            {'KeepKeys': {'keep_keys': ['image', 'shape']}}
        ]
        self.preprocess_op = create_operators(pre_process_list)

        # build post-processing operations
        postprocess_params = {
            'name': 'DetPostProcess',
            'thresh': mask_thes,
            'box_thresh': conf_thres,
            'max_candidates': max_candidates,
            'unclip_ratio': unclip_ratio,
            'use_dilation': False
        }
        self.postprocess_op = build_post_process(postprocess_params)

        # create predictor
        self.predictor, self.input_tensor, _ = create_predictor(
            model_path=self.update_path(model_path), device=device)

    @staticmethod
    def update_path(model_path):
        # Update model path if model_path is not exist

        if not model_path or not os.path.exists(model_path):
            model_path = os.path.join(work_dir, '../../data/model.onnx')

        return model_path

    def order_points_clockwise(self, pts):
        # Order points clockwise

        center = np.mean(pts, axis=0)
        
        # calculate the angle of each point from the centroid
        angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
        
        # sort the points based on the angles
        ordered_indices = np.argsort(angles)
        rect = pts[ordered_indices]
 
        return rect

    def clip_det_res(self, points, img_height, img_width):
        # Clip detection results

        for pno in range(points.shape[0]):
            points[pno, 0] = int(min(max(points[pno, 0], 0), img_width - 1))
            points[pno, 1] = int(min(max(points[pno, 1], 0), img_height - 1))

        return points

    def filter_det_res(self, dt_boxes, image_shape):
        # Filter tag detection results

        img_height, img_width = image_shape[0:2]

        def process_box(box):
            box = self.order_points_clockwise(box)
            box = self.clip_det_res(box, img_height, img_width)
            
            rect_width = int(np.linalg.norm(box[0] - box[1]))
            rect_height = int(np.linalg.norm(box[0] - box[3]))
            if rect_width <= 3 or rect_height <= 3:
                return None
            return box

        dt_boxes_new = []
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = executor.map(process_box, dt_boxes)
        
        for result in results:
            if result is not None:
                dt_boxes_new.append(result)
        
        return dt_boxes_new

    def __call__(self, ori_image):
        # Inference for text detection

        image = ori_image.copy()
        data = {'image': image}

        # transform image
        image, shape_list = transform(data, self.preprocess_op)
        image = np.expand_dims(image, axis=0)
        shape_list = np.expand_dims(shape_list, axis=0)

        # inference model
        input_dict = {}
        input_dict[self.input_tensor.name] = image
        outputs = self.predictor.run(self.output_tensors, input_dict)
       
        # post-processing
        preds = dict()
        preds['maps'] = outputs[0]
        dt_boxes = self.postprocess_op(preds, shape_list)
        dt_boxes = self.filter_det_res(dt_boxes, ori_image.shape)
      
        return dt_boxes
