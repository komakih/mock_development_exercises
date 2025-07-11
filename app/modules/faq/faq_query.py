# app/modules/faq/faq_query.py
from app.models import Faq

def find_similar_questions(user_input, limit=3):
    results = Faq.query.filter(Faq.question.ilike(f'%{user_input}%')).limit(limit).all()
    return [{"question": faq.question, "answer": faq.answer} for faq in results]