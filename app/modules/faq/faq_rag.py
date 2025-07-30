from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import numpy as np
import json

class FAQMemoryRAG:
    def __init__(self, faq_json_path):
        with open(faq_json_path, encoding="utf-8") as f:
            faq_data = json.load(f)
        self.questions = [item['question'] for item in faq_data]
        self.answers = [item['answer'] for item in faq_data]

        self.embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        self.question_embeddings = self.embeddings_model.embed_documents(self.questions)
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    def search(self, query, top_k=5, threshold=0.8):
        query_embedding = self.embeddings_model.embed_documents([query])[0]
        similarities = np.dot(self.question_embeddings, query_embedding)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        if similarities[top_indices[0]] < threshold:
            return "関連する情報が見つかりませんでした。"

        retrieved_qas = [(self.questions[i], self.answers[i]) for i in top_indices]

        prompt = self._format_prompt(query, retrieved_qas)
        result = self.llm.invoke(prompt)

        return result.content

    def _format_prompt(self, query, retrieved_qas):
        qa_pairs = "\n\n".join(
            [f"Q: {q}\nA: {a}" for q, a in retrieved_qas]
        )
        return (
            f"以下のFAQ情報を参考に質問に回答してください。\n\n"
            f"{qa_pairs}\n\n"
            f"質問: {query}\n"
            f"回答:"
        )

# インスタンス化（app起動時に一度だけ）
faq_rag = FAQMemoryRAG('data/faq_data.json')
