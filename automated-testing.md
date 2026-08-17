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

We'll form hypotheses about what it should be doing,
then write some code that checks if the system is doing the right thing.
We'll introduce a library that helps you organize the testing code you just wrote,
and deal with the painful parts of a growing test suite.
When we run into failing tests, we'll get to play with the *debugger*,
a tool that lets you pause your program and investigate what's going wrong.


## Code background

:::: instructor

Use standard VSCode here,
instead of whatever wacky terminal editor you happen to be experimenting with this week.

::::

Look in the `checkpoints/making-sure-your-system-is-behaving` directory,
and open that `main.py` file.

:::: callout
Make sure you open this with a text editor or a code-specific program -
VSCode, PyCharm, Notebook, TextEdit, etc. will all work.
Microsoft Word, LibreOffice,
or anything that lets you bold/italicize/underline text will not.
::::

There are two functions in here.
One just reads in some data.
The other calculates heat rates, split out by year & energy source code.
The heat rate is a measure of energy efficiency of a generator -
how much energy are we putting *in* (in MMBtu) for the electricity we're getting *out* (in MWh)?

Since we're here to learn about what to do when things go wrong,
we've introduced a subtle bug in here.
Don't try too hard to spot it with your eyes,
we'll use *tools* to figure it out together.

## Finding a bug

We want to write some code to check some basic assumptions about the data.

We can use `assert` statements like before,
but as the assertion code gets complicated,
it can be confusing to have it mixed in with the "actual" code.
We can deal with that by keeping the test code in separate files.

Start by creating a new file, `test_main.py`.
Because of how we've set up the package structure,
we need to keep it in the same directory as `main.py`.

For our first assumption, let's check that there is data at all.
We'll start with an empty function and build up to the check that we want.
Starting with something that fails
makes it easy to tell that all the test machinery is working.

```python
def test_data_exists():
    assert False
```

That should fail nicely!
Now let's run it:

```
$ uv run python test_main.py
```

Hmm... no `AssertionError` shows up, so something is fishy.
Aha! We wrote a function, but nothing is calling it.
We need to call our function in the `if __name__ == "__main__":` block in order for it to run.

```python
if __name__ == "__main__":
    test_data_exists()
    # future tests get added here too
```

Now if we run it we'll get an `AssertionError`. Hooray!
If you know that the test code will actually yell at you if it fails,
then you know that if it doesn't yell at you, it has succeeded.

Now let's build up to the check we want.
We need to take the following steps:

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

Now we can try to test some other things!

* the heat rates exist at all
* the heat rates are all non-negative
* the heat rates aren't unreasonably high

Let's have you work on the first one
to get your hands dirty with the testing.

:::: challenge
### Challenge: writing test functions

Write a function in `test_main.py` called `test_heat_rates_exist`,
that tests that the *heat rates* exist.

You'll need to import `yearly_heat_rate_by_energy_source`,
and remember to start with a failing assertion to make sure the test is getting run:

```python
from main import load_generation_data, yearly_heat_rate_by_energy_source

def test_heat_rates_exist():
    # read in the data
    # generate the heat rates
    # assert they're not empty
    assert False
```

:::::::: solution

```python
def test_heat_rates_exist():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert not heat_rates.empty

# don't forget to add it to the if __name__ == "__main__": block!
```

::::::::

::::

Next we might want to assert that all the heat rates are non-negative.

```python
def test_heat_rates_non_negative():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert (heat_rates >= 0).all()

# if __name__ == "__main__": ...
```

We have three tests! That's great.

But ... it's only three tests, and there are already some bits of code
that appear over and over.

A useful programming habit is to be *strategically lazy*:
if you find yourself doing the same thing repeatedly,
that's a signal you are working too hard.
Repetitive code is error-prone, and annoying to maintain.
If you can find a way to do the same work with less repetition,
that will usually be more reliable.

There are a few such annoyances that have started to show up for us today.
First,
it's easy to forget to add the test to
the `if __name__ == "__main__"` block at the end.
Second,
we are repeating our data loading over and over.
If we change the name or location of that file, we have to change all the tests.

We can solve both of these issues by introducing a *test framework*
that can help us reduce repetition and toil.
`pytest` is the de facto standard.

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
and stop worrying about keeping it up to date!
One source of repetition eliminated.

We also eliminated a *future* source of repetition:
we didn't have to specify `test_main.py` when we ran `pytest`.
As our test system grows to include multiple files,
we won't have to remember to run each of them separately.

:::: instructor

Pause a second here and make sure people have had the chance to run pytest -
it's important to be able to run tests for the rest of the lesson.

::::

### Example: shared setup

The other source of repetition we encountered in our tests was loading data.

It is very common to have a bunch of tests that would all require the same
snippet of code to set up the data they want to check.
If you use copy and paste to give each test this snippet,
and you later have to change something about the setup procedure,
you would then have to remember to go make the same change
in all of those places.
That is not being strategically lazy!

In `pytest`, we can reduce this repetition by using
["test fixtures"](https://docs.pytest.org/en/stable/how-to/fixtures.html).
Fixtures let you pull shared setup code into a function *and also*
set a standard variable name for the result,
so that it's clear that every test that uses the same input variable
is getting the same data.

To use fixtures, we add a helper function that generates the data
we want to reuse:

```python

def pr_data():
    return load_generation_data("data/pr_gen_fuel_monthly.parquet")
```

...then we apply a special *decorator* to the function to mark it
as a fixture.

In Python, a decorator is a way to annotate a function with extra
labels (and sometimes data) that can be accessed by other parts of the code.

When we apply the `@pytest.fixture` decorator to our helper function, we get:

```python
import pytest

# ...

@pytest.fixture
def pr_data():
    return load_generation_data("data/pr_gen_fuel_monthly.parquet")
```

And then we can use `pr_data` as a parameter to each test that needs it,
and `pytest` will automatically use the matching fixture
to supply that parameter when it runs the test.

```python
def test_data_exists(pr_data):
    assert not pr_data.empty


def test_heat_rates_exist(pr_data):
    heat_rates = yearly_heat_rate_by_energy_source(pr_data)
    assert not heat_rates.empty


def test_heat_rates_non_negative(pr_data):
    heat_rates = yearly_heat_rate_by_energy_source(pr_data)
    assert (heat_rates >= 0).all()
```

We can run our tests again, and make sure they still pass:

```bash
$ uv run pytest
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving
configfile: pyproject.toml
plugins: anyio-4.10.0
collected 3 items

test_main.py ...                                                         [100%]

============================== 3 passed in 0.52s ===============================
```

Great!
That's another source of repetition... partially eliminated.
We're still computing heat rates multiple times.
We can do something about that!

:::: challenge
### Challenge: nesting fixtures

Fixtures can depend on *other fixtures*.
If you add a parameter to a fixture function,
and that parameter is the name of a fixture,
`pytest` will use the fixture to supply that parameter,
just like it does for test functions.

Add a new fixture, `heat_rates`,
that takes `pr_data` as a parameter
and returns the yearly heat rates.

Then, use `heat_rates` as a parameter for
`test_heat_rates_exist` and `test_heat_rates_non_negative`.

:::::::: solution
```python
import pytest

from main import load_generation_data, yearly_heat_rate_by_energy_source


@pytest.fixture
def pr_data():
    return load_generation_data("data/pr_gen_fuel_monthly.parquet")


@pytest.fixture
def heat_rates(pr_data):
    return yearly_heat_rate_by_energy_source(pr_data)


def test_data_exists(pr_data):
    assert not pr_data.empty


def test_heat_rates_exist(heat_rates):
    assert not heat_rates.empty


def test_heat_rates_non_negative(heat_rates):
    assert (heat_rates >= 0).all()
```
::::::::

::::

Setting up your fixtures well can make your tests very concise.
They'll communicate exactly what the input conditions are for the test
and what the expectations are,
with minimal clutter.

:::: callout
As your software gets more complicated, testing it can also get more complicated.
`pytest` offers a lot more beyond the functions we've already seen.
Check out the [official documentation](https://docs.pytest.org/en/stable/index.html) for more info!
::::

Now let's add one more test,
this time that the heat rates stay within some reasonable magnitude
for every year across every energy source code,
i.e. that no individual fuel type is unrealistically inefficient.

```python
def test_heat_rates_sensible_values(heat_rates):
    assert (heat_rates < 15).all() # 15 feels reasonable?
```

If we run that with `uv run pytest`, we get an error:

```pytest
================================ test session starts ================================
platform linux -- Python 3.13.11, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving
configfile: pyproject.toml
plugins: anyio-4.10.0
collected 4 items

test_main.py ...F                                                             [100%]

===================================== FAILURES ======================================
_______________________ test_heat_rates_sensible_values ________________________

heat_rates = year  energy_source_code
2017  bituminous_coal         10.582860
      distillate_fuel_oil     12.959005
      electr...solar                    3.412120
      wind                     3.411958
Name: heat_rate_mmbtu_per_mwh, dtype: float64

    def test_heat_rates_sensible_values(heat_rates):
>       assert (heat_rates < 15).all()
E       assert np.False_
E        +  where np.False_ = all()
E        +    where all = year  energy_source_code \n2017  bituminous_coal         10.582860\n      distillate_fuel_oil     12.959005\n      electr...solar                    3.412120\n      wind                     3.411958\nName: heat_rate_mmbtu_per_mwh, dtype: float64 < 15.all

test_main.py:28: AssertionError
=========================== short test summary info ============================
FAILED test_main.py::test_heat_rates_sensible_values - assert np.False_
============================ 1 failed, 3 passed in 0.42s ============================
```

We've found a place where the system's behavior doesn't match our expectations!
We should check if the expectations are at fault,
and if not, we should find where the system's behavior starts to go wrong.


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
then slowly go through the program one line at a time.
This will help us figure out what the heck is going on.

The first thing we need to do is add a *breakpoint* to the code,
which is where we will first pause the program.

We do this with the `breakpoint()` function.

First, let's look right before the assertion -
this error just tells us that *something* was greater than 15,
but the debugger can get us a bit more detail.

```python
def test_heat_rates_sensible_values(heat_rates):
    breakpoint()
    assert (heat_rates < 15).all()
```

Running this drops you into this cryptic situation:

```bash
% uv run pytest
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving
configfile: pyproject.toml
plugins: anyio-4.10.0
collected 4 items

test_main.py ...
>>>>>>>>>>>>>>>>>>> PDB set_trace (IO-capturing turned off) >>>>>>>>>>>>>>>>>>>>
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/test_main.py(28)test_heat_rates_sensible_values()
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
 27     def test_heat_rates_non_negative(heat_rates):
 28         assert (heat_rates >= 0).all()
 29
 30
 31     def test_heat_rates_sensible_values(heat_rates):
 32  ->     breakpoint()
 33         assert (heat_rates <= 15).all()
[EOF]
```

This shows some context around where the code execution has been paused.
The arrow shows the line of code that's *about* to run.

Now that we are in here,
you can type any Python expression and it will print out the result.
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
We can't debug any further from here;
we need to catch the program in the act of bugging.

Let's quit out of the debugger (`quit`),
and move the breakpoint to before we calculate the heat rates -
this happens in the fixture:

```python
@pytest.fixture
def heat_rates(pr_data):
    breakpoint()
    return yearly_heat_rate_by_energy_source(pr_data)
```

If we re-run, it pauses us at our new location:

```pdb
(Pdb) list
 11         return load_generation_data("data/pr_gen_fuel_monthly.parquet")
 12
 13
 14     @pytest.fixture
 15     def heat_rates(pr_data):
 16  ->     breakpoint()
 17         return yearly_heat_rate_by_energy_source(pr_data)
 18
 19
 20     def test_data_exists(pr_data):
 21         assert not pr_data.empty
```

We want to see what's going on in that yearly heat rate function,
so let's type `next` to advance the program by one line:

```pdb
(Pdb) next
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving/test_main.py(16)test_heat_rates_sensible_values()
-> heat_rates = yearly_heat_rate_by_energy_source(data)
```

Next, you can `step` into that assignment.
This drops you *into* the function that you're calling,
while still being paused:
`next` moves us forward, but `step` takes us deeper, and deeper is what we want.
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

Let's continue to advance through the code, until we get something interesting to inspect.

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
"I've gone through all the lines of this statement and given you a chance to step into one of the inner components.
Now I'm actually going to execute the whole statement."

Seeing `fuel_gen_monthly` isn't *that* useful, though.
We're mostly curious about which monthly heat rates are causing such high yearly averages.
We'll take a look at that through two challenges.

:::: challenge
### Challenge: Debugger navigation

We know the output of this `yearly_heat_rate_by_energy_source` function looks kind of fishy.

Advance the debugger until you can print out both the return value (`yearly_heat_rates`) and the intermediate value that feeds into the return value (`monthly_heat_rates`).

:::::::: solution

Keep typing `next` until the `->` points at `return yearly_heat_rates`,
and then see if you can print out both monthly and yearly heat rates.

::::::::

::::

:::: challenge
### Challenge: Investigating data in the debugger

Now that we have both the `yearly` and `monthly` heat rates available to us,
we can take a look at what's going on.

First, print out the yearly heat rates which are greater than 15.

Then, pick the combination of `year` and `energy_source_code`
with the most suspicious heat rate value,
and print out the `monthly_heat_rates` for that combination.

See anything strange?

:::::::: hint

Since `monthly_heat_rates` only has `date`, not `year`,
you'll need to use `monthly_heat_rates.date.dt.year` to filter by year.
::::::::


:::::::: solution

```python
monthly_heat_rates[
    (monthly_heat_rates.date.dt.year == 2021) &
    (monthly_heat_rates.energy_source_code == "residual_fuel_oil")
]
```

We see some extremely high heat rates for some plants that appear to have very small amounts of generation.

::::::::

::::

OK - after that challenge, we've almost figured out the bug.
We have some very high heat rates for some very small plants,
and that seems to be disproportionately affecting the average heat rate.

Here, we *do* have to use the traditional "think hard" strategy.
But the debugger has changed the question from
the very broad "is there anything wrong with this code?"
to the somewhat manageable
"why is the code giving so much weight to the small plants?"
Which should help direct your thinking.

:::: instructor

Depending on how much time you have,
you can either have them do the exercise
or just go over the hint and solution.

::::

:::: challenge

### (optional) Challenge: Thinking hard

Take a look at the code in `main.py`,
and ponder this question:

Why is the existing `yearly_heat_rate_by_energy_source` function giving so much weight to the small plants?

:::::::: hint

A 100 MMBtu / 1 MWh plant and a 10,000 MMBtu / 1,000 MWh plant
can be "averaged" in two ways:

* (100/1 + 10,000/1000) / 2 = 55
* (100 + 10,000) / (1 + 1000) ~= 10

Which one do we want?
Which one is in the code?

::::::::

:::::::: solution

We should sum the fuel consumption and net generation over the whole `residual_fuel_oil` fleet
for each timestamp, before dividing them to get heat rate:

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
    ].groupby(["date", "energy_source_code"]).sum().reset_index()
    monthly_heat_rates = fuel_gen_monthly.assign(
        year=fuel_gen_monthly["date"].dt.year,
        heat_rate_mmbtu_per_mwh=fuel_gen_monthly["fuel_consumed_for_electricity_mmbtu"]
        / fuel_gen_monthly["net_generation_mwh"],
    )
    yearly_heat_rates = (
        monthly_heat_rates.groupby(["year", "energy_source_code"], observed=False)[
            "heat_rate_mmbtu_per_mwh"
        ]
        .mean()
        .dropna()
    )
    return yearly_heat_rates
```

Running the test now succeeds.

::::::::

::::

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

Writing code with tests in mind may be slower at first,
but it's more than worth the investment if it means you can
reuse or extend existing code for your next research project
-- and know that it's still working --
instead of starting from a blank notebook.
Using a debugger rapidly accelerates your ability to figure out what's going on
during an unexpected failure,
without having to dedicate time to reproduce the error conditions
in an environment where you can examine what's happening,
or littering the code with print statements you later have to remove or maintain.

Together, testing and debugging can be a powerful starter kit of tools
to produce long-lived research software you can be confident will continue working correctly
across many revisions and extensions.
Go get 'em!

:::: keypoints

- It is good to test your assumptions about your pipeline's output, and `pytest` can help you keep your tests concise and easy to maintain.
- When something fails, you can use the built-in Python debugger, `pdb`, to pause the program at the point of failure and explore until you find the culprit.

::::
