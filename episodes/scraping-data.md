---
title: "Scraping Data"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I avoid the tedium/error-prone-ness of clicking lots of links or making lots of API requests by hand?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use pagination to get all available data
- Automatically download files from a long listing of links on a page

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

Now we've learned about how to download data from websites and from APIs. But some questions linger...

* often there are webpages with lots of links to data you want... copy-pasting each link into our code is a pain, and hardly better than just clicking each link to download the data. Is there a better way?

* you might also remember seeing that 'warning' from the EIA API about only returning 5000 rows at a time... how can we get more?

The thread connecting these two questions/problems is that sometimes your data lives behind *many* URLs, not just one. So you have to go get a bunch of separate data and glue it all together.

## Web scraping

Let's start by downloading files from a webpage that has many links - the good old EIA website.

For all the benefits of the API, some of the EIA 923 data is only available through the downloadable spreadsheets - and the spreadsheets are only available by clicking through the list of links on the EIA 923 page:

![Screenshot of the EIA 923 data page. A listing of each year's files is in the right sidebar.](./fig/ep-4/eia-923-spreadsheets.png){alt="Screenshot of the EIA 923 data page. A listing of each year's files is in the right sidebar."}

There's only a couple dozen, so we could probably get away with just downloading the files by clicking.

You can imagine how this would be annoying if you needed to download, say, a hundred files instead. To keep things simple we'll use the EIA data as an example.

### Example: EIA 923/906

To get the links, first we need to actually get the webpage that the links are on.

```python
import requests

url = "https://www.eia.gov/electricity/data/eia923/"
response = requests.get(url)

response.text
```

```output
'<!doctype html>\r\n<html>\r\n\r\n<head>\r\n\t<title>\r\n\t\tForm EIA-923 detailed data with previous form data (EIA-906/920) -\r\n\t\tU.S. Energy Information Administration (EIA)\t</title>\r\n\t<meta property="og:title" content="Form EIA-923 detailed data with previous form data (EIA-906/920) - U.S. Energy Information Administration (EIA)">\r\n\t<meta property="og:url" content="https://www.eia.gov/electricity/data/eia923/index.php">\r\n\t<meta name="url" content="https://www.eia.gov/electricity/data/eia923/index.php">\r\n\t<meta name="description" content="Clean Air Act Data Browser" />\r\n\t...
```

OK, so that looks like some XML, which we saw a couple episodes ago. We don't expect a *data table* directly in the page, like we did last time. We're more expecting a jumble of links. We need to use a different tool to make sense of all this - a library called `beautifulsoup`. For historical reasons it's imported as `bs4`.

```python
import bs4
soup = bs4.BeautifulSoup(response.text)

soup
```

The first thing you'll notice is that the output looks neater:
```output
<!DOCTYPE html>
<html>
<head>
<title>
		Form EIA-923 detailed data with previous form data (EIA-906/920) -
		U.S. Energy Information Administration (EIA)	</title>
<meta content="Form EIA-923 detailed data with previous form data (EIA-906/920) - U.S. Energy Information Administration (EIA)" property="og:title"/>
```

We'll also be able to filter through this complicated set of tags.

```python
soup.find_all("title")
```

To get all the links, we need to get all the `a` tags - that's where links in HTML usually live:

```python
soup.find_all("a")
```

```output
[<a name="top"></a>,
 <a href="http://x.com/eiagov/" target="_blank"><span class="ico-sticker twitter"></span></a>,
 <a class="addthis_button_tweet"></a>,
 <a href="https://www.facebook.com/eiagov" target="_blank"><span class="ico-sticker facebook"></span></a>,
 <a class="addthis_button_facebook_like at300b" fb:like:layout="button_count"></a>,
 ...
 <a class="ico zip" href="xls/f923_2024.zip" title="2024"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2023.zip" title="2023"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2022.zip" title="2022"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2021.zip" title="2021"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2020.zip" title="2020"><span>ZIP</span></a>,
 ...
```

:::: challenge

#### Challenge: get all the `a` tags from EIA 906

Lots of the data that is collected in EIA 923 was collected in EIA 906 in the past.

We'll have you work through the scraping steps on the 906 data to get a sense of how this all works.


The first step is to get all the `a` tags from this page:

```
https://www.eia.gov/electricity/data/eia923/eia906u.php
```

Start with this skeleton code:

```python
import bs4
import requests

eia_906_url = "https://www.eia.gov/electricity/data/eia923/eia906u.php"

# get the page contents, then use bs4 to get the `a` tags
```

:::::::: solution
```python
import bs4
import requests

url = "https://www.eia.gov/electricity/data/eia923/eia906u.php"
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text)

a_tags = soup.find_all("a")
```
::::::::

::::

OK, so we see a big list of tags, some of which appear to be links to form 923 ZIP files. The URLs for those are included in an `href` attribute. The world of HTML is vast and chaotic, but almost every URL you'll want to use will live in one of these `href` attributes (it stands for "hypertext reference" if that helps you remember).

We can filter based on attributes like this:

```python
soup.find_all("a", href=True)
```

This shows us only the `a` tags with `href`s defined:

```output
[<a href="http://x.com/eiagov/" target="_blank"><span class="ico-sticker twitter"></span></a>,
 <a href="https://www.facebook.com/eiagov" target="_blank"><span class="ico-sticker facebook"></span></a>,
 <a class="eia-accessibility" href="#page-sub-nav">Skip to sub-navigation</a>,
 <a class="logo" href="/">
 <h1>U.S. Energy Information Administration - EIA - Independent Statistics and Analysis</h1>
 </a>,
 <a class="nav-primary-item-link menu-toggle" href="javascript:;">
```

And then you can filter those only for the ones that point at actual ZIP files:

```python
a_with_zip = [a for a in a_with_href if "zip" in a["href"].lower()]
a_with_zip
```

```output
[<a class="ico zip" href="xls/f923_2024.zip" title="2024"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2023.zip" title="2023"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2022.zip" title="2022"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2021.zip" title="2021"><span>ZIP</span></a>,
 ...
 <a class="ico zip" href="archive/xls/f906920_2003.zip" title="2003"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2002.zip" title="2002"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2001.zip" title="2001"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906nonutil2000.zip" title="2000"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906nonutil1999.zip" title="1999"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906nonutil1989.zip" title="1989-1998"><span>ZIP</span></a>]
```


We probably want to skip those Form 906 links too.

```python
eia_923_links = []
for a in a_with_zip:
  if "f906" not in a["href"].lower():
    eia_923_links.append(a)

eia_923_links
```

:::: challenge

#### Challenge: only get the relevant `a` tags

Let's grab only the `a` tags that are links to the actual data files.

This will look a little bit different from the 923 example, since the links are all to XLS files instead of ZIP files.

Let's start with this code:

```python
import bs4
import requests

eia_906_url = "https://www.eia.gov/electricity/data/eia923/eia906u.php"
response = requests.get(eia_906_url)
soup = bs4.BeautifulSoup(response.text)

# get only the `a` tags that are links to Form 906 data files.
```
:::::::: solution


```python
import bs4
import requests

eia_906_url = "https://www.eia.gov/electricity/data/eia923/eia906u.php"
response = requests.get(eia_906_url)
soup = bs4.BeautifulSoup(response.text)

a_tags = soup.find_all("a", href=True)
eia_906_links = []
for a in a_tags:
    if ".xls" in a["href"].lower():
        eia_906_links.append(a)
```
::::::::
::::

OK, now we have our tags, time to use them to download the data! The EIA 923 data all comes in ZIP files - we'll skip over the handling of those for now. Instead we'll use the 906 data that you just got.

```python
import pandas as pd

eia_923_blobs = []
for a in eia_923_links:
  response = requests.get(a["href"])
  eia_923_blobs.append(response.content)
```

Oh no! We get an error:

```output
MissingSchema: Invalid URL 'xls/f923_2024.zip': No scheme supplied. Perhaps you meant https://xls/f923_2024.zip?
```

Looks like the URL in the `href` is incomplete. It turns out that this is a *relative path* - much like the relative paths you had to deal with when loading data on your computer. The full URL we want is
`https://www.eia.gov/electricity/data/eia923/xls/f923_2024.zip` - which combines the URL of the page we got the link from (`https://www.eia.gov/electricity/data/eia923/eia906u.php`) with the fragment we got in the `href` (`xls/f923_2024.zip`).

This is a super common thing to have to do, so there's a useful bit of the Python standard library for this: `urllib.parse.urljoin`:

```
from urllib.parse import urljoin

urljoin(eia_923_url, "xls/f923_2024.zip")
```

We can also do the string concatenation ourselves with `eia_906_url + "..."`, but there are a surprising amount of details to get wrong here so it's nice to just use the function that works.

Let's add that into our loop:

```
for a in eia_923_links:
  full_link = urljoin(eia_923_url, a["href"])
  response = requests.get(a["href"])
  eia_923_blobs.append(response.content)
```
:::: challenge

#### Challenge: get the Form 906 file contents

OK, so now we know how to scrape a bunch of URLs from a webpage. Let's read the Form 906 files into our program! Since they're XLS files, we can read them directly from a URL using `pandas.read_excel` - no need for manually downloading with `requests`.

Try filling out the body of this for loop.

```python
from urllib.parse import urljoin

import bs4
import requests
import pandas as pd

eia_906_url = "https://www.eia.gov/electricity/data/eia923/eia906u.php"
response = requests.get(eia_906_url)
soup = bs4.BeautifulSoup(response.text)

a_tags = soup.find_all("a", href=True)
eia_906_links = []
for a in a_tags:
    if ".xls" in a["href"].lower():
        eia_906_links.append(a)

eia_906_dataframes = []
for a in eia_906_links:
    ___
```

::::::: solution

```python
for a in eia_906_links:
    full_url = urljoin(eia_906_url, a["href"])
    eia_906_dataframes = pandas.read_excel(full_url)
```
:::::::

::::

Once we've completed the challenge above, we have a list of a bunch of dataframes. To bring them all into one dataframe, we can use `pd.concat`:

```python
mega_906 = pd.concat(eia_906_dataframes)
```

If you use `DataFrame.info()` you can quickly see that some columns (YEAR, FIPST, UTILNAME) are more populated than others (MULTIST, GEN01, etc):

```python
mega_906.info()
```

And if you start to dig into the data a bit, such as pulling out the various values of `YEAR`, you see that you have *plenty* of data cleaning to do before this is really usable for analysis. But at least you have all of the data in one dataframe now! We'll go over some more tips for exploratory data analysis in the next episode.

```python
mega_906.YEAR.value_counts()
```

```output
YEAR
96      10507
97      10468
1999    10296
2000     9617
74       6429
73       6363
75       6362
76       6307
72       6198
71       6130
70       6100
81       5692
85       5692
80       5678
82       5669
84       5661
83       5650
87       5647
86       5634
77       5627
78       5594
79       5554
98       5470
89       5263
88       5241
95       5119
1998     5118
93       5109
91       5107
94       5102
92       5100
90       5074
99         40
0          14
Name: count, dtype: int64
```

:::: discussion

Why might you choose to do all this instead of just manually collecting links?

* If it's a lot of effort to get to each link
* If the data is frequently updated
* If I have to download all the files multiple times
* If I have to combine everything into one big dataset programmatically anyways

::::

### pagination

Another time you'll need lots of URLs is when APIs don't give you everything all at once. For example, the EIA API kept giving us this warning:

```
The API can only return 5000 rows in JSON format.  Please consider constraining your request with facet, start, or end, or using offset to paginate results.
```

So if we want a dataset that's bigger than 5000 rows, we'll need to make multiple requests. Instead of scraping many URLs from a page, we'll be generating the URLs ourselves.

This process of "get N rows, then the next N rows, etc." is called "pagination" - like going to the next page of Google results.

We'll go to the docs to look at this `offset` parameter:

> Offset stipulates the row number the API should begin its return with, out of all the eligible rows our query would otherwise provide.
>
> [...]
>
> `https://api.eia.gov/v2/electricity/retail_sales/data?api_key=xxxxxx&data[]=price&facets[sectorid][]=RES&facets[stateid][]=CO&frequency=monthly&sort[0][column]=period&sort[0][direction]=desc&offset=24`
>
> In the above example, the API will skip over the first 24 eligible rows (offset=24), which translates into 24 months (frequency=monthly).

Let's try it out - first, let's make an API request and look at the output. A few things to note:

* we're filtering for CO generation to get a manageable amount of data that's still more than 5000 rows
* we're sorting by the time period - this lets us have a stable order so that the "next 5000 rows" means something well-defined.

```python
import requests

base_url = "https://api.eia.gov/v2/electricity"
api_key = "3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8"

# remember from last time that the shape is a JSON object with everything in "response"
first_page = requests.get(
  f"{base_url}/facility-fuel/data",
  params={
    "data[]": "generation",
    "facets[state][]": "CO",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "api_key": api_key
  }
).json()["response"]

net_generation.keys()
```

Let's grab the next 5000 rows:

```python
next_page = requests.get(
  f"{base_url}/facility-fuel/data",
  params={
    "data[]": "generation",
    "facets[state][]": "CO",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 5000,
    "api_key": api_key
  }
).json()["response"]
```

And if we wanted to grab the first 5 pages, we could use a `for` loop combined with the `range()` function - here's how `range` works:

```python
for page_num in range(5):
    print(page_num)
```

Here the `range()` lets you go through the loop 5 times.

When we are looking to get *all* of the pages, we can use the `"total"` field in the EIA API response to figure out how many total rows there are:

```python
first_page["total"]
```

```output
155130
```

So there are 155,130 rows in this dataset.

:::: discussion
Question for chat: if we have N rows total, and P rows per page, how many pages do we need to get all the data?

:::::::: solution

$ceil(N/P)$

::::::::
::::

And here's how we'd get from the number of total rows to the number of pages we need:

```python
import math

total_rows = net_generation["total"]
page_size = 5000
num_pages = math.ceil(total_rows / page_size)
```

:::: challenge

#### Challenge: pagination
OK, now let's put it all together! Let's fill in the blanks for this code:

```python
import math

base_url = "https://api.eia.gov/v2/electricity"
api_key = "3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8"

page = requests.get(
  f"{base_url}/facility-fuel/data",
  params={
    "data[]": "generation",
    "facets[state][]": "CO",
    "api_key": api_key
  }
).json()["response"]

total_rows = ___
page_size = 5000
num_pages = ___

all_records = []
for page_num in range(num_pages):
    offset = ___
    page = requests.get(
      f"{base_url}/facility-fuel/data",
      params={
        "data[]": "generation",
        "facets[state][]": "CO",
        ___,
        "api_key": api_key
      }
    ).json()["response"]
    all_records.extend(page_of_data["data"])

df = pd.concat(all_records)
```

:::::::: solution

```python
import math

import pandas as pd
import requests

base_url = "https://api.eia.gov/v2/electricity"
api_key = "3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8"

net_generation = requests.get(
  f"{base_url}/facility-fuel/data",
  params={
    "data[]": "generation",
    "facets[state][]": "CO",
    "api_key": api_key
  }
).json()["response"]

total_rows = int(net_generation["total"])
page_size = 5000
num_pages = math.ceil(total_rows / page_size)

all_records = []

for page_num in range(num_pages):
    offset = page_num * page_size
    print(offset)
    page = requests.get(
      f"{base_url}/facility-fuel/data",
      params={
        "data[]": "generation",
        "facets[state][]": "CO",
        "sort[][column]": "period",
        "sort[][direction]": "desc",
        "offset": offset,
        "api_key": api_key
      }
    ).json()["response"]["data"]
    all_records.extend(pd.DataFrame(page_of_data["data"]))

df = pd.concat(all_records)
```

::::::::

::::

This is just one common way APIs do pagination. You'll have to flex those API learning skills (play with the data, read the docs, bounce back and forth) to learn how each new API handles this.

### Further resources

We've only just scratched the surface of programmatically getting data from the Internet here. Sometimes, there are obstacles. We can't teach you how to overcome all of them, but here is a little troubleshooting guide of "something weird? maybe try searching for these keywords."

* Links not showing up in your `bs4` `a` tags?
  * look at the links using the *html inspector* in your browser dev tools.
  * look at what's happening when you download files by using the *network tab* of your browser dev tools.
    * when you click something to download data, or when you load in data for a graph, keep an eye on this. you might find some suspicious looking URLs
* The HTML you see in *browser dev tools* is different from what you get from `requests`?
  * sometimes there's code that your browser runs after the initial load, which changes the HTML after the fact. `requests` won't catch that, but try `playwright` which runs that post-load code. keyword is `headless browser automation`.
  * sometimes servers will be mean to you because of who you say you are (*user agent*).
    * sometimes they'll give you some sort of error, or a CAPTCHA
    * sometimes they will just not give you any response at all
    * If you suspect that... try telling them you're a real human instead of a bot. Look for "spoofing the user agent" to see guides on how to do this.
* Running into rate limits for making too many requests?
  * Try adding some delays in your scraping code so that it's not hammering the server so hard. The `time.sleep` method here is your friend.
  * Do double-check the terms & conditions of the website you're using - if a website is implementing some rate limit, they probably don't want you using automated tools to download the data in the first place.
  * You might need a 'web scraping proxy' service, which will let you get around a lot of limits.
* Have to download a file to disk instead of turning it into a DataFrame immediately?
  * Use `response.content` to get the literal bytes that the response is made of - this will help with files like ZIP files that don't have a nice text representation.
  * Then use the "wb" mode ("write binary") to write that data to disk:
  ```python
  with open(some_filename, "wb") as f:
      f.write(response.content)
  ```

::::::::::::::::::::::::::::::::::::: keypoints

- beautiful soup lets you grab links out of a webpage so that you can then download them
- if you need to get more than one request worth of results from an API, they usually provide some "pagination" capabilities so you can make all the requests programmatically.
- web scraping is a wide world - if you get stuck, try searching for some of the keywords above.

::::::::::::::::::::::::::::::::::::::::::::::::
