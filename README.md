# flake8-jungle

A flake8 plugin to detect bad practices in projects. This plugin is based on [flake8-django](https://github.com/rocioar/flake8-django/).

## Installation

Install from pip with:

```
$ pip install flake8-jungle
```

## `pre-commit` example

```yaml
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        additional_dependencies: ['flake8-jungle==VERSION']
        args: ['--max-condition-complexity=8']
```

## List of Rules

| Rule | Description | Configuration |
| ---- | ----------- | ------------- |
| `JG01` | The order of the model's inner classes, methods, and fields does not follow the [Django Style Guide](https://github.com/HackSoftware/Django-Styleguide). | |
| `JG02` | Do not use `exclude` attribute in `ModelForm`, list all items explicitly in `fields` attribute instead. | |
| `JG03` | Avoid using `null=True` on string-based fields such as `CharField` and `TextField`. | |
| `JG04` | Exceptions should never pass silently, add logging or comment at least. | |
| `JG05` | Condition is too complex which makes it impossible to understand. | `--max-condition-complexity` |
| `JG06` | Function is too long. | `--max-function-length` |
| `JG07` | Model is too long, split it into services, selectors, or utilities. | `--max-model-length` |
| `JG08` | Function or method contains local imports, which should be mostly avoided. If you are trying to fix curcular dependency issues, the design probably has some flaws, you should consider refactoring instead. |
| `JG09` | Incorrect logging format, please use the following syntax: `logging.info("MESSAGE %(arg1)s", {"arg1": "value1"}`) | |
| `JG10` | Too much patching in tests. Consider changing your design to utilize Dependency Injection and fakes. | `--max-patches-in-test` |

## Testing

flake8-jungle uses pytest for tests. To run them use:

```
$ poetry install
$ poetry run pytest tests
```
