#!/usr/bin/ruby

# mdtitles.rb  - Adds chapter titles from mkdocs.yml to chapter files (used for processing mkdocs documentation in pandoc)
#
# usage:
#
#   mdtitles.rb [--base-dir <dir>] <mkdocs configuration file>

require 'fileutils'
require 'optparse'
require 'ostruct'
require 'yaml'

options = OpenStruct.new()
options.basedir = 'pandoc'

OptionParser.new do |opts|
  opts.banner = 
    "mdtitles.rb  - Adds chapter titles from mkdocs.yml to chapter files (used for processing mkdocs documentation in pandoc)\n" +
    "\n" +
    "usage: \n" +
    "  mdtitles.rb [--base-dir <dir>] <mkdocs configuration file>\n" +
    "\n"
  opts.on('-b', '--base-dir DIR', 'Treat paths in mkdocs.yaml relative to this directory (default: pdf/)') { |v| options.basedir = v }
end.parse!

mdfiles = Hash.new()

begin
  config = YAML.load_file(ARGV[0])
rescue => e
  warn "Couldn't open #{ARGV[0]} for reading: #{e.to_s}"
end

config['pages'].each { |chapter|
  mdfiles[chapter.values[0]] = chapter.keys[0] # Reverse keys and values since we need the file names (values) first.
}

mdfiles.each_pair { |filename, title|
  lines = Array.new()
  lines.push('# ' + title)
  lines.push('')
  fname = options.basedir + '/' + filename

  begin
    f = File.open(fname, 'r')
  rescue => e
    warn("Couldn't open #{fname} for reading: #{e.to_s}")
    next
  end

  f.lines().each { |line|
    lines.push(line)
  }
  f.close()

  begin
    f = File.open(fname, 'w')
  rescue => e
    warn("Couldn't open #{fname} for writing: #{e.to_s}")
    next
  end

  lines.each { |line|
    f.puts(line)
  }

  f.close()
}
