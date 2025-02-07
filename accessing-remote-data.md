---
title: Accessing remote data
teaching: 0
exercises: 0
---

**TODO** rework these to be more motivating.

:::::::: questions

* How can I work with the most up-to-date data available?
* How can I work with data that is behind a web API?

::::::::

:::::::: objectives

* Read remote files into `pandas` dataframes
* Investigate the inputs to and outputs from an API

::::::::

## Introduction to remote data

**TODO** why would you want to use remote data?

Remote data is data that's not stored on your computer's hard drive - instead it's stored somewhere else and you access it through a network. This still downloads the data over the network, but doesn't store it on your hard drive.

:::: discussion

What are some advantages and disadvantages you can imagine for using remote data vs. saving the data to your hard drive (aka **local data**)?

:::::::: solution

Some non-exhaustive ideas:

Remote data pros:
* if someone else updates the data, you always have the most recent version
* you don't need to manage multiple versions of the same data on your hard drive
* if you send your code to someone else, you don't also have to package the data with it

Local data pros:
* you can keep track of different versions of the same data, even if the publisher doesn't
* you only need to download the data once, and then you can read from your disk in the future, which is faster
* if someone else updates the data, your data doesn't change until you actively download a new version
* what about no internet
::::::::
::::

## Reading remote files into `pandas` directly

You asked around about the `eia923_2022.parquet` file and found out that it came from the [Public Utility Data Liberation project](https://catalyst.coop/pudl/). After a bit of online digging you find that they update their data regularly! You want to get your hands on more up-to-date data, so you want to check this out. Continuously checking to see if there's new data is annoying, though, so you want to try to get the updated data automatically. You seem to remember that the documentation for `pandas.read_parquet()` mentions that the file path "could be a URL." Let's try it!

**TODO** explain that /nightly is a pointer to the freshest version of the data

```python
import pandas as pd

df = pd.read_parquet("https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/core_eia923__monthly_generation_fuel.parquet")

print(df.report_date.max())
```

```output
report_date
2024-04-01    5362
2024-05-01    5395
2024-06-01    5426
2024-07-01    5435
2024-08-01    5450
Name: count, dtype: int64
```

Indeed, `read_parquet()` does handle URLs without a hiccup! You can see that there are updated rows for data through 2024.

:::: callout

Most, but not all, of the `read_*` functions support URLs -  check the docs to make sure this will work!

::::

:::::::: challenge

Adapt your previous Excel-reading code to read the same Excel file directly from the Internet. You should be able to find the file here: `https://github.com/catalyst-cooperative/open-energy-data-for-all/raw/refs/heads/main/data/eia923_2022.xlsx`

```python
import pandas as pd

pd.read_excel("data/eia923_2022.xlsx", skiprows=5)
```

:::: solution

```python
import pandas as pd

pd.read_excel("https://github.com/catalyst-cooperative/open-energy-data-for-all/raw/refs/heads/main/data/eia923_2022.xlsx", skiprows=5)
```
::::

::::::::

:::::::: callout
If the person maintaining the remote data updates the data without changing the URL, you will get the new version. This can be very useful when exploring data!

This can also be very annoying when you want your analysis to remain stable! In that case, you can try to find data that's hosted on a services like [Zenodo](https://zenodo.org/) which is designed to provide stable URLs. Many data providers also provide distinct URLs for each specific data version as well as a pointer to the latest data version. Of course, archiving the data yourself and managing the data versions can also work.
::::::::

## Using `requests` to download files

It's nice to use functions in the `pd.read_*()` family with a URL, but sometimes you need to do a little bit of reshaping of the data before you can actually use `pd.read_*()`. We saw this with the JSON file earlier. In those cases, you can stil tell your code to download the file instead of having to download it yourself.

While Python has some code in the standard library to help you read data from a URL, the [`requests` library](https://requests.readthedocs.io/en/latest/user/quickstart/) is easier to use and also extremely popular, so we'll focus on using that.

To read a URL we use the [`requests.get()` method](https://requests.readthedocs.io/en/latest/api/#requests.get), which returns a [`requests.Response` object](https://requests.readthedocs.io/en/latest/api/#requests.Response). Let's try using it to read some JSON - the same file we read in the last episode, but without having to save it to disk first!

```python
import requests

response = requests.get("https://raw.githubusercontent.com/catalyst-cooperative/open-energy-data-for-all/refs/heads/main/data/eia923_2022.json")
```

The `Response` object has many useful methods and properties. We'll focus on `response.json()`, which turns JSON data into a Python object we can interact with.


```python
eia923_2022_raw = response.json()
eia923_2022_raw["response"]["data"][:2]
```

This seems to follow the format we saw last time.

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

Adapt the JSON reading code from last episode to use requests.get.

```python
import pandas as pd
import json

with open('data/eia923_2022.json') as file:
    eia923_json = json.load(file)

eia923_json_df = pd.json_normalize(eia923_json, record_path = ['response', 'data'])
```

:::: solution
import pandas as pd
import json
import requests

response = requests.get("https://raw.githubusercontent.com/catalyst-cooperative/open-energy-data-for-all/refs/heads/main/data/eia923_2022.json")
eia923_json = response.json()

eia923_json_df = pd.json_normalize(eia923_json, record_path = ['response', 'data'])
::::

::::::::

## Web APIs: Fancy URLs

**TODO** change from quarterly to yearly, so the electric power operations route to use is clearer.

Suppose someone asks you, "how much natural gas was consumed for electricity generation, totalled across all sectors, in Colorado, for each quarter of 2023?"

You *could* go find the EIA 923 data for 2023, do a bunch of filtering and reshaping of the data, and get an answer.

But, in this case, the EIA has another way - their web API. Web APIs are collections of fancy URLs that allow them to be much more flexible than merely downloading individual files. They can save you a lot of work, if you become good at using them.

For example, to answer that question, you can request this URL:


```python
import requests

response = requests.get("https://api.eia.gov/v2/electricity/electric-power-operational-data/data?data[]=consumption-for-eg&facets[fueltypeid][]=NG&facets[sectorid][]=99&facets[location][]=CO&frequency=quarterly&start=2023-Q1&end=2023-Q4&api_key=3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8")
```

Which gives you the amount of natural gas consumed for electricity generation in Colorado, across all sectors, in each quarter of 2023!

```output
{
  "response": {
    "total": "4",
    "dateFormat": "YYYY-\"Q\"Q",
    "frequency": "quarterly",
    "data": [
      {
        "period": "2023-Q3",
        "location": "CO",
        "stateDescription": "Colorado",
        "sectorid": "99",
        "sectorDescription": "All Sectors",
        "fueltypeid": "NG",
        "fuelTypeDescription": "natural gas",
        "consumption-for-eg": "38922.149",
        "consumption-for-eg-units": "thousand Mcf"
      },
      {
        "period": "2023-Q4",
        "location": "CO",
        "stateDescription": "Colorado",
        "sectorid": "99",
        "sectorDescription": "All Sectors",
        "fueltypeid": "NG",
        "fuelTypeDescription": "natural gas",
        "consumption-for-eg": "30960.083",
        "consumption-for-eg-units": "thousand Mcf"
      },
      {
        "period": "2023-Q1",
        "location": "CO",
        "stateDescription": "Colorado",
        "sectorid": "99",
        "sectorDescription": "All Sectors",
        "fueltypeid": "NG",
        "fuelTypeDescription": "natural gas",
        "consumption-for-eg": "37001.407",
        "consumption-for-eg-units": "thousand Mcf"
      },
      {
        "period": "2023-Q2",
        "location": "CO",
        "stateDescription": "Colorado",
        "sectorid": "99",
        "sectorDescription": "All Sectors",
        "fueltypeid": "NG",
        "fuelTypeDescription": "natural gas",
        "consumption-for-eg": "27915.336",
        "consumption-for-eg-units": "thousand Mcf"
      }
    ],
    "description": "Monthly and annual electric power operations by state, sector, and energy source.\n    Source: Form EIA-923"
  },
  "request": {
    "command": "/v2/electricity/electric-power-operational-data/data/",
    "params": {
      "data": [
        "generation",
        "consumption-for-eg"
      ],
      "frequency": "quarterly",
      "facets": {
        "fueltypeid": [
          "NG"
        ],
        "location": [
          "CO"
        ],
        "sectorid": [
          "99"
        ]
      },
      "start": "2023-Q1",
      "end": "2023-Q4",
      "api_key": "3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8"
    }
  },
  "apiVersion": "2.1.8",
  "ExcelAddInVersion": "2.1.0"
}
```

While that URL can seem impossibly complicated at first, we can break it down into a few parts:

* `https://api.eia.gov/` is the **host** - this means we're asking the **EIA API** for something, as opposed to another website.
* `/v2/electricity/electric-power-operational-data/data?`: the **route** - this tells the API what you're looking for. In this case, "electric power operational data."
* The rest of the URL is a bunch of `name=value` pairs split by `&`s - we'll ignore the `&`'s for clarity. These are called **parameters**.
  * `data[]=consumption-for-eg`: "I only want the consumption for electricity generation"
  * `facets[fueltypeid][]=NG`: "with the fuel type ID NG for natural gas"
  * `facets[sectorid][]=99`: "for sector ID 99, which means 'all sectors'"
  * `facets[location][]=CO`: "within the location CO for colorado"
  * `frequency=quarterly`: "at a quarterly frequency"
  * `start=2023-Q1`: "starting in 2023-Q1"
  * `end=2023-Q4`: "ending in 2023-Q4"
  * `api_key=3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8`: a password to prove you have access to the API. 
  
  
:::: callout
The API key we're using in this lesson is a public one that EIA provides, but it would be polite to request your own API key by clicking the register button on the [EIA open data portal](https://www.eia.gov/opendata/) if you plan on using the API a lot.

Many other APIs will not have a public key, so you'll have to register in one way or another to get one.
::::

Every web API behaves differently, but you only need to be able to do two things to figure any API out:

* read their documentation
* make requests to the API & interpret responses

You can read, and you can use `requests` to make requests. We'll walk through building a similarly complicated query as we just saw, by applying those two skills.

:::: challenge

Make a request to that URL with `requests.get`.

Try removing the `end=2023-Q4` parameter from the URL. What happens?

:::::::: solution

You get data all the way until the present day!

::::::::

::::


:::: keypoints

* web APIs can be thought of as bundles of fancy URLs
* each web API is different, but if you can read the documentation and make requests to URLs, you can figure them out

::::

## Case study: EIA API



Let's get started! You can find the API documentation [here](https://www.eia.gov/opendata/documentation.php). 

Let's focus on a slightly different question than we had before - now that we know the aggregated information, we want to drill down.

**"What was the yearly natural gas consumption, plant-by-plant, in Colorado from 2020-2024?"**

Our first goal is to figure out how to start interacting with the API, and how to map any examples in the documentation to real Python code.

When scrolling through the documentation, we notice a bunch of example URLs. Let's pick a fairly simple one to get started: `https://api.eia.gov/v2/electricity&api_key=xxxxxx`

```python
import requests

api_key = "3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8"

response = requests.get(f"https://api.eia.gov/v2/electricity?api_key={api_key}")
response.json()
```

```output
{'response': {'id': 'electricity',
  'name': 'Electricity',
  'description': 'EIA electricity survey data',
  'routes': [{'id': 'retail-sales',
    'name': 'Electricity Sales to Ultimate Customers',
    'description': 'Electricity sales to ultimate customer by state and sector (number of customers, average price, revenue, and megawatthours of sales).  \n    Sources: Forms EIA-826, EIA-861, EIA-861M'},
   {'id': 'electric-power-operational-data',
    'name': 'Electric Power Operations (Annual and Monthly)',
    'description': 'Monthly and annual electric power operations by state, sector, and energy source.\n    Source: Form EIA-923'},
   {'id': 'rto',
    'name': 'Electric Power Operations (Daily and Hourly)',
    'description': 'Hourly and daily electric power operations by balancing authority.  \n    Source: Form EIA-930'},
   {'id': 'state-electricity-profiles',
    'name': 'State Specific Data',
    'description': 'State Specific Data'},
   {'id': 'operating-generator-capacity',
    'name': 'Inventory of Operable Generators',
    'description': 'Inventory of operable generators in the U.S.\n    Source: Forms EIA-860, EIA-860M'},
   {'id': 'facility-fuel',
    'name': 'Electric Power Operations for Individual Power Plants (Annual and Monthly)',
    'description': 'Annual and monthly electric power operations for individual power plants, by energy source and prime mover\n    Source: Form EIA-923'}]},
 'request': {'command': '/v2/electricity/',
  'params': {'api_key': '3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8'}},
 'apiVersion': '2.1.8',
 'ExcelAddInVersion': '2.1.0'}
```

It looks like there's no actual data here... Going back to the docs, we see:

> Discovering datasets should be much easier in APIv2 because the API now self-documents and organizes itself in a data hierarchy. Parent datasets have child datasets, which may have children of their own, and so on. To investigate what datasets are available, we request a parent node. The API will respond with the child datasets (routes) for the path we've requested.

So it seems like there are a variety of different child routes we could request.

:::: challenge

If we're looking for yearly data about fuel consumption at the plant level, what route should we request next?

:::::::: Solution

`facility-fuel`!

::::::::

::::

OK, so let's drill down into one of those child routes.


```python
import requests

api_key = "3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8"

response = requests.get(f"https://api.eia.gov/v2/electricity/facility-fuel?api_key={api_key}")
resp_json = response.json()
```

```output
{'response': {'id': 'facility-fuel',
  'name': 'Electric Power Operations for Individual Power Plants (Annual and Monthly)',
  'description': 'Annual and monthly electric power operations for individual power plants, by energy source and prime mover\n    Source: Form EIA-923',
  'frequency': [{'id': 'monthly',
    'description': 'One data point for each month.',
    'query': 'M',
    'format': 'YYYY-MM'},
   {'id': 'quarterly',
    'description': 'One data point every 3 months.',
    'query': 'Q',
    'format': 'YYYY-"Q"Q'},
   {'id': 'annual',
    'description': 'One data point for each calendar year.',
    'query': 'A',
    'format': 'YYYY'}],
  'facets': [{'id': 'plantCode', 'description': 'Plant ID and Name'},
   {'id': 'fuel2002', 'description': 'Energy Source'},
   {'id': 'state', 'description': 'State'},
   {'id': 'primeMover', 'description': 'Prime Mover'}],
  'data': {'generation': {'alias': 'Net Generation', 'units': 'megawatthours'},
   'gross-generation': {'alias': 'Gross Generation', 'units': 'megawatthours'},
   'total-consumption': {'alias': 'Consumption of Fuels for Electricity Generation and Useful Thermal Output (Physical Units)'},
   'total-consumption-btu': {'alias': 'Consumption of Fuels for Electricity Generation and Useful Thermal Output (BTUs)',
    'units': 'MMBtu'},
   'consumption-for-eg': {'alias': 'Consumption of Fuels for Electricity Generation (Physical Units)'},
   'consumption-for-eg-btu': {'alias': 'Consumption of Fuels for Electricity Generation (BTUs)',
    'units': 'MMBtu'},
   'average-heat-content': {'alias': 'Average Heat Content of Consumed Fuels'}},
  'startPeriod': '2001-01',
  'endPeriod': '2024-11',
  'defaultDateFormat': 'YYYY-MM',
  'defaultFrequency': 'monthly'},
 'request': {'command': '/v2/electricity/facility-fuel/',
  'params': {'api_key': '3zjKYxV86AqtJWSRoAECir1wQFscVu6lxXnRVKG8'}},
 'apiVersion': '2.1.8',
 'ExcelAddInVersion': '2.1.0'}
```

Still no data! But it seems like we're getting closer - there's a `data` field in the response, and also some `frequency` and `facets` information that looks relevant.

**todo** back to the docs! what do these things do? let's start with `data`, then `frequency`, then `facets`. then we heed the warning and set start/end and we're done!

:::: challenge

What 

::::

:::::::: keypoints

* Many functions in the `pandas.read_*` family can read tabular data from remote servers & cloud storage as if it was on your local computer
* `requests` can get data that's not in the right shape for `pandas.read_*`; you'll have to do the translation from their response format into `pandas.DataFrame` yourself
* when confronted with a new web API, think about the following questions:
  * what functions seem useful?
  * how do I send arguments to that functionality?
  * how do I turn the response data into something I can use?
  * what happens when something goes wrong?
  * how do I authenticate?

::::::::
