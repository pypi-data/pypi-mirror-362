import logging
import json

from .config import Config


def register(subparsers):
    parser = subparsers.add_parser("config", help="Show or set config")
    parser.add_argument("--set", metavar="KEY=VALUE", help="Set a config value")
    parser.set_defaults(func=main)


def main(args):
    config = Config.load()

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
