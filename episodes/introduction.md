---
title: "Introduction"
teaching: 30
exercises: 6
---

:::::::::::::::::::::::::::::::::::::: questions

* where do I start? /how do i know where to begin?
* is it normal to feel like my project has gone nowhere and I should start over?
* my coursework makes sense. what makes research so much harder?
* this sucks. how can I make sure no one else has to suffer this misery?
* what can I do to feel like part of a research community?
* what can I do to help my work have lasting impact?
* what do I need to think about so that my project doesn't fall apart halfway to the finish line?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

* describe (/explain?) the phases of a data processing project (/research project?)
* discuss the benefits of open data principles
* list(/summarize? briefly describe?) the modules covered in this course
* identify key considerations in selecting a dataset for an open data project

::::::::::::::::::::::::::::::::::::::::::::::::


### lost & found bin for unassigned challenges

:::::::: challenge

#### Introspection: durability

Think of one of the well-established ideas or techniques in your field of research, something many people have built upon since it was first published. What do you think made that idea so useful? What helped it take hold? What helped it spread?

::::::::


### Narrative / why open data

TODO: I love this as a cold open but at some point we need a "welcome to OED4A" moment and that transition is being obstinate

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

:::::::: challenge

#### Introspection: replication

Think of a time you've had to replicate someone else's research results, either as a class assignment or by inheriting a project someone else (maybe past-you) started. What was hard about it? What was easy? What changes could the original author have made to ease your way?

::::::::

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

### Welcome

:::: instructor
deliver this as if you are in an infomercial
::::

* have you ever struggled with all the weird little auxiliary bits of writing research software?
* does it ever seem like those weird little auxiliary bits are, like, all of the work you do, and the actual interesting analysis stuff falls by the wayside?
* do you ever feel like there must be a better way to do your research?

That's all normal. There's a lot to the research process that doesn't get covered in class, and people are usually left to learn through personal struggle. We won't be able to cover all of that material, but we've chosen a few areas to cover in our time together to help close that gap.

### The research life cycle

Research is cyclic by nature: we ask questions about the world, and as we investigate them, we make hypotheses, test those hypotheses, and reveal more questions along with our conclusions.
You may have seen a diagram like this in a research methods class or as part of orientation for your research institute.
If not, that's okay!
You don't need to know it by heart to succeed in this course.

[image]

KM TODO: Paragraph: summary

KM TODO: Paragraph: parts of the research process which benefit from collaboration

Data has its own mini-cycle. It comes into play fully at the beginning of a project, and then repeats in parts along the way.
When you identify a new data need, either at the beginning of a project or to solve a problem when you're deep in the middle, you will need to locate an appropriate source for that data, and figure out how to access it.
Data can be messy for many reasons, and most projects include part of the code that cleans it and prepares it for further analysis.
Some cleaning steps might be obvious right away, and others might only be discovered after investigating odd behavior you find later.
You might have a clear idea mathematically of what processing and analysis you want to do with the data, but perfectly translating that idea into code rarely happens on the first try.
You will need to develop strategies for checking that your code has done the right thing, and ways to inspect the data at different points in your pipeline when something has gone wrong.
If your project requires large quantities of data, sufficiently large that your computer cannot load it all into memory at once, you will need to use techniques and tools that are built to handle data at scale.

<!-- Throughout the process, you may wish to get feedback from your peers and mentors about your progress and approach. -->
<!-- There are many steps you can take to make collaboration easier technologically as well as ensuring your work is legible to others. -->

The parts of the research project life cycle that typically receive explicit attention in coursework include selecting a research question, analysis techniques (e.g., selecting the appropriate statistical method), and publication.
Training in the remaining portions is often assumed to happen naturally through research experience, but this is not always effective in practice.
Gaps in these areas can create roadblocks to conducting effective, reproducible and open research, even for experienced researchers.
This course aims to address some of those roadblocks.

:::::::: challenge

#### Introspection: untaught skills

Think of a skill you've found useful in your research that wasn't taught in one of your classes. How did you learn it? Have you taught it to anyone else? Why or why not?

::::::::

#### What we will cover

This course is focused on practical solutions to roadblocks you may encounter in dealing with data, code, and collaboration. We will be following the arc of an open data analysis project in Python, structuring the course into three sections:

Roadblocks to data acquisition:
- My data is in a format I've never worked before
- The data I want to work with is published through an Application Programming Interface
(API), and I don't know how to download it

Roadblocks to data cleaning & processing:
- There's something unexpected about my input data, but I'm not sure what
- The code runs on some of my data, but errors on other input data
- When I re-run my code I get different results, and I'm not sure why
- I have no idea which part of my code is causing a particular problem
- My data changes format or content over time
- My data is too big to work with on a desktop computer

Roadblocks to collaboration:
- I'm not sure how to make it simple for collaborators to run and contribute to my code
- I need to publish my code and/or data for a paper I'm submitting to, but I'm not sure
how best to do so
- A colleague wants to build on my existing code, but I'm not sure how to clearly document
what I've done to make it possible for them to adapt it
- I wrote this code myself six months ago, and I do not recognize it, nor can I remember what I was trying to do

The next episode will discuss reading data in unexpected file formats. But first, we have to locate some data that will help with our research goals.

### Strategies for finding appropriate research data

:::::::: challenge

#### Discussion: challenges in finding data

Think of a time you tried to find a dataset for an energy research project. What was
one unexpected difficulty that came up as you were trying to find an appropriate dataset
to answer your research question? Share with a peer.

::::::::

Our research goal in this course is **TODO**.
In conducting open research, it is best to start right at the beginning, with how we choose our datasets.
Consider the following questions:

- **Relevancy:** Does the data contain the variables you need to answer your question? Does
the spatial and temporal scale of the data match your research needs? For example,
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
