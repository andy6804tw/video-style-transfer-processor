#!/usr/bin/env python
# coding: utf-8
# import os 
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import numpy as np
import imageio
import tensorflow_hub as hub


# gpus = tf.config.experimental.list_physical_devices('GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)

# load TF Hub Fast Style Transfer model
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')


# 將 tensor 轉換成圖片矩陣
def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return tensor

def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

def process_img(img):
    max_dim = 512
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

# def predict():
#     # load style image
#     style_image = load_img('app/demo/style1.png')
#     # load video
#     reader = imageio.get_reader('app/demo/test.MOV')
#     # get video fps
#     fps = reader.get_meta_data()['fps']
#     writer = imageio.get_writer('app/static/output.mp4', fps=fps)

#     for im in reader:
#         im = np.array(im, dtype='f')/255
#         img = process_img(im)
#         stylized_image = hub_model(tf.constant(img), tf.constant(style_image))[0]
#         result = tensor_to_image(stylized_image)
#         writer.append_data(result)
#     writer.close()

def predict(styleImage='', reader=''):
    if(styleImage=='' and reader==''):
        print('--API unit test for GET Router--')
        # load style image
        style_image = load_img('app/demo/style1.png')
        # load video
        reader = imageio.get_reader('app/demo/test.MOV')
    else:
        # load style image
        style_image = np.array(styleImage, dtype='f')/255
        style_image = process_img(style_image)
    # get video fps
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer('app/static/output.mp4', fps=fps)

    for im in reader:
        im = np.array(im, dtype='f')/255
        img = process_img(im)
        stylized_image = hub_model(tf.constant(img), tf.constant(style_image))[0]
        result = tensor_to_image(stylized_image)
        writer.append_data(result)
    writer.close()
    print('ok')




