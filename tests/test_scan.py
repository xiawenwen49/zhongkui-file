import unittest
from pathlib import Path
from zhongkui.logging import initConsoleLogging
from zhongkui.file.scan import (diecScan, ssdeepScan, exiftoolScan, tridScan,
                                magicScan, pefileScan)

MALWARE = Path(__file__).resolve().parent.joinpath("sample")
RESULT = Path(__file__).resolve().parent.joinpath("result")


class TestFileScan(unittest.TestCase):
    @classmethod
    def setUp(cls):
        initConsoleLogging()

    def test_diecScan(self):
        target = MALWARE.joinpath("pe_upx")
        expect = {
            "packer": "UPX(3.95)[NRV,brute]",
            "compiler": "Borland Delphi(-)[-]",
            "linker": "Turbo Linker(2.25*,Delphi)[EXE32,admin]"
        }

        self.assertDictEqual(expect, diecScan(target))

    def test_diecScan_elf(self):
        target = MALWARE.joinpath("elf")
        expect_packer = "UPX(3.91)[NRV,brute]"
        self.assertEqual(expect_packer, diecScan(target).get("packer"))

    def test_ssdeepScan(self):
        target = MALWARE.joinpath("pe")
        expect = {
            "ssdeep":
            "98304:xhvQdnJ46ub80MndJg1SYArmNTmwR9TOI:LKJ46C8XpYArmNTm6TOI"
        }

        self.assertEqual(expect, ssdeepScan(target))

    def test_exiftoolScan(self):
        target = MALWARE.joinpath("pe")
        ignores = ("FileModifyDate", "FileAccessDate", "FileInodeChangeDate")
        expect = {
            "FileSize": "3.7 MB",
            "FileType": "Win32 EXE",
            "FileTypeExtension": "exe",
            "MIMEType": "application/octet-stream",
            "MachineType": "Intel 386 or later, and compatibles",
            "TimeStamp": "1992:06:19 22:22:17+00:00",
            "ImageFileCharacteristics":
            "Executable, No line numbers, No symbols, Bytes reversed lo, 32-bit, Bytes reversed hi",
            "PEType": "PE32",
            "LinkerVersion": 2.25,
            "CodeSize": 1985536,
            "InitializedDataSize": 1913344,
            "UninitializedDataSize": 0,
            "EntryPoint": "0x1e5788",
            "OSVersion": 4.0,
            "ImageVersion": 0.0,
            "SubsystemVersion": 4.0,
            "Subsystem": "Windows GUI",
            "FileVersionNumber": "5.7.1.110",
            "ProductVersionNumber": "5.7.1.110",
            "FileFlagsMask": "0x003f",
            "FileOS": "Win32",
            "ObjectFileType": "Executable application",
            "FileSubtype": 0,
            "LanguageCode": "English (U.S.)",
            "CharacterSet": "Windows, Latin1",
            "FileDescription": "Windows softapp",
            "FileVersion": "5.7.1.110",
            "ProductVersion": "5.7.1.110"
        }
        r = exiftoolScan(target)
        for k in ignores:
            r.pop(k, [])
        self.assertDictEqual(r, expect)

    def test_tridScan(self):
        target = MALWARE.joinpath("pe")
        expect = {
            "InstallShield setup": "53.9%",
            "Win32 Executable Delphi generic": "17.7%",
            "DOS Borland compiled Executable": "12.5%",
            "Win32 Executable": "5.6%",
            "Win16/32 Executable Delphi generic": "2.5%"
        }
        self.assertDictEqual(tridScan(target), expect)

    def test_tridScan_html(self):
        target = MALWARE.joinpath("html")
        expect = {
            "HyperText Markup Language with DOCTYPE": "80.6%",
            "HyperText Markup Language": "19.3%"
        }
        self.assertDictEqual(tridScan(target), expect)

    def test_magicScan(self):
        target = MALWARE.joinpath("pe")
        expect = {
            "mime_type": 'application/x-dosexec',
            "encoding": 'binary',
            "type_name": 'PE32 executable (GUI) Intel 80386, for MS Windows'
        }
        self.assertDictEqual(magicScan(target), expect)

    def test_pefileScan(self):
        target = MALWARE.joinpath("pe")
        expect_header = {
            "timestamp": "1992-06-19 22:22:17",
            "sections": 8,
            "entryPoint": "1988488"
        }
        expect_section_code = {
            "name": "CODE",
            "virtualAddress": "4096",
            "virtualSize": "1985032",
            "rawSize": "1985536",
            "entropy": 6.56,
            "md5": "c7b200326db8ad5b69699767f6e2f2a7"
        }
        expect_import_advapi32 = {
            "dllName": "advapi32.dll",
            "importFunctions":
            ["RegQueryValueExA", "RegOpenKeyExA", "RegCloseKey"]
        }
        expect_sum_import = 21

        pefile_info = pefileScan(target)

        self.assertDictEqual(expect_header, pefile_info["header"])
        self.assertDictEqual(expect_section_code, pefile_info["sections"][0])
        self.assertDictEqual(expect_import_advapi32, pefile_info["imports"][2])
        self.assertEqual(expect_sum_import, len(pefile_info["imports"]))
