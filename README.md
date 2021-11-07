# middleware
Middleware for all occasions

## Usage
```python
import middleware

middleware = middleware.Middleware() # TODO: Resolve name conflict

@middleware
def make_name_title(call_next, name):
    return call_next(name.title())

@middleware
def add_exclamation_mark(call_next, name):
    return call_next(name + '!')

@middleware.bind
def hello(name):
    print(f'Hello, {name}')
```

```python
>>> hello('sam')
Hello, Sam!
```
