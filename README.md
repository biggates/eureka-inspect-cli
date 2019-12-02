# eureka-inspect-cli

This is a simple tool for checking nodes registered with Netflix [eureka](https://github.com/Netflix/eureka) server.

## Installation

For now, use:

```
$ pip install --upgrade click colorama pyquery requests
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

