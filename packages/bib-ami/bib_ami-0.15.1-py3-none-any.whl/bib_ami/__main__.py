"""
Main entry point for the bib-ami command-line tool.

This script is executed when the `bib-ami` command is run from the terminal.
Its primary responsibilities are:
1.  Setting up basic logging for the application.
2.  Parsing command-line arguments and configuration settings using the CLIParser.
3.  Initializing the main BibTexManager with the final settings.
4.  Executing the bibliography processing workflow.
5.  Catching and logging any critical, unhandled exceptions that occur during the process.

----------------------------------------------------------------------
To run the version of bib-ami that's in your project directory (not the one installed by Pip),
you should call it as a module from the root of the project. This ensures you're
always running the latest code you just saved.

Use the python -m command, where -m stands for "module":

python -m bib_ami [ARGUMENTS]

For example, to run it with the necessary arguments, your command would look like this:

python -m bib_ami --input-file my_library.bib --output-file cleaned_library.bib --email "you@example.com"

Pro-Tip 💡: For the best development experience, you can install your project in "editable" mode once from the project root:

pip install -e .

After doing this, you can call bib-ami directly from your terminal, and it will
always point to your source code. Any changes you make are reflected immediately
without needing to reinstall.
"""

import logging
from .cli import CLIParser
from .bibtex_manager import BibTexManager


def main():
    """
    Initializes and runs the bib-ami application workflow.

    This function orchestrates the entire process by parsing arguments,
    instantiating the manager, running the workflow, and handling top-level
    exceptions.
    """
    # Configure the root logger for the application.
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Parse command-line arguments and load any configuration files.
    parser = CLIParser()
    settings = parser.get_settings()

    try:
        # Instantiate the main manager with the user-provided settings.
        manager = BibTexManager(settings=settings)
        # Execute the full bibliography processing pipeline.
        manager.process_bibliography()
    except Exception as e:
        # A top-level catch-all to ensure that any unexpected critical error
        # during the workflow is logged to the console instead of crashing silently.
        logging.error(
            f"A critical error occurred during the workflow: {e}",
            exc_info=True,  # Set to True to include the full traceback in the log.
        )


if __name__ == "__main__":
    # This allows the script to be run directly, e.g., `python -m bib_ami.__main__`.
    # The `entry_points` in setup.py makes this the target for the `bib-ami` command.
    main()
