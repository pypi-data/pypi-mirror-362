#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class OsType(Enum):
    IOS = "IOS"
    ANDROID = "ANDROID"

    def to_aps_dict(self):
        return self.name
