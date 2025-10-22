---
title: "Making assumptions about your data"
teaching: 30
exercises: 20
---

:::: instructor

Prep list:

- [make a Google Doc](https://www.docs.new) that people can put their assumptions in; make it editable by all who have the link
- clean out the example notebook so that you can type everything out again

::::

:::::::::::::::::::::::::::::::::::::: questions

- Exploratory data analysis was fun, but what did I learn?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Articulate assumptions about a dataset
- Programmatically verify those assumptions
- Prioritize which assumptions are worth verifying

::::::::::::::::::::::::::::::::::::::::::::::::

## Intro

As we explore a dataset we naturally start to make assumptions about it.
We also constantly find new evidence that our initial assumptions are incorrect.
We zoom in a little closer to a suspiciously low value,
or we notice that a certain column has more null values than we expected,
or we see that certain values seem to be duplicated in a confusing way,
and suddenly our understanding of the data is irrevocably changed.

This can understandably have impact on your work!
Depending on what you are using the data for,
these shifts will impact your work differently.
Some will not actually affect your output
- maybe you weren't using that column anyways -
but others will mean you have to make changes to your code,
your conclusions,
your methodology section,
or the way you answer a question when presenting at a conference.

It's nice to at least try to see these things coming,
so in this lesson we'll talk about:

* identifying and articulating assumptions about a dataset
* simple tools for testing these assumptions
* prioritizing assumptions for testing

Afterwards, you'll be able to
have your code automatically check that the important assumptions haven't been broken.

While faulty assumptions lurk everywhere,
we'll focus here on assumptions about your *data*.

Speaking of data,
we have a dataset at `data/pr_gen_fuel_monthly.parquet`,
which we'll be using for concrete examples through the rest of the lesson.
It contains fuel consumption and electricity generation information,
split out by generation unit and reported monthly,
for all of Puerto Rico.
This data was collected by the EIA in form EIA 923.

## What is an assumption anyways?

In this context, an *assumption* can be any property you think is true about the data.

Some examples:

- values are reasonable: the reported fuel usage in MMBtu is always non-negative.
- relationships are well-defined: data rows that share the same plant ID correspond to the same plant
- data types are consistent: the "year" column only contains numbers, not words or strings of random characters
- and many more!

The sneakiest assumptions are the ones that are hard to think of.
If they were obvious to you, then you probably were already working around them in some way.
With that in mind, let's try to come up with some assumptions of our own!

:::: challenge

### Challenge: identifying assumptions

Take 5 minutes to list out as many assumptions as you can about the
EIA 923 Puerto Rico data (`pr_gen_fuel_monthly.parquet`) in the [data directory](../data/).

Please put them in the shared Google doc that your instructor prepared for you.
This will serve as a foundation for future challenges in this lesson.

The goal is to get past the obvious ones and start thinking of some un-obvious assumptions -
no need to limit yourself to 'realistic' ones at this stage.

Some prompts to get you started:

* what problems have you run into in previous datasets?
* if you were here for the data exploration episode,
  what are some things you learned about the data then?
* how can I build on others' suggestions in the doc?

When we return, we'll talk about which things worked.

::::

:::: instructor

Some examples, if students are feeling a little quiet:

* the net generation data is actually in MWh and not a mix of units
* the net generation of batteries is strictly less than the fuel consumed in MWh
* the net generation of each individual plant is "reasonable" - i.e. there are no reports of a generator producing more power than the Sun
* the reported dates are all within the last decade
* the fuel mix matches what we know of physical reality
* the total generation matches what we expect for Puerto Rican electricity demand
* all energy source codes correspond to the set in the documentation
* a plant ID corresponds to only one plant name per year
* a given plant ID always corresponds to the same plant name
* plant IDs are distributed in chronological order of construction
* every generator has at least one reporting period for which they have non-zero generation
* electricity generation heat rates are close to known averages for their prime mover / energy source
* if a value is reported, it is correct and reflects reality
* if a generator reports all null values for a specific time period, it was non-operational during that time period; if a generator reports 0 generation for a specific time period, it was operational, but not dispatched

By the end of this we want at least one assumption that fits each of these categories:

* easy to test
* hard to test
* hard to test programmatically, but easy to eyeball
* high impact (probably crashes your system)
* moderate impact (probably makes bad analysis)
* low impact (probably doesn't do anything)
* high likelihood
* low likelihood

::::

## How to test your assumptions

Let's take a look at one of the example assumptions and see how we'd test it:

> the reported fuel consumption in MMBtu is always non-negative.

How would we verify that? We can use an `assert` statement to verify the assumption.

`assert` basically says, "if this next part is True, great! Nothing happens. If it's false, we'll raise an error."

```python
assert 1 == 1
assert 1 == 2
```

We can include a message in the statement as well, to make the error a little nicer:

```python
assert 1 == 2, "Expected 1 to be equal to 2."
```

So let's assert our assumption is true.

```python
# read in the data
monthly_gen_fuel = pd.read_parquet("../data/pr_gen_fuel_monthly.parquet")

# pull out the piece we're interested in
fuel_consumed_mmbtu = monthly_pr_gen_fuel["fuel_consumed_mmbtu"]

# finally make that assertion!
assert (fuel_consumed_mmbtu >= 0).all(), "The reported fuel consumption in MMBtu should be non-negative"
```

Oh no! We find that the assertion is not true!
This is actually pretty common.
Let's dig in to see what's going on.

```python
fuel_consumed_mmbtu[~(fuel_consumed_mmbtu >= 0)]
```

Huh! We get a bunch of not-a-number values.
That is expected, too, so let's tweak our assumption to:
"If fuel consumption in MMBtu is reported at all, it should be non-negative."

```python
assert (fuel_consumed_mmbtu.dropna() >= 0).all(), "If fuel consumption in MMBtu is reported at all, it should be non-negative."
```

Which passes with little fanfare.

## Which assumptions are worth testing?

As we've just seen,
assumptions take some effort to test.
While it's useful to test many assumptions,
the reality is that we have limited time to work on our projects
and need to prioritize the assumptions that are "worth" the investment of testing them.

What makes assumptions worth testing?
Here are three dimensions to consider in a rudimentary prioritization framework:

* How easy it is to test the assumption:
  the less you have to work for this test,
  the more likely it is to be worth it.
* The impact on your code:
  what's the goal of the system you've built up?
  What happens to that goal if your assumption is violated?
* The likelihood the assumption is violated:
  what are some ways this could go wrong?
  Do they feel plausible or implausible?

Some examples:

* the reported fuel consumption in MMBtu is always non-negative
  * pretty easy to test - we didn't have to do *too* much work above
  * moderate impact - though this depends on the goals of my system,
    if I do any analysis that touches the negative fuel consumption
    I will probably end up with numbers that are off in some way.
  * high likelihood - all it takes is a typo, which happens all the time.

* NA values reflect periods of inactivity for the generator
  * quite hard to test - we would have to find another source for month-to-month generator activity status and then cross-reference.
  * high impact - assuming we're looking at any subset of the data that includes NA values,
    if those don't actually correspond to the activity of the generator we are going to be heavily misled.
  * moderate likelihood - it seems easy for some plant administrator to just forget to report data for a month or two,
    but there's likely *some* enforcement from the EIA.

* there is at least one row of data in the report
  * easy to test!
  * high impact - any cleaning and analysis requires data to work on
  * moderate likelihood - some file transfer failure could easily make this fail.

:::: challenge

### Challenge: prioritizing assumptions

Now it's time to try out that prioritization framework!

Let's start by looking at the list of assumptions we came up with.

Take a few minutes to put a `+` next to 3-5 assumptions that feel important to test.

We'll then discuss a few assumptions with many `+`s and how they fit into the framework above.

::::

:::: challenge

### Challenge: testing an assumption

Now that we have our list of high-priority testing targets,
we can go ahead and write some tests for them!

Pick one of the assumptions identified as high-priority in the last challenge,
and write some code to test whether it's true or false.

When we finish,
we'll talk about challenges we ran into in writing these tests.

::::


## Conclusion

We've thought a bunch about assumptions and how to test them.
What can we do with this?

The most important is to add checks to your data processing code,
to make sure that your inputs and outputs are behaving as you expect,
every time the code runs.
This protects you from surprising changes in new data,
or surprising behavior of changes you make to your code.

Hopefully that saves you from some hair-pulling debugging sessions in the future!

:::: keypoints

- you're always making assumptions about your data, and many of them are likely to be wrong
- you can prioritize assumptions by thinking about their impact, likelihood, and testability
- you can use `assert` statements to tell you if an assumption is wrong *every time you run the code*

::::
