import argparse
import json
import os

from konfigurator import load_config, update_config_with_overrides

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test script for purepyconf")

    parser.add_argument(
        "--config",
        type=os.path.abspath,
        required=True,
        help="Path to the config file, e.g. 'configs/test_config.yaml'",
    )

    parser.add_argument(
        "--override",
        action="append",
        help="Override config values, e.g. --override key=value",
    )

    parser.add_argument(
        "--save_to",
        type=os.path.abspath,
        help="Path to the file to save the config as a json",
    )

    args = parser.parse_args()

    config = load_config(config_path=args.config)
    config = update_config_with_overrides(config=config, overrides=args.override)
    with open(args.save_to, "w") as f:
        json.dump(config, f, indent=4)
