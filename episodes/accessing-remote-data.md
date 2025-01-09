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

A useful mental model for a web API is that of a *function call on someone else's computer over the Internet*

Imagine you have a function called `get_electric_power_operational_data` which takes a few different parameters. Maybe you call it like `get_electric_power_operational_data(data_field="generation", frequency="monthly")` and it will return a dataframe with some monthly generation data.

The web API version of that might look like making a request to `https://api.eia.gov/v2/electricity/electric-power-operational-data/data?api_key=XYZXYZXYZ&data[]=generation&frequency=monthly`. Let's break that down.

* `https://api.eia.gov/` specifies which other computer you're making this request to. In this case, this is the EIA API server.
* `/v2/electricity/electric-power-operational-data/data` is the equivalent of the function name `get_electric_power_operational_data` above - it specifies what functionality you are asking for.
* `?api_key=XYZXYZXYZ&data[]=generation&frequency=monthly` is the equivalent of passing in parameters to the function: something like `(api_key="XYZXYZXYZ", data_field="generation", frequency="monthly")`. In this case we need to specify an extra `api_key` field because the other computer wants to verify that you're allowed to ask it to do things. This `?parameter_1=value_1&parameter_2=value_2` syntax is one of the main ways one passes input data to a web API, and is called "URL parameters." The `?` precedes the first parameter, the `=` separates the parameter name from its value, and the `&` separates all parameters from each other.

Learning a web API is similar to learning a new software library. For a software library, you want to quickly zero in on:

* what are the functions that I want to call?
* what are the inputs to those functions?
* what are the outputs?

In the case of a web API, in addition to the above you also need to figure about:

* how do I send the input values?
* how can I get the output values back into my code?
* how do I authenticate myself to the API so it allows my request?

## Case study: EIA API

Let's jump into the EIA API and see how it works!

First of all, the full documentation is [here](https://www.eia.gov/opendata/documentation.php). We'll include relevant links and snippets as we go along.



We'll start with the authentication piece. In the setup instructions, you got an API key, which is effectively the password you use to access the API. Like passwords, API keys are sensitive information. As such, we don't want to hard-code them into our code for the world to see - instead we should store them as environment variables.

:::::::: challenge

Store your API key in an environment variable named `EIA_API_KEY`, so that the following code prints out your API key:


```python
import os

print(os.getenv("EIA_API_KEY"))
```

You might need to look up instructions for your specific shell (run `echo $SHELL` if you're not sure what shell you're using.)

::::::::

Now that we have an API key available to us in Python, we can try to use it. Web APIs just use normal web requests, so `requests` will do the trick.

In the documentation you can see that they expect you to pass the API key as a URL parameter, as well as a few other parameters. While the `?...` syntax works, it gets unwieldy with many parameters. `requests` provides a nice `params` dictionary we can use, which we will do below.

Here's an example of using `requests` to get some data from the EIA API. We've glossed over exactly how to find out which URL to request, and which parameters are available, but we will touch on that later.

```python
import os

import requests

EIA_API_KEY = os.getenv("EIA_API_KEY")

response = requests.get(
    f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data",
    params={
        "api_key": EIA_API_KEY,
        "frequency": "monthly",
        "data[]": "generation",
        "length": 10
    }
)
print(response.json())
```

Here's the output, reformatted to be more readable:

```
{
  "response": {
    "warnings": [
      {
        "warning": "incomplete return",
        "description": "The API can only return 5000 rows in JSON format.  Please consider constraining your request with facet, start, or end, or using offset to paginate results."
      }
    ],
    "total": "4184767",
    "dateFormat": "YYYY-MM",
    "frequency": "monthly",
    "data": [
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "NGO",
        "fuelTypeDescription": "natural gas & other gases",
        "generation": "8.53051",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "OB2",
        "fuelTypeDescription": "biomass",
        "generation": ".306",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "OBW",
        "fuelTypeDescription": "biomass",
        "generation": ".306",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "ORW",
        "fuelTypeDescription": "other renewables",
        "generation": ".306",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "PEL",
        "fuelTypeDescription": "petroleum liquids",
        "generation": "0",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "PET",
        "fuelTypeDescription": "petroleum",
        "generation": "0",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "REN",
        "fuelTypeDescription": "renewable",
        "generation": "69.38363",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "SPV",
        "fuelTypeDescription": "solar photovoltaic",
        "generation": ".61609",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "SUN",
        "fuelTypeDescription": "solar",
        "generation": ".61609",
        "generation-units": "thousand megawatthours"
      },
      {
        "period": "2021-03",
        "location": "SAT",
        "stateDescription": "South Atlantic",
        "sectorid": "6",
        "sectorDescription": "Industrial Non-CHP",
        "fueltypeid": "WAS",
        "fuelTypeDescription": "renewable waste products",
        "generation": ".306",
        "generation-units": "thousand megawatthours"
      }
    ],
    "description": "Monthly and annual electric power operations by state, sector, and energy source.\n    Source: Form EIA-923"
  },
  "request": {
    "command": "/v2/electricity/electric-power-operational-data/data/",
    "params": {
      "api_key": "...",
      "frequency": "monthly",
      "data": [
        "generation"
      ],
      "length": "10"
    }
  },
  "apiVersion": "2.1.8",
  "ExcelAddInVersion": "2.1.0"
}
```

We see a warning, some metadata about the whole response, the actual data we're looking for, and the request that we sent.

The warning says "The API can only return 5000 rows in JSON format.  Please consider constraining your request with facet, start, or end, or using offset to paginate results." This sort of behavior is very common in web APIs - because they have to send their response to you over the Internet, they have to limit the amount of data they send at once. Much like Google search results, you will often need to go through multiple "pages" of response data. We'll deal with how to deal with that later in this lesson.


:::::::: challenge

Imagine a function called `get_electric_power_operational_data()` that runs on your computer, instead of the EIA API server. One might call it like so:

```python
get_electric_power_operational_data(
    some_parameter=some_value,
    ...
)
```

What call to that imaginary function would be equivalent to the API call we just tried out?

:::: solution
```python
get_electric_power_operational_data(
    api_key=EIA_API_KEY,
    frequency="monthly",
    data[]="generation",
    length=10
)
```
::::

::::::::


We can easily modify the code to request data at a yearly granularity:

```python
import os

import requests

EIA_API_KEY = os.getenv("EIA_API_KEY")

response = requests.get(
    f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data",
    params={
        "api_key": EIA_API_KEY,
        "frequency": "yearly",
        "data[]": "generation",
        "length": 10
    }
)
print(response.json())
```

Oops! We got an error response:

```output
{'error': "Invalid frequency 'yearly' provided. The only valid frequencies are 'monthly', 'quarterly', and 'annual'.", 'code': 400}
```

It tells us what the problem is - we need to use the value `annual` instead of `yearly`.

It also tells us a "code" for the error - this expresses the general category of error and is based on the [HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). Mostly you need to know that 4xx means *you* did something wrong and 5xx means *they* did something wrong.

:::::::: challenge

How can we figure out the valid values *without* guessing one and then reading the error message? In many APIs, you will be able to find this information in the documentation. For the EIA API, you have to make a metadata request. Read [that section of the documentation](https://www.eia.gov/opendata/documentation.php#Examiningametadatarequ).

Then, use that to figure out what the valid data columns exist for the `electricity/electric-power-operational-data/` endpoint.

:::: solution

Query the `electricity/electric-power-operational-data` endpoint without `/data`.

```python
import os

import requests

EIA_API_KEY = os.getenv("EIA_API_KEY")

response = requests.get(
    "https://api.eia.gov/v2/electricity/electric-power-operational-data",
    params={
        "api_key": EIA_API_KEY,
    }
)
```

```output
{
  "generation": {
    "alias": "Utility Scale Electricity Net Generation"
  },
  "total-consumption": {
    "alias": "Consumption of Fuels for Electricity Generation and Useful Thermal Output (Physical Units)"
  },
  "consumption-for-eg": {
    "alias": "Consumption of Fuels for Electricity Generation (Physical Units)"
  },
  "consumption-uto": {
    "alias": "Consumption of Fuels for Useful Thermal Output (Physical Units)"
  },
  "total-consumption-btu": {
    "alias": "Consumption of Fuels for Electricity Generation and Useful Thermal Output (BTUs)"
  },
  "consumption-for-eg-btu": {
    "alias": "Consumption of Fuels for Electricity Generation (BTUs)"
  },
  "consumption-uto-btu": {
    "alias": "Consumption of Fuels for Useful Thermal Output (BTUs)"
  },
  "stocks": {
    "alias": "Stocks of Fuel (Physical Units)"
  },
  "receipts": {
    "alias": "Receipts of Fuel (Physical Units)"
  },
  "receipts-btu": {
    "alias": "Receipts of Fuel (BTUs)"
  },
  "cost": {
    "alias": "Average Cost of Fuels (per Physical Unit)"
  },
  "cost-per-btu": {
    "alias": "Average Cost of Fuels (per BTU)"
  },
  "sulfur-content": {
    "alias": "Average Sulfur Content of Consumed Fuel"
  },
  "ash-content": {
    "alias": "Average Ash Content of Consumed Fuel"
  },
  "heat-content": {
    "alias": "Average Heat Content of Consumed Fuels"
  }
}
```

This sort of metadata request is also how we found the `/electricity/electric-power-operational-data/` endpoint in the first place, by first querying `https://api.eia.gov/v2/` and walking down the tree. If you're interested, you can try querying that. What other categories of data are available?
::::

::::::::

:::::::: challenge

What is wrong with this API call?

```python
response = requests.get(
    url="https://api.eia.gov/v2/electricity/electric-power-operational-data/data/",
    params={
        "api_key": EIA_API_KEY,
        "frequency": "annual",
        "data[]": "consumption",
        "length": 5
    }
)
```

:::: solution

The JSON response had information about the error:

```json
{
    'error': "Invalid data 'consumption' provided. The only valid data are 'generation', 'total-consumption', 'consumption-for-eg', 'consumption-uto', 'total-consumption-btu', 'consumption-for-eg-btu', 'consumption-uto-btu', 'stocks', 'receipts', 'receipts-btu', 'cost', 'cost-per-btu', 'sulfur-content', 'ash-content', and 'heat-content'.",
    'code': 400
}
```

This suggests that if we change the `data[]` parameter to `total-consumption`, `consumption-for-eg`, `consumption-uto`, etc. we should get something back. 

Which one we should change it to depends on what you want.

::::
::::::::



:::::::: challenge

<!-- TODO this is not actually taught *anywhere* in the docs. --> 
<!-- TODO is this challenge... necessary? -->
You want to get generation data for Colorado only. What is the right parameter?

a. `"stateid[]": "Colorado"`
a. `"facets[stateid][]": "Colorado"`
a. `"facets[stateid]": "CO"`
a. `"facets[stateid][]": "CO"`

* make sure it hits "can you read the EIA documentation and figure out the right way to do something"

* maybe example about facets?
  * look for list of facets
  * explain the facet[facet_name][list index]=value syntax - which is a lot easier to understand if you've already seen the data[list index]=value syntax.
  * explain facet[facet_name][list_index]=adofadfalsdkf returning nothing
    * stateid = California doesn't return anything, stateid=CA probably does
  
::::::::


* other apis are different from this one.

## Generalizing to other APIs

Other APIs will be different from the EIA API - both in what functionality is available, and in how you access that functionality. Let's practice reading the documentation for another useful API, this time from the EPA.

[You can find the documentation here.](https://www.epa.gov/power-sector/cam-api-portal#/swagger/facilities-mgmt)

:::::::: challenge

Let's analyze this with the framework we introduced earlier.

* what functions seem useful to you?
* what are their inputs/outputs?
* how do you pass parameters?
* how do you parse the response?
* how do you authenticate?

::::::::

:::::::: challenge
MCQ: look at this. and then tell us which requests.get() call will work for doing whatever

https://www.epa.gov/power-sector/cam-api-portal#/swagger/facilities-mgmt

* read the EPA CAMD API docs and get some clean air data back

::::::::

::::::::

:::::::: keypoints

* `pandas.read_*` can read tabular data from remote servers & cloud storage as if it was on your local computer
* `requests` can get data that's not in the right shape for `pandas.read_*`, so you can then get it into the Pandas shape APIs, though you'll have to do the translation from their response format into `pandas.DataFrame` yourself
* To get access to access-restricted APIs, you will usually pass in an API key, as a request *header* or as a request *parameter*. Both `requests` and `pandas.read_*` have the ability to do this.
* when encountering a new API, ask yourself these questions:
  * what functions seem useful to you?
  * what are their inputs/outputs?
  * how do you pass parameters?
  * how do you parse the response?
  * how do you authenticate?

::::::::
