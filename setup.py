from setuptools import setup, find_packages

setup(name='req2vec',
      version='0.0.1',
      description="Vectorisation toolkit for Integrating Scrapy + SKLearn.",
      long_description=open('Readme.md').read().strip(),
      author="Cathal Garvey",
      author_email="cathalgarvey@cathalgarvey.me",
      url='https://github.com/cathalgarvey/req2vec',
      license='AGPLv3+',
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=['scrapy', 'scikit-learn'],
)
