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
- Import tabular data from Excel, XML, JSON, and Parquet formats to pandas dataframes using the `pandas` library
- Use `pandas` documentation to select and implement parameters - refine this.

::::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints 

- `pandas` has functionality to read in many data formats (e.g., XML, JSON,
Parquet) into the same kind of DataFrame in Python. We can take advantage of this to
transform many kinds of data with similar functions in Python.
- `pandas` accepts both relative and absolute file paths on read-in.

::::::::::::::::::::::::::::::::::::::::::::::::

# Untangling a data pile
While poking around in your lab's computer, you find the folder that the postdoc was
using to store data inputs to his model. Inside the `data` folder, however, is a bit of
a mess! Every file in the folder has the same name ("eia923_2022") but a different file
extension. To make sense of this undocumented pile of files, we'll need to read in each
file and compare them. 

# EIA 923 data
The Energy Information Administration (EIA)'s [Form 923](https://www.eia.gov/electricity/data/eia923) collects detailed monthly and
annual electric power data on electricity generation, fuel consumption, fossil fuel
stocks, and receipts at the power plant and prime mover level.
    TODO: Why is it a good choice for answering the question?

# `pd.read_excel()`

One of the most popular libraries used to work with tabular data in Python is called the
[Python Data Analysis Library](https://pandas.pydata.org/) (or simply, Pandas). Pandas
has functions to handle reading in a diversity of file types, from CSVs and Excel spreadsheets to more complex data formats such as XML and Parquet. Each read function offers a variety of parameters designed to handle common complexities specific to the file type on import. For a refresher (TODO: Is this an ok wording?) on Pandas, Pandas DataFrames and reading in files, see the [Starting with Data](https://datacarpentry.github.io/python-ecology-lesson/instructor/02-starting-with-data.html) lesson.

Of all the files in the `data` folder, you decide to start with the Excel spreadsheet.
To read in an Excel spreadsheet using `pandas`, you will use the `read_excel()` function:

```python
import pandas as pd
pd.read_excel('data/eia923_2022.xlsx')
```

Unfortunately, something doesn't look quite right! When opening the file in a
spreadsheet software, you see that the first few rows look like this:

![The first few rows of the eia923_2022.xlsx file](fig/excelheader.png){alt="Snapshot of
the Excel file showing the first 6 rows contain metadata, blank spaces and column
names".}

To read the spreadsheet in correctly, we want to ignore these first five rows. Luckily,
`read_excel()` offers built-in functionality to handle various Excel formatting
challenges. To identify which parameter we need to use to skip these rows when reading
in the file, we can use the `help()` function to pull up the function documentation:

```python
help(pd.read_excel)
```

For each parameter, the documentation provides the name of the parameter, the format for the parameter input (e.g., list, string, int), the default value if no value is provided, and an explanation of what the parameter does.

For example, the `nrows` parameter provides the following documentation:

```output
nrows : int, default None
    Number of rows to parse.
```

So, if we only want to parse the first 100 rows of the data, we can call:

```python
pd.read_excel('data/eia923_2022.xlsx', nrows=100)
```

:::::::: challenge

## Challenge 1: handling gnarly 

Using `pd.read_excel()`, read in the first sheet ("Page 1 Generation and Fuel Data") using the `skiprows` parameter to skip any rows that don't contain the column headers.

:::: solution

```python
import pandas as pd

excel_923 = pd.read_excel('data/eia923_2022.xlsx', sheet_name="Page 1 Generation and Fuel Data", skiprows=5)
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

TODO: Migrate to fill in the blanks


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
talk a bit about deeper nesting - what did I mean by this haha.

# `pd.read_xml()

TODO:
What is an XML file and when might you see it
    - it's old.
    - what are some examples of xml in the wild - e.g., xbrl, html
What's different from JSONs?
Explain xpath + demo one level

:::::::: challenge

## Challenge 3: unpacking XML files
### QUESTION - any way to make this more exciting?

Using `pd.read_xml()`, read in the `data` from the `eia923_2022.xml` file into a Pandas DataFrame using the `xpath` parameter.

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
* to add - isin()?? info()
::::

::::::::