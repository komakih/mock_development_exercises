import os
from app.modules.utils.slack_notifier import send_slack_message

webhook_url = os.getenv("SLACK_WEBHOOK_URL")
if webhook_url:
    success = send_slack_message("Slack通知のテストメッセージです。", webhook_url)
    print("送信成功" if success else "送信失敗")
else:
    print("Webhook URLが設定されていません")
