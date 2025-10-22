---
title: "Introduction"
teaching: 25
exercises: 12
---

:::::::::::::::::::::::::::::::::::::: questions

* Working with data sucks. How can I make sure no one else has to suffer this misery?
* What can I do to help my work have lasting impact?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

* Discuss the benefits of open data principles.
* Identify key challenges to using data in research

::::::::::::::::::::::::::::::::::::::::::::::::

:::: instructor

Intro exercise: As people trickle in:
* online: in the chat, write your name and one thing you're excited to learn about in the course.
* in person: if small enough, ask one by one. If bigger, do the same thing on a sticky note.

::::

### Greetings

Welcome to Open Energy Data for All!

:::: instructor

Deliver this as if you are in an infomercial, and as if everyone is on board with the character you are playing.

::::

* Have you ever struggled with all the weird little auxiliary bits of writing research software?
* Does it ever seem like those weird little auxiliary bits are, like, all of the work you do,
and the actual interesting energy analysis you want to do falls by the wayside?
* Do you ever feel like there must be a better way to do your research?

That's all normal. There's a lot to working with data that doesn't get covered in class,
and people are usually left to learn through personal struggle. Drawing on our experiences
working with real-world energy data, we'll focus on a few practical skills that can help close that gap.

:::: instructor

Logistics:

* My name is $name and I come from $background. Your other instructors will be $list (ask them for quick intro).
* Most sessions are structured as sets of short explanations or demonstrations, interspersed with exercises. Be prepared to alternate listening-mode with thinking-mode and doing-mode.
* Ask questions by using the "raise hand" indicator or typing into chat.
* Follow along on the website and/or use it to catch up if you need to space out or step out: https://docs.catalyst.coop/open-energy-data-for-all/

Any other questions on what to expect or how to participate?

::::


### The energy data landscape

Working with energy data can be hard and frustrating. Data problems can wreck a research
project before it starts, or crop up unexpectedly near the finish line. Why is energy data
be so hard to work with?

* **Energy data can be hard to access:** When three federal agencies, state agencies, and
Independent System Operators (ISOs) all publish overlapping data about boilers, generators,
smokestacks, plants and so on, it can be hard to know where to start. Changes in data
structure and format, the large variety of file types, and the sheer size of some datasets
all pose challenges. Where data is regularly updated, it can be tricky to keep your
workflow up to date, and make sure that your collaborators are working with the same
version of the data you're using.
* **Energy data can be messy and unpredictable:** Why is this coal plant labelled as retired one
year and operating the next? Energy data often requires substantial cleaning
before it is ready for analysis, and it's common that even mid-way through a research
process a model or analysis will reveal problems that weren't obvious at first. Commercial
data promises to be analysis-ready, but hides assumptions and transformations in a black
box, and imposes restrictions on the reproducibility and openness of your research - if
you can afford it!

### A new way...

What if instead of each one of us reproducing the same frustrating data wrangling tasks
on our own, we found a different way? What would a collaborative, open, and reproducible
energy research ecosystem look like?

**Collaborative:** How can you bring in other people starting early on in
the project? It'd be nice if your other team members could review your work,
provide feedback, and contribute to parts of the analysis. Then if you have to
disappear for a while, other people can carry the project forward.

**Open and transparent:** What are the inputs, what are the outputs, and how did you get
from A to B? When you're talking to a potential collaborator, a new teammate, or
just getting back into the project after a break, being able to see all the steps and
assumptions you've made along the way can save you a lot of pain. Whether to meet
publishing requirements or to contribute to open-source science, you want to be able
to share your code and data without hesitation.

**Reproducible:** How can researchers in other labs can build on the work that you're
about to do, and confirm your results? Maybe you end up getting a new job, leaving
someone else in the lab to keep the project going. In your new role, you might find that
you yourself want to build on all your old work.

#### What we will cover

How do we get there? Often, we assume that the skills needed to actually enact these
principles are learned naturally through research experience, but this is not always
effective in practice. Gaps in these areas can create roadblocks to conducting effective,
reproducible and open research, even for experienced researchers.

:::: instructor

Modify for whatever subset is being presented.

::::

This course is focused on practical solutions to roadblocks you may encounter in dealing
with data, code, and collaboration. We will be following the arc of an open data analysis
project in Python, structuring the course into three sections:

Roadblocks to data acquisition:

* My data is in a format I've never worked before
* The data I want to work with is published through an Application Programming Interface
(API), and I don't know how to download it

Roadblocks to data cleaning & processing:

* There's something unexpected about my input data, but I'm not sure what
* The code runs on some of my data, but errors on other input data
* When I re-run my code I get different results, and I'm not sure why
* I have no idea which part of my code is causing a particular problem
* My data changes format or content over time
* My data is too big to work with on a desktop computer

Roadblocks to collaboration:

* I'm not sure how to make it simple for collaborators to run and contribute to my code
* I need to publish my code and/or data for a paper I'm submitting to, but I'm not sure
how best to do so
* A colleague wants to build on my existing code, but I'm not sure how to clearly document
what I've done to make it possible for them to adapt it
* I wrote this code myself six months ago, and I do not recognize it, nor can I remember what I was trying to do

The next episode will discuss reading data in unexpected file formats.

:::: keypoints

* Open data principles such as reproducibility, transparency, and collaboration make it easier to share, interpret, and build upon research projects.
* Enacting these values doesn't 'just happen' - it requires specific skills and strategies.

::::

:::::::: instructor

Don't cover this, unless you have a lot of extra time or this is high priority for your students.
Instead, direct students to the course website for tips on locating and identifying appropriate datasets for open research projects.

::::::::

Strategies for finding the 'right' data are highly dependent on your specific research
field, so we don't delve into this in the course. However, below you'll find some
resources and aspects of data that are important to consider as you progress

### Additional resources: strategies for finding appropriate research data

In conducting open research, it is best to start right at the beginning, with how we choose our datasets.
This is not something we'll cover in detail anywhere else, but we can give some rough guidelines here.
Consider the following attributes of a potential data source:

- **Relevancy:** Does the data contain the variables you need to answer your question? Does
the spatial and temporal scale of the data match your research needs? For example,
data at the utility level probably won't be sufficient to answer questions about boiler-level operations.
- **Licensing:** People often assume that any content they can download from the internet is freely available for use, but this is not true. By default, all creative works are protected by copyright, and if you try to republish something copyrighted, you can run into trouble. If a specific license is set for a dataset, sometimes that might make it free to use, and other times it might set some additional restrictions. Verify that a dataset's license meets your needs as soon as possible in the research process.
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

We also have several recommendations to give you a start finding appropriate data for your own research project, depending on your area of interest:

- For national-scale research, federal agencies such as the EIA, EPA and FERC all publish
free and regularly-updated data.
- For local/state-level research: some states maintain their own data portals (e.g., the
[Alaska Energy Data Gateway](https://akenergygateway.alaska.edu/)), and some ISOs publish
regularly-updated operational data (e.g., [CAISO's hourly data](https://www.caiso.com/todays-outlook)).
- For analysis-ready data: projects such as the [Public Utility Data Liberation (PUDL) project](https://catalystcoop-pudl.readthedocs.io/en/latest/index.html),
[PowerGenome](https://github.com/PowerGenome/PowerGenome?tab=readme-ov-file), Gridstatus, and others publish pre-processed data that addresses many
of the common foundational challenges that make federal energy data hard to work with.
