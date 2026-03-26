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


:::: instructor

Prep checklist:

* [ ] make a [google doc](https://www.docs.new) for challenges

::::

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

We'll start by looking at an example of a system-in-progress
and forming some hypotheses about what it *should* be doing -
what the inputs are, yes,
but also what we expect the outputs to look like.

Then we'll write some code that checks if the system is doing the right thing.
Along the way, we'll get to play with the *debugger*,
a tool that lets you pause your program and investigate what's going wrong.

Finally, we'll introduce a library that helps you organize the testing code you just wrote,
and deal with the painful parts of a growing test suite.


## Inputs and outputs

TODO
"Let's look in checkpoints/... - there's a small python project in there, that reads the raw EIA923 PR input files, does some cleaning, and creates a new table with some analysis of the cleaned data. Let's specifically look at the do_analysis function."

TODO
* make some code that has a subtle bug in it that deals with eia 923 data from PR

* have a docstring which describes the intent of the code

:::: instructor

Use VS Code here.

::::

:::: callout
Make sure you open this with a text editor or a code-specific program -
VSCode, PyCharm, Notebook, TextEdit, etc. will all work.
Microsoft Word, LibreOffice,
or anything that lets you bold/italicize/underline text will not.
::::

:::: challenge

### Challenge: characterize the function

Look at this function!

TODO think about connecting this back to the assumptions work earlier.

What are the inputs to this function? What do you think is true about them?

What are the outputs from this function? What do you think is true about them?

Write these down in the Google Doc.

::::

## Test functions

Now that we know *what* to expect,
let's figure out if those expectations are fulfilled.
We can use the `assert` statement we introduced in the assumptions lesson.
That can absolutely work to tell you if your system is functioning as expected.
But oftentimes the assertion code is complicated,
and can be confusing to have next to the "actual" code.

We can fix that by extracting the assertion logic out into its own function!
Think of it as modularizing your test code.
Let's do it!

:::: instructor

Encourage people to really follow along on their own, something like:

"The tools we use here are *very* interactive,
so it will be a lot easier to learn if you are *literally* typing out the commands with your fingers
instead of trying to remember all the things I'm doing.
If you need a minute to get set up, or fall behind,
throw up the NO react in Zoom and we'll give you time to catch up."

::::

Start by creating a new file, `test_main.py`.
Because of how we've set up the package structure,
we need to keep it in the same directory as `main.py` and `utils.py`.

Next we need to pick something to test.

One thing we expect from the output is that
there's a `fuel_consumption_units` column and that its value is 0 for sun, wind, and water.

Let's start writing the test.
We start with an `assert False` to make sure we will notice if the test fails:


```python
def test_renewables_fuel_units():
    assert False
```

Now let's run it:

```
$ uv run test_main.py
```

Hmm... no assertion error shows up, something's fishy.
We need to add the test function to the `if __name__ == "__main__":` block in order for it to run.

```python
if __name__ == "__main__":
    test_renewables_fuel_units()
    # future tests get added here too
```

Now if we run it we'll get an `AssertionError`. Hooray!
Always good to know that the test code will actually yell at you if it fails.

Now let's actually write the test - we need to take the following steps:

```python
def test_renewables_fuel_units():
    # Read in the raw data...
    # Then run the code...
    # Then pull out the subset we care about...
    # Finally, assert something!
    assert False
```

This can get a little confusing since we haven't worked with the data much yet.
It sure would be nice if we could investigate each step interactively,
sort of like what we'd do in a Jupyter noteboook.


### Debugger introduction

We can use the Python debugger, `pdb`, to do exactly that.
Let's try it out!

The first thing we need to do is add a *breakpoint* to the code,
a place where we are going to pause our code and mess around inside it.
We do this with the `breakpoint()` function:

```python
from main import extract_pr_gen_fuel, transform_pr_gen_fuel

def test_renewables_fuel_units():
    breakpoint()
    # Read in the raw data...
    raw_pr_gen_fuel, raw_pr_plant_frame = extract_pr_gen_fuel()
    # Then run the code...
    pr_gen_fuel, pr_plant_frame = transform_pr_gen_fuel(
        raw_pr_gen_fuel, raw_pr_plant_frame
    )
    # Then pull out the subset we care about...
    # Finally, assert something!
    assert False
```

Running this drops you into this cryptic situation:

```bash
% uv run test_main.py
> /home/daz/work/open-energy-data-for-all/checkpoints/making-sure-your-system-is-behaving-start/test_main.py(5)test_renewables_fuel_units()
-> breakpoint()
(Pdb)
```

If you're seeing that, you've successfully hit the breakpoint.
In hacker parlance, "you're in."
That `(Pdb)` is a prompt for further commands.

A good first command is `list`
(or `l` - most of the common commands have one-letter abbreviations):

TODO show output

This shows some context around where the code execution has been paused.
The arrow at line 5 shows the line of code that's *about* to run.

Note that if you type `list` again it will keep scanning down through the file
until it hits the end of the file (`EOF`):

TODO show output

Now that we know where we are, what else can we do here?
We can:

* run the next step of the code as written and see what happens
* type some new code and see the results

TODO: show the following
* `next` (gets extracted stuff into scope)
* evaluating expressions (show the extracted stuff & call methods on it)
* show that the next line hasn't executed yet and you get a name error
* `step`/`return` to get the transforms in
* a bunch of variable assignment to get the subset we want & the assertion we care about
* `quit`
* paste the assertion code into the test function and run again
* this time, hit `continue` to continue execution
* hooray it works!

Now it's your turn.

:::: challenge

### Writing a test function

Think about the data processing code in `main.py` and the output expectations we came up with.

Pick one of those expectations and write a function in `test_main.py` that tests it. Start with the following skeleton:

TODO check if this still works with the new ETL

```python
def test_cool_output_property():
    # Read in the raw data...
    raw_pr_gen_fuel, raw_pr_plant_frame = extract_pr_gen_fuel()
    # Then run the code...
    pr_gen_fuel = transform_pr_gen_fuel(raw_pr_gen_fuel, raw_pr_plant_frame)[0]
    breakpoint()
    # Then pull out the subset we care about...
    # Finally, assert something!
```

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

### Example: fixtures

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


## Conclusion

"How to find what's going wrong with your system" is an extremely deep topic,
with lots and lots of tools that people have worked on through the years.
We've just started exploring this, through the basic strategy applies everywhere:

* identify bad outputs of your system
* investigate the subsystems that produced the bad outputs - are they flawed or did they get fed bad inputs?
* repeat

We introduced some tools to help with this strategy:
an automated test runner and the test functions that go with it make the loop go much more smoothly;
a debugger lets you investigate your system much more effectively.
