import difflib


def get_title_diff(original_title: str, retrieved_title: str) -> str:
    """
    Generates a human-readable unified diff for two titles.

    Returns 'No change' if the titles are identical.
    """
    if original_title == retrieved_title:
        return "No change"

    # Using splitlines to handle multi-line titles gracefully
    diff = difflib.unified_diff(
        original_title.splitlines(keepends=True),
        retrieved_title.splitlines(keepends=True),
        fromfile='original',
        tofile='retrieved',
    )
    return ''.join(diff) if diff else "No change"


def get_authors_diff(original_authors: list[str], retrieved_authors: list[str]) -> dict:
    """
    Generates a diff for two lists of authors, showing added/removed names.

    Args:
        original_authors: A list of author names from the local entry.
        retrieved_authors: A list of author names from the CrossRef response.

    Returns:
        A dictionary with 'added' and 'removed' author lists.
    """
    # Normalize by sorting to handle order differences
    original_set = set(original_authors)
    retrieved_set = set(retrieved_authors)

    if original_set == retrieved_set:
        return {"added": [], "removed": []}

    added = sorted(list(retrieved_set - original_set))
    removed = sorted(list(original_set - retrieved_set))

    return {"added": added, "removed": removed}
