import cv2
from matplotlib import pyplot as plt


def gaussian_blur(filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plt.subplot(1, 2, 1), plt.imshow(gray), plt.title("Normal img")
    plt.subplot(1, 2, 2), plt.imshow(img), plt.title("Blurred image")


if __name__ == '__main__':
    gaussian_blur('home.jpg')
