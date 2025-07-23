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
- Use tests to identify what parts of the system are broken/working
- Use a debugger to narrow down the source of bad behavior

::::::::::::::::::::::::::::::::::::::::::::::::

## Intro

So we just wrote a little data pipeline... how do we know if it works?

First, we should know what "it works" means.
Think about what you expect from the system - what do you think the output should look like?
This is sort of the mirror image of those assumptions you made about the data inputs earlier.

Then we should figure out if the system actually works.
We can use that same `assert` statement from before.

If, somehow, we find that our system doesn't work, what do we do?

Well, the system is a chain of sub-systems, each of which take some input and make some output. If the last part of the system produced a bad output, either (a) there is a problem in that part or (b) it got bad input. We can apply that same two-step process from above to the subsystems as well: figure out what success means, then check to see if it's happening.

Once we find the problem sub-system, we can continue fractally drilling down until we find the piece of code we need to change.

We can do this purely with the `assert` statement we worked with already, but we'll introduce some tools that help make this process much smoother:

- *test functions* tell you if your system is functioning as expected
- an *automated test runner* makes it easy to run all your tests at once so you don't have to remember/manually execute all the steps
- a *debugger* lets you zoom in even further to your system to figure out what exactly is happening

### Test functions

Writing assertions in various places can absolutely work to tell you if your system is functioning as expected. But there are some common situations that can make it a little painful:

* sometimes there's a bunch of weird setup to even make that assertion, and you'd like to keep that out of your actual pipeline
* sometimes you want to test that something works in a variety of situations, but the assertions need to change based on the situation
* sometimes your *full* pipeline takes forever but there's a subsetted version of your pipeline that will expose most of the problems anyways, so you want to run the same checks on both

That's where test functions come in.
By writing small functions that do that setup for you,
or take some parameters to test a variety of scenarios,
you can avoid those pain points.
You can think of it sort of like the modularized version of writing in-line assertions in your code.

Let's do an example in `tests/test_pipeline.py` in our project.
Take the transformation pipeline from the last episode,
which takes the raw Puerto Rico data and does some cleaning and reshaping. 
One thing we expect from the output is that there's a `fuel_consumption_units` column and that its value is 0 for renewables.

**TODO** make sure this code actually works with the shape of the output from previous episode

```python
def test_fuel_consumption_units_for_renewables():
    raw_data = pd.read_parquet(...)
    pr_gen_fuels = process(raw_data)
    renewable_codes = {"SUN", "WND", "WAT"}
    renewable_gen_fuels = pr_gen_fuels[pr_gen_fuels["energy_source_code"] in renewable_codes]
    renewable_fuel_units = renewable_gen_fuels["fuel_consumption_units"]
    assert (renewable_fuel_units == 0).all()
```

It's kind of nice to not have to do that setup for extracting the renewable data within your pipeline code itself!
Let's actually run this function when we run `uv run tests/test_pipeline.py` by calling the function here:

```python
if __name__ == "__main__":
    test_fuel_consumption_units_for_renewables()
    # future tests get added here too
```

```bash
% uv run tests/test_pipeline.py
```

Now it's your turn.

:::: challenge

#### Writing a test function

:::::::: instructor

**TODO**
We can also prepare a separate broken pipeline in case we run this standalone.

::::::::

Think about the pipeline we made together in the modularization episode.

What is a property that you expect the output to have?
Write a function in `test_pipeline.py` that tests this by filling out the following skeleton:

**TODO** get the right filenames/function names
```python
def test_cool_output_property():
    input_data = pd.read_parquet(...)
    output = process(input_data)
    # make some assertions about the data
```
::::

Another thing we can do with test functions is test a smaller piece of the pipeline instead of the whole thing.
This can be particularly helpful when you want to add functionality to that piece of the pipeline
without breaking any of the old behavior.


Let's try just testing the NA-cleaning code.

Maybe in the future we will find other NA values too,
but we want to make sure that the `.` is always marked as NA.


**TODO** update to work with modularized code from previous lesson

```python
import pandas as pd

def test_function_happy_path():
    input = pd.DataFrame({"nullable_column": [1, 2, ".", 4]})
    expected = pd.DataFrame({"nullable_column": [1, 2, pd.NA, 4]})
    observed = clean_nas(input)
    assert expected.equals(observed)
```

This is known as a "happy path" test:
when given the nice inputs you expect,
the outputs are nice as well.
You will probably also want to test that your system works even when you throw some strange inputs at it.
These are called "edge cases."
Let's try writing one!

:::: challenge

### Writing a test for an edge case

Pick one of the functions that makes up the data pipeline.

What do you expect the output to look like?
Can you imagine some weird input that *might* break your function?

Try writing a test in `test_pipeline.py` that tells you what happens with that weird input!
If it fails with an error telling you that your function can't actually handle that weird input, that is a totally acceptable output of this challenge.

```python
def test_function_edge_case():
    # weird_input = ...
    # observed = function(weird_input)
    # expected = ...
    # assert ...
```
::::


#### Automated test runners

As we write more tests,
we're starting to run into some of the problems with our `if __name__ == "__main__":...` strategy:

- the boilerplate is annoying and it's easy to forget to add a test
- if you have lots of tests & want to break them into multiple files, you now have to run all these other files too
- if one test breaks it immediately exits with an `AssertionError` and now you don't know what else broke

What would be nice is some tool that
automatically finds testing code,
runs tests separately,
and reports the outputs of *all* your tests regardless of if one failed or not.
`pytest` solves all these quality-of-life problems and more.

While the fullness of `pytest` is quite complicated, the basics actually make our existing testing code simpler!

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
* it runs all those tests and makes a nice report


:::: challenge

#### Try `pytest`

Try running `uv run pytest tests/` in your own project and see if it's picking up your tests!
::::

### The debugger

We've found out which function isn't working right. How do we figure out why that function isn't working?

Options:
- break the function down into smaller parts and write more tests: sometimes a good idea, but often tedious and breaks up your code into unnecessarily small chunks
- throw in a bunch of `print(f"value of something is {something}")` statements: super easy, but kind of annoying to go back and keep adding more until you figure your stuff out. Plus then you have to delete them later to not clutter your output.
- use an **interactive debugger**!

An interactive debugger pauses your program at a specific spot (a "breakpoint"),
at which point you get to go in and poke around.
It can be super powerful and overwhelmingly complicated - let's go over the basics:

* how to get help: ?
* how to figure out what you're looking at & where you are in the execution: `l` `list`
* how to print out values of variables / expressions: `p` `pp`
* how to move: `next` vs `step`
* how to quit: `q`

do this in a live demo

:::: challenge

If your function fails your unit test, throw a breakpoint in the function & go check it out! Can you figure out what's going wrong?

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

Additional notes?

- `pytest --pdb`?
- stepping into library code is useful!

::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
