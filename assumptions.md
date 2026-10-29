---
title: "Making assumptions about your data"
teaching: 30
exercises: 20
---

:::: instructor

Prep list:

- [make a Google Doc](https://www.docs.new) that people can put their assumptions in; make it editable by all who have the link; zoom in to 150%

::::

:::::::::::::::::::::::::::::::::::::: questions

- How can I be sure that what I learned about my data is actually true?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Articulate assumptions about a dataset
- Prioritize which assumptions are worth verifying
- Programmatically verify those assumptions

::::::::::::::::::::::::::::::::::::::::::::::::

## Intro

When exploring a dataset,
you can learn lots of things!
But then, as good scientists, doubt starts to creep in.

How do you know what you learned is true?
Or that it will *stay* true as the data gets updated?

We'll focus on a few skills that, together, will help you feel a little more confident in your work.

* identifying and articulating assumptions about a dataset
* a framework for evaluating and prioritizing assumptions
* programmatically checking assumptions

While faulty assumptions lurk everywhere,
we'll focus here on assumptions about your *data*.

For this lesson,
we'll keep using the Puerto Rico electricity data from the previous lesson,
located at `data/pr_gen_fuel_monthly.parquet`.

## What is an assumption anyways?

In this context, an *assumption* can be any property you think is true about the data.

Some examples:

- values are reasonable: the reported fuel usage in MMBtu is always non-negative.
- relationships are well-defined: data rows that share the same plant ID correspond to the same plant
- data types are consistent: the "year" column only contains numbers, not words or strings of random characters
- and many more!

Your work is based on these assumptions!
Which means that your work can suffer if:

* an assumption's not true
* it not being true impacts your work
* you don’t know that it's not true
* you don’t know that it impacts your work

It's good to defend ourselves against these.
The first step is to identify assumptions you've already made about your data.

:::: challenge

### Challenge: identifying assumptions

Take 5 minutes to list out as many assumptions as you can **about the
EIA 923 Puerto Rico data** (`pr_gen_fuel_monthly.parquet`) in the [data directory](../data/).

Please put them in the shared Google doc that your instructor prepared for you.
This will serve as a foundation for future challenges in this lesson.

The goal is to get past the obvious ones and start thinking of some un-obvious assumptions -
no need to limit yourself to 'realistic' ones at this stage.

Some prompts to get you started:

* what problems have you run into in previous datasets?
* if you were here for the data exploration episode,
  what are some things you learned about the data then?
* how can I build on others' suggestions in the doc?

When we return, we'll talk about which things worked.

::::

:::: instructor

Some examples, if students are feeling a little quiet:

* the net generation data is actually in MWh and not a mix of units
* the net generation of batteries is strictly less than the fuel consumed in MWh
* the net generation of each individual plant is "reasonable" - i.e. there are no reports of a generator producing more power than the Sun
* the reported dates are all within the last decade
* the fuel mix matches what we know of physical reality
* the total generation matches what we expect for Puerto Rican electricity demand
* all energy source codes correspond to the set in the documentation
* a plant ID corresponds to only one plant name per year
* a given plant ID always corresponds to the same plant name
* plant IDs are distributed in chronological order of construction
* every generator has at least one reporting period for which they have non-zero generation
* electricity generation heat rates are close to known averages for their prime mover / energy source
* if a value is reported, it is correct and reflects reality
* if a generator reports all null values for a specific time period, it was non-operational during that time period; if a generator reports 0 generation for a specific time period, it was operational, but not dispatched

::::

## How to test your assumptions

Now that we have some assumptions,
we'll introduce a tool we can use to check them programmatically,
before talking about a framework for evaluating and prioritizing assumptions.

Let's take a look at one of the example assumptions and see how we'd test it:

> the reported fuel consumption in MMBtu is always non-negative.

How would we verify that? We can use an `assert` statement to verify the assumption.

`assert` basically says, "if this next part is True, great! Nothing happens. If it's False, we'll raise an error."

```python
assert 1 == 1
assert 1 == 2
```

We can include a message in the statement as well, to make the error a little nicer:

```python
assert 1 == 2, "Expected 1 to be equal to 2."
```

Note that, for weird historic reasons, there are no parentheses here - Python will warn you about this:

```python
assert(1 == 2, "Expected 1 to be equal to 1.")
```

So let's assert our assumption is true.
You'll notice this flow is pretty similar to the flow in data exploration.
The main difference being that we have the *computer* evaluate whether the expectation is true.

```python
# carve off the data we need
fuel_consumed_mmbtu = gen_fuel["fuel_consumed_mmbtu"]

# assert our expectation is true
assert (fuel_consumed_mmbtu >= 0).all(), "We thought all fuel consumption would be non-negative."
```

Oh no! We find that the expectation is not true!
It's actually very common to find that,
once you start writing down your assumptions,
that they're incomplete in some subtle way.
Let's dig in to see what's going on.

```python
fuel_consumed_mmbtu[~(fuel_consumed_mmbtu >= 0)]
```

Huh! We get a bunch of not-a-number values.
That's expected, since we know that some values aren't reported,
so let's tweak our assumption to:
"If fuel consumption in MMBtu is reported at all, it should be non-negative."

```python
assert (fuel_consumed_mmbtu.dropna() >= 0).all(), "If fuel consumption in MMBtu is reported at all, it should be non-negative."
```

Which passes with little fanfare.

It is important to include plenty of context in the assert message.
A good assert message sheds light on where things are going wrong,
even when it is buried in a long data transformation pipeline.

We'll practice this skill in a bit,
after we talk about which assumptions might be good to practice with.

## Which assumptions are worth testing?

As we've just seen,
assumptions take some effort to test.
While it's useful to test many assumptions,
the reality is that we have limited time to work on our projects
and need to prioritize the assumptions that are "worth" the investment of testing them.

What makes assumptions worth testing?
Here are three dimensions to consider in a rudimentary prioritization framework:

* How easy it is to test the assumption:
  the less you have to work for this test,
  the more likely it is to be worth it.
  This is not an *objective* measure -
  this is about how easy it would be for whoever is going to be doing the work.
* The impact on your code:
  what's the goal of the system you've built up?
  What happens to that goal if your assumption is violated?
* The likelihood the assumption is violated:
  what are some ways this could go wrong?
  Do they feel plausible or implausible?

You'll build up an intuition for these,
especially likelihood,
as you see more and more issues pop up over time.

Some examples:

:::: instructor

Put this up on the screen! Using *markdown cells*.

::::

* the reported fuel consumption in MMBtu is always non-negative
  * pretty easy to test - we didn't have to do *too* much work above
  * moderate impact - though this depends on the goals of my system,
    if I do any analysis that touches the negative fuel consumption
    I will probably end up with numbers that are off in some way.
  * high likelihood - all it takes is a typo, which happens all the time.

:::: challenge

### Challenge: prioritizing assumptions

Now it's time to try out that framework!

Let's start by looking at the list of assumptions we came up with.

Take a few minutes to evaluate the assumptions along those three axes:

* add a thumbs up emoji (👍) to 3-5 that seem easy to test.
* add a scream emoji (😱) to 3-5 that seem like they would have high impact on your work.

* add a clover emoji (🍀) to 3-5 that seem like they have a high chance of being broken.

This will serve as the basis of the next exercise.

::::

:::: challenge

### Challenge: testing an assumption

Now that we have evaluated potential testing targets,
we can go ahead and write some tests for them!

In this challenge you'll pick an assumption from the list we generated above,
and write some code that checks if it's true or not.

Please put your initials next to an assumption if you're working on it.
Feel free to work on the same thing as someone else,
this just helps us prepare for the discussion at the end.

We'll take 10 minutes for this.
Since this is a small amount of time for open-ended coding work,
we don't expect everything to be perfect or even working.
The point is to get some practice --
not just at translating assumptions into code,
but at finding the places where our initial assumptions were incomplete,
and refining them to be more effective.

If you have questions during these 10 minutes,
feel free to ask them in chat.
At the end,
we'll ask about problems you encountered.

If someone is feeling particularly generous,
they can share their code and we can try to work through their problem together.

::::


## Conclusion

We've now practiced some crucial skills:

* identifying and articulating assumptions about your data
* evaluating which assumptions are most valuable to check
* checking those assumptions

What can we do with this?

The most important is to add checks to your data processing code,
to make sure that your inputs and outputs are behaving as you expect,
every time the code runs.

This protects you from surprises about your code down the line,
letting you make changes without worrying that
some foundation of your work has shifted while you weren't looking.

:::: keypoints

- you're always making assumptions about your data, and many of them are likely to be wrong, so you need to check them
- you can prioritize assumptions by thinking about their impact, likelihood, and testability
- you can use `assert` statements to tell you if an assumption is wrong *every time you run the code*

::::
