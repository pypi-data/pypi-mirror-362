# Writer: LauNT - 07/2025 - akaOCR Team

from PIL import Image
import sys
import cv2
import numpy as np


class ToCHWImage:
    # Convert hwc image to chw image

    def __init__(self, **kwargs):
        pass

    def __call__(self, data):

        img = data['image']
        if isinstance(img, Image.Image):
            img = np.array(img)
        data['image'] = img.transpose((2, 0, 1))

        return data


class KeepKeys:
    def __init__(self, keep_keys, **kwargs):
        self.keep_keys = keep_keys

    def __call__(self, data):

        data_list = []
        for key in self.keep_keys:
            data_list.append(data[key])

        return data_list


class NormalizeImage:
    # Normalize image such as substract mean, divide std

    def __init__(self, scale=None, mean=None, std=None, order='chw', **kwargs):
        if isinstance(scale, str):
            scale = eval(scale)
        self.scale = np.float32(scale if scale is not None else 1.0 / 255.0)
        mean = mean if mean is not None else [0.485, 0.456, 0.406]
        std = std if std is not None else [0.229, 0.224, 0.225]

        shape = (3, 1, 1) if order == 'chw' else (1, 1, 3)
        self.mean = np.array(mean).reshape(shape).astype('float32')
        self.std = np.array(std).reshape(shape).astype('float32')

    def __call__(self, data):

        img = data['image']
        if isinstance(img, Image.Image):
            img = np.array(img)
        assert isinstance(
            img, np.ndarray), "invalid input 'img' in NormalizeImage"
        data['image'] = (
            img.astype('float32') * self.scale - self.mean) / self.std
        
        return data


class DetResize:
    def __init__(self, **kwargs):
        super(DetResize, self).__init__()

        self.limit_side_len = kwargs["limit_side_len"]
        self.limit_type = kwargs["limit_type"]

    def __call__(self, data):
        # Resize image to a size multiple of 32

        img = data['image']
        src_h, src_w, _ = img.shape
        if sum([src_h, src_w]) < 64:
            img = self.image_padding(img)

        img, [ratio_h, ratio_w] = self.resize_image(img)
        data['image'] = img
        data['shape'] = np.array([src_h, src_w, ratio_h, ratio_w])

        return data

    def image_padding(self, im, value=0):
        # Padding image with specific value

        h, w, c = im.shape
        im_pad = np.zeros((max(32, h), max(32, w), c), np.uint8) + value
        im_pad[:h, :w, :] = im

        return im_pad
    
    @staticmethod
    def get_ratio(limit_type, h, w, limit_side_len):
        # Get ratio value (for resizing image)

        if limit_type == 'max' and max(h, w) > limit_side_len:
            return float(limit_side_len) / max(h, w)
        if limit_type == 'min' and min(h, w) < limit_side_len:
            return float(limit_side_len) / min(h, w)
        
        return 1.

    def resize_image(self, img):
        """
        Resize image to a size multiple of 32
        Args:
            img(array): array with shape [h, w, c]
        Returns:
            tuple: img, (ratio_h, ratio_w)
        """
        h, w, _ = img.shape

        if self.limit_type not in ['max', 'min']:
            raise ValueError(f'Not support type: {self.limit_type}')
        
        ratio = self.get_ratio(self.limit_type, h, w, self.limit_side_len)
        resize_h = int(h * ratio)
        resize_w = int(w * ratio)

        resize_h = max(int(round(resize_h / 32) * 32), 32)
        resize_w = max(int(round(resize_w / 32) * 32), 32)

        try:
            img = cv2.resize(img, (resize_w, resize_h))
        except Exception as e:
            print(f"Error resizing image: {e}")
            sys.exit(0)

        ratio_h = resize_h / float(h)
        ratio_w = resize_w / float(w)

        return img, [ratio_h, ratio_w]