import os
import math
import shutil
import hashlib
import binascii
import tempfile
from pathlib import Path
from collections import Counter
from dataclasses import asdict
from typing import Dict, Any
from .exceptions import ZhongkuiCriticalError
from .model import (DIEC, PEFILE, FILETYPE, EXIFTOOL, STATICINFO,
                    FileinfoBasic)
from .scan import (exiftoolScan, ssdeepScan, magicScan, pefileScan, tridScan,
                   diecScan)

FILE_CHUNK_SIZE = 16 * 1024 * 1024


def temppath():
    """Returns temporary directory."""
    tmppath = Path(tempfile.gettempdir()).joinpath("zhongkui-tmp")

    if not tmppath.exists():
        os.mkdir(tmppath)

    return tmppath


class Storage:
    @staticmethod
    def getFilenameFromPath(path: Path) -> str:
        return Path(path).name
        
    @staticmethod
    def tempPut(content, path: Path = None) -> Path:
        """Store a temporary file or files.
        Args:
            content: the content of this file
            path: directory path to store the file
        Return:
            filepath
        """
        fd, filepath = tempfile.mkstemp(
            prefix="upload_", dir=path or temppath())

        if hasattr(content, "read"):
            chunk = content.read(1024)
            while chunk:
                os.write(fd, chunk)
                chunk = content.read(1024)
        else:
            os.write(fd, content)

        os.close(fd)
        return filepath

    @staticmethod
    def tempNamedPut(content, filename, path: Path = None) -> Path:
        """Store a named temporary file.
        Args:
            content: the content of this file
            filename: filename that the file should have
            path: directory path to store the file
        Return:
            full path to the temporary file
        """
        filename = Storage.getFilenameFromPath(filename)
        dirpath = tempfile.mkdtemp(dir=path or temppath())
        Storage.create(dirpath, filename, content)
        return Path(dirpath).joinpath(filename)

    @staticmethod
    def create(root, filename, content):
        if isinstance(root, (tuple, list)):
            root = Path().joinpath(*root)

        filepath = Path(root).joinpath(filename)
        with open(filepath, "wb") as f:
            if hasattr(content, "read"):
                chunk = content.read(1024 * 1024)
                while chunk:
                    f.write(chunk)
                    chunk = content.read(1024 * 1024)
            else:
                f.write(content)
        return filepath

    @staticmethod
    def delete(folder: Path):
        # if Path(file).exists():
        #     try:
        #         os.remove(file)
        #     except OSError:
        #         raise ZhongkuiCriticalError(
        #             "Unable to delete file: {}".format(file))
        if Path(folder).exists():
            try:
                shutil.rmtree(folder)
            except OSError:
                raise ZhongkuiCriticalError(
                    "Unable to delete folder: {}".format(folder))

    @staticmethod
    def copy(path_target: Path, path_dest: Path) -> Path:
        """Copy a file. The destination may be a directory.
        Return:
            path to the file or directory
        """
        shutil.copy(src=path_target, dst=path_dest)
        return Path(path_dest).joinpath(Path(path_target).name)


class File(Storage):
    """zhongkui basic file class"""

    def __init__(self, file_path, temporary=False):
        """
        Args:
            file_path: file path.
            temporary: is the file temporary
        """
        self.file_path = file_path
        self.temporary = temporary

        # for cache property
        self._file_data = None
        self._crc32 = None
        self._md5 = None
        self._sha256 = None
        self._sha1 = None
        self._sha512 = None
        self._ssdeep = None
        self._is_probably_packed = None

        # for cache info
        self._basic = None
        self._trid = None
        self._magic = None
        self._pefile = None
        self._diec = None
        self._exiftool = exiftoolScan(self.file_path)

    def isValid(self):
        return (self.file_path and Path(self.file_path).exists()
                and Path(self.file_path).is_file()
                and os.path.getsize(self.file_path) != 0)

    def getChunks(self):
        """Read file contents in chunks (generator)."""

        with open(self.file_path, "rb") as fd:
            while True:
                chunk = fd.read(FILE_CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk

    def calcEntropy(self, data=None):
        """calcuate the entropy of a chunk of data"""
        if data is None:
            return 0.0

        cnt = Counter(bytearray(data))
        entropy = 0
        for i in cnt.values():
            p_i = float(i) / len(data)
            entropy -= p_i * math.log(p_i, 2)

        return entropy

    def calcHashes(self):
        """Calculate all possible hashes for this file."""
        crc = 0
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()
        sha512 = hashlib.sha512()

        for chunk in self.getChunks():
            crc = binascii.crc32(chunk, crc)
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
            sha512.update(chunk)

        self._crc32 = "".join(
            "%02X" % ((crc >> i) & 0xff) for i in [24, 16, 8, 0])
        self._md5 = md5.hexdigest()
        self._sha1 = sha1.hexdigest()
        self._sha256 = sha256.hexdigest()
        self._sha512 = sha512.hexdigest()

    @property
    def fileName(self):
        return Path(self.file_path).name

    @property
    def fileType(self):
        return self._exiftool.get(EXIFTOOL.FILETYPE)

    @property
    def fileData(self):
        if self._file_data is None:
            with open(self.file_path, "rb") as f:
                self._file_data = f.read()
        return self._file_data

    @property
    def fileSize(self):
        return os.path.getsize(self.file_path)

    @property
    def md5(self):
        if self._md5 is None:
            self.calcHashes()
        return self._md5

    @property
    def sha1(self):
        if self._sha1 is None:
            self.calcHashes()
        return self._sha1

    @property
    def sha256(self):
        if self._sha256 is None:
            self.calcHashes()
        return self._sha256

    @property
    def sha512(self):
        if self._sha512 is None:
            self.calcHashes()
        return self._sha512

    @property
    def crc32(self):
        if self._crc32 is None:
            self.calcHashes()
        return self._crc32

    @property
    def ssdeep(self):
        if self._ssdeep is None:
            self._ssdeep = ssdeepScan(self.file_path).get("ssdeep")
        return self._ssdeep

    @property
    def packer(self):
        """return file packer name and version if exit"""
        return self.getDiec().get(DIEC.PACKER)

    @property
    def isProbablyPacked(self) -> bool:
        """A file is probably packed:
        1. detect packer;
        2. entropy of at least 20% data > 7.4.
        """
        if self._is_probably_packed is not None:
            return self._is_probably_packed

        if self.packer is not None:
            self._is_probably_packed = True
            return True

        # pe
        if self.fileType in FILETYPE.WINEXE:
            self._is_probably_packed = self.getPefile().get(
                PEFILE.ISPROBABLYPACKED)

        # # elf
        # if self.fileType in FILETYPE.LINUXELF:
        #     # TODO: add pyelftools to calculate `section` entropy
        #     raise NotImplementedError

        # others
        total_file_data = self.fileData
        total_compressed_data = 0

        for data in self.getChunks():
            ck_entropy = self.calcEntropy(data)
            ck_length = len(data)
            if ck_entropy > 7.4:
                total_compressed_data += ck_length
        if ((1.0 * total_compressed_data) / total_file_data) > 0.2:
            self._is_probably_packed = True
        else:
            self._is_probably_packed = False

        return self._is_probably_packed

    def getTrid(self):
        """file component info"""
        if self._trid is None:
            self._trid = tridScan(self.file_path)
        return self._trid

    def getMagic(self):
        """file magic info"""
        if not self._magic:
            self._magic = magicScan(self.file_path)
        return self._magic

    def getExiftool(self):
        """file exiftool info"""
        return self._exiftool

    def getPefile(self):
        """pefile info"""
        if self.fileType in FILETYPE.WINEXE:
            if self._pefile is None:
                self._pefile = pefileScan(self.file_path)
        return self._pefile

    def getDiec(self):
        """diec info"""
        if not self._diec_info:
            self._diec_info = diecScan(self.file_path)

        return self._diec_info

    def getBasicInfo(self):
        """file basic info"""
        if self._basic_info is None:
            # basic info
            basic_info = FileinfoBasic()
            basic_info.name = self.name
            basic_info.md5 = self.md5
            basic_info.sha256 = self.sha256
            basic_info.crc32 = self.crc32
            basic_info.fileType = self.fileType
            basic_info.magic = self.getMagic()
            basic_info.ssdeep = self.ssdeep
            basic_info.trid = self.getTrid()
            basic_info.packer = self.packer
            basic_info.isProbablyPacked = self.isProbablyPacked
            basic_info.fileSize = self.getExiftool().get(EXIFTOOL.FILESIZE)
            # basic_info.familyType = self.family_type
            self._basic_info = asdict(basic_info)

        return self._basic_info

    def getAllInfo(self) -> Dict[str, Any]:
        """file all info"""
        infos = {}
        infos[STATICINFO.BASIC] = self.getBasicInfo()
        infos[STATICINFO.PE] = self.getPefile()
        infos[STATICINFO.DIEC] = self.getDiec()
        infos[STATICINFO.EXIFTOOL] = self.getExiftool()
