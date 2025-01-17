---
title: Accessing remote data
teaching: 0
exercises: 0
---

:::::::: questions

* How can I access data without manually saving it to my hard drive?
* How can I work with data that is behind a web API?

::::::::

:::::::: objectives

* Read remote files into `pandas` dataframes
* Investigate the inputs to and outputs from an API

::::::::

## Reading files into `pandas` directly

You asked around about the `eia923_2022.parquet` file and found out that it came from the Public Utility Data Liberation project. After a bit of online digging you find that they update their data nightly! You want to get your hands on more up-to-date data, so you want to check this out. Downloading a new file each day seems like a pain, though. You seem to remember that the documentation for `pandas.read_parquet()` mentions that the file path "could be a URL." Let's try it!

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

To read a URL we use the [`requests.get()` method](https://requests.readthedocs.io/en/latest/api/#requests.get), which returns a [`requests.Response` object](https://requests.readthedocs.io/en/latest/api/#requests.Response). Let's try using it to read some JSON.

```python
import requests

response = requests.get("https://raw.githubusercontent.com/catalyst-cooperative/open-energy-data-for-all/refs/heads/main/data/eia923_2022.json")
```

The `Response` object has many useful methods and properties, which we can see with `help(response)`. We'll focus on the following:

* `response.status_code`, which tells you if the request succeeded or if it failed, and how it might have failed.
* `response.text`, which provides the returned data as a *text string*
* `response.json()` which parses the returned data as if it were JSON, and provide a Python list or dictionary.

First, let's look at the status code. These are HTTP status codes - numbers between 100 and 600 that indicate what happened.

You might have seen these before:
* when you've tried to access a webpage that doesn't exist (`404 Not Found`)
* when you've tried to access something you didn't have access to (`403 Forbidden`)
* when a website was down (`502 Bad Gateway`)

A number above 400 means something went wrong - 4xx means "the person making
the request messed up" and 5xx means "the person in charge of responding to the
request messed up."

Most of the time, the status code is `200 OK` for requests that succeeded, and that is indeed what we see.

```python
response.status_code
```

```output
200
```

Next, we'll look at `response.text`. You'll find that, in this case, that returns a very long string:

```python
len(response.text)
```

```output
1562319
```

And that the string looks like the JSON file you loaded in last episode:

```python
response.text[:100]
```

```output
'{"response":{"warnings":[{"warning":"incomplete return","description":"The API can only return 5000 '
```

Since this response appears to be JSON, as we expected, let's try using `response.json()` to parse it. Using what we just learned about this particular JSON's structure we can see the first few records from the data:

```python
eia923_2022_raw = response.json()
eia923_2022_raw["response"]["data"][:2]
```

```output
[{'period': '2022-12',
  'plantCode': '6761',
  'plantName': 'Rawhide',
  'fuel2002': 'ALL',
  'fuelTypeDescription': 'Total',
  'state': 'CO',
  'stateDescription': 'Colorado',
  'primeMover': 'ALL',
  'generation': '188961',
  'gross-generation': '203283',
  'generation-units': 'megawatthours',
  'gross-generation-units': 'megawatthours'},
 {'period': '2022-12',
  'plantCode': '54142',
  'plantName': 'Hillcrest Pump Station',
  'fuel2002': 'WAT',
  'fuelTypeDescription': 'Hydroelectric Conventional',
  'state': 'CO',
  'stateDescription': 'Colorado',
  'primeMover': 'HY',
  'generation': '342.43',
  'gross-generation': '358.27',
  'generation-units': 'megawatthours',
  'gross-generation-units': 'megawatthours'}]
```

:::::::: challenge

When might you want to use `.text` instead of `.json()`?

:::: solution
There are many situations! Here are a few:

* if the response is in XML or HTML instead of JSON
* if the JSON is consistently malformed in some way, and you need to modify it before parsing it as JSON
* if you don't actually need to parse the JSON and instead need to store it somewhere as text
::::

::::::::


## Introduction to APIs

The previous postdoc left a note that he had gotten the JSON files straight from the EIA API. While you might not have dealt with a web API before, you have the tools to do so now and resolve to jump in.


### Web APIs are just libraries of functions

A web API consists of a bunch of functionality which you access via *API requests*. A useful mental model for a *making a web API request* is that of *calling a function over the Internet*.

For example, imagine you have a function called `get_electric_power_operational_data` which takes a few different parameters. Maybe you call it like `get_electric_power_operational_data(data_field="generation", frequency="monthly")` and it will return a dataframe with some monthly generation data.

The web API version of that might look like making a request to `https://api.eia.gov/v2/electricity/electric-power-operational-data/data?data[]=generation&frequency=monthly`. 

These both correspond to the following English sentence:

> Get {a specific computer} to do something for me: get me electric power operational data. I only want generation data, and I want it at a monthly granularity.

Let's break down that correspondence.

| English | function call | API request |
|-----------|---------------|-------------|
| Get {a specific computer} to do something for me: | implicitly, your own computer | `https://api.eia.gov` |
| get me electric power operational data. | `get_electric_power_operational_data()` | `v2/electricity/electric-power-operational-data/data` |
| I only want generation data, | `data_field="generation"` | `data[]=generation` |
| and I want it at a monthly granularity. | `frequency="monthly"` | `frequency=monthly` |

In this case, we passed function arguments with a ["query string" or "URL parameters"](https://en.wikipedia.org/wiki/Query_string). This format specifies that everything after the `?` is an argument of some sort; the key and value are separated with `=` and the arguments are separated with `&`.


Since web APIs are basically a bundle of functions that you call on someone else's computer, learning them is much like learning a new library:

1. Figure out what functionality is available 
2. Figure out how to interact with it:
  * what inputs look like
  * what outputs look like
  * what happens when things go wrong?

The "how to interact with it" piece is a little bit more complicated for web APIs than regular libraries.

While the functions in all Python libraries are roughly called in the same way (`returned_value = function_name(param_1=value_1, param_2=value_2`), web APIs have a variety of ways to pass in parameters and return their data to you in different ways. They also return their error status to you differently. Additionally, most web APIs have some sort of authentication mechanism to control access. You wouldn't want other people running code on *your* computer willy-nilly, right?

We'll talk about these three, then dive into the EIA API to see if we can figure out the available functionality and how to interact with it.

### Inputs

### Outputs

### Authentication
* 


**TODO key points recap: look for what you can do, figure out how to interact with the thing, look at error messages**

## Case study: EIA API

**TODO maybe reorganize this a little based on the framework outlined above - start with "what are the functions & the inputs/outputs", learn that "oops, you need to hit the API to figure out how to hit the API," then go to auth/input/output, and finally go back and find some good functions and parse their output.**

**TODO we want to do this because we're interested in up-to-date generation & fuel consumption on a monthly basis.**

**TODO call out that this actually only has aggregated data across regions, not at the plant level!**


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

What call to that imaginary function would be equivalent to the API call we just tried out? Feel free to make up parameters for the function.

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

This API call will error out. Try running it - what's going wrong and how can you fix it?

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

If you try to make this request, the JSON response will give you information about the error:

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


## Generalizing to other APIs

Other APIs will be different from the EIA API - both in what functionality is available, and in how you access that functionality. Let's practice reading the documentation for another useful API, this time from the EPA.

[You can find the documentation here.](https://www.epa.gov/power-sector/cam-api-portal#/swagger/facilities-mgmt)

:::::::: challenge

Let's analyze this with the framework we introduced earlier.

* what is a function that seems useful to you?
* what are their inputs/outputs?
* how do you pass parameters?
* how do you parse the response?
* how do you authenticate?

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
