---
title: "Modularization"
teaching: 30
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I re-use code I've already written to address similar problems?
- How can I clearly communicate what my code is doing?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use a "plain language" strategy to help decide how best to design your functions
- Structure code to isolate discrete, inspectable steps
- Design code modules for clarity and reuse

::::::::::::::::::::::::::::::::::::::::::::::::

- cover 'plain language' code descriptions
- this gives us tools to think about the code in parts and make improvements

why plain language?
- gives us important context about the *why*
- helps us assess whether the code does what we think it should do
- there are many ways to do most tasks. helps us assess whether different options of doing the same thing will meet our goals better.
- helps us pay attention to the desired outcome, rather than the specific method.
- when data changes, keeps us attuned to what we actually care about.
- helps us to understand the discrete steps involved in a method.
- helps us communicate what our code does to others 

:::::::: challenge

### Challenge 1: breaking down code

Look at the following code. Which of these best describes what it does in plain language?

```python
pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA).convert_dtypes()
pr_gen_fuel_final = pr_gen_fuel.loc[~((pr_gen_fuel.plant_id_eia == 62410) & (pr_gen_fuel.date.dt.year == 2020) & (pr_gen_fuel.value.isnull()))]
```

A. Clean up non-standard nulls, convert dtypes, and drop a bad value in a Pandas DataFrame.
B. Address some data problems and return a cleaner Pandas DataFrame.
C. Replace all "." values with null values, automatically convert data types, and drop any rows with a null in the "value" column for plant ID 62410 in 2020.
D. Create ``pr_gen_fuel_final``.

:::: solution
A. Clean up non-standard nulls, convert dtypes, and drop a bad value in a Pandas DataFrame.

Why A.? Unlike B., A. describes the *intention* behind the code (e.g., we're dropping a
value because we've subjectively decided that it is *bad*), while providing enough detail
about the specific steps taked in the code (unlike C. or D.).

* B. does not give us any specific information about what types of cleaning we are performing.
* C. gives us a lot of information about the methods we're using, but not any more information than reading the code would directly.
* D. only describes the name of the final output, but doesn't explain at all what the code does.
::::

::::::::

Having a plain language description of the code is an important first step for function
design.

- what is a function?

* what makes a good function? (brief, callback to the last challenge)
    * it has one task (can be composed of multiple other functions)
    * someone other than the person who wrote it can understand what it does
    * it can be adaptable (e.g., we can run this transformation function on a new year of data).
    * it can be tested (next module!)

- when we're taught how to write a function, typically focus on the basics: var names
and function name

```python
def transform_pr_gen_fuel(raw_pr_gen_fuel):
    # Your code here
    return pr_gen_fuel_final
```

TODO: In setting this up, borrow heavily from:
https://carpentries-lab.github.io/good-enough-practices/03-software.html#decompose-programs-into-functions
https://carpentries-lab.github.io/good-enough-practices/03-software.html#give-functions-and-variables-meaningful-names

- plain language approach: documentation isn't just something we shoehorn in at the end
for someone else - it helps us and others understand what we're doing.
- use type hints to specify inputs and output datatypes (what do we expect to feed into this and get back?)
- docstring explains in plain english what the function does, what the arguments are, and
what it returns
- choose names for functions and vars that are informative, but not unwieldy. `i` is bad, but so is
`raw_puerto_rico_generation_fuel_data_from_eia_923`.

```python
def transform_pr_gen_fuel(raw_pr_gen_fuel: pd.DataFrame) -> pd.DataFrame:
    """ This function cleans Puerto Rico generation fuel data from EIA 923.

    The transformations include:
    * replace non-standard EIA "." NAs with nulls
    * conversion of datatypes
    * dropping known bad values for plants

    Args:
        raw_pr_gen_fuel: The raw Puerto Rico generation fuel dataframe.

    Returns:
        A dataframe of cleaned Puerto Rico generation fuel data.
    """
    pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA).convert_dtypes()
    pr_gen_fuel_final = pr_gen_fuel.loc[~((pr_gen_fuel.plant_id_eia == 62410) & (pr_gen_fuel.date.dt.year == 2020) & (pr_gen_fuel.value.isnull()))]
    return pr_gen_fuel_final
```

Borrow from: https://carpentries-incubator.github.io/python-intermediate-development/32-software-architecture-design.html#good-software-design-goals

* We're done! Just kidding. Now that we have a plain language description, it's
clear to us what our *intentions* are regarding the transformation of our data. Knowing
what we *want* to be doing helps us to creatively tackle changes in the data, see opportunities
to apply the same code to other contexts, and switch out existing implementations for more efficient or generalized ones.
* Let's take a look at a specific example to make this more concrete.
    
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

As you can see, this takes some time! Being strategic about when and where to pull
code out for this kind of treatment takes some practice, but can save a lot of time and
pain in the long run.

When is code a good candidate for modularization?
* In plain language, it's a discrete step
* You find yourself copy-pasting the same lines of code over and over again.
* You want to do pretty much the same thing in many different contexts (e.g., on other columns, on other datasets).
* It's a complex task (e.g., an involved multi-line transformation) that requires some extra explanation
* You want to be able to test it (we'll cover this shortly)

When is code a *bad* candidate for modularization?
* In plain language, it's actually more than one step (e.g., converting data types *and* dropping rows)
* You never anticipate reusing it (e.g., a completely bespoke transformation step)
- It's already a modularized function. For example, Pandas' .replace() method can already
take multiple input values flexibly, so there's no need to reproduce someone else's work here.

:::: discussion
Which other parts of this code are good candidates for modularization?
::::

:::::::: challenge

### Challenge 3: putting it all together!

In a group, take one part of the code we discussed as being a good candidate for
modularization. In plain language, identify what you want the function you're writing
to accomplish. Then, write a generalizeable function that accomplishes that step.

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

### TODO:
problems:
* right now we only have one good candidate for the revamp - the known bad plants.
* how do we see if it works.... foreshadow the next lesson hehehe
* what if it fails? transition to next lesson hahaha.

:::: instructor
Ask each team to paste their function into the codi. Try to put it all together into one
transformation function, then visualize the results.
::::

::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
