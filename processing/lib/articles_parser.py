"""
Parse articles from Wikipedia XML dump.
"""
import xml.etree.ElementTree as ET


# TODO better NS handling
XML_NS = "{http://www.mediawiki.org/xml/export-0.10/}"


def parse_articles_from_string(input_str, namespaces):
    """
    Parse a string from a Wikipedia XML dump for articles
    returns a list of dicts with keys: title, id, namespace, text
    """
    root = ET.fromstring(input_str)

    data = []
    for child in root:
        item = {}
        if child.tag != XML_NS + "page":
            continue

        if child.find(XML_NS + "ns").text not in [str(ns) for ns in namespaces]:
            # print('skipping', child.find(XML_NS + 'ns').text)
            continue

        for subchild in child:
            if subchild.tag == XML_NS + "title":
                item["title"] = subchild.text
            if subchild.tag == XML_NS + "id":
                item["id"] = int(subchild.text)
            if subchild.tag == XML_NS + "ns":
                item["namespace"] = int(subchild.text)
            if subchild.tag == XML_NS + "redirect":
                item["redirect"] = subchild.attrib["title"]
            if subchild.tag == XML_NS + "revision":
                for subsubchild in subchild:
                    if subsubchild.tag == XML_NS + "text":
                        item["text"] = subsubchild.text
        data.append(item)

    return data


def parse_articles_from_file(file, namespaces):
    """Parse a file from a Wikipedia XML dump for articles."""
    with open(file, "rb") as open_file:
        lines = open_file.read().decode("utf-8", errors="ignore")

    return parse_articles_from_string(lines, namespaces)
