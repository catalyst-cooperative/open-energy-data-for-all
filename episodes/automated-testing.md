---
title: "Making sure your system is behaving"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I make sure that my system is working as I expect?
- How do I make sure that new code changes or new data aren't breaking my system?
- When something does break, how can I identify which part of the system has broken?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Write tests that reduce the toil of manually checking that your system works
- Use an automated test runner to further reduce that toil
- Use a debugger to narrow down the source of bad behavior

::::::::::::::::::::::::::::::::::::::::::::::::


## Intro

With what we've learned so far,
you are well on your way towards a robust and reproducible research system!
But, as the system grows,
it's easy for it to get out of hand.

We've gone over some tools to manage the complexity:

* enforcing important assumptions about your input data
* organizing your code into manageable and reusable pieces
* nailing down flexible notebooks into orderly Python scripts

Even with these tools,
not to mention the miracle of human intellect,
things can still go wrong sometimes.
In this lesson,
we'll introduce some tools to help you *detect* when that happens
and *diagnose* the problem.

We'll start by looking at a small slice of a system-in-progress.

We'll form a hypothesis about what it should be doing,
then write some code that checks if the system is doing the right thing.
Along the way, we'll get to play with the *debugger*,
a tool that lets you pause your program and investigate what's going wrong.

Finally, we'll introduce a library that helps you organize the testing code you just wrote,
and deal with the painful parts of a growing test suite.


## Code background

Look in the `checkpoints/making-sure-your-system-is-behaving` directory,
and open that `main.py` file.
There are two functions in here.
One just reads in some data.
The other calculates heat rates, split out by year & energy source code.

Since we're here to learn about what to do when things go wrong,
we've introduced a subtle bug in here.
Don't try too hard to spot it with your eyes,
we'll use *tools* to figure it out together.

:::: instructor

Use VS Code here.

::::

:::: callout
Make sure you open this with a text editor or a code-specific program -
VSCode, PyCharm, Notebook, TextEdit, etc. will all work.
Microsoft Word, LibreOffice,
or anything that lets you bold/italicize/underline text will not.
::::


## Finding a bug

Let's start out by writing some code to check some basic assumptions about the data.

We can use `assert` statements like before,
But as the assertion code gets complicated,
and can be confusing to have next to the "actual" code.
We can deal with that by modularizing the test code,
separating it out into its own functions.

We won't get into anything too complicated here,
but let's practice writing the tests separately!

Start by creating a new file, `test_main.py`.
Because of how we've set up the package structure,
we need to keep it in the same directory as `main.py` and `utils.py`.

Let's check that there is data at all.
But first, it's nice to start with something that fails.
Then at least you know all the test machinery is working.

```python
def test_data_exists():
    assert False
```

That should fail nicely!
Now let's run it:

```
$ uv run test_main.py
```

Hmm... no `AssertionError` shows up, something's fishy.
We need to add the test function to the `if __name__ == "__main__":` block in order for it to run.

```python
if __name__ == "__main__":
    test_data_exists()
    # future tests get added here too
```

Now if we run it we'll get an `AssertionError`. Hooray!
Always good to know that the test code will actually yell at you if it fails.

Now let's actually write the test - we need to take the following steps:

```python
def test_data_exists():
    # read in the data
    # assert existence
    assert False
```

Which looks like...

```python
from main import load_generation_data

def test_data_exists():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    assert not data.empty
```

And if we run the test with `uv run python test_main.py`,
all is clear.

While it's good to know that there are values at all,
it's also nice to know that they're within a reasonable range -
say, nothing has a negative heat rate, or a heat rate higher than 15.

:::: challenge
### Challenge: writing test functions

First, write a test in `test_main.py`, `test_heat_rates_exist`,
that tests that the *heat rates* exist.

You'll need to import `yearly_heat_rate_by_energy_source`,
and remember to start with a failing assertion to make sure the test is getting run:


```python
from main import load_generation_data, yearly_heat_rate_by_energy_source

def test_heat_rates_exist():
    # flesh me out!
    assert False
```

Then, write another test in `test_main.py` that tests that
the heat rates are non-negative and also less than 15,
called `test_heat_rates_sensible_values`.

Note that the subtle bug we warned you about should cause this second test to fail.


:::::::: solution

```python
def test_heat_rates_sensible_values():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert not heat_rates.empty


def test_heat_rates_sensible_values():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert (heat_rates >= 0).all()
    assert (heat_rates <= 15).all()
```

::::::::

::::


The plot thickens - we appear to have found some strange behavior in our code.


### Debugger introduction

:::: instructor

Encourage people to really follow along on their own, something like:

"The tools we use here are *very* interactive,
so it will be a lot easier to learn if you are *literally* typing out the commands with your fingers
instead of trying to remember all the things I'm doing.
If you need a minute to get set up, or fall behind,
throw up the NO react in Zoom and we'll give you time to catch up."

::::

Here is where a **debugger** comes in.

We'll use the built-in Python debugger to pause execution of the program,
look around and observe the state,
then slowly step through the program.
This will help us figure out what the heck is going on.

The first thing we need to do is add a *breakpoint* to the code,
which is where we will first pause the program.

We do this with the `breakpoint()` function. 

First, let's look right before the assertion -
this error just tells us that *something* was greater than 15,
but the debugger can get us a bit more detail.

```python
def test_heat_rates_sensible_values():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert (heat_rates >= 0).all()
    breakpoint()
    assert (heat_rates <= 15).all()
```

Running this drops you into this cryptic situation:

```bash
% uv run python test_main.py
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/test_main.py(17)test_heat_rates_sensible_values()
-> breakpoint()
(Pdb)
```

If you're seeing that, you've successfully hit the breakpoint.
In hacker parlance, "you're in."
That `(Pdb)` is a prompt for further commands.

:::: instructor

If you're used to using the short forms of the `pdb` commands (`l`, `n`, `s`, and so on) you should warn the students and *try* to use the full commands.

::::

A good first command is `list`:

```pdb
(Pdb) list
 12
 13     def test_heat_rates_sensible_values():
 14         data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
 15         heat_rates = yearly_heat_rate_by_energy_source(data)
 16         assert (heat_rates >= 0).all()
 17  ->     breakpoint()
 18         assert (heat_rates <= 15).all()
 19
 20
 21     if __name__ == "__main__":
 22         test_heat_rates_exist()
```

This shows some context around where the code execution has been paused.
The arrow shows the line of code that's *about* to run.

Now that we are in here,
you can type any expression and it will print out the result.
Let's see what `heat_rates` looks like.

```pdb
(Pdb) heat_rates
year  energy_source_code
2017  bituminous_coal         10.582860
      distillate_fuel_oil     12.959005
...
2025  bituminous_coal         11.209529
      distillate_fuel_oil     10.451752
      natural_gas              7.054819
      residual_fuel_oil       11.578304
      solar                    3.412120
      wind                     3.411958
Name: heat_rate_mmbtu_per_mwh, dtype: float64
```

Woah! That's a lot. Let's actually just look for the values that are higher than 15:

```pdb
(Pdb) heat_rates[heat_rates > 15]
year  energy_source_code
2017  residual_fuel_oil       45.389131
2018  distillate_fuel_oil     15.031923
2020  residual_fuel_oil       30.369541
2021  residual_fuel_oil      121.799209
Name: heat_rate_mmbtu_per_mwh, dtype: float64
```

So it seems like we have some truly **OUTRAGEOUS** numbers for `residual_fuel_oil`.
We should see what's going on.
Unfortunately, at this point the heat rates have already been calculated.
The cake has already been baked, so to speak.
We need to catch the program in the act of bugging.

Let's quit out of the debugger (`quit`), and move the breakpoint up a bit, to before we calculate the heat rates:

```python
def test_heat_rates_sensible_values():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    breakpoint()
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert (heat_rates >= 0).all()
    assert (heat_rates <= 15).all()
```

If we re-run, it pauses us slightly before where we were:

```pdb
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/test_main.py(15)test_heat_rates_sensible_values()
-> breakpoint()
(Pdb) list
 10         assert not heat_rates.empty, "Heat rates should be non-empty series."
 11
 12
 13     def test_heat_rates_sensible_values():
 14         data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
 15  ->     breakpoint()
 16         heat_rates = yearly_heat_rate_by_energy_source(data)
 17         assert (heat_rates >= 0).all()
 18         assert (heat_rates <= 15).all()
 19
 20
```

We want to see what's going on in that yearly heat rate function,
so let's type `next` to advance the program one line:

```pdb
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/test_main.py(16)test_heat_rates_sensible_values()
-> heat_rates = yearly_heat_rate_by_energy_source(data)
```

Note that `heat_rates` isn't available yet,
because we're *about to* execute the assignment statement:

```pdb
(Pdb) heat_rates
*** NameError: name 'heat_rates' is not defined
```

Next, you can `step` into that assignment,
instead of simply executing it with `next`.
This drops you *into* the function that you're calling,
while still being paused.
It's easier to see than explain:

```pdb
(Pdb) step
--Call--
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/main.py(10)yearly_heat_rate_by_energy_source()
-> def yearly_heat_rate_by_energy_source(data: pd.DataFrame) -> pd.DataFrame:
(Pdb) list
  5         """Load the cleaned Puerto Rico generator operations data from disk."""
  6
  7         return pd.read_parquet(path)
  8
  9
 10  -> def yearly_heat_rate_by_energy_source(data: pd.DataFrame) -> pd.DataFrame:
 11         """Calculate yearly heat rates for each energy source code."""
 12
 13         fuel_gen_monthly = data.loc[
 14             data["net_generation_mwh"] > 0,
 15             [
```

We've just followed the program execution into a totally different file!

Let's step through the code a bit, until we get something interesting to inspect.

```pdb
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/main.py(13)yearly_heat_rate_by_energy_source()
-> fuel_gen_monthly = data.loc[
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/main.py(14)yearly_heat_rate_by_energy_source()
-> data["net_generation_mwh"] > 0,
```

You might expect that at this point
we can look at `fuel_gen_monthly`,
because we've passed the `fuel_gen_monthly = ...`:

```pdb
(Pdb) fuel_gen_monthly
*** NameError: name 'fuel_gen_monthly' is not defined
```

But, since this is a multi-line statement,
we have to `next` through the internal pieces first:

```pdb
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/main.py(15)yearly_heat_rate_by_energy_source()
-> [
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/main.py(14)yearly_heat_rate_by_energy_source()
-> data["net_generation_mwh"] > 0,
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/main.py(13)yearly_heat_rate_by_energy_source()
-> fuel_gen_monthly = data.loc[
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/main.py(22)yearly_heat_rate_by_energy_source()
-> monthly_heat_rates = fuel_gen_monthly.assign(
(Pdb) fuel_gen_monthly
           date   energy_source_code  fuel_consumed_for_electricity_mmbtu  net_generation_mwh
0    2017-04-01                 wind                             101260.0             10991.0
1    2017-04-01          natural_gas                                  0.0             86494.0
2    2017-04-01          natural_gas                            1976130.0            189669.0
3    2017-04-01                solar                              31886.0              3461.0
4    2017-04-01      bituminous_coal                            3258736.0            310975.0
...         ...                  ...                                  ...                 ...
5361 2024-09-01    residual_fuel_oil                            1162501.0             98726.0
5362 2024-09-01  distillate_fuel_oil                             332108.0             25652.0
5363 2024-09-01    residual_fuel_oil                            1041201.0             98601.0
5364 2024-09-01  distillate_fuel_oil                             633760.0             51293.0
5365 2024-09-01  distillate_fuel_oil                             526019.0             48201.0

[3776 rows x 4 columns]
```

Notice how the `->` arrow jumped *back* to the `fuel_gen_monthly` assignment.
That's `pdb`'s way of telling you,
"I've gone through all the lines of this statement and given you a chance to pause.
Now I'm actually going to execute the statement."

Seeing `fuel_gen_monthly` isn't *that* useful, though.
We're mostly curious about what the monthly heat rates are which cause such high yearly averages.

:::: challenge
### Challenge: Debugger sleuthing

Let's think back to our bad heat rates. One that particularly stands out was

```
2021  residual_fuel_oil      121.799209
```

What's going on here?

Use the debugger to find the values in `monthly_heat_rates` that correspond to both the *year* 2021 and the *energy source code* `residual_fuel_oil`.

Do you see any strangely high values?

:::::::: hint

To select for those values,
you can hit `next` until `monthly_heat_rates` is available to print,
then print this out in the debugger:

```python
monthly_heat_rates[(monthly_heat_rates.date.dt.year == 2021) & (monthly_heat_rates.energy_source_code == "residual_fuel_oil")]
```
::::::::


:::::::: solution

We see some extremely high heat rates for some plants that appear to have very small amounts of generation.

::::::::

::::

OK - after that challenge, we've almost figured out the bug.
We have some very high heat rates for some very small plants,
and that seems to be disproportionately affecting the average heat rate.

Here, we *do* have to use the traditional "think hard" strategy.
But the debugger has changed the question from
"is there anything wrong with this code?" to
"how do I need to change my code to properly account for these outliers?"
Which should help direct your thinking.

:::: instructor

Depending on how much time you have,
you can either have them do the exercise
or just go over the hint and solution.

::::

:::: challenge

### (optional) Challenge: Thinking hard

How do you need to change your code to properly account for these tiny outliers?

:::::::: hint

You can think of the average of "one out of two, and 100 out of 1000" in two ways:

* (1/2 + 100/1000) / 2 = 0.3
* (1 + 100) / (2 + 1000) ~= 0.1
::::::::

:::::::: solution

We should sum the fuel consumption and net generation over the whole `residual_fuel_oil` fleet, before dividing them to get heat rate:

```python
def yearly_heat_rate_by_energy_source(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate yearly heat rates for each energy source code."""

    fuel_gen_monthly = data.loc[
        data["net_generation_mwh"] > 0,
        [
            "date",
            "energy_source_code",
            "fuel_consumed_for_electricity_mmbtu",
            "net_generation_mwh",
        ],
    ]
    fuel_gen_yearly = fuel_gen_monthly.assign(
        year=fuel_gen_monthly["date"].dt.year
    ).drop(columns="date")
    fleets_yearly = fuel_gen_yearly.groupby(by=["year", "energy_source_code"], observed=True).sum()
    yearly_heat_rates = (
        fleets_yearly["fuel_consumed_for_electricity_mmbtu"]
        / fleets_yearly["net_generation_mwh"]
    ).dropna()
    return yearly_heat_rates
```

Running the test now succeeds.

::::::::

::::


## Automated test runners

As we write more tests,
we'll starting to run into some problems:

- The boilerplate is annoying and it's easy to forget to add a test. Then you'll think your code works when it doesn't.
- Shared test setup can get complicated quickly
- If you have lots of tests & want to break them into multiple files, you now have to run all these other files too
- If one test breaks, it immediately exits with an `AssertionError` and the rest of the tests are skipped. Now you don't know what else broke!
  - This mirrors one of the problems with peppering your processing code with `assert` statements -
    sometimes you don't want the whole process to come crashing down in the middle because of one assertion failure!

What would be nice is some tool that
automatically finds testing code,
runs tests separately,
and reports the outputs of *all* your tests regardless of if one failed or not.
`pytest` solves all these quality-of-life problems and more.
Let's try it out.

### Example: pytest quickstart

First we need to install `pytest`:

```bash
% uv add pytest
```

Then we can run our tests:

```bash
% uv run pytest
```

```output
> uv run pytest
============================ test session starts ============================
platform linux -- Python 3.13.11, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving-end
configfile: pyproject.toml
plugins: anyio-4.10.0
collected 3 items

test_main.py ...                                                              [100%]

============================= 3 passed in 0.35s =============================
```

What `pytest` is doing is:

* it looks for files named `test_*.py` or `*_test.py` within the given directory (defaults to current directory)
* in those files, it looks for functions that start with `test`
* it runs all those tests independently and makes a nice report

Now you can take that `if __name__ == "__main__"` block out of your test code,
and stop worrying about maintaining it!

While it doesn't make a big difference with just one file with a small number of tests,
this can quickly become indispensable as your testing suite grows.

### Example: shared setup

Your little modularization-pilled brain may already be itching to
take that shared data loading setup out into its own helper function.

While that works, `pytest` has a more standard
(and more powerful, though we won't get into the complexities of power)
way of handling shared test setup:
["test fixtures"](https://docs.pytest.org/en/stable/how-to/fixtures.html).

To use them, we add the `@pytest.fixture` decorator to a helper function:

```python
import pytest

# ...

@pytest.fixture
def pr_data():
    return load_generation_data("data/pr_gen_fuel_monthly.parquet")
    return heat_rates
```

And then we can use `pr_data` as a parameter to each test that needs it:

```python

def test_data_exists(pr_data):
    assert not pr_data.empty

def test_heat_rates_exist(pr_data):
    heat_rates = yearly_heat_rate_by_energy_source(pr_data)
    assert not heat_rates.empty


def test_heat_rates_sensible_values(pr_data):
    heat_rates = yearly_heat_rate_by_energy_source(pr_data)
    assert (heat_rates >= 0).all()
    assert (heat_rates <= 15).all()
```

:::: challenge
### Challenge: nesting fixtures

One very useful thing about fixtures is that they can depend on other fixtures.
Add a new fixture, `heat_rates`, that generates the heat rates based on the `pr_data`.

Rewire the tests so the various fixtures are used appropriately.

:::::::: solution
```python
import pytest

from main import (
    load_generation_data,
    yearly_heat_rate_by_energy_source,
)


@pytest.fixture
def pr_data():
    return load_generation_data("data/pr_gen_fuel_monthly.parquet")


@pytest.fixture
def heat_rates(pr_data):
    return yearly_heat_rate_by_energy_source(pr_data)


def test_data_exists(pr_data):
    assert not pr_data.empty


def test_heat_rates_exist(heat_rates):
    assert not heat_rates.empty, "Heat rates should be non-empty series."


def test_heat_rates_sensible_values(heat_rates):
    assert (heat_rates >= 0).all()
    assert (heat_rates <= 15).all()
```
::::::::

::::

Setting up your fixtures well can make your tests very concise.
They'll communicate exactly what the input conditions are for the test
and what the expectations are,
with minimal clutter.

As your software gets more complicated, testing it can also get more complicated.
`pytest` offers a lot more beyond the functions we've already seen.
Check out the [official documentation](https://docs.pytest.org/en/stable/index.html) for more info!


## Conclusion

"How to find what's going wrong with your system" is an extremely deep topic,
with lots and lots of tools that people have worked on through the years.
We've just started exploring this, through the basic strategy applies everywhere:

* find some way to produce bad output
* work backwards, narrowing in on the place where it all went wrong
* repeat

We introduced some tools to help with this strategy:

* test functions to identify and reproduce bad output
* the debugger to dig into the process that produced the bad output
* an automated testing framework that helps organize your rapidly-growing test suite

