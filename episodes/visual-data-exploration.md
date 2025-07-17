---
title: "Visual Data Exploration"
teaching: 55
exercises: 25
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I get ready to do research with this new data I found?
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

In this session we will do some initial data explorations,
build familiarity with the kinds of cleaning that are typically necessary for energy data,
and develop strategies for identifying and diagnosing sneaky data problems
-- including the use of data visualization as part of your exploration toolkit.
Plots aren't just for papers!

# 1: Look at the data

You have a raw data file, `raw_eia923__puerto_rico_generation_fuel.parquet`.

You also have a notebook from your predecessor, `puerto-rico-project.ipynb`.

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
