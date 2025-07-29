# veras

Universal agent tracing SDK for Python. Drop-in decorators to trace any agent and send to AWS.

## Install

```sh
pip install veras
```

## Usage

```python
from veras import trace, span

@trace
def my_agent(input):
    ...

@span
def my_tool(...):
    ...
``` 