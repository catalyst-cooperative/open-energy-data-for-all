---
title: "Handling diverse filetypes in Pandas"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions 

- How can I read in different tabular data types to a familiar format in Python?
- What are some common errors that occur when importing data, and how can I troubleshoot them?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Import tabular data from XML, JSON, and Parquet formats to pandas dataframes using the `pandas` library
- Import a table from a SQL database using the `pandas` library
- Implement strategies to handle common errors on data import

::::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints 

- `pandas` has functionality to read in many data formats (e.g., XML, JSON, SQL,
Parquet) into the same kind of DataFrame in Python. We can take advantage of this to
transform many kinds of data with similar functions in Python.
- `pandas` accepts both relative and absolute file paths on read-in.

::::::::::::::::::::::::::::::::::::::::::::::::

