# In bib_ami/validator.py

import logging
from bibtexparser.bibdatabase import BibDatabase
import requests  # Make sure requests is imported

from .cross_ref_client import CrossRefClient


class Validator:
    """
    Validates each entry to find and verify its canonical DOI.
    """

    def __init__(self, client: CrossRefClient):
        self.client = client

    def _is_doi_resolvable(self, doi: str) -> bool:
        """
        Checks if a DOI is active by sending a request to the doi.org resolver.

        Args:
            doi: The DOI string to check.

        Returns:
            True if the DOI resolves successfully, False otherwise.
        """
        url = f"https://doi.org/{doi}"
        try:
            # We use the existing robust session from our client.
            # We don't need to follow the redirect, just know that it exists.
            response = self.client.session.head(
                url, allow_redirects=False, timeout=10
            )
            # A successful resolution will be a redirect (3xx status codes)
            if 300 <= response.status_code < 400:
                logging.info(f"DOI {doi} successfully resolved.")
                return True
            else:
                logging.warning(f"DOI {doi} did not resolve (Status: {response.status_code}).")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed when trying to resolve DOI {doi}: {e}")
            return False

    def _validate_entry(self, entry: dict) -> str or None:
        """
        Contains the specific logic for validating a single BibTeX entry.
        """
        if entry.get('ENTRYTYPE') == 'book':
            logging.info(f"Entry '{entry.get('ID')}' is a book, treating as pre-validated.")
            return entry.get('doi')

        # First, get a candidate DOI from the CrossRef API
        candidate_doi = self.client.get_doi_for_entry(entry)

        # --- NEW: Verify the candidate DOI is resolvable ---
        if candidate_doi and self._is_doi_resolvable(candidate_doi):
            return candidate_doi

        # If the DOI wasn't found or didn't resolve, return None.
        return None

    def validate_all(self, database: BibDatabase) -> (BibDatabase, int):
        """
        Orchestrates the validation process for the entire database.
        """
        logging.info("--- Phase 2a: Validating Entries with Authoritative Source ---")
        validated_count = 0
        for entry in database.entries:
            entry["audit_info"] = {"changes": []}
            verified_doi = self._validate_entry(entry)

            if verified_doi:
                original_doi = entry.get("doi", "").lower()
                if not original_doi:
                    entry["audit_info"]["changes"].append(
                        f"Added new DOI [{verified_doi}]."
                    )
                elif original_doi != verified_doi.lower():
                    entry["audit_info"]["changes"].append(
                        f"Corrected DOI from [{original_doi}] to [{verified_doi}]."
                    )
                validated_count += 1

            entry["verified_doi"] = verified_doi

        logging.info(f"Successfully validated {validated_count} entries with a DOI.")
        return database, validated_count