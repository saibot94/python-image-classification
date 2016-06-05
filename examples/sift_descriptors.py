import cv2
from matplotlib import pyplot as plt


def sift_finder():
    img = cv2.imread('home.jpg')
    print img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp, desc = sift.detectAndCompute(gray, None)
    cv2.drawKeypoints(gray, kp, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # a keypoint contains the following: angle, class_id, octave, pt, response, size
    # for each keypoint there's going to be computed an 128 long feature vector (descriptor)

    original_img = cv2.imread('home.jpg')
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    plt.subplot(1, 2, 1), plt.imshow(img), plt.title("SIFT Keypoints")
    plt.subplot(1, 2, 2), plt.imshow(original_img), plt.title("Original image")

    plt.show()


if __name__ == '__main__':
    sift_finder()
