---
title: "Modularization"
teaching: 30
exercises: 15
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I re-use code I've already written to address similar problems?
- How can I reduce duplication in my code?
- How can I clearly communicate what my code is doing?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use a "plain language" strategy to identify good candidates for modularization
- Structure code to isolate discrete, inspectable steps
- Communicate what code is doing using docstrings

::::::::::::::::::::::::::::::::::::::::::::::::

As we explore our data, assert assumptions about it and transform it to meet those
assumptions, it's easy to quickly write hundreds of lines of code. Yet as our code grows,
it can get increasingly repetitive, confusing, and challenging to explain to others.
In this lesson, we'll explore practical approaches to **modularizing** our code - breaking
it into smaller chunks we can reuse, test, and combine to transform our data.

:::::::: challenge
### Challenge 1: Identifying duplicated code
Open `notebooks/etl.ipynb`. Do you see any code that performs the same task? What differences do you note between the code itself?

:::: solution
- Cell 2 replaces NAs twice.
- Cells 3 and 5 are performing the same code assertion.
- Cell 4 and 7 are doing the same unit conversion.
- Cell 6 handles three bad values.
::::

::::::::

Even in this short notebook, we're already seeing a lot of duplication! How should we reorganize it?

## A plain language approach to code reorganization

As we think about how to organize our code into discrete and reusable steps (or to *modularize* it), it doesn't take long to run into these types of tricky questions. One strategy to help us figure out which code we can modularize is a **plain language approach**.

Often, we start by writing our code first and adding comments or documentation at the end. However, language can be an important tool to guide code design and reorganization.

A **plain language description** tells us what our code *should do*.

```python
def double_x(df):
    df['doubled_x'] = df['x'] * 2
    return df
```

This code creates a new column with values that are twice the value of X.

```python
def two_x(df):
    df['two_x'] = df['x'] + df['x']
    return df
```

This code creates a new column with values that are also twice the value of X.

Even though the code is not identical, these two lines are performing an identical task
and we could replace them with one shared function. Where these descriptions
are very similar, we should consider combining the code into one shared function.

However, not all similar code should be automatically reorganized together. A plain
language description should also give us important context about *why* we've written
this code:

```python
def speed_limit():
    return 35
```

```python
def age():
    return 35
```

For instance, if we know that the first function returns the speed limit and the second returns someone's
age, we **should not** combine them into one function, even if the underlying code is identical.
Intent is a key component of a plain language description.

Let's practice on some real code!

:::::::: challenge

### Challenge 2: Writing a plain language description

Look at the following code. Which of these best describes the intent of the code?

```python
# Plant 62410 has two 2020 data entries but one is null
pr_gen_fuel_clean = pr_gen_fuel_clean.loc[
    ~((pr_gen_fuel_clean.plant_id_eia == 62410)
    & (pr_gen_fuel_clean.date.dt.year == 2020)
    & (pr_gen_fuel_clean.fuel_consumed_for_electricity_mmbtu.isnull()))
]
```

* A. Drop a duplicated entry with missing data.
* B. Address some data problems and return a cleaner Pandas DataFrame.
* C. Drop any rows with a null in the "value" column for plant ID 62410 in 2020.
* D. Create ``pr_gen_fuel_clean``.

:::: solution
A. Drop a duplicated entry with missing data.

Why A.? Unlike B., A. describes the *intention* behind the code (e.g., we're dropping a
value because we've subjectively decided that it is *bad*), while providing enough detail
about the specific steps taked in the code (unlike C. or D.).

B. does not give us any specific information about what types of cleaning we are performing. We could return a completely different output that would still meet this description.

C. gives us a lot of information about the methods we're using, but not any more information than reading the code would directly. We would have to completely rewrite this description if we were handling a new bad plant or a new invalid date.

D. only describes the name of the final output, but doesn't explain at all what the code does.
::::
::::::::

A good plain language description should:
- explain what the code accomplishes in a few sentences
- describe the intent of the code (why did we write this?)
- give us important detail without needing to be completely rewritten every time we use our code in a similar context (e.g., on a new year of data).

### Identifying good candidates for modularization

Modularizing our code can take some time! Being strategic about when and where to pull
code out for this kind of treatment takes some practice, but can save a lot of time and
pain in the long run.

When is code a *good* candidate for modularization?

- In plain language, it's a discrete step.
- You find yourself copy-pasting the same lines of code over and over again.
- You want to do pretty much the same thing in many different contexts (e.g., on other columns, on other datasets).
- It's a complex task (e.g., an involved multi-line transformation) that requires some extra explanation
- You want to be able to test it (we'll cover this shortly)

When is code a *bad* candidate for modularization?

- In plain language, it's actually more than one step (e.g., converting data types *and* dropping rows)
- You never anticipate reusing it (e.g., a completely bespoke transformation step)
- It's already a modularized function. For example, Pandas' .drop() method can already
take multiple input values flexibly, so there's no need to reproduce someone else's work here.

:::: discussion
Which parts of this code could be a good candidate for modularization?
::::

:::: solution
Here are a few options:

- Code mapping in cell 3: this is a multi-line task that we're performing more than once and
could imagine wanting to perform on additional columns in the future.
- Duplicated data with a null value in cell 6: this seems to be a somewhat common
reporting problem that we can imagine showing up in other timeframes or tables from the
same source.
- Thousands units in cell 4 and 7: both of these lines have the same intent and require
some explanation.

The following aren't great candidates:

- Cell 2: There's no need to write a function, we can just pass both parameters to .replace()
- All of cell 6: the last part has a different intent than the first two steps.
::::

Now that we've identified some promising candidates, it's time to write some code!

## A plain language approach to function design

:::: callout
What's a **function**? A function is a reusable piece of code that can be treated as a black box by the
rest of your workflow.

What makes a good function?:

- It has one task
- Someone other than the person who wrote it can understand what it does
- It can be adaptable (e.g., we can run this transformation function on a new year of data).
- It can be tested (we'll talk about this in a future module!)

::::

Plain language not only helps us to identify meaningful similarities and differences across
our code, but it can also serve as an important starting place for function design:

- There are many ways to do most tasks. Using plain language descriptions focuses us
on the desired outcome, and helps us assess whether different ways of doing the same
thing might help meet our goals better.
- Plain language helps us break down the discrete steps involved in a task and the expected outcome.
- When our underlying data changes or we try to reuse our code in a different context,
plain language descriptions can help us pay attention to what the code we've written
can and can't be used to do.

When we're taught how to write a function, lessons typically focus on the basics:

- A function should have a name
- A function should have inputs
- A function can have an output (return something)
- Function and variable names should be informative, but not unwieldy. `i` is bad, but so is `raw_puerto_rico_generation_fuel_data_from_eia_923`.

Let's look at this code from the notebook:

```python
# convert codes to strings
ENERGY_SOURCE_DICT = {'WND':'wind', 'NG':'natural_gas', 'SUN':'solar',
    'BIT':'bituminous_coal', 'MWH':"electricity_for_energy_storage", 'DFO':'distillate_fuel_oil', 'RFO':'residual_fuel_oil', 'WAT':'hydro'}

assert all([code in ENERGY_SOURCE_DICT for code in pr_gen_fuel['energy_source_code'].unique()]) # Check all codes present
pr_gen_fuel['energy_source_code_full'] = pr_gen_fuel['energy_source_code'].replace(ENERGY_SOURCE_DICT)
pr_gen_fuel = pr_gen_fuel.drop(columns='energy_source_code').rename(columns={'energy_source_code_full':'energy_source_code'})
```

:::: instructor
1. Start with the code from cell 3.
2. Update existing comment into a plain language description (e.g., "Replace short-hand codes in a column with interpretable strings using a dictionary.") You can ask for suggestions here!
3. Use description to name function.
4. Then swap out the dictionary and column name for more generic variables.
::::

We can generalize our code into a function that looks like this:

```python
# Replace short-hand codes in a column with more easily interpretable strings using a dictionary
def map_code_to_strings(df, mapped_col, code_dictionary):
    assert all([code in code_dictionary for code in df[mapped_col].unique()]) # Check all codes present
    df['code_name'] = df[mapped_col].replace(ENERGY_SOURCE_DICT)
    df = df.drop(columns=mapped_col).rename(columns={'code_name':mapped_col})
    return df
```

:::: instructor
Demonstrate that the code works on cell 5 as well.
::::

### Docstrings

We can attach our plain language summary of the function directly to our code by using a docstring. Unlike an in-line comment which uses the hash symbol (e.g., `# Check all codes present`), a docstring uses triple quotation marks and is written right after the definition of a function, module, method or class.

A docstring can contain the following information:

- A one-line summary of your function.
- A paragraph with a longer description (optional)
- A list of input arguments, and what they are expected to be

```python
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
    df['code_name'] = df[mapped_col].replace(ENERGY_SOURCE_DICT)
    df = df.drop(columns=mapped_col).rename(columns={'code_name':mapped_col})
    return df
```

Now in two months, when you return to your code and wonder what it does, you can simply call:

```python
help(map_code_to_strings)
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
    """
    # your code here
    return output
```

::::::::

:::: instructor
Ask each team to paste their function into the codi and explain why they chose it. Pick one or two of these to test.
::::

::::::::::::::::::::::::::::::::::::: keypoints

- Plain language descriptions can help us choose which code to reorganize by identifying
goals and intent.
-
- We can attach our descriptions directly to our functions using docstrings.

::::::::::::::::::::::::::::::::::::::::::::::::
