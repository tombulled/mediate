# mediate
Middleware for every occasion

## Installation
`mediate` can be installed from [PyPI](https://pypi.org/project/mediate/)
```console
pip install mediate
```

## Usage
### `@middleware`
```python
from mediate import middleware

def shout(call_next, name):
    return call_next(name.upper())

def exclaim(call_next, name):
    return call_next(name + "!")

@middleware(shout, exclaim)
def hello(name):
    print(f"Hello, {name}")
```

```python
>>> hello("sam")
Hello, SAM!
```

### `Middleware`
#### `Middleware.bind`
```python
import mediate

middleware = mediate.Middleware()

@middleware
def shout(call_next, name):
    return call_next(name.upper())

@middleware
def exclaim(call_next, name):
    return call_next(name + "!")

@middleware.bind
def hello(name):
    print(f"Hello, {name}")
```

```python
>>> hello("sam")
Hello, SAM!
```

#### `Middleware.compose`
```python
import mediate

middleware = mediate.Middleware()

@middleware
def shout(call_next, name):
    return call_next(name.upper())

@middleware
def exclaim(call_next, name):
    return call_next(name + "!")

def hello(name):
    print(f"Hello, {name}")

composed_hello = middleware.compose(hello)
```

```python
>>> hello("sam")
Hello, sam
>>> composed_hello("sam")
Hello, SAM!
```