from typing import List, Dict
from dataclasses import dataclass, field


class MAGIC:
    MIME = "mime_type"
    ENCODING = "encoding"
    TYPE = "type_name"


class DIEC:
    PROTECTOR = "protector"
    PACKER = "packer"
    COMPILER = "compiler"
    LINKER = 'linker'


class STATICINFO:
    BASIC = "basicInfo"
    DIEC = "diecInfo"
    PE = "peInfo"
    EXIFTOOL = "exiftoolInfo"


class PEFILE:
    ISPROBABLYPACKED = "isProbablyPacked"


class FILETYPE:
    PE = ("Win32 EXE", "Win32 DLL", "Win64 DLL", "Win64 EXE")
    ELF = ("ELF executable", "ELF shared library")


class EXIFTOOL:
    FILESIZE = "FileSize"
    FILETYPE = "FileType"
    FILETYPEEXTENSION = "FileTypeExtension"


@dataclass
class FileinfoBasic:
    name: str = field(default="")
    md5: str = field(default="")
    sha256: str = field(default="")
    # crc32: str = field(default="")
    fileType: str = field(default="")
    magic: str = field(default="")
    # ssdeep: str = field(default="")
    trid: Dict[str, str] = field(default_factory=dict)
    packer: str = field(default="")
    isProbablyPacked: bool = field(default=False)
    # unpackedFile: str = field(default="")
    fileSize: str = field(default="")
    familyType: str = field(default="")
    timeStamp: str = field(default="")


# pe header
@dataclass
class PEHeader:
    timestamp: str = field(default="")
    entryPoint: str = field(default="")
    sections: int = field(default=0)


# pe section
@dataclass
class PESection:
    name: str = field(default="")
    virtualAddress: str = field(default="")
    virtualSize: str = field(default="")
    rawSize: str = field(default="")
    entropy: float = field(default=0.0)
    md5: str = field(default="")


# pe imports:
@dataclass
class PEImport:
    dllName: str = field(default="")
    importFunctions: List[str] = field(default_factory=list)


# pefile info
@dataclass
class PEfileInfo:
    header: PEHeader = field(default_factory=PEHeader)
    sections: List[PESection] = field(default_factory=list)
    imports: List[PEImport] = field(default_factory=list)
    isProbablyPacked: bool = field(default=False)