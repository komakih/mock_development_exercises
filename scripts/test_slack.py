import os
from app import create_app
from app.modules.utils.slack_notifier import send_slack_message

app = create_app()
with app.app_context():
    success = send_slack_message("Slack通知のテストメッセージです。")
    print("送信成功" if success else "送信失敗")
