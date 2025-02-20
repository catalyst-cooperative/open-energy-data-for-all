# Open Energy Data For All

A two-day, 16-hour course on foundational software and data engineering skills
aimed at energy graduate students looking to generate more robust, replicable
energy analyses.

Authors: @e-belfer @jdangerx

## Code of Conduct

We expect everyone to adhere to the [Code of
Conduct](https://catalystcoop-pudl.readthedocs.io/en/stable/code_of_conduct.html)
to promote a safe, welcoming, and productive learning environment.

## Building the lesson locally

1. Follow the [installation
   instructions](https://carpentries.github.io/sandpaper-docs/index.html)
   provided by the Carpentries to install the `sandpaper`/`pegboard`/`varnish`
   R packages required for building this.

2. Run `Rscript build.R` to build the lesson locally & open it in your browser.

## Configure a new lesson

Follow the steps below to
complete the initial configuration of a new lesson repository built from this template:

1. **Adjust the
   `CITATION.cff`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `LICENSE.md` files**
   as appropriate for your project.
   -  `CITATION.cff`:
      this file contains information that people can use to cite your lesson,
      for example if they publish their own work based on it.
      You should [update the CFF][cff-sandpaper-docs] now to include information about your lesson,
      and remember to return to it periodicallt, keeping it updated as your
      author list grows and other details become available or need to change.
      The [Citation File Format home page][cff-home] gives more information about the format,
      and the [`cffinit` webtool][cffinit] can be used to create new and update existing CFF files.
   -  `CODE_OF_CONDUCT.md`:
      if you are using this template for a project outside The Carpentries,
      you should adjust this file to describe
      who should be contacted with Code of Conduct reports,
      and how those reports will be handled.
   -  `CONTRIBUTING.md`:
      depending on the current state and maturity of your project,
      the contents of the template Contributing Guide may not be appropriate.
      You should adjust the file to help guide contributors on how best
      to get involved and make an impact on your lesson.
   -  `LICENSE.md`:
      in line with the terms of the CC-BY license,
      you should ensure that the copyright information
      provided in the license file is accurate for your project.

[cff-home]: https://citation-file-format.github.io/
[cff-sandpaper-docs]:  https://carpentries.github.io/sandpaper-docs/editing.html#making-your-lesson-citable
[cffinit]: https://citation-file-format.github.io/cff-initializer-javascript/
[workbench]: https://carpentries.github.io/sandpaper-docs/
