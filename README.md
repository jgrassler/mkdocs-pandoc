# DESCRIPTION

This is a mixed bag of preprocessors for [mkdocs](http://www.mkdocs.org) style
markdown that will convert it into one markdown file suitable for consumption
by [pandoc(1)](http://www.pandoc.org). Their original purpose is providing a
path for generating PDF and EPUB output in a sane manner, i.e. without having
to resort to a HTML to PDF conversion step. It may be useful for other purposes
as well, but this is the one I'm reasonably sure it works for.

# DEPENDENCIES

In order to actually convert `mkdocs` documention to PDF you will need
`mkdocs`, `pandoc` and the toolchain pandoc uses to generate PDF. On an Ubuntu
14.04 LTS system you would have to install a bunch of Debian packages...

```
aptitude install \
fonts-lmodern \
lmodern \
markdown \
pandoc \
texlive-base \
texlive-latex-extra \
texlive-fonts-recommended \
texlive-latex-recommended \
texlive-xetex
```

...and `mkdocs` itself:

```
pip install mkdocs
```

Optionally, you may want to install markdown-include:

```
pip install markdown-include
```

This is a markdown extension that lets you build a hierarchy of Markdown
documents using include statements (similar to LaTeX's `\input{}`.

# INSTALLATION

Retrieve the source code...

```
git clone https://github.com/jgrassler/mkdocs-pandoc
```

...and add the repository's bin/ directory to your current shell's search
path:

```
PATH=$PATH:$(readlink -e mkdocs-pandoc/bin)
```

Add the result of `echo "PATH=\$PATH:$(readlink -e mkdocs-pandoc/bin)"` to your
shell's initialization file, e.g. `~/.bashrc` or `~/.zshrc` to add the
repository's `bin/` directory to your shell's search path permanently.

# USAGE

When executed in the directory where your documentation's `mkdoc.yml` and the
`docs/` directory containing the actual documentation resides, `mkdocs2pandoc`
should print one long Markdown document suitable for `pandoc(1)` on standard
output. This works under the following assumptions:

1. The commands in this repository's `bin/` directory are in your shell's
   `PATH` variable (if you followed the installation instructions above they
   should be).

2. `docs_dir` in `mkdocs.yml` is set to `docs` or unset (in this case it
   defaults to `docs`). If your `docs_dir` is set to a different value specify
   it as the first argument to mkdocs2pandoc.

## Usage example

```
cd ~/mydocs
mkdocs2pandoc > mydocs.pd
pandoc --toc -f markdown+grid_tables+table_captions -o mydocs.pdf mydocs.pd   # Generate PDF
pandoc --toc -f markdown+grid_tables -t epub -o mydocs.epub mydocs.pd         # Generate EPUB
```

# BUGS

The following things are known to be broken:

* `mdtableconv.py`: Line wrapping in table cells will wrap links, which causes
  whitespace to be inserted in their target URLs, at least in PDF output. While
  this is a bit of a Pandoc problem,

* `mdtitles.rb`, `mdchapters.rb`, and (indirectly) `mdhead.rb`: these scripts
  use information from the `pages` data structure in `mkdocs.yml` and go about
  it in a rather naive way that breaks with 
  [Multilevel Documentation](http://www.mkdocs.org/user-guide/writing-your-docs/#multilevel-documentation).

* [Internal Hyperlinks](http://www.mkdocs.org/user-guide/writing-your-docs/#internal-hyperlinks) 
  between markdown documents will be reduced to their link titles, i.e. they
  will not be links in the resulting Pandoc document.

# ROADMAP

I plan on turning this mess of scripts into a proper Python module. Stay tuned
and feel free to play with the existing code in the mean time.

# COPYRIGHT

(C) 2015 Johannes Grassler <johannes@btw23.de>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

You will also find a copy of the License in the file `LICENSE` in the top level
directory of this source code repository. In case the above URL is unreachable
and/or differs from the copy in this file, the file takes precedence.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
