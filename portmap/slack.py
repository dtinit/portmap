from django.conf import settings
import requests

def notify(text):
    requests.post(settings.SLACK_NOTIFICATION_WEBHOOK_URL, json={'text':text})
