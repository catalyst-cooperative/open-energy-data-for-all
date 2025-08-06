---
title: "Visual Data Exploration"
teaching: 55
exercises: 25
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I get ready to do research with data that is new to me?
- What should I do when I find something that doesn't look right?
- How can I get a head start on identifying data problems that might cause headaches later?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use divide-and-conquer to split a wide table into manageable pieces
- Examine data for anomalies using summarization and visualization
- Articulate the difference between refining plots for exploration and refining plots for presentation
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

* **Problems introduced by the respondent** - typos and other data entry errors - These can be fixed if they're simple, or can be a reason to exclude certain rows if correct values can't be reconstructed.
* **Problems introduced by the data aggregator** - disagreement between documentation you received and the actual forms filled out by respondents; a bad choice of data format that doesn't preserve relationships within the data - These can sometimes be "fixed" by working out logically what the definition of a column should actually be, but sometimes TODO
* **"Problems" introduced by external forces** - natural disasters, policy change - These may be retained or excluded depending on your exact area of research.
* **Problems we created for ourselves** - We'll talk about this in a later session.

Data problems can be identified at the column level and in the relationship between columns.

When identifying data problems, it is useful to think about what you expect to see from certain kinds of data.

* **Numeric data** might be in whole numbers (1, 2, -11, 56,912) or use decimal fractions (3.14, 0.000123, -65,536.2).
  In programming, a whole number is often called an "integer" or "int" while a number with a decimal fraction is often called a "float"
  (short for "floating point", which has to do with minutiae of how fractions are implemented in binary -- we don't need to know the details for this course)
* **Categorical data** takes on one of a restricted set of available values.
  They might be ID numbers, an alphanumeric string, a few words, or a few letters meant to abbreviate a longer category name.
  If a value appears that is not in the restricted set, that value is invalid, and likely resulted from a typo or similar error.
  An explanation of all the available values for each categorical column is usually included in the documentation for a data source, but sometimes you can get a rough idea from context.
* **Free text data** [which we won't cover today] is unrestricted, except perhaps in length.
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

* `pr_gen_fuel_annual.parquet`
* `pr_gen_fuel_monthly.parquet`

(They also left you their source code, but we'll start with the data and take a look at the code in another session)

We will ask ourselves:

* What kinds of data are there?
* What do I expect to see from this data?
* What do I actually see?
* Can I justify or explain any differences between what I expect and what I actually see?

## Annual data

We'll start with the annual file.

```python
import pandas as pd
pr_gen_fuel_annual = pd.read_parquet('../data/pr_gen_fuel_annual.parquet')
pr_gen_fuel_annual
```

Our predecessor has already taken care of a lot of the cleaning necessary for this data.
If any of you have used EIA data before, you may know that they use "." to encode missing numeric values, which does not normally play nicely with math.
In this data frame, those have all been converted to something else, probably pandas `NA` or Python `None`:

```python
pr_gen_fuel_annual == "."
(pr_gen_fuel_annual == ".").any()
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
If we were familiar with EIA 923 from other research, we might know that already.
If not, we can open up the source data Excel file, the grandfather of this dataframe, which has some documentation we can look at.

![Excel screenshot showing tab Page 7 File Layout of data/eia923_pr.xlsx](fig/ep-5/eia923-filelayout.png){alt="Excel screenshot showing tab Page 7 File Layout of file data/eia923_pr.xlsx.
A table titled Generation and Fuel Data has two columns, Data Elements and Description.
The first few rows are visible; contents as follows.
Plant ID: EIA Plant Identification number. One to five digit numeric.
Combined Heat & Power Plant: Whether or not the plant is a combined heat & power facility (cogenerator). One character alphanumeric, Y or N.
Nuclear Unit ID: For nuclear plants only, the unit number. One digit numeric. Nuclear plants are the only type of plants for which data are shown explicitly at the generating unit level.
Plant Name: Plant name. Alphanumeric.
Operator Name: The name of the entity which operates the plant. Alphanumeric.
Operator ID: The EIA operator identification number. Five digit numeric, padded with leading zeros.
State: State the facility is located in. Two character alphanumeric (standard state postal codes)."}

The documentation doesn't say what has to be unique for each entry; we will have to reason it out.
We know each plant has to file with the EIA every year, so we'll use that as our initial guess:

* Plant ID
* Year

Let's check.
If that's the primary key, then we expect each pair of (plant ID, year) values to only occur once in the data frame.
We can test that by grouping by those columns and then looking at the size of each group.
If there are no groups with more than one row in them, or few enough that we could believe they were mistakes, then we got it.

```python
primary_key_columns = ["plant_id_eia", "report_year"]
pr_gen_fuel_annual.groupby(primary_key_columns).size()
```

Oh dear there are some twos and threes.
For easier readability we can add the plant name in.

```python
primary_key_columns = ["plant_id_eia", "plant_name_eia", "report_year"]
pr_gen_fuel_annual.groupby(primary_key_columns).size()
```

And then filter for just the ones with multiple rows.

```python
primary_key_columns = ["plant_id_eia", "plant_name_eia", "report_year"]
pk_sizes = pr_gen_fuel_annual.groupby(primary_key_columns).size()
pk_sizes.loc[pk_sizes>1]
```

Ninety one! Out of 283.
That's almost a third.
We might expect a few errors but a third is too many;
it's more likely we're wrong about the primary key.
Let's look at one example.

```python
pr_gen_fuel_annual.loc[
    (pr_gen_fuel_annual.plant_id_eia == 61034) &
    (pr_gen_fuel_annual.report_year == 2017)
].transpose()
```

Looks like these two records differ in `prime_mover_code`.
Let's add that in.

```python
primary_key_columns = ["plant_id_eia", "plant_name_eia", "report_year", "prime_mover_code"]
pk_sizes = pr_gen_fuel_annual.groupby(primary_key_columns).size()
pk_sizes.loc[pk_sizes>1]
```

Better, but we still have a lot of duplicates.

::: challenge

Look at one of the duplicate entries and propose another column to add to our primary key.

:::: solution

If we add `energy_source_code` to our primary key, we end up with only one duplicate entry.


```python
primary_key_columns = [
    'plant_id_eia', 'plant_name_eia', 'report_year', 'prime_mover_code', 'energy_source_code'
]
pk_sizes = pr_gen_fuel_annual.groupby(primary_key_columns).size()
pk_sizes.loc[pk_sizes>1]
```

```output
plant_id_eia  plant_name_eia            report_year  prime_mover_code  energy_source_code
62410         Cervecera de Puerto Rico  2020         IC                DFO                   2
dtype: int64
```

::::

:::


Only one!
That's plausibly a respondent error or data entry problem.
We can note that plant down as a possible troublemaker to investigate later.

But we have our primary key!
That's five columns we've carved off of the original 24, using the "split columns by purpose" strategy.
We wound up needing a combination of domain knowledge from the documentation, and empirical knowledge gained by guess-and-check.

Using this approach, we found one duplicate entry that could mess up our analysis later.

Next let's take a look at an example of the "split columns by data type" strategy.

### String data as categorical data

We'll start with string data.
First, we'll print out the data type of each column.

```python
pr_gen_fuel_annual.dtypes
```

Some of these have already been labeled as categorical data.
We know from our earlier peek at the full data frame that none of these string columns contain free text.
Unless we have domain-specific knowledge telling us otherwise, it is reasonable to guess that any column with a string type contains categorical data.
This might not capture all the categorical data in the data frame, but it'll get us started.
To get a list, we can filter:

```python
category_columns = list(
    pr_gen_fuel_annual.dtypes[
        (pr_gen_fuel_annual.dtypes == "category") |
        (pr_gen_fuel_annual.dtypes == "string[python]") |
        (pr_gen_fuel_annual.dtypes == "boolean")
    ].index
)
category_columns
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
pr_gen_fuel_annual[identifier_columns].describe()
```

```output
                             operator_name plant_name_eia
count                                  450            450
unique                                  30             55
top     Puerto Rico Electric Pwr Authority  Aguirre Plant
freq                                   206             45
```

* `count` shows us how many rows have a value set. If it's equal to the total number of rows, you know you have no nulls. Looks like there aren't any nulls in the operator name or plant name columns, which is good.
* `unique` shows us how many unique values are in each column. Looks like there are 30 operators and 55 plants. If we knew how many operators and how many plants to expect, this could tell us if there were typos -- each typo would register as an extra unique value.
* `top` shows us the most common value each each column, and `freq` shows how many times that value appeared. Looks like just under half the rows have the top operator, Puerto Rico Electric Pwr Authority. Exactly 10% of the rows have the top plant, Aguirre.

If we did suspect a typo, we could look at all the unique values and their frequencies using `.value_counts()`.

```python
pr_gen_fuel_annual.operator_name.value_counts()
```

By default this gives you the results in descending order of frequency, which is helpful: typos and other errors are likely to be at the bottom. If there are entries that appear a suspiciously small number of times, you can sort by index to re-order the list and make it more obvious when two neighboring entries differ by a letter:

```python
pr_gen_fuel_annual.operator_name.value_counts().sort_index()
```

Here we see some similar names, but no typos.

:::: challenge

Your turn: Use `.describe()` on the other category columns. Use the File Layout documentation to verify whether the `reporting_frequency_code` and `fuel_unit` columns have the expected number of unique values in them.

:::::: solution

```python
pr_gen_fuel_annual[category_columns].describe()
```

`reporting_frequency_code` looks good; the File Layout documentation says there are three options, and we see three unique values here. There are some nulls though. Something to keep an eye on if we end up needing this column for something later.

`fuel_unit` looks off, since File Layout says there should be three values but `.describe()` found four. Let's look closer:

```python
pr_gen_fuel_annual.fuel_unit.value_counts()
```

```output
fuel_unit
barrels          237
mcf               49
megawatthours     24
short tons         9
Name: count, dtype: Int64
```

Huh. `megawatthours` is not a valid physical unit, according to the documentation... but it's definitely not a typo. How is this being used in the data?

We can filter for just the rows that use `megawatthours` in the `fuel_unit` column:

```python
pr_gen_fuel_annual.loc[pr_gen_fuel_annual.fuel_unit == "megawatthours"]
pr_gen_fuel_annual.loc[pr_gen_fuel_annual.fuel_unit == "megawatthours", category_columns].describe()
```

We can eyeball the whole dataframe looking for patterns, or we can use `.describe()` to help us know for sure whether each column has multiple values or only one.

* `energy_source_code` is MWH, which intuitively matches the unit but isn't particularly illuminating
* `fuel_type_code_agg` is OTH, probably for "Other"; no help there
* `prime_mover_code` is BA, which is worth looking up. "Energy Storage, Battery" -- looks like at least some of the PR respondents report generation from batteries using a fuel unit, which isn't expected by the EIA, but they're consistent about it, which is nice.

::::::

::::

We've split off 11 of the 24 columns (2 identifiers, 9 other categoricals) using the "split by data type" approach to look at string data.
Using this approach, we found some null values we'll need to handle carefully if we need those columns for our research,
and we found one off-spec-but-ultimately-reasonable rogue value for `fuel_unit` that could have tripped us up if we relying on the documentation alone.

### Numeric data

But we're here for *visual* data exploration! Let's look at some data we can plot.

```python
pr_gen_fuel_annual.dtypes
pr_gen_fuel_annual.drop(columns=category_columns).dtypes
```

So while the string data was pretty much all categorical, the numeric data is... more of a mess.
A bunch of these columns are numeric identifiers for other kinds of categories.
We want to plot measurement data, not numeric identifiers.
We need some domain knowledge to help us sort numeric measurement data from the others.
This is where dataset documentation can help.

::: challenge

Open `data/eia923_pr.xlsx` and use the File Layout tab to determine which columns contain measurement data.

Watch out!

* Some of the column names in our data frame have been changed from the originals referenced in the documentation.
* Some of the documentation has typos.

:::: solution

```python
measurement_columns = [
    "elec_fuel_consumption_mmbtu", "electric_fuel_consumption_quantity",
    "total_fuel_consumption_mmbtu", "total_fuel_consumption_quantity",
    "total_net_generation_mwh"
]
```

::::

:::

When we were looking at categorical string data, we used `.describe()` to show a summary that helped us determine whether the data was reasonable or not.
We can use `.describe()` on numeric data, too!

```python
pr_gen_fuel_annual[measurement_columns].describe()
```

For numeric data, `.describe()` gives us statistics for each column.

* `count` is the same as with string data: it shows us how many rows have a value set. For all of these numeric columns, it is equal to the total number of rows, so we know we have no nulls.
* `mean` is the average. If one of these showed a wildly unexpected scale, or large negative, we would know something was weird, but these all look plausible.
* `std` is the standard deviation, which tells you how spread out the values are in each column.
* `min`, `25%` `50%` `75%` (quartiles), `max` give a rough idea of how the data are distributed. We have some negatives in `total_net_generation_mwh`, but negatives do show up sometimes in netgen, and negative 3,000 on a maximum of 3,000,000 is reasonable.

We've got two pairs of mmbtu+quantity variables.
Since they're measuring in different units,
we don't expect their values to match,
but we do kinda expect them to have the same shape.
But it looks like the `_quantity` variables have a lot more zeros in them.
Let's look closer with a histogram:

```python
elec_fuel_consumption_cols = ["elec_fuel_consumption_mmbtu","electric_fuel_consumption_quantity"]
elec_fuel_consumption = pr_gen_fuel_annual[elec_fuel_consumption_cols]
elec_fuel_consumption.hist()
# elec_fuel_consumption.hist(sharey=True)
elec_fuel_consumption.hist(sharey=True, log="y")
```

The first thing it prints out is this array of Axes.
There is one for each column we plotted.
We'll talk more about Axes in a little bit.

The next thing is shows is the histogram.
There are a few things preventing this graph from telling us what we want to know.
A histogram has the value on the x axis and the frequency of that value / range of values on the y axis.
These two plots have different y axes, which makes it difficult to see that the zero bin has a different frequency for mmbtus on the left than for quantity on the right.
We can fix that with `sharey`.

```python
elec_fuel_consumption_cols = ["elec_fuel_consumption_mmbtu","electric_fuel_consumption_quantity"]
elec_fuel_consumption = pr_gen_fuel_annual[elec_fuel_consumption_cols]
elec_fuel_consumption.hist(sharey=True)
```

Now we can see that zeros are much more common on the right.
In fact, zeros are so common in both variables that the shape of the distribution over the rest of the values is difficult to see.
We can sacrifice some detail at the top of the y axis in exchange for greater detail at the bottom of the y axis by switching the y axis to log scale.

```python
elec_fuel_consumption_cols = ["elec_fuel_consumption_mmbtu","electric_fuel_consumption_quantity"]
elec_fuel_consumption = pr_gen_fuel_annual[elec_fuel_consumption_cols]
elec_fuel_consumption.hist(sharey=True, log="y")
```

This refinement was more of a tradeoff.
The differences in frequencies for the bins above zero is now more clear,
but the zero bin looks more similar.
We can turn off log scale until we have a question that needs more detailed comparison of the bins above zero.

Finally let's make use of this empty space to the right of the plot.
The default plot width is quite narrow.
To widen it, we will use the following incantation:

```python
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10, 4]
```

This sets the default figure size to 10 inches wide and 4 inches tall.
You can use whatever default size makes sense for your monitor.

Back to our question: why does `_quantity` have so many more zeros than `_mmbtu`?

The easiest explanation would be if one of our categorical variables could identify a group that behaved wildly differently in `_quantity` than it did in `_mmbtu`.

Let's check one categorical variable together.

We can use a for loop to plot each group from `associated_combined_heat_power`:

```python
for gr, df in pr_gen_fuel_annual.groupby("associated_combined_heat_power"):
    axs = df.hist(column=elec_fuel_consumption_cols, sharey=True)
```

That gave us one row for each value of `associated_combined_heat_power`, but it hasn't told us which value goes with which row.
That's confusing.
Let's add some labels using the `legend()` function:

```python
for gr, df in pr_gen_fuel_annual.groupby("associated_combined_heat_power"):
    axs = df.hist(column=elec_fuel_consumption_cols, sharey=True)
    axs[-1][-1].legend([f"associated_combined_heat_power: {gr}"])
```

Okay, so the first row is for `associated_combined_heat_power` No and the second row is for `associated_combined_heat_power` Yes.
These show some slight differences, particularly for the Yes group, but nothing overwhelmingly convincing.
Ideally we would want to see a group that had some nonzero bins for `mmbtu`, but only the zero bin for `quantity`.
We can mark `associated_combined_heat_power` as a "maybe" for helping explain our question.

:::: challenge

Now it's your turn.
Find a categorical column that seems to explain why there are so many more zeros in `quantity` than in `mmbtu`.

:::::::: solution

```python
for gr, df in pr_gen_fuel_annual.groupby("energy_source_code"):
    axs = df.hist(column=elec_fuel_consumption_cols, sharey=True)
    axs[-1][-1].legend([gr])
```

* SUN, WAT, and WND _always_ have zero `quantity`.
  You can kinda guess from the codes themselves, or look them up in the File Layout documentation ("Reported Fuel Type Code"), but these are the energy source codes for solar (SUN), hydro (WAT), and wind (WND) power.
  Which kinda makes sense, if we're trying to measure a "quantity of fuel consumed".
  How many units of sun did we burn today at the power plant?
  How about wind? ... water?
  It doesn't explain why `mmbtu` for renewables is nonzero, but it's something!
* Bonus confidence: the other energy source codes have _excellent_ matching between `quantity` and `mmbtu`.
* Bonus puzzle: MWH always has zero `mmbtu`! How odd.

Honorable mentions:

* `prime_mover` shows moderate differences for BA, CT, and ST as well as the overwhelming differences for HY, PV, and WT.
  If you're a little more endowed with domain knowledge (or handy with the File Layout documentation, "Reported Primer[sic] Mover") you may notice that these are the prime mover codes for hydro (HY), photovoltaic (PV), and wind turbines (WT), which line up exactly with the WAT, SUN, and WND energy source codes.
  The only reason this wasn't my top choice for the solution is because this dataset covers 8 energy source codes and 9 prime mover codes.
* `fuel_unit` shows suspicious differences for megawatthours, though it's in the opposite direction
* `reporting_frequency_code` shows suspicious differences for AM, but that only covers ~10 respondents, and our discrepancy is more like 50.
* `data_maturity` shows mild differences for incremental_ytd

Alternate approach: use boxplots

```python
axs=pr_gen_fuel_annual.groupby("energy_source_code")[elec_fuel_consumption_cols].plot.box(
    label="energy_source_code")
for i, ax in zip(axs.index, axs.values):
    ax.legend([i])
```

::::::::

::::

So now we know to stick to mmbtus if we want to capture renewables.

Splitting off the numerical measurement data got us through another 5 columns.
Using this approach, we found out that renewables are handled oddly in the `fuel_consumption` columns:
For solar, wind, and hydro, all the useful data are in `_mmbtu`, and for battery storage, they're all in `_quantity`.
If our research relies on fuel consumption figures, we'll need to either exclude renewables from our analyses, or treat them separately.

The remaining 8 columns are 7 identifiers and the report year.
We got through a 24-column table of annual data from EIA 923 in Puerto Rico, and we know something about the index columns, string categorical columns, and numeric measurement columns.
That's a significant step in getting familiar with this dataset!

## Monthly data

Now let's look at the monthly data.

```python
pr_gen_fuel_monthly = pd.read_parquet("../data/pr_gen_fuel_monthly.parquet")
pr_gen_fuel_monthly
```

Most of these variables are time series, and that lends itself to plotting especially well.

Most people are familiar with putting plots in research papers, reports, and slides, where they're useful as evidence supporting your argument. To be effective, those plots need to -- essentially -- look nice: clear labels and titles, appropriate units and limits, good color separation for print or screen, tidy legends, minimizing extraneous data. The goal is to communicate your point.

When you're in the exploratory phase, you don't know what the point is yet, and you're communicating with yourself, now and future-you. To be effective, exploratory plots need to tell you something you don't already know, and ideally they should do that quickly, so you don't lose track of what you're doing. We can skip a lot of the presentation refinements, so long as a plot is not _actively confusing_.

Pandas has great support for exploratory plotting, since it doesn't require much extra setup, and the options for presentation refinements are extremely limited, reducing the risk of going down pixel-perfection rabbit holes.

In the last section, we started to establish a rhythm for exploratory data visualization.
Let's break that out more explicitly.
The steps are:

1. Decide what we want to see
1. Get pandas/matplotlib to show it to us
1. If what we want to see is too hard to see, refine the plot
1. Make a note of anything surprising or weird for followup

Let's look at all the monthly variables at once.

What do we want to see?

* a different line for each variable: fuel consumed for electricity, fuel consumed, fuel mmbtu, and net generation
* one value for each month -- we'll sum across all the plants

Now let's get pandas to show it to us.

The primary key or index columns for this data frame are the month ("date"), plant id, plant name, prime mover, and energy source code.

```python
monthly_index_columns = [
    "date",
    "plant_id_eia",
    "plant_name_eia",
    "prime_mover_code",
    "energy_source_code",
    "fuel_unit",
]
```

We want one value for each month, so we'll group by date and then sum.

```python
pr_gen_fuel_monthly
pr_gen_fuel_monthly.groupby("date").sum()
```

When we sum on some of the index columns, we make a huge mess!
Let's move the index columns to the actual index; then pandas won't sum them.

```python
pr_gen_fuel_monthly.set_index(monthly_index_columns).groupby("date").sum()
```

Much better. Now plot!

```python
pr_gen_fuel_monthly.set_index(monthly_index_columns).groupby("date").sum().plot()
```

Check: can we see a different line for each variable, and one value per month? Yes.

Things to notice:

* Big zero spike in late 2017, all variables
* Everything drops to zero after early 2025; that's probably the end of the real data
* Variables are on vastly different scales but pandas did its best and it's okay

Let's dive in further. What's the energy source breakdown look like throughout the year?

What do we want to see?

* a different line for each energy source: CFO, SUN, NG, etc
* just fuel consumed mmbtus; we'll lose battery storage but get to see solar, hydro, and wind
* one value for each month -- we'll sum across all the plants

Now let's get pandas to show it to us.

```python
(
    pr_gen_fuel_monthly
    .groupby(["energy_source_code", "date"])
    .fuel_consumed_mmbtu.sum()
    .unstack("energy_source_code").plot()
)
```

Check: does this show us the lines we want?
Yes, though it's pretty busy.
We may need to split it up to see some elements more clearly.

::: challenge

What do you notice?

:::: solution

* Zero spike in 2017 visible in all energy sources but recovery severely delayed for BIT and renewables
* NG another big drop in late 2019/early 2020; again in late 2021. Independent of other energy sources though.
* RFO also seems to vary quite a lot; also not related to other energy sources.
* Renewables way smaller than others
* Renewables all drop starting in 2022

::::

:::

Let's put the renewables on their own plot so we can see them better.

```python
renewables = ["SUN", "WND", "WAT"]
(
    pr_gen_fuel_monthly
    .loc[pr_gen_fuel_monthly.energy_source_code.isin(renewables)]
    .groupby(["energy_source_code", "date"])
    .fuel_consumed_mmbtu.sum()
    .unstack("energy_source_code").plot()
)
```

Okay, yes, that is dramatic.
We can also see that hydro spends a lot of time offline.
Sufficiently so that we can't really see if it's affected by whatever has happened in 2022.

Does this 2022 event show up in the net generation as well?

:::: challenge

Adapt our current fuel_consumed_mmbtu plot to show net_generation instead.

:::::::: solution

```python
(
    pr_gen_fuel_monthly.set_index("energy_source_code").loc[renewables].reset_index()
    .groupby(["energy_source_code", "date"]).sum()
    .net_generation_mwh.unstack("energy_source_code").plot()
)
```

No, not really :(

::::::::

:::

Okay, what else could it be? Maybe a big renewables plant opened or closed that did things differently than the others? Let's look for patterns or clusters in the relationship between net generation and fuel consumed mmbtus for renewables.

What do we want to see?

* a scatter plot with one point for each row
* net generation on the x axis
* fuel consumed on the y axis

Now let's get pandas to show it to us.

```python
renewables_monthly = pr_gen_fuel_monthly.loc[pr_gen_fuel_monthly.energy_source_code.isin(renewables)]
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu")
)
```

Check: does this show us a scatter plot with netgen on the x and fuel consumed on the y?
Yes, and we can even see there are at least two distinct patterns.
It's pretty blobular though, and that makes it tough to see whether there are only two or if more are hiding here in this top one.
This is an appropriate time for refinement: the current graph settings aren't giving us all the information we want.

We can reduce the size of each point to see if that gives us clearer separation.

```python
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.5)
)
```

Is that three lines? Three lines for three energy sources is awfully suspicious.

This is another appropriate time for refinement: we can add color to show whether each line is for a different energy source.

```python
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.1, c="energy_source_code")
)
```

oh gee thanks pandas, the default colormap is grayscale. That's not helping at all.

```python
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.1, c="energy_source_code", colormap="rainbow")
)
```

Oh do not like that.
Instead of each line a different color, there are colors for all three energy sources on all the lines.
So energy source code does not explain what's going on here.

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

But at least it clearly identifies three lines. This feels like a policy change effect -- a coordinated change throughout Puerto Rico in how fuel consumption is reported for renewables (which as we know from the annual data, is already pretty weird).

:::::::

::::

We've probably extracted all the information we can out of this plot.
Sometimes viewing the same data from another angle can reveal further insights.
Let's try that now: What are the slopes of these lines?


Fuel consumed per MWH generated is the heat rate, and we can compute that directly:

```python
(
    renewables_monthly
    .assign(heat_rate=renewables_monthly.fuel_consumed_mmbtu/renewables_monthly.net_generation_mwh)
    .plot.scatter(x="date", y="heat_rate", s=0.5, c="date", colormap="rainbow")
)
```

Oh hey, more subtle than we thought.
It looks like whatever constant everyone was using to compute fuel consumption changed a little bit each year, with a big gap for Maria, and then suddenly decided once and for all in 2022.


:::: callout

This was a real policy change, and it affected more than Puerto Rico!

Starting in 2023 (in which reports on 2022 data were published), the EIA changed how it assesses noncombustible renewable energy contributions.
The old way used a fossil fuel equivalency approach and was adjusted each year using an average heat rate;
the new way uses a captured energy approach and uses a constant heat conversion factor.

For more information, see this [CleanEnergyTransition explainer](https://www.cleanenergytransition.org/post/understanding-how-the-eia-is-measuring-noncombustible-renewables?u).

::::

The colormap made it easy to see how the different heatrate values corresponded to our line chart from before, but it's making these little stragglers hard to see.
Now that we have established some continuity from the previous plot, we can drop the colormap and focus on the stragglers.

```python
(
    renewables_monthly
    .assign(heat_rate=renewables_monthly.fuel_consumed_mmbtu/renewables_monthly.net_generation_mwh)
    .plot.scatter(x="date", y="heat_rate", s=0.5)
)
```

Are those individual plants or some other effect?

```python
(
    renewables_monthly
    .assign(heat_rate=renewables_monthly.fuel_consumed_mmbtu/renewables_monthly.net_generation_mwh)
    .assign(plant_factor=renewables_monthly.plant_name_eia.astype("category"))
    .plot.scatter(x="date", y="heat_rate", s=0.5, c="plant_factor", colormap="rainbow")
)
```

This colormap is a little too squished to tell us exactly which plant is the troublemaker, but it does give us enough to suggest that it's only one or two plants.
If we wanted to figure out exactly which ones, we could split the data by year, use `.describe()` to get the median ratio for each year, then select all the rows that had a different ratio.
We'll leave that for future research!

In the meantime, let's review:
We were able to use timeseries plots to identify a weird effect in the data, and then use two other visualizations to narrow down the cause and extent of the weirdness.
We now know that any models that make use of fuel consumed or heat rate will need to account for the changes in how renewables were handled in pre- and post-2022 data.
Any models that compare or rely on differences in heat rates between plants will probably need to exclude renewables entirely.


::::::::::::::::::::::::::::::::::::: keypoints

- If you are struggling with how to start acquainting yourself with a new data set, looking for data gremlins can be a good icebreaker.
- Different kinds of data -- indexing, categorical, numeric, time series -- are suited to different kinds of summarization.
- Use divide-and-conquer strategies when working with tables that have a lot of columns (common in energy data).
- Visualization is not just for reports, papers, and talks! If you incorporate plotting into your exploration & troubleshooting toolbox you'll be able to identify and diagnose data problems much more quickly than if you wait for your model to exhibit strange behavior.

::::::::::::::::::::::::::::::::::::::::::::::::
