import requests

def send_slack_message(message, webhook_url=None):
    if webhook_url is None:
        # ← 遅延インポートで循環回避
        from app.models import AppConfig
        webhook_url = AppConfig.get_config('SLACK_WEBHOOK_URL')

    if webhook_url is None:
        print("Slack webhook URLが見つかりません。")
        return False

    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[Slack通知失敗] {e}")
        return False
