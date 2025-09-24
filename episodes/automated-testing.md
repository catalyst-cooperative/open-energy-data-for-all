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

So we just wrote a bunch of code... how do we know if it works?

First, we should know what "it works" means.
Think about what you expect from the system - what do you think the output should look like?
This is sort of the mirror image of those assumptions you made about the data inputs earlier.
Then we should figure out if the system actually works.
We can use that same `assert` statement from before.

If, somehow, we find that our system doesn't work, what do we do?

Well, the system is a chain of sub-systems,
each of which take some input and make some output.
If the last part of the system produced a bad output,
either (a) there is a problem in that part or (b) it got bad input.
We can apply that same two-step process from above to the subsystems as well:
figure out what success means, then check to see if it's happening.

Once we find the problem sub-system,
we can continue fractally drilling down until we find the piece of code we need to change.

We'll introduce some tools that help make this process go smoothly:

- *test functions* tell you if your system is functioning as expected
- an *automated test runner* makes it easy to run all your tests at once so you don't have to remember/manually execute all the steps
- a *debugger* lets you zoom in even further to your system to figure out what exactly is happening

## Test functions

Writing assertions in various places can absolutely work to tell you if your system is functioning as expected.
But there are some common situations that can make it a little painful:

* sometimes there's a bunch of weird setup to even make that assertion, and you'd like to keep that out of your actual pipeline
* sometimes you want to test that something works in a variety of situations, but the assertions need to change based on the situation
* sometimes your *full* pipeline takes forever but there's a subsetted version of your pipeline that will expose most of the problems anyways, so you want to run the same checks on both
* when an assertion fails, your whole pipeline stops running - so if there are multiple problems you only know about the first one.

Test functions, together with an automated test runner, can help.
By writing small functions that do that setup for you,
or take some parameters to test a variety of scenarios,
you can avoid those pain points.
You can think of it sort of like the modularized version of writing in-line assertions in your code.

Let's do an example in our project!
You can get a copy of the project by unzipping the `making-sure-your-system-is-behaving-start.zip` file in the `checkpoints` folder of the course repository.

This project takes the raw Puerto Rico data and does some cleaning and reshaping.
It's reorganized a bit from the output of the previous episode:
we've split out the parts that read input files and write output files,
so the transformation function takes `DataFrame`s for inputs and produces them as outputs.

One thing we expect from the output is that
there's a `fuel_consumption_units` column and that its value is 0 for sun, wind, and water.

How would we test that?

First, we need to read in the raw data.
Then, we need to run the transformation code.
Then, we would want to read the `fuel_consumption_units` column from the output of the code.
Finally, we'd want to assert that those values are 0 for sun, wind, and water.

Let's create a new file, `test_main.py`.
Feel free to use any text or code editor you'd like for this (VSCode, Notepad, TextEdit, gedit, etc.) -
just avoid programs like Word or LibreOffice that automatically capitalize text or let you format things for print.
Because of how we've set up the package structure,
we need to keep it in the same directory as `main.py` and `utils.py`.

Then let's do those steps:

```python
import pandas as pd
from main import extract_pr_gen_fuel, transform_pr_gen_fuel


def test_renewables_fuel_units():
    # Read in the raw data...
    raw_pr_gen_fuel, raw_pr_plant_frame = extract_pr_gen_fuel()
    # Then run the code...
    pr_gen_fuel = transform_pr_gen_fuel(raw_pr_gen_fuel, raw_pr_plant_frame)[0]
    # Then pull out the subset we care about...
    renewable_codes = {"SUN", "WND", "WAT"}
    renewable_gen_fuels = pr_gen_fuel[
        pr_gen_fuel["energy_source_code"].isin(renewable_codes)
    ]
    renewable_fuel_units = renewable_gen_fuels["fuel_consumed_units"]
    # Finally, assert something!
    assert (renewable_fuel_units.dropna() == 0).all()
```

We need to add the test function to the `if __name__ == "__main__":` block in order for it to run.

```python
if __name__ == "__main__":
    test_renewables_fuel_units()
    # future tests get added here too
```

```bash
% uv run tests/test_pipeline.py
```

Hooray! No errors.
It's nice to not have that setup for extracting the renewable data cluttering or slowing down your processing code!

Now it's your turn.

:::: challenge

### Writing a test function

Think about the data processing code in `main.py`.

What is a property that you expect the output to have?

You can pick from this list, or come up with your own:

* all plants report some non-null values for net generation
* all fuel consumption units are non-negative
* the heat rate of combined cycle plants is roughly 7,000 Btu/kWh (this one will require a bunch of processing to calculate the heat rate!)

Write a function in `test_main.py` that tests this property by filling out the following skeleton:

```python
def test_cool_output_property():
    # Read in the raw data...
    raw_pr_gen_fuel, raw_pr_plant_frame = extract_pr_gen_fuel()
    # Then run the code...
    pr_gen_fuel = transform_pr_gen_fuel(raw_pr_gen_fuel, raw_pr_plant_frame)[0]
    # Then pull out the subset we care about...
    # Finally, assert something!
```

Don't forget to add it to the `if __name__ == "__main__":` block so you can run it!

It's OK if the test fails when you run it.
The point of writing tests is to find out when things are broken!
We'll talk about how to find the specific problem later.

#### Optional food for thought

Reading the input data and processing it is a shared setup step between multiple tests.
That seems wasteful and slow, especially if the processing step gets more and more complicated.
How would you approach reducing this duplication?

::::

## Automated test runners

As we write more tests,
we're starting to run into some problems:

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
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/daz/scratch/pr-gen-fuel
configfile: pyproject.toml
plugins: anyio-4.10.0
collected 1 item

test_main.py .                                                           [100%]

============================== 1 passed in 0.47s ===============================
```

What `pytest` is doing is:

* it looks for files named `test_*.py` or `*_test.py` within the given directory (defaults to current directory)
* in those files, it looks for functions that start with `test`
* it runs all those tests independently and makes a nice report

While it doesn't make a big difference with just one file with a small number of tests,
this can quickly become indispensable as your testing suite grows.

:::: challenge

### Challenge: try `pytest`

Try installing `pytest`, then running `uv run pytest` in your own project and see if it's picking up your tests!

::::

### Example: fixtures

:::: instructor

If we are low on time, can skip this example and just mention that there's a lot more to `pytest`.

::::

Another key feature of `pytest` is ["test fixtures"](https://docs.pytest.org/en/stable/how-to/fixtures.html).
These are a way of organizing and reusing test setup steps.

To use them, we first extract some shared setup into a function -
let's use the example test skeleton from before:

```python

def test_cool_output_property():
    # Read in the raw data...
    raw_pr_gen_fuel, raw_pr_plant_frame = extract_pr_gen_fuel()
    # Then run the code...
    pr_gen_fuel = transform_pr_gen_fuel(raw_pr_gen_fuel, raw_pr_plant_frame)[0]
    # Then pull out the subset we care about...
    # Finally, assert something!
```

Let's extract that setup into a function called `monthly_clean`:

```python
def monthly_clean():
    # Read in the raw data...
    raw_pr_gen_fuel, raw_pr_plant_frame = extract_pr_gen_fuel()
    # Then run the code...
    pr_gen_fuel = transform_pr_gen_fuel(raw_pr_gen_fuel, raw_pr_plant_frame)[0]
    # Then pull out the subset we care about...
    return pr_gen_fuel
```

Now, if we add the `@pytest.fixture` decorator,
we can use `monthly_clean` in multiple tests by adding it as a parameter to the test.

```python
@pytest.fixture
def monthly_clean():
    # Read in the raw data...
    raw_pr_gen_fuel, raw_pr_plant_frame = extract_pr_gen_fuel()
    # Then run the code...
    pr_gen_fuel = transform_pr_gen_fuel(raw_pr_gen_fuel, raw_pr_plant_frame)[0]
    # Then pull out the subset we care about...
    return pr_gen_fuel


def test_one(monthly_clean):
    ...


def test_two(monthly_clean):
    ...
```

Crucially, `pytest` knows enough to only run the function once and save the output.
That lets you share the setup between multiple tests!

:::: challenge

### Challenge: fixtures

Imagine you wanted to write a few tests that checked properties of the raw data.

The `monthly_clean` fixture doesn't help you because it doesn't expose the raw data!

How would you deal with this?

Write two tests:

* one that asserts that the raw data is not empty
* one that asserts that the `plant_id_eia` column is present in the raw data

We'll go over a few different ways to set this up once everyone's given it a shot.

::::

:::: instructor

The ways we'll go over:

* anything people tried to do
* just call extract_pr_gen_fuel() in the two tests
* make a new fixture that just does the raw data - `raw_data`
* make a new fixture that does the raw data, *and* make `monthly_clean` depend on `raw_data`


::::

As your software gets more complicated, testing it can also get more complicated.
`pytest` offers a lot more beyond the functions we've already seen.
Check out the [official documentation](https://docs.pytest.org/en/stable/index.html) for more info!

## The debugger

Suppose we have a test that fails.
Now we know that a subsystem isn't working right.
How do we figure out why it's broken?

At this point, we have a few options:
- break the function down into smaller parts and write more tests:
  this can totally work,
  but is often tedious and breaks up your code into unnecessarily small chunks
- throw in a bunch of `print(f"value of something is {something}")` statements:
  super easy, but annoying to keep going back and adding more.
  Plus then you have to delete them later to not clutter your output.
- use an **interactive debugger**: avoids both of these problems!

An interactive debugger pauses your program at a specific spot (a "breakpoint"),
at which point you get to go in and poke around.
Let's look at how to use `pdb`, the built-in Python debugger.

:::: instructor

Probably encourage people to really follow along on their own, something like:

"This tool is *very* interactive so it will be a lot easier to learn if you are
*literally* typing out the commands with your fingers instead of trying to remember all the things I'm doing.
If you need a minute to get set up, or fall behind,
throw up the NO react in Zoom and we'll give you time to catch up."

::::

:::: callout
Programs like VSCode often come with their own debuggers, which can be very powerful.

We're using `pdb` since it's available to everyone,
and the basic concepts apply for all debuggers.
::::

First, how to start the debugger at all: `breakpoint()`.
If you decide you want to figure out what's going on in a certain part of your code,
add the `breakpoint()` statement right where you want to pause the execution.
When you call your code from the CLI (or from a Jupyter notebook), it will pause right there.
Here's an example:

```python
# debugger_example.py

def inner_func(x, y):
    return f"({x}, {y})"


def outer_func():
    x = 1
    breakpoint()
    y = x + 1
    z = inner_func(x, y)
    return z


if __name__ == "__main__":
    outer_func()
```

```bash
% python debugger_example.py
```

This will drop you into the debugger,
at which point you'll be greeted with this terse situation:

```
-> breakpoint()
(Pdb)
```

`l` or `list` shows the code around where your execution is paused.
The `->` denotes the line that is *about* to run.

```
(Pdb) l
  2         return f"({x}, {y})"
  3
  4
  5     def outer_func():
  6         x = 1
  7  ->     breakpoint()
  8         y = x + 1
  9         z = inner_func(x, y)
 10         return z
 11
 12
(Pdb) l
 13     if __name__ == "__main__":
 14         outer_func()
[EOF]
(Pdb) list
[EOF]
```

If you call it multiple times in a row,
it tries to keep reading out more lines of the file.
Our file is very short, so this quickly reaches the end of the file (`[EOF]`).

To take a look at variable values, we can use `p` (short for "print"), or omit the command entirely:

```
(Pdb) p x
1
(Pdb) x
1
```

We can also print out an expression value to check that something behaves the way we expect:

```
(Pdb) x+1
2
```

We can also slowly step through the code using `next`/`n`:
```
(Pdb) next
> /home/daz/scratch/foo.py(8)outer_func()
-> y = x + 1
```

At this point, we are about to execute `y = x + 1`, which means that `x` should be defined as 1, but `y` is not defined yet:
```
(Pdb) x
1
(Pdb) y
*** NameError: name 'y' is not defined
```

But if we use `next` to move to the next line, we expect `y` to have the value 2:
```
(Pdb) n
> /home/daz/scratch/foo.py(9)outer_func()
-> z = inner_func(x, y)
(Pdb) y
2
```

Now we're about to call `inner_func()`. If we run `next` we'll run `z = inner_func(x, y)`:

```
(Pdb) n
> /home/daz/scratch/foo.py(10)outer_func()
-> return z
(Pdb) z
'(1, 2)'
```

But if we call `step` or `s` instead, we can go into that `inner_func` call:

```
(Pdb) step
--Call--
> /home/daz/scratch/foo.py(1)inner_func()
-> def inner_func(x, y):
```

This drops you in right at the beginning of the function call,
where you can continue using your other commands:

```
(Pdb) l
  1  -> def inner_func(x, y):
  2         return f"({x}, {y})"
  3
  4
  5     def outer_func():
  6         x = 1
  7         breakpoint()
  8         y = x + 1
  9         z = inner_func(x, y)
 10         return z
 11
(Pdb) n
> /home/daz/scratch/foo.py(2)inner_func()
-> return f"({x}, {y})"
```

It will pause you before you return a value as well:
```
(Pdb) next
--Return--
> /home/daz/scratch/foo.py(2)inner_func()->'(1, 2)'
-> return f"({x}, {y})"
(Pdb) l
  1     def inner_func(x, y):
  2  ->     return f"({x}, {y})"
  3
  4
  5     def outer_func():
  6         x = 1
  7         breakpoint()
  8         y = x + 1
  9         z = inner_func(x, y)
 10         return z
 11
```

And a further `next` drops you back into the original calling function:
```
(Pdb) next
> /home/daz/scratch/foo.py(10)outer_func()
-> return z
(Pdb) z
'(1, 2)'
```

Finally, to quit your session, you can use `q`:
```
(Pdb) q
Traceback (most recent call last):
  File "/home/daz/scratch/foo.py", line 14, in <module>
    outer_func()
    ~~~~~~~~~~^^
  File "/home/daz/scratch/foo.py", line 10, in outer_func
    return z
           ^
  File "/usr/lib64/python3.13/bdb.py", line 102, in trace_dispatch
    return self.dispatch_line(frame)
           ~~~~~~~~~~~~~~~~~~^^^^^^^
  File "/usr/lib64/python3.13/bdb.py", line 129, in dispatch_line
    if self.quitting: raise BdbQuit
                      ^^^^^^^^^^^^^
bdb.BdbQuit
```

Note that if you quit, you get this `BdbQuit` error in the console. That's totally normal.

:::: challenge

### Challenge: using the interactive debugger

Let's use the debugger! Here's a test that tests the `get_heat_rates` function.
As is, it is broken.

Let's add it to `test_main.py` and throw a breakpoint in there.
Then if you run `pytest` it will pause at the breakpoint.
Take some time to explore what's going on in the code!

If you're lost, try thinking about:

* Are the variables currently the values you expect?
* If not, what creates the bad values?
  Did it get the correct input (and, therefore, cause the problem itself),
  or was the input to *that* also wrong?

```python

def get_heat_rates(monthly, source_codes):
    filtered = monthly.loc[monthly.energy_source_code.isin(source_codes)]
    generation_kwh = filtered["net_generation_mwh"] * 1_000
    consumption_btu = filtered["fuel_consumed_mmbtu"] * 1_000_000
    heat_rate = consumption_btu.sum() / generation_kwh.sum()
    return heat_rate


def test_heat_rates(monthly_clean):
    """Compare heat rates between fosil fuels and renewables.

    Before 2022, the EIA used the "fossil fuel equivalency" methodology to
    calculate fuel_consumed_per_mmbtu for non-combustible renwables - which assumes
    that the *heat rate* of renewables is the same as that of fossil fuels.

    Let's check that assumption.

    Heat rates are typically represented as BTU per kWh.
    """
    fossil_source_codes = {"DFO", "RFO", "NG", "BIT"}
    renewable_source_codes = {"SUN", "WND", "WAT"}
    years_to_check = [2017, 2018, 2019, 2020, 2021]
    for year in years_to_check:
        one_year_gen_fuel = monthly_clean.loc[monthly_clean.date.dt.year == year]
        fossil_fuel_heat_rates = get_heat_rates(one_year_gen_fuel, fossil_source_codes)
        renewable_heat_rates = get_heat_rates(one_year_gen_fuel, renewable_source_codes)

        assert fossil_fuel_heat_rates == renewable_heat_rates
```

There are lots of paths to go down here.
We'll do this for about 8 minutes and then reconvene to discuss what we all tried and learned.

::::

:::: instructor

We should hammer home the "is this variable value what we expect? if not, why? walk backwards" loop when discussing.

::::

Those are the basics of how to use the interactive debugger.
Some additional tips:

- When running tests in `pytest`, you can automatically drop into a debugger whenever a test fails or errors - run `pytest --pdb`.
- The libraries you use are mostly Python code as well, which means you can `step` your way into them. This is a great way to understand the details of how that library code works!
- Type `help` while in a `(Pdb)` prompt to see what other things the debugger can do for you.

::::::::::::::::::::::::::::::::::::: keypoints

- Use `breakpoint()` to get into a debugger interface
- Use `l`/`list` to look around,
  `n`/`next` and `s`/`step` to control execution,
  and `p` to observe what's happening at each point.

::::::::::::::::::::::::::::::::::::::::::::::::

## Conclusion

"How to find what's going wrong with your system" is an extremely deep topic,
with lots and lots of tools that people have worked on through the years.
We've just started exploring this, through the basic strategy of:

* identify bad outputs of your system
* investigate the subsystems that produced the bad outputs - are they flawed or did they get fed bad inputs?
* repeat

We hope that you're able to leverage the tools of
automated testing and the interactive debugger
to go through that process more effectively and fix your systems more quickly in the future.
