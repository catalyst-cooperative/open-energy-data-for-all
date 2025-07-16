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
* Some of the numeric columns have weird numbers in them like ".", which doesn't seem right
* There's a column for each month, but these are in... alphabetical order?
* Year is an integer but also sometimes a float?

We could try to clean this up ourselves, but there's a good chance our predecessor fixed at least some of them. Let's go see!

# 2: Look at our predecessor's work

If we open `puerto-rico-project.ipynb` we see:


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
