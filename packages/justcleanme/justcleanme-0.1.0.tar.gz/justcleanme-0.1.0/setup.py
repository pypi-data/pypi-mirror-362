from setuptools import setup, find_packages

setup(
    name='justcleanme',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'emoji',
        'textblob',
        'scikit-learn',
        'sentence-transformers',
    ],
    python_requires='>=3.6',
    description='Simple and easy NLP text preprocessing package',
    author='Rituraj Pandey',
)
