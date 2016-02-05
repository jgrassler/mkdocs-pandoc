import mkdocs_pandoc.filters.anchors
import mkdocs_pandoc.filters.chapterhead
import mkdocs_pandoc.filters.headlevels
import mkdocs_pandoc.filters.images
import mkdocs_pandoc.filters.exclude
import mkdocs_pandoc.filters.include
import mkdocs_pandoc.filters.tables
import mkdocs_pandoc.filters.toc
import mkdocs_pandoc.filters.xref

from mkdocs_pandoc.exceptions import FatalError

import codecs
import os
import yaml


class PandocConverter:
    """Top level converter class. Instatiate separately for each mkdocs.yml."""

    def __init__(self, **kwargs):
        self.config_file = kwargs.get('config_file', 'mkdocs.yml')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.exclude = kwargs.get('exclude', None)
        self.filter_tables = kwargs.get('filter_tables', True)
        self.filter_xrefs = kwargs.get('filter_xrefs', True)
        self.image_ext = kwargs.get('image_ext', None)
        self.strip_anchors = kwargs.get('strip_anchors', True)
        self.width = kwargs.get('width', 100)

        try:
            cfg = codecs.open(self.config_file, 'r', self.encoding)
        except IOError as e:
            raise FatalError("Couldn't open %s for reading: %s" % (self.config_file,
                e.strerror), 1)

        self.config = yaml.load(cfg)

        if not 'docs_dir' in self.config:
            self.config['docs_dir'] = 'docs'

        if not 'site_dir' in  self.config:
            self.config['site_dir'] = 'site'

        # Set filters depending on markdown extensions from config
        # Defaults first...
        self.filter_include = False
        self.filter_toc = False

        # ...then override defaults based on config, if any:

        if 'markdown_extensions' in self.config:
          for ext in self.config['markdown_extensions']:
              extname = ''
              # extension entries may be dicts (for passing extension parameters)
              if type(ext) is dict:
                  extname = list(ext.keys())[0]
              if type(ext) is str:
                  extname = ext

              if extname == 'markdown_include.include':
                  self.filter_include = True
              if extname == 'toc':
                  self.filter_toc = True

        cfg.close()

    def flatten_pages(self, pages, level=1):
        """Recursively flattens pages data structure into a one-dimensional data structure"""
        flattened = []

        for page in pages:
            if type(page) is list:
                flattened.append(
                             {
                                'file': page[0],
                                'title': page[1],
                                'level': level,
                             })
            if type(page) is dict:
                if type(list(page.values())[0]) is str:
                    flattened.append(
                            {
                                'file': list(page.values())[0],
                                'title': list(page.keys())[0],
                                'level': level,
                             })
                if type(list(page.values())[0]) is list:
                    flattened.extend(
                            self.flatten_pages(
                                list(page.values())[0],
                                level + 1)
                            )


        return flattened

    def convert(self):
        """User-facing conversion method. Returns pandoc document as a list of
        lines."""
        lines = []

        pages = self.flatten_pages(self.config['pages'])

        f_exclude = mkdocs_pandoc.filters.exclude.ExcludeFilter(
                exclude=self.exclude)

        f_include = mkdocs_pandoc.filters.include.IncludeFilter(
                base_path=self.config['docs_dir'],
                encoding=self.encoding)

        # First, do the processing that must be done on a per-file basis:
        # Adjust header levels, insert chapter headings and adjust image paths.

        f_headlevel = mkdocs_pandoc.filters.headlevels.HeadlevelFilter(pages)

        for page in pages:
            fname = os.path.join(self.config['docs_dir'], page['file'])
            try:
                p = codecs.open(fname, 'r', self.encoding)
            except IOError as e:
                raise FatalError("Couldn't open %s for reading: %s" % (fname,
                    e.strerror), 1)
            f_chapterhead = mkdocs_pandoc.filters.chapterhead.ChapterheadFilter(
                    headlevel=page['level'],
                    title=page['title']
                    )

            f_image = mkdocs_pandoc.filters.images.ImageFilter(
                    filename=page['file'],
                    image_path=self.config['site_dir'],
                    image_ext=self.image_ext)

            lines_tmp = []

            for line in p.readlines():
                lines_tmp.append(line.rstrip())

            if self.exclude:
                lines_tmp = f_exclude.run(lines_tmp)

            if self.filter_include:
                lines_tmp = f_include.run(lines_tmp)

            lines_tmp = f_headlevel.run(lines_tmp)
            lines_tmp = f_chapterhead.run(lines_tmp)
            lines_tmp = f_image.run(lines_tmp)
            lines.extend(lines_tmp)
            # Add an empty line between pages to prevent text from a previous
            # file from butting up against headers in a subsequent file.
            lines.append('')

        # Strip anchor tags
        if self.strip_anchors:
            lines = mkdocs_pandoc.filters.anchors.AnchorFilter().run(lines)

        # Fix cross references
        if self.filter_xrefs:
            lines = mkdocs_pandoc.filters.xref.XrefFilter().run(lines)

        if self.filter_toc:
            lines = mkdocs_pandoc.filters.toc.TocFilter().run(lines)

        if self.filter_tables:
            lines = mkdocs_pandoc.filters.tables.TableFilter().run(lines)

        return(lines)
