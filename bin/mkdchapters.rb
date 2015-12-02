#!/usr/bin/ruby
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
# mkdchapters.rb - Lists chapter file names retrieved from mkdocs.yml

require 'optparse'
require 'ostruct'
require 'yaml'

options = OpenStruct.new()
options.basedir = nil

OptionParser.new do |opts|
  opts.banner =
    "mdchapters.rb  - Lists chapter file names retrieved from mkdocs.yaml\n" +
    "\n" +
    "usage: \n" +
    "  mkdchapters.rb [--base-dir <dir>] <mkdocs configuration file>\n" +
    "\n"
  opts.on('-b', '--base-dir DIR', 'Optionaly prepend DIR/ to file names.') { |v| options.basedir = v }
end.parse!

require 'yaml'

config = YAML.load_file(ARGV[0])

config['pages'].each { |page|
  if ( options.basedir )
    puts([options.basedir, page.values[0]].join('/'))
  else
    puts(page.values[0])
  end
}
