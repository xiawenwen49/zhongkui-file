# zhongkui-file

zhongkui file analysis package


## Installation

- run zhongkui-file in docker

```bash
$ git clone ssh://git@git.kongkongss.com:222/jyker/zhongkui-file.git
$ cd zhongkui-file
$ make dev
# in docker
$ pip install zhongkui-file
```

## Getting Started

```shell
>>> from zhongkui.file import File
>>> sample = File("tests/sample/pe_upx")
>>> print(sample.getBasicInfo())
>>>
{
    'name': 'pe_upx',
    'md5': '7dc2d5890f2944c4e9365cdebc59f189',
    'sha256':
    'c8ab92f1706a99eff8f9cd91d2551fb78308a775dadb77bbab96360213b62602',
    'crc32': '0CA62494',
    'fileType': 'Win32 EXE',
    'magic': {
        'mime_type':
        'application/x-dosexec',
        'encoding':
        'binary',
        'type_name':
        'PE32 executable (GUI) Intel 80386, for MS Windows, UPX compressed'
    },
    'ssdeep':
    '49152:7M+qNpdkzUiZJpxMRaW+OAji7PzKhEKXzlYusu/WnW5+YPPKBiLPby0nmAezy:4+qOUiZ6oWB/LKPlYusu/WW5+YPPKBiz',
    'trid': {
        ' UPX compressed Win32 Executable ': '58.5%',
        ' Win32 Dynamic Link Library ': '14.2%',
        ' Win32 Executable ': '9.7%',
        ' Win16/32 Executable Delphi generic ': '4.4%',
        ' OS/2 Executable ': '4.3%'
    },
    'packer': 'UPX(3.95)[NRV,brute]',
    'isProbablyPacked': True,
    'unpackedFile': '',
    'fileSize': '1973 kB',
    'familyType': ''
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
