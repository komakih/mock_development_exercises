import os
import requests

def send_slack_message(message, webhook_url=None):
    if webhook_url is None:
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if webhook_url is None:
        raise ValueError("Slack webhook URLが設定されていません。")

    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200