from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.0.4'

setup(
    name='py2captcha',

    version='0.1.1',

    description='Client library for solve captchas with 2captcha.com support.',

    long_description=long_description,

    long_description_content_type='text/markdown',

    author='SDASolutions',

    author_email='sdasolutions.co@gmail.com',

    license='MIT',

    packages=['py2captcha'],

    install_requires=[
        'requests',
        'six',
        'beautifulsoup4'
    ],

    url='https://github.com/sdasolutions/py2captcha',

    keywords=[
        'CAPTCHA',
        'reCAPTCHA'
    ],

    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License'
    ],
)
