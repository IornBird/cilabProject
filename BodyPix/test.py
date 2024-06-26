import tensorflow as tf
import cv2
import numpy as np

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def overlay_transparent(background_path, overlay_path, x, y):
    background = cv2.imread(background_path, -1)
    overlay = cv2.imread(overlay_path, -1)

    background_width = background.shape[1]
    background_height = background.shape[0]
    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1],
                        1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y + h, x:x + w] = (1.0 - mask) * \
        background[y:y + h, x:x + w] + mask * overlay_image

    return background


if __name__ == '__main__':
    
    overlay_transparent('background.png', 'overlay.png', 0, 0)
