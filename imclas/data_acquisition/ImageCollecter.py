import requests, base64, urllib
#import imclas.configuration as conf

class ImageCollecter:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'Authorization': 'Basic ' + base64.b64encode(self.api_key + ':' + self.api_key)}

    def execute_query(self, query):
        if query:
            query = "\'" + query + "\'"
            to_encode = {
                'Query' : query,
                '$format' : 'json'
            }
            encoded_query = urllib.urlencode(to_encode)
            url = self.base_url + '?' + encoded_query
            response = requests.get(url, headers=self.headers)
            return response.json()
        return None


if __name__ == '__main__':
    apiKey = '<YOUR_API_KEY>'
    base_url = 'https://api.datamarket.azure.com/Bing/Search/v1/Image'
    ic = ImageCollecter(api_key=apiKey, base_url=base_url)

    res = ic.execute_query('xbox')
    if res is not None:
        for result in res['d']['results']:
            print result['MediaUrl']
