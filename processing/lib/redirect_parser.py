"""
Parser for Wikipedia redirects from redirect table from Wikipedia dump.

Table definition:

```mysql
CREATE TABLE `redirect` (
  `rd_from` int(8) unsigned NOT NULL DEFAULT 0,
  `rd_namespace` int(11) NOT NULL DEFAULT 0,
  `rd_title` varbinary(255) NOT NULL DEFAULT '',
  `rd_interwiki` varbinary(32) DEFAULT NULL,
  `rd_fragment` varbinary(255) DEFAULT NULL,
  PRIMARY KEY (`rd_from`),
  KEY `rd_ns_title` (`rd_namespace`,`rd_title`,`rd_from`)
);
```
"""
import re


def parse_redirects_from_string(input_str):
    """Parse a string from a redirect table dump for redirects."""
    # TODO actually parse the mysql syntax

    # from, namespace, title, interwiki, fragment
    redirect_regex = re.compile(r"\((\d+),(\d+),\'(.*?)\',\'(.*?)\',\'(.*?)\'\)")
    matches = redirect_regex.findall(input_str)

    data = []
    for match in matches:
        data.append(
            {
                "from": int(match[0]),
                "namespace": int(match[1]),
                "title": match[2],
                "interwiki": match[3],
                "fragment": match[4],
            }
        )

    return data


def parse_redirects_from_file(file):
    """Parse a file from a redirect table dump for redirects."""
    with open(file, "rb") as open_file:
        lines = open_file.read().decode("utf-8", errors="ignore")

    return parse_redirects_from_string(lines)
