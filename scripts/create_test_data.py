#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Create testdata for extractor tests"""

import argparse
from  gallery_dl import job, config, extractor

TESTDATA_FMT = """
    test = [("{}", {{
        "url": "{}",
        "keyword": "{}",
        "content": "{}",
    }})]
"""

TESTDATA_EXCEPTION_FMT = """
    test = [("{}", {{
        "exception": "{}",
    }})]
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", action="store_true")
    parser.add_argument("--recreate", action="store_true")
    parser.add_argument("urls", nargs="*")
    args = parser.parse_args()

    if args.recreate:
        urls = [
            test[0]
            for extr in extractor.extractors() if extr.category in args.urls
            for test in extr.test
        ]
    else:
        urls = args.urls

    config.load()
    for url in urls:
        tjob = job.TestJob(url, content=args.content)
        try:
            tjob.run()
        except Exception as exc:
            fmt = TESTDATA_EXCEPTION_FMT
            data = (exc.__class__.__name__,)
        else:
            fmt = TESTDATA_FMT
            data = (tjob.hash_url.hexdigest(),
                    tjob.hash_keyword.hexdigest(),
                    tjob.hash_content.hexdigest())
        print(tjob.extractor.__class__.__name__)
        print(fmt.format(url, *data))

if __name__ == '__main__':
    main()
