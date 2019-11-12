import unittest
import tempfile
import json
from pathlib import Path
from zhongkui.logging import initConsoleLogging
from zhongkui.file import File, Storage

MALWARE = Path(__file__).resolve().parent.joinpath("sample")
RESULT = Path(__file__).resolve().parent.joinpath("result")


class TestStorage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        initConsoleLogging()
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
        self.file = File(MALWARE.joinpath("pe"))

    def test_isValid(self):
        assert self.file.isValid()

    def test_getAllInfo(self):
        self.file.getAllInfo()
        result = self.file.getBasicInfo()
        assert result is not None
        with open(RESULT.joinpath("fileInfo.json"), "w") as f:
            json.dump(result, f)
            