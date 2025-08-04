---
title: "Modularization"
teaching: 30
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I re-use code I've already written to address similar problems?
- How can I reduce duplication in my code?
- How can I clearly communicate what my code is doing?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use a "plain language" strategy to help decide how best to design your functions
- Structure code to isolate discrete, inspectable steps
- Design code modules for clarity and reuse

::::::::::::::::::::::::::::::::::::::::::::::::

As we explore our data, assert assumptions about it and transform it to meet those
assumptions, it's easy to quickly write hundreds of lines of code. Yet as our code grows,
it can get increasingly repetitive, confusing, and challenging to explain to others.
In this lesson, we'll explore practical approaches to **modularizing** our code - breaking
it into smaller chunks we can reuse, test, and combine to transform our data.

## A plain language approach to code reorganization

We can start by looking at a single cell of code from the `etl.ipynb` notebook:

```python
# Pivot fuel_consumed_for_electricity MMBTU columns

fuel_elec_mmbtu_cols = index_cols + [col for col in pr_gen_fuel.columns if "fuel_consumed_for_electricity_mmbtu" in col]
fuel_elec_mmbtu = pr_gen_fuel.loc[:, fuel_elec_mmbtu_cols]

## Melt the fuel_consumed columns
fuel_elec_mmbtu_melt = fuel_elec_mmbtu.melt(
    id_vars=index_cols,
    var_name="month",
    value_name="fuel_consumed_for_electricity_mmbtu"
)
fuel_elec_mmbtu_melt["month"] = fuel_elec_mmbtu_melt["month"].str.replace("fuel_consumed_for_electricity_mmbtu_", "")
fuel_elec_mmbtu_melt = fuel_elec_mmbtu_melt.set_index(index_cols + ["month"])
fuel_elec_mmbtu_melt
```

What does this code do? It transforms a table that looks like this:

| plant_id_eia | plant_name_eia | report_year | prime_mover_code | energy_source_code | fuel_unit | fuel_consumed_for_electricity_mmbtu_january | fuel_consumed_for_electricity_mmbtu_february |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 61034 | EcoElectrica | 2017 | CA | NG | mcf | 4773.0 | 0.0 |
| 61034 | EcoElectrica | 2017 | CT | NG | mcf | 2195139.0 | 2044214.0 |

into a table that looks like this:

|  | plant_id_eia | plant_name_eia | report_year | prime_mover_code | energy_source_code | fuel_unit | month | fuel_consumed_for_electricity_mmbtu |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1801 | 61034 | EcoElectrica | 2017 | CA | NG | mcf | january | 4773.0 |
| 1351 | 61034 | EcoElectrica | 2017 | CA | NG | mcf | february | 0.0 |
| 1802 | 61034 | EcoElectrica | 2017 | CT | NG | mcf | january | 2195139.0 |
| 1352 | 61034 | EcoElectrica | 2017 | CT | NG | mcf | february | 2044214.0 |

Or, in words: this code takes a table with data stored in one column per month and stacks all the fields for a single variable (fuel_consumed_for_electricity_mmbtu), returning a table with one month column and one value column for this variable in
order to make it easier to plot our data over time.

:::::::: challenge
Open `notebooks/etl.ipynb`. Do you see any code that performs this same task? What differences do you note between the code itself?

:::: solution
Cells 6, 7, 8, and 9 all do the same thing. Note that each cell does this for a different variable (e.g., "fuel_consumed_units" instead of "fuel_consumed_for_electricity_mmbtu"). In cell 9, we also see that the way we're selecting the columns is different: `if col.startswith()` instead of `if x in col`.
::::

::::::::

We're doing *almost* the same thing five times! Imagine you find an error in your first code
cell - now you have to copy paste the code into each cell where similar code appears. Or,
image you want to do this for 25 columns rather than five. What if instead of repeating this code,
we replaced it with single function we could re-use each time? 

:::: callout
What's a **function**? A function is a reusable piece of code that can be treated as a black box by the
rest of your workflow.

What makes a good function?
* It has one task (can be composed of multiple other functions)
* Someone other than the person who wrote it can understand what it does
* It can be adaptable (e.g., we can run this transformation function on a new year of data).
* It can be tested (we'll talk about this next module!)
::::

We can imagine writing a function called `melt_monthly_vars` to replace our repetitive code. Then, our many lines of code might look something like this:

```python
def melt_monthly_vars(df, variable_name):
    #some code here
    return df_melt

fuel_elec_mmbtu_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_electricity_mmbtu")
fuel_elec_units_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_electricity_units")
fuel_mmbtu_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_mmbtu")
...
```

Yet, as we just saw, this redundant code isn't *identical* across all variables: the cell working with `net_generation_mwh` selects
cells differently than the others. *Should* it get combined into this `melt_monthly_vars`?

As we think about how to organize and re-organize our code, it doesn't take long to run into
these types of tricky questions. One strategy to help us figure out which
code we can modularize is a **plain language approach**. 

Often, we start by writing our code first and adding comments or documentation at the end. In contrast, starting by briefly outlining what a piece of our code *should do* and *why* can be incredibly valuable.

Let's go back to the description we wrote earlier:

> This code takes a table with data stored in one column per month and stacks all the fields for a single variable 
> (fuel_consumed_for_electricity_mmbtu), returning a table with one month column and one value column for this variable in
> order to make it easier to plot our data over time.

Yes, the code definitely does this! Whatever code we use to write our `melt_monthly_vars`
function, it should definitely work for this case.

Let's take another example from our notebook:

```python
# Plant 62410 has two 2020 data entries but one is null
# Drop the bad row
pr_gen_fuel_final = pr_gen_fuel_clean.loc[
    ~((pr_gen_fuel_clean.plant_id_eia == 62410) 
    & (pr_gen_fuel_clean.date.dt.year == 2020)
    & (pr_gen_fuel_clean.fuel_consumed_for_electricity_mmbtu.isnull()))
]

# drop after 2025-03-01 (for now) as these values should not exist
pr_gen_fuel_final = pr_gen_fuel_final.loc[pr_gen_fuel_clean.date < pd.Timestamp("2025-03-01")]
```

:::::::: challenge
Write a plain language description (1-2 sentences) for each of these two lines of code. Should they be combined into one `drop_bad_values()` function?

:::: solution
1. This code drops a specific row that has been identified as a "bad" (in this case, duplicated and empty) value.
2. This code drops all data reported with invalid timestamps.

Though both of these lines are dropping low-quality records, their intent is very different. The first line targets a very specific known bad value, while the second drops a potentially large number of records based on valid values in a single column. Though both may address "bad" data, they shouldn't get combined into a single function.
::::
::::::::

When is code a good candidate for modularization?
- In plain language, it's a discrete step.
- You find yourself copy-pasting the same lines of code over and over again.
- You want to do pretty much the same thing in many different contexts (e.g., on other columns, on other datasets).
- It's a complex task (e.g., an involved multi-line transformation) that requires some extra explanation
- You want to be able to test it (we'll cover this shortly)

When is code a *bad* candidate for modularization?
- In plain language, it's actually more than one step (e.g., converting data types *and* dropping rows)
- You never anticipate reusing it (e.g., a completely bespoke transformation step)
- It's already a modularized function. For example, Pandas' .replace() method can already
take multiple input values flexibly, so there's no need to reproduce someone else's work here.

Modularizing our code can take some time! Being strategic about when and where to pull
code out for this kind of treatment takes some practice, but can save a lot of time and
pain in the long run.

:::: discussion
Which other parts of this code are good candidates for modularization?
::::

:::: instructor
The code that handles the data type transformations for both the plant frame and the generation
fuel table can probably be modularized. We could consider writing a function that maps Y/N to
boolean columns, for example.
::::

## A plain language approach to function design

Plain language not only helps us to identify meaningful similarities and differences across
our code, but it can also serve as an important starting place for function design:
- There are many ways to do most tasks. Using plain language descriptions focuses us
on the desired outcome, and helps us assess whether different ways of doing the same
thing might help meet our goals better.
- Plain language helps us break down the discrete steps involved in a task and the expected outcome.
- When our underlying data changes or we try to reuse our code in a different context,
plain language descriptions can help us pay attention to what the code we've written
can and can't be used to do.
- Plain language helps provide important context about *why* we've written this code and what it does.

When we're taught how to write a function, lessons typically focus on the basics:
* A function should have a name
* A function should have inputs
* A function should have an output (return something)
* Function and variable names should be informative, but not unwieldy. `i` is bad, but so is
`raw_puerto_rico_generation_fuel_data_from_eia_923`.

:::: instructor
Start with the code for the net generation melt. First, swap out the variable name for a variable
that is called `variable_name`. Then, rename the variables to be more generic (as below). Check that the
startwith() method works for all the columns by showing that all the other columns we're interested in also start
with their variable names.

We can use this to demonstrate that we can get the same method to work for all 5 cases with one additional variable.
::::

```python
def melt_monthly_vars(pr_gen_fuel, variable_name):
    var_cols = index_cols + [col for col in pr_gen_fuel.columns if col.startswith(variable_name)]
    var_df = pr_gen_fuel.loc[:, var_cols]

    ## Melt the fuel_consumed columns
    var_melt = var_df.melt(
        id_vars=index_cols,
        var_name="month",
        value_name=variable_name
    )
    var_melt["month"] = var_melt["month"].str.replace(f"{variable_name}_", "")
    var_melt = var_melt.set_index(index_cols + ["month"])
    return var_melt
```

### Docstrings

We can attach our plain language summary of the function directly to our code by using a docstring. Unlike an in-line comment which uses the hash symbol (e.g., `# melt the vars`), a docstring uses triple quotation marks and is written right after the definition of a function, module, method or class.

A docstring can contain the following information:
- A one-line summary of your function.
- A paragraph with a longer description (optional)
- A list of input arguments, and what they are expected to be
- A list of returned objects, and what they are expected to be

```python
def melt_monthly_vars(pr_gen_fuel, variable_name):
    """Melt many columns of monthly data for a single variable into a month column and a value column.
    
    This code takes a table with data stored in one column per month and stacks all the fields for a single variable (fuel_consumed_for_electricity_mmbtu), returning a table with one month column and one value column for this variable in
    order to make it easier to plot our data over time. Note that this drops the other variables of data.
    
    Args:
        pr_gen_fuel: EIA 923 Puerto Rico generation fuel data.
        variable_name: The variable to be melted.

    Returns:
        var_melt: A dataframe containing only index columns, a month column and the melted variable data.
    """
    var_cols = index_cols + [col for col in pr_gen_fuel.columns if col.startwith(variable_name)]
    var_df = pr_gen_fuel.loc[:, var_cols]

    ## Melt the fuel_consumed columns
    var_melt = var_df.melt(
        id_vars=index_cols,
        var_name="month",
        value_name=variable_name
    )
    var_melt["month"] = var_melt["month"].str.replace(f"{variable_name}_", "")
    var_melt = var_melt.set_index(index_cols + ["month"])
    return var_melt
```

Now in two months, when you return to your code and wonder what it does, you can simply call:

```python
help(melt_monthly_vars)
```

### Type hints

In our docstring, we're already implying some things about what we should and shouldn't
be able to pass into our variables (for example, should we be able to pass a number in as `variable_name`?).
**Type hints** help us know exactly what data types our functions take. We can specify one or more datatypes expected as the input and output of the code as follows:

```python
def melt_monthly_vars(pr_gen_fuel: pd.DataFrame, variable_name: str) -> pd.DataFrame:
```

In this case, take a Pandas DataFrame and a string and return another Pandas DataFrame.
Multiple types can be formatted as follows:

```python
def my_cool_function(list_of_ints: list[int], str_or_int_or_none: str|int|None) -> list[int|str]:
```

While Python won't raise an error if you pass a different datatype in, this provides a helpful form of documentation to yourself and others about what types of data you expect to work with this function, and what the format of the output is intended to be.


```python
def melt_monthly_vars(pr_gen_fuel: pd.DataFrame, variable_name: str) -> pd.DataFrame:
    """Melt many columns of monthly data for a single variable into a month column and a value column.
    
    This code takes a table with data stored in one column per month and stacks all the fields for a single variable (fuel_consumed_for_electricity_mmbtu), returning a table with one month column and one value column for this variable in
    order to make it easier to plot our data over time. Note that this drops the other variables of data.
    
    Args:
        pr_gen_fuel: EIA 923 Puerto Rico generation fuel data.
        variable_name: The variable to be melted.

    Returns:
        var_melt: A dataframe containing only index columns, a month column and the melted variable data.
    """
    var_cols = index_cols + [col for col in pr_gen_fuel.columns if col.startwith(variable_name)]
    var_df = pr_gen_fuel.loc[:, var_cols]

    ## Melt the fuel_consumed columns
    var_melt = var_df.melt(
        id_vars=index_cols,
        var_name="month",
        value_name=variable_name
    )
    var_melt["month"] = var_melt["month"].str.replace(f"{variable_name}_", "")
    var_melt = var_melt.set_index(index_cols + ["month"])
    return var_melt
```

:::::::: challenge

### Challenge 3: putting it all together!

In a group, identify one task in the `etl.ipynb` that you think is a good candidate for modularization.
In plain language, identify what you want the function you're writing
to accomplish. Then, try and write a generalizeable function that accomplishes that step.

```python
def my_cool_function(input: Type) -> Type:
    """ This function does something.

    Any more notes can go here.

    Args:
        input: What the input is

    Returns:
        Something useful.
    """
    # your code here
    return output
```

::::::::

:::: instructor
Ask each team to paste their function into the codi and explain why they chose it. Pick one or two of these to test.
::::

::::::::::::::::::::::::::::::::::::: keypoints

- TODO

::::::::::::::::::::::::::::::::::::::::::::::::
