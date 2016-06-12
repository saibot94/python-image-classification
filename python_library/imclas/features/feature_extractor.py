import cv2
from collections import deque
from multiprocessing.pool import ThreadPool
from imclas.util import array_utils


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

    def extract_features_from_collection(self, collection_items):
        """
        Takes an iterable of item paths and returns the full array of SIFT descriptors
        for them.

        For efficiency, the extraction is performed with a thread pool
        """
        pool = ThreadPool(processes=10)
        async_results = deque()

        q = deque()
        for item in collection_items:
            async_results.append(pool.apply_async(self.perform_sift, (item, )))

        for result in async_results:
            async_response = result.get()
            if async_response is not None:
                q.extend(async_response)
        return q