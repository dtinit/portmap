# Portability Map

<br><br>

> A way to search a content repository of portability solutions

<br>

**PortMap** is an open-source [Django](https://www.djangoproject.com/) project that hosts structured
query access to a content repository of portability solutions.

PortMap is based on [Sidewinder](https://stribny.github.io/sidewinder) which is a django starter project template,
which sets us up with:

* Poetry as dependency manager to manage the virtual environment
* environment variables instead of juggling multiple configuration files
* Use HTMX for modern frontends
* Use django-allauth to provide email-based and 3rd party authentication.
* Have a custom User model for ultimate flexibility
* Have a Huey task queue for background and periodic tasks
* auto reloading, debugging and profiling tools, linters and formatters
* Log anything you want with structured logging
* Execute automated tests using the best testing library pytest
* Write test fixtures efficiently using factoryboy and Faker
* End-to-end test your frontend using Playwright
* Deploy to your own VPS in the "It just works" style using Ansible
* Not be limited in customization as all important files are exposed and ready to be changed
