# 🎓 EduBot – AI-Powered College Chatbot  
**Dhaanish Ahmed Institute of Technology**

> An intelligent and interactive chatbot designed to answer student queries about courses, admissions, fees, placements, and more — powered by Semantic Search and Generative AI (LLMs).

![EduBot Screenshot](backend/static/assets/Screen.png) 

---

## 🚀 Features

- 💬 **Smart Chat Interface**: Built with HTML/CSS and responsive UI design.
- 🔍 **Semantic Search Matching**: Uses `sentence-transformers` to match user queries with college FAQs.
- 🤖 **LLM-Powered Fallback (FLAN-T5)**: Generates intelligent responses when no exact FAQ match is found.
- 📁 **College Website Clone UI**: Integrated as a floating chatbot on a clone of your college homepage.
- 🌗 **Dark/Light Mode Toggle**: Modern theme support for better accessibility.
- 📌 **Suggested Quick Prompts**: Users can click preset questions like “Fees” or “Placement”.
- 🔒 **Deployed via Flask**: Fast and easy backend setup ready for cloud deployment.

---

## 🛠️ Tech Stack

| Frontend | Backend | AI Models | Libraries |
|----------|---------|-----------|-----------|
| HTML, CSS, JS | Flask (Python) | `all-MiniLM-L6-v2`, `flan-t5-base` | sentence-transformers, transformers, NumPy, scikit-learn |

---

## 🧠 How It Works

1. The user sends a query via the chatbot interface.
2. The system first attempts **semantic similarity** with a local FAQ list.
3. If no match is strong enough (threshold < 0.5), a **LLM (FLAN-T5)** generates a response.
4. The chatbot replies in real-time with helpful college-specific information.

---
