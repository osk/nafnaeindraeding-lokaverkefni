"""Tests for the articles parser"""
from lib.articles_parser import parse_articles_from_string


def test_articles_parser_single():
    """Test that the parser works for a single line"""
    input_str = """
    <mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="is">
   <page>
    <title>Verslunarmannahelgin</title>
    <ns>0</ns>
    <id>10899</id>
    <revision>
      <id>1719477</id>
      <parentid>1709045</parentid>
      <timestamp>2021-05-15T16:46:02Z</timestamp>
      <contributor>
        <username>InternetArchiveBot</username>
        <id>75347</id>
      </contributor>
      <comment>Bjarga 1 heimildum og merki 0 sem dauðar.) #IABot (v2.0.8</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text bytes="1948" xml:space="preserve">texti</text>
      <sha1>i8k6t99569ru8qwh52u9ujodypko3bk</sha1>
    </revision>
  </page>
</mediawiki>
    """

    parsed = parse_articles_from_string(input_str, [0])

    assert parsed == [
        {"id": 10899, "namespace": 0, "title": "Verslunarmannahelgin", "text": "texti"}
    ]


def test_articles_parser_redirect():
    """Test that the parser works for a single line"""
    input_str = """
    <mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="is">
    <page>
    <title>X</title>
    <ns>0</ns>
    <id>65229</id>
    <redirect title="Y" />
    <revision>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text bytes="40" xml:space="preserve">t</text>
      <sha1>ez6j47ek0bcpma4w4jri28kcqk07n56</sha1>
    </revision>
  </page>
</mediawiki>
    """

    parsed = parse_articles_from_string(input_str, [0])
    print(parsed)
    assert parsed == [
        {"id": 65229, "namespace": 0, "title": "X", "text": "t", "redirect": "Y"}
    ]
