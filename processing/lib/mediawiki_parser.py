"""Parse MediaWiki text."""
import mwparserfromhell


def parse_template_name(name):
    """Parse a template name."""
    if name.isdigit():
        return None
    return name.strip()


def parse_template_value(value):
    """Parse a template value."""
    return value.strip()


def parse_mediawiki_text(text):
    """Parse a string of MediaWiki text.
    Parse every template and every Wikilink up to the first heading."""
    wikicode = mwparserfromhell.parse(text)

    templates = []
    weak_relations = []
    intro_text_parts = []
    all_pairs = []

    for node in wikicode.nodes:
        # We want all Wikilinks up to the first heading
        if node.__class__.__name__ == "Heading":
            break
        if node.__class__.__name__ == "Wikilink":
            weak_relations.append(str(node.title))

        if node.__class__.__name__ != "Template":
            # TODO strip this text of all mediawiki syntax
            # or do we since we loose context for the weak relations? Maybe both?
            intro_text_parts.append(str(node))

    # We want all templates irregradless of where they are
    for template in wikicode.filter_templates(recursive=False):
        current_template = {"name": str(template.name), "params": []}
        for param in template.params:
            pair = {
                "name": str(param.name),
                "value": str(param.value),
                "parsed_name": parse_template_name(param.name),
                "parsed_value": parse_template_value(param.value),
            }
            current_template["params"].append(pair)
            all_pairs.append(pair)
        templates.append(current_template)

    return {
        "templates": templates,
        "all_pairs": all_pairs,
        "weak_relations": weak_relations,
        "intro_text": "".join(intro_text_parts).strip(),
    }


def parse_mediawiki_text_and_add_to_article(article):
    """Parse the MediaWiki text of an article and add it back to it."""
    parsed_text = parse_mediawiki_text(article["text"])

    article["templates"] = parsed_text["templates"]
    article["all_pairs"] = parsed_text["all_pairs"]
    article["weak_relations"] = parsed_text["weak_relations"]
    article["intro_text"] = parsed_text["intro_text"]

    return article
