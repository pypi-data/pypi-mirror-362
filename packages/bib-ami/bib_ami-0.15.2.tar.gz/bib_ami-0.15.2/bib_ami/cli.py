# In bib_ami/cli.py

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any


class CLIParser:
    """
    Parses command-line arguments and configuration for bib-ami.
    Supports sub-commands for running the workflow and managing configuration.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Clean, merge, and enrich BibTeX files.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")
        # By not setting `required=True`, the absence of a command is allowed,
        # which we treat as the default 'run' behavior.

        self._setup_run_parser(subparsers)
        self._setup_config_parser(subparsers)

    def parse_args(self):
        """A simple wrapper around argparse's parse_args."""
        return self.parser.parse_args()

    def _setup_run_parser(self, subparsers):
        """Defines the arguments for the main bibliography processing workflow."""
        run_parser = subparsers.add_parser("run",
                                           help="Run the main bibliography workflow (this is the default action).",
                                           formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        run_parser.add_argument("--input-dir", required=True, type=Path, help="Directory containing input .bib files.")
        run_parser.add_argument("--output-file", required=True, type=Path, help="Path for the main output file.")
        run_parser.add_argument("--suspect-file", type=Path, default=None,
                                help="Path for the suspect entries file. Defaults to being based on the main output file name.")
        run_parser.add_argument("--config-file", type=Path, default="bib_ami_config.json",
                                help="Path to a JSON configuration file.")
        run_parser.add_argument("--email", type=str, help="Email for CrossRef API Polite Pool.")
        # Add other 'run' specific flags here in the future

    def _setup_config_parser(self, subparsers):
        """Defines the new 'config' sub-command and its actions (set, get, list)."""
        config_parser = subparsers.add_parser("config", help="Manage default settings in the user config file.")
        config_actions = config_parser.add_subparsers(dest="action", required=True, help="Configuration actions")

        set_parser = config_actions.add_parser("set", help="Set a default value.")
        set_parser.add_argument("key", type=str, help="The configuration key (e.g., 'email').")
        set_parser.add_argument("value", type=str, help="The value to set.")

        config_actions.add_parser("get", help="Get a default value. (Not yet implemented)")
        config_actions.add_parser("list", help="List all default values. (Not yet implemented)")

    def handle_config_command(self, args: argparse.Namespace):
        """Handles the logic for the 'config' sub-command."""
        config_path = Path.home() / ".config" / "bib-ami" / "config.json"

        if args.action == "set":
            self._set_config_value(config_path, args.key, args.value)
            print(f"Success: Set '{args.key}' to '{args.value}' in {config_path}")
        else:
            print(f"Action '{args.action}' is not yet implemented.")

        # In bib_ami/cli.py

    def _set_config_value(self, config_path: Path, key: str, value: Any):
        """Reads, updates, and writes a key-value pair to the JSON config file."""
        config = {}
        # Check if the file exists first.
        if config_path.exists():
            with open(config_path, "r") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    logging.warning(f"Config file at {config_path} is corrupted. It will be overwritten.")
                    config = {}
        # --- NEW LOGIC: Only create the directory if the file does NOT exist ---
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)

        # This logic for updating the dictionary remains the same
        keys = key.split('.')
        d = config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

        # Write the file at the end
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

    def get_run_settings(self, args: argparse.Namespace) -> argparse.Namespace:
        """Loads configs and returns final settings for the 'run' command."""
        config = self._load_config(getattr(args, 'config_file', 'bib_ami_config.json'))
        settings = vars(args)
        for key, value in config.items():
            # Command line args take precedence, so only set from config if not present in args
            if settings.get(key) is None:
                settings[key] = value

        if settings.get("suspect_file") is None:
            output_file = settings.get("output_file")
            base_name = output_file.stem
            suffix = output_file.suffix
            settings["suspect_file"] = output_file.parent / f"{base_name}.suspect{suffix}"

        if not settings.get("email"):
            self.parser.error("An email address is required. Provide it via --email or in the config file.")

        return argparse.Namespace(**settings)

    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        # This can be expanded to search the full hierarchy later
        if config_path and config_path.exists():
            try:
                with open(config_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}