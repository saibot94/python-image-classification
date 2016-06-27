import cv2
from collections import deque
from multiprocessing.pool import ThreadPool
from imclas.util import array_utils
import collections
import numpy as np


class FeatureExtractor:
    def __init__(self):
        pass

    def perform_sift(self, image_path):
        """
        Run the opencv detect & compute phase for SIFT descriptors on the data

        Return the matrix of N x 128 feature descriptors
        """

        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        sift = cv2.xfeatures2d.SIFT_create()
        kp, desc = sift.detectAndCompute(gray, None)

        return desc

    def extract_features_from_collection(self, collection_items, async=False):
        """
        Takes an iterable of item paths and returns the full array of SIFT descriptors
        for them.

        For efficiency, the extraction is performed with a thread pool
        """

        q = deque()
        if async:
            pool = ThreadPool(processes=10)
            async_results = deque()

            for item in collection_items:
                async_results.append(pool.apply_async(self.perform_sift, (item,)))

            for result in async_results:
                async_response = result.get()
                if async_response is not None:
                    q.extend(async_response)
        else:
            for item in collection_items:
                q.extend(self.perform_sift(item))
        return q

    def extract_histograms_from_images(self, classifier, images, nr_of_bins=50):
        zrs = collections.deque()
        for image in images:
            image = self.perform_sift(image)
            if image is not None:
                zr = classifier.predict(image)
                hist, bin_edges = np.histogram(zr, bins=nr_of_bins, density=True)
                zrs.append(hist)
        return zrs
