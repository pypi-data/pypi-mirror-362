import os
import logging
import argparse
import json
from importlib.metadata import version


from jbussdieker.config.config import Config
from jbussdieker.logging import setup_logging
from jbussdieker.project.generator import ProjectGenerator
from jbussdieker.commit.util import run_commit


def _get_parser():
    parser = argparse.ArgumentParser(description="CLI for jbussdieker")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    subparsers.add_parser("version", help="Show the version")
    parser_config = subparsers.add_parser("config", help="Show or set config")
    parser_config.add_argument("--set", metavar="KEY=VALUE", help="Set a config value")
    parser_create = subparsers.add_parser(
        "create", help="Create a new project directory"
    )
    parser_create.add_argument("name", metavar="NAME", help="Name of the new project")
    parser_commit = subparsers.add_parser(
        "commit", help="Generate and create a conventional commit"
    )
    parser_commit.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate commit message without creating commit",
    )

    return parser


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)
    config = Config.load()
    log_level = logging.DEBUG if args.verbose else getattr(logging, config.log_level)
    setup_logging(level=log_level, format=config.log_format)
    logging.debug("Parsed args: %s", args)
    if args.command == "version":
        project_version = version("jbussdieker-project")
        commit_version = version("jbussdieker-commit")
        logging.info(f"jbussdieker: v{version('jbussdieker')}")
        logging.info(f"        app: v{version('jbussdieker-app')}")
        logging.info(f"     config: v{version('jbussdieker-config')}")
        logging.info(f"     commit: v{version('jbussdieker-commit')}")
        logging.info(f"    project: v{version('jbussdieker-project')}")
        logging.info(f"    serivce: v{version('jbussdieker-service')}")
    elif args.command == "config":
        if args.set:
            key, sep, value = args.set.partition("=")
            if not sep:
                logging.error("Invalid format. Use KEY=VALUE.")
                return
            if hasattr(config, key):
                attr = getattr(config, key)
                if isinstance(attr, bool):
                    value = value.lower() in ("1", "true", "yes")
                setattr(config, key, value)
                config.save()
                logging.info(f"Set {key} = {value}")
            else:
                config.custom_settings[key] = value
                config.save()
                logging.info(f"Set custom setting {key} = {value}")
        else:
            logging.info("Current config:")
            logging.info(json.dumps(config.asdict(), indent=2))
    elif args.command == "create":
        generator = ProjectGenerator(args.name, config=config)
        generator.run()
    elif args.command == "commit":
        try:
            run_commit(config.openai_api_key, dry_run=args.dry_run)
        except Exception as e:
            logging.error(f"Commit failed: {e}")
            return 1
    else:
        parser.print_help()
