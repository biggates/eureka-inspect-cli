# eureka-inspect-cli

This is a simple tool for checking nodes registered with Netflix [eureka](https://github.com/Netflix/eureka) server.

## Installation

For now, use:

```
$ pip3 install --upgrade click colorama requests
$ pip3 install -i https://test.pypi.org/simple/ eureka-inspect-cli --no-deps --upgrade
```

```
$ pip install --upgrade click colorama requests
$ pip install -i https://test.pypi.org/simple/ eureka-inspect-cli --no-deps --upgrade
```

## Usage

```
$ eureka_inspect --help
Options:
  -h, --host TEXT     Eureka host  [default: localhost]
  -p, --port INTEGER  Eureka port  [default: 8761]
  -v, --version       Display version.
  -V, --verbose       Display more info.
  --help              Show this message and exit.

```

## Development

### Running from source

```
python3 -m eureka_inspect_cli.main --verbose
```

### Packaging

```
python3 setup.py sdist bdist_wheel
```

### Distribution

```
python3 -m twine upload --repository testpypi dist/*
```

* see https://packaging.python.org/tutorials/packaging-projects/
