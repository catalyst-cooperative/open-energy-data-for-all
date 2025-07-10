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

So we just wrote a little data pipeline... how do we know it works?

- think of what properties you expect from the whole system output
- look at output and see if those properties hold

Then if it doesn't work, what do we do?

- check sub-parts of the system - did it get the right input? did it produce the right output?
- repeat fractally until you find the specific cause of the problem

In this episode, we'll introduce some tools that help make this process smoother:

- integration tests: tell you if your system is functioning as expected
  - mention that it's probably good to write tests about the input data assumptions too...
- unit tests: tell you if the subparts of your system are functioning as expected
- automated test runner: makes it easy to run all your tests at once so you don't have to remember/manually execute all the steps
- debugger: lets you zoom in even further to your system to figure out what exactly is happening

### Integration tests


blah blah

:::: challenge

#### Writing an integration test

Think about the pipeline we made together in the modularization episode.

:::::::: instructor

**TODO**
We can also prepare a separate broken pipeline in case we run this standalone.

::::::::

What is a property that you expect the output to have? Write a function that tests this, by filling out the following skeleton:

**TODO** get the right filenames/function names
```python
def test_cool_output_property():
    input_data = pd.read_parquet(...)
    output = process(input_data)
    # make some assertions about the data
```
::::

#### Unit tests

- show a happy path test

:::: challenge

### Writing a unit test

Pick one of the functions that makes up the data pipeline.

What do you expect the output to look like?
Can you imagine some weird input that *might* break your function?

Try writing a test that tells you if that weird input breaks things or not!

```python
def test_function_edge_case():
    # weird_input = ...
    # observed = function(weird_input)
    # expected = ...
    # assert expected == observed
```

**TODO what if you want to grab a sub-property of `function(weird_input)` instead of the whole output? adjust skeleton**

::::


#### Automated test runners

OK, how do we run these tests?

We could add `if __name__ == "__main__":...` to tests.py and run `uv run tests.py`

But that runs into problems:
- annoying boilerplate
- if you have lots of tests & want to break them up you now have to run all these other files
- if one test breaks it immediately exits with an `AssertionError` and now you don't know what else broke

Enter `pytest` - solves all these quality-of-life problems and more.
Lots of docs and functionality, we'll just touch on the basic bit where it discovers tests and runs them for you.

### Example: a pytest test & how to run it

* use `test_`
* use `assert`
* `uv run pytest`

Oooooh pretty output :heart_eyes:

:::: challenge

#### Try `pytest`

**TODO do we need to make them install pytest in their project?**

To install `pytest` we can add it to the `pyproject.toml` dependency list as before, then run `uv sync`.

Try running `uv run pytest` in your own project and see if it's picking up your tests!
::::

### The debugger

We've found out which function isn't working right. How do we figure out why that function isn't working?

Options:
- break the function down into smaller parts and write more unit tests: sometimes a good idea, but often tedious and breaks up your code into unnecessarily small chunks
- throw in a bunch of `print(f"value of something is {something}")` statements: super easy, but kind of annoying to go back and keep adding more until you figure your stuff out
- use the **interactive debugger** wheeeeee

Interactive debugger pauses your program at a specific spot ("breakpoint") and then you get to go in and poke around. Super powerful, lots of documentation here as well, but let's go over the basics:

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
