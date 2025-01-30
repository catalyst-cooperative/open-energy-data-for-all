---
title: Setup
---

## Summary - TODO

::: prereq

### Prerequisite Python knowledge
This lesson assumes an introductory knowledge of Python and the `pandas` library. Participants should:

* be comfortable reading CSV files into Pandas DataFrames
* be able to do basic data transformations in Pandas: for instance, renaming columns, merging two datasets on a shared column, or multiplying a column by a scalar value.
* be able to save transformed Pandas DataFrames locally (e.g., as a CSV)
* be able to create simple graphs in Python
* be able to write a simple function

These skills are equivalent to the completion of the [Data Analysis and Visualization in
Python for Ecologists](https://datacarpentry.github.io/python-ecology-lesson/) lesson. If you
haven’t already completed this lesson and aren’t familiar with the skills listed above, please
review those materials before starting this lesson.

### Prerequisite Git knowledge
This lesson assumes `git` is installed locally, and that participants have a basic
familiarity with the `git` version control command-line tool. Participants should be able to:
* create a local Git repository
* use commits to track changes in files
* push to and pull from a remote repository

These skills are covered in the Software Carpentries' [Version Control with Git](https://swcarpentry.github.io/git-novice/) lesson. If you aren't familiar with the skills listed above, please review
those materials before starting this lesson.    

### Other prerequisite knowledge
Throughout this lesson, we'll be working with a variety of energy datasets. In order to
get the most out of this lesson, we expect that participants:
* have some domain knowledge about the energy sector (e.g., are studying energy systems
in university).
* have energy-relevant research questions that you want to answer using data

Though these are not *mandatory* for participation in the lesson, we believe these skills
are critical to interpreting the data and applying the skills learned in these lessons
to your own work.

:::

## Setup: Overview

This lesson is designed to be run on a personal computer.
All of the software and data used in this lesson are freely available online,
and instructions on how to obtain them are provided below.

## Obtain lesson materials

In the terminal, navigate to the directory where you want to save the lesson materials.
Clone the lesson repository using the `git clone` command:

```bash
git clone https://github.com/catalyst-cooperative/open-energy-data-for-all.git
```

This will create an `open-energy-data-for-all` folder in your selected location containing
all lesson materials.

To clone the repository, you must have `git` installed and configured on your computer (one of
the prerequisites for this lesson). If you need additional guidance on `git` setup, see the Software Carpentries' [Version Control with Git](https://swcarpentry.github.io/git-novice/) lesson.

## Setting up the `uv` package manager

We use `uv` to manage the installation of Python packages needed for this lesson. `uv` is
a package manager

### Installing `uv`

1. Follow the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/) provided for `uv`.
2. Run the command `uv` in your terminal to verify that the installation has succeeded.

### Setting up the lesson environment
Once we've installed `uv`, we can use it to create a virtual environment. We'll cover
virtual environments in lesson *(TODO)*, but in short these are virtual, disposable Python
software environments that contain only the packages you want to use for a particular project
or task. If you don't have a working copy of Python locally, `uv` will install it as part
of the environment set-up step.

__TODO__: Write `uv` set-up instructions from `pyproject.toml` file.

## Accessing remote lesson data

In episodes 3 and 4 of this lesson, we'll learn how to efficiently access remote data.
To do so, we'll need to set up credentials to access these resources.

### Create an API key for accessing the EIA API
In episode 3 and 4, we'll be learning how to access the Application Programming Interface (API)
for the Energy Information Administration (EIA). To register for an EIA API key:

1. Go to the [EIA API website](https://www.eia.gov/opendata/).
2. Click "Register" on the right-hand side and complete the form.
3. Log in to the email address you provided - you should have received an email from the
EIA with the subject line "EIA API Registration Key" that contains your API key.

### Create an API key for accessing the EPA API
In episode 3 and 4, we'll also be exploring the Environmental Protection Agency's (EPA)
Clean Air Markets API portal. To register for an EPA API key:

1. Go to the [registration page](https://www.epa.gov/power-sector/cam-api-portal#/api-key-signup) and fill out the form.
2. Log in to the email address you provided. You should have received an email from the EPA
containing an API key for the Clean Air Markets API portal.

## Create an account on GitHub

You will need an account for [GitHub](https://github.com) to follow episodes *(TODO!)* in this lesson.

1. Go to <https://github.com> and follow the "Sign up" link at the top-right of the window.
2. Follow the instructions to create an account.
3. Verify your email address with GitHub.
4. Configure multifactor authentication (see below).

Basic GitHub accounts are free. As you set up your account, please consider what personal
information you'd like to reveal. For example, you may want to review these
[instructions for keeping your email address private]("https://help.github.com/articles/keeping-your-email-address-private/") provided at GitHub.

### Multi-factor Authentication

In 2023, GitHub introduced a requirement for 
all accounts to have 
[multi-factor authentication (2FA)](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication) 
configured for extra security.
Several options exist for setting up 2FA, which are summarised here:

1. If you already use an authenticator app, 
   like [Google Authenticator](https://support.google.com/accounts/answer/1066447?hl=en&co=GENIE.Platform%3DiOS&oco=0) 
   or [Duo Mobile](https://duo.com/product/multi-factor-authentication-mfa/duo-mobile-app) on your smartphone for example, 
   [add GitHub to that app](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-a-totp-mobile-app).
2. If you have access to a smartphone but do not already use an authenticator app, install one and 
   [add GitHub to the app](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-a-totp-mobile-app).
3. If you do not have access to a smartphone or do not want to install an authenticator app, you have two options:
    1. [set up 2FA via text message](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-text-messages) 
       ([list of countries where authentication by SMS is supported](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/countries-where-sms-authentication-is-supported)), or
    2. [use a hardware security key](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-a-security-key) 
       like [YubiKey](https://www.yubico.com/products/yubikey-5-overview/) 
       or the [Google Titan key](https://store.google.com/us/product/titan_security_key?hl=en-US&pli=1).

The GitHub documentation provides [more details about configuring 2FA](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication).

## Launch Python interface - TODO!

To start working with Python, we need to launch a program that will interpret and execute our
Python commands. Below we list several options. If you don't have a preference, proceed with the
top option in the list that is available on your machine. Otherwise, you may use any interface
you like.

## Option A: Jupyter Notebook

A Jupyter Notebook provides a browser-based interface for working with Python.
If you installed Anaconda, you can launch a notebook in two ways:

::::::::::::::::: spoiler

## Anaconda Navigator

1. Launch Anaconda Navigator.
  It might ask you if you'd like to send anonymized usage information to Anaconda developers:
  ![](fig/anaconda-navigator-first-launch.png){alt='Anaconda Navigator first launch'}
  Make your choice and click "Ok, and don't show again" button.
2. Find the "Notebook" tab and click on the "Launch" button:
  ![](fig/anaconda-navigator-notebook-launch.png){alt='Anaconda Navigator Notebook launch'}
  Anaconda will open a new browser window or tab with a Notebook Dashboard showing you the
  contents of your Home (or User) folder.
3. Navigate to the `data` directory by clicking on the directory names leading to it:
  `Desktop`, `swc-python`, then `data`:
  ![](fig/jupyter-notebook-data-directory.png){alt='Anaconda Navigator Notebook directory'}
4. Launch the notebook by clicking on the "New" button and then selecting "Python 3":
  ![](fig/jupyter-notebook-launch-notebook.png){alt='Anaconda Navigator Notebook directory'}

:::::::::::::::::::::::::


::::::::::::::::: spoiler

## Command line (Terminal)

1\. Navigate to the `data` directory:

::::::::::::::::: spoiler

## Unix shell

If you're using a Unix shell application, such as Terminal app in macOS, Console or Terminal
in Linux, or [Git Bash][gitbash] on Windows, execute the following command:

```bash
cd ~/Desktop/swc-python/data
```

:::::::::::::::::::::::::

::::::::::::::::: spoiler

## Command Prompt (Windows)

On Windows, you can use its native Command Prompt program.  The easiest way to start it up is
pressing <kbd>Windows Logo Key</kbd>\+<kbd>R</kbd>, entering `cmd`, and hitting
<kbd>Return</kbd>. In the Command Prompt, use the following command to navigate to
the `data` folder:

```source
cd /D %userprofile%\Desktop\swc-python\data
```

:::::::::::::::::::::::::

2\. Start Jupyter server

::::::::::::::::: spoiler

## Unix shell

```bash
jupyter notebook
```

:::::::::::::::::::::::::


::::::::::::::::: spoiler

## Command Prompt (Windows)

```source
python -m notebook
```

:::::::::::::::::::::::::

3\. Launch the notebook by clicking on the "New" button on the right and selecting "Python 3"
from the drop-down menu:
![](fig/jupyter-notebook-launch-notebook2.png){alt='Anaconda Navigator Notebook directory'}

:::::::::::::::::::::::::

  <!-- vertical spacer -->
