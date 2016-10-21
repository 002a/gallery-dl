# -*- coding: utf-8 -*-

# Copyright 2016 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract manga-chapters from https://kobato.hologfx.com/"""

from .powermanga import PowermangaChapterExtractor

class DokireaderChapterExtractor(PowermangaChapterExtractor):
    """Extractor for manga-chapters from kobato.hologfx.com"""
    category = "dokireader"
    subcategory = "chapter"
    pattern = [(r"(?:https?://)?kobato\.hologfx\.com/reader/read/"
                r"(.+/([a-z]{2})/\d+/\d+)")]
    test = [("https://kobato.hologfx.com/reader/read/hitoribocchi_no_oo_seikatsu/en/3/34", {
        "keyword": "303f3660772dd393ce01cf248f5cf376629aebc7",
    })]

    def __init__(self, match):
        PowermangaChapterExtractor.__init__(self, match)
        self.url_base = "https://kobato.hologfx.com/reader/read/"
