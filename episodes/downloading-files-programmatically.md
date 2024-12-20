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

* [ ] Access data over the Internet using `pandas`
* [ ] Access data over the Internet using `requests`
* [ ] Identify when to use `requests` vs. `pandas`
* Request data from a REST API that requires authentication

* talk about pagination
::::::::

Motivate: your data might change frequently. Let's just use the latest version online.

Example: parquet file - the latest `stable` one from PUDL has more updated data! Turns out reading from HTTP is easy.

:::::::: challenge

Adapt your previous Excel-reading code to read the same Excel file directly from the Internet. You should be able to find the file here: ...

:::: solution

`pd.read_excel` can read from a URL just as easily as it can read from a local file.

```python
pd.read_excel("https://...", ...)
```
::::

::::::::

Example: XML - you have to do a bit of digging, so pd.read_... doesn't get you there. Use `requests.get` instead. Explain what a requests.Response is.

:::::::: challenge

Adapt this JSON-reading code to read the same JSON file directly from the Internet. You should be able to find the file here: raw.githubusercontent.com/...

```python
import json

import pandas as pd

with open("...") as f:
    raw_json = json.loads(f.read())

dataframe = pd.json_normalize(raw_json, ["response", "data"])
```
:::: solution

You'll need to replace the `open()` call, which reads from local file, with `requests.get`. The `requests.Response` object has a `.json()` method which parses the content as JSON for you.

```python
import requests
import pandas as pd

response = requests.get("https://raw.githubusercontent.com/...")
raw_json = response.json()

dataframe = pd.json_normalize(raw_json, ["response", "data"])
```
::::

OK, we can get stuff from normal HTTP URLs. APIs are really... just complicated URLs. So we can use `requests.get` again.

note to self: or maybe APIs are just function calls that happen over HTTP? Is that a useful mental model? I think so...

Aside: API keys are sensitive information, like passwords. Don't store them in your code.

Link to documentation. Emphasize that every API is different, the core skill is reading the docs & figuring out how it works.

Example: hit the EIA API for monthly generation data.
Example: modify previous code to do yearly. Oops, it's actually supposed to be "annual".

:::::::: challenge

Here's some code that is supposed to ask the EIA API for some fuel consumption data - but it doesn't work. How can we fix it?

```python
import os

import pandas as pd
import requests

EIA_API_KEY = os.getenv("EIA_API_KEY")

response = requests.get(
    url="https://api.eia.gov/v2/electricity/electric-power-operational-data/data/",
    params={
        "api_key": EIA_API_KEY,
        "frequency": "annual",
        "data[]": "consumption",
        "length": 5
    }
)

raw_json = response.json()
print(raw_json)
dataframe = pd.json_normalize(raw_json, ["response", "data"])
print(dataframe)
```

:::: solution

The JSON response had information about the error:

```json
{
    'error': "Invalid data 'consumption' provided. The only valid data are 'generation', 'total-consumption', 'consumption-for-eg', 'consumption-uto', 'total-consumption-btu', 'consumption-for-eg-btu', 'consumption-uto-btu', 'stocks', 'receipts', 'receipts-btu', 'cost', 'cost-per-btu', 'sulfur-content', 'ash-content', and 'heat-content'.",
    'code': 400
}
```

This suggests that if we change the data request to `total-consumption` we should get something back. 

For the EIA API in particular, you can query https://api.eia.gov/v2/electricity/electric-power-operational-data/ to figure out what `total-consumption` corresponds to - which will tell you that it is "Consumption of Fuels for Electricity Generation and Useful Thermal Output (Physical Units)".


```python
import os

import pandas as pd
import requests

EIA_API_KEY = os.getenv("EIA_API_KEY")

response = requests.get(
    url="https://api.eia.gov/v2/electricity/electric-power-operational-data/data/",
    params={
        "api_key": EIA_API_KEY,
        "frequency": "annual",
        "data[]": "total-consumption",
        "length": 5
    }
)

raw_json = response.json()
print(raw_json)
dataframe = pd.json_normalize(raw_json, ["response", "data"])
print(dataframe)
```
:::: 

::::::::

Example: show the documentation about the data[] parameter, then add another data[] field.


:::::::: challenge

Take the above code - how would you modify it to include both `generation` and `total-consumption` data? (maybe skip this and go straight to the 'add a sort' exercise below)

Maybe a straightforward "here's length + offset - do some simple pagination" fill-in-the-blanks problem?

:::: solution

```python
response = requests.get(
    url="https://api.eia.gov/v2/electricity/electric-power-operational-data/data/",
    params={
        "api_key": EIA_API_KEY,
        "frequency": "annual",
        "data[]": "total-consumption",
        "data[]": "generation",
        "length": 5
    }
)
```
::::
::::::::

:::::::: challenge
read the EIA API docs and see if you can sort the results
::::::::



:::::::: challenge
How would you generalize this to other APIs?
* read the EPA CAMD API docs and get some clean air data back
::::::::

::::::::

:::::::: keypoints

* `pandas.read_*` can read tabular data from remote servers & cloud storage as if it was on your local computer
* `requests` can get data that's not in the right shape for `pandas.read_*`, so you can then get it into the Pandas shape APIs, though you'll have to do the translation from their response format into `pandas.DataFrame` yourself
* To get access to access-restricted APIs, you will usually pass in an API key, as a request *header* or as a request *parameter*. Both `requests` and `pandas.read_*` have the ability to do this.

::::::::