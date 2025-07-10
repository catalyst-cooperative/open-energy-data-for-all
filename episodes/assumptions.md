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


### Example: assessing risk/effort


- some are maybe more useful than others...

- useful:
  - 'this column always has values between 10 and 1000'
  - 'the ratio of column A to column B is roughly stable'
  - 'the order of columns is the same'

- less useful:
  - 'the person filling out the form is trying to tell the truth'

- what makes these useful/less useful? impact/likelihood/testability.

:::: challenge

### Assessing risk and effort

**TODO: maybe move this "assess impact" part to the actual testing module**

Think about your list that you just wrote down.

For each assumption, spend a little time thinking about:

* what will happen if this assumption isn't true? Will it crash your code? Or, worse, will it just quietly feed you bad data? (also you might not know what your code is doing yet that's OK) (flesh out what 'bad data' means here)
* can you imagine situations in which this assumption isn't true? how likely do those situations feel?
* can you imagine an easy way to test this assumption?

Can you identify any assumptions that are high impact, high likelihood, and easy to test?

::::


### Asserting that an assumption is true

- pick an assumption (that is false)
- write an expression that shows the property
- use an assert statement

:::: challenge

### Writing code to test an assumption

Take an assumption you identified as easy to test, and write some code to assert that the assumption is true!

::::

:::: keypoints

- you're always making assumptions about your data - nice to know when they've been broken
- you can use `assert` statements to tell you they're broken

::::
