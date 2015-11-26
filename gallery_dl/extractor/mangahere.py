# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract manga pages from http://www.mangahere.co/"""

from .common import AsynchronousExtractor, Message
from .. import text
import re

class MangaHereExtractor(AsynchronousExtractor):

    category = "mangahere"
    directory_fmt = ["{category}", "{manga}", "c{chapter:>03}"]
    filename_fmt = "{manga}_c{chapter:>03}_{page:>03}.{extension}"
    pattern = [r"(?:https?://)?(?:www\.)?mangahere\.co/manga/([^/]+(?:/v0*(\d+))?/c0*(\d+))"]
    url_fmt = "http://www.mangahere.co/manga/{}/{}.html"

    def __init__(self, match):
        AsynchronousExtractor.__init__(self)
        self.part = match.group(1)
        self.volume = match.group(2)
        self.chapter = match.group(3)

    def items(self):
        page = self.request(self.url_fmt.format(self.part, 1)).text
        data = self.get_job_metadata(page)
        yield Message.Version, 1
        yield Message.Directory, data.copy()
        for i, url in zip(range(int(data["count"])), (self.get_image_urls(page))):
            data["page"] = i+1
            text.nameext_from_url(url, data)
            yield Message.Url, url, data.copy()

    def get_job_metadata(self, page):
        """Collect metadata for extractor-job"""
        manga, pos = text.extract(page, '<title>', '</title>')
        chid , pos = text.extract(page, 'a.mhcdn.net/store/manga/', '/', pos)
        _    , pos = text.extract(page, '<select class="wid60"', '', pos)
        _    , pos = text.extract(page, '</select>', '', pos)
        count, pos = text.extract(page, '>', '<', pos-30)
        manga = re.match(r"(.+) \d+ - Read .+ Chapter \d+ Online", manga).group(1)
        return {
            "category": self.category,
            "manga": text.unescape(manga),
            # "title": TODO,
            "volume": self.volume or "",
            "chapter": self.chapter,
            "chapter-id": chid,
            "count": count,
            "lang": "en",
            "language": "English",
        }

    def get_image_urls(self, page):
        """Yield all image-urls for this chapter"""
        pnum = 1
        while True:
            url, pos = text.extract(page, '<img src="', '"')
            yield url
            _  , pos = text.extract(page, '<img src="', '"', pos)
            url, pos = text.extract(page, '<img src="', '"', pos)
            yield url
            pnum += 2
            page = self.request(self.url_fmt.format(self.part, pnum)).text
