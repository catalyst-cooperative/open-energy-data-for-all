---
title: Accessing remote data
teaching: 0
exercises: 0
---

:::::::: questions

* How can I access the latest version of a frequently updated dataset without downloading it every time?
* How can I work with data that is behind an API with access restrictions?

::::::::

:::::::: objectives

* Access data over the Internet using `pandas`
* Access data over the Internet using `requests`
* Identify when to use `requests` vs. `pandas`
* Request data from a REST API that requires authentication

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
* `requests` can get data that's not in the right shape for `pandas.read_*`, so you can then get it into the Pandas shape APIs, though you'll have to do the translation from their response format into `pandas.DataFrame` yourself
* To get access to access-restricted APIs, you will usually pass in an API key, as a request *header* or as a request *parameter*. Both `requests` and `pandas.read_*` have the ability to do this.

::::::::