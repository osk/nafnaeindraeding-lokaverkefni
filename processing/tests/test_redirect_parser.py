"""Tests for the props parser module"""

from lib.redirect_parser import parse_redirects_from_string


def test_redirects_parser_single():
    """Test that the parser works for a single line"""
    input_str = "(596,0,'Nefnifall','','')"

    parsed = parse_redirects_from_string(input_str)

    assert parsed == [
        {
            "from": 596,
            "namespace": 0,
            "title": "Nefnifall",
            "interwiki": "",
            "fragment": "",
        }
    ]


def test_redirects_parser_many():
    """Test that the parser works for many lines"""
    input_str = "(743,0,'Frumeind','',''),(772,0,'Barnaskóli_Vestmannaeyja','',''),(774,0,'Korn_(hljómsveit)','','')"

    parsed = parse_redirects_from_string(input_str)

    assert parsed == [
        {
            "from": 743,
            "namespace": 0,
            "title": "Frumeind",
            "interwiki": "",
            "fragment": "",
        },
        {
            "from": 772,
            "namespace": 0,
            "title": "Barnaskóli_Vestmannaeyja",
            "interwiki": "",
            "fragment": "",
        },
        {
            "from": 774,
            "namespace": 0,
            "title": "Korn_(hljómsveit)",
            "interwiki": "",
            "fragment": "",
        },
    ]
