#!/usr/bin/env/python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = (
    "mkdocs_pandoc is a library of preprocessors that convert mkdocs style markdown "
    "(multiple files, with the document structure defined in the mkdocs "
    "configuration file mkdocs.yml) into a single markdown document digestible by "
    "pandoc. It ships with the command line frontend tool mkdocs2pandoc as its primary " 
    "user interface."
    )

setup(
    name='mkdocs-pandoc',

    version='0.2.6',

    description='A translator from mkdocs style markdown to pandoc style '
                + 'markdown',

    long_description=long_description,

    url='https://github.com/jgrassler/mkdocs-pandoc',
    author='Johannes Grassler',
    author_email='johannes@btw23.de',
    license='Apache',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='mkdoc markdown pandoc',
    packages=find_packages(),

    install_requires=['mkdocs>=0.14.0',
            'markdown-include>=0.5.1'
            ],

    entry_points={
        'console_scripts': [
            'mkdocs2pandoc=mkdocs_pandoc.cli.mkdocs2pandoc:main',
        ],
    },
)
