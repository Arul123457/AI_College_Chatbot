# ✅ test_tulasi_bot.py

import requests
import csv
import time

# URL of your running Flask server
CHATBOT_URL = "http://127.0.0.1:5000/chat"  # or your Render URL if hosted

# List of 50 queries for testing
queries = [
    "What is the B.Tech fees per year?",
    "When does admission start?",
    "What courses are available?",
    "How can I contact the college?",
    "How is the food in hostel?",
    "Can I join with one backlog?",
    "Are there any robotics clubs?",
    "How to apply for lateral entry?",
    "Does the college provide internships?",
    "What documents are needed for admission?",
    "Is placement support available?",
    "How to register for convocation?",
    "Is there a separate hostel for girls?",
    "What is the highest placement salary?",
    "Tell me about Dhaanish Ahmed Institute.",
    "How can I apply for admission?",
    "Any ragging issues in campus?",
    "Are smart classes available?",
    "What is the vision and mission of the college?",
    "How good is your placement record?",
    "Who are your top recruiters?",
    "Are scholarships offered?",
    "How good are the campus facilities?",
    "Is transport provided for students?",
    "What are hostel fees?",
    "Are there weekend classes available?",
    "How are the lab facilities?",
    "Is WiFi available in hostels?",
    "What is the college timing?",
    "Are there cultural events?",
    "Can international students apply?",
    "Is dress code mandatory?",
    "How is the library infrastructure?",
    "How can I apply for scholarships?",
    "Do you have a canteen?",
    "Are there placement training programs?",
    "What extracurricular activities are available?",
    "Do you have MOUs with industries?",
    "Is biometric attendance mandatory?",
    "What are hostel rules?",
    "How many students are placed every year?",
    "Tell me about the Food Technology department.",
    "Do you have smart boards in classes?",
    "Are there startup support programs?",
    "How many students can stay in a room?",
    "What sports facilities are available?",
    "Can students take industrial visits?",
    "How to get convocation certificate?",
    "Is there on-campus medical support?",
    "Are you approved by AICTE and NAAC?"
]

# Save results to a CSV
with open('tulasi_bot_test_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Bot Answer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for query in queries:
        try:
            res = requests.post(CHATBOT_URL, json={"message": query})
            bot_response = res.json().get("response", "❌ Error")
            print(f"Q: {query}\nA: {bot_response}\n")
            writer.writerow({'Query': query, 'Bot Answer': bot_response})
            time.sleep(0.5)  # Avoid sending too fast
        except Exception as e:
            print(f"Error for query '{query}': {e}")

print("\n✅ Testing completed. Results saved to 'tulasi_bot_test_results.csv'.")
