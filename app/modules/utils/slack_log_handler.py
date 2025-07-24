import logging, json
from app.modules.utils.slack_notifier import send_slack_message


class SlackLogHandler(logging.Handler):
    def emit(self, record):
        from app.modules.utils.buffered_slack_notifier import buffer  # 遅延import
        try:
            log_json = json.loads(record.getMessage())
            log_entry = (
                f"{log_json.get('error_type', 'UnknownError')}: {log_json.get('message', '')}\n"
                f"Trace: {log_json.get('stack_trace', '')[:500]}"
            )
        except json.JSONDecodeError:
            log_entry = self.format(record)

        buffer.add(log_entry)