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

### What is an assumption anyways?

In this context, an *assumption* can be any property you think is true about the data.

Some examples:
- the data values themselves are clean: year is something sensible (some time close-ish to present day, probably), categorical values have well-defined meanings
- relationships are well-defined: same ID -> same plant, columns sum up to "total" columns, ratio of one column to another is roughly what you expect
- data types are consistent: an ID field that is all numbers doesn't occasionally have a letter in it
- column headers are stable: each new data file has the same column names
- stable NA values: there's a well-defined, non-growing set of values that mean "there is no value here"
- units stay the same: each new data file has the same units for each column

These assumptions form the core of your mental model, and if they turn out not to be true then anything that depends on your mental model might break in unexpected ways. That includes your code, of course, but also your documentation, and any papers or articles you may write.

The most dangerous assumptions (and thus, the most useful to enumerate) are particulary hard to think of - if they're obvious to you, then on some level you are aware of the need to work around them. With that in mind, let's try to come up with some assumptions of our own!
 
:::: challenge

### Challenge: identifying assumptions

Take 5 minutes to list out as many assumptions as you can about the EIA 923 Puerto Rico data in the [data directory](../data/).

The goal is to get past the obvious ones and start thinking of some un-obvious assumptions - no need to limit yourself to 'realistic' ones at this stage.

:::::::: solution

Some options...

* '.' means "no value reported (expected)" *and* "no value reported (unexpected)"
* the utility worker filling out the form didn't make any mistakes
* the 'MMBtu of fuel consumed' field has different values for renewables in different years, and those values mean something related to the real world
* there will be future versions of this data

::::::::

::::


## Testing assumptions

### Which assumptions are worth testing?

After that challenge, you might feel like some assumptions are more useful to test than others in some nebulous way:

Some examples of assumptions that might feel "more useful":

- this column always has values between 10 and 1000
- the ratio of column A to column B is roughly stable
- the same plant always has the same name over time

Some examples of "less useful" assumptions:
- only one specific plant reports `fuel_consumption_mmbtu` to a 0.1 MMBtu precision
- the plant name column is always going to be a string of characters, not a numeric field
- the person filling out the form is trying to tell the truth

What makes these useful or less so?

* the impact on your system if the assumption turns out to not be true
* the likelihood this assumption is violated
* how easy it is to test these assumptions


Impact is hard to think about when you haven't built up a whole system yet.
 But you can usually sort problems into "won't cause any problems,"
"will cause problems which will be easy to notice (i.e. the whole program crashing),"
and "will cause problems which will be hard to notice (i.e., the data will just be wrong)."
In most cases, it is better to have your program crash loudly than to have your program silently give you bad data.

:::: challenge

### Challenge: evaluating impact

Look at the list of your assumptions and imagine each one is not actually true.

Can you identify one example for each of the following?

* will probably break downstream work in some obvious way?
* will probably not break anything downstream?
* will cause some subtle and hard-to-notice problem?

::::

Likelihood can also be tricky - you are guessing at the future based on your experience of the past.
The easiest heuristic is "can I imagine a situation where this assumption would be false?"
You'll build up a more nuanced intuition over time.


:::: challenge

### Challenge: evaluating likelihood

Look at the list of your assumptions and imagine a scenario in which they would not be true.

Can you identify an example scenario that:
* seem very plausible?
* seems very implausible?

::::

The effort required to test these assumptions is similarly easiest evaluated with the question,
"Can I imagine a snippet of code that would verify this assumption?"
If you don't have a lot of tools for assumption verification, that can be hard.
Let's introduce a simple one.

### Example: testing assumptions

Here's an assumption we dug into last time:

> For solar photovoltaics, the reported heat rate (Btu of fuel consumed / KWh of net generation) is fairly consistent after 2022.

How would we verify that?

First, we can calculate that heat rate:

```python

solar_pv_post_2022 = monthly_gen_fuel[
    (monthly_gen_fuel["date"] >= "2022-01-01") &
    (monthly_gen_fuel["energy_source_code"] == "SUN") &
    (monthly_gen_fuel["prime_mover_code"] == "PV")
]
consumption_btu = solar_pv_post_2022["fuel_consumed_for_electricity_mmbtu"] * 1_000_000
net_gen_kwh = solar_pv_post_2022["net_generation_mwh"] * 1_000
heat_rate = consumption_btu / net_gen_kwh
```

Let's take a quick look:

```python
heat_rate.hist()
```

Yeah, looks like almost all of the values are clustered at 3500, and the min and max values are between 2000 and 5000.

Then, we can use an `assert` statement to verify some fact about it.

`assert` basically says, "if this next part is True, great! Nothing happens. If it's false, we'll raise an error."

```python
assert 1 == 1
assert 1 == 2
```

So let's assert something about this heat rate - maybe that the standard deviation is below a certain percentage of the mean:

```python
assert heat_rate.std() / heat_rate.mean() <= 0.05
```

:::: challenge

### Writing code to test an assumption

Take an assumption you identified as easy to test, and write some code to assert that the assumption is true!

::::


:::: challenge

### Evaluating testability

Look at your list of assumptions.

Can you find one that would be easy to test, and one that would be hard to test?

::::


:::: keypoints

- you're always making assumptions about your data - nice to know when they've been broken
- you can use `assert` statements to tell you they're broken
- you can evaluate the usefulness of assumptions by thinking about their impact, likelihood, and testability.

::::
