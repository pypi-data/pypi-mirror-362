## <ins> Follow </ins>

Follow is a flexible Python decorator that lets you trace, inspect, and log exactly what happens inside your Python code — line by line <br>
Use it to debug, audit, or understand your code’s behavior in real time <br>

### <ins> Features </ins>

- Trace every executed line of a decorated function
- Log local variables, line content, and time spent between lines
- Selectively tracing (FollowConfig)
- Custom follower — Send trace data to print, a logger, or your own collector
- Supports multithreaded tracing with automatic worker wrapping

### <ins> Installation </ins>

You can install this package via PIP: pip install python-follow <br>

### <ins> Usage </ins>

```python
from follow import follow, FollowConfig

# Define your config
config = FollowConfig(
    follow_threads=True,
    follow_for_loops=True,
    follow_variable_set=True,
    follow_prints=True,
)

# Decorate your function
@follow(config=config)
def my_function():
    a = 1
    for i in range(3):
        b = a + i

my_function()

# Output:
# {'function': 'my_function', 'instruction': 'a = 1', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}]}
# {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 0, 'type': 'int'}]}
# {'function': 'my_function', 'instruction': 'b = a + i', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 0, 'type': 'int'}, {'var': 'b', 'val': 1, 'type': 'int'}]}
# {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 1, 'type': 'int'}, {'var': 'b', 'val': 1, 'type': 'int'}]}
# {'function': 'my_function', 'instruction': 'b = a + i', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 1, 'type': 'int'}, {'var': 'b', 'val': 2, 'type': 'int'}]}
# {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 2, 'type': 'int'}, {'var': 'b', 'val': 2, 'type': 'int'}]}
# {'function': 'my_function', 'instruction': 'b = a + i', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 2, 'type': 'int'}, {'var': 'b', 'val': 3, 'type': 'int'}]}
# {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': []}
```

## <ins> Usage - Custom Collector </ins>

```python
from follow import follow, FollowConfig

class CustomCollector:
    def __init__(self):
        self.traces = []

    def collect(self, data: dict):
        self.traces.append(data)

custom_collector = CustomCollector()

# Decorate your function
@follow(follower=custom_collector.collect)
def my_function():
    a = 1
    for i in range(3):
        b = a + i

my_function()

# Output:
# [
#     {'function': 'my_function', 'instruction': 'a = 1', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}]},
#     {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 0, 'type': 'int'}]},
#     {'function': 'my_function', 'instruction': 'b = a + i', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 0, 'type': 'int'}, {'var': 'b', 'val': 1, 'type': 'int'}]},
#     {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 1, 'type': 'int'}, {'var': 'b', 'val': 1, 'type': 'int'}]},
#     {'function': 'my_function', 'instruction': 'b = a + i', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 1, 'type': 'int'}, {'var': 'b', 'val': 2, 'type': 'int'}]},
#     {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 2, 'type': 'int'}, {'var': 'b', 'val': 2, 'type': 'int'}]},
#     {'function': 'my_function', 'instruction': 'b = a + i', 'execution_time': 0.0, 'local_vars': [{'var': 'a', 'val': 1, 'type': 'int'}, {'var': 'i', 'val': 2, 'type': 'int'}, {'var': 'b', 'val': 3, 'type': 'int'}]},
#     {'function': 'my_function', 'instruction': 'for i in range(3):', 'execution_time': 0.0, 'local_vars': []}
# ]
print(custom_collector.traces)
```