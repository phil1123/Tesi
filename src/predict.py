import os
from matplotlib import pyplot as plt
import cv2
import sys
sys.path.append('/home/phil/unimib/tesi/src')
import config as cfg


def get_list_per_type(directory, scan):
    names = [f for f in os.listdir(directory) if f[:2] == scan[:2]]
    return names


def get_image(names, directory, n):
    image = cv2.imread(directory+names[n])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def pred(net, weigths, directory, scans, figures, exp, n):
    for scan in scans:
        autoencoder, encoder = net
        autoencoder.load_weights(weigths)
        img = get_image(get_list_per_type(directory, scan), directory, n)
        img = cv2.resize(img, dsize=(192, 192), interpolation=cv2.INTER_LANCZOS4)
        pred_img = autoencoder.predict(img.reshape((1,) + img.shape + (1,)))
        pred_img = pred_img.reshape((192, 192))
        # plot prediction and save image
        plt.figure(figsize=(14, 7))
        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.subplot(1, 2, 2)
        plt.imshow(pred_img)
        plt.savefig(os.path.join(figures, exp, scan+'_CAE.png'))
        print('Prediction on done.')
