"""
Parse Wikipedia dump files for redirects, articles, Wikidata IDs and relations.
Saves to a single JSON file.
"""
from lib.props_parser import parse_page_props_for_wikidata_ids_from_file
from lib.redirect_parser import parse_redirects_from_file
from lib.articles_parser import parse_articles_from_file
from lib.combiner import combine_data
from lib.utils import save_file

ARTICLE_XML_FILE = './data/iswiki-20230320-pages-articles.xml'
# ARTICLE_XML_FILE = './data/small.xml'
REDIRECTS_FILE = './data/iswiki-20230320-redirect.sql'
PAGE_PROPS_FILE = './data/iswiki-20230320-page_props.sql'
OUTPUT_FILE = './data/wikipedia-combined.json'

# Wikipedia namespaces to include (see mediawiki/siteinfo/namespaces)
#                  page 👇  👇 sniðmát
# WIKIPEDIA_NAMESPACES = [0, 10]
WIKIPEDIA_NAMESPACES = [0]

wikidata = parse_page_props_for_wikidata_ids_from_file(PAGE_PROPS_FILE)
print(f'Found {len(wikidata)} items with Wikidata IDs')

redirects = parse_redirects_from_file(REDIRECTS_FILE)
print(f'Found {len(redirects)} redirects')

articles = parse_articles_from_file(ARTICLE_XML_FILE, WIKIPEDIA_NAMESPACES)
print(f'Found {len(articles)} articles')

print('Combining data...')
combined = combine_data(wikidata, redirects, articles)

if len(combined["problems"]) > 0:
    print('Potential roblems:')
    for problem in combined["problems"]:
        print(problem)

print('Saving to file...')
save_file(combined["data"], OUTPUT_FILE)
