import requests, base64, urllib
import collections
from imclas import configuration as conf
from imclas.util import ImageUtils
import urllib
import os
from threading import Thread
import cv2
from imclas.data_acquisition.dal import DAL
from imclas.util import array_utils


class ImageCollector:
    def __init__(self, api_key=conf.API_KEY, base_url=conf.SEARCH_SERVICE_BASE_URL):
        self.dal = DAL()
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'Authorization': 'Basic ' + base64.b64encode(self.api_key + ':' + self.api_key)}

    @staticmethod
    def _do_parallel_download(arg):
        i = arg['image_nr']
        origin = i
        for image_url in arg['chunk']:
            url_extension = '.jpg'
            image_name = arg['col_name'] + str(i) + url_extension
            full_image_path = arg['path'] + image_name
            try:
                urllib.urlretrieve(image_url, full_image_path)
                res_img = ImageUtils.resize_image(full_image_path, 300, 300)
                cv2.imwrite(full_image_path, res_img)
            except Exception as e:
                print "Error on image {}".format(image_name)
                print "The error was: {}".format(e)
                if os.path.exists(full_image_path):
                    os.remove(full_image_path)
            i += 1
        print 'Thread for argument {} is done'.format(origin)

    @staticmethod
    def _download_chunk(chunk, collection_name, image_nr):
        ImageCollector._do_parallel_download(
            {'chunk': chunk,
             'col_name': collection_name,
             'path': conf.COLLECTIONS_DIR + os.path.sep + collection_name + os.path.sep,
             'image_nr': image_nr})

    def download_all(self, urls, collection_name):
        """
        Given a list of image urls, download them to the disk and add them to the database
        """
        sys_collection_path = conf.COLLECTIONS_DIR + os.path.sep  + collection_name
        if not os.path.exists(sys_collection_path):
            os.makedirs(sys_collection_path)
        try:
            to_process = list(array_utils.chunks(list(urls), 10))
            i = 0
            for chunk in to_process:
                ImageCollector._download_chunk(chunk, collection_name, i)
                i += 10

            return sys_collection_path
        except Exception as e:
            print "Error in threads: {}".format(e)

    def get_image_urls(self, query, nr_of_urls):
        query_result = self.execute_query(query)
        media_urls = collections.deque()
        if query_result:
            while nr_of_urls > 0:
                next_url, res_urls = self.extract_media_urls_and_next(query_result, nr_of_urls)
                media_urls.extend(res_urls)
                nr_of_urls -= len(res_urls)
                if next_url:
                    r = requests.get(next_url + '&$format=json', headers=self.headers)
                    if r.ok:
                        query_result = r.json()
                    else:
                        raise Exception("Error in request: ".format(str(r.status_code)))
                else:
                    return media_urls
            return media_urls
        else:
            raise Exception("Couldn't extract images")

    def extract_media_urls_and_next(self, query_result, nr_of_urls):
        next_url = None
        if '__next' in query_result['d']:
            next_url = query_result['d']['__next']
        media_urls = collections.deque()

        for res in query_result['d']['results']:
            media_urls.append(res['MediaUrl'])
            nr_of_urls -= 1
            if nr_of_urls == 0:
                return None, media_urls

        return next_url, media_urls

    def execute_query(self, query):
        if query:
            query = "\'" + query + "\'"
            to_encode = {
                'Query': query,
                '$format': 'json'
            }
            encoded_query = urllib.urlencode(to_encode)
            url = self.base_url + '?' + encoded_query
            response = requests.get(url, headers=self.headers)
            return response.json()
        return None


if __name__ == '__main__':

    ic = ImageCollector()

    res = ic.execute_query('xbox')
    print res
    if res is not None:
        nexturl = res['d']['__next']
        print "Next url: %s" % nexturl
        for result in res['d']['results']:
            print result['MediaUrl']

    ic.get_image_urls('xbox', 100)
