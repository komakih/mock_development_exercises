from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock
from app.openai_utils import get_chatgpt_response
from app.modules.utils.slack_notifier import send_slack_message

class LogBuffer:
    def __init__(self):
        self._logs = []
        self._lock = Lock()

    def add(self, log_entry):
        with self._lock:
            self._logs.append(log_entry)

    def flush(self):
        with self._lock:
            logs = self._logs[:]
            self._logs.clear()
        return logs

buffer = LogBuffer()

def summarize_and_notify(app):
    with app.app_context():  # ← Flaskのアプリインスタンスを直接指定
        from app.models import AppConfig
        logs = buffer.flush()
        if not logs:
            return

        prompt = "以下のログを運用チーム向けに簡潔に要約してください:\n" + "\n".join(logs)

        try:
            summary, _ = get_chatgpt_response("log_summary", [
                {"role": "system", "content": "あなたはインフラ監視用の要約AIです。"},
                {"role": "user", "content": prompt}
            ])
        except Exception as e:
            summary = f"[要約失敗] {e}"

        if AppConfig.get_config("ENABLE_SLACK_LOG_SUMMARY") != "false":
            send_slack_message(summary)

def get_notify_interval(app):
    with app.app_context():
        from app.models import AppConfig
        try:
            return int(AppConfig.get_config("SLACK_NOTIFY_INTERVAL") or 60)
        except Exception:
            return 60

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        summarize_and_notify,
        'interval',
        seconds=get_notify_interval(app),
        args=[app],
        max_instances=1
    )
    scheduler.start()

    return scheduler
