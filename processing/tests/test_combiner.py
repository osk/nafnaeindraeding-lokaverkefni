"""Tests for the combiner module"""
from lib.combiner import combine_data


def test_combine_data():
    """Test that the combiner works"""
    wikidata = [
        {"id": 1, "wikidata_id": "Q1"},
        {"id": 2, "wikidata_id": "Q2"},
    ]
    redirects = [
        {"from": 99, "title": "Article 1"},
        {"from": 999, "title": "Article 2"},
        {"from": 9999, "title": "Article 2"},
    ]
    articles = [
        {"id": 1, "title": "Article 1", "namespace": 0, "text": "Text 1"},
        {"id": 2, "title": "Article 2", "namespace": 0, "text": "Text 2"},
        {
            "id": 99,
            "title": "Article 1 alias",
            "namespace": 0,
            "text": "Text 2",
            "redirect": "Article 1",
        },
        {
            "id": 999,
            "title": "Article 2 alias",
            "namespace": 0,
            "text": "Text 2",
            "redirect": "Article 2",
        },
        {
            "id": 9999,
            "title": "Article 2 alias 2",
            "namespace": 0,
            "text": "Text 2",
            "redirect": "Article 2",
        },
    ]

    combined = combine_data(wikidata, redirects, articles)

    assert combined["data"] == [
        {
            "id": 1,
            "title": "Article 1",
            "namespace": 0,
            "text": "Text 1",
            "wikidata_id": "Q1",
            "aliases": ["Article 1 alias"],
        },
        {
            "id": 2,
            "title": "Article 2",
            "namespace": 0,
            "text": "Text 2",
            "wikidata_id": "Q2",
            "aliases": ["Article 2 alias", "Article 2 alias 2"],
        },
    ]
