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

Jupyter notebooks can get us very far. But, when do Jupyter notebooks fail us?
- You have to make sure your collaborator has the same packages *and* versions of those packages installed as you.
- Having to re copy-paste a giant code block into the top of each notebook?
- Your collaborator identified a problem and fixed it in their notebook. But you copy-pasted the function into your
notebook and now you have to remember to update it in yours.
- Having to decipher what the heck your collaborator changed in a 2000 line notebook you’re both editing?
- Having to constantly scroll up and down to find that helpful function you wrote…. Somewhere?

In contrast, moving towards modules offers us numerous advantages:
- easy to see line-by-line changes you or others make
- easy to re-use code across multiple places
- organize code into discrete steps and themes, making it more legible to you and collaborators
- prevent you from accidentally defining multiple versions of `transform_eia_gen_fuel()` in the same file

### Creating a codebase

- Theoretically, what changes when we move from Jupyter notebooks?
-- Need to tell people to install packages (can't just add an install line up above)
-- some more stuff

- Introduce the concept of a virtual environment: wrapping your project up in a box - everything someone needs
to work on it (packages) is all there.

Like other tools you may have encountered (`pip`, `pyenv`, `virtualenv`), [`uv`](https://docs.astral.sh/uv/) is a tool that helps you install and update packages, and then share those exact installation
instructions with your peers. It also helps us set up a skeleton for our code project.

Open up your shell (see here for [OS-specific instructions](https://swcarpentry.github.io/shell-novice/index.html#open-a-new-shell).) In a terminal, navigate up one folder.
```shell
cd ..
```

Let's pick a name for our project, one that's short and doesn't use spaces: `pr-gen-fuel`.

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
document your project. For instance, who wrote it, what is in it, and how can people
get in contact with you? For an excellent 101 on what to put into a README,
we recommend [this Carpentries lesson](https://carpentries-lab.github.io/good-enough-practices/04-collaboration.html).

#### pyproject.toml
A TOML file is a standard configuration format used for Python projects. It can be used
to specify many, many things about project set-up. To get us started, we can see `uv` has included:
- name
- version: which version of the codebase this is, to help others keep track of updates.
- description: A short summary of the project (save longer descriptions for the readme).
- readme: What the `readme` file is called.
- requires-python: the version of Python your code uses
- dependencies: which packages are needed to run the code. Right now we can see we don't have any!

TODO: add some pyproject.toml reference.

#### Adding packages to uv
Let's add our first package:
```bash
uv add pandas
```

In the terminal, you should be able to see that `uv` successfully added and installed `pandas` and packages it relies on. In the `pyproject.toml` file, we can now see pandas listed in the dependencies:

```
dependencies = [
    "pandas>=2.3.1", # Your version might be different!
]
```

`pyproject.toml` allows us to set high-level requirements (e.g., pick whichever pandas version is newer than 2.3.1, don't yet upgrade to version 3.0 as it breaks my code).

In the corresponding `uv.lock` file, we can also see a ton of new information! While `pyproject.toml` gives us high-level instructions, `uv.lock` tells us which exact version of each package and which link it was installed from. This is the recipe other computers will follow to recreate the same environment when they setup your environment.

To keep our environment up to date as time goes on, we can run `uv sync`.

#### Challenge 1: setting up our working environment

What are the packages we were using before? let's add them.

:::: challenge
Which packages were we importing to transform the code in the previous module? Add these packages into your uv environment.
::::

#### Setting up our data pipeline

Let's move some code over:
- copy the data folder

- explain main() and  if __name__ == "__main__":
-- When this file is run directly (e.g., uv run main.py), execute the code in this section.
Right now: when we run main.py, run the main function.
-- We'll talk more about when *not* to use this in the next section.

- rename main.py to transform.py
- move over our first code block
- add in read/write if not in plotting already

:::: challenge
- run the damn thing using uv!
::::

###


** out of scope: we'll cover creating utils.py in the modularization lesson

::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
