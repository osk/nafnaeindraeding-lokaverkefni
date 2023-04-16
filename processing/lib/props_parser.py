"""
Parser for Wikidata IDs from page_props table from Wikipedia dump.
"""
import re


def parse_page_props_for_wikidata_ids(input_str):
    """Parse a string from a page_props table dump for Wikidata IDs."""
    # TODO actually parse the mysql syntax
    wikibase_regex = re.compile(r"\((\d+),\'wikibase_item\',\'(Q\d+)\',")

    matches = wikibase_regex.findall(input_str)

    data = []
    for match in matches:
        data.append({"id": int(match[0]), "wikidata_id": match[1]})

    return data


def parse_page_props_for_wikidata_ids_from_file(file):
    """Parse a file from a page_props table dump for Wikidata IDs."""
    with open(file, "rb") as open_file:
        lines = open_file.read().decode("utf-8", errors="ignore")

    return parse_page_props_for_wikidata_ids(lines)
