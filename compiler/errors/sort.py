from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import requests  # requests==2.28.1


def sort_tsv_files():
    """Sorts TSV files in the 'source' directory by their keys."""
    for p in Path("source").glob("*.tsv"):
        with p.open() as f:  # Replaced open() with Path.open()
            reader = csv.reader(f, delimiter="\t")
            dct = {k: v for k, v in reader if k != "id"}  # Dictionary comprehension
            keys = sorted(dct)

        with p.open("w") as f:  # Replaced open() with Path.open()
            f.write("id\tmessage\n")
            for i, item in enumerate(keys, start=1):
                f.write(f"{item}\t{dct[item]}")
                if i != len(keys):
                    f.write("\n")


def scrape_telegram_errors():
    """Scrapes error data from Telegram's API and updates corresponding TSV files."""
    base_url = "https://corefork.telegram.org"
    api_errors_path = "/api/errors"
    response = requests.get(base_url + api_errors_path)
    if response.status_code != 200:
        print("Failed to fetch errors from Telegram API")
        sys.exit(1)

    # Extract link to additional error details
    html_content = response.text
    link_pattern = r'<a href="(.*)">here.*</a>'
    match = re.search(link_pattern, html_content)
    if not match:
        print("No error details found")
        return

    error_url = base_url + match[1]
    error_response = requests.get(error_url)
    if error_response.status_code != 200:
        print("Failed to fetch detailed errors")
        sys.exit(1)

    errors_data = error_response.json()
    process_errors(errors_data, base_url)


def process_errors(errors_data: dict, base_url: str):
    """Processes errors and updates the TSV files with error messages."""
    error_entries = errors_data.get("errors", {})
    descriptions = errors_data.get("descriptions", {})

    for error_code, error_list in error_entries.items():
        dct = {}

        # Process each error
        for error in error_list:
            if error.endswith("_*"):
                continue

            description = descriptions.get(error, "")
            description = format_description(description, base_url)
            formatted_key = error.replace("_%d", "_X")
            dct[formatted_key] = description

        update_tsv_files(error_code, dct)


def format_description(description: str, base_url: str) -> str:
    """Formats the description by replacing specific characters and links."""
    description = description.replace("%d", "{value}")
    description = description.replace("&raquo;", "»")
    description = description.replace("&laquo;", "«")
    return description.replace("](/api/", f"]({base_url}/api/")


def update_tsv_files(error_code: str, dct: dict):
    """Updates the TSV files for the given error code with the provided dictionary of error messages."""
    for p in Path("source/").glob(f"{error_code}*.tsv"):
        with p.open() as f:  # Replaced open() with Path.open()
            reader = csv.reader(f, delimiter="\t")
            dct.update(
                {k: v for k, v in reader if k != "id"}
            )  # Dictionary comprehension

        keys = sorted(dct)

        with p.open("w") as f:  # Replaced open() with Path.open()
            f.write("id\tmessage\n")
            for i, item in enumerate(keys, start=1):
                f.write(f"{item}\t{dct[item]}\n")


if sys.argv[1] == "sort":
    sort_tsv_files()
elif sys.argv[1] == "scrape":
    scrape_telegram_errors()
