from app import create_app, db
from app.models import Faq

app = create_app()
with app.app_context():
    db.create_all()
    sample_faqs = [
        Faq(question="ログインできない", answer="パスワード再設定を試してください。"),
        Faq(question="登録方法を教えて", answer="登録ページから必要事項を入力してください。"),
        Faq(question="パスワードを忘れた", answer="パスワード再設定リンクを送信しますのでメールアドレスを入力してください。")
    ]
    db.session.add_all(sample_faqs)
    db.session.commit()