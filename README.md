# SITNAGPUR Student FAQ Chatbot

This project is a student-support chatbot prototype built for a chatbot/NLP assignment. It includes a web-based interface in HTML/CSS/JavaScript and a more detailed CLI-oriented Python version for demonstrating the assignment topics.

## Assignment Coverage

The project now covers the key chatbot requirements shown in the rubric:

- Rule-based FAQ responses
- Text preprocessing with lowercasing, punctuation cleanup, and stopword removal
- Synonym-aware matching
- FAQ retrieval with TF-IDF-style scoring
- Intent classification using patterns
- Entity extraction for dates, courses, semesters, and branches
- Follow-up context handling
- Fallback and human handover logic
- Basic analytics tracking

## Files

- `index.html` - chatbot UI
- `style.css` - chatbot styling
- `script.js` - browser chatbot logic with assignment features
- `student_faq_chatbot.py` - CLI chatbot with multichannel formatting and analytics

## Run the Web Version

1. Open `index.html` in a browser.
2. Use the chat box or quick actions to test the bot.

Suggested test queries:

- `What is the fee for B.Tech?`
- `Tell me about scholarships`
- `When is the exam timetable for third year?`
- `What about hostel?`
- `I have an urgent complaint`

## Run the Python Version

```bash
python3 student_faq_chatbot.py
```

The Python version also demonstrates:

- multichannel formatting (`cli`, `sms`, `email`, `whatsapp`)
- persistent analytics logging
- command-based interaction like `stats`, `history`, and `switch whatsapp`

## Notes

- The data is demo data for a student chatbot prototype.
- The web version stores lightweight analytics in browser `localStorage`.
- The Python version stores analytics in `chat_analytics.json`.
