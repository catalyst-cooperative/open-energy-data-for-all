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


:::::::: challenge

### Challenge 1: breaking down code

Look at the following code. Which of these best describes what it does?

```python
pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA).convert_dtypes()
pr_gen_fuel_final = pr_gen_fuel.loc[~((pr_gen_fuel.plant_id_eia == 62410) & (pr_gen_fuel.date.dt.year == 2020) & (pr_gen_fuel.value.isnull()))]
```

A. Replace all non-standard EIA null values with Pandas null values, automatically convert data types to the best possible choice, and then subset the data to only include plant ID 62410 in 2020.
B. Replace all "." in the data with null values, convert the data to strings, and then drop any null data for plant ID 62410 in 2020.
C. Replace all "." values with null values, automatically convert data types to the best possible choice, and then drop a single row for plant ID 62410 in 2020.
D. Replace all "." in the data with null values, automatically convert data types to the best possible choice, and then drop any null data for plant ID 62410 in 2020.

::::hint
- Remember, using `help()` on a function can give you insight into what it does!
- The `~` here means "not" - give me any row that doesn't meet this condition.
::::

:::: solution
D. is the correct answer.

- `.replace(to_replace = ".", value = pd.NA)` replaces any "." value in the dataframe with an NA.
- `.convert_dtypes()` automatically converts the data type of each column to the best possible choice.
- `pr_gen_fuel.loc[~((pr_gen_fuel.plant_id_eia == 62410) & (pr_gen_fuel.date.dt.year == 2020) & (pr_gen_fuel.value.isnull()))]` selects all rows that *aren't* null data reported for plant ID 62410 in 2020. In effect, this drops null data for plant ID 62410 in the year 2020.

::::

::::::::

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
* What are the inputs (e.g., a list of plant IDs)?
* What does the function do with these inputs?
* What is the output?

Some things to consider as you design your function:
* TODOs ---- general vs specific, avoiding edge cases. e.g., we don't want a function
that just drops all nulls here.

::: solution
There are many good answers here. Here are a few examples:
* A function that takes `pr_gen_fuel_elec` and a multi-index of plant and date values
that we know contain null values. The function drops the rows in the multi-index.
* A function that takes `pr_gen_fuel_elec` and a list of tuples of plant and date values.
The function compares the rows with null values to the list, and TODO....
:::

::::::::




::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::

Objectives:

Exercises (unweeded):
Look at this long function. What are some ways we can split it up?
Look at this long function. What the hell is it doing?
Look at this long function. We’ve split it up in multiple ways… which one does the best on the plain English test?
Look at this long function. We’ve split it up in multiple ways. Now we need to fix something/change something… how would you do it in each one?
What are the inputs and outputs of this function? (in English?) (write this down in your docstring or something!!)
What does this code do? in one sentence
What are the data frames we needed to look at more closely in the last episode?
What did we do over and over again?
What are you tired of having to look up every time?
What prerequisites / inputs are needed for this code? is there a way we can reduce that?
