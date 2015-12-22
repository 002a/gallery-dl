# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract image-urls from https://yande.re/"""

from . import booru

class YandereExtractor(booru.JSONBooruExtractor):
    """Base class for yandere extractors"""
    category = "yandere"
    api_url = "https://yande.re/post.json"

class YandereTagExtractor(YandereExtractor, booru.BooruTagExtractor):
    """Extract images from yandere based on search-tags"""
    subcategory = "tag"
    pattern = [r"(?:https?://)?(?:www\.)?yande\.re/post\?tags=([^&]+)"]
    test = [("https://yande.re/post?tags=ouzoku armor", {
        "content": "59201811c728096b2d95ce6896fd0009235fe683",
    })]

class YanderePoolExtractor(YandereExtractor, booru.BooruPoolExtractor):
    """Extract image-pools from yandere"""
    subcategory = "pool"
    pattern = [r"(?:https?://)?(?:www\.)?yande.re/pool/show/(\d+)"]
    test = [("https://yande.re/pool/show/318", {
        "content": "2a35b9d6edecce11cc2918c6dce4de2198342b68",
    })]

class YanderePostExtractor(YandereExtractor, booru.BooruPostExtractor):
    """Extract single images from yandere"""
    subcategory = "post"
    pattern = [r"(?:https?://)?(?:www\.)?yande.re/post/show/(\d+)"]
    test = [("https://yande.re/post/show/51824", {
        "content": "59201811c728096b2d95ce6896fd0009235fe683",
    })]
