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

- you've looked at the data and gotten a sort of intuitive feel for it
- it might be useful to characterize the data in a slightly more rigorous way - can point you at current holes or future problems.
- we'll go through a framework: list out a bunch of assumptions, then figure out which ones are likely to be problematic

### What is an assumption anyways?

- it's just a property you think is true about the data

- the trickiest assumptions are the ones that you scrape the bottom of the barrel for - you're really looking for stuff that you didn't expect. so just... no judgement, throw whatever you can think of at this next challenge.

- some examples
  - data values are good: year is real, categoricals exist
  - relationships are good: same ID -> same plant, columns sum up or provide good ratios
  - data types are consistent
  - column headers are stable
  - stable na values
  - units stay the same
  etc.
    

- where are assumptions embedded? in documentation, your  code, library code, papers, etc.
 
:::: challenge

### Identifying assumptions

Take 3 minutes to list out as many assumptions as you can about the EIA 923 Puerto Rico data in the [data directory](../data/).

:::::::: solution

Some options...

* '.' means "no value reported (expected)" *and* "no value reported (unexpected)"
* the categorical 'energy source' 'prime mover' etc. values all correspond to the values listed in the spreadsheet
* same ID -> same plant
* the monthly columns sum up to the total columns
* net generation always positive
* the order of the columns will always be the same
* there are no values reported where we would actually expect a null value
* ...

::::::::

::::


### Example: testing assumptions


example:

here's an assumption: cool property of input

here's how we might test that using an `assert` statement.

`assert` basically says, "if this next part is True, great! if it's false, we'll raise an error."

```python
assert 1 == 1
assert 1 == 2
```

We can also add a little message if we want a friendlier error:

```python
assert 1 == 2, "useful message for debugging :)"
```

```python
property = df.loc[...]...
assert property.all(), "all x must be y"
```

:::: challenge

### Writing code to test an assumption

Take an assumption you identified as easy to test, and write some code to assert that the assumption is true!

::::



### Which assumptions are worth testing?

- some are maybe more useful than others...

- useful:
  - 'this column always has values between 10 and 1000'
  - 'the ratio of column A to column B is roughly stable'
  - 'the order of columns is the same'

- less useful:
  - 'the person filling out the form is trying to tell the truth'

- what makes these useful/less useful? impact/likelihood/testability.

- impact is hard to think about when you haven't built up a whole system yet
  - though - it is better for your system to crash, than for it to subtly give you incorrect output... noodle on that.
- likelihood is a gut check that you'll refine over time


:::: challenge

### Identifying worthwhile assumptions

Look at your list of assumptions. See if you can find an example for each of these criteria:
* has a high impact
* has a low impact
* high/low likelihood
* high/low testability

::::

:::: keypoints

- you're always making assumptions about your data - nice to know when they've been broken
- you can use `assert` statements to tell you they're broken
- impact/likelihood/testability framework

::::
