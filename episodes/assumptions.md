---
title: "Making assumptions about your data"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- Exploratory data analysis was fun, but what did I learn?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Articulate assumptions about a dataset
- Evaluate assumptions by impact and likelihood of breakage

::::::::::::::::::::::::::::::::::::::::::::::::

## Intro

Now that you've looked at the data and gotten a sort of intuitive feel for it, it might be useful to characterize the data in a slightly more rigorous way. This can point you at current holes in your understanding or future problems with however you are planning on working with the data.

We'll go through three steps:

1. list out a bunch of assumptions about your assumptions
2. identify useful assumptions to test
3. write some code to verify those assumptions

## What is an assumption anyways?

In this context, an *assumption* can be any property you think is true about the data.

Some examples:
- assumptions about the values: the heat rate of renewables after 2022 is reported as a consistent value
- relationships are well-defined: data rows that share the same plant ID correspond to the same plant
- data types are consistent: the "year" column only contains numbers, not words or strings of random characters
- and many more!

These assumptions form the core of your mental model,
and if they turn out not to be true then anything that depends on your mental model might break in unexpected ways.
That includes your code crashing or spitting out bad data, of course.
It could also make your documentation confusing or misleading,
causing others to misinterpret your results.
It could also end with you publishing results that are based on incorrect data.

The most dangerous assumptions (and thus, the most useful to enumerate) are particulary hard to think of -
if they're obvious to you, then on some level you are aware of the need to work around them.
With that in mind, let's try to come up with some assumptions of our own!
 
:::: challenge

### Challenge: identifying assumptions

Take 5 minutes to list out as many assumptions as you can about the EIA 923 Puerto Rico data in the [data directory](../data/).

The goal is to get past the obvious ones and start thinking of some un-obvious assumptions - no need to limit yourself to 'realistic' ones at this stage.

::::


## Testing assumptions

### Example

Let's take a look at one of the example assumptions and see how we'd figure out if it's true:

> The heat rate of renewables after 2022 is reported as a consistent value.

How would we verify that?

First, we can calculate that heat rate:

```python

renewables_2022 = monthly_gen_fuel[
    (monthly_gen_fuel["date"] >= "2022-01-01") &
    (monthly_gen_fuel["energy_source_code"].isin({"SUN", "WND", "WAT"}))
]
consumption_btu = renewables_2022["fuel_consumed_for_electricity_mmbtu"] * 1_000_000
net_gen_kwh = renewables_2022["net_generation_mwh"] * 1000
heat_rate = consumption_btu / net_gen_kwh
```

Let's take a quick look:

```python
heat_rate.hist()
```

Looks like almost all of the values are clustered at 3400,
and the min and max values are between 2000 and 5000.

Then, we can use an `assert` statement to verify some fact.

`assert` basically says, "if this next part is True, great! Nothing happens. If it's false, we'll raise an error."

```python
assert 1 == 1
assert 1 == 2
```

So let's assert something about this heat rate - maybe that the standard deviation is below a certain percentage of the mean:

```python
assert heat_rate.std() / heat_rate.mean() <= 0.05
```


This took some effort, but now we have some code that verifies that assumption.
If we add new data in the future, or change how we process the data,
we can see if this assumption breaks by running this code again.
Pretty neat - let's try doing another one.

:::: challenge

### Challenge: writing code to test an assumption

Pick an assumption from the list we generated above and write some code to assert that the assumption is true!

::::

## Which assumptions are worth testing?

As we just saw, all assumptions take some effort to test.
While it's useful to test many assumptions,
the reality is that we have limited time to work on our projects
and need to prioritize the assumptions that are "worth" the investment of testing them.

What makes assumptions useful or less so?

* how easy it is to test these assumptions
* the impact on your system if the assumption turns out to not be true
* the likelihood this assumption is violated

Some examples of less useful assumptions:
- the person filling out the form is trying to tell the truth:
  this is *hard to test*.
  This sort of external human factor, while very impactful and nebulously possible,
  would require some detailed analysis and cross-comparison of different datasets to even begin testing.
- `fuel_consumption_mmbtu` is largely reported to 0.1 MMBtu precision,
  but one specific plant reports `fuel_consumption_mmbtu` to a 0.01 MMBtu precision:
  this has *low impact*.
  If there are more plants that report with higher precision,
  you are not likely to run into problems.
- the plant name column is always going to be a string of characters, not a numeric field:
  this has *low probability of being violated*.
  It would be hard to imagine a plant name column that doesn't have *some* words in the reported values,
  and that would force the whole column to be "string" type.

We'll think through each of these criteria together:

:::: challenge

### Challenge: evaluating testability

The effort required to test these assumptions can be evaluated with the question,
"Can I imagine a snippet of code that would verify this assumption?"

Look at your list of assumptions.
Think about how you would write code to test each one.

Can you identify one that would be easy to test, and one that would be hard to test?

::::

:::: challenge

### Challenge: evaluating impact

Impact is hard to think about when you haven't built up a whole system yet.
 But you can usually sort problems into "won't cause any problems,"
"will cause problems which will be easy to notice (i.e. the whole program crashing),"
and "will cause problems which will be hard to notice (i.e., the data will just be wrong)."
In most cases,
it is better to have your program crash loudly than to have your program silently give you bad data.

Look at the list of your assumptions and imagine each one is not actually true.

Can you identify one example for each of the following?

* will probably break downstream work in some obvious way?
* will probably not break anything downstream?
* will cause some subtle and hard-to-notice problem?

::::


:::: challenge

### Challenge: evaluating likelihood

Evaluating likelihood can be difficult:
you are guessing at the future based on your experience of the past.
A heuristic is "can I imagine a situation where this assumption would be false?"
You'll build up a more nuanced intuition over time.

Look at the list of your assumptions and imagine a scenario in which they would not be true.

Can you identify an example scenario that:
* seem very plausible?
* seems very implausible?

::::


:::: keypoints

- you're always making assumptions about your data - nice to know when they've been broken
- you can use `assert` statements to tell you they're broken
- you can evaluate the usefulness of assumptions by thinking about their impact, likelihood, and testability.

::::
