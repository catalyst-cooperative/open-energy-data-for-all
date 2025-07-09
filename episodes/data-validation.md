---
title: "Data validation"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- Exploratory data analysis was fun, but what did I learn?
- How do I make sure that new code changes or new data aren't breaking my system?
- When something does break, how can I identify which part of the system has broken?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Articulate assumptions about a dataset
- Evaluate assumptions by impact and likelihood of breakage

- Write tests that reduce the toil of manually checking that your system works
- Use tests to identify what parts of the system are broken/working


::::::::::::::::::::::::::::::::::::::::::::::::

**By the time the students hit here, they should not freak out when they see `uv run pytest` and they should feel OK about slamming a bunch of functions in a .py file.**

## Making assumptions about your data


### Intro

#### post-eda

- you've looked at the data and gotten a sort of intuitive feel for it
- it might be useful to characterize the data in a slightly more rigorous way - can point you at current holes or future problems.
- we'll go through a framework: list out a bunch of assumptions, then figure out which ones are likely to be problematic

#### post-modularization-2

- you've learned about automated testing for functions & their inputs/outputs
- but your whole system also has inputs/outputs
- maybe we can apply that testing tool here, too!
- start w checking assumptions about the input data, then move to assumptions about the outputs
  - TODO: this signals... too much - this is where we're going but we're not going to cover it all until the second hemiepisode


### What is an assumption anyways?

- it's just a property you think is true about the data

- the trickiest assumptions are the ones that you scrape the bottom of the barrel for - you're really looking for stuff that you didn't expect. so just... no judgement, throw whatever you can think of at this next challenge.
 
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

- less useful:
  - 'the person filling out the form is trying to tell the truth'

- what makes these useful/less useful? impact/likelihood/testability.

:::: challenge

### Assessing risk and effort

Think about your list that you just wrote down.

For each assumption, spend a little time thinking about:

* what will happen if this assumption isn't true? Will it crash your code? Or, worse, will it just quietly feed you bad data?
* can you imagine situations in which this assumption isn't true? how likely do those situations feel?
* can you imagine an easy way to test this assumption?

Can you identify any assumptions that are high impact, high likelihood, and easy to test?

:::::::: callout

Some of the assumptions in your list, especially the later ones you wrote down after you ran out of ideas, will feel "ridiculous." Oftentimes these are actually good ideas to test precisely because they are the ones that you weren't thinking about when working with the data the first time around.

::::::::

::::

## Making sure your system is behaving

:::: challenge

### Writing testing code

Pick one of the high risk/low effort assumptions, then flesh out the body of this function:

```python

def check_cool_assumption(input_data: DataFrame) -> bool:
    """Return whether or not the cool assumption holds for the input data.
    """
    # check the cool assumption 
```
::::


## Managing your testing code

* ok, now imagine you have multiple of these test functions. lots of assumptions * lots of datasets = lots & lots of tests
* annoying to go call them all manually and/or store them in your notebook.
* so let's pull them into `tests.py`.

:::: challenge
### put your code in tests.py

::::

... wait, but how do we run these tests?

enter... pytest!

### Example: a pytest test & how to run it

* use `test_`
* use `assert`
* `uv run pytest`

Oooooh pretty output :heart_eyes:

:::: challenge

### Challenge: moving your test(s) in test.py to pytest

Go take your test.py and make it so that when you run `uv run pytest` you get some output.

Can you make your test fail? What does that look like?

::::

### Example: fixtures

* you might want to reuse the same test data for a bunch of different assumptions... use a *fixture* to do that.
* you *don't* want to use a constant dataframe... what if you mutate it in one test?? then you'll literally die

```python
@pytest.fixture
def sweet_dataframe():
    pass
```


:::: challenge

### Challenge: fixtures

Add another test for the same dataframe (pulling from your Cool List of Cool Assumptions).

Update your `test.py` to use fixtures for your two tests.

::::


### Example: parametrization

* OK, now what if 
   

To think about: introduce parametrization? (years? states?)

EB: official parametrization docs are kind of mid, so maybe worth giving people the Short Version?


:::: challenge

### Testing outputs

Since the output of your code is just the input to other code...

What assumptions will other people want to make about your code?
Which ones do you expect to actually be true?
Write a test that makes sure that one of those assumptions about your *output* holds

KM: assumptions other ppl will make is hard. consider just "what guarantees are you making"

KM: other common approach. your jerk/pedant friend doesn't believe you that your function works. how do you prove to them that it works?

EB: maybe there's a more concrete version of this. we've been talking about Doing A Bunch Of Stuff to the data. how do we check that we actually did what we think we did? ties in well to "see if it works" from the last lesson.

KM: also ties in better to "what guarantees are you making"

```python

def test_output_assumption():
    input_data = pd.read_parquet(...)
    observed = my_cool_pipeline(input_data)
    # expected = ...
    # assert(...)
```

::::

:::: challenge

### connect to new data high-level question

* run this on... some different data? imagine your analysis expands beyond PR - what if you want to know about FL too?

KM: probably worth thinking about, but not worth doing.

EB: helpful to think of these three modules as a loop. explore, modularize, test. bring in new data - something is wrong but at least you have something firm to stand on. go back to the start.

TODO: this is not actually a Challenge, this is a "discuss" or a "really makes you think, huh?" at the end

::::

:::: challenge

for the folks who are bored and reading ahead:

* here is a function and a test, the test is kind of awkward, how would you rearrange the function so the test was easier to read?

::::

::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
