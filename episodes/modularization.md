---
title: "Modularization"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I re-use code I've already written to address similar problems?
- How can I clearly communicate what my code is doing?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Structure code to isolate discrete, inspectable steps
- Design code modules for clarity and reuse
- Use a "plain english" strategy to help decide how best to design your functions

::::::::::::::::::::::::::::::::::::::::::::::::

- cover 'plain english' code descriptions
- this gives us tools to think about the code in parts and make improvements

why plain english?
- helps us assess whether the code does what we think it should do
- there are many ways to do most tasks. helps us assess whether different options of doing the same thing will meet our goals better.
- helps us pay attention to the desired outcome, rather than the method.
- when data changes, keeps us attuned to what we actually care about.
-

:::::::: challenge

### Challenge 1: breaking down code

Look at the following code. Which of these best describes what it does in plain English?

#### TODO: figure out which actual bad value I need to drop here, pre-column rotation.

```python
pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA).convert_dtypes()
pr_gen_fuel_final = pr_gen_fuel.loc[~((pr_gen_fuel.plant_id_eia == 62410) & (pr_gen_fuel.date.dt.year == 2020) & (pr_gen_fuel.value.isnull()))]
```

A. Clean up non-standard nulls, convert dtypes, and drop a bad value.
B. Clean up the data.
C. Replace all "." values with null values, automatically convert data types to the best possible choice, and then drop any null data for plant ID 62410 in 2020.
D. TODO.

:::: solution
Fix!
::::

::::::::

* having a high-level understanding of what code does gives us tools to respond to data changes

* review - what is a function
* what makes a good function (brief, callback to the last challenge)
* why should we make our functions reusable and modularized?

TODO: In setting this up, borrow heavily from:
https://carpentries-lab.github.io/good-enough-practices/03-software.html#decompose-programs-into-functions
https://carpentries-lab.github.io/good-enough-practices/03-software.html#give-functions-and-variables-meaningful-names

Here or below??, mention:
* function should have data type specified

To cover briefly?:
* some other best practices for functions - demo naming, text. No exercises needed.
Do this at the end to make it a seperate skill than the structural stuff

* function should have clear name
* inputs should have clear names
* docstring should explain what the function does

```python
def transform_pr_gen_fuel(raw_pr_gen_fuel: pd.DataFrame) -> pd.DataFrame:
    """ This function cleans raw Puerto Rico generation fuel data from EIA 923.

    The transformations include:
    * replace EIA "." NAs with nulls
    * conversion of datatypes
    * dropping known bad values for plants

    Args:
        raw_pr_gen_fuel: The raw Puerto Rico generation fuel dataframe.

    Returns:
        A dataframe of cleaned Puerto Rico generation fuel data.
    """

    return pr_gen_fuel_final
```

:::::::: challenge

### Challenge 2: moving towards reusability

Currently, our code drops one plant's null data in a particular year:

```python
pr_gen_fuel_final = pr_gen_fuel.loc[~((pr_gen_fuel.plant_id_eia == 62410) & (pr_gen_fuel.date.dt.year == 2020) & (pr_gen_fuel.value.isnull()))]
```

What if this is no longer a problem isolated to one plant?

In words (not code!), describe a function that could be used to reproducibly drop null
data in `pr_gen_fuel_elec` for a known list of plants in particular years. You
don't want to drop *all* null values here, only a few known 'bad' values.

* What are the inputs (e.g., a list of plant IDs)? What data type is each input?
* What does the function do with these inputs?
* What is the output?

TODO: Write me one of these
```python
def terrible_function_name(pr_gen_fuel: pd.DataFrame) -> pd.DataFrame:
    """ This function does some stuff

    The transformations include:
    *

    Args:
        pr_gen_fuel: The raw Puerto Rico generation fuel dataframe.

    Returns:
        A dataframe of cleaned Puerto Rico generation fuel data.
    """

    return pr_gen_fuel_final
```

Consider:
* What situations does this function cover? What kinds of situations does it *not* cover?

::: solution
There are many good answers here. Here are but a few examples:
* A function that takes `pr_gen_fuel_elec` and a multi-index of plant and date values
`bad_plants_index` that we know contain null values. The function drops any values from
`bad_plants_index` that are in the index of `pr_gen_fuel_elec`, and returns `pr_gen_fuel_elec` without these records.
* A function that takes `pr_gen_fuel_elec` and a list of tuples of plant and date
values, `null_records`. The function zips together the plant and date values in
`pr_gen_fuel_elec`, and compares these to `null_records`, dropping any values in
`null_records` from the dataframe. The function returns `pr_gen_fuel_elec` without these records.
* A function that takes `pr_gen_fuel_elec` and dictionary of bad values called
`null_values_dict`, where the key is the date and the list of values is the 'bad' plant
IDs for that year. Iterating through each year key in `null_values_dict`, the function drops values
from the bad plants for that year and returns `pr_gen_fuel_elec` without these records.
:::

::: instructor
Give your students five minutes to work on this. Then, put them in breakout rooms with
1-2 others and ask them to share their solutions.
:::

::::::::

To cover: what makes a piece of code a *good* candidate for modularization?
- in plain english, it makes sense as a discrete step
- something you do often
- something that you might want to reuse in other contexts (on other columns, on other datasets)
- a complex and discrete task (e.g., an involved multi-line transformation)
- something you want to test?????
- it's difficult to read

What makes something a piece of code a *bad* candidate for modularization?
- in plain english, it's actually more than one step (e.g., converting data types *and* dropping rows)
- you never anticipate reusing it (e.g., a completely bespoke transformation step)
- it's already a modularized function. For example, Pandas' .replace() method can already
take multiple values flexibly, so there's no need to reproduce work here.

:::: discussion
Which other parts of this code are good candidates for modularization?
::::

:::::::: challenge

### Challenge 3: putting it all together!

Ideally..... take a bunch of tasks from the discussion above, split up into teams,
write a function for each section. Meet back up, try to put it all together into one
transformation function and see if it works. Debug as needed.

problems:
* right now we only have one good candidate for the revamp - the known bad plants.
* how do we see if it works.... foreshadow the next lesson hehehe
* what if it fails? transition to next lesson hahaha.

::::::::



::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
