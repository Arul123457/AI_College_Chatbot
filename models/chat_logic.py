import os
os.environ["USE_TF"] = "0"

import json, random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import pipeline

# ─── 1) Load models ─────────────────────────────────────────────────────────────
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
generative = pipeline("text2text-generation", model="google/flan-t5-base", device=-1)

# ─── 2) Load FAQ ────────────────────────────────────────────────────────────────
with open(os.path.join(os.path.dirname(__file__), "..", "data", "college_faq.json"), encoding="utf-8") as f:
    faq = json.load(f)
questions = [q["question"] for q in faq]
embeddings = semantic_model.encode(questions)

# ─── 3) Helper: get top‑k FAQs ─────────────────────────────────────────────────
def retrieve_top_k(user_input, k=3):
    emb = semantic_model.encode([user_input])[0]
    sims = cosine_similarity([emb], embeddings)[0]
    idxs = np.argsort(sims)[::-1][:k]
    return [(faq[i]["question"], faq[i]["answer"], float(sims[i])) for i in idxs]

# ─── 4) Main response generator ────────────────────────────────────────────────
GREET_INS = {"hi","hello","hey"}
GREET_OUTS = [
    "Hi! Tulasi here – how can I help you today?",
    "Hello! What would you like to know about our college?",
]

def generate_chat_response(user_input: str) -> str:
    ui = user_input.strip().lower()
    if ui in GREET_INS:
        return random.choice(GREET_OUTS)

    top = retrieve_top_k(user_input, k=3)
    # if best is *very* close, just return it
    if top[0][2] > 0.75:
        return top[0][1]

    # build RAG prompt
    context = "\n".join([f"Q: {q}\nA: {a}" for q,a,_ in top])
    prompt = (
        "You are Tulasi, the AI assistant for Dhaanish Ahmed Institute of Technology.\n"
        "Use the facts below to answer the student’s question. "
        "If none apply, say “I’m sorry, I don’t have that information. Please contact administartion office 0422 7272065”\n\n"
        f"{context}\n\n"
        f"Student Q: {user_input}\nTulasi A:"
    )
    out = generative(prompt, max_new_tokens=80)[0]["generated_text"].strip()
    return out
