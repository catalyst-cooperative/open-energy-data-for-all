---
title: "Modularization 2- return of the modularization"
teaching: 15
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I actually *use* the functions I've rewritten?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Extract reusable functionality into an importable module

::::::::::::::::::::::::::::::::::::::::::::::::

Scratch notes from discussion

Goal end state of lesson:
package_name/
package_name/
__init__.py
transform.py
utils.py - added in this session
pyproject.toml
Add test.py in validation lesson

Perks of doing this:
Reuse core utils across multiple notebooks

Motivation: import
Having to re copy-paste a giant code block into the top of each notebook or script?
Having to change one of your useful utility functions… in every notebook that has this block
Having to constantly scroll up and down to find that helpful function you wrote…. Somewhere?

Objective:
- Extract reusable functionality into an importable module
- Demonstrate that you can also import this into a notebook? If so, can show that you can call help() on your
own functions (nice!).

Challenge:
Add your cool new function into utils and call it in your transform.py file (probably the drop nulls one)


::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
