# -*- coding: utf-8 -*-

# Copyright 2018 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Common classes and constants used by postprocessor modules."""

from . import log


class PostProcessor():
    log = log

    def run(self, pathfmt):
        raise NotImplementedError()
