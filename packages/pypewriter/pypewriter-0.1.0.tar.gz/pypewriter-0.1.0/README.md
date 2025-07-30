# pypewriter

[![PyPI - Version](https://img.shields.io/pypi/v/pypewriter.svg)](https://pypi.org/project/pypewriter)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypewriter.svg)](https://pypi.org/project/pypewriter)

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install pypewriter
```

## Usage

```py
from pypewriter.Pypewriter import * 
```

Two basic functions are provided, `pypewrite()` and `get_random_color()`:

```py
pypewrite(string: str, speed: float, pause: float, color: str, new_line: bool) -> None
get_random_color() -> str
```

There's also a built-in dictionary of ASCII color codes for further customization:

```py
pypewriter_colors = {
    'end_color': '\033[0m', 
    # If you're coloring a substring, always place this where you want the color to end
    # E.g. {red}Hello{end_color} World!

    'red': '\x1b[1;31m',
    'green': '\x1b[1;32m',
    'yellow': '\x1b[1;33m',
    'blue': '\x1b[1;34m',
    'magenta': '\x1b[1;35m',
    'cyan': '\x1b[1;36m',

    'red_bg': '\x1b[1;37;41m',
    'green_bg': '\x1b[1;37;42m',
    'yellow_bg': '\x1b[1;37;43m',
    'blue_bg': '\x1b[1;37;44m',
    'magenta_bg': '\x1b[1;37;45m',
    'cyan_bg': '\x1b[1;37;46m'        
}
```

## License

`pypewriter` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.