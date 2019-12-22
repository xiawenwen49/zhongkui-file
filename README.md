# zhongkui-file

zhongkui file analysis package


## Installation

- run zhongkui-file in docker

```bash
$ git clone git@git.kongkongss.com:zhongkui/zhongkui-file.git
$ cd zhongkui-file
$ make dev
# in docker `run as developer`
$ pip install zhongkui-file -e .
```

## Getting Started

```shell
>>> from zhongkui.file import File
>>> sample = File("tests/sample/pe_upx")
>>> print(sample.getBasicInfo())
>>>
{
    "name": "pe",
    "md5": "ff2a00e3d07afcf32a7459040bc9cc41",
    "sha256": "fb12aec2553bd2567a82f18ca2e0710e8d72b22b1d2bdcf3a296e987ad3c398a",
    "fileType": "Win32 EXE",
    "magic": {
        "mime_type": "application/x-dosexec",
        "encoding": "binary",
        "type_name": "PE32 executable (GUI) Intel 80386, for MS Windows"
    },
    "trid": {
        "InstallShield setup": "53.9%",
        "Win32 Executable Delphi generic": "17.7%",
        "DOS Borland compiled Executable": "12.5%",
        "Win32 Executable": "5.6%",
        "Win16/32 Executable Delphi generic": "2.5%"
    },
    "packer": null,
    "isProbablyPacked": true,
    "fileSize": "3.7 MB",
    "familyType": "",
    "timeStamp": "1992:06:19 22:22:17+00:00"
}
```


## Running the tests

```shell
$ cd zhongkui-file
$ pytest -s
```

## Changelog
[release Changelog](./CHANGELOG.md)

## TODOs

- parse `elf` [#2](https://git.kongkongss.com/jyker/zhongkui-file/issues/2)
- add `pyelftools` to calculate `section` entropy of `elf` [#3](https://git.kongkongss.com/jyker/zhongkui-file/issues/3)
- add `stringsifter` to parse string [#1](https://git.kongkongss.com/jyker/zhongkui-file/issues/1)

## Authors

* **kongkong Jiang** - *Initial work* - [jyker](https://git.kongkongss.com/jyker)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
