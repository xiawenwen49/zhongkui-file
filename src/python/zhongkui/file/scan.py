import os
import logging
import json
import magic
import pefile
import tempfile
from peutils import is_probably_packed
from datetime import datetime
from subprocess import Popen, PIPE, TimeoutExpired
from pathlib import Path
from typing import Dict
from dataclasses import asdict
from .exceptions import ZhongkuiScanError
from .model import PEfileInfo, PESection, PEImport

log = logging.getLogger(__name__)


def exiftoolScan(target: Path) -> Dict[str, str]:
    '''exiftool scan target
    Args:
        target: A Path to target file
    Raise:
        ZhongkuiScanError
    Return:
        A dict result
    '''
    log.info("start exftoolScan...")
    # ? http://owl.phy.queensu.ca/~phil/exiftool/exiftool_pod.html#Input-output-text-formatting
    # -charset [[TYPE=]CHARSET]        Specify encoding for special characters
    # -j[[+]=JSONFILE] (-json)         Export/import tags in JSON format
    args = ('exiftool', '-charset', 'utf-8', '-json', target)
    proc = Popen(args, stdout=PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    if stderr:
        log.error("exiftoolScan stderr: {}".format(stderr))

    try:
        stdout = stdout.decode('utf-8', errors='ignore')
        results = json.loads(stdout)[0]
    except Exception as e:
        log.error("exiftoolScan json load error: {}".format(e))
        raise ZhongkuiScanError("exiftoolScan json loads error: {}".format(e))

    ignores = [
        'SourceFile', 'ExifToolVersion', 'FileName', 'Directory',
        'FilePermissions', ''
    ]

    nulls = ('', '(none)')

    # filter results
    for k, v in results.items():
        if v in nulls:
            ignores.append(k)

    for key in ignores:
        results.pop(key, [])

    return results


def ssdeepScan(target: Path) -> Dict[str, str]:
    '''ssdeep scan target
    Args:
        target: A Path to target file
    Raise:
        ZhongkuiScanError
    Return:
        A dict result
    '''
    log.info("start ssdeepScan...")
    # ? ssdeep -h
    # -c - Prints output in CSV format
    args = ('ssdeep', '-c', target)
    proc = Popen(args, stdout=PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    if stderr:
        log.error("ssdeepScan stderr: {}".format(stderr))

    try:
        stdout = stdout.decode('utf-8', errors='ignore')
        # ? ssdeep output example
        # ssdeep,1.1--blocksize:hash:hash,filename
        # 98304:xhvQdnJ46ub80MndJg1SYArmNTmwR9TOI:LKJ46C8XpYArmNTm6TOI,"/fileinfo/tests/malware"
        results = {'ssdeep': stdout.splitlines()[1].split(',')[0]}
    except Exception as e:
        log.error("ssdeepScan parse error: {}".format(e))
        raise ZhongkuiScanError("ssdeepScan parse error: {}".format(e))

    return results


def diecScan(target: Path) -> Dict[str, str]:
    '''diec scan target
    Args:
        target: A Path to target file
    Raise:
        ZhongkuiScanError
    Return:
        A dict result
    '''
    log.info("start diecScan...")
    args = ('diec', target)
    proc = Popen(args, stdout=PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    if stderr:
        log.error("diecScan stderr: {}".format(stderr))

    tkeys = ("packer", "protector", "compiler", 'linker')
    results = {}

    try:
        stdout = stdout.decode('utf-8', errors='ignore')
        for line in stdout.splitlines():
            line_split = line.split(':')
            key = line_split[1].strip()
            if key in tkeys:
                val = [v.strip() for v in line_split[2:]]  # combine val
                val = ':'.join(val)
                results.update({key: val})
    except Exception as e:
        log.error("diecScan parse error: {}".format(e))
        raise ZhongkuiScanError("diecScan parse error: {}".format(e))

    return results


def tridScan(target: Path) -> Dict[str, str]:
    '''trid scan target
    Args:
        target: A Path to target file
    Raise:
        ZhongkuiScanError
    Return:
        A dict result
    '''
    log.info("start tridScan...")
    args = ('trid', target)
    proc = Popen(args, stdout=PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    if stderr:
        log.error("tridScan stderr: {}".format(stderr))

    results = {}

    try:
        stdout = stdout.decode('utf-8', errors='ignore')
        for line in stdout.splitlines():
            if "%" not in line:
                continue

            line_split = line.split('(')
            val = line_split[0].strip()
            key = line_split[1].split(')')[1].strip()
            results.update({key: val})
    except BaseException as e:
        log.error("tridScan parse error: {}".format(e))
        raise ZhongkuiScanError("tridScan parse error: {}".format(e))

    return results


def magicScan(target: Path) -> Dict[str, str]:
    '''trid scan target
    Args:
        target: A Path to target file
    Return:
        A dict result
    '''
    detected = magic.detect_from_filename(target)

    return {
        "mime_type": detected.mime_type,
        "encoding": detected.encoding,
        "type_name": detected.name
    }


def pefileScan(target: Path) -> Dict[str, str]:
    '''pefile scan target
    Args:
        target: A Path to target file
    Raise:
        ZhongkuiScanError
    Return:
        A dict result
    '''
    pe = pefile.PE(target)
    pe_info = PEfileInfo()

    try:
        # parse header
        pe_info.header.timestamp = str(
            datetime.fromtimestamp(pe.FILE_HEADER.TimeDateStamp))
        pe_info.header.sections = pe.FILE_HEADER.NumberOfSections
        pe_info.header.entryPoint = str(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
        # parse sections
        for section in pe.sections:
            sec_info = PESection()
            sec_info.name = bytes(
                [i for i in section.Name if i != 0]).decode("utf-8")
            sec_info.virtualAddress = str(section.VirtualAddress)
            sec_info.virtualSize = str(section.Misc_VirtualSize)
            sec_info.rawSize = str(section.SizeOfRawData)
            sec_info.entropy = round(section.get_entropy(), 2)
            sec_info.md5 = section.get_hash_md5()
            pe_info.sections.append(sec_info)
        # parse imports
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            imp_info = PEImport()
            imp_info.dllName = entry.dll.decode("utf-8")
            imp_info.importFunctions = [
                imp.name.decode("utf-8") for imp in entry.imports
            ]
            pe_info.imports.append(imp_info)
        # is_probably_packed
        pe_info.isProbablyPacked = is_probably_packed(pe)
    except Exception as e:
        log.error("pefile parse error: {}".format(e))
        raise ZhongkuiScanError("pefile parse error: {}".format(e))

    return asdict(pe_info)