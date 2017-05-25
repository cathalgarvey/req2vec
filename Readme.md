# Req2Vec - Easy Bolt-On Data Collection & Feature Engineering Transformers for Scrapy and SKLearn
by Cathal Garvey, Copyright 2017, released under the LGPLv3 or later.

## Scrapy <3 SKLearn
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

## Usage

The `transformers` submodule contains lots of pipeline transformers for
extracting various features from Response objects, including Url, Referer,
HTML, Text, and Links (all, local, or off-site). These transformers are
generally stateless and should 'just work', though most will return
variable-length outputs and will need further processing to become useful
features.

For the special case of URLs, two transformers are presented that vectorise
URL content either as bag-of-words (excluding the primary domain name,
to prevent overfitting to training domains), or as character trigrams.

The 'featurisers' submodule includes a bunch of data-collection utilities
for scrapy spiders, which are intended (but untested) to act as rapidly-
insertable decorators on existing data-collection methods in existing
spiders. In other words, the goal is that you can take the `parse(self, response)`
method of an existing spider, and decorate it with `req2vec.featurisers.capture_features`,
and get the following:

* Outgoing Requests will have some extra magic (currently minimal) to collect extra context.
* Outgoing Items will have an additional field added (default 'response_data')
  containing potentially valuable data for HTML-response feature-engineering.
  There is no need to add this field to your Scrapy items, as items are cast
  first to regular dictionaries.

## Warnings

### Development Status
This is all experimental. I'm literally committing this prior to local testing.
I'll increment version numbers as I develop and test this.

### Spider Decorators for Data Collection
Collecting all this extra data in your item pipelines is obviously going
to bloat the hell out of your output data. **This is especially true when
you yield more than one item per page!**

### Pipelines, Transformers Etc.
These should be somewhat sane and stable; they are performing trivial
tasks and probably work as intended.
