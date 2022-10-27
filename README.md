# mediate
Middleware for every occasion

## Installation
```console
pip install mediate
```

## Usage
```python
import mediate

middleware = mediate.Middleware()

@middleware
def shout(call_next, name):
    return call_next(name.upper())

@middleware
def exclaim(call_next, name):
    return call_next(name + '!')

@middleware.bind
def hello(name):
    print(f'Hello, {name}')
```

```python
>>> hello('sam')
Hello, SAM!
```
