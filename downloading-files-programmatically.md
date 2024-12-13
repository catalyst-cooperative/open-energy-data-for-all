---
title: Downloading files programmatically
teaching: 0
exercises: 0
---

:::::::: questions

* How can I get data when there isn't a 'download' link?
* How can I work with data that is behind an API with access restrictions?

::::::::

:::::::: objectives

* request data from a REST API using `requests`
* authenticate to a REST API using HTTP basic auth, bearer tokens, etc.
* explore directories in AWS cloud buckets
* download data from AWS using pandas

::::::::

:::::::: challenge

Make a `GET` request to `https://www.catalyst.coop` using `requests`!

:::: solution

```python
import requests

requests.get("https://www.catalyst.coop")
```

::::

::::::::

:::::::: keypoints

* `pandas.read_*` can read tabular data from remote servers & cloud storage as if it was on your local computer
* `requests` can get data from APIs, though you'll have to do the translation from their response format into `pandas.DataFrame` yourself
* To get access to access-restricted APIs, you will usually pass in an API key, as a request *header* or as a request *parameter*. Both `requests` and `pandas.read_*` have the ability to do this.

::::::::