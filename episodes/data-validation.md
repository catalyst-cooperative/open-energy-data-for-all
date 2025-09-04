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

Let's do an example in `tests/test_pipeline.py` in our project.
Take the transformation pipeline from the last episode,
which takes the raw Puerto Rico data and does some cleaning and reshaping.
One thing we expect from the output is that
there's a `fuel_consumption_units` column and that its value is 0 for sun, wind, and water.

How would we test that?

First, we would want to run the code.
Then, we would want to read the `fuel_consumption_units` column from the output of the code.
Finally, we'd want to assert that those values are 0 for sun, wind, and water.


```python
import pandas as pd
from pr_gen_fuel.main import transform_pr_gen_fuel


def test_renewables_fuel_units():
    transform_pr_gen_fuel()
    pr_gen_fuel = pd.read_parquet("data/pr_gen_fuel_monthly.parquet")
    renewable_codes = {"SUN", "WND", "WAT"}
    renewable_gen_fuels = pr_gen_fuel[
        pr_gen_fuel["energy_source_code"].isin(renewable_codes)
    ]
    renewable_fuel_units = renewable_gen_fuels["fuel_consumed_units"]
    assert (renewable_fuel_units.dropna() == 0).all()
```

It's kind of nice to not have to do that setup for extracting the renewable data within your pipeline code itself!

**TODO**: "it is annoying, though, to read from a file on disk, what if you change the output file location, or you want to run this test without overwriting the actual output file? let's refactor

We need to add the test function to the `if __name__ == "__main__":` block in order for it to run.

```python
if __name__ == "__main__":
    test_fuel_consumption_units_for_renewables()
    # future tests get added here too
```

```bash
% uv run tests/test_pipeline.py
```

Hooray! No errors.

Now it's your turn.

:::: challenge

### Writing a test function

Think about the data pipeline we wrote in the last exercise in the modularization episode.

What is a property that you expect the output to have?

You can pick from this list, or come up with your own:

* all plants report non-null values for net generation
* all fuel consumption units are non-negative
* the heat rate of combined cycle plants is roughly 7,000 Btu/kWh (this one will require a bunch of processing to calculate the heat rate!)

Write a function in `test_pipeline.py` that tests this property by filling out the following skeleton:

```python
def test_cool_output_property():
    input_data = pd.read_parquet("../data/pr_gen_fuel_monthly.parquet")
    output = process_monthly(input_data)
    # make some assertions about the data
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
we're starting to run into some of the problems with our `if __name__ == "__main__":...` strategy:

- The boilerplate is annoying and it's easy to forget to add a test. Then you'll think your code works when it doesn't.
- Shared test setup can get complicated quickly
- If you have lots of tests & want to break them into multiple files, you now have to run all these other files too
- If one test breaks it immediately exits with an `AssertionError` and now you don't know what else broke

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
% uv run pytest tests
```

**TODO** paste some output!

What `pytest` is doing is:

* it looks for files named `test_*.py` or `*_test.py` within the given directory (defaults to current directory)
* in those files, it looks for functions that start with `test`
* it runs all those tests independently and makes a nice report


:::: challenge

### Challenge: try `pytest`

Try installing `pytest`, then running `uv run pytest tests/` in your own project and see if it's picking up your tests!

::::

### Example: fixtures

:::: instructor

If we are low on time, can skip this example and just mention that there's a lot more to `pytest`.

::::

One key feature of `pytest` is ["test fixtures"](https://docs.pytest.org/en/stable/how-to/fixtures.html).
These are a way of organizing test setup steps.

To use them, we first extract some shared setup into a function -
let's use the example test skeleton from before:

```python
def test_cool_output_property():
    input_data = pd.read_parquet("../data/pr_gen_fuel_monthly.parquet")
    output = process_monthly(input_data)
    # make some assertions about the data
```

Let's extract that setup into a function called `monthly_clean`:

```python
def monthly_clean():
    input_data = pd.read_parquet("../data/pr_gen_fuel_monthly.parquet")
    output = process_monthly(input_data)
    return output
```

Now, if we add the `@pytest.fixture` decorator,
we can use `monthly_clean` in multiple tests.
Crucially, `pytest` knows enough to only run the function once, so

```python

@pytest.fixture
def monthly_clean():
    input_data = pd.read_parquet("../data/pr_gen_fuel_monthly.parquet")
    output = process_monthly(input_data)
    return output


def test_one(monthly_clean):
    ...


def test_two(monthly_clean):
    ...
```

::::

As your software gets more complicated, testing it can also get more complicated.
`pytest` offers a lot more beyond the functions we've already seen
(automatically finding your test functions & running them separately for you).
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
- use an **interactive debugger**:

An interactive debugger pauses your program at a specific spot (a "breakpoint"),
at which point you get to go in and poke around.
Let's look at how to use it.

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
% python foo.py
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

If your function failed your test, throw a breakpoint in the function & go check it out! Can you figure out what's going on?

You can also copy this function & test code if your function already works perfectly:

```python
def foo():
    breakpoint()
    ...


def bar():

    # bug should be in here
    ...

def test_foo():
    observed = foo()
    expected = ...
    assert observed == expected
```

::::

Those are the basics of how to use the interactive debugger.
Some additional tips:

- When running tests in `pytest`, you can drop into a debugger whenever a test fails or errors - run `pytest <your_test_location> --pdb`.
- The libraries you use are mostly Python code as well, which means you can `step` your way into them. This is a great way to understand the details of how that library code works!
- Type `help` while in a `(Pdb)` prompt to see what other things the debugger can do for you.

::::::::::::::::::::::::::::::::::::: keypoints

- Use `breakpoint()` to get into a debugger interface
- Use `l`/`list` to look around,
  `n`/`next` and `s`/`step` to control execution,
  and `p` to observe what's happening at each point.

::::::::::::::::::::::::::::::::::::::::::::::::
