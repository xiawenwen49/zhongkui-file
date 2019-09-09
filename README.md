# zhongkui-file

zhongkui file utils package

## Relases

- 1.0.5
```shell
2019-09-07
add TempPath
```

- 1.0.4

```shell
2019-08-23 release
fix tridScan parse error
```

- 1.0.3

```shell
2019-08-23 release
fixed isProbablyPacked
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

### Prerequisites

- ubuntu >= 18.04
- python >= 3.7.3

details in `docker/Dockerfile`;

### Installing

`pip install zhongkui-file`

or use docker (`>=18.09.5`)

```shell
$ git clone ssh://git@git.kongkongss.com:222/jyker/zhongkui-file.git
$ cd zhongkui-file
$ make build
$ make test
```
[How to use our harbor](https://www.kongkongss.com/pages/viewpage.action?pageId=65835)

## Running the tests

```shell
$ cd zhongkui-file
$ pytest
```

## Versioning
latest version is avaiable in [pypi](https://pypi.org/project/zhongkui-file/)

## TODOs

- add `pyelftools` to calculate `section` entropy of `elf`
- parse `apk`
- parse `elf`

## Authors

* **kongkong Jiang** - *Initial work* - [jyker](https://git.kongkongss.com/jyker)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details