# Writer: LauNT - 07/2025 - akaOCR Team

import numpy as np
import pyclipper
import cv2

from shapely.geometry import Polygon
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


class DetPostProcess:
    """
    Post-processing for Differentiable Binarization (DB).
    Args:
        thresh: Threshold for binarization.
        box_thresh: Threshold for box scoring.
        max_candidates: Maximum number of candidates.
        unclip_ratio: Ratio for expanding the boxes.
        min_size: Minimum size of the box.
    """
    def __init__(self, thresh=0.25, box_thresh=0.5, max_candidates=1000, unclip_ratio=1.5, **kwargs):
        self.thresh = thresh
        self.box_thresh = box_thresh
        self.max_candidates = max_candidates
        self.unclip_ratio = unclip_ratio
        self.min_size = 3
        
    def process_contour(self, contour, pred, width, height, dest_width, dest_height):
        # Convert contour to bounding box
        
        try:
            points, sside = self.get_mini_boxes(contour)
            if sside < self.min_size:
                return None

            score = self.box_score(pred, contour)
            if self.box_thresh > score:
                return None

            box = self.unclip(points, self.unclip_ratio).reshape(-1, 1, 2)
            if len(box) == 0:
                return None

            box, sside = self.get_mini_boxes(box)
            if sside < self.min_size + 2:
                return None

            box[:, 0] = np.clip(np.round(box[:, 0] / width * dest_width), 0, dest_width)
            box[:, 1] = np.clip(np.round(box[:, 1] / height * dest_height), 0, dest_height)
            
            return box.astype("int32")
        except Exception:
            return None
    
    def boxes_from_bitmap(self, pred, bitmap, dest_width, dest_height):
        # Generate boxes from the bitmap.
        
        height, width = bitmap.shape
        contours, _ = cv2.findContours((bitmap * 255).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        num_contours = min(len(contours), self.max_candidates)

        boxes = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(self.process_contour, contours[i], pred, width, height, dest_width, dest_height) 
                for i in range(num_contours)
            ]
            for future in as_completed(futures):
                box = future.result()
                if box is not None:
                    boxes.append(box)

        return np.array(boxes, dtype=np.float32)

    def unclip(self, box, unclip_ratio):
        """
        Unclip a box with a given ratio.
        Args:
            box: Input box points.
            unclip_ratio: Ratio for unclipping.
        Returns:
            Expanded box points.
        """
        try:
            poly = Polygon(box)
            distance = poly.area * unclip_ratio / poly.length
            offset = pyclipper.PyclipperOffset()
            offset.AddPath(box, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
            expanded = np.array(offset.Execute(distance))
            if len(expanded) == 0:
                return box
            return expanded
        except Exception as e:
            print(f"Error unclipping box: {e}")
            return box

    def get_mini_boxes(self, contour):
        # Get minimum bounding boxes from contour.

        bounding_box = cv2.minAreaRect(contour)
        points = cv2.boxPoints(bounding_box)
        points = sorted(points, key=lambda x: x[0])

        if points[1][1] > points[0][1]:
            index_1, index_4 = 0, 1
        else:
            index_1, index_4 = 1, 0

        if points[3][1] > points[2][1]:
            index_2, index_3 = 2, 3
        else:
            index_2, index_3 = 3, 2
        box = [points[index_1], points[index_2], points[index_3], points[index_4]]
        
        return np.array(box), min(bounding_box[1])  # minimum side length

    def box_score(self, bitmap, contour):
        # Calculate the score of the box.

        h, w = bitmap.shape[:2]
        contour = np.reshape(contour, (-1, 2))

        xmin = np.clip(np.min(contour[:, 0]), 0, w - 1)
        xmax = np.clip(np.max(contour[:, 0]), 0, w - 1)
        ymin = np.clip(np.min(contour[:, 1]), 0, h - 1)
        ymax = np.clip(np.max(contour[:, 1]), 0, h - 1)

        mask = np.zeros((ymax - ymin + 1, xmax - xmin + 1), dtype=np.uint8)
        contour[:, 0] -= xmin
        contour[:, 1] -= ymin
        cv2.fillPoly(mask, [contour.astype("int32")], 1)

        return cv2.mean(bitmap[ymin:ymax + 1, xmin:xmax + 1], mask)[0]

    def __call__(self, outs_dict, shape_list):
        # Generate bounding boxes from the prediction map.
        
        pred = outs_dict['maps']
        pred = pred[:, 0, :, :]
        segmentation = pred > self.thresh
        src_h, src_w = shape_list[0][:2]
        mask = segmentation[0]
        boxes = self.boxes_from_bitmap(pred[0], mask, src_w, src_h)
        
        return boxes
