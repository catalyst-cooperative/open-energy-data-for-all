---
title: "Data validation"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I make sure that new data doesn't break my system?
  - figure out what assumptions you are making about the inputs and enforce them
- How do I make sure that new code changes aren't breaking the outputs?
  - figure out what guarantees you are making about the outputs and enforce them
  - your outputs are just inputs for someone else... or your next function

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Prioritize assumptions by importance and likelihood
- Programmatically detect violations of high-impact assumptions

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

have you ever:
- noticed something funny about your data output
- spent hours tracing backwards through your code to figure out what went wrong
- eventually found that it was due to some strange thing about the input data?

let's try to avoid that by:
- identifying *input assumptions*: what we need to be true about the input data so that our code will produce the correct output
- prioritizing which ones to check
- writing code to check these assumptions easily
 
:::: challenge

### Identifying assumptions

Take 3 minutes to list out as many assumptions as you can about [the subset of the PR data that we looked at].

:::::::: solution

Some options...

* '.' means NA
* the categorical 'energy source' 'prime mover' etc. values all correspond to the values listed in the spreadsheet
* same ID -> same plant
* the monthly columns sum up to the total columns
* net generation always positive
* ...

::::::::

::::


:::: challenge

### Assessing risk and effort

Think about your list that you just wrote down.

* here is a list of assumptions. which ones will crash your code if untrue? which ones will not affect your code? which ones will be in the middle?
* here is a list of assumptions. which ones feel safe? which ones feel like something that could easily get screwed up?
* here is a list of assumptions. which ones would be easy to check? which ones would be hard?

Which assumptions are in the high risk/low effort bucket?

KM: some of the assumptions from challenge 1 will feel "ridiculous" to the people who suggested them, but they will actually not be ridiculous and be good ideas. We should make sure that people know that assumptions that seem ridiculous at first glance are often the ones you're looking for.

::::

:::: challenge

### Writing testing code

Pick one of the high risk/low effort assumptions, then flesh out the body of this function:


```python

def check_cool_assumption(input_data: DataFrame) -> bool:
    """Return whether or not the cool assumption holds for the input data.
    """
    # check the cool assumption idk
```
::::


KM: motivate pytest - "what if we wanted to check all of these assumptions?"
(still need a little motivation for why not just write "test_whatever.py" and run it that way)
(pytest gives a lot of nice QOL stuff, and is very straightforward to get started with.)

:::: challenge

### Porting the code to pytest

Take that `check_cool_assumption` code and turn it into a test that pytest will pick up.

```python

@pytest.fixture()
def my_cool_df():
    ....

def test_cool_assumption(my_cool_df):
    pass
    

def test_cooler_assumption(my_cool_df):
    pass
    
def test_cool_assumption_for_one_dataframe():
    # ...

    df = pd.read....
    assert check_cool_assumption(df)

def test_cool_assumption_for_other_dataframe():
    # ...

    df = pd.read....
    assert check_cool_assumption(df)


def test_cool_assupmtion_for_lots_of_dfs():
    dfs = [...]
    for df in dfs:
        assert check...


@pytest.mark.parametrize(
...
)
def test_cool_assumption():
    ....
```

::::


TODO: use the various snippets that people made for testing, and introduce fixtures.

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
