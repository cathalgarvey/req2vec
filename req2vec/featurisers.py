import functools
import scrapy
import scrapy.http
import base64
import gzip


def response_data(response):
    "Returns response data that is expected to be useful for vectorisation.. this means everything, more or less."
    data = {
        'url': response.url,
        'body': base64.b64encode(gzip.compress(response.text.encode())).decode(),
        'headers' = { k.decode(): [s.decode() for s in response.headers.getlist(k)]
                        for k in response.headers.keys() },
        'request_headers' = { k.decode(): [s.decode() for s in response.request.headers.getlist(k)]
                                for k in response.headers.keys() },
    }
    if 'Referer' in data['headers'] and len(data['headers']['Referer'])>0:
        data['referer'] = data['headers']['Referer'][0]
    if 'capture_features_meta' in response.meta:
        data.update(response.meta['capture_features_meta'])
    # TODO: Compressed request content?0
    return data


def capture_features(scrapy_parsing_method, *, data_field='response_data'):
    """
    A decorator for an existing parse method on a scrapy spider, which:
    * Hijacks outgoing requests to add metadata that may be useful for data
      collection later (e.g. Referer)
    * Hijacks output Items to add features concerning the request and response
      content, which is added as a new field 'response_data'.
    """
    @functools.update_wrapper(wrapped=scrapy_parsing_method)
    def wrapper(self, response):
        ref = response.url
        for yielded in scrapy_parsing_method(self, response):
            if isinstance(yielded, (dict, scrapy.Item)):
                yielded = dict(yielded)
                yielded[data_field] = response_data(response)
                yield yielded
            elif isinstance(yielded, scrapy.http.Request):
                yielded.meta['capture_features_meta'] = {
                    'referer': ref
                }
                yield yielded
            else:
                raise TypeError("Unexpected type yielded from parse method: {} -> {}".format(type(yielded), yielded))
    return wrapper
