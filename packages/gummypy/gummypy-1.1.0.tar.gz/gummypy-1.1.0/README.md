# Gummypy
A small library that contains wrapper functions around the [gum](https://github.com/charmbracelet/gum) CLI tool.

# Usage
Below is an example on how to use the `choose` function.

```python
# `GumWrappers` is a class that only has static methods (classmethods) of each subcommands of `gum` 
from gummypy import *

# entrypoint
def main():
    # Runs `gun choose --limit=2 "foo" "bar" "baz"` in the terminal
    choose(["foo", "bar", "baz"], limit=2)

if __name__ == "__main__":
    main()
```

## Installation

To use this library, you can install via your package manager like `pip` or `uv`)

### install using `pip`
```sh
pip install gummypy
```

### install using `uv`
```sh
uv add gummypy
```
