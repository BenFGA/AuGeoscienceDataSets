import unittest
from src.augeosciencedatasets import readers
from pathlib import Path

class ReadFiles(unittest.TestCase):
    filepath = Path('examples','data')
    def test_no_defaults(self):
        readers.dmp(self.filepath.joinpath('a126037_mj_wasg4_surf2020a.txt'))
    def test_change_encoding_1(self):
        readers.dmp(self.filepath.joinpath('a126051_ta_wasl4_ass_rk2020f.txt'),encoding='utf-16')
    def test_change_encoding_2(self):
        readers.dmp(self.filepath.joinpath('a126051_ta_wasl4_geo_2020f.txt'),encoding='utf-16')

if __name__ == '__main__':
    unittest.main()