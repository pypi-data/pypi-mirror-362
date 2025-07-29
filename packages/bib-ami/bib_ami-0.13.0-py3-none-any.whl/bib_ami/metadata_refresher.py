"""
This module contains the MetadataRefresher class, responsible for enriching
BibTeX entries with authoritative metadata from an external source.
"""

import logging
from bibtexparser.bibdatabase import BibDatabase
from .cross_ref_client import CrossRefClient


class MetadataRefresher:
    """
    Refreshes BibTeX entry metadata using a verified DOI.

    This class takes a database of entries that have already been validated
    (i.e., have a 'verified_doi' field) and uses an API client to fetch
    the canonical metadata for each entry, updating it in place.
    """

    def __init__(self, client: CrossRefClient):
        """
        Initializes the MetadataRefresher.

        Args:
            client: An instance of an API client (e.g., CrossRefClient)
                that has a `get_metadata_by_doi` method.
        """
        self.client = client

    def refresh_all(self, database: BibDatabase) -> BibDatabase:
        """
        Iterates through a database and refreshes metadata for entries with a DOI.
        """
        logging.info("--- Phase 2b: Refreshing Metadata from CrossRef ---")
        refreshed_count = 0
        for entry in database.entries:
            if entry.get("verified_doi"):
                metadata = self.client.get_metadata_by_doi(
                    doi=entry["verified_doi"],
                    original_entry=entry
                )
                if metadata:
                    changed = False

                    # --- NEW: Process and format fields before updating ---
                    # Handle title (which can be a list)
                    if 'title' in metadata and metadata['title']:
                        # Join title parts, which are returned as a list
                        new_title = ' '.join(metadata['title'])
                        if entry.get('title') != new_title:
                            entry['title'] = new_title
                            changed = True

                    # Handle authors (which is a list of dicts)
                    if 'author' in metadata and metadata['author']:
                        # Format authors into "Family, Given and Family, Given"
                        author_names = []
                        for author in metadata['author']:
                            name = f"{author.get('family', '')}, {author.get('given', '')}"
                            author_names.append(name.strip(', '))
                        new_authors_str = " and ".join(author_names)

                        if entry.get('author') != new_authors_str:
                            entry['author'] = new_authors_str
                            changed = True

                    # Handle simple fields like year and journal
                    for field in ["year", "journal"]:
                        new_value = metadata.get(field)
                        if new_value and str(entry.get(field)) != str(new_value):
                            entry[field] = str(new_value)  # Ensure it's a string
                            changed = True
                    # --- End of new logic ---

                    if changed:
                        # This logic for audit_info can remain the same
                        if "audit_info" not in entry:
                            entry["audit_info"] = {"changes": []}
                        entry["audit_info"]["changes"].append(
                            "Refreshed metadata from CrossRef."
                        )
                        refreshed_count += 1

        logging.info(f"Refreshed metadata for {refreshed_count} entries.")
        return database
