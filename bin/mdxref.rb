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
# mdxref.rb - converts mkdocs style cross-references in markdown files since pandoc does not support them

require 'fileutils'
require 'optparse'
require 'ostruct'
require 'yaml'

options = OpenStruct.new()
options.inplace = false
options.offset = 0
options.format = 'titleonly'

OptionParser.new do |opts|
  opts.banner = 
    "mdxref.rb - converts mkdocs style cross-references in markdown files since pandoc does not support them\n" +
    "\n" +
    "usage: \n" +
    '  mdxref.rb [-i] [-f][ <file> ... ]' +
    "\n\n"
  opts.on('-i', '--in-place', 'Edit files in place (default is to write to standard output)') { |v| options.inplace = true }
  opts.on('-f F', '--format F', 'Convert cross references to format F (available formats: titleonly; default: `titleonly`)') { |v| options.format = v }
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
    while m = line.match(/\[([^\]]*)\]\{([^}]*)\}/)
      title = m[1]
      target = m[2]

      case options.format
      when 'titleonly'
        line.sub!(/\[([^\]]*)\]\{([^}]*)\}/, title)
      else
        warn 'Invalid cross-reference format, exiting'
        exit(1)
      end
    end
    lines.push(line)
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
