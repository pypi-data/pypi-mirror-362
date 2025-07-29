A python package that extracts rust audit  information from rust audit based executables.


Example usage

```python

from pyrustaudit import get_rust_audit
import json


def test_get_info(file):
    res = get_rust_audit(file)
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
on success a python dict is rturned like this

```python
{
    "packages": [
        {
            "name": "adler",
            "version": "1.0.2",
            "source": "registry",
            "kind": "build",
            "dependencies": null,
            "features": null,
            "root": false
        },
        {
            "name": "auditable",
            "version": "0.1.0",
            "source": "registry",
            "kind": "runtime",
            "dependencies": null,
            "features": null,
            "root": false
        },
        {
            "name": "auditable-build",
            "version": "0.1.0",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                3,
                5,
                7,
                15
            ],
            "features": null,
            "root": false
        },
        {
            "name": "auditable-serde",
            "version": "0.1.0",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                5,
                11,
                13,
                15
            ],
            "features": [
                "cargo_metadata",
                "default",
                "from_metadata"
            ],
            "root": false
        },
        {
            "name": "autocfg",
            "version": "1.2.0",
            "source": "registry",
            "kind": "build",
            "dependencies": null,
            "features": null,
            "root": false
        },
        {
            "name": "cargo_metadata",
            "version": "0.11.4",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                11,
                13,
                15
            ],
            "features": [
                "default"
            ],
            "root": false
        },
        {
            "name": "itoa",
            "version": "1.0.11",
            "source": "registry",
            "kind": "build",
            "dependencies": null,
            "features": null,
            "root": false
        },
        {
            "name": "miniz_oxide",
            "version": "0.4.4",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                0,
                4
            ],
            "features": null,
            "root": false
        },
        {
            "name": "proc-macro2",
            "version": "1.0.79",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                18
            ],
            "features": [
                "proc-macro"
            ],
            "root": false
        },
        {
            "name": "quote",
            "version": "1.0.35",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                8
            ],
            "features": [
                "proc-macro"
            ],
            "root": false
        },
        {
            "name": "ryu",
            "version": "1.0.17",
            "source": "registry",
            "kind": "build",
            "dependencies": null,
            "features": null,
            "root": false
        },
        {
            "name": "semver",
            "version": "0.10.0",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                12,
                13
            ],
            "features": [
                "default",
                "serde"
            ],
            "root": false
        },
        {
            "name": "semver-parser",
            "version": "0.7.0",
            "source": "registry",
            "kind": "build",
            "dependencies": null,
            "features": null,
            "root": false
        },
        {
            "name": "serde",
            "version": "1.0.197",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                14
            ],
            "features": [
                "default",
                "derive",
                "serde_derive",
                "std"
            ],
            "root": false
        },
        {
            "name": "serde_derive",
            "version": "1.0.197",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                8,
                9,
                16
            ],
            "features": [
                "default"
            ],
            "root": false
        },
        {
            "name": "serde_json",
            "version": "1.0.115",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                6,
                10,
                13
            ],
            "features": [
                "default",
                "std"
            ],
            "root": false
        },
        {
            "name": "syn",
            "version": "2.0.58",
            "source": "registry",
            "kind": "build",
            "dependencies": [
                8,
                9,
                18
            ],
            "features": [
                "clone-impls",
                "derive",
                "parsing",
                "printing",
                "proc-macro"
            ],
            "root": false
        },
        {
            "name": "test-data",
            "version": "0.1.0",
            "source": "local",
            "kind": "runtime",
            "dependencies": [
                1,
                2
            ],
            "features": null,
            "root": false
        },
        {
            "name": "unicode-ident",
            "version": "1.0.12",
            "source": "registry",
            "kind": "build",
            "dependencies": null,
            "features": null,
            "root": false
        }
    ]
}

```


