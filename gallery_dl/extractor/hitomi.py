# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from https://hitomi.la/"""

from .common import Extractor, Message
from .. import text
import os.path

info = {
    "category": "hitomi",
    "extractor": "HitomiExtractor",
    "directory": ["{category}", "{gallery-id} {title}"],
    "filename": "{category}_{gallery-id}_{num:>03}_{name}.{extension}",
    "pattern": [
        r"(?:https?://)?hitomi\.la/(?:galleries|reader)/(\d+)\.html",
    ],
}

class HitomiExtractor(Extractor):

    def __init__(self, match):
        Extractor.__init__(self)
        self.gid = match.group(1)

    def items(self):
        page = self.request("https://hitomi.la/galleries/" + self.gid + ".html").text
        data = self.get_job_metadata(page)
        images = self.get_image_urls(page)
        data["count"] = len(images)
        yield Message.Version, 1
        yield Message.Directory, data
        for num, url in enumerate(images, 1):
            name, ext = os.path.splitext(text.filename_from_url(url))
            data["num"] = num
            data["name"] = name
            data["extension"] = ext[1:]
            yield Message.Url, url, data

    def get_job_metadata(self, page):
        """Collect metadata for extractor-job"""
        _     , pos = text.extract(page, '<h1><a href="/reader/', '')
        title , pos = text.extract(page, '.html">', "</a></h1>", pos)
        _     , pos = text.extract(page, '<li><a href="/artist/', '', pos)
        artist, pos = text.extract(page, '.html">', '</a</li>', pos)
        return {
            "category": info["category"],
            "gallery-id": self.gid,
            "title": title,
            "artist": artist,
        }

    @staticmethod
    def get_image_urls(page):
        """Extract and return a list of all image-urls"""
        pos = 0
        images = list()
        while True:
            urlpart, pos = text.extract(page, "'//tn.hitomi.la/smalltn/", ".jpg',", pos)
            if not urlpart:
                return images
            images.append("https://g.hitomi.la/galleries/" + urlpart)
