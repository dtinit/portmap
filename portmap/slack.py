from django.conf import settings
import requests

def notify(text):
    try:
        requests.post(settings.SLACK_NOTIFICATION_WEBHOOK_URL, json={'text':text})
    except:
        print("Slack notification failed. Is SLACK_NOTIFICATION_WEBHOOK_URL set correctly?")
