A python package that extracts rpm package information from rpm database.

Why this and not "rpm" I needed a package that could run on environment without rpm shared libraries installable. This leverage go's portability to enable this.


Example usage

```python

from pyrpmdb import get_rpm_db_info
import json


def test_get_info(file):
    res = get_rpm_db_info(file)
    print(json.dumps(res, indent=4))


test_get_info("foo/bar")
test_get_info("/usr/bin/du")
test_get_info("test-data/centos5-plain-Packages")

```

The result returned is always a dict object for errors  the dictionary returned contains a key;
"error" like;
```python
{
    "error": "path error:foo/bar"
}
```
or
```python
{
    "error": "/usr/bin/du: could not read Go build info from /usr/bin/du: unrecognized file format"
}
```
on success a python list of rpm package info struct is returned of this go structure serialized

```go
{
    Name            string
    Version         string
    Release         string
    Arch            string
    SourceRpm       string
    Size            int
    License         string
    Vendor          string
    Modularitylabel string
    Summary         string
    PGP             string
    SigMD5          string
    InstallTime     int
    BaseNames       []string
    DirIndexes      []int32
    DirNames        []string
    FileSizes       []int32
    FileDigests     []string
    FileModes       []uint16
    FileFlags       []int32
    UserNames       []string
    GroupNames      []string
    
    Provides []string
    Requires []string
}
```
```python
[
    {
        "Name": "package_name",
        "Version": "version",
        "Release": "blah"
    }
]
```
This spackage relies on a shared go library that leverages https://pkg.go.dev/github.com/knqyf263/go-rpmdb/pkg

So relies on this for database support.

