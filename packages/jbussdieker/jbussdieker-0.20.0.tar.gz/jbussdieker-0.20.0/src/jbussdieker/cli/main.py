import sys
import argparse
import logging
from importlib.metadata import entry_points as eps, version

from jbussdieker.config.config import Config
from jbussdieker.logging import setup_logging


if sys.version_info >= (3, 10):  # pragma: no cover

    def get_eps(group):
        return eps(group=group)

else:  # pragma: no cover

    def get_eps(group):
        return eps().get(group, [])


def main(argv=None):
    parser = argparse.ArgumentParser(description="CLI for jbussdieker")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    subparsers.add_parser("version", help="Show the version")

    for ep in get_eps("jbussdieker.cli"):
        try:
            register = ep.load()
        except Exception as e:
            logging.error(f"Failed to load CLI entry point {ep.name}: {e}")
            continue
        register(subparsers)

    args = parser.parse_args(argv)

    config = Config.load()
    log_level = logging.DEBUG if args.verbose else getattr(logging, config.log_level)
    setup_logging(level=log_level, format=config.log_format)
    logging.debug("Parsed args: %s", args)

    if args.command == "version":
        logging.info(f"jbussdieker: v{version('jbussdieker')}")
    elif hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
