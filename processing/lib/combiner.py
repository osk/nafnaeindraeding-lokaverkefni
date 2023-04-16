"""Combine data."""


def combine_data(wikidata, redirects, articles):
    """Combine Wikidata, redirects and articles into a single list of dicts."""
    data = []
    problems = []
    for article in articles:
        if "redirect" in article:
            continue

        item = {}
        item["title"] = article["title"]
        item["id"] = article["id"]
        item["namespace"] = article["namespace"]
        item["text"] = article["text"]
        item["aliases"] = []

        # Find Wikidata ID
        found_wikidata_ids = []
        for wikidata_item in wikidata:
            if wikidata_item["id"] == item["id"]:
                item["wikidata_id"] = wikidata_item["wikidata_id"]
                found_wikidata_ids.append(wikidata_item["wikidata_id"])

        if len(found_wikidata_ids) > 1:
            problems.append(f"Found multiple Wikidata IDs for article {item['title']}")

        # Find aliases via redirects
        for redirect in redirects:
            if redirect["title"] == item["title"]:
                redirected_article = next(
                    (a for a in articles if a["id"] == redirect["from"]), None
                )
                if redirected_article:
                    item["aliases"].append(redirected_article["title"])

        data.append(item)

    return {"data": data, "problems": problems}
