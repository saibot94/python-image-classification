from imclas.data_acquisition import DAL, ImageCollector
from imclas.features import FeatureExtractor
import os


class CollectionManager:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.dal = DAL()
        self.image_collector = ImageCollector()
        self.dal.create_image_collection()

    def create_collection(self, query, nr_of_items, collection_name):
        if self.dal.get_collection_id(collection_name) is None:
            urls = self.image_collector.get_image_urls(query, nr_of_items)
            sys_collection_path = self.image_collector.download_all(urls, collection_name)
            if sys_collection_path:
                self.add_paths_to_db(collection_path=sys_collection_path,
                                     collection_name=collection_name)

        else:
            raise Exception("Collection already exists!")

    def remove_collection(self, collection_name):
        coll_id = self.dal.get_collection_id(collection_name)
        if coll_id is not None:
            collection_items = self.dal.get_items_in_collection(collection_name)
            for item in collection_items:
                os.remove(item)

            self.dal.remove_collection(collection_name)
        else:
            raise Exception('Collection does not exist!')


    def add_paths_to_db(self, collection_path, collection_name):
        for item in os.listdir(collection_path):
            full_path = collection_path + '\\' + item
            self.dal.insert_path_for_collection(item_path=full_path,
                                                collection_name=collection_name)
