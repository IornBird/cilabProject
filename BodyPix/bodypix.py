# https://github.com/de-code/python-tf-bodypix/

import tensorflow as tf
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths
import cv2
import numpy as np


def test_bodypix_cv2():
    print('Start testing BodyPix...')
    print(BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16)
    bodypix_model = load_model(download_model(
        BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16))

    output_dir = './output/'
    ip = '140.115.136.175'
    port = '8080'
    https_url = f"https://{ip}:{port}/video"
    cap = cv2.VideoCapture(https_url)
    while cap.isOpened():
        ret, frame = cap.read()

        # BodyPix Segmentation
        result = bodypix_model.predict_single(frame)
        mask = result.get_mask(threshold=0.5).numpy().astype(np.uint8)
        # masked_image = cv2.bitwise_and(frame, frame, mask=mask) # background removed
        seg = result.get_colored_part_mask(mask)

        tf.keras.preprocessing.image.save_img(
            output_dir+f"output-colored-mask.jpg",
            seg
        )

        cv2.imshow('BodyPix', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Done testing BodyPix...')

def test_bodypix_image():
    print('Start testing BodyPix...')
    print(BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16)
    bodypix_model = load_model(download_model(
        BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16))

    output_dir = './output/'
    frame = cv2.imread(fr"D:\NCU\Special_Project\Taekwondo_media\video\vid2img\313 R16 M +80kg CHN MENG M CRO SAPINA I\video-7m53s-2-x3htXTI7nDI\original\0017.png")
    # BodyPix Segmentation
    result = bodypix_model.predict_single(frame)
    mask = result.get_mask(threshold=0.5).numpy().astype(np.uint8)
    # masked_image = cv2.bitwise_and(frame, frame, mask=mask) # background removed
    seg = result.get_colored_part_mask(mask)

    tf.keras.preprocessing.image.save_img(
        output_dir+f"output-colored-mask.jpg",
        seg
    )

    cv2.imshow('BodyPix', frame)
    cv2.imshow('BodyPix Segmentation', seg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('Done testing BodyPix...')


if __name__ == '__main__':
    test_bodypix_image()



