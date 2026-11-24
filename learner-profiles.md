---
title: Learner Profiles
---

## Sparky Watts

#### Profile

Sparky Watts is a second-year PhD student in an interdisciplinary energy studies department.
As she's preparing for her qualifying exams, Sparky is looking at the available energy
data sources that she could use for her doctoral research.

A few years ago, a postdoctoral scholar in her research lab worked on an analysis of hourly
demand data published by the EIA. With a clear research question in mind, Sparky is
interested in building on the postdoc's data cleaning scripts and updating them to
include newer years of data, but the code is scattered over several Jupyter Notebooks
without much documentation. None of the other lab members remember much about the
project.

The postdoc also left a folder with a handful of CSVs that Sparky thinks contain
the raw data he was using, and she'll need to come up with a strategy to get new input
data. She's considering using the EIA's new API to access the new years of data, but
other lab members have told her the documentation is a bit confusing.

Though Sparky has taken a Python Software Carpentry workshop before and done some coding
using Pandas in Jupyter Notebooks, she's not quite sure where to start. The data is
larger than other datasets she's worked with before, and she can't even open it in a
spreadsheet to look at a few rows without Excel crashing. Inspired by her experiences
of looking at this postdoc's code, she's hoping to write software that others will be
able to use and adapt for their own work long after she's left the lab.

#### Background knowledge and skills:

* Has energy domain knowledge and a research area in mind
* Recently attended the Data Analysis and Visualization in Python for Ecologists workshop
* Can install software using GUI’s
* Has recently used Jupyter Notebooks and Pandas to analyze tabular data
* Is comfortable reading in CSVs to Python using `pandas.read_csv()`

#### Goals:

* Adapt existing cleaning scripts to run more reproducibly on an open-source dataset
* Figure out how to programatically download raw data using the EIA API
* Analyze data that's too big to work with in a spreadsheet
* Write and document code in a way that others can build on in the future

## Gene Rator

#### Profile

Gene Rator is a postdoctoral researcher studying the carbon intensity of electricity
production.

He writes his own analysis pipelines using Python scripts that he’s developed over the
years and is comfortable transforming data using Pandas.

Recently, Gene sent his scripts to a collaborator at another research institute, who
struggled to run the pipeline because it’s heavily tied to Gene's own research
environment. They also complained about having to manually download 50 CSVs to get the
raw data needed in order to run Gene's pipeline locally.

Gene needs to publish his own pipeline to both share his work and fulfill publication
requirements. More worryingly, he recently tried re-running the pipeline after making
some small tweaks in response to feedback from a collaborator, and got some unexpected
results - something might be going wrong somewhere in his pipeline, but it's hard to
tell where.

Gene needs strategies to debug his existing workflow, and a way to effectively share his
work with collaborators and the public.

#### Background knowledge and skills:

* Proficient in writing Python scripts using Pandas
* Uses Git to manage his code locally
* Can install software using conda and write his own environment files

#### Goals:

* Debug unexpected problems in existing pipeline
* Specify his pipeline’s software requirements so that others can run it
* Automate download of input data so that others can easily access the raw data
* Version his input data so that others running his pipeline can exactly reproduce his results

## Saul R. Panel

#### Profile

Saul R. Panel is a 1st-year PhD student who wants to work on modeling the US
energy system. Until recently they were working at a nonprofit which paid for a
commercial energy data subscription. Now that they're in school, they have lost
access to that data. They want to build a web portal that shows people the
effects of different local policy decisions on their energy bills.

They want to use public data to do this, but the constellation of different
open datasets in different formats is overwhelming and confusing compared to
the commercial dataset which provided a simple interface for getting the data
into an analysis-ready form. They've played around with some data for a single county,
but figuring out how to scale this up to a U.S.-wide analysis is overwhelming.

Some folks in their lab have done a lot of policy modeling in Python. Saul is
just starting out, but has learned the basics of Python from their coworkers in
the past few months. They're wondering how to connect the publicly available
data into the policy models from the lab so the web portal can access model
outputs.


#### Background knowledge and skills:

* Has energy domain knowledge and experience working with commercial models
* Has used Python and Pandas to write some simple data-processing scripts

#### Goals:

* Work with openly licensed data instead of commercially provided and licensed data
* Move from working with a small data sample to a large US-wide dataset
