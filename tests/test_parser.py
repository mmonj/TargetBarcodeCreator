import os
import sys

testdir = os.path.dirname(__file__)
srcdir = '../src'
srcdir = os.path.abspath(os.path.join(testdir, srcdir))
sys.path.insert(0, srcdir)
os.chdir(srcdir)

import unittest
import data_parser

class Tester(unittest.TestCase):
    def test_data_parser(self):
        items = data_parser.parse_item_dump()
        [print(f) for f in items]
