#!/usr/bin/env python
#from distutils.core import setup

import io
import os

from setuptools import setup,find_packages

# For Testing:
#
# python3.4 setup.py register -r https://testpypi.python.org/pypi
# python3.4 setup.py bdist_wheel upload -r https://testpypi.python.org/pypi
# python3.4 -m pip install -i https://testpypi.python.org/pypi
#
# For Realz:
#
# python3.4 setup.py register
# python3.4 setup.py bdist_wheel upload
# python3.4 -m pip install

here = os.path.dirname(__file__)

def read(fname, encoding='utf-8'):
    with io.open(os.path.join(here, fname), encoding=encoding) as f:
        return f.read()

setup(
    name='vstruct',
    version='2.0.2',
    description='Vivisect Structure Definition/Parsing Library',
    long_description=read('README.rst'),
    author='Invisigoth Kenshoto',
    author_email='visi@vertex.link',
    url='https://github.com/vivisect/vstruct',
    license='Apache License 2.0',

    packages=find_packages(exclude=['*.tests','*.tests.*']),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 2.7',
    ],

)
