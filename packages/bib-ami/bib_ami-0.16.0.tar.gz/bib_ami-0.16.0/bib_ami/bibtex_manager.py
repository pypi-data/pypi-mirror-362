"""
This module contains the BibTexManager class, the central orchestrator for the
bib-ami application.
"""

import argparse
import logging
from typing import Optional

from .cross_ref_client import CrossRefClient
from .ingestor import Ingestor
from .metadata_refresher import MetadataRefresher
from .reconciler import Reconciler
from .triage import Triage
from .validator import Validator
from .writer import Writer


class BibTexManager:
    """
    Orchestrates the end-to-end bibliography processing workflow.

    This class initializes all the necessary components (Ingestor, Validator, etc.)
    and executes the integrity-first pipeline in the correct sequence based on
    the user-provided settings.
    """

    def __init__(
            self,
            settings: argparse.Namespace,
            client: Optional[CrossRefClient] = None,
    ):
        """
        Initializes the manager and all its workflow components.

        Args:
            settings: An argparse.Namespace object containing all command-line
                and configuration settings for the current run.
            client: An optional API client instance. If provided, it will be
                used for testing purposes (dependency injection). If None, a
                new CrossRefClient is created.
        """
        self.settings = settings

        # Use the injected client if provided (for testing), otherwise create a real one.
        self.client = (
            client if client else CrossRefClient(email=self.settings.email)
        )

        # Instantiate all the components that make up the workflow pipeline.
        self.ingestor = Ingestor()
        self.validator = Validator(client=self.client)
        self.refresher = MetadataRefresher(client=self.client)
        self.reconciler = Reconciler()
        self.triage = Triage()
        self.writer = Writer()

    def process_bibliography(self):
        """
        Executes the full, integrity-first data processing pipeline.
        """
        # Phase 1: Ingestion
        database, num_files = self.ingestor.ingest_from_directory(
            self.settings.input_dir
        )

        if self.settings.merge_only:
            self.writer.write_raw_database(database, self.settings.output_file)
            logging.info(f"Merge-only complete. Merged {num_files} files into {self.settings.output_file}")
            return

        # Phase 2: Validation and Enrichment
        database, validated_count = self.validator.validate_all(database)

        # Store original titles before they are changed by the refresher
        for entry in database.entries:
            if "title" in entry:
                entry.setdefault("audit_info", {})["original_title"] = entry["title"]

        database = self.refresher.refresh_all(database)

        # Phase 3: Reconciliation
        database, duplicates_removed = self.reconciler.deduplicate(database)

        # Phase 4: Triage and Writing
        verified_db, suspect_db = self.triage.run_triage(
            database, self.settings.filter_validated
        )
        self.writer.write_files(
            verified_db,
            suspect_db,
            self.settings.output_file,
            self.settings.suspect_file,
        )

        logging.info("Workflow complete.")
