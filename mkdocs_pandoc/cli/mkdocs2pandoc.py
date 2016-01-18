#!/usr/bin/python
#
# Copyright 2015 Johannes Grassler <johannes@btw23.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# mkdocs2pandoc - converts mkdocs documentation into a single pandoc markdown document

from __future__ import print_function

import argparse
import codecs
import sys

import mkdocs.config
from mkdocs_pandoc.exceptions import FatalError

import mkdocs_pandoc

def main():
    opts = argparse.ArgumentParser(
            description="mdtableconv.py " +
            "- converts pipe delimited tables to Pandoc's grid tables")

    opts.add_argument('-e', '--encoding', default='utf-8',
            help="Set encoding for input files (default: utf-8)")

    opts.add_argument('-f', '--config-file', default='mkdocs.yml',
            help="mkdocs configuration file to use")

    opts.add_argument('-i', '--image-ext', default=None,
            help="Extension to substitute image extensions by (default: no replacement)")

    opts.add_argument('-w', '--width', default=100,
            help="Width of generated grid tables in characters (default: 100)")

    opts.add_argument('-x', '--exclude', default=None, action='append',
            help="Include files to skip (default: none)")

    opts.add_argument('-o', '--outfile', default=None,
            help="File to write finished pandoc document to (default: STDOUT)")

    args = opts.parse_args()

    # Python 2 and Python 3 have mutually incompatible approaches to writing
    # encoded data to sys.stdout, so we'll have to pick the appropriate one.

    if sys.version_info.major == 2:
      out = codecs.getwriter(args.encoding)(sys.stdout)
    elif sys.version_info.major >= 3:
      out = open(sys.stdout.fileno(), mode='w', encoding=args.encoding, buffering=1)

    try:
      pconv = mkdocs_pandoc.PandocConverter(
                config_file=args.config_file,
                exclude=args.exclude,
                image_ext=args.image_ext,
                width=args.width,
                encoding=args.encoding,
                )
    except FatalError as e:
        print(e.message, file=sys.stderr)
        return(e.status)
    if args.outfile:
        try:
          out = codecs.open(args.outfile, 'w', encoding=args.encoding)
        except IOError as e:
          print("Couldn't open %s for writing: %s" % (args.outfile, e.strerror), file=sys.stderr)

    for line in pconv.convert():
        out.write(line + '\n')
    out.close()
