import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-data-sniffer',
    version='0.1',
    packages=['data_sniffer'],
    description='Sniff your data to look for any data issues',
    long_description=README,
    author='Fedor Garin',
    author_email='fedor.garin@gmail.com',
    url='https://github.com/thefedoration/django-data-sniffer/',
    license='MIT',
    install_requires=[
        'Django>=1.7,<1.9',
    ]
)