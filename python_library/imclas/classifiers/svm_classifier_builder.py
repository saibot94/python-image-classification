from imclas.data_acquisition import DAL
from imclas.features import FeatureExtractor
import numpy as np
from collections import deque
from sklearn.cluster import KMeans
from sklearn.svm import SVC
import math
from sklearn.cross_validation import train_test_split


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
        k_means_clf.fit(list(collection_features))

        self.dal.persist_classifier(k_means_clf, model_name, 'kmeans')

        return k_means_clf

    def build_model(self, collections, number_of_clusters=50, train_percentage=0.8):
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
        print 'Started building model: {}. \nParams:\n train_size: {}, number_of_cluster: {}'.format(model_name, str(
            train_percentage), str(number_of_clusters))
        self.dal.get_classifier(model_name, 'kmeans')
        # Step 1: extract features and create KMeans classifier
        print '==> Step 1: Extracting features and creating kmeans'
        k_means_clf = self._build_kmeans_classifier(number_of_clusters,
                                                    collections,
                                                    model_name)

        # Step 2: create histograms out of features for each image
        print '==> Step 2: Creating data histograms'
        data = []
        labels = []
        for collection in collections:
            collection_items = self.dal.get_items_in_collection(collection)
            collection_histograms = self.feature_extractor.extract_histograms_from_features(k_means_clf,
                                                                                            collection_items,
                                                                                            nr_of_bins=number_of_clusters)
            collection_labels = [collection for x in collection_histograms]
            data.extend(collection_histograms)
            labels.extend(collection_labels)

        # Step 3: split into train - test data all of the classes
        print '==> Step 3: Splitting data into train and test'
        train_quantity = int(math.floor(len(data) * train_percentage))
        X_train, y_train = data[:train_quantity], labels[:train_quantity]
        X_test, y_test = data[train_quantity:], labels[train_quantity:]
        print 'Train data size : %d ' % len(X_train)
        print 'Test data size : %d ' % len(X_test)
        X_train, X_test, y_train, y_test = train_test_split(data, labels, train_size=train_percentage)

        # Step 4: create the classifier and then validate it + get metrics
        print '==> Step 4: Creating the classifier and doing some metrics'
        svm_classifier = SVC(probability=True)
        svm_classifier.fit(X_train, y_train)
        mean_score = svm_classifier.score(X_test, y_test)

        self.dal.persist_classifier(svm_classifier, model_name, 'svm')

        print "The mean score for this test was: %f" % mean_score


if __name__ == '__main__':
    svm = SVMClassifierBuilder()
    svm.build_model(['stop signs', 'no left turn signs'], train_percentage=0.8)
