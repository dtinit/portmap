# Portability Map

<br><br>

> A way to search a content repository of portability solutions

<br>

**PortMap** is an open-source [Django](https://www.djangoproject.com/) project that hosts structured
query access to a content repository of portability solutions.

PortMap pulls articles on portability solutions from the
[portability-articles](https://github.com/dtinit/portability-articles) repository, which is where
volunteers can contribute content.

The articles are organized by topic, data type, source and destination, and cached in a
PostgreSQL DB.  The DB also captures query data so we can learn what users most need to find.

Dependency management is by the process recommended in "Boost Your Django DX" and in Adam Johnson's
blog posts: use pip, venv, and requirements.txt.  For dev requirements, also use pip to install ipython...

PortMap's original project organization is from [Sidewinder](https://stribny.github.io/sidewinder), a django starter project template,
which set us up with:

* environment variables (and the 'environ' package) instead of juggling multiple configuration files
* Use HTMX for modern frontends
* Use django-allauth to provide email-based and 3rd party authentication.
* Have a custom User model for ultimate flexibility
* auto reloading, debugging and profiling tools, linters and formatters
* Log anything you want with structured logging
* Execute automated tests using the best testing library pytest
* Write test fixtures efficiently using factoryboy and Faker
