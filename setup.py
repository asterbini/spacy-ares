from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='spacy-ares',
    version='0.1',
    author='Andrea Sterbini',
    author_email='sterbini@di.uniroma1.it',
    url='http://github.com/asterbini/spacy-ares',
    license='GPL v3',
    description="Spacy token disambiguation through BERT+ARES",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['spacy_ares'],
    install_requires=[
        'spacy>=3',
        'spacy-transformers>=1',
        'gensim',
    ],
    package_data={
        #'spacy_ares': ['data/*'],
        },
)
