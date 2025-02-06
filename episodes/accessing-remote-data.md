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

## Introduction to remote data

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

::::::::
::::

## Reading remote files into `pandas` directly

You asked around about the `eia923_2022.parquet` file and found out that it came from the [Public Utility Data Liberation project](https://catalyst.coop/pudl/). After a bit of online digging you find that they update their data nightly! You want to get your hands on more up-to-date data, so you want to check this out. Downloading a new file each day seems like a pain, though. You seem to remember that the documentation for `pandas.read_parquet()` mentions that the file path "could be a URL." Let's try it!

```python
import pandas as pd

df = pd.read_parquet("https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/core_eia923__monthly_generation_fuel.parquet")

print(df.report_date.value_counts().sort_index().tail(5))
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

Most, but not all, of the `read_*` functions support URLs - the exceptions are `read_spss`, `read_hdf`, and `read_clipboard`. Check the docs to make sure this will work!

::::

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

First, let's look at the status code. These are [HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) - numbers between 100 and 600 that indicate what happened.

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

And that the start of the string looks like the JSON file you loaded in last episode:

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

While the functions in all Python libraries are roughly called in the same way (`returned_value = function_name(param_1=value_1, param_2=value_2`), web APIs have a variety of ways to pass in parameters and return their data to you in different ways. They also return their error status to you differently. Additionally, most web APIs have an **authentication** mechanism to control access.

We'll talk about these three, then dive into the EIA API to see if we can figure out the available functionality and how to interact with it.

### Inputs and outputs

Above, we saw one common way of passing arguments to an API - a query string. This can be done with `requests.get`:

```python
import requests

requests.get("https://the-url-you-want", params={"key": "value"})
```

Another common method is to attach a JSON document to the web request. This is usually done using `requests.post`:

```python
import requests

requests.post("https://the-url-you-want", json={"key": "value"})
```

### Outputs

Each API will return data in a different format, though the vast majority will return data as either JSON or XML. As you saw in the last episode, JSON and XML data can take many different shapes, and you can reshape them in your code to suit your needs. However, you'll have to read each API's specific documentation to interpret the return data.

### Error messages

Often, when something goes wrong with your API request, you will receive some sort of indication about what went wrong. This information is usually part of the JSON response - sometimes it is paired with an status code within the JSON response as well.

The response will also have an HTTP status code, no matter what. Unfortunately, many APIs don't return the status code that corresponds to the actual error you've run into - so it's best to check the actual response contents.

### Authentication

Much of the time, you will need to authenticate to an API in order to use it. This is usually done by sending an **API key** with your request.

This key is usually sent either alongside the inputs (for example, as part of the query string) or as a **request header**.

Request headers are a separate metadata dictionary that get sent along with each request - you can send them with `requests` by passing a `headers={...}` argument to the `requests.get` function:

```python
requests.get("https://some-api.com/api/endpoint", headers={"Authentication": "some key"}) # also works with .post()!
```

:::: caution

API keys are secrets, just like passwords! Don't commit them to your Git repository, since that poses a risk that someone else will be able to use your credentials.

Instead, you should store them as environment variables, and read them in your code.

Here is how to set the environment variables in various operating systems - we'll use the EIA API key that you got in the setup instructions.

:::::::: tab

### Windows

Open a command prompt, then use the [`setx` command](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx):

```cmd
setx EIA_API_KEY some-secret-key-value
```

Then close the command prompt.

### Linux/Mac

This will depend a bit on your shell. The default shell for Mac OS is `zsh`; for Linux, and older Mac installations, you'll probably be using `bash` (run `echo $SHELL` to find out).

Open your `~/.zshrc` (or `~/.bashrc`, if you're running `bash` instead) and add the following to the end:

```zsh
export EIA_API_KEY="some-secret-key-value"
```
::::::::

Future Python scripts should be able to read the environment variable:


```python
import os

print(os.getenv("EIA_API_KEY"))
```
::::


:::: keypoints

* web APIs can be thought of like libraries that you call in a special way
* each web API is different, but there are common patterns to interacting with them
* when confronted with a new web API, think about the following questions:
  * what functions seem useful?
  * how do I send arguments to that functionality?
  * how do I turn the response data into something I can use?
  * how do errors get reported?
  * how do I authenticate?

::::

## Case study: EIA API

You know that you need generation, consumption, and carbon emissions data for your research - and that the EIA provides access to at least some of this data through an API. You decide to check it out!

You find the API documentation [here](https://www.eia.gov/opendata/documentation.php). 

### Finding functionality

Let's go through the framework outlined above. What functionality do they have, that you care about?

In many APIs, you will be able to find this information in the documentation. While reading the EIA API documentation, you find [a section of the documentation](https://www.eia.gov/opendata/documentation.php#Examiningametadatarequ) that indicates you need to make requests *to* the API to figure out what functionality is available:

> Discovering datasets should be much easier in APIv2 because the API now self-documents and organizes itself in a data hierarchy. Parent datasets have child datasets, which may have children of their own, and so on. To investigate what datasets are available, we request a parent node. The API will respond with the child datasets (routes) for the path we've requested. 

To make such a request, we'll have to figure out the authentication piece.

### Authentication

In the documentation you can see that they [expect you to pass the API key](https://www.eia.gov/opendata/documentation.php#UsinganAPIkey) as part of the query string, alongside the other parameters. Fortunately, you've set up the EIA API key as an environment variable already, so you should be able to just use it. `requests` provides a nice `params` dictionary we can use, which we will do below. 

### Finding functionality, part 2

We start with the simplest endpoint of the API:

```python
import os

import requests

EIA_API_KEY = os.getenv("EIA_API_KEY")

response = requests.get(
    f"https://api.eia.gov/v2/",
    params={
        "api_key": EIA_API_KEY,
    }
)
# print(response.json())
print(response.text)
```

Much like the JSON you saw last episode, it looks like the data is contained in the `"response"` key. There's a `"routes"` key within that which has the available endpoints and their descriptions:

:::: spoiler
```output
[
  {
    "id": "coal",
    "name": "Coal",
    "description": "EIA coal energy data"
  },
  {
    "id": "crude-oil-imports",
    "name": "Crude Oil Imports",
    "description": "Crude oil imports by country to destination, \r\n        includes type, grade, quantity.  Source: EIA-814  Interactive data \r\n        product:  www.eia.gov/petroleum/imports/companylevel/"
  },
  {
    "id": "electricity",
    "name": "Electricity",
    "description": "EIA electricity survey data"
  },
  {
    "id": "international",
    "name": "International",
    "description": "Country level production, consumption, imports, exports by energy source (petroleum, natural gas, electricity, renewable, etc.)  \r\n        Interactive product:  https://www.eia.gov/international/data/world"
  },
  {
    "id": "natural-gas",
    "name": "Natural Gas",
    "description": "EIA natural gas survey data"
  },
  {
    "id": "nuclear-outages",
    "name": "Nuclear Outages",
    "description": "EIA nuclear outages survey data"
  },
  {
    "id": "petroleum",
    "name": "Petroleum",
    "description": "EIA petroleum gas survey data"
  },
  {
    "id": "seds",
    "name": "State Energy Data System (SEDS)",
    "description": "Estimated production, consumption, price, and expenditure data for all energy sources by state and sector.  \r\n        Source:  https://www.eia.gov/state/seds/seds-technical-notes-complete.php  \r\n        Product:  SEDS (https://www.eia.gov/state/seds/)"
  },
  {
    "id": "steo",
    "name": "Short Term Energy Outlook",
    "description": "Monthly short term (18 month) projections using STEO model.  \r\n        Report and interactive projection data browser:  STEO (www.eia.gov/steo/)"
  },
  {
    "id": "densified-biomass",
    "name": "Densified Biomass",
    "description": "EIA densified biomass data"
  },
  {
    "id": "total-energy",
    "name": "Total Energy",
    "description": "These data represent the most recent comprehensive energy statistics integrated across all energy sources.  The data includes total energy production, consumption, stocks, and trade; energy prices; overviews of petroleum, natural gas, coal, electricity, nuclear energy, renewable energy, and carbon dioxide emissions; and data unit conversions values.  Source: https://www.eia.gov/totalenergy/data/monthly/pdf/mer_a_doc.pdf  Report:  MER (https://www.eia.gov/totalenergy/data/monthly/)"
  },
  {
    "id": "aeo",
    "name": "Annual Energy Outlook",
    "description": "Annual U.S. projections using National Energy Modelling System (NEMS) for release year.  Report, documentation, and interactive projection data browser:  AEO (www.eia.gov/aeo/)"
  },
  {
    "id": "ieo",
    "name": "International Energy Outlook",
    "description": "Annual international projections using the World Energy Projection System (WEPS) model for release year.  Report and interactive projection data browser:  IEO (www.eia.gov/ieo/)"
  },
  {
    "id": "co2-emissions",
    "name": "State CO2 Emissions",
    "description": "EIA CO2 Emissions data"
  }
]
```
::::

You can repeat this process, appending route IDs to the URL, until you map out the entire functionality of the API. We won't do all of that, but a more directed search will help us figure out what we can actually use this API for.

:::: challenge


Some of those endpoints above look relevant to your research - let's investigate them further.

1. Tweak the above code to list the endpoints under `https://api.eia.gov/v2/electricity`.
2. List out some sub-endpoints that seem relevant.
3. Keep going down the trail of "endpoints that seem relevant" until the metadata response doesn't have a `"routes"` key in it anymore, indicating that you've reached the end of that particular trail.
4. What is the endpoint that you are most interested in using? What data fields does it return? How can you filter the data?


:::::::: hint

* To find out what data fields an endpoint returns, check out the `data` key in the response.
* To find out how to filter the data, check out the `facets` key in the response.

::::::::

::::

### Inputs and outputs

Now that we know what we want to do, we need to figure out how to do it. For this example, we'll look at the `https://api.eia.gov/v2/electricity/electric-power-operational-data` endpoint, and try to access monthly net generation data for Colorado.

We can take a look at the [Parameters](https://www.eia.gov/opendata/documentation.php#Parameters) section of the documentation.

We see that we need to access a slightly different endpoint:

> To request data points from the API, we stipulate /data as the final node in our API call. 

So we should be accessing `https://api.eia.gov/v2/electricity/electric-power-operational-data/data`.

Let's take a look in the [Data[]](https://www.eia.gov/opendata/documentation.php#Data) section of the docs to see what we can find out about requesting specific data!

> To retrieve data points and their values from the API, we need to specify the specific columns we are interested in. In this document, we've been asking about electricity residential sales, but many data points about that subject matter are available. As of early 2022, our API has data values on revenue, sales, price, and number of customers.
>
> [...]
>
> Given these columns, let's ask for the price. Remember, in addition to specifying the column in the data[] parameter, we must also specify /data as the last node in the route:
> 
> `https://api.eia.gov/v2/electricity/retail-sales/data/?api_key=XXXXXX&data[]=price`

We'll want to adjust the endpoint and the parameter value, but we should be able to use that example URL to create our own request. For the purpose of illustration, we've added in the "length" parameter as well, which limits the number of returned rows:

```python
import os

import requests

EIA_API_KEY = os.getenv("EIA_API_KEY")

response = requests.get(
    f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data",
    params={
        "api_key": EIA_API_KEY,
        "data[]": "generation",
        "length": 2
    }
)
print(response.json()["response"])
```

```
{
  "warnings": [
    {
      "warning": "incomplete return",
      "description": "The API can only return 5000 rows in JSON format.  Please consider constraining your request with facet, start, or end, or using offset to paginate results."
    }
  ],
  "total": "4202279",
  "dateFormat": "YYYY-MM",
  "frequency": "monthly",
  "data": [
    {
      "period": "2019-06",
      "location": "HI",
      "stateDescription": "Hawaii",
      "sectorid": "3",
      "sectorDescription": "IPP CHP",
      "fueltypeid": "BIS",
      "fuelTypeDescription": "bituminous coal and synthetic coal",
      "generation": "0",
      "generation-units": "thousand megawatthours"
    },
    {
      "period": "2019-06",
      "location": "HI",
      "stateDescription": "Hawaii",
      "sectorid": "3",
      "sectorDescription": "IPP CHP",
      "fueltypeid": "BIT",
      "fuelTypeDescription": "bituminous coal",
      "generation": "0",
      "generation-units": "thousand megawatthours"
    }
  ],
  "description": "Monthly and annual electric power operations by state, sector, and energy source.\n    Source: Form EIA-923"
}
```

That's nice, but we need the Colorado data, not the Hawaii data.

Unintuitively, instructions for doing so lie within the [Frequency](https://www.eia.gov/opendata/documentation.php#Frequency) section of the documentation.

The skill we'd like to practice here is *reading the documentation*, so go read that section with the following challenge in mind:

:::: challenge

Which of the following query parameters will get us the data for generation in Colorado?

a. `.../data?api_key=XXXX&data[]=generation&stateid[]=CO`
c. `.../data?api_key=XXXX&data[]=generation&facets[stateid][]=CO`
b. `.../data?api_key=XXXX&data[]=generation&facets[location][]=CO`
d. `.../data?api_key=XXXX&data[]=generation&facets[location][]=Colorado`

:::::::: hint

To see what facet types are available, look at the metadata for this endpoint by querying the endpoint without `/data`.

::::::::

:::::::: hint

You may need to get the available facet values - see [Facets and their available values](https://www.eia.gov/opendata/documentation.php#Facetsandtheiravailabl).

::::::::

:::::::: solution

The example in the docs says:

> To do so, we'll add the facet[stateid] and set it to CO. Remember to ask for a column return, in this case, price:
>
> https://api.eia.gov/v2/electricity/retail-sales/data?api_key=xxxxxx&data[]=price&facets[sectorid][]=RES&facets[stateid][]=CO

But the metadata for *this* endpoint indicates that `stateid` is *not* an available type - instead it requires `location`.

b. `.../data?api_key=XXXX&data[]=generation&facets[location][]=CO`

::::::::

::::


### Errors

Sometimes, despite all of our best intentions, we run into issues dealing with the API. In many cases, they'll send back some useful error message.

For example, let's try to modify our previous code to get yearly data.

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
        "length": 2
    }
)
print(response.json())
```

Oops! We got an error response:

```output
{'error': "Invalid frequency 'yearly' provided. The only valid frequencies are 'monthly', 'quarterly', and 'annual'.", 'code': 400}
```

It tells us what the problem is - we need to use the value `annual` instead of `yearly`.

It also tells us a "code" for the error - this expresses the general category of error and is based on the HTTP status codes. The overachieving reader may note that `response.status_code` actually returns `500`, which disagrees with the code above. A grim reminder that web APIs play fast and loose with HTTP status codes and should not be trusted.

:::::::: challenge

You're trying to get the BTUs of fuel consumption for electricity generation, so you try this API call. However, it fails.

Try running it - what's going wrong and how can you fix it?

```python
response = requests.get(
    url="https://api.eia.gov/v2/electricity/electric-power-operational-data/data/",
    params={
        "api_key": EIA_API_KEY,
        "frequency": "annual",
        "data[]": "consumption",
        "length": 2
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

Which one we should change it to depends on what you want - go back to the metadata for this endpoint to identify which of these you mean!

We see:

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

So it looks like we want `consumption-for-eg-btu` here.

::::

::::::::


## Generalizing to other APIs

Other APIs will be different from the EIA API - both in what functionality is available, and in how you access that functionality. Let's practice reading the documentation for another useful API, this time from the EPA. It's focused on different facilities and their attributes such as the different fuel types, environmental equipment, etc. at each facility.

[You can find the documentation here.](https://www.epa.gov/power-sector/cam-api-portal#/swagger/facilities-mgmt)

Let's analyze this with the framework we introduced earlier.


Let's start with "is this interesting or useful at all?":

:::: challenge

Which endpoint seems most interesting to you?

::::

The documentation is pretty sparse, so we'll probably need to play around with the API to actually understand it. That means we need to figure out authentication.

:::: challenge

What would you add to your `requests.get()` call to authenticate?

:::::::: hint

Click on the green Authorize button!

::::::::


:::::::: solution

You'll need to add an `x-api-key` header to your `requests.get()`:

```python

response = requests.get(..., headers={"x-api-key": "THE_API_KEY"})
```

::::::::

::::

For the purposes of this exploration, you can use the built-in "try it out" buttons on the website - make sure you click that "authorize" button and paste your API key first.

:::: challenge

Choose one interesting endpoint. What are the inputs/outputs?

:::::::: hint

The inputs are listed as parameters once you expand each endpoint.

The outputs are a little harder to find. There are some output types listed at the bottom of the page (the "DTO"s), but you'll have to actually try out the API to figure out which output types go with which endpoints.

::::::::

::::

:::: challenge
How do you pass parameters to your interesting endpoint?

:::::::: solution

Most endpoints take parameters as query parameters, just like the EIA API.

One of these endpoints take parameters as part of their path (`/facilities-mgmt/facilities/{id}`).
::::::::

::::

:::: challenge
What format are the responses in?

:::::::: solution

The responses are in JSON - and they seem to correlate with the grey DTO definitions at the bottom of the page!

::::::::

::::

:::: challenge

What happens when things go wrong?

:::::::: hint

Try inputting parameters that are obviously wrong, like a negative year number.

::::::::

:::::::: solution

We get a bunch of error information back in the JSON response, similar to the EIA API.

::::::::

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
