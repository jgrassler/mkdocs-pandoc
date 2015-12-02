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
# mdhead.rb - increases header level in markdown files by an arbitrary number of levels.
#
# usage:
#
#   mdhead.rb [-i] [ <file> ... ]

require 'fileutils'
require 'optparse'
require 'ostruct'
require 'yaml'

options = OpenStruct.new()
options.inplace = false
options.offset = 0

OptionParser.new do |opts|
  opts.banner = 
    "mdhead.rb - increases header level in markdown files by an arbitrary number of levels.\n" +
    "\n" +
    "usage: \n" +
    '  mdhead.rb [-i] [ <file> ... ]' +
    "\n\n"
  opts.on('-i', '--in-place', 'Edit files in place (default is to write to standard output)') { |v| options.inplace = true }
  opts.on('-l', '--level-offset OFFSET', 'Increase header levels by this amount (must be a positive integer. default: 0)') { |offset| options.offset = offset.to_i}
end.parse!


files = Array.new()

if ( ARGV.length > 0 )
  ARGV.each { |arg|
    begin
      files.push(File.open(arg, 'r'))
    rescue => e
      "Couldn't open #{arg} for reading: #{e.to_s}"
    end
  }
else
  files.push(STDIN)
end

files.each { |f|
  lines = Array.new()
  f.lines().each { |line|
    lines.push(line.sub(/^#/, '#' + ('#' * options.offset)))
  }

  f.close()

  out = STDOUT

  if ( options.inplace and f.path )
    begin
      out = File.open(f.path, 'w')
    rescue => e
      warn("Couldn't open #{arg} for writing, skipping.")
      next
    end
  end

  lines.each { |line|
    out.puts(line)
  }

  if ( options.inplace and f.path )
    out.close()
  end
}
