import os
os.environ["USE_TF"] = "0"  # Prevent transformers from loading TensorFlow

import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import pipeline

# Load semantic model
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load fallback LLM
generative_model = pipeline("text2text-generation", model="google/flan-t5-base", device=-1)

# Load FAQ data
faq_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'college_faq.json')
with open(faq_path, 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

faq_questions = [item['question'] for item in faq_data]
faq_embeddings = semantic_model.encode(faq_questions)

# Keyword Boost Map
KEYWORD_BOOST = {
    "fees": "What are the fees for B.Tech?",
    "btech fees": "What are the fees for B.Tech?",
    "admission date": "When does the admission process start?",
    "admission process": "When does the admission process start?",
    "courses": "Which courses are offered?",
    "course list": "Which courses are offered?",
    "contact": "How can I contact the college?",
    "college contact": "How can I contact the college?",
    "hostel food": "How is the food in the hostel?",
    "backlog": "Can I apply with a backlog?",
    "clubs": "Are there any AI or robotics clubs?",
    "robotics club": "Are there any AI or robotics clubs?",
    "ai club": "Are there any AI or robotics clubs?",
    "lateral entry": "What is the process for lateral entry?",
    "internship": "Does the college offer internships?",
    "documents": "What documents are required for admission?",
    "placement": "Is placement support available?",
    "convocation": "How do I register for convocation?",
    "girls hostel": "Are there hostel facilities for girls?",
    "highest salary": "What is the highest placement package?",
    "placement package": "What is the highest placement package?",
    "about college": "Tell me about the college?",
    "college info": "Tell me about the college?",
    "how to apply": "How can I get admission?",
    "ragging": "Is ragging allowed in the campus?",
    "smart class": "Are smart classrooms available?",
    "smart classroom": "Are smart classrooms available?",
    "vision": "What is your college vision and mission?",
    "mission": "What is your college vision and mission?",
    "placement record": "What is your placement record?",
    "placed": "What is your placement record?",
    "companies": "Which companies hire from your campus?",
    "recruiters": "Which companies hire from your campus?",
    "scholarship": "Does your college offer scholarships?",
    "infrastructure": "How is your campus infrastructure?",
    "facilities": "How is your campus infrastructure?",
    "transport": "Do you offer transportation facilities?",
    "bus facility": "Do you offer transportation facilities?"
}

def semantic_match(user_input):
    user_embedding = semantic_model.encode([user_input])[0]
    similarities = cosine_similarity([user_embedding], faq_embeddings)[0]
    best_match_index = int(np.argmax(similarities))
    best_score = float(similarities[best_match_index])
    return best_score, faq_data[best_match_index]['answer']

def keyword_boost_match(user_input):
    for keyword, question_text in KEYWORD_BOOST.items():
        if keyword in user_input.lower():
            for item in faq_data:
                if item["question"].lower().strip() == question_text.lower().strip():
                    return item['answer']
    return None

def llama_generate(prompt):
    response = generative_model(prompt, max_new_tokens=100)[0]['generated_text']
    return response.strip()

def generate_chat_response(user_input):
    # Try keyword-boosted match first
    keyword_answer = keyword_boost_match(user_input)
    if keyword_answer:
        return keyword_answer

    # Fallback to semantic matching
    score, answer = semantic_match(user_input)
    if score >= 0.5:
        return answer

    # LLM fallback with custom bot identity
    fallback_prompt = (
        f"You are a helpful college chatbot named Tulasi from Dhaanish Ahmed Institute of Technology. "
        f"Answer the following question in a polite and informative tone.\n\nQ: {user_input}\nA:"
    )
    return llama_generate(fallback_prompt)