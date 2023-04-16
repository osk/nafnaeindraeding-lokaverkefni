# Data processing

## Data

Download data from a Wikipedia dump (e.g. [Icelandic Wikipedia](https://dumps.wikimedia.org/iswiki/20230320/)) and save the following into `./data`:

- `...pages-articles.xml`
- `...redirect.sql`
- `...page_props.sql`

And update `./wikipedia_combine.py` constants to match.

## Running

```bash
poetry install
poetry run black

# tests
poetry run pytest
poetry run ptw # with watch
```

Run the `wikipedia_combine.py` first to create `./data/wikipedia_combined.json` file with only "real" articles (in namespace `0`, not redirected).

Second, run `extract_relations.py` to create `./data/wikipedia_relations.json` and `./data/wikipedia_relations_all.json`. `wikipedia_relations_all.json` includes all data created while running.
