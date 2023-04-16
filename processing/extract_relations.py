"""Extracts relations from Wikipedia articles and saves them to a JSON file."""
import json

from lib.utils import save_file
from lib.relations import calculate_strong_relations
from lib.mediawiki_parser import parse_mediawiki_text_and_add_to_article


INPUT_FILE = './data/wikipedia-combined.json'
OUTPUT_FILE_ALL = './data/wikipedia_relations_all.json'
OUTPUT_FILE_RELATIONS = './data/wikipedia_relations.json'
OUTPUT_FILE_WEAK_RELATIONS = './data/wikipedia_weak_relations.json'

DERIVE_RELATIONS = False
WEAK_RELATION_MAX = 2


def extract_from_articles(articles):
    """Extracts relations from articles."""
    missing_wikidata_id = []
    all_strong_relations = []
    processed = 0
    for article in articles:
        processed += 1
        if processed % 500 == 0:
            print(f'Processed {processed} articles')

        if not 'wikidata_id' in article:
            missing_wikidata_id.append(article['title'])

        article = parse_mediawiki_text_and_add_to_article(article)

        article['strong_relations'] = calculate_strong_relations(
            article, DERIVE_RELATIONS)
        all_strong_relations.extend(article['strong_relations'])

    print(f'Found {len(missing_wikidata_id)} articles without Wikidata IDs')
    print(f'Found {len(all_strong_relations)} strong relations')

    return all_strong_relations


with open(INPUT_FILE, 'r', encoding='utf8') as open_file:
    data = json.load(open_file)  # [:1000]

print(f'Loaded {len(data)} articles')

print('Extracting relations...')
strong_relations = extract_from_articles(data)

all_relations = []
weak_relations = []
for item in data:
    all_relations.extend(item['all_pairs'])

    for weak_relation in item['weak_relations'][:WEAK_RELATION_MAX]:
        # cheap trick to avoid category pages and files
        if '.' in weak_relation or ':' in weak_relation:
            continue
        weak_relations.append({
            'type': 'weak',
            'source': item['title'],
            'target': weak_relation,
        })

print(f'Found {len(weak_relations)} weak relations')

print('Saving to files...')

save_file(data, OUTPUT_FILE_ALL)
save_file(weak_relations, OUTPUT_FILE_WEAK_RELATIONS)
save_file(strong_relations, OUTPUT_FILE_RELATIONS)
