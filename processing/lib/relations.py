"""
Module for calculating relations.

For types of relations we define two methods: a parser and a deriver.

The parser takes a string and parses it into a list of relations from the source. The deriver
takes a list of relations and derives a list of relations from it.

A relation has the following structure:

```json
{
    "type": "<RELATION_TYPE>",
    "source": "<SOURCE_WIKIPEDIA_TITLE>",
    "target": "<TARGET_WIKIPEDIA_TITLE>"
}
```

TODO: relation metadata, add wikidata lookup

Known relations:

* `spouse` (`maki` parsed and derived)
* `studied_at` (`háskóli` parsed)
* `had_as_student` (`háskóli` derived)
"""
import mwparserfromhell


def parse_relation_maki(source, value):
    """
    Parses a `maki` relation and returns a list of spouses, e.g.

    * `[[Ingibjörg Einarsdóttir]] (g. 1845)`
    * `[[Dorrit Moussaieff]], áður [[Guðrún Katrín Þorbergsdóttir]]`
    * `1. [[Elín Haraldsdóttir]] (skilin)<br />2. [[Eliza Jean Reid]]`
    * `John Doe (g. 1980)`

    TODO order is implicit and is not captured correctly (reverse order)
    """
    relations = []
    wikicode = mwparserfromhell.parse(value)
    for node in wikicode.nodes:
        if node.__class__.__name__ == "Wikilink":
            relations.append(
                {
                    "type": "spouse",
                    "source": source,
                    "target": str(node.title),
                }
            )
    return relations


def derive_relation_spouse(relation):
    """Derives a `spouse` relation from a `spouse` relation."""
    if relation["type"] == "spouse":
        return [
            {
                "type": "spouse",
                "source": relation["target"],
                "target": relation["source"],
            }
        ]
    return None


def parse_relation_haskoli(source, value):
    """Parse a `háskóli` relation and returns a list of universities."""
    relations = []
    wikicode = mwparserfromhell.parse(value)
    for node in wikicode.nodes:
        if node.__class__.__name__ == "Wikilink":
            relations.append(
                {
                    "type": "studied_at",
                    "source": source,
                    "target": str(node.title),
                }
            )
    return relations


def derive_relation_studied_at(relation):
    """Derives a `had_as_student` relation from a `studied_at` relation."""
    if relation["type"] == "studied_at":
        return [
            {
                "type": "had_as_student",
                "source": relation["target"],
                "target": relation["source"],
            }
        ]
    return None


def parse_relation_thjoderni(source, value):
    """Parse a `þjóðerni` relation and returns a list of countries."""
    relations = []
    wikicode = mwparserfromhell.parse(value)
    for node in wikicode.nodes:
        if node.__class__.__name__ == "Wikilink":
            relations.append(
                {
                    "type": "born_in",
                    "source": source,
                    "target": str(node.title),
                }
            )
    return relations


def parse_relation_stjornmalaflokkur(source, value):
    """Parse a `stjórnmálaflokkur` relation and returns a list of parties."""
    relations = []
    wikicode = mwparserfromhell.parse(value)
    for node in wikicode.nodes:
        if node.__class__.__name__ == "Wikilink":
            relations.append(
                {
                    "type": "member_of",
                    "source": source,
                    "target": str(node.title),
                }
            )
    return relations


# Map of relation names to their parsers
relation_parsers = {
    "maki": parse_relation_maki,
    "háskóli": parse_relation_haskoli,
    "þjóðerni": parse_relation_thjoderni,
    "stjórnmálaflokkur": parse_relation_stjornmalaflokkur,
    "flokkur": parse_relation_stjornmalaflokkur,
}

relation_derivers = {
    "maki": derive_relation_spouse,
    "háskóli": derive_relation_studied_at,
}


def calculate_strong_relations(article, derive_relations=True):
    """Calculates strong relations between articles based on its data.
    Returns both the parsed and derived relations."""
    relations = []

    for pair in article["all_pairs"]:
        if pair["parsed_name"] and pair["parsed_name"] in relation_parsers:
            parsed_relations = relation_parsers[pair["parsed_name"]](
                article["title"], pair["parsed_value"]
            )
            if parsed_relations:
                relations.extend(parsed_relations)
                if derive_relations and pair["parsed_name"] in relation_derivers:
                    for relation in parsed_relations:
                        derived_relations = relation_derivers[pair["parsed_name"]](
                            relation
                        )
                        if derived_relations:
                            relations.extend(derived_relations)

    return relations
