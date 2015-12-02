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
# mdinclude.py - Wrapper for using markdown.markdown_include as simple preprocessor (just pulls in includes without running the HTML generator)

from __future__ import print_function
import argparse
import markdown_include.include as incl
import os
import sys
import re

opts = argparse.ArgumentParser(description='Wrapper for using markdown.markdown_include as simple preprocessor (just pulls in includes without running the HTML generator)')
opts.add_argument('-b', '--base-path', default='.', 
        help="Base path to prepend file names in include statements with (default: '.')")
opts.add_argument('-e', '--encoding', default='utf-8',
        help="Character encoding for file names in include statements (default: 'utf-8')")
opts.add_argument('-i', '--adjust-images', default=False, action='store_true',
        help="Adjust image paths (default: no change)")
opts.add_argument('-I', '--image-ext', default=None,
    help="Adjust image file extension to the extension passed as argument, e.g. 'pdf' (default: no change)")
opts.add_argument('-o', '--output', default=None,
        help='File to write processed markdown code to (output will be written to STDOUT if unset)')
opts.add_argument('-p', '--image-path', default=None,
        help='Path to prepend to relative image paths (directory of chapter file, if applicable)')
opts.add_argument('FILE', nargs='*', default=[])
args = None

### This class is merely a wrapper for providing markdown_include.include
class IncludeWrapper(incl.IncludePreprocessor):
    def __init__(self, base_path='.', encoding='utf-8'):
        self.base_path = base_path
        self.encoding = encoding


def process_images(lines,
        filename=None,
        image_path=None,
        base_path=None,
        adjust_path=False,
        image_ext=None):

    # Nothing to do in this case
    if (not adjust_path) and (not image_ext):
        return lines

    for i in range(len(lines) - 1):
        alt = ''
        img_name = ''

        matches = re.match(r'!\[(.*?)\]\((.*?)\)', lines[i])

        # Make sure there is in fact an image file name
        if matches:
            alt = matches.group(1)
            img_name = matches.group(2)
        else:
            continue

        if image_ext:
            img_name = re.sub(r'\.\w+$', '.' + image_ext, img_name)

        if adjust_path and (image_path or filename):
            # explicitely specified image path takes precedence over path
            # relative to chapter
            if image_path and filename:
                img_name = os.path.join(os.path.abspath(image_path), img_name)
            # generate image path relative to chapter's main file
            if filename and (not image_path):
                img_name = os.path.join(
                        os.path.abspath(
                            os.path.dirname(filename)),
                        img_name)

        lines[i] = '![%s](%s)' % (alt, img_name)

    return lines

if __name__ == '__main__':
    args = opts.parse_args()

    if args.output and (args.output != '-'):
        try:
          out = open(args.output, 'w')
        except Exception as e:
          print("Couldn't open %s for writing: %s" % (args.output, e.message), file=sys.stderr)
          exit(1)
    else:
        out = sys.stdout

    if len(args.FILE) == 0:
        w = IncludeWrapper(args.base_path, args.encoding)
        lines = []
        for line in sys.stdin.readlines():
            lines.append(line.rstrip('\n'))
        for line in process_images(w.run(lines),
                None,
                args.image_path,
                args.base_path,
                args.adjust_images,
                args.image_ext):
          print(line, file=out)
          print(file=out)
    else:
      for f in args.FILE:
        try:
          fh = open(f, 'r')
        except Exception as e:
          print("Couldn't open %s for reading: %s" % (f, e.message), file=sys.stderr)
        w = IncludeWrapper(args.base_path, args.encoding)
        lines = []
        for line in fh.readlines():
            lines.append(line.rstrip('\n'))
        for line in process_images(w.run(lines),
            f,
            args.image_path,
            args.base_path,
            args.adjust_images,
            args.image_ext):
          print(line, file=out)
        print(file=out)
        fh.close()

    if args.output:
        out.close()
