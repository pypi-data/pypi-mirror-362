# reconciler.py

import logging
import string
from typing import Dict, Any, List

from bibtexparser.bibdatabase import BibDatabase
from fuzzywuzzy import fuzz


class Reconciler:
    """
    Deduplicates entries and merges metadata into a single "golden record".
    """

    def __init__(self, fuzzy_threshold=95):
        self.fuzzy_threshold = fuzzy_threshold

    @staticmethod
    def _normalize_title(title: str) -> str:
        if not title:
            return ""
        return title.lower().translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def _create_golden_record(group: List[Dict]) -> Dict[str, Any]:
        if not group:
            return {}
        winner = max(group, key=len)
        golden_record = winner.copy()
        if "audit_info" not in golden_record:
            golden_record["audit_info"] = {"changes": []}
        if len(group) > 1:
            notes = {e.get("note") for e in group if e.get("note")}
            if len(notes) > 1:
                golden_record["note"] = " | ".join(sorted(list(notes)))
                golden_record["audit_info"]["changes"].append("Merged 'note' fields.")
            merged_ids = sorted([e["ID"] for e in group if e["ID"] != winner["ID"]])
            if merged_ids:
                golden_record["audit_info"]["changes"].append(f"Merged with: {', '.join(merged_ids)}.")
        return golden_record

    @staticmethod
    def _group_by_doi(entries: List[Dict]) -> (List[List[Dict]], List[Dict]):
        """First pass: Groups entries by verified DOI."""
        doi_map: Dict[str, List[Dict]] = {}
        no_doi_entries: List[Dict] = []
        for entry in entries:
            if doi := entry.get("verified_doi"):
                doi_key = doi.lower()
                if doi_key not in doi_map:
                    doi_map[doi_key] = []
                doi_map[doi_key].append(entry)
            else:
                no_doi_entries.append(entry)
        return list(doi_map.values()), no_doi_entries

    def _group_by_fuzzy_title(self, entries: List[Dict], initial_groups: List[List[Dict]]) -> List[List[Dict]]:
        """Second pass: Merges remaining entries into groups using fuzzy title matching."""
        final_groups = list(initial_groups)
        for entry_to_check in entries:
            # Use the original_title saved by the manager
            original_title_to_check = entry_to_check.get("audit_info", {}).get("original_title",
                                                                               entry_to_check.get("title"))
            normalized_title_to_check = self._normalize_title(original_title_to_check)

            found_group = False
            for group in final_groups:
                group_leader = group[0]
                # Use the original_title of the group leader for a fair comparison
                original_leader_title = group_leader.get("audit_info", {}).get("original_title",
                                                                               group_leader.get("title"))
                existing_title = self._normalize_title(original_leader_title)

                if fuzz.ratio(normalized_title_to_check, existing_title) > self.fuzzy_threshold:
                    group.append(entry_to_check)
                    found_group = True
                    break

            if not found_group:
                final_groups.append([entry_to_check])
        return final_groups

    def deduplicate(self, database: BibDatabase) -> (BibDatabase, int):
        """Executes the full deduplication and reconciliation process."""
        initial_count = len(database.entries)

        doi_groups, remaining_entries = self._group_by_doi(database.entries)
        final_groups = self._group_by_fuzzy_title(remaining_entries, doi_groups)
        reconciled = [self._create_golden_record(group) for group in final_groups]

        database.entries = reconciled
        duplicates_removed = initial_count - len(reconciled)
        logging.info(
            f"Reconciled {initial_count} entries into {len(reconciled)}, removing {duplicates_removed} duplicates.")
        return database, duplicates_removed
