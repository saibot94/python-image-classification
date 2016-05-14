import matplotlib.pyplot as plt

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics


class DigitRecognitionExample:

    def run(self):
        digits = datasets.load_digits()
        images_and_labels = list(zip(digits.images, digits.target))
        for index, (image,label) in enumerate(images_and_labels[:4]):
            plt.subplot(2,4, index+1)
            plt.axis('off')
            plt.imshow(image, cmap = plt.cm.gray_r, interpolation='nearest')
            plt.title('Training %i' % label)

        plt.show()