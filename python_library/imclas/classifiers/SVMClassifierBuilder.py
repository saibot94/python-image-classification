from imclas.data_acquisition import DAL
from imclas.features import FeatureExtractor
import numpy as np
from collections import deque
from sklearn.cluster import KMeans


class SVMClassifierBuilder:
    def __init__(self):
        self.dal = DAL()
        self.feature_extractor = FeatureExtractor()

    def _build_kmeans_classifier(self, number_of_clusters, collections, model_name):
        collection_features = deque()
        for collection in collections:
            collection_items = self.dal.get_items_in_collection(collection)
            collection_features.extend(self.feature_extractor.extract_features_from_collection(collection_items))

        k_means_clf = KMeans(n_jobs=-1, n_clusters=number_of_clusters)
        k_means_clf.fit(collection_features)

        return k_means_clf

    def build_model(self, collections, number_of_clusters=50):
        """
        This function creates the KMeans classifier and
        SVM classifiers (afterwards).

        collections :param
        list of collection names

        number_of_clusters :param
        how many clusters to create for the file
        """

        if len(collections) < 2:
            print 'Not enough collections specified!'
            return

        try:
            for collection in collections:
                self.dal.get_collection_id(collection)
        except Exception:
            print 'One or more collections does not exist!'
            return

        model_name = '~'.join(collections)
        self.dal.get_classifier_with_name(model_name)
        # Step 1: extract features and create KMeans classifier
        k_means_clf = self._build_kmeans_classifier(number_of_clusters,
                                                    collections,
                                                    model_name)
