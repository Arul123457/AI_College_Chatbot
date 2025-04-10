import os
os.environ["USE_TF"] = "0"  # Disable TensorFlow backend

import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ✅ Load the semantic model (lightweight & fast)
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ Load FAQ data
faq_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'college_faq.json')
with open(faq_path, 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

faq_questions = [item['question'] for item in faq_data]
faq_embeddings = semantic_model.encode(faq_questions)

# ✅ Keyword to question mapping
KEYWORD_BOOST = {
    "btech fees": "What are the fees for B.Tech?",
    "fees": "What are the fees for B.Tech?",
    "admission date": "When does the admission process start?",
    "admission process": "When does the admission process start?",
    "course list": "Which courses are offered?",
    "courses": "Which courses are offered?",
    "contact": "How can I contact the college?",
    "college contact": "How can I contact the college?",
    "hostel food": "How is the Food at Hostel?",
    "food": "How is the Food at Hostel?",
    "backlog": "Can I apply with a backlog in one subject?",
    "ai club": "Are there any AI or robotics clubs in the college?",
    "robotics club": "Are there any AI or robotics clubs in the college?",
    "lateral entry": "What is the process for lateral entry into B.Tech?",
    "internship": "Does the college provide internships?",
    "documents": "What documents are required for admission?",
    "placement facility": "Is placement support available for students?",
    "convocation": "How can I register for convocation?",
    "girl hostel": "Are hostel facilities available for girls?",
    "salary": "What is the Highest salary package student placed?",
    "highest package": "What is the Highest salary package student placed?",
    "about": "About the college?",
    "college info": "About the college?",
    "how to apply": "How can I get a admission?",
    "ragging": "Is there any ragging issues in the campus?",
    "smart class": "Does your college provide smart classes?",
    "vision": "What is your college vision and mission?",
    "mission": "What is your college vision and mission?",
    "placement record": "What is your college placement Record?",
    "placed": "What is your college placement Record?",
    "companies": "Who are some of the recruiters that visit the campus?",
    "recruiters": "Who are some of the recruiters that visit the campus?"
}

# ✅ Semantic matching
def semantic_match(user_input):
    user_embedding = semantic_model.encode([user_input])[0]
    similarities = cosine_similarity([user_embedding], faq_embeddings)[0]
    best_match_index = int(np.argmax(similarities))
    best_score = float(similarities[best_match_index])
    return best_score, faq_data[best_match_index]['answer']

# ✅ Keyword booster
def keyword_boost_match(user_input):
    for keyword, question_text in KEYWORD_BOOST.items():
        if keyword in user_input.lower():
            for item in faq_data:
                if item["question"].lower().strip() == question_text.lower().strip():
                    return item['answer']
    return None

# ✅ Main response logic
def generate_chat_response(user_input):
    # Priority 1: Keyword Boost
    keyword_answer = keyword_boost_match(user_input)
    if keyword_answer:
        return keyword_answer

    # Priority 2: Semantic Match
    score, answer = semantic_match(user_input)
    if score >= 0.5:
        return answer

    # Priority 3: Fallback message
    return "I'm sorry, I couldn't find a relevant answer. Could you rephrase your question?"
