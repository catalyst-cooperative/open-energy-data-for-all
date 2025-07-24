---
title: "Visual Data Exploration"
teaching: 55
exercises: 25
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I get ready to do research with data that is new to me?
- What should I do when I find something that doesn't look right?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use divide-and-conquer to split a wide table into manageable pieces
- Examine data for anomalies
- Execute strategies for locating cause and extent of anomalies

::::::::::::::::::::::::::::::::::::::::::::::::

Now that you have some raw data, how do you get from there to actually doing research with it?

Maybe you already have a research question;
how do you get your data into a form that can help you answer it?
How do you know your data doesn't have gremlins hiding in it that will mess up your research?

In this session we will do some initial data explorations and develop strategies for identifying and diagnosing sneaky data problems
-- including the use of data visualization as part of your exploration toolkit.
Plots aren't just for papers!

Data problems come in many different forms, and how you respond to them will depend on the source of the problem and what kind of impact it will have on the kinds of modeling and analysis you want to do.

* Problems introduced by the respondent - typos and other data entry errors - These can be fixed if they're simple, or can be a reason to exclude certain rows if correct values can't be reconstructed.
* Problems introduced by the data aggregator - disagreement between documentation you received and the actual forms filled out by respondents; a bad choice of data format that doesn't preserve relationships within the data - These can sometimes be "fixed" by working out logically what the definition of a column should actually be, but sometimes
* "Problems" introduced by external forces - natural disasters, policy change - These may be retained or excluded depending on your exact area of research.
* Problems we created for ourselves - We'll talk about this later.

Data problems can be identified at the column level and in the relationship between columns.

When identifying data problems, it is useful to think about what you expect to see from certain kinds of data.

* Numeric data might be in whole numbers (1, 2, -11, 56,912) or use decimal fractions (3.14, 0.000123, -65,536.2).
  In programming, a whole number is often called an "integer" or "int" while a number with a decimal fraction is often called a "float"
  (short for "floating point", which has to do with minutiae of how fractions are implemented in binary -- we don't need to know the details for this course)
* Categorical data takes on one of a restricted set of available values.
  They might be ID numbers, an alphanumeric string, a few words, or a few letters meant to abbreviate a longer category name.
  If a value appears that is not in the restricted set, that value is invalid, and likely resulted from a typo or similar error.
  An explanation of all the available values for each categorical column is usually included in the documentation for a data source, but sometimes you can get a rough idea from context.
* Free text data [which we won't cover today] is unrestricted, except perhaps in length.
  It might be a description of an incident, location, or piece of equipment.
  A free text value is not required to match any other entry or registry, and there's usually no such thing as an invalid value.
  Free text typically requires the application of qualitative research methods before it can be analyzed further.

All data types need to deal with situations where no value is available for that entry.
In pandas, we usually encode an intentionally missing value as `NA`.
Elsewhere in Python, we use `None`.
Other programming languages, software, and systems may make different choices.
Often, one of the first things to do when getting a new data set ready for research is to figure out how missing data was encoded by the data source, and map that to how *you* plan to encode missing data.

# Put it into practice

Let's take a look at how these ideas apply to real data.

You have two data files which were prepared by your predecessor, based on raw data from EIA-923 for Puerto Rico:

* `eia923__annual_puerto_rico_generation_fuel.parquet`
* `eia923__monthly_puerto_rico_generation_fuel.parquet`

(They also left you their source code, but it looks horrendous, so we'll start with the data and take a look at the code in another session)

We will ask ourselves:

* What kinds of data are there?
* What do I expect to see from this data?
* What do I actually see?
* Can I justify or explain any differences between what I expect and what I actually see?

## Annual data

We'll start with the annual file.

```python
annual_pr_gen_fuel = pd.read_parquet('../data/eia923__annual_puerto_rico_generation_fuel.parquet')
annual_pr_gen_fuel
```

Our predecessor has already taken care of a lot of the cleaning necessary for this data.
If any of you have used EIA data before, you may know that they use "." to encode missing numeric values, which does not normally play nicely with math.
In this data frame, those have all been converted to something else, probably pandas `NA` or Python `None`:

```python
annual_pr_gen_fuel == "."
(annual_pr_gen_fuel == ".").any()
```

There are 24 columns here, which is a little much to reason about all at once.
One way to tackle a problem that seems too large is to break it up into smaller pieces.
There are lots of ways to split up a wide table, and they'll all work well enough to get you started:

* Split up columns by purpose
  * Primary key or index columns: the columns that uniquely identify each row of data; closely related to what each row represents
  * Timeseries columns: the independent and dependent variables you would plot in a line chart
  * _ columns: the columns you could use to group data together and see if different groups have different properties
* Split up columns by data type
  * Numeric data
  * Categorical data
    * Identifiers
    * ...Other stuff

Generally, splitting up columns by purpose requires more domain knowledge, but can also help you understand the meaning of the data more quickly than looking just based on data type.
We'll use a little of both so you can see what they're like.

### Primary key

Let's start with a primary key.
What columns, taken together, have unique values from row to row?
What does each row in this file represent?
If you happen to know, you can shout it out in chat, otherwise I'll open up the source data Excel file, the grandfather of this dataframe, which has some documentation we can look at.

TODO: screenshot. Alt text:
Excel screenshot showing tab "Page 7 File Layout" of file "eia923_pr.xlsx".
A table titled "Generation and Fuel Data" has two columns, "Data Elements" and "Description".
The first few rows are visible; contents as follows.
Plant ID: EIA Plant Identification number. One to five digit numeric.
Combined Heat & Power Plant: Whether or not the plant is a combined heat & power facility (cogenerator). One character alphanumeric, "Y" or "N".
Nuclear Unit ID: For nuclear plants only, the unit number. One digit numeric. Nuclear plants are the only type of plants for which data are shown explicitly at the generating unit level.
Plant Name: Plant name. Alphanumeric.
Operator Name: The name of the entity which operates the plant. Alphanumeric.
Operator ID: The EIA operator identification number. Five digit numeric, padded with leading zeros.
State: State the facility is located in. Two character alphanumeric (standard state postal codes).

The documentation doesn't tell you what has to be unique for each entry; we will have to reason it out.

[time passes]

* Plant ID
* Year

Let's check.
If that's the primary key, then we expect each pair of (plant ID, year) values to only occur once in the data frame.
We can test that by grouping by those columns and then printing the size of each group.
If there are no groups with more than one row in them, or few enough that we could believe they were mistakes, then we got it.

```python
primary_key_columns = ["plant_id_eia", "report_year"]
annual_pr_gen_fuel.groupby(primary_key_cols).size()
```

Oh dear there are some twos and threes.
For easier readability we can add the plant name in.

```python
primary_key_columns = ["plant_id_eia", "plant_name_eia", "report_year"]
annual_pr_gen_fuel.groupby(primary_key_cols).size()
```

And then filter for just the ones with multiple rows.

```python
primary_key_columns = ["plant_id_eia", "plant_name_eia", "report_year"]
pk_sizes = annual_pr_gen_fuel.groupby(primary_key_cols).size()
pk_sizes.loc[pk_sizes>1]
```

Ninety one! Out of 283.
That's almost a third.
We might expect a few errors but a third is too many;
it's more likely we're wrong about the primary key.

[time passes]

```python
primary_key_columns = [
    'plant_id_eia', 'plant_name_eia', 'report_year', 'prime_mover_code', 'energy_source_code'
]
pk_sizes = annual_pr_gen_fuel.groupby(primary_key_columns).size()
pk_sizes.loc[pk_sizes>1]
```

```output
plant_id_eia  plant_name_eia            report_year  prime_mover_code  energy_source_code
62410         Cervecera de Puerto Rico  2020         IC                DFO                   2
dtype: int64
```

Only one!
That's plausibly a respondent error or data entry problem.
We can note that plant down as a possible troublemaker to investigate later.

But we have our primary key!
That's five columns we've carved off of the original 24, using the "split columns by purpose" strategy.
We wound up needing a combination of domain knowledge from the documentation, and empirical knowledge gained by guess-and-check.

Next let's take a look at an example of the "split columns by data type" strategy.

### Categorical data

To find out what columns probably contain categorical data, we can list the data type of each column.

```python
annual_pr_gen_fuel.dtypes
```

Because this data frame doesn't contain any free text, it is likely that any column with a string type contains categorical data.
To get a list, we can filter:

```python
annual_pr_gen_fuel.dtypes[annual_pr_gen_fuel.dtypes == "string[python]"]
annual_pr_gen_fuel.dtypes[annual_pr_gen_fuel.dtypes == "string[python]"].index
list(annual_pr_gen_fuel.dtypes[annual_pr_gen_fuel.dtypes == "string[python]"].index)
category_columns = list(annual_pr_gen_fuel.dtypes[annual_pr_gen_fuel.dtypes == "string[python]"].index)
```

We know from the documentation we looked at earlier that some of these are identifiers with large sets of possible values, and the rest have much smaller sets of possible values.
It is useful to treat these separately.
Let's do that now.

```python
identifier_columns = [
    "operator_name",
    "plant_name_eia",
]
category_columns = [c for c in category_columns if c not in identifier_columns]
category_columns
```

We can use `.describe()` to show some basic information about category data.
Let's look at the identifier columns as an example:

```python
annual_pr_gen_fuel[identifier_columns].describe()
```

```output
                             operator_name plant_name_eia
count                                  450            450
unique                                  30             55
top     Puerto Rico Electric Pwr Authority  Aguirre Plant
freq                                   206             45
```


----

## Previous content

We could jump right into the notebook, but reading someone else's code is always easier if you can establish a little context first.

Let's take a look at the data ourselves.

```python
pr_gen_fuel_raw = pd.read_pickle('../data/raw_eia923__puerto_rico_generation_fuel')
pr_gen_fuel_raw
```

Things to notice:

* There are multiple different data types: category data (associated_combined_heat_power) and numeric data (*_mmbtus)
* Some of the numeric columns have weird "." entries, which doesn't seem right
* There's a column for each month, but these are in... alphabetical order?
* Year is an integer but also sometimes has a decimal?

We could try to clean this up ourselves, but there's a good chance our predecessor fixed at least some of them. Let's go see!

# 2: Look at our predecessor's work

If we open `puerto-rico-project.ipynb` we see:

```python
# Handle EIA null values
pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA)
```

Hey, nice! That's the weird "." out of the way.

Next we get:

```python
# Convert data types (mmbtu/units to numeric)
pr_gen_fuel = pr_gen_fuel.convert_dtypes()
```

The help() for `convert_dtypes()` says:

> Convert columns to the best possible dtypes using dtypes supporting ``pd.NA``.

That seems close-ish to the problem with years being integers or floats. If we get stuck on dtypes later we can always come back to it.

Next we get:

```python
# create some useful column sets
primary_key_columns = ['plant_id_eia', 'plant_name_eia', 'report_year', 'prime_mover_code', 'energy_source_code']

monthly_variables = []
for col in pr_gen_fuel.columns:
    if col.endswith("january"):
        monthly_variables.append(col.replace("_january", ""))

monthly_columns = []
for col in pr_gen_fuel.columns:
    for var in monthly_variables:
        if col.startswith(var):
            monthly_columns.append(col)
```

A primary key is sometimes called an index; it just means that no two rows have the same values for those columns taken together.

It looks like they built a list of the monthly data columns by first grabbing all the January columns, then using the front part of the string to get a list of all the monthly variables. Then from there, you can grab all the columns that start with each monthly variable, and get all the months.

Next we get:

```python
# pivot the monthly variables into their own df
monthly_dfs = []
# swap in a different date column
monthly_primary_key_columns = ["date"] + [c for c in primary_key_columns if c != "report_year"]
for monthly_var in monthly_variables:
    ## Only keep the index and monthly variable columns
    column_subset_list = primary_key_columns + [col for col in pr_gen_fuel.columns if col.startswith(monthly_var)]
    var_pivot = (
        pr_gen_fuel.loc[:, column_subset_list]
        .melt(id_vars = primary_key_columns)
    )
    ## Split the month from the variable
    var_pivot[['variable', 'month']] = var_pivot['variable'].str.rsplit("_", n=1, expand=True)
    ## Create date from month and year
    var_pivot['date'] = pd.to_datetime(var_pivot['month'] + var_pivot['report_year'].astype(str), format='%B%Y')
    # we don't need the year/month/variable cols anymore
    monthly_dfs.append(
        var_pivot.drop(columns=["report_year", "month", "variable"])
        .rename(columns={"value":monthly_var})
        # setting an index so we can concatenate later
        .set_index(monthly_primary_key_columns)
    )
pr_gen_fuel_monthly = pd.concat(monthly_dfs, axis="columns").reset_index()
```

That's ... a big chunk of code. Rather than try to interpret it line-by-line, let's see if we can match their comment `split off a separate table for monthly data` to the actual output.

```python
pr_gen_fuel_monthly
```

That went from 96 columns down to 11! There's now a `date` column that looks like it's always the first of the month. Then we have columns identifying the plant, prime mover, and energy source. Then six numeric columns, one for each monthly variable.

That looks like it could be very useful!

There are only two more cells. First we have:

```python
# the rest of the columns are annual
pr_gen_fuel_annual = pr_gen_fuel.drop(columns=monthly_columns)
```

That's fair; with the monthly data in a separate table we don't need to keep those columns around.

Then we have:

```python
# drop a bad plant
pr_gen_fuel_monthly = (
    pr_gen_fuel_monthly.loc[~(
        (pr_gen_fuel_monthly.plant_id_eia == 62410)
        & (pr_gen_fuel_monthly.date.dt.year == 2020)
        & (pr_gen_fuel_monthly.fuel_consumed_for_electricity_mmbtu.isnull()))]
)
```

Dropping a bad plant sounds like something we may need to do again later, so we'll remember this is here but otherwise leave it alone.

Let's store the clean version of the data so we can play with it more in our notebook, without polluting this one too much:

```python
pr_gen_fuel_monthly.to_parquet("../data/eia923__monthly_puerto_rico_generation_fuel.parquet")
pr_gen_fuel_annual.to_parquet("../data/eia923__annual_puerto_rico_generation_fuel.parquet")
```

Back in our notebook, we'll load up the data:

```python
pr_gen_fuel_monthly = pd.read_parquet("../data/eia923__monthly_puerto_rico_generation_fuel.parquet")
pr_gen_fuel_annual = pd.read_parquet("../data/eia923__annual_puerto_rico_generation_fuel.parquet")
```

Let's start with annual data first.

# 3: Build on our predecessor's work

Our predecessor had these set as primary key columns; let's take a closer look at them.

```python
primary_key_columns = [
    'plant_id_eia', 'plant_name_eia', 'report_year', 'prime_mover_code', 'energy_source_code'
]
pr_gen_fuel_annual[primary_key_columns]
```

They're supposed to be unique combinations; are they?

```python
pr_gen_fuel_annual[primary_key_columns].groupby(primary_key_columns).size()
```

```
pk_hits = pr_gen_fuel_annual[primary_key_columns].groupby(primary_key_columns).size()
pk_hits[pk_hits>1]
```

```output
plant_id_eia  plant_name_eia            report_year  prime_mover_code  energy_source_code
62410         Cervecera de Puerto Rico  2020         IC                DFO                   2
dtype: int64
```

Just one weirdo. Any chance it's from the same plant our predecessor found?

Why, yes. Indeed it is. We'll add that to the "deal with later" list while we're still exploring.

## Categorical data

What columns contain categorical data? Are they well-behaved?

```python
pr_gen_fuel_annual.dtypes
```

```python
pr_gen_fuel_annual.dtypes[pr_gen_fuel_annual.dtypes == "string[python]"]
```

```python
list(pr_gen_fuel_annual.dtypes[pr_gen_fuel_annual.dtypes == "string[python]"].index)
```

```python
category_cols = list(pr_gen_fuel_annual.dtypes[pr_gen_fuel_annual.dtypes == "string[python]"].index)
pr_gen_fuel_annual[category_cols[0]].value_counts()
```

:::: challenge

Make a `for` loop to show the value counts for all the category columns. Do any of them show anything wacky?

:::::::: solution
```python
for c in category_cols:
    print("="*40)
    print(pr_gen_fuel_annual[c].value_counts())
```
::::::::

::::

## Numeric data

What columns contain numeric data? Are they well-behaved?

```python
pr_gen_fuel_annual.dtypes
```

Oh dang, most of these integer columns aren't really numeric. Looks like we want four of the int columns and one of the floats. It's probably easier to make a list manually.

```python
numeric_cols = [
    "elec_fuel_consumption_mmbtu", "electric_fuel_consumption_quantity",
    "total_fuel_consumption_mmbtu", "total_fuel_consumption_quantity",
    "total_net_generation_mwh"
]
pr_gen_fuel_annual[numeric_cols].describe()
```

We've got two pairs of mmbtu+quantity variables. Since they're measuring in different units, we don't expect their quartiles to match, but we do kinda expect them to have the same shape. Let's look closer with a histogram:

```python
elec_fuel_consumption = (
    pr_gen_fuel_annual[["elec_fuel_consumption_mmbtu","electric_fuel_consumption_quantity"]]
)

(elec_fuel_consumption / elec_fuel_consumption.max()).plot.hist(bins=20, logy=True, alpha=0.5)
```

Wow, that's seriously systemic.

```python
for gr, df in pr_gen_fuel_annual.groupby("associated_combined_heat_power"):
    axs = df.hist(column=elec_fuel_consumption_cols, density=True)
    axs[-1][-1].legend([gr])
```

:::: challenge

Find a categorical column that seems to explain why there are so many more zeros in `quantity` than in `mmbtu`.

:::::::: solution

```python
for gr, df in pr_gen_fuel_annual.groupby("energy_source_code"):
    axs = df.hist(column=elec_fuel_consumption_cols, density=True)
    axs[-1][-1].legend([gr])
```

* SUN, WAT, and WND _always_ have zero `quantity`. Which kinda makes sense! How many suns did we burn today at the power plant? How about winds? ... waters? It doesn't explain why `mmbtu` for renewables is nonzero, but it's something!
* Bonus puzzle: MWH always has zero `mmbtu`! How odd.

Honorable mentions:

* `prime_mover` shows moderate differences for BA, CT, and ST as well as the overwhelming differences for HY, PV, and WT
* `fuel_unit` shows suspicious differences for megawatthours, though it's in the opposite direction
* `reporting_frequency_code` shows suspicious differences for AM, and mild but noticeable differences for M and A
* `data_maturity` shows mild differences for incremental_ytd

::::::::

::::

So now we know to stick to mmbtus if we want to capture renewables.

# Monthly data

Now let's look at the monthly data.

Most of these variables are time series, and that lends itself to plotting especially well.

Most people are familiar with putting plots in research papers, reports, and slides, where they're useful as evidence supporting your argument. To be effective, those plots need to -- essentially -- look nice: clear labels and titles, appropriate units and limits, good color separation for print or screen, tidy legends, minimizing extraneous data. The goal is to communicate your point.

When you're in the exploratory phase, you don't know what the point is yet, and you're communicating with yourself, now and future-you. Exploratory plots can be sloppy, so long as they are not _actively confusing_.

Pandas has great support for sloppy, but _quick_, plotting.

Let's look at all the monthly variables at once.

What do we want to see?

* a different line for each variable: fuel consumed for electricity, fuel consumed, fuel mmbtu, and net generation
* one value for each month -- we'll sum across all the plants

```python
pr_gen_fuel_monthly
pr_gen_fuel_monthly.groupby("date").sum()
pr_gen_fuel_monthly.groupby("date").sum().plot(y=monthly_variables)
```

Things to notice:
* Big zero spike in late 2017, all variables
* Everything drops to zero after early 2025; that's probably the end of the real data
* Variables are on vastly different scales but pandas did its best and it's okay

Let's dive in further. What's the energy source breakdown look like throughout the year?

What do we want to see?

* just fuel consumed mmbtus
* a different line for each energy source: CFO, SUN, NG, etc
* one value for each month -- we'll sum across all the plants

```python
pr_gen_fuel_monthly
pr_gen_fuel_monthly.groupby(["energy_source_code", "date"]).sum()
pr_gen_fuel_monthly.groupby(["energy_source_code", "date"]).sum().fuel_consumed_mmbtu
pr_gen_fuel_monthly.groupby(["energy_source_code", "date"]).sum().fuel_consumed_mmbtu.unstack("energy_source_code")
pr_gen_fuel_monthly.groupby(["energy_source_code", "date"]).sum().fuel_consumed_mmbtu.unstack("energy_source_code").plot()
```

Things to notice:

* Zero spike in 2017 visible in all energy sources but recovery severely delayed for BIT and renewables
* NG another big drop in late 2019/early 2020; again in late 2021. Independent of other energy sources though.
* RFO also seems to vary quite a lot; also not related to other energy sources.
* Renewables way smaller than others
* Renewables all drop starting in 2022

Let's put the renewables on their own plot so we can see them better.

```python
(
    pr_gen_fuel_monthly.loc[pr_gen_fuel_monthly.energy_source_code in renewables]
    .groupby(["energy_source_code", "date"]).sum()
    .fuel_consumed_mmbtu.unstack("energy_source_code").plot()
)
```

That makes an error. Darn. It would've been super convenient if that had worked.

What are our options here?

* do `(== "SUN") | (== "WND") | (== "WAT")`
* do something ... a little more flexible

```python
(
    pr_gen_fuel_monthly.set_index("energy_source_code").loc[renewables].reset_index()
    .groupby(["energy_source_code", "date"]).sum()
    .fuel_consumed_mmbtu.unstack("energy_source_code").plot()
)
```

Okay, yes, that is dramatic. Does this show up in the net generation as well?

:::: challenge

Adapt our current fuel_consumed_mmbtu plot to show net_generation instead.

:::::::: solution

(
    pr_gen_fuel_monthly.set_index("energy_source_code").loc[renewables].reset_index()
    .groupby(["energy_source_code", "date"]).sum()
    .net_generation_mwh.unstack("energy_source_code").plot()
)

::::::::

No, not really :(

:::

Okay, what else could it be? Maybe a big renewables plant opened or closed that did things differently than the others? Let's look for patterns or clusters in the relationship between net generation and fuel consumed mmbtus for renewables.

What do we want to see?

* a scatter plot with one point for each row
* net generation on the x axis
* fuel consumed on the y axis

```python
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu")
)
```

Well that's quite linear. Let's clean it up a little so we can see better; the dots are overlapping a lot.


```python
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.1)
)
```

Is that three lines? Three lines for three energy sources is awfully suspicious. Let's add color.

```python
(
    renewables_monthly
    .plot.scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.1, c="energy_source_code")
)
```

"c must be a sequence of numbers, not an array of strings"

Okay, well pandas has a categorical type that will turn our array of strings into numbers, let's use that.

```python
(
    renewables_monthly.assign(energy_source_code=pr_gen_fuel_monthly_renewables.energy_source_code.astype("category"))
    .plot.scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.1, c="energy_source_code", colormap="rainbow")
)
```

Oh do not like that. There are colors for all three energy sources on both lines. That does not explain this at all.

:::: challenge

Are there any other variables in our data that, when used to color this plot, clearly separate the lines by color?

::::::: solution

Disappointingly, `date` is the only one that really does it:

```python
(
    renewables_monthly
    .plot.scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.2, c="date", colormap="rainbow")
)
```

But at least it clearly identifies three lines. This feels like a policy change effect -- a coordinated change throughout Puerto Rico in how fuel consumption is reported for renewables (which as we know, is already a little weird).

:::::::

::::

Let's grab the slopes of those lines and see if that gets us any further:

```python
(
    renewables_monthly
    .assign(ratio=renewables_monthly.fuel_consumed_mmbtu/renewables_monthly.net_generation_mwh)
    .plot.scatter(x="date", y="ratio", s=0.2, c="date", colormap="rainbow")
)
```

Oh hey, more subtle than we thought. It looks like whatever constant everyone was using to compute fuel consumption changed a little bit each year, with a big gap for Maria, and then suddenly decided once and for all in 2022.

There's these little stragglers though; are those individual plants or some other effect?

```python
(
    renewables_monthly
    .assign(ratio=renewables_monthly.fuel_consumed_mmbtu/renewables_monthly.net_generation_mwh)
    .assign(plant_factor=renewables_monthly.plant_name_eia.astype("category"))
    .plot.scatter(x="date", y="ratio", s=0.2, c="plant_factor", colormap="rainbow")
)
```

Seems likely to be one or a small number of plants. If we wanted to figure out exactly which ones, we could split the data by year, use `.describe()` to get the median ratio for each year, then select all the rows that had a different ratio.


----
# Prior draft

* primary key columns: plant_id_eia, energy_source_code, prime_mover_code, report_year

## What are all the categorical columns?

* Use `.dtypes`
* Use `.dtypes.value_counts()`
* Use `.dtypes[.dtypes=="object"]`
* Use `.dtypes[.dtypes=="object"].index`
* Whoops it's got all the monthly columns in it.
* We'll want to look at monthly data later anyhow so let's identify all the monthly columns now so we can filter them out. We'll figure out why they're objects once we're done with categories.
* Demo: grab all the month columns of a single variable
* Demo: grab all the variable columns for january

:::: challenge

Make a list of all the monthly columns. Possible strategies:

- Make a list of variables and filter .columns using .startswith
- Make a list of months and filter .columns using .endswith
- Both? Something else?

:::::::: solution

::::::::

::::

* Drop monthly columns and *then* use & save `.dtypes[.dtypes=="object"].index`
* Use `[category_columns].info()`
  * 2 columns are always null
  * 2 columns have some nulls

### What is the NA situation?

* Drop the always-null columns and use `.loc[.isna().any(axis="columns")]`
* Hypothesis: nulls in fuel_unit are for renewables
  * Use `.loc[.fuel_unit.isna()].energy_source_code.value_counts()`
  * Confirmed!

## What are the non-monthly numerical columns?

* Use `.dtypes[.dtypes=="float64"]`; point out pairs of variables
* Use & save `.dtypes[.dtypes=="float64"].index`
* Use `[numerical_columns].describe()`
* Whoops why does quantity have more zeros?
* Use `.loc[.electric_fuel_consumption_quantity==0) & (.elec_fuel_consumption_mmbtu>0)]`
* Use `.report_year.value_counts()`

:::: challenge

Find out if one of the categorical columns explains what's happening with the zeros in quantity

* Demo `.loc[..., "report_year"].value_counts()`
* Demo `print(.loc[..., "report_year"].value_counts())`

:::::::: solution

it's renewables

::::::::

::::

# 2. Look at how far your predecessor got

* Read df from `pr_gen_fuel_elec_final.parquet`
  * Super narrow! only one numerical variable, fuel_consumed_for_electricity_mmbtu
  * Date is monthly
  * "." values are proper NAs
  * Nice
* Plot using `.groupby("date").sum().plot()`
* What is that big drop in 2017?
* Plot using `.groupby(["energy_source_code","date"]).sum().unstack("energy_source_code").plot()`
* Ohh that's probably Hurricane Maria :(
  * Interesting; it took longer for coal to come back than anything else
* What happened to renewables starting in 2022?
* Plot just renewables
* Yep. Let's check netgen. Our predecessor didn't make that one though, so we'll have to extend their code.

# 3. Extend predecessor's code

* Open old notebook & step through what it does
  * There's the fix for the . thing! Hooray
  * Here's where it gets rid of all the other numeric columns
  * Stacking monthly data... looks complicated. We'll come back to it.
  * A bad plant! good to know
  * Column renaming. normal
  * Stacking month columns: the details
    * Demo melt results: variable vs value
    * Demo rsplit results: setting fuel_variable and month
    * Demo month + report_year.astype(str): setting date
    * Dropping columns we don't need anymore
* Bring stacking code into our notebook and turn it into a for loop over our monthly variables
* Use `.set_index` so each item just has its value column
* Use `pd.concat`
* Visual check: use `.groupby('date").sum().plot(y=monthly_variables)`
* Use `.set_index("energy_source_code").loc[renewables].reset_index()`
* Plot renewables
  * Oh no netgen stays the same :(

# 4. Grind

* Plot by energy source code -- no help
* I wonder if some big plants closed that tracked things differently.
* Plot netgen x fuel mmbtu for each plant
  * Well there's the problem
  * It doesn't seem to be split by plants though
  * There are suspiciously three lines and we know there are three renewables
* Color by energy source code
  * That's not it :(
* Okay, uh, color by date?
  * Bingo
  * Probably some kind of coordinated change in reporting
  * Any models we make will have to account for that carefully


::::::::::::::::::::::::::::::::::::: keypoints

- Cleaning is an important part of/easy way into getting to know a new data set
- Different kinds of data -- indexing, categorical, numeric, periodic -- are suited to different kinds of summarization
- Use divide-and-conquer strategies when working with tables that have a lot of columns (common in energy data)
- Visualization is not just for reports, papers, and talks! If you incorporate plotting into your exploration & troubleshooting toolbox you'll be able to identify and diagnose data problems much more quickly than if you wait for your model to exhibit strange behavior.

::::::::::::::::::::::::::::::::::::::::::::::::
