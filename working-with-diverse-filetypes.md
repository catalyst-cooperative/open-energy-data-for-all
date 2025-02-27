---
title: "Handling diverse filetypes in Pandas"
teaching: 0
exercises: 0
---

Expected duration: 45 min?

:::: questions

- How can I read in different tabular data types to a familiar format in Python?
- What are some common errors that occur when importing data, and how can I troubleshoot them?

::::

:::: objectives
- Import tabular data from Excel, JSON, XML and Parquet formats to pandas dataframes using the `pandas` library
- Use `help` and function documentation to select and implement parameters in function calls.

::::

## Untangling a data pile
While poking around in your lab's computer, you find the folder that the postdoc was
using to store data inputs to his model. Inside the `data` folder, however, is a bit of
a mess! Every file in the folder has the same name ("eia923_2022") but a different file
extension. To make sense of this undocumented pile of files, we'll need to read in each
file and compare them.

## EIA 923 data
The Energy Information Administration (EIA)'s [Form 923](https://www.eia.gov/electricity/data/eia923) is known as the Power Plant Operations Report. The data include electric power generation, energy source consumption, end of reporting period fossil fuel stocks, as well as the quality and cost of fossil fuel receipts at the power plant and prime mover level (with a subset of +10MW steam-electric plants reporting at the boiler and generator level). Information is available for non-utility plants starting in 1970 and utility plants beginning in 1999. The Form EIA-923 has evolved over the years, beginning as an environmental add-on in 2007 and ultimately eclipsing the information previously recorded in EIA-906, EIA-920, FERC 423, and EIA-423 by 2008.

Given your interest in generation and fuel consumption data for your research, the EIA
Form 923 data is a great starting point for data exploration.

## Reading Excel files with Pandas

One of the most popular libraries used to work with tabular data in Python is called the
[Python Data Analysis Library](https://pandas.pydata.org/) (or simply, Pandas). Pandas
has functions to handle reading in a diversity of file types, from CSVs and Excel spreadsheets to more complex data formats such as XML and Parquet. Each read function offers a variety of parameters designed to handle common complexities specific to the file type on import. For a refresher on Pandas, Pandas DataFrames and reading in files, see the [Starting with Data](https://datacarpentry.github.io/python-ecology-lesson/instructor/02-starting-with-data.html) lesson.

::: callout
### Identifying file paths

In order to read data into Pandas or any Python function, we'll need to identify the
*path* to that file. The path tells the code where that file lives. There are two ways
to specify the path to any file on your computer:

- __Relative path__: A relative path specifies a location starting from the current location.
- __Absolute path__: An absolute path specifies a location from the root of the filesystem.

For example, to get to the `eia923_2022.json` file in the `data` folder from a notebook
in the `open-energy-data-for-all` folder, we can either specify:

- __Relative path__: `data/eia923_2022.json`
- __Absolute path__: `/home/user/Desktop/path/to/open-energy-data-for-all/folder/data/eia923_2022.json`
:::

### Handling spreadsheet formatting on read-in

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
names."}

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

### Challenge 1: handling Excel formatting on read-in

Looking at the documentation for `pd.read_excel()`, identify the parameter needed to skip the first few rows of the spreadsheet. Then, using `pd.read_excel()`, read in the "Page 1 Generation and Fuel Data" sheet using this parameter to skip any rows that don't contain the column headers.

:::: solution

```python
import pandas as pd

excel_923 = pd.read_excel('data/eia923_2022.xlsx', sheet_name="Page 1 Generation and Fuel Data", skiprows=5)

# sheet_name can also take the number of the sheet
excel_923 = pd.read_excel('data/eia923_2022.xlsx', sheet_name=0, skiprows=5)
```

::::

::::::::

Each row contains monthly generation data for each plant's prime mover. While a subset of plants fill out Form 923 at the boiler and generator, a large proportion of plants only report at this more aggregated level. For more on the nuances of the Form 923 data, see PUDL's [data source page](https://catalystcoop-pudl.readthedocs.io/en/latest/data_sources/eia923.html).

## Reading in JSON files

JavaScript Object Notation (JSON) is a lightweight file format based on name-value pairs, similar to Python dictionaries. JSON often used to send data to and from web applications, and is one of the most common formats provided when you're accessing data from an Application Programming Interface (API). JSON data can be found saved as either `.json` or `.txt` files.

### Nested formats in JSON files

Pandas `read_*()` methods transform data into a tabular format.  When a JSON file is already formatted as a table, we can use `pd.read_json()` to read it in directly. Most often, we know a JSON file contains a table when we see a list of dictionaries, or a dictionary of lists.

However, JSON files are very rarely formatted to _only_ contain a table. Instead, most JSONs contain data in a *nested* format. To successfully extract tabular generation data from a nested JSON, we need to identify which part of the nested JSON contains the tabular data we're looking for.

A nested JSON contains multiple levels of data:

```output
{'response':
    {'data': [
        {'period':'2022-12',
        'plantCode': '6761'},
        {'period':'2022-12',
        'plantCode': '54152'}
        ]
    }}
```

Here, the `response` contains another name-value pair called `data`, and `data`
contains a list with two records, each of which has two name-value pairs (`period` and `plantCode`).

The `data` contained in this JSON file can be represented as a table! In this data format,
each dictionary corresponds to one row of the data, and each name (e.g., "period") corresponds
to a column name. JSON files typically represent this data format using lists of dictionaries, as above.

### Reading in JSON files using `json.load()`

To better visualize our JSON file, let's read it into Python without changing its format. To do this, we use the `json` package, and the `load` method.

While Pandas handles opening a file in the `read_*()` methods, `json.load()` does not - so, we first need to open the file in Python. To do so, we use the `open()` function to read in the `eia923_2022.json` file.

:::callout
When we `open()` a file in Python, we should always close it after we've extracted the data we need. Closing a file frees up system resources and ensures that we aren't accidentally modifying our original file.

To automatically handle file opening and closing, we use a *context manager*. Using the word `with`, we put all the code we want to run on the opened file into an indented block.
:::

```python
import json
with open('data/eia923_2022.json') as file:
    eia923_json = json.load(file)

eia923_json
```
The first part of the response looks like this:

```output
{'response': {'warnings': [{'warning': 'incomplete return',
    'description': 'The API can only return 5000 rows in JSON format.  Please consider constraining your request with facet, start, or end, or using offset to paginate results.'}],
  'total': '10426',
  'dateFormat': 'YYYY-MM',
  'frequency': 'monthly',
  'data': [{'period': '2022-12',
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
    .....
```
Now we can treat `eia923_json` like any other Python dictionary. We can use `.keys()`
to see a list of all the keys in the first level of the dictionary - this is a quick and
helpful way to get a sense for what is contained in different parts of the JSON file, without having to scroll through the entire output.

To see the value of any particular key, we can call it in square brackets by name:

```python
eia923_json['response']
```

This returns yet another dictionary with a list of keys. To look more closely at the `warnings` the file contains, we can add another square bracket:

```python
eia923_json['response']['warnings']
```

```output
[{"warning":"incomplete return","description":"The API can only return 5000 rows in JSON format.  Please consider constraining your request with facet, start, or end, or using offset to paginate results."}, {"warning":"another warning", "description":"Hey! Watch out!"}]
```

:::::::: challenge

### Challenge 2: find that table!

Load the `eia923_2022.json` file using `json.load()`, and find the data table containing net generation data by iterating through the dictionary keys.

:::: solution

```python
import pandas as pd
import json

import json
with open('data/eia923_2022.json') as file:
    eia923_json = json.load(file)

eia923_json['response']['data']

```

::::

::::::::

### Using `json.normalize()`

Now that we've found the path to our data table in the JSON file, we still need to transform the data into a Pandas DataFrame. Luckily for us, Pandas has a function to transform nested or semi-structured JSON files into Pandas DataFrames: `json_normalize()`.

Unlike `read_json()`, `json_normalize()` expects that the JSON object has already been read into Python using `json.load()`. Once we've loaded the JSON file, we can use the `record_path`
parameter to specify the path to follow to get to our tabular data - for the warnings data, first `response` and then `warnings`:

```python
pd.read_json(eia923_json, record_path = ['response','warnings'])
```
The function returns a DataFrame that looks like this:

```output
|           warning |                                       description |
|------------------:|--------------------------------------------------:|
| incomplete return | The API can only return 5000 rows in JSON form... |
|   another warning |                                   Hey! Watch out! |
```

The first row of this table is letting us know that when the postdoc queried and saved this data from the API, he only got the first 5,000 rows of data. We'll tackle this problem in a later episode, but for now let's investigate the data that we do have saved locally.

:::::::: challenge

### Challenge 3: handling nested JSONs

Fill in the blanks in the code below to read in the `data` from the `eia923_2022.json` file into a Pandas DataFrame.

```python
import pandas as pd
import json

import json
with open('data/eia923_2022.json') as file:
    eia923_json = ...

eia923_json_df = pd.json_normalize(eia923_json, record_path = [...])

```

:::: solution

```python
import pandas as pd
import json

import json
with open('data/eia923_2022.json') as file:
    eia923_json = json.load(file)

eia923_json_df = pd.json_normalize(eia923_json, record_path = ['response', 'data'])

```

::::

::::::::

:::callout
JSONs can include many levels of nesting, including different levels of nesting for similar records or other formatting that doesn't obey the principles of tabular structure (where each row represents a single record, and each column represents a single variable). `pd.json_normalize()` provides a set of parameters that can used to wrangle more deeply nested JSON data. Call `help(pd.json_normalize)` and look at the provided examples to get a better sense of its capabilities.
:::

## Deciphering XML

eXtensible Markup Language (XML) is a plain text file that uses tags to describe the
structure and content of the data they contain. For example, the following might be a way
to represent a note from Saul R. Panel to Dr. Watts apologizing for leaving the project
in an incomplete state:

```xml
<note>
  <from>Saul R. Panel</from>
  <to>Dr. Watts</to>
  <heading>Note about project</heading>
  <body>Sorry for leaving the project in an incomplete state!</body>
</note>
```

In JSON, the equivalent information could be formatted as:
```output
{"note":
    {"from": "Saul R. Panel",
    "to": "Dr. Watts",
    "heading": "Note about project",
    "body": "Sorry for leaving the project in an incomplete state!"
    }
}
```

Like other markup languages (HTML, LaTeX), XML wraps around data, providing information
about the structure, format, and relationships between components. Each tag provides
metadata about what the piece of data it contains represents - for instance `<row>` will
contain a row of data, while `<plantCode>243</plantCode>` will means that the plant code
is 243.

Each tag in XML shares similarities with a key in a JSON file:
- both provide metadata about what the corresponding value _is_ (e.g., a note, net generation in watts)
- both provide information about nested relationships (e.g., the note contains a heading and a body)

However, unlike JSON, XML tags:
- can have additional attributes (e.g., <note date="2008-01-10">), providing a way to
share more complex metadata about a given data point and to search for tags matching
additional filters (e.g., all notes written after Jan 01, 2008).

While XML is harder and slower to read than JSON, it also has more capabilities. You might
be likely to see an XML file if the data you're looking at:
- is old! XML was invented in 1998 and is still widely in use in older data distribution
methods.
- has deeply nested hierarchies of relationships, like FERC's accounting data.
- is large and complex! For instance, JSON can only handle strings, numbers and booleans,
while XML can also be used to share images, charts and graphs.
- is distributed through an RSS feed. For instance, FERC publishes filings on a rolling
basis using an RSS feed and the XML data format.

::: challenge
### Challenge 4: From XML to Pandas

Look at the following XML code.

```output
<data>
    <row>
        <period>2022-12</period>
        <plantCode>59656</plantCode>
        <plantName>Comanche Solar</plantName>
    </row>
    <row>
        <period>2023-01</period>
        <plantCode>59657</plantCode>
        <plantName>Comanche</plantName>
    </row>
</data>
```

Which of the following Pandas DataFrames would best represent the data in this XML file?

A.
```output
|    data   |       row      |
|:---------:|:--------------:|
| period    | 2022-12        |
| plantCode | 59656          |
| plantName | Comanche Solar |
| period    | 2023-01        |
| plantCode | 59657          |
| plantName | Comanche       |
```

B.
```output
|    row    |      data      |
|:---------:|:--------------:|
| period    | 2022-12        |
| plantCode | 59656          |
| plantName | Comanche Solar |
| period    | 2023-01        |
| plantCode | 59657          |
| plantName | Comanche       |
```

C.
```
|  period | plantCode | plantName      |
|:-------:|-----------|----------------|
| 2022-12 | 59656     | Comanche Solar |
| 2023-01 | 59657     | Comanche       |
```

D.
```
| plantName | Comanche Solar | Comanche |
|:---------:|----------------|----------|
| period    | 2022-12        | 2023-01  |
| plantCode | 59656          | 59657    |
```

:::solution
The solution is C:
```
|  period | plantCode | plantName      |
|:-------:|-----------|----------------|
| 2022-12 | 59656     | Comanche Solar |
| 2023-01 | 59657     | Comanche       |
```

The `<data>` is split into two seperate chunks of data seperated by `<row>` tags, which
tells us that everything between these tags corresponds to a single row of data. Then,
we know that the `<period>`, `<plantCode>` and `<plantName>` tags are telling us what
variable the values correspond to - or in other words, what the column name is that
corresponds to each tag.
:::

:::

## Using `pd.read_xml()`

Like with our other data types, we can use `pd.read_xml()` to parse XML files into Pandas DataFrames. `pd.read_xml()` is designed to ingest tabular data nested in XML files,
not to coerce highly nested data into a table format. To use this method, we'll need to
identify where in our XML file the data is structured into a table-like format and can
be easily extracted to a DataFrame. For more on `pd.read_xml()`, see the [Pandas documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_xml.html#pandas.read_xml#notes).

Let's try to explore the XML file that the postdoc left behind:
```python
pd.read_xml('data/eia923_2022.xml')
```

Each tag has been assigned as a column name, and the value inside has been added as a row. To drill down to the `<data>` we are actually interested in,
we can use the `xpath` parameter, which lets you specify where in the XML file to look for a table.

The `xpath` query we're looking for is formatted as follows:
- // are used at the beginning to note that we want to select all items with the tags specified
- Then, like specifying which directory we want to access in a terminal, slashes are used to specify the path to the desired tag.

So to get all the `<row>`s of `<data>`, we call:
```python
pd.read_xml('data/eia923_2022.xml', xpath = "//response/data/row")
```

`xpath` can be used to make more complex queries (e.g., only picking `<note>`'s written
after a certain date), but we won't cover more advanced usage of `xpath` in this tutorial.
See this [Library Carpentries tutorial](https://carpentries-incubator.github.io/lc-webscraping/02-xpath/index.html) for more about `xpath`.

## `pd.read_parquet()`

There's one more file left in the `data` folder the postdoc left behind - a Parquet file!
You can think of Parquet files as spreadsheet storage optimized for computers. Like an
Excel file, it's very difficult for a human to read the plain text of the file, as
it is designed to be read efficiently by software. To get into the technical weeds, see
the [Parquet documentation](https://parquet.apache.org/docs/overview/).

Parquet files:
- are designed to efficiently process and store large volumes of data, making them about
50x faster than using `pd.read_csv()` on comparable file sizes.
- compress data efficiently, reducing file size
- are saved with data organized into chunks (e.g., one chunk per month), making it possible
to quickly load data from some part of the dataset without loading everything into memory.
- are supported by many existing tools, including `Pandas`.

We can read a Parquet file to a Pandas DataFrame using `pd.read_parquet()`, almost identical to how we read in a CSV:

```py
eia923_parquet = pd.read_parquet('data/eia923_2022.parquet')
```

:::::::: challenge

Pick two datasets we've just read in, and compare them. How are they similar, and how are they different? Share your reflections with a peer.

:::: hint

- `df.info()` provides a high level summary of the data, including the
columns available, their data types, the number of non-null values in each column, and the overall number of rows in the DataFrame.
- Inspect a column in a DataFrame `df` by using `df[column_name]`.
- To quickly see what values are contained in a column, you can use `df[column_name].unique()` to get a list of unique values in the column.
- Try using `df.iloc[0]` to get the values from the first row of the data.
- `df.head(n)` returns the first n rows of the data, and `df.tail(n)` returns the last n rows.

::::

::::::::


:::: keypoints

- `pandas` has functionality to read in many data formats (e.g., XML, JSON,
Parquet) into Pandas DataFrames in Python. We can take advantage of this to
transform many kinds of structured and semi-structured data into similarly formatted data.
- The `help` function can be used to access function documentation, providing avenues to resolve problems on import of various data types.
- When semi-structured data contains tabular data, we can extract the tabular data into a Pandas Dataframe.
- `pandas` accepts both relative and absolute file paths on read-in.

::::
