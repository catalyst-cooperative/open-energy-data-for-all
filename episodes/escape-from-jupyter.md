---
title: "Escape from Jupyter!"
teaching: 20
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I break up this giant notebook I have into smaller pieces?
- How can I effectively reuse modularized functions in multiple places?
- I want to collaborate with someone in another city. How can I get them to run my code?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Identify limitations of Jupyter notebooks for collaborative and reproducible research
- Reorganize code from a Jupyter notebook into series of Python scripts
- Use `uv` to create a virtual environment and codebase

::::::::::::::::::::::::::::::::::::::::::::::::

So far, we've been doing all of our code extraction, exploration, transformation and
documentation in Jupyter notebooks. Jupyter notebooks are incredibly versatile, and
are incredibly useful starting points for data exploration and visualization. Yet as
your code grows more complex or you start to collaborate with others, you might find
it increasingly challenging to work entirely in Jupyter notebooks.

In contrast, moving towards coding in scripts and modules offers us numerous advantages:
- **Keep code organized:** Having to constantly scroll up and down to find that helpful function you wrote… somewhere?
By organizing code into discrete steps and themes (e.g., one file per dataset), you and your collaborators can easily find relevant code.
- **Track changes:** Using .py files and modules makes it easy for to see line-by-line
changes you or others make to files.
- **Concretize final code:** While you might test out three versions of a `transform_eia_gen_fuel()`
function in a Jupyter notebook or make four exploratory plots, you'll ultimately want to make sure
you're running the code you need for your final transformation process, and *only* that code. Moving
to modules helps us distinguish between our exploration process and our final code.
- **Reuse code:** Rather than copy-pasting a useful snippet or function into each notebook you're working in,
you can store essential functions in one place and reuse them across your code, just like you'd import any other
Python package.
- **Test your code:** We'll cover this next! In short, using scripts and modules unlocks a world of tools
you can use to test, debug and correct your code.

### Creating a codebase

What changes when we move our code out of a Jupyter notebook? One of the first roadblocks
to creating a codebase is specifying which packages need to be installed to run your code.
We have to make sure that collaborators have the same packages *and* versions of those
packages installed to avoid unexpected problems.

Luckily for us, developers have made it possible to set up a **virtual environment**
in which to run any code we write. A virtual environment is a box that you can use to
wrap up your project and hand it over to a collaborator - it tells their computer how to
replicate the environment you used when developing your code (e.g., which packages, which Python version).

Like other tools you may have encountered (`pip`, `pyenv`, `virtualenv`), [`uv`](https://docs.astral.sh/uv/) is a tool that helps you install and update packages, and then share those exact installation
instructions with your peers. In fact, if you've run any of the code in prior episodes,
you're already using `uv`! Helpfully, as we move away from Jupyter, we can use `uv` to set up a
skeleton for our code project.

:::: callout
If you haven't yet installed `uv`, follow the [setup instructions](../learners/setup.md) before continuing.
::::

Open up your shell (see here for [OS-specific instructions](https://swcarpentry.github.io/shell-novice/index.html#open-a-new-shell).) In a terminal, navigate up one folder.
```shell
cd ..
```

Let's pick a short but descriptive name for our project (avoid using spaces): `pr-gen-fuel`.

Now, run:
```shell
uv init pr-gen-fuel
```

What happened? If we navigate to the new folder that has been created, we can see a series
of new files.

```shell
cd pr-gen-fuel
ls
```

```
main.py  pyproject.toml  README.md
```

We'll talk through each file in a moment, but first, let's just try and run our `.py` file.
We will use `uv run` to run the script within our virtual
environment.

```shell
uv run main.py
```

```
Using CPython 3.13.2
Creating virtual environment at: .venv
Hello from pr-gen-fuel!
```

What did we just do? Since this is a brand new environment, `uv` set up a virtual
environment, and ran this Python script from within it.

Let's revisit our list of files:

```shell
cd pr-gen-fuel
ls
```

```
main.py  pyproject.toml  README.md uv.lock
```

A new file has appeared! Before we get to our Python script itself, let's talk through
each of these other files in turn.

#### READMEs
`README.md` is a [Markdown](https://www.markdownguide.org/) file that you can use to
document your project. Any information about what your project is, who has worked on it,
and how to get in touch with the authors should live here. For an excellent 101 on what
to put into a README, we recommend [this Carpentries module](https://carpentries-lab.github.io/good-enough-practices/04-collaboration.html).

#### pyproject.toml
A TOML file is a standard configuration format used for Python projects. It can be used
to specify many, many things about project set-up. To get us started, we can see `uv` has included:
- name: the name you specified when running `uv init`.
- version: which version of the codebase this is, to help others keep track of updates.
- description: A short summary of the project (save longer descriptions for the readme).
- readme: What the `readme` file is called.
- requires-python: the version of Python your code uses
- dependencies: which packages are needed to run the code. Right now we can see we don't have any!

For more information on `pyproject.toml` files, we recommend this
[Python packaging user guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/),
which identifies additional fields you can add to your TOML file and provides a full example.

#### Adding packages to uv

Let's add our first package. We can use `uv add` to add the Pandas package and Jupyter
to our virtual environment, seperating the packages by a space:

```bash
uv add pandas jupyter
```

In the terminal, you should be able to see that `uv` successfully added and installed
`pandas`, `jupyter` and all the packages they rely on. In the `pyproject.toml` file,
we can now see Pandas and Jupyter listed in the dependencies:

```
dependencies = [
    "jupyter>=1.1.1",
    "pandas>=2.3.1", # Your version might be different!
]
```

::::callout
Sometimes a new version is released that breaks our code, or contains a bug that hasn't
yet been fixed. `pyproject.toml` allows us to set high-level requirements
(e.g., pick whichever version is newer than 2.3.1, don't yet upgrade to version
3.0). `uv add` will specify sensible ranges by default, but we can override these ranges
in the `dependencies` section. For example:

```
dependencies = [
    "pandas>=2.2.9,<2.3.1",
]
```

::::

In the corresponding `uv.lock` file, we can also see a ton of new information! While `pyproject.toml` gives us high-level instructions, `uv.lock` tells us which exact version of each package and which link it was installed from. This is the recipe other computers will follow to recreate the same environment when they setup your environment.

:::: callout
How do we keep our packages up to date as new versions are released? Luckily for us, we
don't have to think about it! Every time we use `uv run` to run our Python files,
`uv` will check for new package releases and update our environment.
::::

#### Challenge 1: setting up our working environment

What are the packages we were using before? Let's add them.

:::: challenge
Which packages do we import in our `etl.ipynb` notebook? Add these packages into your uv environment.
::::

#### Setting up our data pipeline

Now let's migrate our code over. First, let's copy over our `data` folder into our
project folder. The folder should now look like this:

```shell
ls
```

```
data  main.py  pyproject.toml  README.md  uv.lock
```

The `main.py` file provides a helpful skeleton for migrating our code.
In it, we can see two things:
1. a function called `main()` with a print statement
2. an if statement that calls `main` if `__name__ == "__main__"`

Let's start by replacing `main()`. We can migrate our modularized code from `etl.ipynb` into one main transformation function called `etl_pr_gen_fuel()`.

```python
import somestuff
#TODO add the freaking code.
```

How do we actually run this code? We can amend the code block that begins with `if __name__ == "__main__"`.
This section of the file helps us distinguish between what we want to have happen when we
run this script directly (e.g., use `uv run main.py`) and what we want to happen when we
use this code in any other context (e.g., import it into a Jupyter notebook).

`__name__` is a built-in variable in Python; a variable that gets set by the system and not by you.
When we run this file directly (e.g., using `uv run main.py`), Python sets the value of `__name__` to the string `"__main__"`.
We can use this `if __name__ == "__main__":` block to specify which code we want
to run *only when we run the script directly*.
Calling our pipeline function in this `if` block will prevent us from running the entire
transformation unexpectedly in other contexts.

```python
if __name__ == "__main__":
    etl_pr_gen_fuel()
```

:::: challenge
Run this code using uv, and check to see that it saved the expected transformed files.
::::

### Importing your own code

In the last lesson, we wrote a number of generalizeable functions that could get reused
across multiple contexts. In order to keep things organized, we can split out these
general purpose functions from our EIA 923-specific code by creating another script.

:::: callout
A note on terminology:
- **File:** A file can contain many things - documentation, code definitions, or code that
can be run.
- **Script:** A file that contains code that can be run directly (e.g., `main.py`)
- **Module:** A piece of code that can be used in other contexts (e.g., the `pandas` library, or a sub-section of a library (e.g., `pandas.eval`))
::::

Let's start by creating a new file, and call it `utils.py`. In this file, let's
migrate over the `TODOFUNCTIONNAME()` function we wrote in the last episode:

```python
import somestuff

def TODOFUNCTIONNAME():
    # some code
    return something
```

Because we only want to use this function in other contexts and not run any of the
functions in this file, we don't need to include an `if __name__ == "__main__":` block.

#### Importing your code into a notebook

Now that we've created our `utils.py` file, we can use it in a Jupyter notebook
just like any other package by importing it.

```python
import utils
```

Better yet, we can access the excellent documentation we've written about it.

```python
help(utils)
help(utils.TODOFUNCTIONNAME)
```

#### Importing your code into `main.py`

The same is true in our `main.py` file.

::: challenge
Import `utils` and replace existing references to `TODOFUNCTIONNAME` with
`utils.TODOFUNCTIONNAME()`.
:::

Now, when you make a tweak to `TODOFUNCTIONNAME`, that tweak will be applied across
all of your code immediately. No more copy-pasting!

As your code grows, you can use modules and imports to reorganize your project into
multiple files in folders and subfolders, as makes sense to you. Here are but a few options:
- One script per dataset (e.g., `eia923_pr.py`, `eia860_pr.py`, `eia923_nonpr.py`), with a general `utils.py` file
- One folder per step of the data transformation process (e.g., `extract`, `transform`, `load`)

::::::::::::::::::::::::::::::::::::: keypoints

- Jupyter is great for data exploration and visualization, but working with scripts
and modules is preferable for reusability, legibility and collaboration
- `uv` bundles packages into a virtual environment, and helps us move our code into
a codebase
- Reorganizing code into multiple modules can help us reuse code in multiple places and
keep our project organized.

::::::::::::::::::::::::::::::::::::::::::::::::
