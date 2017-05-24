from sklearn.base import TransformerMixin, BaseEstimator
#from scrapy.http import HtmlResponse, TextResponse
import tldextract
import html_text
import urllib.parse


def url_to_words(url):
    """
    This turns a URL into a word-list consisting of the subdomain (if any),
    any path elements, and successive key:value pairs from the query-string.
    URL Fragments are not transformed.
    """
    p = urllib.parse.urlparse(url)
    t = tldextract.extract(url)
    words = []
    if t.subdomain:
        words += [t.subdomain]
    words += p.path.strip("/").split("/")
    for key, values in urllib.parse.parse_qs(p.query).items():
        words += [key]
        words += values
    return words


def char_ngrams(text, n=3):
    """
    This simply returns character ngrams from input text, default 3-grams.
    """
    for n in range(0, len(text)):
        yield text[n:n+3]


def _dummy_fit(self, X, y=None):
    "This is a Fit method, and expects an X parameter and optionally a Y parameter."
    return X

def lambda_transformer(name, func, docs="This is a functional transform method created using lambda_transformer."):
    """
    This function constructs a class that inherits from BaseEstimator and TransformerMixin,
    provides a 'dummy' fit method (returning self), and uses the provided func
    on every element of X in the transform method. This scratches a common itch;
    simply functional pipeline transforms on input data.
    Many of the classes in this module are defined using this function.
    """
    T = type(name, (BaseEstimator, TransformerMixin), {
        'fit': _dummy_fit,
        'transform': lambda self, X: [func(x) for x in X],
    })
    T.transform.__doc__ = docs
    T.__doc__ = docs
    return T

ResponseTextTransformer = lambda_transformer('ResponseTextTransformer', lambda R: R.text,
    """This transformer simply extracts the 'text' field from each element in X;
    it assumes that X is an array of scrapy.http.TextResponse objects
    (or subclasses thereof, such as scrapy.http.HtmlResponse)""")

ResponseUrlTransformer = lambda_transformer('ResponseUrlTransformer', lambda R: R.url,
    """This transformer simply extracts the 'url' field from each element in X;
    it assumes that X is an array of scrapy.http.Response objects or
    subclasses thereof.""")

ResponseDomainTransformer = lambda_transformer('ResponseDomainTransformer', lambda R: tldextract.extract(R.url).registered_domain,
    """This transformer simply extracts the registered domain from the URL of
    each Scrapy response object in an array.""")

ResponsePlaintextTransformer = lambda_transformer('ResponsePlaintextTransformer', lambda R: html_text.extract_text(R.text),
    """This transformer extracts the 'plain text' from a HTML document, using
    the html_text library. This excludes inline styles, javascript, comments
    and other text that is not normally visible to the users.""")

ResponseRefererTransformer = lambda_transformer('ResponseRefererTransformer', lambda R: R.request.headers.get("Referer", "").decode(),
    """Get the value of the 'Referer' heading, default empty-string, from the
    request that lead to this response.""")

ResponseLinksTransformer = lambda_transformer('ResponseLinksTransformer', lambda R: list(map(R.urljoin, R.css("a[href]").xpath("@href").extract())),
    """Get all links from the current response page, with local links made
    fully-qualified.""")

class ResponseLocalLinksTransformer(BaseEstimator, TransformerMixin):
    """
    This transformer returns a list of all links that are relative, or which
    point to the same domain or some subdomain of the same primary domain.
    The URLs are returned fully-qualified, even if they began relative.
    """
    def fit(self, X, y=None): return self
    def transform(self, X):
        X_ = []
        for response in X:
            lns = []
            cur_domain = tldextract.extract(response.url).registered_domain
            for u in response.css("a[href]").xpath("@href").extract():
                u = response.urljoin(u)
                if tldextract.extract(u).registered_domain == cur_domain:
                    lns.append(u)
            X_.append(lns)
        return X_

ResponseLocalLinksTransformer.transform.__doc__ = ResponseLocalLinksTransformer.__doc__

# TODO: Image vectorizers for binary/image responses would be pretty cool.
