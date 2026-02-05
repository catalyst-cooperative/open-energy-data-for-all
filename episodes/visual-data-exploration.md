---
title: "Visual Data Exploration"
teaching: 75
exercises: 35
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I get ready to do research with data that is new to me?
- What should I do when I find something that doesn't look right?
- How can I get a head start on identifying data problems that might cause headaches later?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Identify a primary key and explain its significance
- Examine data for anomalies using summarization and visualization
- Articulate the difference between refining plots for exploration and refining plots for presentation
- Execute a repeatable strategy for locating the cause and extent of anomalies

::::::::::::::::::::::::::::::::::::::::::::::::

:::: instructor

Prep:

* Start a spreadsheet application but do not open anything in it yet
* Share whole screen or screen region with the following (overlapping is fine):

  * Web browser with slides for the intro
  * Terminal window open to the course repo
  * File browser open to the course repo

* Unshared screen or region:

  * Course website instructor view or raw episode file

* Adapt intro to whether workshop is part of the full series or running
  as part of the VisEx+Assumptions standalone.

* Setup instructions: https://docs.catalyst.coop/open-energy-data-for-all/index.html#setup
* GitHub repo: https://github.com/catalyst-cooperative/open-energy-data-for-all/
* Course website: https://docs.catalyst.coop/open-energy-data-for-all/visual-data-exploration.html
::::

Now that you have some raw data, how do you get from there to actually doing research with it?

Maybe you already have a research question;
how do you get your data into a form that can help you answer it?
How do you know your data doesn't have gremlins hiding in it that will mess up your research?

In this session we will do some initial data explorations and develop strategies for identifying and diagnosing sneaky data problems
-- including the use of data visualization as part of your exploration toolkit.
Plots aren't just for papers!

## What kinds of data problems are common in energy data?

Data problems come in many different forms:

* **Problems introduced by the respondent,** such as typos and other data entry errors.
* **Problems introduced by the data aggregator,** such as confusing or inconsistent documentation,
  or a bad choice of data format that doesn't preserve relationships within the data.
* **"Problems" introduced by external forces,** such as natural disasters and policy change.

Data problems can occur in a single column, or in the relationship between columns, or even in the relationship between tables.

How you respond to them will depend on the source of the problem
and what kind of impact it will have on the kinds of modeling and analysis you want to do.
For example,

* Simple typos can often be fixed, but if the correct values can't be reconstructed,
  you may need to exclude the affected rows from your analysis.
* If the data doesn't seem to match the documentation published with it,
  you can sometimes track down the instructions respondents were given
  and use that to work out what's supposed to be there.
* Irregular data from a natural disaster may be exactly what you're studying,
  but might need to be excluded from analyses focused on steady-state behavior.

## What is a good general strategy for finding problems in unfamiliar data?

Data problems aren't always obvious. To uncover them, we will need to go looking for them.

There is a pattern to this:

* Carve off a chunk of data small enough to reason about
* Identify what we expect to see from that data
* Check whether that is actually true or not
* Justify or explain any differences between what we expect and what is actually there

When we first start out, our expectations will be quite general, often based on data type --
whether the data is numeric, categorical, or free text.
As we become more familiar with the data, our expectations will become more sophisticated.
Sometimes the data defies our expectations in ways that reveal new research questions.
Keep an open mind, and be sure to leave yourself good notes as you go!

## Put it into practice

Let's take a look at how these ideas apply to real data.
We'll build up some practice with our problem-hunting strategy by starting with summary statistics.
Then once the strategy feels comfortable, we'll bring in visualization.

Fire up Jupyter notebook:

```bash
$ uv run jupyter notebook
```

& open `notebooks/5-visual-data-exploration.ipynb`

We'll be looking at form EIA-923, which records electricity generation and fuel consumption for power plants that serve the United States.

You have a raw file for EIA-923 data from Puerto Rico, and a processed file which was prepared by your predecessor.
The paths are already in the notebook for you:

```python
raw_file = "../data/raw_eia923__puerto_rico_generation_fuel.parquet"
monthly_file = "../data/pr_gen_fuel_monthly.parquet"
```

We will ask ourselves:

* What kinds of data are there? Can I look at just one kind at a time?
* What do I expect to see from this data?
* What do I actually see?
* Can I justify or explain any differences between what I expect and what I actually see?

### Primary keys

Let's load the processed file and see what's in there.

```python
import pandas as pd
pr_gen_fuel_monthly = pd.read_parquet(monthly_file)
pr_gen_fuel_monthly
```

EIA-923 records fuel consumption and electricity generation over time.
To better reason about this data frame, it is important to identify its **primary key**:
What columns, taken together, uniquely identify each row of data?
What does each row represent?

If we were familiar with EIA-923 from other research, we might know that already.
If not, we can check the dataset documentation.

The EIA website is a good place to check first for all EIA forms.
[The page for Form EIA-923](https://www.eia.gov/electricity/data/eia923/) has a summary that hints at the primary key:

![Screenshot from the page for Form EIA-923](fig/ep-5/eia923-website-summary.png){alt="Screenshot from the page for Form EIA-923. The text 'at the power plant and prime mover level' is highlighted. The full text reads, 'The survey Form EIA-923 collects detailed electric power data — monthly and annually — on electricity generation, fuel consumption, fossil fuel stocks, and receipts at the power plant and prime mover level. Specific survey information provided...'"}

The documentation suggests a primary key that includes:
the date ("monthly and annually" implies a time series), power plant identifiers, and prime mover.
Sometimes documentation is incomplete, so it's always good to double check.

We can use our problem-hunting strategy to do so.
First, we'll grab just the columns we think define the primary key.

```python
# carve off a chunk: what is the primary key?
#    maybe: plant ids, prime mover, and date
primary_key_columns = ["plant_id_eia", "plant_name_eia", "prime_mover_code", "date"]
pr_gen_fuel_monthly[primary_key_columns]
```

Next, identify what we expect.
For a primary key to do its job, it needs to be unique from row to row.
We expect each set of plant id, name, prime mover, and date values in the data frame to only appear once.

```python
# what do we expect: each set of values only occurs once
```

Now we need to check whether our expectation is true in the data.
There are lots of ways we could do that.
`.value_counts()` is a great function for this situation -- it works on single columns, but also on multiple columns taken together.

```python
# what do we expect: each set of values only occurs once
# check whether that's actually true: use value_counts
pr_gen_fuel_monthly[primary_key_columns].value_counts()
```

This tells us that the combination ID 61147, name Costa Sur Plant, prime mover ST, and date 2017-11-01 occurs twice in the data frame.
Not ideal.
Let's see if we can justify that.
Is this a case of a few isolated problems, or a systemic problem, or is our guess at the primary key just wrong?

The output also tells us there are 4504 unique values for our candidate primary key.
We can see there are at least 5 keys that occur more than once.
How common is the duplication?
If there are really only 5 duplicates, it could be a few isolated problems.
If it's significantly more than that, we would start looking at our primary key with suspicion.

Let's filter for just the keys that occur more than once, and see how many there are.

```python
# explain the differences: how many duplicates are there?
pk_sizes = pr_gen_fuel_monthly[primary_key_columns].value_counts()
pk_sizes.loc[pk_sizes>1]
```

554 duplicates out of that 4504... so more than 10 percent.
That's either a massively systemic problem, or there's one or more columns we need to add to our primary key to distinguish between duplicate rows.

::: challenge

Look at one of the duplicate entries and propose another column to add to our primary key.

:::: hint

Use `.loc` to grab the data for one of the duplicate keys.
Are there any columns, other than the measurement columns, that differ between the two entries?

```python
pr_gen_fuel_monthly.loc[
    (pr_gen_fuel_monthly.plant_id_eia == 61147) &
    (pr_gen_fuel_monthly.plant_name_eia == "Costa Sur Plant") &
    (pr_gen_fuel_monthly.prime_mover_code == "ST") &
    (pr_gen_fuel_monthly.date == "2017-11-01")
]
```

::::

:::: solution

If we add `energy_source_code` to our primary key, there are no more duplicates: we uniquely identify all rows.

```python
primary_key_columns = ["plant_id_eia", "plant_name_eia", "prime_mover_code", "energy_source_code", "date"]
pk_sizes = pr_gen_fuel_monthly[primary_key_columns].value_counts()
pk_sizes.loc[pk_sizes>1]
```

::::
:::

We have our primary key!
How does this help us?

* Before, we didn't really know what each measurement corresponded to.
  Fuel consumed, sure, but consumed by what?
  an entire power plant? a single generator?
  Now we know exactly how everything is aggregated.
* Because each key only appears once, we know that each
  (plant, prime mover, energy source) combination
  yields a single time series --
  a log of fuel consumption and electricity generation, with only one point for each month.

Since this was annoying to figure out, we should make a note of how we got here.
If we have to put this project down for a while,
future-us will appreciate being able to get a jumpstart when we pick it back up.

```python
# you need *both* prime mover and energy source, because
# prime mover isn't enough to uniquely identify each record on its own
primary_key_columns = ["plant_id_eia", "plant_name_eia", "prime_mover_code", "energy_source_code", "date"]
```

### Data types

Now that we've seen one way to summarize primary key information,
let's take a moment to talk about data types.

```python
pr_gen_fuel_monthly.dtypes
```

```output
plant_id_eia                                    Int64
plant_name_eia                         string[python]
prime_mover_code                             category
energy_source_code                           category
fuel_consumed_for_electricity_mmbtu           float64
fuel_consumed_mmbtu                           float64
net_generation_mwh                            float64
date                                   datetime64[ns]
dtype: object
```

Primary key columns are often:

* Integers (whole numbers) - used for numeric IDs
* Strings (text) - used for names
* Categories - used for classification among a restricted set of available values
* Dates or times - used for time series records and logs

`.value_counts()` is a good summarization tool for all four of these data types.
We've already seen how we can use it to check our expections of how often a value or set of values appears in the data frame.
It can also be useful at building basic familiarity with the data.

Let's take a closer look at `energy_source_code` as an example.
We can use `.value_counts()` to quickly see what values appear in the column.

```python
# carve off a chunk: just energy_source_code
# what we expect: ...learning
pr_gen_fuel_monthly.energy_source_code.value_counts()
```

```output
energy_source_code
distillate_fuel_oil    2104
solar                  1148
residual_fuel_oil       548
natural_gas             538
electricity_storage     268
wind                    184
water                   170
bituminous_coal          98
Name: count, dtype: int64
```

In this case there are a handful of different possible energy sources.

The frequency information in `.value_counts()` output can also help us become more familiar with the data.
Even without looking at the fuel consumed and electricity generated, it can help us start to understand the shape of the energy system in Puerto Rico.

What do you notice about the frequency of each energy source?
Does it defy any of your expectations?

::: challenge

Write down three observations about the distribution of energy source codes in the data frame,
whether each seems normal or odd, and why.

:::: hint

* What energy sources appear most frequently? Is that common for energy generation in the U.S.?
* What energy sources appear least frequently? Is that expected?
* What are the most and least common energy sources in the U.S.? Do those generalizations seem to hold in PR?

::::

:::: solution

Here are a few:

* Lots of oil. That's weird; oil is expensive.
* Solar is surprisingly common. Is that weird? solar is growing but like. Not **that** much.
* Wind and hydro are more rare, which seems normal.
* Very few coal entries. Is that expected? Not sure.

Remember though, that these numbers are counting rows of the data frame, not the fuel mix of the grid.
What does each count represent?
From our primary key exploration, we know that each row represents just part of a plant for a particular month.
Each entry counts the same whether it represents a tiny or huge amount of actual generated energy.
What could it mean for an energy source code to have high frequency?

* Many tiny plants
* A smaller number of plants that have operated for a very long time (many months)

We're starting to generate more questions than we can reasonably answer all at once,
so it's a good time to step back and think about where to go next.

```text
- Oil and solar very common
- Coal very rare
- Does the fuel mix of the grid match the distribution of records?
- Are the oil and solar plants tiny but many?
- Are the coal plants huge but few?
```

If we want to explore our expectations about the fuel mix of the grid, we'll need to look at the numeric data.

::::
:::

### Summarizing numeric data

As a first step, let's look again at the data types in our data frame:

```python
pr_gen_fuel_monthly.dtypes
```

```output
plant_id_eia                                    Int64
plant_name_eia                         string[python]
prime_mover_code                             category
energy_source_code                           category
fuel_consumed_for_electricity_mmbtu           float64
fuel_consumed_mmbtu                           float64
net_generation_mwh                            float64
date                                   datetime64[ns]
dtype: object
```

The numeric data we want to look at next are in the columns with `float64` data type.
"Float" is short for "floating point", and basically just means a decimal fraction --
it's how we encode continuous measurements on a computer.

The expectations we have for these values are not particularly sophisticated -- we're just looking for big obvious problems here.

Pandas has some built-in tools for summarizing numeric data like this.

```python
# carve off a chunk: fuel consumption continuous measurement columns only
# what we expect: basic good behavior
# check: use .describe()
pr_gen_fuel_monthly[[
    "fuel_consumed_for_electricity_mmbtu",
    "fuel_consumed_mmbtu",
]].describe()
```

```output
fuel_consumed_for_electricity_mmbtu	fuel_consumed_mmbtu
count	4.948000e+03	4.948000e+03
mean	2.880679e+05	2.912271e+05
std	7.149827e+05	7.187600e+05
min	0.000000e+00	0.000000e+00
25%	0.000000e+00	0.000000e+00
50%	2.904000e+03	2.985500e+03
75%	5.604050e+04	5.612400e+04
max	4.701353e+06	4.701353e+06
```

For each column, we get a stack of summary statistics.

* count: the number of non-null values in the column.
  If this is less than the length of the data frame, we know there are nulls in the column.
* mean, std: the average and standard deviation,
  establishing the center and spread of the distribution of values in the column.
* min, 25-75%, max: the quartiles for the distribution.
  Min and Max can tell you about outliers,
  and the difference between the 50th percentile and the Mean can tell you about skew.

For count, let's check the length of the data frame.

```python
len(pr_gen_fuel_monthly)
```

```output
5058
```

Okay, so we've got ~100 nulls in these columns, or 2%.
Both columns have the same number of nulls,
so it's likely that the nulls occur in the same places in both columns.
This is not a big problem; we'll just need to keep in mind that not every record has a proper value,
and some pandas functions will drop those records automatically.

The means look basically plausible, in that they're positive and large enough to believably support a few million people (if less than in the rest of the U.S.).

The standard deviations seem a bit big, since they're larger than the means.

The suspiciously large spread is confirmed in the quartiles.
These columns are more than 1/4 zeros,
which means the outliers at the other extreme have to be really huge in order to push the mean up as high as it is.
So we know fuel consumption is dominated by a few really heavy users.

```python
# what we found: some nulls; large standard deviations; quartiles show a ton of skew
# explain why: mostly small producers with some huge ones dominating overall fuel consumption
# bonus expectation update: patterns we found in record counts unlikely to be reproduced in the actual fuel mix
```

### Visualizing numeric data

To learn more about the actual fuel mix and generation in PR,
we can bring in the the `date` column and start looking at these measurements as time series.
Time series data lends itself to plotting especially well!

Most people are familiar with putting plots in reports, research papers, and presentation slides,
where they are useful as evidence supporting your argument.
To be effective, presentation plots need to -- essentially -- look nice:

* clear labels and titles,
* appropriate units and limits,
* good color separation for print or screen,
* tidy legends,
* minimizing extraneous data.

The goal of presentation plotting is to communicate your point.

When you're in the exploratory phase, you don't know what the point is yet,
and you're communicating with yourself, now and future-you.
To be effective, exploratory plots need to:

* tell you something you don't already know,
* do it quickly, so you don't lose track of what you're doing.

In exploratory plotting, we can skip a lot of the presentation refinements,
so long as a plot is not _actively confusing_.

Pandas has great support for exploratory plotting, since it doesn't require much extra setup,
and the options for presentation refinements are extremely limited,
reducing the risk of going down pixel-perfection rabbit holes.

We already have a solid strategy for identifying data problems:

* Carve off a chunk of data small enough to reason about
* Identify what we expect to see in the data
* Check whether that is actually true
* Justify or explain any differences

Exploratory visualization helps us check whether our expectations are actually true,
but sometimes it can take a few steps to get from the data we have to something we can plot.
We then have to decide whether our plot is showing us enough information to actually check the data,
or if the plot needs a refinement or two to show us everything we need.

Let's look at an example.

#### Plot all monthly variables

Let's look at all the monthly variables at once, for a big-picture look at the energy generated in Puerto Rico as a whole.

```python
# carve off a chunk: monthly fuel consumed and net generation for all of Puerto Rico
# (sum over all plants)
# what we expect:
# some kind of annual cycle
# maybe increasing slowly?
```

How do we check this?
If we were limited to tables and formulas, it would be a huge pain,
but with visualization, we'll be able to get there significantly quicker.
What needs to be in our plot?

* a different line for each variable
* one value for each month -- we'll sum across all the plants

Now let's get pandas to show it to us.

We want one value for each month, so we'll group by date and then sum.

```
pr_gen_fuel_monthly.groupby("date").sum()
```

```output
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[35], line 1
----> 1 pr_gen_fuel_monthly.groupby("date").sum()
[...]
2723     # raise TypeError instead of NotImplementedError to ensure we
2724     #  don't go down a group-by-group path, since in the empty-groups
2725     #  case that would fail to raise
2726     raise TypeError(f"Cannot perform {how} with non-ordered Categorical")

TypeError: category type does not support sum operations
```

Oh no! We can't sum a category column.

```python
pr_gen_fuel_monthly.dtypes
```

```output
plant_id_eia                                    Int64
plant_name_eia                         string[python]
prime_mover_code                             category
energy_source_code                           category
fuel_consumed_for_electricity_mmbtu           float64
fuel_consumed_mmbtu                           float64
net_generation_mwh                            float64
date                                   datetime64[ns]
dtype: object
```

`.sum()` told it to sum all the columns, but we only want to sum the measurement columns,
and leave the primary key columns alone.
There are lots of ways to tell pandas to do this,
but the one I want to show you to day is to set an index:

```python
pr_gen_fuel_monthly.set_index(primary_key_columns).groupby("date").sum()
```

An index is a little more general than a primary key, because it doesn't have to be unique.
An index is useful any time you want to hold some columns aside from the measurement columns you want to do math with,
or any time you want to designate certain columns for quickly selecting blocks of rows in your data frame.

But our sum is looking much better. Now plot!

```python
pr_gen_fuel_monthly.set_index(primary_key_columns).groupby("date").sum().plot()
```

Check: does this plot show us everything we need from it?
Can we see a different line for each variable, and one value per month? Yes.

Does it help us see whether what we expected to find is actually true?

Are there any surprises?
Does the plot make anything visible that we didn't even think to list as an expectation?

```python
# what we found:
# annual cycle: yes
# slowly increasing: no, mostly the same
# surprises: big zero spike in late 2017
# can we explain it? hurricane Maria
```

Recall that one of the kinds of problems we are hunting for comes from
_external_ forces, like natural disasters -- this one had quite an effect!
If we make a note of the approximate scope of the affected data,
we'll be able to focus on it or hold it out from our research models later.

```text
# NB Hurricane Maria data extends from late 2017 to early 2019.
```

#### Compare energy source breakdown over time

Let's dive in further and look at the actual fuel mix of the grid.
What does the energy source breakdown look like over time?

Restart the cycle again.

```python
# carve off a chunk: fuel consumed, by energy source, for all of PR
# what we expect:
# does it match record mix? high oil, high-ish solar, low coal
```

How do we check this?
What needs to be in our plot?

* just fuel consumed mmbtus
* a different line for each energy source: `distillate_fuel_oil`, `solar`, `natural_gas`, etc
* one value for each month -- we'll sum across all the plants

Now let's get pandas to show it to us.
To get `.plot()` to show the lines we want, we'll need to make one column for each energy source,
where each row is the sum for one month.

```python
(
    pr_gen_fuel_monthly
    .groupby(["energy_source_code", "date"], observed=True)
    .fuel_consumed_mmbtu.sum()
    .unstack("energy_source_code").plot()
)
```

::: instructor

`unstack` is a bit of a brain warp, so take extra time here to check that students are with you.

:::

Check: does this plot show us everything we need from it?
Do we have a line for each energy source, and one value per month?
Yes, though it's pretty busy.
We may need to split it up to see some elements more clearly.

::: challenge

Use this plot to determine whether what we expected to find is actually true.
How does the fuel mix of the grid compare with the frequency of different energy source codes we found in the data frame?

Are there any surprises?

:::: hint

Recall that we found the distribution of energy source codes in the data frame using `.value_counts()`:

```python
pr_gen_fuel_monthly.energy_source_code.value_counts()
```

Recall that overall fuel consumed and net generation took a big hit in late 2017 due to hurricane Maria.
Would we expect all plants to take the same amount of time to come back online after an event like that,
or are some energy sources more difficult to bring back up than others?

A sudden drop that never comes back up is often a sign of a potential data problem.
Do all the drops that appear in this plot recover,
or do some of them continue for long periods of time?
::::

:::: solution

```python
# what we found:
# oil high? yes
# solar high-ish? no, very low
# coal low? no, medium
# surprises:
# NG about as high as oil! & seem to trade off on >1yr timescales, maybe based on price?
# Maria affects all energy sources, but coal and renewables take a long time to recover
# Speaking of: what does "fuel consumed" even mean for renewables?
# And why do all renewables drop suddenly in 2022 and never come back?
```

Some of these point not to data problems, but to possible research questions:

```text
Potential research projects
- Do oil and ng trade off dominance due to price or some other factor?
- Hurricane recovery differs by energy source
```

::::

:::

Our first priority though is problem-hunting,
and that suggests we focus on places where data might be missing or misplaced.

That makes the drop in renewables in 2022 incredibly suspicious.
The line we made is a sum, so a big sustained drop like that could mean
that a bunch of different plants stopped getting tracked properly.
That could definitely affect any research we'd do with this data.
We should investigate further.

#### Focus on renewables

This is an appropriate time for refinement: the current graph settings aren't giving us enough detail on the renewable energy sources.

Let's put the renewables on their own plot so we can see them better.

```python
renewables = ["solar", "wind", "water"]
(
    pr_gen_fuel_monthly
    .loc[pr_gen_fuel_monthly.energy_source_code.isin(renewables)]
    .groupby(["energy_source_code", "date"], observed=True)
    .fuel_consumed_mmbtu.sum()
    .unstack("energy_source_code").plot()
)
```

Okay, yes, that is dramatic.
We can also see that hydro spends a lot of time offline.
Sufficiently so that we can't really see if it's affected by whatever has happened in 2022.

Does this 2022 event show up in the net generation as well?

<!-- consider refreshing the cycle here; we have a new hypothesis. -->

:::: challenge

Adapt our current fuel_consumed_mmbtu plot to show net_generation instead.

:::::::: solution

```python
# carve off a chunk: net generation, by energy source, renewables only
# what we expect: maybe also drops in 2022?
(
    pr_gen_fuel_monthly
    .loc[pr_gen_fuel_monthly.energy_source_code.isin(renewables)]
    .groupby(["energy_source_code", "date"], observed=True)
    .net_generation_mwh.sum()
    .unstack("energy_source_code").plot()
)
```

No, not really :(

```python
# what we found: no
# explain why: ???
```

::::::::

:::

#### Try a scatter plot

Okay, what else could it be?
Maybe a big renewables plant opened or closed that did things differently than the others?
Let's look for patterns or clusters in the relationship between net generation and fuel consumed mmbtus for renewables.

```python
# carve off a chunk: netgen and fuel consumed for renewables
# what we expect: ? some factor that explains fuel drop in 2022
```

What could help us check this?
Scatter plots are great for any time you suspect you have multiple distinct behaviors in your data.
If we make a scatter plot of net generation against fuel consumed,
and we get clear separation between groups of points,
then identifying what each group has in common could help explain this fuel drop.

What needs to be in our plot?

* one point for each row, renewables only
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

Is that three lines?
Three lines for three energy sources?
Awfully suspicious.

This is another appropriate time for refinement: we can add color to show whether each line is for a different energy source.

```python
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.1, c="energy_source_code")
)
```

oh gee thanks pandas, the default colormap is grayscale.
That's not helping at all.

```python
(
    renewables_monthly.plot
    .scatter(x="net_generation_mwh", y="fuel_consumed_mmbtu", s=0.1, c="energy_source_code", colormap="rainbow")
)
```

Oh do not like that.
Instead of each line a different color, there are colors for all three energy sources on all the lines.
So energy source code does not help us separate the groups we see in this plot.

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

But at least it clearly identifies three lines.
We wanted to know what each group had in common, so that it would help us explain the drop in 2022.
Since the only thing the groups really have in common is date,
this feels like a policy change effect --
a coordinated change throughout Puerto Rico in how fuel consumption is reported for renewables.

```python
# what we found: only date really helps
# explain why: policy change maybe?
```

:::::::

::::

#### Try plotting the heat rate

We've probably extracted all the information we can out of this scatter plot.
Sometimes viewing the same data from another angle can reveal further insights.
Let's try that now: What are the slopes of these lines?

```python
# carve off a chunk: still netgen and fuel consumed for renewables
# what we expect: ? some factor that supports or eliminates the policy change explanation
# how to check: plot slopes of the scatter plot lines, by date
```

Fuel consumed per MWH generated is the heat rate, and we can compute that directly:

```python
(
    renewables_monthly
    .assign(heat_rate=renewables_monthly.fuel_consumed_mmbtu/renewables_monthly.net_generation_mwh)
    .plot.scatter(x="date", y="heat_rate", s=0.5, c="date", colormap="rainbow")
)
```

Oh hey, more subtle than we thought.
It looks like whatever constant everyone was using to compute fuel consumption changed a little bit each year,
with a big gap for Maria,
and then suddenly decided once and for all in 2022.


:::: callout

This was a real policy change, and it affected more than Puerto Rico!

Starting in 2023 (in which reports on 2022 data were published),
the EIA changed how it assesses noncombustible renewable energy contributions.
The old way used a fossil fuel equivalency approach and was adjusted each year using an average heat rate;
the new way uses a captured energy approach and uses a constant heat conversion factor.

For more information, see this [CleanEnergyTransition explainer](https://www.cleanenergytransition.org/post/understanding-how-the-eia-is-measuring-noncombustible-renewables?u).

::::

The colormap made it easy to see how the different heatrate values corresponded to our line chart from before,
but it's making these little stragglers hard to see.
Now that we have established some continuity from the previous plot,
we can drop the colormap and focus on the stragglers.

```python
(
    renewables_monthly
    .assign(heat_rate=renewables_monthly.fuel_consumed_mmbtu/renewables_monthly.net_generation_mwh)
    .plot.scatter(x="date", y="heat_rate", s=0.5)
)
```

Are those individual plants or some other effect?
We can color the plot by `plant_name_eia` to find out.
We were able to use `energy_source_code` to color the plot before because it had a category dtype,
but `plant_name_eia` is just a string, so we have to convert it first:

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

- We were able to use timeseries plots to identify a weird effect in the data, and then use two other visualizations to narrow down the cause and extent of the weirdness.
- We now know that any models that make use of fuel consumed or heat rate will need to account for the changes in how renewables were handled in pre- and post-2022 data.
- Any models that compare or rely on differences in heat rates between plants will probably need to exclude renewables entirely.

Let's take some notes for ourselves so we can pick this back up later:

```text
# Renewables drop suddenly in 2022 and stay low -- probably a policy change:
# - Renewables all show same heat rate, updated each year, then constant starting 2022
# - where does this heat rate come from?
# - there are a bunch of stragglers that don't use the common heat rate. maybe exclude those plants or points?
# - definitely exclude renewables from heat rate analyses involving combustibles
```

::::::::::::::::::::::::::::::::::::: keypoints

- Different kinds of data -- indexing, categorical, numeric, time series -- are suited to different kinds of summarization and visualization.
- Successful strategies for assessing data problems alternate between noticing your expectations about the data and checking to see if the data match your expectations -- and sometimes, updating your expectations based on what you find!
- Visualization is not just for reports, papers, and talks! If you incorporate plotting into your exploration & troubleshooting toolbox, you'll be able to identify and diagnose data problems much more quickly than if you wait for your model to exhibit strange behavior.

::::::::::::::::::::::::::::::::::::::::::::::::
