# Testing

## Run tests

By default, pytest is configured to run tests without end-to-end UI tests:

```bash
# inside project root
poetry shell

# inside virtual environment
pytest
```

## Run UI tests

```bash
pytest -m ui
```
