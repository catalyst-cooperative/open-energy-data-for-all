---
title: "Handling diverse filetypes in Pandas"
teaching: 0
exercises: 0
---

Expected duration: 45 min?

:::::::::::::::::::::::::::::::::::::: questions 

- How can I read in different tabular data types to a familiar format in Python?
- What are some common errors that occur when importing data, and how can I troubleshoot them?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Import tabular data from XML, JSON, and Parquet formats to pandas dataframes using the `pandas` library
- Import a table from a SQL database using the `pandas` library
- Implement strategies to handle common errors on data import

::::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints 

- `pandas` has functionality to read in many data formats (e.g., XML, JSON, SQL,
Parquet) into the same kind of DataFrame in Python. We can take advantage of this to
transform many kinds of data with similar functions in Python.
- `pandas` accepts both relative and absolute file paths on read-in.

::::::::::::::::::::::::::::::::::::::::::::::::

# `pd.read_xlsx()

TODO:
recap pd.read methods and imports
set the scene
describe the EIA data we're working with.
pd.read_excel() with no input
using help() to get the docs.

:::::::: challenge

## Challenge 1: handling gnarly 

Using `pd.read_excel()`, read in the first sheet ("Page 1 Energy Storage") using the `skiprows` parameter to select the column header row. 

:::: solution

```python
import pandas as pd

excel_923 = pd.read_excel('data/eia923_2022.xlsx', sheet_name=0, skiprows=)
```

::::

::::::::

# `pd.read_json()

TODO:
What is a json file and when might you see it
Try to use straight pd.read_json
When might you need to load a JSON first - nested JSONs.
Practice with the warnings table.
FLAG as decision - teach json_normalize() or no?
Drill down through the dictionary, this is basically what the param is doing under the hood.

:::::::: challenge

## Challenge 2: handling nested JSONs

Using `json.load()` and Pandas, read in the `data` from the `eia923_2022.json` file into a Pandas DataFrame.

:::: solution

```python
import pandas as pd
import json

# First, read in the file
import json
with open('data/eia923_2022.json') as file:
    eia923_json = json.load(file)

eia923_json = pd.json_normalize(eia923_json, record_path = ['response', 'data'])

# OR
eia923_json = pd.DataFrame(eia923_json['response']['data'])

```

::::

::::::::

TODO:
talk a bit about deeper nesting

# `pd.read_xml()

TODO:
What is an XML file and when might you see it
What's different from JSONs?

:::::::: challenge

## Challenge 3: unpacking XML files
### QUESTION - any way to make this more exciting?

Using `pd.read_xml()`, read in the `data` from the `eia923_2022.xml` file into a Pandas DataFrame.

:::: solution

```python
import pandas as pd

eia923_xml = pd.read_xml('data/eia923_2022.xml', xpath = '//response/data/row')

```
::::

::::::::

# `pd.read_parquet()

TODO:
What is a Parquet file and when might you see it
Just demo pd.read_parquet, no need for a challenge here.

`pd.read_parquet('data/eia923_2022.parquet)`

:::::::: challenge

Pick two datasets we've just read in, and compare them. How are they similar, and how are they different? Share your reflections with a peer.

:::: hint

* Inspect a column in a DataFrame `df` by using `df[column_name]`.
* To quickly see what values are contained in a column, you can use `df[column_name].unique()` to get a list of unique values in the column.
* Try using `df.iloc[0]` to get the values from the first row of the data.
* `df.head(n)` returns the first n rows of the data, and `df.tail(n)` returns the last n rows.
* to add - isin()??
::::

::::::::