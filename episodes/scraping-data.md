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

* you might remember seeing that 'warning' from the EIA API about only returning 5000 rows at a time... how can we get more?

* often there are webpages with lots of links to data you want... copy-pasting each link into our code is a pain, and hardly better than just clicking each link to download the data. Is there a better way?

The thread connecting these two questions/problems is that sometimes your data lives behind *many* URLs, not just one.

## Web scraping

Let's start by downloading files from a webpage that has many links - the good old EIA website.

For all the benefits of the API, some of the EIA 923 data is only available through the downloadable spreadsheets - and the spreadsheets are only available by clicking through the list of links on the EIA 923 page:

![Screenshot of the EIA 923 data page. A listing of each year's files is in the right sidebar.](./fig/ep-4/eia-923-spreadsheets.png){alt="Screenshot of the EIA 923 data page. A listing of each year's files is in the right sidebar."}

There's only a couple dozen, so we could probably get away with just downloading the files by clicking.

You can imagine how this would be annoying if you needed to download, say, a hundred files instead. To keep things simple we'll use the EIA data as an example.

### Example: EIA 923

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

OK, so that looks like some XML, which we saw a couple episodes ago. We don't expect a *data table*, though - more a jumble of links. We need to use a different tool to make sense of all this - a library called `beautifulsoup`. For historical reasons it's imported as `bs4`.

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

More importantly, we'll be able to filter through this complicated set of tags.

```python
soup.find_all("title")
```

To get all the links, we need to get all the `a` tags:

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
 <a class="ico zip" href="archive/xls/f923_2020.zip" title="2020"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2019.zip" title="2019"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2018.zip" title="2018"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2017.zip" title="2017"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2016.zip" title="2016"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2015.zip" title="2015"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2014.zip" title="2014"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2013.zip" title="2013"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2012.zip" title="2012"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2011.zip" title="2011"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2010.zip" title="2010"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2009.zip" title="2009"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f923_2008.zip" title="2008"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2007.zip" title="2007"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2006.zip" title="2006"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2005.zip" title="2005"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2004.zip" title="2004"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2003.zip" title="2003"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2002.zip" title="2002"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906920_2001.zip" title="2001"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906nonutil2000.zip" title="2000"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906nonutil1999.zip" title="1999"><span>ZIP</span></a>,
 <a class="ico zip" href="archive/xls/f906nonutil1989.zip" title="1989-1998"><span>ZIP</span></a>]
```

That looks about right - maybe we want to skip those non-utility links at the bottom as well.


```python
eia_923_906s = [a for a in a_with_zip if "nonutil" not in a["href"].lower()]
eia_923_906s
```

OK, now we have our tags, time to download them, right?

```python
for tag in eia_923_906s:
    # get a nice name for the file
    # download the file from the URL
    # write the outputs somewhere
```
* generate a nice name for each file
  * if you just look on the page, everything is called "ZIP"
  * if you look at the links, everything is `fXXX_YYYY`
  * it would be nice to have something readable like `eia_923_2010`
  * there's a title attribute that gets you the year, so let's do some fstring stuff to make this.
  * `file_name = f"eia_923_{tag['title']}"`
* download the URL
  * oh wait, need to clean up the URL
  * clean up the URL:
    * looks like tags have weird fragments: relative paths 
      * ... relative to what? the URL of the page. good thing we have that
    * requests needs an absolute path
    * use urljoin to get an absolute path: `url = urljoin(base_url, fragment)`
  * then put it into normal requests.
* write the outputs somewhere
  * resp.text is... not what you want. because it's binary blob.
    * **TODO** how to explain the difference between text and binary blob...?
  * instead you want resp.content
  * then you need to `with open(filename, "wb") as f: f.write(resp.content)` - wb for 'write binary'
  

### Exercise:

Get historical 906 data off of this site:
https://www.eia.gov/electricity/data/eia923/eia906u.php

**TODO** should we move the first part of this exercise to right after they see the bs4 stuff? might be nice to ground the "do something useful with these tags" if they've played with the tags a bit first
1. get the relevant links using bs4: 10m
2. make filenames, clean urls, download: 10m

```
import bs4
import requests


def get_spreadsheet_links(soup) -> list[url]:
    ...
    
def download_a_link(tag) -> None:
    ...

def main():
    soup = bs4...
    links = get_spreadsheet_links(soup)
    for link in links:
        download_a_link(link)
```

:::: discussion

Why else might you choose to do this instead of just manually collecting links?

* If there are lots of links to download
* If it's a lot of effort to get to each link
* If the data is frequently updated
* If I have to download all the files multiple times

::::

### pagination

* Another place you need lots of URLs is when APIs don't give you everything all at once
* API only returns 5k rows at a time
* this time, you're generating the URLs yourself instead of scraping them from a page
* the process of getting the first 5k rows, then the next 5k rows, etc. is "pagination" - like going to the next page of Google results.

* Closer look at EIA API - check out limit and offset in the docs. also check out the "total" in response

Example:

Get the first 10 rows

Exercise:

Get the second 10 rows

Example:

Get 10 pages:

```python
n_pages = 10
page_size = 10

all_records = []
for page_num in range(n_pages)0:
    offset = page_num * page_size
    requests.get(...)
    all_records.extend(...)
```

Exercise:

We have total XXX rows, how many pages do we need?

```python
import math

total_rows = response["response"]["total"]
page_size = 100
n_pages = math.ceil(total_rows / page_size)
```

Exercise:

OK, now put it all together!

```python
all_records = []
for ______:
    offset = ___
    page_of_data = requests.get("...", params={...}).json()
    all_records.extend(page_of_data["response"]["data"])
```

### Further resources

* Sometimes, there are obstacles. We can't teach you how to overcome all of them here...

* But here is a little guide of "something weird? maybe try searching for these tools/ideas"

* links aren't showing up in your `bs4` a tags?
  * look at the links using the *html inspector*
  * look at what's happening when you download files by using *network tab*
    * when you click something to download data, or when you load in data for a graph, keep an eye on this. you might find some suspicious looking URLs
* is the html you see in browser *different* from what you get from `requests`?
  * sometimes there's code that your browser runs after the initial load. try playwright which automates a browser for you, instead of just using requests. keyword is `headless browser automation`
  * sometimes servers will be mean to you because of who you say you are (*user agent*).
    * giving you some sort of error/captcha
    * just not giving you anything at all
    * if you suspect that... try telling them you're a real human instead of a bot by "spoofing user agent"
* do you get blocked a lot for scraping?
  * try adding some delays in your scraping code so that it's not hammering the server so hard.
  * do double-check the terms & conditions of the website you're using...
  * you might need a 'web scraping proxy' service.


::::::::::::::::::::::::::::::::::::: keypoints

- beautiful soup lets you grab links out of a webpage so that you can then download them
- ... pagination?

::::::::::::::::::::::::::::::::::::::::::::::::
