---
title: "Escape from Jupyter!"
teaching: 45
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
you can store essential functions in one place and reuse them across your code, similar to how you'd import a
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
Using CPython 3.13.5
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
    "pandas>=3.0.2", # Your version might be different!
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

Now let's migrate our code over. First, let's copy over the file and the `data` folder in the `checkpoints/escape-from-jupyter` folder into our project folder. They contain our modularized code from the last lesson. The folder should now look like this:

```shell
ls
```

```
data  etl.ipynb  main.py  pyproject.toml  README.md  uv.lock
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

Let's start by replacing `main()`. We can migrate our modularized code from `etl.ipynb` into one main transformation function called `etl_pr_gen_fuel()`.

First, we can open up the notebook:

```shell
uv run jupyter notebook etl.ipynb
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

def load_generation_data(path):
    """Load the cleaned Puerto Rico generator operations data from disk.

    Args:
        path: Path to raw data file on disk.
    """
    return pd.read_parquet(path)

def write_generation_data(df, path):
    df.to_parquet(path)
    return


def map_code_to_strings(df, mapped_col, code_dictionary):
    """Convert a column of codes into strings defined by a dictionary.

    This code takes a dataframe with a column of codes and returns a dataframe with the same column
    mapped to strings to prevent users from needing to consult a look-up table. The relationship between columns and strings is defined by a dictionary.

    Args:
        df: A Pandas DataFrame.
        mapped_col: The name of the column to be mapped.
        code_dictionary: A dictionary containing code-string pairs.
    """
    assert all([code in code_dictionary for code in df[mapped_col].unique()]) # Check all codes present
    df['code_name'] = df[mapped_col].replace(code_dictionary)
    df = df.drop(columns=mapped_col).rename(columns={'code_name':mapped_col})
    return df

def handle_thousands_fuel_units(df, thousands_unit: str):
    """Where the fuel unit column contains a small number of thousands, multiply by 1000 and update the unit label.

    This expects the thousands_unit to be in a column called "fuel_unit", and the units column to live in a
    column called "fuel_consumed_for_electricity_units".

    Args:
        df: A Pandas DataFrame.
        unit_column: The column containing unit names.
        thousands_unit: The name of the unit to be normalized.
    """
    df.loc[df.fuel_unit == thousands_unit,"fuel_consumed_for_electricity_units"] = df.loc[df.fuel_unit == thousands_unit, "fuel_consumed_for_electricity_units"]*1000
    df.loc[df.fuel_unit == thousands_unit, "fuel_unit"] = df.loc[df.fuel_unit == thousands_unit].fuel_unit.str.replace("thousand ", "")
    return df


def transform_pr_gen_fuel():
    raw_pr_gen_fuel = load_generation_data(path="data/pr_gen_fuel_monthly.parquet")
    # Standardize NAs
    pr_gen_fuel = raw_pr_gen_fuel.replace(to_replace = ".", value = pd.NA)
    pr_gen_fuel = pr_gen_fuel.replace(to_replace = "null", value = pd.NA)

    # convert codes to strings
    ENERGY_SOURCE_DICT = {'WND':'wind', 'NG':'natural_gas', 'SUN':'solar',
                        'BIT':'bituminous_coal', 'MWH':"electricity_for_energy_storage",
                        'DFO':'distillate_fuel_oil', 'RFO':'residual_fuel_oil', 'WAT':'hydro'}

    PRIME_MOVER_CODE_DICT = {
        'WT':'onshore_wind', 'CA':'cc_steam', 'CT':'cc_combustion_turbine',
        'PV':'photovoltaic', 'ST':'steam_turbine', 'BA':'battery',
        'IC': 'internal_combustion', 'GT': 'gas_turbine', 'HY':'hydraulic_turbine'
    }

    pr_gen_fuel = map_code_to_strings(df = pr_gen_fuel, mapped_col = "energy_source_code", code_dictionary = ENERGY_SOURCE_DICT)
    pr_gen_fuel = map_code_to_strings(df = pr_gen_fuel, mapped_col = "prime_mover_code", code_dictionary = PRIME_MOVER_CODE_DICT)

    pr_gen_fuel = handle_thousands_fuel_units(pr_gen_fuel, thousands_unit = "thousand_short_tons")
    pr_gen_fuel = handle_thousands_fuel_units(pr_gen_fuel, thousands_unit = "thousand barrels")

    # drop after 2025-03-01 (for now) as these values should not exist
    pr_gen_fuel = pr_gen_fuel.loc[pr_gen_fuel.date < pd.Timestamp("2025-03-01")]

    ### save cleaned file
    write_generation_data(pr_gen_fuel, "data/pr_gen_fuel_monthly_clean.parquet")

if __name__ == "__main__":
    transform_pr_gen_fuel()
```

::::

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
general purpose functions from our EIA 923-specific code in another file.

Let's start by copying the `main.py` file and renaming it `utils.py`. In this file, let's
only keep the `melt_monthly_vars()` and `handle_data_types()` functions we wrote in the last episode:

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
::::

Because we only want to use this function in other contexts, we don't need to include
an `if __name__ == "__main__":` block.

#### Importing your code into a notebook

Now that we've created our `utils.py` file, we can use it in a Jupyter notebook
by importing it.

```shell
uv run jupyter notebook etl.ipynb
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
Import our helper functions from `utils.py` into `main.py`. Test that this works by re-running
the script using uv.
:::

Now, when you make a tweak to `handle_data_types()`, that tweak will be applied across
all of your code immediately. No more copy-pasting!

:::: callout
As your code grows in complexity, you might find yourself wanting to reorganize your scripts into folders, call custom commands from the command-line, or even distribute your code so anyone else can install it using tools like `uv`. If so, you'll likely want to re-organize your code into a package.

Running `uv init --package your-project-name` will create the skeleton for a Python package, just as `uv init pr-gen-fuel` created our project template above. See the [uv docs](https://docs.astral.sh/uv/concepts/projects/init/#packaged-applications) for more detail.

For more on Python packages, see these [Python docs](https://docs.python.org/3/tutorial/modules.html#packages) and this [explainer](https://docs.astral.sh/uv/concepts/projects/config/#project-packaging) from uv.
::::

::::::::::::::::::::::::::::::::::::: keypoints

- Jupyter is great for data exploration and visualization, but working with scripts
and modules is preferable for reusability, legibility and collaboration
- `uv` bundles packages into a virtual environment, and helps us move our code into
a codebase
- Reorganizing code into multiple modules can help us reuse code in multiple places and
keep our project organized.

::::::::::::::::::::::::::::::::::::::::::::::::
