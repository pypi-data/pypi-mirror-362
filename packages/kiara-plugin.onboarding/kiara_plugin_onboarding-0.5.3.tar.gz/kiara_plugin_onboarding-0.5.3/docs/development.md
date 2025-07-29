# Development


## Prepare development environment

### Using conda (recommended)

```
conda create -n onboarding python=3.9
conda activate onboarding
conda install -c conda-forge mamba   # this is optional, but makes everything install related much faster, if you don't use it, replace 'mamba' with 'conda' below
mamba install -c conda-forge -c dharpa kiara
mamba install -c conda-forge -c dharpa kiara_plugin.core_types kiara_plugin.tabular   # optional, adjust which plugin packages you depend on, those two are quite common
```

### Using Python venv

Later, alligator.


## Check out the source code

First, fork the [kiara_plugin.onboarding](https://github.com/DHARPA-Project/kiara_plugin.onboarding) repository into your personal Github account.

Then, use the resulting url (in my case: https://github.com/makkus/kiara_modules.onboarding.git) to clone the repository locally:

```
https://github.com/<YOUR_FORKED_GITHUB_ID>/kiara_plugin.onboarding
```

## Install the kiara plugin package into it

```
cd kiara_plugin.onboarding
pip install -e '.[all_dev]'
```

Here we use the `-e` option for the `pip install` command. This installs the local folder as a package in development mode into the current environment. Development mode makes it so that if you change any of the files in this folder, the Python environment will pick it up automatically, and whenever you run anything in this environment the latest version of your code/files are used.

We also install a few additional requirements  (the `[all_dev]` part in the command above) that are not strictly necessary for `kiara` itself, or this package, but help with various development-related tasks.

## Install some pre-commit check tooling (optional)

This step is optional, but helps with keeping the code clean and CI from failing. By installing [pre-commit](https://pre-commit.com/) hooks like here,
whenever you do a `git commit` in this repo, a series of checks and cleanup tasks are run, until everything is in a state
that will hopefully make Github Actions not complain when you push your changes.

```
pre-commit install
pre-commit install --hook-type commit-msg
```

In addition to some Python-specific checks and cleanup tasks, this will also check your commit message so it's in line with the suggested format:
https://www.conventionalcommits.org/en/v1.0.0/

## Run kiara

To check if everything works as expected and you can start adding/changing code in this repository, run any `kiara` command:

```
kiara operation list -t onboarding
```

If everything is set up correctly, the output of this command should contain a few operations that are implemented in this repository.
