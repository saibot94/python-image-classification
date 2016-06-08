import requests, base64, urllib
import collections
from imclas import configuration as conf


class ImageCollector:
    def __init__(self, api_key=conf.API_KEY, base_url=conf.SEARCH_SERVICE_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'Authorization': 'Basic ' + base64.b64encode(self.api_key + ':' + self.api_key)}

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
