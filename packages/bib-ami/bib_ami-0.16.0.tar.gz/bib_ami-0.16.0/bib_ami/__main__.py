import logging
from .cli import CLIParser
from .bibtex_manager import BibTexManager


def main():
    """
    Initializes and runs the bib-ami application workflow.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = CLIParser()
    args = parser.parse_args()

    try:
        # Check which command was used
        if hasattr(args, 'action'):  # This attribute only exists for the 'config' command
            parser.handle_config_command(args)
        else:
            # By default, execute the main workflow
            settings = parser.get_run_settings(args)
            manager = BibTexManager(settings=settings)
            manager.process_bibliography()

    except Exception as e:
        logging.error(f"A critical error occurred during the workflow: {e}", exc_info=True)


if __name__ == "__main__":
    main()
