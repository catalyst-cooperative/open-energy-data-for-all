---
title: "Introduction"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

* what do I need to think about so that my project doesn't fall apart halfway to the finish line?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

* describe the phases of a data processing project

::::::::::::::::::::::::::::::::::::::::::::::::

### Narrative / why open data

TODO: Do we want this to be in the second-person, or 3rd?

You're poking around your research lab's collaborative drive when you find a folder
containing data, code and some notes from a former postdoctoral researcher. They were
investigating patterns in the emissions intensity of electricity production
in Colorado as exploratory work for a potential research project, but wound up pursuing
another idea instead.

As you prepare for your qualifying exams, you're interested in picking up on their
work and developing it further. While they give you the go-ahead over email, they let
you know that they're travelling for field work for the next six months and won't be
able to respond to further questions - the documents in the drive will be your only
source of information going forward.

This is not a resilient way to work on a research project. Many common events
can cause big challenges:

* someone leaves the project, temporarily or permanently
* the project gets put on pause for a while
* someone new wants to join the project and help out
* someone wants to build new work on top of the project

As you are left to puzzle everything out on your own, you daydream about a
project where these events are much less disruptive. What might that look like?

You'd want to be able to **collaborate** with other people starting early on in
the project - it'd be nice if your other team members could review your work,
provide feedback, and contribute to parts of the analysis. Then if you have to
disappear for a while, other people can carry the project forward.

You'd want to be **open and transparent** about the data - what the inputs are,
what the outputs are, and how you got from A to B. When you're talking to a
potential collaborator, a new teammate, or just getting back into the project
after a break, being able to see the core data flows can save you a lot of
pain.

You'd also want the project outcomes to be **reproducible**, so researchers in
other labs can build on the work that you're about to do, and confirm your
results. Maybe you end up getting a new job, leaving someone else in the lab to
keep the project going. In your new role, you might find that you yourself want
to build on all your old work.

We'll keep these principles in mind as we work through the material in this
course.

### Working with the data

Though coursework often focuses on analysis techniques (e.g., selecting the appropriate
statistical method), researchers often encounter more foundational roadblocks to
effective, reproducible and open analysis of the data. Over the course of this lesson, we
cover practical solutions to the following roadblocks:

Challenges with the data:
- My data is in a format I've never worked before
- The data I want to work with is published through an Application Programming Interface
(API), and I don't know how to download it.
- My data is too big to work with on a desktop computer
- My data changes format or content over time
- There's something unexpected about my input data, but I'm not sure what.

Challenges with the code:
- The code runs on some of my data, but errors on other input data
- When I re-run my code I get different results, and I'm not sure why
- I have no idea which part of my code is causing a particular problem.

Challenges with collaboration:
- I'm not sure how to make it simple for collaborators to run and contribute to my code.
- I need to publish my code and/or data for a paper I'm submitting to, but I'm not sure
how best to do so.
- A colleague wants to build on my existing code, but I'm not sure how to clearly document
what I've done to make it possible for them to adapt it.

## The stages of an open data project

This lesson follows the arc of an open data analysis project in Python, providing concrete
skills and strategies to resolve common challenges along the way. We structure these
episodes into four sections:

1. Collecting and reading in data
2. Identifying and reproducibly addressing data problems
3. Debugging code and working with 'big data'
4. Collaborative development and sharing your work

### Strategies for finding appropriate research data

**TODO:** this section feels somewhat out of place / off-topic, but probably worth covering?

Once you've identified your research problem, the first step is to find dataset(s) you
can use to investigate it. In choosing your dataset(s), you'll need to consider the
following questions:

- **Relevancy:** Does the data contain the variables you need to answer your question? Does
the spatial and temporal scale of the data match your research needs? For example, you
data at the utility level probably won't be sufficient to answer questions about boiler-level operations.
- **Licensing:** People often assume that any content they can download from the internet is
freely available for use. By default, all creative works are protected by copyright – “All rights reserved”
means that nobody can legally use or republish data. Standardized, open licenses are how
a creator gives the public legal permission to use their work, while retaining some control.
Some licenses might impose additional restrictions - e.g.,
prohibiting commercial use, or prohibiting processing and republishing the data as part
of a new dataset. Verify that a dataset's license meets your needs as soon as possible
in the research process.
- **Documentation:** Is the data published with descriptions of any processing done or notable caveats,
explanations of variable definitions, and contact information for any further questions?
- **Level and type of processing:** The more processed a dataset is, the more you're
depending on others' judgement. If you trust those people, and they make it clear what
they’ve done and why, and the result is a dataset that’s much easier to use, this can be
a great trade-off. Pre-processed datasets may combine multiple datasets together,
use extensive validation techniques, or handle missing and outlying values - depending on
your research needs, these can save valuable time and effort or enable you to ask questions
that would otherwise be out of scope for a research project.
- **Format:** Data contained in poorly scanned PDFs will require much more extensive
processing to use than data contained in spreadsheets or computer-optimized data formats
such as Parquet. If you require multiple years of data for your research, look out for
changes in data formats over time.

This lesson will use a few key open energy data sets to illustrate the arc of data
analysis. For a start finding appropriate data for your research project, we recommend:
- For national-scale research, federal agencies such as the EIA, EPA and FERC all publish
free and regularly-updated data.
- For local/state-level research: some states maintain their own data portals (e.g., the
[Alaska Energy Data Gateway](https://akenergygateway.alaska.edu/)), and some ISOs publish
regularly-updated operational data (e.g., [CAISO's hourly data](https://www.caiso.com/todays-outlook)).
- For analysis-ready data: projects such as the [Public Utility Data Liberation (PUDL) project](https://catalystcoop-pudl.readthedocs.io/en/latest/index.html),
[PowerGenome](https://github.com/PowerGenome/PowerGenome?tab=readme-ov-file), **TODO: some more examples** publish pre-processed data that addresses many
of the common foundational challenges that make federal energy data hard to work with.

:::::::: challenge

#### Discussion: challenges in finding data

Think of a time you tried to find a dataset for an energy research project. What was
one unexpected challenge that came up as you were trying to find an appropriate dataset
to answer your research question? Share with a peer.
::::::::
