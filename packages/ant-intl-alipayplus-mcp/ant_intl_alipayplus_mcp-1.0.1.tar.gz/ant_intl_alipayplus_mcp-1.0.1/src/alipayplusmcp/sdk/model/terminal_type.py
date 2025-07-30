#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class TerminalType(Enum):
    WEB = "WEB"
    WAP = "WAP"
    APP = "APP"
    MINI_APP = "MINI_APP"

    def to_aps_dict(self):
        return self.name
