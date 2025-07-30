[![CircleCI](https://circleci.com/gh/hrolfrc/bib-ami.svg?style=shield)](https://circleci.com/gh/hrolfrc/bib-ami)
[![ReadTheDocs](https://readthedocs.org/projects/bib-ami/badge/?version=latest)](https://bib-ami.readthedocs.io/en/latest/)
[![Codecov](https://codecov.io/gh/hrolfrc/bib-ami/branch/master/graph/badge.svg)](https://codecov.io/gh/hrolfrc/bib-ami)
[![DOI](https://zenodo.org/badge/1012755631.svg)](https://doi.org/10.5281/zenodo.15795717)

# bib-ami: A Bibliography Integrity Manager

**bib-ami** is a smart command-line tool for cleaning, enriching, and managing the quality of your BibTeX bibliographies. It automates a rigorous data integrity workflow by consolidating `.bib` files, validating every entry against external APIs like CrossRef, and deduplicating records with confidence.

The tool intelligently scores the quality of each reference and triages them based on your own configurable rules, enabling researchers to build a clean, reliable, and auditable bibliography for their LaTeX, Zotero, or other reference management workflows.

## Key Features

  * **Merge & Consolidate:** Combines multiple `.bib` files from a directory into a single source.
  * **Validate & Enrich:** Validates entries against CrossRef to find canonical DOIs, and automatically enriches records with missing data like full author lists, publication years, and ISBNs.
  * **Active DOI Resolution:** Goes beyond just finding a DOI; `bib-ami` verifies that every DOI is active and resolvable via `doi.org`, protecting against stale or invalid identifiers.
  * **Intelligent Deduplication:** Uses verified DOIs as the primary key for accurate deduplication, with a fuzzy-matching fallback for entries without a DOI.
  * **Configurable Quality Gating:** Define your own standards for a "publishable" reference using a simple configuration file. Set quality thresholds (e.g., "Verified", "Confirmed") to automatically triage your entire library.
  * **Centralized Configuration:** Use the `bib-ami config set` command to easily manage your default settings, like your email and quality rules, without ever touching a JSON file.
  * **Detailed Audit Trail:** Provides transparent reporting on every action taken, with quality scores and changes noted directly in the output `.bib` files as comments.

## Getting Started

### 1\. Installation

Ensure you have Python 3.7+ installed. You can install `bib-ami` using pip:

```bash
pip install bib-ami
```

### 2\. Quick Start

To process a directory of `.bib` files, run the following command. You must provide an email address for responsible use of the CrossRef API.

```bash
bib-ami --input-dir path/to/your/bibs --output-file cleaned.bib --email "your.email@example.com"
```

This will produce two files:

  * `cleaned.bib`: Contains the entries that meet your quality standards.
  * `cleaned.suspect.bib`: Contains entries that could not be verified and require manual review. This file is created automatically using a default name based on your main output file.

## Configuration

`bib-ami` is highly configurable. You can set personal defaults for your email and quality filtering rules so you don't have to type them every time. The easiest way to do this is with the `config` command:

```bash
bib-ami config set email "your.email@example.com"
bib-ami config set triage_rules.min_quality_for_final_bib "Verified"
```

For a complete guide on all commands, configuration file locations, and available settings, please see the full **[Usage & Configuration documentation](https://www.google.com/search?q=https://bib-ami.readthedocs.io/en/latest/usage.html)**.