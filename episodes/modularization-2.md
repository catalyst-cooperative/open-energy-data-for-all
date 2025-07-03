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
utils.py
Pyproject.toml
Add transform.py and test.py in validation lesson

Perks of doing this:
Reuse core utils across multiple notebooks
Make notebooks shorter and more re-readable
Prevent general chaos and unexpected code migration when collaborating (e.g., we have two slightly different drop_null functions)

Motivation: import
Having to re copy-paste a giant code block into the top of each notebook?
Having to change one of your useful utility functions… in every notebook that has this block
Your collaborator changed one of those functions but forgot to change it everywhere. What a jerk
Having to decipher what the heck your collaborator changed in a 2000 line notebook you’re both editing?
Having to constantly scroll up and down to find that helpful function you wrote…. Somewhere?


We’ll have to cover:
Pyproject.toml - briefly
__init__.py - briefly

Objective:
Extract reusable functionality into an importable module

Challenge:
Add your cool new function into utils and call it in your notebook (probably the drop nulls one)



::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
