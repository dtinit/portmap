# Installation

!!! info

    There is currently no project generator. To start using Sidewinder, clone the [repository](https://github.com/stribny/sidewinder) and make configuration
    changes in your local copy.

## Clone the repository

!!! tip

    Feel free to [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) first so that you don't have to
    set up Git remotes later.

You can clone Sidewinder from the official repository or your fork:

```
git clone https://github.com/stribny/sidewinder
```

## Prerequisites

### Install Python 3.9+

Before installing Sidewinder, you will need Python 3.9

### Install watchman

For fast hot-reloading, make sure to install [watchman](https://facebook.github.io/watchman/docs/install.html).

### Install graphviz (optional)

Graphviz is needed by [django-extensions](https://django-extensions.readthedocs.io) for generating model diagrams. You will need to figure out how to
install it for your system.

On Fedora, use `dnf`:

```
dnf install graphviz graphviz-devel
```

If you plan to use this feature, install dependencies in the next step with `--with graphviz`.

You can also skip this step if you don't plan to use this feature.

## Use virtualenv and pip install

In order to work on Google App Engine, which seems to require requirements.txt, this
project ought to be run with a plain old virtual env and pip

```
pip install -r requirements.txt
```

## Install Playwright

```bash
# inside virtual environment
playwright install
```

Now, [configure the project](configuration.md).
