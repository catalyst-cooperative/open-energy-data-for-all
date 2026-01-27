---
title: "Making assumptions about your data"
teaching: 30
exercises: 20
---

:::: instructor

Prep list:

- [make a Google Doc](https://www.docs.new) that people can put their assumptions in; make it editable by all who have the link
- clean out the example notebook so that you can type everything out again

::::

:::::::::::::::::::::::::::::::::::::: questions

- Exploratory data analysis was fun, but what did I learn?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Articulate assumptions about a dataset
- Programmatically verify those assumptions
- Prioritize which assumptions are worth verifying

::::::::::::::::::::::::::::::::::::::::::::::::

## Intro

As we explore a dataset we naturally start to make assumptions about it.

We also constantly find new evidence that our initial assumptions are incorrect.

We zoom in a little closer to a suspiciously low value,
or we notice that a certain column has more null values than we expected,
or we see that certain values seem to be duplicated when they shouldn't be,
and suddenly our understanding of the data is irrevocably changed.

This can have an impact on your work!
Depending on what you are using the data for,
these shifts will impact your work differently.
Some will not actually affect your output
- maybe you weren't using that data anyways -
but others will mean you have to make changes to your code,
your conclusions,
your methodology section,
or the way you answer a question when presenting at a conference.

It's nice to not be *surprised* by these changes,
so this lesson will focus on:

* identifying and articulating assumptions about a dataset
* programmatically checking assumptions
* a framework for evaluating and prioritizing assumptions

Afterwards, you'll be able to
put those skills together to identify high-priority assumptions to check programmatically.

While faulty assumptions lurk everywhere,
we'll focus here on assumptions about your *data*.

Speaking of data,
we have a dataset at `data/pr_gen_fuel_monthly.parquet`,
which we'll be using for concrete examples through the rest of the lesson.
It contains fuel consumption and electricity generation information,
split out by generation unit and reported monthly,
for all of Puerto Rico.
This data was collected by the EIA in form EIA 923.

## What is an assumption anyways?

In this context, an *assumption* can be any property you think is true about the data.

Some examples:

- values are reasonable: the reported fuel usage in MMBtu is always non-negative.
- relationships are well-defined: data rows that share the same plant ID correspond to the same plant
- data types are consistent: the "year" column only contains numbers, not words or strings of random characters
- and many more!

The sneakiest assumptions are the ones that are hard to think of.
If they were obvious to you, then you probably were already working around them in some way.
With that in mind, let's try to come up with some assumptions of our own!

:::: challenge

### Challenge: identifying assumptions

Take 5 minutes to list out as many assumptions as you can about the
EIA 923 Puerto Rico data (`pr_gen_fuel_monthly.parquet`) in the [data directory](../data/).

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

```python
# pull out the piece we're interested in
fuel_consumed_mmbtu = gen_fuel["fuel_consumed_mmbtu"]

# finally make that assertion!
assert (fuel_consumed_mmbtu >= 0).all(), "The reported fuel consumption in MMBtu should be non-negative"
```

Oh no! We find that the assertion is not true!
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

Pick an assumption from the list we generated above,
and write some code that checks if it's true or not.

Let's take 10 minutes for this.
Since this is a small amount of time for open-ended coding work,
we don't expect everything to be perfect or even working.
The point is to get some practice --
not just at translating assumptions into code,
but at finding the places where our initial assumptions were incomplete,
and refining them to be more effective.

If you're unsure of which assumption to pick,
the instructor will pick one for everyone to go over together after the time is up -
we invite you to try doing that one!


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

- you're always making assumptions about your data, and many of them are likely to be wrong
- you can prioritize assumptions by thinking about their impact, likelihood, and testability
- you can use `assert` statements to tell you if an assumption is wrong *every time you run the code*

::::
