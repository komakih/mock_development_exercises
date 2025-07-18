from app import create_app
from app.modules.routes.index_manager import IndexManager
from app.modules.utils.slack_notifier import send_slack_message
import sys

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        result = IndexManager.update_index()
        if result['success']:
            print(f"インデックス更新成功！処理した文書数: {result['document_count']}（所要時間: {result['time']:.2f}秒）")
        else:
            error_message = f"CLIからのインデックス更新でエラーが発生しました: {result['error']}"
            print(error_message)
            send_slack_message(error_message)  # Slack通知を送信
            sys.exit(1)