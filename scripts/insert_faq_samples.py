import re
import os
from app import create_app, db
from app.models import Faq

# ChromaDBを初期化させないよう、環境変数で制御する（アプリ側で対応必要）
os.environ["SKIP_CHROMADB_INIT"] = "true"

app = create_app()

def parse_faq_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"### Q: (.*?)\nA: (.*?)(?=\n### Q:|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    faq_entries = [Faq(question=q.strip(), answer=a.strip()) for q, a in matches]
    return faq_entries

if __name__ == "__main__":
    faq_file_path = 'data/faq.md'
    faqs = parse_faq_markdown(faq_file_path)

    with app.app_context():
        db.create_all()
        db.session.bulk_save_objects(faqs)
        db.session.commit()

    print(f"{len(faqs)}件のFAQをDBに投入しました。")
