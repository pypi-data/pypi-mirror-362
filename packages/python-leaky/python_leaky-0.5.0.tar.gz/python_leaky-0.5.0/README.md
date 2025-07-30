# Leaky

Leaky finds memory leaks in Python programs. 

**WARNING**: This is not finished! Use at your own risk.

## Installation

Install using pip:

```bash
pip3 install python-leaky
```

## Getting Started

To get started, call this code after your Python program starts:

```python
import leaky

leaky.start(max_object_lifetime=60.0)
```

This will periodically print out potential memory leaks to the console. An object is considered a potential leak if it lives for more than `max_object_lifetime` seconds. For more details on
this parameter see [Object Lifetime](#object_lifetime).

**Note**: leaky may slow down your program, so be wary of using it in a production system.

## Decorator

Leaky can be used as a decorator. This is useful if you know there is a specific function
in your program that leaks memory. For example:

```python
from leaky import leak_monitor

@leak_monitor
def function_that_leaks_memory():
    # Code that leaks memory here
```

In this case, when the function exits leaky will print out potential memory leaks.
That is, objects that were created within the function which cannot be garbage collected.

Note: you should *not* call `leaky.start` when using the decorator. 
