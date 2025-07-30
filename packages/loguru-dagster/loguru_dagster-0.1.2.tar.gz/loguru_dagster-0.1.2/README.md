# loguru-dagster

**loguru-dagster** is a lightweight utility package that bridges [Loguru](https://github.com/Delgan/loguru) with [Dagster](https://dagster.io/).  
It enables **colorized, contextual logging** inside Dagster pipelines with a single decorator.

## 🚀 Installation

```bash
pip install loguru-dagster
```

This will automatically install the required `loguru` and `dagster` dependencies.

## 📦 Import Path

```python
from loguru_dagster import dagster_context_sink, with_loguru_logger
```

## 🧪 Usage Example

```python
from loguru import logger
from loguru_dagster import dagster_context_sink, with_loguru_logger

@dg.asset
@with_loguru_logger
def my_asset(context: dg.AssetExecutionContext):
    logger.info("Hello loguru-dagster!")

defs = dg.Definitions(
    assets=[my_asset]
)
```

## 🔗 Repository

[https://github.com/albertfast/loguru-dagster](https://github.com/albertfast/loguru-dagster)
