import requests
from app.models import AppConfig

def send_slack_message(message, webhook_url=None):
    webhook_url = AppConfig.get_config('SLACK_WEBHOOK_URL')
    if webhook_url is None:
        raise ValueError("Slack webhook URLが設定されていません。")

    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200