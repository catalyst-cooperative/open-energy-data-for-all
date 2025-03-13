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

### Narrative



* you're trying to pick up this project from someone else
* goals: transparency & reproducibility for others
* here are the phases of an open research process: finding data, working with the data, sharing code & data with other people (as you're working on it!)

**TODO figure out if we want to have all these discussions as separate discussions, or one set of breakout groups***

## The stages of an open data project

This lesson follows the arc of an open data analysis project, providing concrete skills and
strategies to resolve common challenges along the way. 

1. Collecting and reading in data
2. Identifying and reproducibly addressing data problems
3. Debugging code and working with 'big data'
4. 

### Finding appropriate research data

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


We won't teach you how to do this.
But. Look at public sources like EIA/FERC/EPA, PUCs, pudl

:::::::: challenge

## Discussion: challenges in finding data

Think of a time you tried to find a dataset for an energy research project. What was
one unexpected challenge that came up as you were trying to find an appropriate dataset
to answer your research question? Share with a peer.
::::::::

### Working with the data

Visualization
Analysis - this is your problem, not ours
Reusability - how to keep this ball of wax together
(chapters 2 and 3)

discussion:

* think about a time you had to re-run your old code. what were challenges you faced?

### Collaborating

You want your work to matter, right? Also sometimes you need to do this pro forma

GH, python environments, data environments/versioning, documentation

discussion:

* what was hard about working with someone else's code in the past?