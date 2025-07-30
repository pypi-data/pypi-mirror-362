"""
This module contains the Triage class, which is responsible for categorizing
processed BibTeX records based on their verification status.
"""

from bibtexparser.bibdatabase import BibDatabase


class Triage:
    """
    Categorizes records as Verified, Accepted, or Suspect.

    This class applies a set of rules to each processed record to determine
    its final status. This is the final classification step before the records
    are written to their respective output files.
    """

    @staticmethod
    def run_triage(
            database: BibDatabase, filter_validated: bool
    ) -> (BibDatabase, BibDatabase):
        """
        Separates a database into verified/accepted and suspect records.

        The logic is as follows:
        - An entry is considered TRUSTWORTHY if it has a verified DOI OR if it is a
          book or technical report.
        - All other entries are considered 'Suspect'.
        - The `filter_validated` flag is currently not used in this simplified
          logic but is kept for potential future use where rules for other
          entry types might be more complex.

        Args:
            database: The BibDatabase object containing the processed entries.
            filter_validated: A boolean flag from the CLI.

        Returns:
            A tuple containing two BibDatabase objects:
                - The first database contains 'Verified' and 'Accepted' records.
                - The second database contains 'Suspect' records.
        """
        verified_db, suspect_db = BibDatabase(), BibDatabase()

        for entry in database.entries:
            is_verified_by_doi = bool(entry.get("verified_doi"))
            is_book_or_report = entry.get("ENTRYTYPE", "misc").lower() in [
                "book",
                "techreport",
            ]

            # An entry is trustworthy if it has a DOI or if it's a book/report.
            if is_verified_by_doi or is_book_or_report:
                if is_verified_by_doi:
                    entry["audit_info"]["status"] = "Verified by DOI"
                else:
                    entry["audit_info"]["status"] = "Accepted (Book/Report)"
                verified_db.entries.append(entry)
            else:
                # Everything else is considered suspect.
                entry["audit_info"]["status"] = "Suspect"
                suspect_db.entries.append(entry)

        return verified_db, suspect_db
