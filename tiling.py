import os
from typing import LiteralString
import tensorflow as tf


def read_image(filename):
    img = tf.io.read_file(filename)
    name, ext = os.path.splitext(filename)
    if ext == 'dis.bmp':
        img = tf.image.decode_bmp(img, channels=3)
    else:
        img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return img


def tile_image(full_img, filename, image, channels=3, tile_ht=400, tile_wd=400):
    tiles = tile(full_img, channels, tile_ht, tile_wd)
    no_rows = tiles.shape[0]
    no_cols = tiles.shape[1]
    path = save(tiles, filename, image)
    return path, no_rows, no_cols


def tile(full_img, channels=3, tile_ht=400, tile_wd=400):
    images = tf.expand_dims(full_img, axis=0)
    tiles = tf.image.extract_patches(
        images=images,
        sizes=[1, tile_ht, tile_wd, 1],
        strides=[1, tile_ht, tile_wd, 1],
        rates=[1, 1, 1, 1],
        padding='VALID')

    tiles = tf.squeeze(tiles, axis=0)
    no_rows = tiles.shape[0]
    no_cols = tiles.shape[1]
    tiles = tf.reshape(tiles, [no_rows, no_cols, tile_ht, tile_wd, channels])
    return tiles


def save(tiles, image_file, image) -> LiteralString | str | bytes:
    file_name, file_extension = os.path.splitext(image_file)
    image, ext = os.path.splitext(image)

    path = os.path.join(file_name)
    if not os.path.exists(path):
        os.mkdir(path)

    rows = tiles.shape[0]
    cols = tiles.shape[1]
    for row_no in range(rows):
        for col_no in range(cols):
            img = tiles[row_no][col_no]
            image_path = os.path.join(file_name, image + "_" + str(row_no) + "_" + str(col_no) + '.jpg')
            tf.keras.utils.save_img(
                image_path, img
            )

    return path
