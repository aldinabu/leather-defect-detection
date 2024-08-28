import configparser
import glob
import os

import tensorflow as tf
from tiling import read_image
import json

config = configparser.ConfigParser()
config.read('config.ini')


def save_image(image_to_save, augmented_file_name, img_name):
    image_path = os.path.join(augmented_file_name, img_name + '.jpg')
    tf.keras.utils.save_img(image_path, image_to_save)


def process(image, path_to_save, img_name):
    image = tf.image.adjust_brightness(image, 0.8)
    flipped = tf.image.flip_left_right(image)
    saturated = tf.image.adjust_brightness(image, 0.3)
    bright = tf.image.flip_up_down(image)
    # hue = tf.image.adjust_hue(image, 0.3)
    random_hue = tf.image.random_hue(image, 0.5)
    flipped_saturated = tf.image.adjust_saturation(flipped, 1)
    rotated = tf.image.rot90(image)
    #for i in range(3):
     #   seed = (i, 0)
     #   stateless_random_brightness = tf.image.stateless_random_hue(image, max_delta=0.5, seed=seed)
     #   save_image(stateless_random_brightness, path_to_save, img_name + '_random_hue_' + str(i))

    #save_image(flipped, path_to_save, img_name + '_flipped')
    #save_image(flipped_saturated, path_to_save, img_name + '_flipped_saturated')
    save_image(saturated, path_to_save, img_name + '_saturated')
    #save_image(hue, path_to_save, img_name + '_quality')
    #save_image(random_hue, path_to_save, img_name + '_random_hue')
    #save_image(bright, path_to_save, img_name + '_flipped_up_down')
    #save_image(rotated, path_to_save, img_name + '_rotated')


def data_augmentation(path_or, path_for_saving):
    images = [[read_image(file), file] for file in glob.glob(path_or)]
    for img in images:
        file_path = img[1]
        file_name = os.path.basename(file_path)
        file = os.path.splitext(file_name)

        process(img[0], path_for_saving, file[0])


def get_classes():
    with open("defect.json") as jsonfile:
        defect_dict = json.load(jsonfile)
        print(len(defect_dict['defects']))


def read(filename):
    img = tf.io.read_file(filename)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return img


def merge(path, image_name, rows, cols):
    images = [[read(file), file] for file in glob.glob(path)]
    stacked_hori = images[0][0]
    stacked_vert = images[0][0]
    i = 0

    for r in range(rows):
        for c in range(cols):
            if c == 0:
                stacked_hori = images[i][0]
                i = i+1
                continue
            stacked_hori = tf.concat((stacked_hori, images[i][0]), axis=1)
            i = i+1

        if r == 0:
            stacked_vert = stacked_hori
            stacked_hori = []
        else:
            stacked_vert = tf.concat((stacked_vert, stacked_hori), axis=0)
            stacked_hori = []

    print('Image merged back successfully!')

    merged_img_path = './images/' + image_name + '.jpg'
    tf.keras.utils.save_img(
        merged_img_path, stacked_vert
    )

    return merged_img_path


def merge_tiles(tiles, img_path):

    rows = tiles.shape[0]
    cols = tiles.shape[1]

    images = tiles
    stacked_hori = images[0][0]
    stacked_vert = images[0][0]

    for r in range(rows):
        for c in range(cols):
            img = images[r][c]
            if c == 0:
                stacked_hori = img
                continue
            stacked_hori = tf.concat((stacked_hori, img), axis=1)

        if r == 0:
            stacked_vert = stacked_hori
            stacked_hori = []
        else:
            stacked_vert = tf.concat((stacked_vert, stacked_hori), axis=0)
            stacked_hori = []

    tf.keras.utils.save_img(
        img_path, stacked_vert
    )
    print('Image merged back successfully!')

