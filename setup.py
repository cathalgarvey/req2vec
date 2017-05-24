from setuptools import setup, find_packages
import textwrap

setup(name='req2vec',
      version='0.0.1',
      description="Vectorisation toolkit for Integrating Scrapy + SKLearn.",
      long_description=textwrap.dedent("""\
        # Scrapy <3 SKLearn
        Scrapy is an ideal toolkit for data collection for web/scale data science
        and NLP tasks. However, it's easy to forget to collect a given feature
        for a new project the first time around, and regret not having it, later.

        I found myself collecting the same sorts of features each time, so I started
        writing this as an ergonomic toolkit to facilitate collecting the "right kind"
        of data for a Data Science project along with the business-as-usual data
        defined in Scrapy Item syntax.

        In other words, given a spider that goes to a certain kind of page and
        extracts a certain record or records, I wanted a toolkit that I could add
        in several lines of python, which would expand the scope of data collection
        to include capturing page content, URL, request and response headers,
        etcetera.

        Additionally, using this data in a machine learning project often meant
        rewriting the same modules time and again; transformers for pipelines that
        would extract the URL for one feature vectorization sub-element, and the
        page HTML for another, and the page text content for another again. So,
        I wanted a module full of simple, fluent pipeline transformers, also.
        So, given data extracted using the above methods from a Scrapy crawl,
        it should be easy to direct this dataset through a pipeline to train a
        classifier or tool, and it should then be easy to deploy this pipeline
        into a scrapy project and simply pass it `response` items directly, and
        have it 'just work'.

        # Usage

        The `transformers` submodule contains lots of pipeline transformers for
        extracting various features from Response objects, including Url, Referer,
        HTML, Text, and Links (all, local, or off-site). These transformers are
        generally stateless and should 'just work', though most will return
        variable-length outputs and will need further processing to become useful
        features.

        For the special case of URLs, two transformers are presented that vectorise
        URL content either as bag-of-words (excluding the primary domain name,
        to prevent overfitting to training domains), or as character trigrams.
      """).strip(),
      author="Cathal Garvey",
      author_email="cathalgarvey@cathalgarvey.me",
      url='https://github.com/cathalgarvey/req2vec',
      license='AGPLv3+',
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=['scrapy', 'scikit-learn'],
)
