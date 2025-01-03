---
title: Accessing remote data
teaching: 0
exercises: 0
---

:::::::: questions

* How can I access the latest version of a frequently updated dataset without saving it to my hard drive every time?
* How can I work with data that is behind a web API?

::::::::

:::::::: objectives

* Read remote files into `pandas` dataframes
* Investigate the inputs to and outputs from an API

::::::::

## Reading files into `pandas` directly

You asked around about the `eia923_2022.parquet` file and found out that it came from the Public Utility Data Liberation project. After a bit of online digging you find that they update their data nightly! You want to get your hands on more up-to-date data, so you want to check this out. Downloading a new file each day seems like a pain, though. You seem to remember that the documentation for `pandas.read_parquet()` mentions that the file path "could be a URL." Let's try it!

<!-- TODO get the right URL for the corresponding parquet file -->
```python
import pandas as pd

df = pd.read_parquet("https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/core_eia923__monthly_generation_fuel.parquet")

print(df.report_date.value_counts())
```

Indeed, `read_parquet()` does handle URLs without a hiccup! You can see that there are rows for data through 2024.

:::::::: challenge

<!-- TODO 2025-01-03 add the link, and previous Excel example, here. -->
Adapt your previous Excel-reading code to read the same Excel file directly from the Internet. You should be able to find the file here: ...

:::: solution

Much like `pd.read_excel` can read from a URL just as easily as it can read from a local file.

```python
pd.read_excel("https://raw.githubusercontent.com/...", ...)
```
::::

::::::::

:::::::: callout
If the person maintaining the remote data updates the data without changing the URL, you will get the new version. This can be very useful when exploring data!

This can also be very annoying when you want your analysis to remain stable! In that case, you can try to find data that's hosted on a services like [Zenodo](https://zenodo.org/) which is designed to provide stable URLs. Many data providers also provide distinct URLs for each specific data version as well as a pointer to the latest data version. Of course, archiving the data yourself and managing the data versions can also work.
::::::::

## Using `requests` to download files

It's nice to use functions in the `pd.read_*()` family with a URL, but sometimes you need to do a little bit of reshaping of the data before you can actually use `pd.read_*()`. We saw this with the XML file earlier. In those cases, you can stil tell your code to download the file instead of having to download it yourself.

While Python has some code in the standard library to help you read data from a URL, the [`requests` library](https://requests.readthedocs.io/en/latest/user/quickstart/) is easier to use and also extremely popular, so we'll focus on using that.

To read a URL we use the [`requests.get()` method](https://requests.readthedocs.io/en/latest/api/#requests.get), which returns a [`requests.Response` object](https://requests.readthedocs.io/en/latest/api/#requests.Response):

```python
import requests

response = requests.get("URL")
```

<!-- TODO think about whether we want to have an example of read_xml here - since we'd then need to do io.StringIO, etc. probably not worth it?  -->

The `Response` object has many useful methods and properties, but for now we can focus on how to get the data back out:
* `response.text` will provide the returned data as a *text string* 
* `response.json()` will parse the returned data as if it were JSON, and provide a Python list or dictionary.

:::::::: challenge

The same JSON file you dealt with earlier is available online at raw.gihubusercontent.com/...

How would you read the file contents into a dictionary called `result` without manually downloading it to your hard drive?

a.  ```python
    with open("URL") as f:
        result = f.read()
    ```
a.  ```python
    result = json.loads(requests.get("URL").text)
    ```
a.  ```python
    result = requests.get("URL").json()
    ```
a.  ```python
    with requests.get("URL") as f:
        result = f.json()
    ```

:::: solution

The answer is

```python
result = requests.get("URL").json()
```

The other answers are wrong because:
* `open()` can only read from a file on your local computer.
* `json.loads(requests.get("URL").text)` does work, but this functionality is more directly achieved with `Response.json()`
* You don't need to use `with` here because there is no cleanup required after a web request returns.
::::
    
::::::::


## Introduction to APIs

The previous postdoc left a note that he had gotten the JSON files straight from the EIA API. While you might not have dealt with a web API before, you have the tools to do so now and resolve to jump in.

A useful mental model for a web API is that of a "function call over the Internet."

With a function call to `some_function(param_1=foo, param_2=bar)`, you are asking your computer to run the code that is referred to by `some_function`, and telling it that `param_1` should take the value of `foo` and `param_2` should take the value of `bar`. You learned about the function, the parameters, and what types of input they take, by reading the documentation. Then it returns a value, which you also expect based on the documentation.

With a call to a web API, you are asking someone else's computer to run some code, using some inputs, and then it returns a value back to you.

<!-- TODO make a comparison table here -->

Emphasize that every API is different, the core skill is reading the docs & figuring out how it works. (what are the params, and how do you pass them?) (connect back to the read_* functions from last lesson)

## Case study: EIA API

Aside: API keys are sensitive information, like passwords. Don't store them in your code. store them in env vars instead.

:::::::: challenge

get your api key stored in env var and print it from python

::::::::

Link to EIA documentation + include relevant snippets of it in the actual lesson.

Example: hit the EIA API for monthly generation data.

explain result limits and pagination, and that we'll talk about how to get around pagination in the next lesson

Example: modify previous code to do yearly. Oops, it's actually supposed to be "annual".
Example: discuss error codes when talking about the error message

:::::::: challenge

<!-- TODO: get specific about which fuel consumption data -->
TODO: break this up into multiple steps:
* figure out what the valid options are:
    * here's a snippet of the documentation. https://www.eia.gov/opendata/documentation.php#Examiningametadatarequ
    * Which one of these endpoints would let us figure out what valid data columns exist?
* figure out which option you actually need
    * 
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

TODO: break this out into its own exercise where input is EIA documentation, output is "consumption-uto" or whatever.
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

:::::::: challenge

You want to get Colorado generation data.

<!-- TODO: faceting as a MCQ instead of all these "add data, add sort, etc." questions -->
* make sure it hits "can you read the EIA documentation and figure out the right way to do something"

* maybe example about facets?
  * look for list of facets
  * explain the facet[facet_name][list index]=value syntax - which is a lot easier to understand if you've already seen the data[list index]=value syntax.
  * explain facet[facet_name][list_index]=adofadfalsdkf returning nothing
    * stateid = California doesn't return anything, stateid=CA probably does
  
::::::::


* other apis are different from this one.

## Generalizing to other APIs

:::::::: challenge
How would you generalize this to other APIs?
MCQ: look at this. and then tell us which requests.get() call will work for doing whatever

https://www.epa.gov/power-sector/cam-api-portal#/swagger/facilities-mgmt

* read the EPA CAMD API docs and get some clean air data back

::::::::

::::::::

:::::::: keypoints

* `pandas.read_*` can read tabular data from remote servers & cloud storage as if it was on your local computer
* `requests` can get data that's not in the right shape for `pandas.read_*`, so you can then get it into the Pandas shape APIs, though you'll have to do the translation from their response format into `pandas.DataFrame` yourself
* To get access to access-restricted APIs, you will usually pass in an API key, as a request *header* or as a request *parameter*. Both `requests` and `pandas.read_*` have the ability to do this.

::::::::