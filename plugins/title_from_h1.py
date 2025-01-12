# -*- coding: utf-8 -*-

from nikola.plugin_categories import MetadataExtractor
from nikola.metadata_extractors import MetaSource, MetaPriority
import re


class _accumulated:
    tag_re = re.compile(r'<.*?>')


    def __init__(self):
        self._title, self._formatted_title = '', ''
        self._category, self._tags = None, []


    def _add_tag(self, tag):
        self._tags.append(tag)


    def _set_category(self, category):
        if self._category is not None:
            raise ValueError("May only mark one category.")
        self._category = category


    def _formatted_line(self, line):
        return f'<br><small>{line}</small>' if self._formatted_title else line


    def _plain_line(self, line):
        line = self.tag_re.sub('', line)
        return f' - {line}' if self._title else line


    def add(self, title, markings):
        self._formatted_title += self._formatted_line(title)
        self._title += self._plain_line(title)
        for marking in markings.split():
            action = {'@': self._set_category, '#': self._add_tag}[marking[0]]
            action(marking[1:])


    def result(self):
        result = {
            'title': self._title, 'formatted_title': self._formatted_title,
            'tags': self._tags
        }
        if self._category is not None:
            result['category'] = self._category
        return result


class TitleFromH1(MetadataExtractor):
    """A metadata extractor that looks for Markdown h1 formatting
    (a line starting with `#`) and creates `title` and `html_title` metadata.
    """
    name = 'title_from_h1'
    source = MetaSource.text
    priority = MetaPriority.specialized
    supports_write = False
    split_metadata_re = re.compile('\n\n')
    h1_re = re.compile(r'^# (.*?)((?:\s+[#@][a-zA-Z-]+)*)$')


    def _extract_metadata_from_text(self, source_text: str) -> dict:
        """Extract metadata from text."""
        a = _accumulated()
        for line in source_text.split('\n'):
            match = self.h1_re.match(line)
            if match:
                a.add(*match.groups())
        return a.result()
