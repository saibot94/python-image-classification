import cv2


class ImageUtils(object):
    @staticmethod
    def resize_image(original_img, width, height):
        """
        Resizes an image with the given parameters

        :param
        original_img: string

        :param
        width: int

        :param
        height: int

        :returns
        resized_image: numpy_array
        """
        if isinstance(original_img, basestring):
            original_img = cv2.imread(original_img)
        return cv2.resize(original_img, (width, height))
