#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest
from pathlib import Path
from typing import Union, TypeAliasType

from pathorstr import PathOrStr

class TestCasePathOrStr_01:

    def test_type_specifix(self):
        assert type(PathOrStr) is Union or TypeAliasType
