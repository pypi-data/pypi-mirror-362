"""
This module contains the MetadataRefresher class, responsible for enriching
BibTeX entries with authoritative metadata from an external source.
"""

import logging
from bibtexparser.bibdatabase import BibDatabase
from .cross_ref_client import CrossRefClient


class MetadataRefresher:
    """
    Refreshes BibTeX entry metadata using a verified DOI from an authoritative source.
    """

    def __init__(self, client: CrossRefClient):
        self.client = client

    @staticmethod
    def _refresh_single_entry(entry: dict, metadata: dict) -> bool:
        """
        Updates a single entry with new metadata from an API response.
        This method contains all the field-specific parsing logic.

        Args:
            entry: The BibTeX entry dictionary to update.
            metadata: The raw metadata dictionary from the API client.

        Returns:
            True if the entry was changed, False otherwise.
        """
        changed = False

        # Handle title (which can be a list)
        if 'title' in metadata and metadata['title']:
            new_title = ' '.join(metadata['title'])
            if entry.get('title') != new_title:
                entry['title'] = new_title
                changed = True

        # Handle authors (which is a list of dicts)
        if 'author' in metadata and metadata['author']:
            author_names = [
                f"{author.get('family', '')}, {author.get('given', '')}".strip(', ')
                for author in metadata['author']
            ]
            new_authors_str = " and ".join(author_names)
            if entry.get('author') != new_authors_str:
                entry['author'] = new_authors_str
                changed = True

        # Handle simple, single-value fields
        for field in ["year", "journal", "publisher", "isbn"]:
            # ISBNs are often returned as a list, so we take the first one.
            new_value_list = metadata.get(field)
            if isinstance(new_value_list, list) and new_value_list:
                new_value = new_value_list[0]
            else:
                new_value = new_value_list

            if new_value and str(entry.get(field)) != str(new_value):
                entry[field] = str(new_value)
                changed = True

        return changed

    def refresh_all(self, database: BibDatabase) -> BibDatabase:
        """
        Orchestrates refreshing metadata for all entries in the database with a DOI.
        """
        logging.info("--- Phase 2b: Refreshing Metadata from CrossRef ---")
        refreshed_count = 0
        for entry in database.entries:
            if doi := entry.get("verified_doi"):
                metadata = self.client.get_metadata_by_doi(
                    doi=doi, original_entry=entry
                )
                if metadata:
                    # Delegate all the detailed work to the helper method
                    if self._refresh_single_entry(entry, metadata):
                        entry.setdefault("audit_info", {}).setdefault("changes", []).append(
                            "Refreshed metadata from CrossRef."
                        )
                        refreshed_count += 1

        logging.info(f"Refreshed metadata for {refreshed_count} entries.")
        return database
