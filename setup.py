import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-data-sniffer',
    version='0.4.1',
    packages=[
        'data_sniffer',
        'data_sniffer.templatetags',
    ],
    include_package_data=True,
    description='Sniff your django models to look for any data issues',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Fedor Garin',
    author_email='fedor.garin@gmail.com',
    url='https://github.com/thefedoration/django-data-sniffer/',
    license='MIT',
    install_requires=[
        'Django>=1.7,<1.8',
        'requests'
    ]
)