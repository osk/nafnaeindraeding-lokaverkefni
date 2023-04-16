"""Tests for the props parser module"""

from lib.props_parser import parse_page_props_for_wikidata_ids


def test_props_parser_single():
    """Test that the parser works for a single line"""
    input_str = "(639,'wikibase_item','Q8990577',NULL)"

    parsed = parse_page_props_for_wikidata_ids(input_str)

    assert parsed == [{"id": 639, "wikidata_id": "Q8990577"}]


def test_props_parser_many():
    """Test that the parser works for a many matches in a single line"""
    input_str = "(620,'page_image_free','MartinLuther-workshopCranachElder.jpg',NULL),(620,'wikibase_item','Q9554',NULL),(621,'wikibase-badge-Q70893996','1',1),(621,'wikibase_item','Q225997',NULL),(623,'wikibase_item','Q2076',NULL),(630,'wikibase_item','Q1328144',NULL),(631,'wikibase_item','Q110',NULL),(632,'wikibase_item','Q217724',NULL),(639,'wikibase_item','Q8990577',NULL)"

    parsed = parse_page_props_for_wikidata_ids(input_str)

    assert parsed == [
        {"id": 620, "wikidata_id": "Q9554"},
        {"id": 621, "wikidata_id": "Q225997"},
        {"id": 623, "wikidata_id": "Q2076"},
        {"id": 630, "wikidata_id": "Q1328144"},
        {"id": 631, "wikidata_id": "Q110"},
        {"id": 632, "wikidata_id": "Q217724"},
        {"id": 639, "wikidata_id": "Q8990577"},
    ]
