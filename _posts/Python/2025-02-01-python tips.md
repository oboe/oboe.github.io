---
layout: post
tags:
  - Python
---
<https://book.pythontips.com/en/latest/index.html>

## args and kwargs
Already know this but can be useful to define functions to patch code at runtime, which could see as being useful for debugging.
```python
import someclass

def get_info(self, *args):
    return "Test data"

someclass.get_info = get_info
```
## Debugging
```python
import pdb

 def make_bread(arg):
     pdb.set_trace()
     return "I don't have time" + arg

 print(make_bread(" and money"))
```

Pretty simple, enter with `pdb.set_trace()` or `python -m pdb myscript.py`.
#### Visibility
- w: view current line
- a: view args
- l: view code
- ll: view code
- b: list all breaks
- p, pp, display: print an expression!
- w: view the current stack

#### Movement
- c: continue
- n, s: next line

## Generators

## Map, Filter and Reduce
Map and filter are commonly used, reduced less so. What other ones might be more interesting. 

```python
from functools import reduce
 a = [1,2,3,4]
 b = reduce((lambda x,y: x + y), a)
 print("{} {}".format(a,b))
```
## Ternaries
Huh shorthand ternaries are kinda like nullish coalescing.
```python
output or "something"
```
## One liners
Thats pretty neat, can host a quick http server with python
```bash
# Python 2
python -m SimpleHTTPServer

# Python 3
python -m http.server

# Can also profile with
python -m cProfile script.py
```
## Context managers
Simple RAII style classes. Just implement the enter and exit functions.
```python
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()
```