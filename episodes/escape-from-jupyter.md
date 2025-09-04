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
changes you or others make to files, especially when using Github to collaborate.
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

Like other tools you may have encountered (`pip`, `pyenv`, `virtualenv`), [`uv`](https://docs.astral.sh/uv/) is a tool that helps you install and update Python packages, and then share those exact installation
instructions with your peers. In fact, if you've run any of the code in prior episodes,
you're already using `uv`! Helpfully, as we move away from Jupyter, we can use `uv` to set up a
skeleton for our code project.

:::: callout
If you haven't yet installed `uv`, follow the [setup instructions](../learners/setup.md) before continuing. Windows users, you should already have "Git Bash" installed locally if you've followed the [setup instructions](../learners/setup.md), and you can use this, Powershell or WSL for this lesson.
::::

Open up your shell (see here for [OS-specific instructions](https://swcarpentry.github.io/shell-novice/index.html#open-a-new-shell)). In a terminal, navigate up one folder.
```shell
cd ..
```

:::: instructor
Take a moment to check that your students are all one directory above the lesson content.
Otherwise, `uv` will create a workspace in the lesson's existing `uv` environment instead
of a new project.
::::

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
    "pandas>=2.3.2", # Your version might be different!
]
```

::::callout
Sometimes a new version is released that breaks our code, or contains a bug that hasn't
yet been fixed. `pyproject.toml` allows us to set high-level requirements
(e.g., pick whichever version is newer than 2.1, don't yet upgrade to version
3.0). `uv add` will specify sensible ranges by default, but we can override these ranges
in the `dependencies` section. For example:

```
dependencies = [
    "pandas>=2.2.9,<2.3.2",
]
```

::::

:::: instructor
The precise numbers of packages resolved, prepared and installed will vary for each
user. In case your students are curious:

- *Resolution*: Recursively searching for compatible package versions, ensuring that the
requested requirements are fulfilled and that the requirements of each requested package
are compatible. See [docs](https://docs.astral.sh/uv/concepts/resolution/) for more detail.
::::

In the corresponding `uv.lock` file, we can also see a ton of new information! While `pyproject.toml` gives us high-level instructions, `uv.lock` tells us which exact version of each package and which link it was installed from. This is the recipe other computers will follow to recreate the same environment when they setup your environment.

:::: callout
How do we keep our packages up to date as new versions are released? Luckily for us, we
don't have to think about it! Every time we use `uv run` to run our Python files,
`uv` will check for new package releases and update our environment.
::::


#### Setting up our data pipeline

Now let's migrate our code over. First, let's copy over our `data` folder and the `checkpoints/transform.ipynb` notebook
containing our modularized code from the last lesson into our project folder. The folder should now look like this:

```shell
ls
```

```
data  main.py  pyproject.toml  README.md  transform.ipynb  uv.lock
```

:::: instructor
If at any point students are struggling to get to this point, they can catch up by
unzipping the `pr-gen-fuel-init.zip` file from the `checkpoints` folder into a different
folder than the lesson is in.
::::

The `main.py` file provides a helpful skeleton for migrating our code.
In it, we can see two things:
1. a function called `main()` with a print statement
2. an if statement that calls `main` if `__name__ == "__main__"`

```python
def main():
    print("Hello from pr-gen-fuel!")


if __name__ == "__main__":
    main()
```

Let's start by replacing `main()`. We can migrate our modularized code from `transform.ipynb` into one main transformation function called `etl_pr_gen_fuel()`.

First, we can open up the notebook:

```shell
uv run jupyter notebook transform.ipynb
```

:::: instructor
Copy over the cells, with the import and utility function outside of `main()` and the remaining cells in `main()`. Once that's done, rename
`main()` to `transform_pr_gen_fuel()` and update the `if __name__ == "__main__":` to call that function instead.
::::

We should wind up with a block of code in `main.py` that looks like this:

:::: spoiler

```python
import pandas as pd
import numpy as np

# Silence some warnings about deprecated Pandas behavior
pd.set_option("future.no_silent_downcasting", True)

# Utility functions
def melt_monthly_vars(pr_gen_fuel: pd.DataFrame, melted_var: str) -> pd.DataFrame:
    """Melt many columns of monthly data for a single variable into a month and a value column.

    This code takes a table with data stored in one column per month and stacks all
    the fields for a single variable (fuel_consumed_for_electricity_mmbtu), returning
    a table with one month column and one value column for this variable in order to
    make it easier to plot our data over time. Note that this drops the other
    variables of data.

    Args:
        pr_gen_fuel: EIA 923 Puerto Rico generation fuel data.
        melted_var: The variable to be melted.
    """
    # set up shared index
    index_cols = ["plant_id_eia", "plant_name_eia", "report_year", "prime_mover_code", "energy_source_code", "fuel_unit"]
    
    var_cols = index_cols + [col for col in pr_gen_fuel.columns if col.startswith(melted_var)]
    var_df = pr_gen_fuel.loc[:, var_cols]

    ## Melt the fuel_consumed columns
    var_melt = var_df.melt(
        id_vars=index_cols,
        var_name="month",
        value_name=melted_var
    )
    var_melt["month"] = var_melt["month"].str.replace(f"{melted_var}_", "")
    var_melt = var_melt.set_index(index_cols + ["month"])
    return var_melt

def handle_data_types(pr_df: pd.DataFrame, categorical_cols: list[str]) -> pd.DataFrame:
    """Convert EIA 923 PR columns into desired data types.

    In addition to using the standard convert_dtypes() function, handle a series of
    non-standard data types conversions for associated_combined_heat_power
    and create categorical columns to save memory.

    Args:
        pr_df: Dataframe with EIA 923 Puerto Rico data.
        categorical_cols: List of columns that should be converted to a categorical dtype.
    """
    pr_df = pr_df.convert_dtypes()
    pr_df["associated_combined_heat_power"] = (
        pr_df["associated_combined_heat_power"]
        .astype("object") # necessary for the types to work for the .replace() call
        .replace({"Y": True, "N": False})
        .astype("boolean")
    )
    pr_df = pr_df.astype({col: "category" for col in categorical_cols})
    return pr_df

def transform_pr_gen_fuel():
    # Read in the raw data
    pr_gen_fuel = pd.read_parquet("data/raw_eia923__puerto_rico_generation_fuel.parquet")
    pr_plant_frame = pd.read_parquet("data/raw_eia923__puerto_rico_plant_frame.parquet")
    # Handle EIA null values
    pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA)

    # Convert data types (mmbtu/units to numeric, booleans, categories)
    pr_gen_fuel = handle_data_types(
            pr_gen_fuel,
            categorical_cols = ["energy_source_code","fuel_type_code_agg", "prime_mover_code", "reporting_frequency_code", "data_maturity", "plant_state"]
                                )

    for colname in pr_gen_fuel.columns: # TODO: Do we need this? Check.
        if (
            "fuel_consumption" in colname
            or "fuel_consumed" in colname
            or "net_generation" in colname
            or "fuel_mmbtu_per_unit" in colname
        ):
            pr_gen_fuel[colname] = pr_gen_fuel[colname].astype("float64")
            
    # Handle EIA null values
    pr_plant_frame = pr_plant_frame.replace(to_replace = ".", value = pd.NA)

    # Convert data types (mmbtu/units to numeric, categories, booleans)
    pr_plant_frame = handle_data_types(pr_plant_frame, categorical_cols = ["reporting_frequency_code", "data_maturity", "plant_state"])

    #### monthly pivoting
    # Pivot variable columns
    fuel_elec_mmbtu_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_for_electricity_mmbtu")
    fuel_elec_units_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_for_electricity_units")
    fuel_mmbtu_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_mmbtu")
    fuel_units_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_units")
    net_gen_melt = melt_monthly_vars(pr_gen_fuel, "net_generation_mwh")

    # Combine all the pivoted DFs
    pr_gen_fuel_melt = pd.concat(
        [fuel_elec_mmbtu_melt, fuel_elec_units_melt, fuel_mmbtu_melt, fuel_units_melt, net_gen_melt],
        axis="columns",
    ).reset_index()

    ## Create date from month and year
    pr_gen_fuel_melt["date"] = pd.to_datetime(
        pr_gen_fuel_melt["month"] + pr_gen_fuel_melt["report_year"].astype(str),
        format="%B%Y",
    )
    ## Drop old date columns
    pr_gen_fuel_clean = pr_gen_fuel_melt.drop(columns = ["report_year", "month"])

    # Plant 62410 has two 2020 data entries but one is null
    # Drop the bad row
    pr_gen_fuel_final = pr_gen_fuel_clean.loc[
        ~((pr_gen_fuel_clean.plant_id_eia == 62410) 
        & (pr_gen_fuel_clean.date.dt.year == 2020)
        & (pr_gen_fuel_clean.fuel_consumed_for_electricity_mmbtu.isnull()))
    ]

    # drop after 2025-03-01 (for now) as these values should not exist
    pr_gen_fuel_final = pr_gen_fuel_final.loc[pr_gen_fuel_clean.date < pd.Timestamp("2025-03-01")]

    ### output the data to Parquet files
    pr_gen_fuel_final.to_parquet("data/pr_gen_fuel_monthly.parquet")
    pr_plant_frame.to_parquet("data/pr_plant_frame.parquet")

if __name__ == "__main__":
    transform_pr_gen_fuel()
```

:::: spoiler

Let's try and run this code:

```shell
uv run main.py
```

Hm, looks like we got an import error:

```shell
ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'.
A suitable version of pyarrow or fastparquet is required for parquet support.
Trying to import the above resulted in these errors:
 - Missing optional dependency 'pyarrow'. pyarrow is required for parquet support. Use pip or conda to install pyarrow.
 - Missing optional dependency 'fastparquet'. fastparquet is required for parquet support. Use pip or conda to install fastparquet.
```

:::::::: challenge
Use `uv` to install the missing packages.

:::: solution
Run `uv add pyarrow fastparquet`.
::::

::::::::

Let's try that again:

```shell
uv run main.py
```

If we check our `data` folder, we can see we created two new files!

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
migrate over the `melt_monthly_vars()` and `handle_data_types()` functions we wrote in the last episode:

:::: spoiler
```python
import pandas as pd
import numpy as np

# Silence some warnings about deprecated Pandas behavior
pd.set_option("future.no_silent_downcasting", True)

# Utility functions
def melt_monthly_vars(pr_gen_fuel: pd.DataFrame, melted_var: str) -> pd.DataFrame:
    """Melt many columns of monthly data for a single variable into a month column and a value column.

    This code takes a table with data stored in one column per month and stacks all the fields for a
    single variable (fuel_consumed_for_electricity_mmbtu), returning a table with one month column
    and one value column for this variable in order to make it easier to plot our data over time.
    Note that this drops the other variables of data.

    Args:
        pr_gen_fuel: EIA 923 Puerto Rico generation fuel data.
        melted_var: The variable to be melted.
    """
    # set up shared index
    index_cols = ["plant_id_eia", "plant_name_eia", "report_year", "prime_mover_code", "energy_source_code", "fuel_unit"]
    
    var_cols = index_cols + [col for col in pr_gen_fuel.columns if col.startswith(melted_var)]
    var_df = pr_gen_fuel.loc[:, var_cols]

    ## Melt the fuel_consumed columns
    var_melt = var_df.melt(
        id_vars=index_cols,
        var_name="month",
        value_name=melted_var
    )
    var_melt["month"] = var_melt["month"].str.replace(f"{melted_var}_", "")
    var_melt = var_melt.set_index(index_cols + ["month"])
    return var_melt

def handle_data_types(pr_df: pd.DataFrame, categorical_cols: list[str]) -> pd.DataFrame:
    """Convert EIA 923 PR columns into desired data types.

    In addition to using the standard convert_dtypes() function, handle a series of
    non-standard data types conversions for associated_combined_heat_power
    and create categorical columns to save memory.

    Args:
        pr_df: Dataframe with EIA 923 Puerto Rico data.
        categorical_cols: List of columns that should be converted to a categorical dtype.
    """
    pr_df = pr_df.convert_dtypes()
    pr_df["associated_combined_heat_power"] = (
        pr_df["associated_combined_heat_power"]
        .astype("object") # necessary for the types to work for the .replace() call
        .replace({"Y": True, "N": False})
        .astype("boolean")
    )
    pr_df = pr_df.astype({col: "category" for col in categorical_cols})
    return pr_df
```
:::: spoiler

Because we only want to use this function in other contexts and not run any of the
functions in this file, we don't need to include an `if __name__ == "__main__":` block.

#### Importing your code into a notebook

Now that we've created our `utils.py` file, we can use it in a Jupyter notebook
just like any other package by importing it.

```shell
uv run jupyter notebook transform.ipynb
```

```python
import utils
```

Better yet, we can access the excellent documentation we've written about it.

```python
help(utils)
help(utils.handle_data_types)
```

Now we can use our functions in any notebook we write, without having to copy it over
into a cell at the top - nice!

#### Importing your code into `main.py`

The same is true in our `main.py` file.

::: challenge
From `utils`, import our helper functions into `main.py`. Test that this works by re-running
the script using uv.
:::

Now, when you make a tweak to `handle_data_types()`, that tweak will be applied across
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
