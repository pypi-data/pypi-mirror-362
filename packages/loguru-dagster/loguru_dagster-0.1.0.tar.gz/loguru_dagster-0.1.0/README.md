# loguru-dagster

**loguru-dagster** is a lightweight utility package that bridges [Loguru](https://github.com/Delgan/loguru) with [Dagster](https://github.com/dagster-io/dagster).  
It enables colorized, contextual logging in Dagster pipelines with just a decorator.

## Installation

```bash
pip install loguru-dagster
```

## Usage

```python
from loguru import logger
from loguru_dagster import with_loguru_logger

@asset
@with_loguru_logger
def greet(context):
    logger.info("Hello from Loguru!")
```

All logs will show up in Dagster UI with proper formatting and level awareness.

## Configuration

Customize logging behavior using environment variables:

- `DAGSTER_LOGURU_ENABLED` (`true`|`false`)
- `DAGSTER_LOGURU_LOG_LEVEL` (`DEBUG`, `INFO`, ...)
- `DAGSTER_LOGURU_FORMAT`
- `DAGSTER_LOGURU_FILE_PATH`

## License

MIT
