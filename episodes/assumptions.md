---
title: "Making assumptions about your data"
teaching: 30
exercises: 20
---

:::: instructor

Prep list:

- make a Google Doc that people can put in their assumptions
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

Take 5 minutes to list out as many assumptions as you can about the EIA 923 Puerto Rico data (`pr_gen_fuel_monthly.parquet`) in the [data directory](../data/).

Please put them in the shared Google doc that your instructor prepared for you.

The goal is to get past the obvious ones and start thinking of some un-obvious assumptions - no need to limit yourself to 'realistic' ones at this stage.

:::::::: instructor

Put these in a Google doc that you share with the class.


Some examples, if students are feeling a little quiet:

* the net generation data is actually in MWh and not a mix of units
* for a given generator in a given time period, NAs mean there was no data reported at all
  (all measured values are NA or none are)
* the net generation of batteries is strictly less than the fuel consumed in MWh
* all energy source codes correspond to the set in the documentation
* a plant ID corresponds to only one plant name per year
* every generator has at least one reporting period for which they have non-zero generation
* electricity generation heat rates are close to known averages for their prime mover / energy source
* if a value is reported, it is correct and reflects reality
* if a generator reports all null values for a specific time period, it was non-operational during that time period; if a generator reports 0 generation for a specific time period, it was operational, but not dispatched

::::::::

::::

## Which assumptions are worth testing?

All assumptions take some effort to test.
While it's useful to test many assumptions,
the reality is that we have limited time to work on our projects
and need to prioritize the assumptions that are "worth" the investment of testing them.

What makes assumptions worth testing?

* how easy it is to test the assumption
* the impact on your system if the assumption turns out to not be true
* the likelihood the assumption is violated

Let's look at each of these dimensions one by one.

## Testability

### How to test your assumptions

It's hard to imagine how easy it is to test an assumption
without having seen any examples of assumptions being tested!
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

Oho! We find that the assertion is not true!
This is pretty common.
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

Now that your imagination is primed,
we can evaluate assumptions for whether they'd be easy or hard to test.
There's no hard and fast rule here - a useful heuristic is,
"Can I imagine a snippet of code that would verify this assumption?"

Let's go through some examples.

The assumption we just tested,
"the reported fuel consumption in MMBtu is always non-negative",
is not so bad - we just imagined that snippet of code together above.

One that might be a bit harder would be
"for renewables after 2022, the reported fuel consumption in MMBtu is equivalent to the net generation in MWh." This is a little trickier because of two reasons:

* we have to do some unit conversions to even compare these
* we need to think about "how close is close enough?" due to different precision,
  and the loss of precision from unit conversions

One that might be quite hard to test would be
"There were no mistakes in the data entry."
That would require some sort of cross-checking with a different reputable source,
and likely some communication with EIA as well.

:::: challenge

### Challenge: evaluating testability

Look at the list of assumptions.

Can you identify one that would be easy to test, and one that would be hard to test?

If you have time, write some code to verify the easy assumption!

When we finish,
we will share some examples of easy and hard assumptions to test with the rest of the group.

::::


## Impact

Let's talk about impact!

We can't evaluate the impact of a faulty assumption
without a corresponding use case to be impacted.
And different use cases will lead to different impact for the same faulty assumption.

One way to think about the severity of impact is a three-level system:

* no effect: nothing bad happens to your use case.
* quiet failure: your system produces incorrect outputs
* loud failure: your system doesn't produce outputs at all

Consider the following:

#### Case 1
* Use case: longitudinal analysis of one specific plant
* Assumption: this specific plant reports net generation data for all years it was active.
* Impact of faulty assumption: there are data gaps in the net generation data.
  In this case it would probably cause a quiet or loud failure,
  depending on the specifics of the system.

#### Case 2
* Use case: aggregate analysis of all plants in Puerto Rico
* Assumption: a specific plant reports net generation data for all years it was active.
* Impact of faulty assumption:
  there are data gaps for that specific plant,
  but the aggregate values are not heavily affected.
  This would probably lead to no effect or a quiet failure.

We see that the same assumption can lead to different impacts
due to the use cases we apply them to.

:::: challenge

### Challenge: evaluating impact

Look at the list of assumptions and choose one.

Can you come up with use cases where this assumption's failure will:

* not affect the use case
* quietly affect the use case
* loudly affect the use case?

When we finish,
we will share some examples of how different use cases affect the impact of failure with the rest of the group.

::::

## Likelihood

Evaluating likelihood can be difficult:
you are guessing at the future based on your experience of the past.
A heuristic is
"Can I imagine a situation where this assumption would be false?
How improbable is that situation?"
You'll build up a more nuanced intuition over time.

Some example assumptions:

* The "year" column only contains numbers, not words or strings of random characters
  * this seems somewhat plausible:
    if, for example,
    this comes from a scan of a handwritten form,
    and there was some automatic character recognition involved,
    you could totally end up with some wonky values in here.
* The data is being filled out in good faith
  * This seems implausible to be broken:
    in theory,
    people are not lying to the EIA about the amount of electricity they generated,
    and the EIA is still considered a trustworthy organization.

:::: challenge

### Challenge: evaluating likelihood

Look at the list of assumptions and pick two.

Imagine scenarios in which they are individually broken.

Do they both seem plausible? Does one seem more plausible than the other?

Finally, can you find an assumption where failure seems particularly implausible?

When we finish,
we will share some plausible and implausible stories about how assumptions might be broken.

::::


:::: keypoints

- you're always making assumptions about your data, and many of them are likely to be wrong
- you can use `assert` statements to tell you if an assumption is wrong
- you can evaluate the usefulness of assumptions by thinking about their impact, likelihood, and testability.

::::
