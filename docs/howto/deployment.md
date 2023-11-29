# Ansible deployment

It's possible that this works or can be made to work easily - I do not know.  The ansible setup was inherited
from the Sidewinder template project.

# GCloud deployment

Mostly this is rough notes for my own (Lisa's) benefit, I should clean up at some point.
DTI is running this on Google Cloud at present, using Google App Engine and Cloud SQL.

I used these instructions: https://cloud.google.com/python/django/run
* including the part about proxying to Cloud SQL so that commands to migrate the db could
be run locally

'''
gcloud app deploy
gcloud auth application-default login
(stop competing SQL ports if necessary)
../bin/cloud-sql-proxy --address 0.0.0.0 --port 5432 portability-map:europe-west1:portability-map
(edit .env to use proxy instead of direct cloud cxn)
python3 manage.py migrate
(reset to local SQL and regular .env)


gcloud app browse
gcloud app logs tail -s default
'''
