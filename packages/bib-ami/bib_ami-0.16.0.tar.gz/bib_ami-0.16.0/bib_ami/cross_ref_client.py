"""
This module contains the CrossRefClient class, which is responsible for all
interactions with the public CrossRef API.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Optional, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .diff_utils import get_title_diff, get_authors_diff
from .log_setup import setup_json_logger

# Configure basic logging for this module.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Get the standard console logger
logger = logging.getLogger(__name__)


class CrossRefClient:
    """
    A client for querying the CrossRef API to find and validate DOIs.

    This client is designed for robustness and responsible API usage. It uses a
    requests.Session for connection pooling and implements an automatic retry
    strategy with exponential backoff to handle transient network issues or
    API rate limits gracefully.
    """

    BASE_URL = "https://api.crossref.org/works"

    def __init__(
            self,
            email: str,
            timeout: int = 10,
            max_retries: int = 3,
            results_log_file: str = "crossref_results.jsonl"
    ):
        """
        Initializes the CrossRefClient.

        Args:
            email: Your email address, required by the CrossRef Polite Pool
                policy for responsible API usage.
            timeout: The timeout in seconds for each API request.
            max_retries: The maximum number of times to retry a failed request.
        """
        if not email:
            raise ValueError(
                "An email address is required for the CrossRef API's Polite Pool."
            )

        self.email = email
        self.timeout = timeout
        self.session = self._create_session(max_retries)

        self.results_logger = setup_json_logger('results_logger', results_log_file)

    def _create_session(self, max_retries: int) -> requests.Session:
        """
        Configures and returns a requests.Session with a robust retry strategy.

        This private method sets up the session headers and the retry logic that
        will be used for all outgoing requests.

        Args:
            max_retries: The maximum number of retries for failed requests.

        Returns:
            A requests.Session object configured with headers and retry logic.
        """
        session = requests.Session()
        session.headers.update(
            {
                # The User-Agent is crucial for the CrossRef Polite Pool.
                "User-Agent": f"bib-ami/1.0 (mailto:{self.email})",
                "Accept": "application/json",
            }
        )

        # Define a retry strategy for specific HTTP status codes.
        # This will automatically retry on common server errors or rate limits.
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],  # Codes to retry on.
            backoff_factor=1,  # e.g., sleep for 1s, 2s, 4s between retries.
            respect_retry_after_header=True,
        )

        # Mount the retry strategy to the session for all HTTPS requests.
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def get_doi_for_entry(self, entry: Dict[str, Any]) -> Optional[str]:
        """
        Queries CrossRef using metadata to find the most likely DOI for an entry.

        This method constructs a query based on the entry's title and author,
        as these are the most reliable fields for finding a match.

        Args:
            entry: A dictionary representing a citation, expected to have
                at least a 'title' key.

        Returns:
            The found DOI as a string, or None if no match is found or an
            error occurs.
        """
        title = entry.get("title")
        if not title:
            logging.warning(
                f"Entry with ID '{entry.get('ID', 'unknown')}' is missing a title for lookup."
            )
            return None

        # Build query parameters for the API request.
        params = {"query.title": title, "rows": 1}
        if "author" in entry and entry["author"]:
            # Using just the first author's last name is often sufficient and robust.
            first_author_lastname = entry["author"].split(",")[0].strip()
            params["query.author"] = first_author_lastname

        logging.info(f"Querying CrossRef for title: '{title}'")
        try:
            response = self.session.get(
                self.BASE_URL, params=params, timeout=self.timeout
            )
            response.raise_for_status()  # Raises an HTTPError for bad responses.

            data = response.json()
            items = data.get("message", {}).get("items", [])

            if items:
                doi = items[0].get("DOI")
                if doi:
                    logging.info(f"Found DOI {doi} for title: '{title}'")
                    return doi

            logging.warning(f"No DOI match found for title: '{title}'")
            return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for title '{title}': {e}")
            return None

    def get_metadata_by_doi(self, doi: str, original_entry: dict) -> Optional[dict]:
        """
        Fetches metadata for a given DOI and logs a rich diff of the result.

        This method leverages the client's session to ensure robust request
        handling with retries.

        Args:
            doi: The DOI string to query.
            original_entry: The original BibTeX entry dictionary for comparison.
                            Expected to have 'title' and 'author' keys.

        Returns:
            The metadata message from CrossRef as a dictionary, or None if the
            request fails.
        """
        # Construct the full URL for the specific work
        url = f"{self.BASE_URL}/{doi}"

        # Prepare the payload for structured logging
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "doi": doi,
            "query_url": url,
            "original_entry": {
                "title": original_entry.get("title", ""),
                "authors": original_entry.get("author", "").split(' and ')
            }
        }

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()  # Raises HTTPError for bad responses

            data = response.json()['message']

            # Prepare data for diffing and logging
            retrieved_title = " ".join(data.get('title', []))
            retrieved_authors = [
                f"{author.get('given', '')} {author.get('family', '')}".strip()
                for author in data.get('author', [])
            ]

            log_payload.update({
                "status": "SUCCESS",
                "retrieved_entry": {
                    "title": retrieved_title,
                    "authors": retrieved_authors
                },
                "diff": {
                    "title_diff": get_title_diff(log_payload["original_entry"]["title"], retrieved_title),
                    "authors_diff": get_authors_diff(log_payload["original_entry"]["authors"], retrieved_authors)
                }
            })
            self.results_logger.info(log_payload)

            logger.info(f"Successfully retrieved and logged metadata for DOI: {doi}")
            return data

        except requests.exceptions.RequestException as e:
            log_payload.update({
                "status": "FAILURE",
                "error_message": str(e)
            })
            self.results_logger.info(log_payload)
            logger.error(f"Failed to retrieve metadata for DOI: {doi}. Error: {e}")
            # We return None to signal failure, consistent with get_doi_for_entry
            return None
