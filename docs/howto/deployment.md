# Ansible deployment

It's possible that this works or can be made to work easily - I do not know.  The ansible setup was inherited
from the Sidewinder template project.

# GCloud deployment

Mostly this is rough notes for my own (Lisa's) benefit, I should clean up at some point.
DTI is running this on Google Cloud at present, using Google App Engine and Cloud SQL.

I used these instructions: https://cloud.google.com/python/django/run

* including the part about proxying to Cloud SQL so that commands to migrate the db could
be run locally
* deploying from a directory just for deploy means I have an .env file ready for deploy in that directory

First time:

* create a directory portmap-deploy
* git clone the portmap project into it
* copy the production .env file into it
* copy the production key file (.pem file) into it
* create a .gcloudignore file (TODO can include in project?) so as not to deploy .git files especially
* get gcloud permissions for SQL, App Engine, 3 storage buckets, builds and service accounts
* Run `gcloud config set project portability-map`

To do a deploy
```
cd portmap-deploy
git pull origin main
python3 manage.py collectstatic
gcloud app deploy

gcloud app browse
gcloud app logs tail -s default
```

to clean up:

```
gcloud app versions list --format="value(version.id)" --sort-by="~version.createTime" | tail -n +6 | xargs -r gcloud app versions delete --quiet
```

to do direct db stuff like migrations:

```
gcloud auth application-default login
../bin/cloud-sql-proxy --address 0.0.0.0 --port 1234 portability-map:europe-west1:portability-map
(edit .env to use proxy instead of direct cloud cxn)
python3 manage.py migrate
(reset to regular .env that gets pushed to gcloud)

```

LMDTODO: these need to be put into a script - instead of editing .env, have a env variable for proxy run right from the command
