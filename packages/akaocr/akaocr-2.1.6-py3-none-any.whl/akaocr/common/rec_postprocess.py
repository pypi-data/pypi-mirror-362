# Writer: LauNT - 07/2025 - akaOCR Team

import numpy as np
import os
import math
import cv2

work_dir = os.path.dirname(os.path.realpath(__file__))


class CTCLabelDecode:
    def __init__(self, character_dict_path=None, use_space_char=False):
        # Init vocab & some parameters

        self.beg_str = "sos"
        self.end_str = "eos"
        self.reverse = False
        self.character_str = []

        # get vocab path
        if not character_dict_path or not os.path.exists(character_dict_path):
            character_dict_path = os.path.join(work_dir, '../', "recog/data/vocab.txt")

        # read vocab path
        with open(character_dict_path, "rb") as fin:
            self.character_str = [line.decode('utf-8').strip() for line in fin.readlines()]
    
        # create character dictionary
        if use_space_char:
            self.character_str.append(" ")
        dict_character = list(self.character_str)

        dict_character = self.add_special_char(dict_character)
        self.dict = {char: i for i, char in enumerate(dict_character)}
        self.character = dict_character

    def add_special_char(self, dict_character):
        # Add blank for CTC decode

        return ['blank'] + dict_character

    def decode(self, text_index, text_prob=None, is_remove_duplicate=False):
        # CTC label decode

        result_list = []
        ignored_tokens = [0]
        batch_size = len(text_index)

        for batch_idx in range(batch_size):
            selection = np.ones(len(text_index[batch_idx]), dtype=bool)
            if is_remove_duplicate:
                selection[1:] = text_index[batch_idx][1:] != text_index[batch_idx][:-1]
            for ignored_token in ignored_tokens:
                selection &= text_index[batch_idx] != ignored_token

            char_list = [self.character[text_id] for text_id in text_index[batch_idx][selection]]
            if text_prob is not None:
                conf_list = text_prob[batch_idx][selection]
            else:
                conf_list = np.ones(len(selection))
            if len(conf_list) == 0:
                conf_list = np.array([0])
            text = ''.join(char_list)
            result_list.append((text, np.mean(conf_list).tolist()))

        return result_list

    def __call__(self, preds, label=None, *args, **kwargs):
        # Convert between text-label and text-index

        if isinstance(preds, (tuple, list)):
            preds = preds[-1]
        preds_idx = preds.argmax(axis=2)
        preds_prob = preds.max(axis=2)
        text = self.decode(preds_idx, preds_prob, is_remove_duplicate=True)
        if label is None:
            return text
        label = self.decode(self.character, label)
        
        return text, label
    

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
