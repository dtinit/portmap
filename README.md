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
PostgreSQL DB. The DB also captures query data so we can learn what users most need to find.

Dependency management is by the process recommended in "Boost Your Django DX" and in Adam Johnson's
blog posts: use pip, venv, and requirements.txt. For dev requirements, also use pip to install ipython...

PortMap's original project organization is from [Sidewinder](https://stribny.github.io/sidewinder), a django starter project template,
which set us up with:

- environment variables (and the 'environ' package) instead of juggling multiple configuration files
- Use HTMX for modern frontends
- Use django-allauth to provide email-based and 3rd party authentication.
- Have a custom User model for ultimate flexibility
- auto reloading, debugging and profiling tools, linters and formatters
- Log anything you want with structured logging
- Execute automated tests using the best testing library pytest
- Write test fixtures efficiently using factoryboy and Faker

## Local development

### First time setup

You will need Python 3 and pip (`python -m ensurepip --upgrade`). PortMap also requires a PostgreSQL database for storing artices; create one locally named "portmap" and start it.

1. Get the private key file from @lisad for accessing the GitHub API. This should not be checked into git, so **please don't put it in this repository!**

2. Make a copy of .env-example and name it .env. This is where your local configuration will be stored; it's not checked into git.

3. In your new .env file, change `DJ_DATABASE_CONN_STRING` to point to your local PostgreSQL database.

4. Also in your .env file, change `GITHUB_PRIVATE_KEY_PEM_FILE=<path to the key file from step 1>`.

5. Install dependencies with pip.

```bash
python -m pip install -r requirements.txt
```

> Note: This may fail if you're missing external dependencies; you'll need to inspect the output and install whatever is missing (e.g. python3-devel, gcc, libpq-devel)

6. Initialize your PostgreSQL database.

```bash
./manage.py migrate
```

7. Create a superuser for yourself for accessing the database management portal.

```bash
./manage.py createsuperuser
```

8. Start the server. By default it will listen for requests at http://localhost:8000

```bash
./manage.py runserver
```

9. To populate your local database with articles from https://github.com/dtinit/portability-articles, go to https://localhost:8000/dj-admin and enter your superuser credentials from step 7. Click on "Articles" (under "Core"), and then press the "Populate Articles" button in the top right.

### Frontend

Frontend dev tools like ESLint are delivered via [npm](https://www.npmjs.com/), which is included with Node.js. To use the tools locally, you'll need to:

1. Install [Node.js](https://nodejs.org).
2. Run `npm install` wherever you cloned this repository to.

#### Linting with ESLint

You can run the linter by executing `npm run lint`. If there are no issues, there won't be any output.

To get linting feedback right in your code editor, [check here](https://eslint.org/docs/latest/use/integrations) to find an ESLint integration or instructions for your editor. The configuration file is named [.eslintrc.json](.eslintrc.json), but your editor/integration will probably find it for you.
