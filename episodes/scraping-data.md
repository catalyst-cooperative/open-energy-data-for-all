---
title: "Scraping Data"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I get *all* of the data out of an API call when we've hit the limit for a single request?
- How do I download all the data files from a webpage?
- Can I download files from a webpage even there are no visible links?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Automatically download files from a long listing of links on a page
- Investigate webpage structure with browser dev tools
- Observe network requests and form hypotheses about how to copy them

::::::::::::::::::::::::::::::::::::::::::::::::

* why might you scrape at all?
  * *lots* of links: ~100
  * multiple times
  * frequently updated

### pagination

Motivation: API only returns 5k rows at a time. You want MORE.

Example:

One single limit/offset request - get 10 rows, then show how you can get that as 2 sets of 5 rows instead.

Exercise:
Grab *all* of one specific facet.

Basically - this would be a fill in the blank / complete the code exercise - we have most of the loop body

```python
# get first page
# get total row count
# pre-calculate how many pages there are
all_records = []
for ______:
    # params missing limit & offset
    page_of_data = requests.get("...", params={}).json()
    all_records.append(page_of_data["response"]["data"])
```

### spreadsheets

Motivate: there's data that's available via spreadsheet that's not available via API.

Example:

Grab the 923 spreadsheets that they want with bs4

* grab all links
* filter out the bad ones
* grab the href and the title
* use urljoin to get actual absolute link
* download

Exercise:
Get historical 906 data

https://www.eia.gov/electricity/data/eia923/eia906u.php

```
import bs4


def get_spreadsheet_links(soup) -> list[url]:
    ...

def main():
    soup = bs4...
    links = get_spreadsheet_links(soup)
    for link in links:
        request.get(...)

```

### Further resources

Motivate: sometimes this won't be enough.

* inspect html structure
* javascript
* user agents
* network tab


::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
