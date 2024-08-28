import os

import cv2
from PIL import Image
import torch
import torch.nn as nn
from torchvision.transforms import v2
import configparser
import tensorflow as tf

from Defect import get_classes
from augmentation import merge
from logging_defects import log_prediction
from tiling import tile

config = configparser.ConfigParser()
config.read('config.ini')

classes = get_classes()

images_reference_list = []
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def get_model():
    model = torch.hub.load('pytorch/vision:v0.18.1', 'inception_v3', weights='Inception_V3_Weights.DEFAULT')
    model.aux_logits = False
    model = model.to(device)
    model.fc = nn.Linear(model.fc.in_features, 6)
    model_state_dict = config['DATASET']['model_net_state_dict']
    state_dict = torch.load(model_state_dict, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()

    return model


m = get_model()


def transform_image(img1, path=True):
    my_transforms = v2.Compose([
        v2.Resize((299, 299)),
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale=True),
        v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(img1).convert('RGB') if path else img1
    return my_transforms(image).unsqueeze(0)


def get_prediction(image, path=True):
    tensor = transform_image(image, path)
    tensor = tensor.to(device)
    with torch.no_grad():
        outputs = m(tensor)
        _, predicted = torch.max(outputs, 1)

    defect = next((x for x in classes if x['num'] == predicted[0]), None)
    return defect


def save_image(image_file):
    image_path = "./images/" + image_file.filename
    image_file.save(image_path)
    return image_path


def extract_patch(image_path):
    file_name, file_extension = os.path.splitext(image_path)
    img_name1, ext1 = os.path.splitext(file_name)

    roi_width, roi_height = 400, 400
    slide_x, slide_y = 280, 280

    image = cv2.imread(image_path)
    image_original = image.copy()
    height, width, channels = image.shape

    for roi_x in range(0, width, slide_x):
        for roi_y in range(0, height, slide_y):
            roi = image_original[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
            cropped_width, cropped_height, channel = roi.shape
            if cropped_width < roi_width or cropped_height < roi_height:
                continue

            path = './images/' + str(roi_y) + 'check.png'
            cv2.imwrite(path, roi)

            predicted = get_prediction(path, True)
            if predicted['color'] != 'None':
                cv2.rectangle(image, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height),
                              get_color(predicted["color"]), -1)
            else:
                image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width] = roi

    added_image = cv2.addWeighted(image_original, 0.5, image, 0.5, 0)
    added_image_path = img_name1 + '_predicted.jpg'
    cv2.imwrite(added_image_path, added_image)
    return added_image_path


def tile_and_predict_image(full_img, filename, image):
    return extract_patch(filename)


def tile_and_predict_image1(full_img, filename, image):
    tiles = tile(full_img)

    file_name, file_extension = os.path.splitext(filename)
    image, ext = os.path.splitext(image)

    path = os.path.join(file_name)
    if not os.path.exists(path):
        os.mkdir(path)

    rows = tiles.shape[0]
    cols = tiles.shape[1]
    for row_no in range(rows):
        for col_no in range(cols):
            img = tf.Variable(tiles[row_no][col_no])
            image_path = os.path.join(file_name, image + "_" + str(row_no) + "_" + str(col_no) + '.jpg')
            tf.keras.utils.save_img(
                image_path, img
            )
            predicted = get_prediction(image_path)
            log_prediction(image_path, predicted)
            if predicted['color'] != 'None':
                im = cv2.imread(image_path)
                im = cv2.rectangle(im, (7, 7), (img.shape[0]-7, img.shape[0]-7), get_color(predicted['color']), -1)
                cv2.imwrite(image_path, im)

    image_path = os.path.join(file_name, '*.jpg')
    return merge(image_path, image, rows, cols)


def get_color(color_name):
    colors = {
        "yellow": (0, 255, 255),
        "red": (0, 0, 255),
        "blue": (255, 0, 0),
        "green": (0, 255, 0),
        "orange": (0, 140, 255)
    }

    return colors.get(color_name)
