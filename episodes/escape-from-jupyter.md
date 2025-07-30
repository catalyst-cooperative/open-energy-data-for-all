---
title: "Escape from Jupyter!"
teaching: "ideally 20"
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I break up this giant notebook I have into smaller pieces?
- I want to collaborate with someone in another city. How can we effectively share work?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Identify limitations of Jupyter notebooks for collaborative and reproducible research
- Reorganize code from a Jupyter notebook into a Python script environment

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
Rather than using `python main.py`, we use `uv run` to run the script within our virtual
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

Let's add our first package. We can use `uv add` to add the Pandas package to our
virtual environment:

```bash
uv add pandas
```

In the terminal, you should be able to see that `uv` successfully added and installed
`pandas` and packages it relies on. In the `pyproject.toml` file, we can now see Pandas
listed in the dependencies:

```
dependencies = [
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

How do we actually run this code? We can amend the code block that begins with `if __name__ == "__main__"`. This section of the file tells us what happens when we run `uv run main.py`.

When we run this file directly (e.g., using `uv run main.py`), Python assigns this file the attribute `__name__` as `__main__`. While we might add many functions into `main.py`, we can use
this `if __name__ == "__main__":` code block to specify which functions we want to run, and even which variables they should take by default.

```python
if __name__ == "__main__":
    etl_pr_gen_fuel()
```

:::: challenge
Run this code using uv, and check to see that it saved the expected transformed files.
::::

### Importing your own code

In the last lesson, we wrote a number of generalizeable functions that could get reused across multiple contexts.

TODO:
- create utils.py
- add a docstring at the top explaining what the file contains
- import from utils.py into a notebook
- import from utils.py into main.py
- add a docstring there too
- general reflections on organization of modules


::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
