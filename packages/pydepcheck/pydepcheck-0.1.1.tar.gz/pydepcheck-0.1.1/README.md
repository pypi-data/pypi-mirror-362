# pydepcheck

A Python tool to analyze dependences in Python loop nests.

## Installation

```bash
pip install pydepcheck
```

## Usage Example

```python
from pydepcheck import analyze_loop_dependences

code = """
for i in range(10):
    a[i] = a[i-1] + 1
"""

result = analyze_loop_dependences(code)
print(result)
```