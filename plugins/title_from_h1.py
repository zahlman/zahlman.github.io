# -*- coding: utf-8 -*-

from nikola.plugin_categories import MetadataExtractor
from nikola.metadata_extractors import MetaSource, MetaPriority
import re


class TitleFromH1(MetadataExtractor):
    """A metadata extractor that looks for Markdown h1 formatting
    (a line starting with `#`) and creates `title` and `html_title` metadata.
    """
    name = 'title_from_h1'
    source = MetaSource.text
    priority = MetaPriority.specialized
    supports_write = False
    split_metadata_re = re.compile('\n\n')
    h1_re = re.compile(r'^# (.*)')
    tag_re = re.compile(r'<.*?>')

    def _extract_metadata_from_text(self, source_text: str) -> dict:
        """Extract metadata from text."""
        title, formatted_title = '', ''
        for line in source_text.split('\n'):
            match = self.h1_re.match(line)
            if not match:
                continue
            text = match.group(1)
            if formatted_title:
                formatted_title += f'<br><small>{text}</small>'
            else:
                formatted_title = text
            filtered = self.tag_re.sub('', text)
            if title:
                title += f' &mdash; {filtered}'
            else:
                title = filtered
        return {'title': title, 'formatted_title': formatted_title}
