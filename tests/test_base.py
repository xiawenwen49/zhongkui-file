import unittest
import tempfile
import json
from pathlib import Path
from .test import MALWARE, RESULT
from zhongkui.file.base import File, Storage


class TestStorage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open(MALWARE.joinpath("pe_upx"), "rb") as fb:
            self.data = fb.read()

    def test_tempPut(self):
        fpath = Storage.tempPut(self.data)
        assert Path(fpath).is_file()
        Storage.delete(fpath)

    def test_create(self):
        fpath = Storage.create(tempfile.gettempdir(), "pe_upx", self.data)
        assert Path(fpath).is_file()
        Storage.delete(fpath)


class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.file = File(MALWARE.joinpath("pe_upx"))

    def test_isValid(self):
        assert self.file.isValid()

    def test_getAllInfo(self):
        result = self.file.getAllInfo()
        with open(RESULT.joinpath("fileInfo.json"), "w") as f:
            json.dump(result, f)