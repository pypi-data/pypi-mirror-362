import argparse
import sys
from . import __version__

def main():
    parser = argparse.ArgumentParser(
        description="loguru-dagster: Bridge between Loguru and Dagster for enhanced logging capabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"loguru-dagster {__version__}"
    )
    
    parser.add_argument(
        "--example",
        action="store_true",
        help="Print an example usage of loguru-dagster"
    )
    
    args = parser.parse_args()
    
    if args.example:
        print_example()
    else:
        parser.print_help()

def print_example():
    example = """
Example usage of loguru-dagster:

from loguru import logger
from loguru_dagster import dagster_context_sink, with_loguru_logger

@dg.asset
@with_loguru_logger
def my_asset(context: dg.AssetExecutionContext):
    logger.info("Hello loguru-dagster!")

defs = dg.Definitions(
    assets=[my_asset]
)

For more examples and documentation, visit:
https://github.com/albertfast/loguru-dagster
"""
    print(example)

if __name__ == "__main__":
    main()
