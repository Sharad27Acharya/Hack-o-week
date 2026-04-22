import re
import json
import math
import datetime
import string
import os
from collections import defaultdict, Counter


# ─────────────────────────────────────────────────────────────────
# TOPIC 1 — BASIC FAQ KNOWLEDGE BASE
# ─────────────────────────────────────────────────────────────────
FAQ_DB = {
    "admission": {
        "answer": "Admissions are open from June 1 to August 31 every year. "
                  "Apply online at admissions.college.edu or visit the office.",
        "keywords": ["admission", "apply", "enroll", "registration", "join"]
    },
    "fee": {
        "answer": "Tuition fee for undergraduate is ₹45,000/year and postgraduate is ₹60,000/year. "
                  "Scholarships are available for meritorious students.",
        "keywords": ["fee", "fees", "tuition", "cost", "payment", "scholarship", "money"]
    },
    "exam": {
        "answer": "Mid-term exams are held in October and March. "
                  "Final exams are in December and May. Hall tickets are issued 10 days before.",
        "keywords": ["exam", "examination", "test", "midterm", "final", "hall ticket", "schedule"]
    },
    "result": {
        "answer": "Results are declared within 30 days of the last exam. "
                  "Check the student portal at results.college.edu using your roll number.",
        "keywords": ["result", "results", "marks", "grade", "score", "pass", "fail", "gpa", "cgpa"]
    },
    "library": {
        "answer": "The library is open Monday–Saturday, 8 AM to 8 PM. "
                  "Students can borrow up to 3 books for 14 days.",
        "keywords": ["library", "book", "books", "borrow", "return", "reading"]
    },
    "hostel": {
        "answer": "Hostel accommodation is available on campus. "
                  "Apply through the hostel office before July 15. Monthly fee is ₹4,500.",
        "keywords": ["hostel", "accommodation", "dorm", "dormitory", "room", "stay", "residential"]
    },
    "holiday": {
        "answer": "The academic calendar lists all holidays. Major ones: Diwali (5 days), "
                  "Christmas (2 days), Holi (1 day), and all national holidays.",
        "keywords": ["holiday", "vacation", "break", "off", "leave", "festival"]
    },
    "course": {
        "answer": "We offer B.Tech, BCA, BBA, MBA, MCA, and M.Tech programs. "
                  "Each has specialisations. Visit college.edu/courses for details.",
        "keywords": ["course", "courses", "program", "programmes", "branch", "stream", "department"]
    },
    "attendance": {
        "answer": "Minimum 75% attendance is mandatory to sit in exams. "
                  "Medical leave requires a certificate submitted within 3 days.",
        "keywords": ["attendance", "absent", "present", "proxy", "leave", "bunk"]
    },
    "placement": {
        "answer": "Our placement cell organises campus drives from October to March. "
                  "Past recruiters include TCS, Infosys, Wipro, and Google. Average package: ₹6 LPA.",
        "keywords": ["placement", "job", "recruit", "campus", "company", "salary", "package", "career"]
    },
    "contact": {
        "answer": "Reach the admin office at: 📞 +91-22-12345678 | ✉ info@college.edu | "
                  "Office hours: Mon–Fri, 9 AM–5 PM.",
        "keywords": ["contact", "phone", "email", "address", "office", "reach", "call", "helpdesk"]
    },
    "greeting": {
        "answer": "Hello! I'm the College FAQ Bot 🎓. I can help with admissions, fees, "
                  "exams, results, library, hostel, placements, and more. What's your question?",
        "keywords": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy"]
    },
    "farewell": {
        "answer": "Goodbye! Feel free to return if you have more questions. Good luck! 👋",
        "keywords": ["bye", "goodbye", "see you", "thanks", "thank you", "ok thanks", "that's all"]
    },
}

# ─────────────────────────────────────────────────────────────────
# TOPIC 3 — SYNONYMS MAP
# ─────────────────────────────────────────────────────────────────
SYNONYMS = {
    "fee": ["fees", "tuition", "cost", "charge", "payment", "price", "money", "rupees", "amount"],
    "exam": ["examination", "test", "assessment", "quiz", "paper", "viva", "mid sem", "end sem"],
    "result": ["results", "marks", "grades", "score", "gpa", "cgpa", "percentage", "outcome"],
    "admission": ["admissions", "apply", "application", "enrollment", "enroll", "joining"],
    "hostel": ["dorm", "dormitory", "accommodation", "residence", "pg", "room", "lodge"],
    "course": ["program", "branch", "stream", "subject", "department", "degree", "specialization"],
    "placement": ["job", "internship", "recruit", "campus drive", "career", "hiring", "package"],
    "holiday": ["vacation", "break", "off day", "leave", "festival", "recess"],
    "attendance": ["absent", "present", "bunk", "proxy", "missing class"],
    "library": ["books", "reading room", "journal", "borrow", "lending"],
    "contact": ["helpline", "phone", "email", "reach out", "get in touch", "call", "support"],
    "hi": ["hello", "hey", "hiya", "sup", "greetings", "namaste", "good morning", "good evening"],
    "bye": ["goodbye", "see you", "cya", "take care", "later", "thanks", "thank you"],
}

# ─────────────────────────────────────────────────────────────────
# TOPIC 5 — INTENT PATTERNS
# ─────────────────────────────────────────────────────────────────
INTENT_PATTERNS = {
    "greeting":    [r"\b(hi|hello|hey|howdy|namaste|good\s?(morning|evening|afternoon))\b"],
    "farewell":    [r"\b(bye|goodbye|see\s?you|cya|take\s?care|thanks|thank\s?you)\b"],
    "fee_inquiry": [r"\b(fee|fees|tuition|cost|how\s?much|payment|scholarship)\b"],
    "exam_inquiry":[r"\b(exam|test|examination|midterm|final|schedule|paper|hall\s?ticket)\b"],
    "result_query":[r"\b(result|marks|grade|score|cgpa|gpa|pass|fail)\b"],
    "admission":   [r"\b(admission|apply|enroll|registration|join)\b"],
    "hostel":      [r"\b(hostel|dorm|accommodation|room|stay)\b"],
    "placement":   [r"\b(placement|job|career|company|package|recruit)\b"],
    "course_info": [r"\b(course|program|branch|b\.?tech|mba|mca|bca|bba|m\.?tech)\b"],
    "attendance":  [r"\b(attendance|absent|present|bunk|proxy|leave)\b"],
    "library":     [r"\b(library|book|borrow|return|reading)\b"],
    "contact":     [r"\b(contact|phone|email|address|office|call|reach)\b"],
    "holiday":     [r"\b(holiday|vacation|break|festival|off)\b"],
    "help":        [r"\b(help|what\s?can\s?you|options|menu|assist)\b"],
}

# ─────────────────────────────────────────────────────────────────
# TOPIC 6 — ENTITY PATTERNS (Dates & Courses)
# ─────────────────────────────────────────────────────────────────
DATE_PATTERNS = [
    r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",                         # 12/05/2024
    r"\b(\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s?\d{0,4})\b",  # 12 May 2024
    r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b",
    r"\b(today|tomorrow|yesterday|next\s?week|next\s?month|monday|tuesday|wednesday|thursday|friday)\b",
    r"\b(\d{4})\b(?=\s*(year|batch|semester))",                       # 2024 year
]

COURSE_PATTERNS = [
    r"\b(b\.?tech|m\.?tech|bca|mca|bba|mba|b\.?sc|m\.?sc|b\.?com|m\.?com|phd|diploma)\b",
    r"\b(computer\s?science|information\s?technology|mechanical|civil|electrical|electronics)\b",
    r"\b(data\s?science|artificial\s?intelligence|machine\s?learning|cyber\s?security)\b",
    r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth)\s?(year|semester|sem)\b",
    r"\b([1-8](?:st|nd|rd|th)\s?(year|semester|sem))\b",
]

# ─────────────────────────────────────────────────────────────────
# TOPIC 2 — PREPROCESSING
# ─────────────────────────────────────────────────────────────────
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "you", "your", "he", "she",
    "it", "they", "what", "which", "who", "this", "that", "am", "is",
    "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "must", "shall", "can", "a", "an", "the", "and", "but",
    "or", "so", "if", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "up", "about", "into", "through", "during", "before",
    "after", "then", "than", "also", "just", "no", "not", "only", "same",
    "please", "tell", "know", "want", "need", "get", "got", "like", "how",
}

def preprocess(text: str) -> str:
    """Topic 2: Normalize, lowercase, remove punctuation, strip stopwords."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)          # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()       # collapse spaces
    tokens = text.split()
    filtered = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return " ".join(filtered) if filtered else text


def apply_synonyms(text: str) -> str:
    """Topic 3: Replace synonyms with canonical keywords."""
    words = text.split()
    result = []
    for word in words:
        replaced = False
        for canonical, variants in SYNONYMS.items():
            if word in variants:
                result.append(canonical)
                replaced = True
                break
        if not replaced:
            result.append(word)
    return " ".join(result)


# ─────────────────────────────────────────────────────────────────
# TOPIC 4 — TF-IDF RETRIEVAL
# ─────────────────────────────────────────────────────────────────
class TFIDFRetriever:
    def __init__(self):
        self.docs = {}      # topic -> full text (keywords + answer)
        self.idf = {}
        self.tf_idf_matrix = {}

    def build_index(self):
        """Build TF-IDF index from FAQ_DB."""
        for topic, data in FAQ_DB.items():
            doc_text = " ".join(data["keywords"]) + " " + data["answer"].lower()
            self.docs[topic] = doc_text

        all_terms = set()
        term_doc_count = Counter()
        doc_tf = {}

        for topic, text in self.docs.items():
            tokens = text.split()
            tf = Counter(tokens)
            total = len(tokens)
            doc_tf[topic] = {t: c / total for t, c in tf.items()}
            all_terms.update(tokens)
            for term in set(tokens):
                term_doc_count[term] += 1

        N = len(self.docs)
        self.idf = {
            term: math.log((N + 1) / (count + 1)) + 1
            for term, count in term_doc_count.items()
        }

        for topic in self.docs:
            self.tf_idf_matrix[topic] = {
                term: doc_tf[topic].get(term, 0) * self.idf.get(term, 0)
                for term in all_terms
            }

    def cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        common = set(vec1) & set(vec2)
        dot = sum(vec1[t] * vec2[t] for t in common)
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        return dot / (mag1 * mag2 + 1e-9)

    def query_vector(self, text: str) -> dict:
        tokens = text.split()
        tf = Counter(tokens)
        total = len(tokens) or 1
        return {
            term: (count / total) * self.idf.get(term, 0.1)
            for term, count in tf.items()
        }

    def retrieve(self, query: str, top_n: int = 1) -> list:
        """Return top_n matching FAQ topics with scores."""
        qvec = self.query_vector(query)
        scores = {
            topic: self.cosine_similarity(qvec, tvec)
            for topic, tvec in self.tf_idf_matrix.items()
        }
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_n]


# ─────────────────────────────────────────────────────────────────
# TOPIC 5 — INTENT CLASSIFIER
# ─────────────────────────────────────────────────────────────────
def classify_intent(text: str) -> str:
    """Detect the primary intent using regex patterns."""
    lower = text.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, lower):
                return intent
    return "unknown"


# ─────────────────────────────────────────────────────────────────
# TOPIC 6 — ENTITY EXTRACTOR
# ─────────────────────────────────────────────────────────────────
def extract_entities(text: str) -> dict:
    """Extract dates and course names from user query."""
    entities = {"dates": [], "courses": []}
    lower = text.lower()

    for pat in DATE_PATTERNS:
        matches = re.findall(pat, lower)
        entities["dates"].extend([m.strip() for m in matches if m.strip()])

    for pat in COURSE_PATTERNS:
        matches = re.findall(pat, lower)
        entities["courses"].extend([m.strip() for m in matches if m.strip()])

    entities["dates"] = list(set(entities["dates"]))
    entities["courses"] = list(set(entities["courses"]))
    return entities


# ─────────────────────────────────────────────────────────────────
# TOPIC 7 — CONTEXT MANAGER
# ─────────────────────────────────────────────────────────────────
class ContextManager:
    def __init__(self):
        self.history = []          # list of (user_msg, bot_reply, intent)
        self.last_intent = None
        self.last_topic = None
        self.last_entities = {}
        self.max_history = 5

    def update(self, user_msg: str, bot_reply: str, intent: str,
               topic: str, entities: dict):
        self.history.append({
            "user": user_msg,
            "bot": bot_reply,
            "intent": intent,
            "topic": topic,
            "entities": entities,
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
        })
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.last_intent = intent
        self.last_topic = topic
        self.last_entities = entities

    def is_follow_up(self, query: str) -> bool:
        """Detect if this is a follow-up to the previous turn."""
        follow_up_signals = [
            r"\b(more|else|also|another|what about|tell me more|explain|details|elaborate)\b",
            r"\b(and|additionally|further|besides)\b",
            r"^(it|that|this|they|those|these)\b",
            r"\b(when|where|how much|who|which one)\b",
        ]
        lower = query.lower().strip()
        for pat in follow_up_signals:
            if re.search(pat, lower):
                return True
        # Very short queries with no strong intent are likely follow-ups
        if len(lower.split()) <= 3 and self.last_topic:
            return True
        return False

    def get_context_hint(self) -> str:
        if self.last_topic and self.last_topic in FAQ_DB:
            return f"(Follow-up about '{self.last_topic}')"
        return ""


# ─────────────────────────────────────────────────────────────────
# TOPIC 8 — FALLBACK & HANDOVER
# ─────────────────────────────────────────────────────────────────
FALLBACK_THRESHOLD = 0.08   # TF-IDF similarity below this = fallback
HANDOVER_KEYWORDS = [
    "urgent", "emergency", "complaint", "grievance", "principal",
    "dean", "serious", "harassment", "issue", "problem", "not working",
    "broken", "wrong", "mistake", "error", "fraud", "scam",
]

def needs_handover(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in HANDOVER_KEYWORDS)

FALLBACK_RESPONSES = [
    "I'm not sure I understood that. Could you rephrase your question?",
    "Hmm, that's outside my current knowledge. Try asking about fees, exams, or admissions.",
    "I couldn't find a good match for your query. Would you like me to connect you to a human agent?",
]
_fallback_idx = 0

def get_fallback(consecutive_count: int = 0) -> str:
    global _fallback_idx
    if consecutive_count >= 2:
        return ("You've asked a few questions I couldn't answer. "
                "📞 Please contact the helpdesk: +91-22-12345678 or ✉ info@college.edu")
    msg = FALLBACK_RESPONSES[_fallback_idx % len(FALLBACK_RESPONSES)]
    _fallback_idx += 1
    return msg


# ─────────────────────────────────────────────────────────────────
# TOPIC 9 — MULTICHANNEL DEPLOYMENT MOCKUP
# ─────────────────────────────────────────────────────────────────
class Channel:
    """Simulates different deployment channels."""

    @staticmethod
    def format_cli(response: str, entities: dict, intent: str) -> str:
        sep = "─" * 60
        lines = [f"\n{sep}"]
        lines.append(f"  🤖 BOT  [{intent.upper()}]")
        lines.append(f"{sep}")
        for line in response.split(". "):
            if line.strip():
                lines.append(f"  {line.strip()}.")
        if entities["dates"] or entities["courses"]:
            lines.append(f"\n  📌 Detected Entities:")
            if entities["dates"]:
                lines.append(f"     Dates   : {', '.join(entities['dates'])}")
            if entities["courses"]:
                lines.append(f"     Courses : {', '.join(entities['courses'])}")
        lines.append(sep)
        return "\n".join(lines)

    @staticmethod
    def format_sms(response: str, **kwargs) -> str:
        """SMS: keep it short, no formatting."""
        clean = re.sub(r"[^\w\s.,!?₹@:/+-]", "", response)
        return f"[SMS] {clean[:160]}"   # SMS 160-char limit

    @staticmethod
    def format_email(response: str, intent: str, **kwargs) -> str:
        subject_map = {
            "fee_inquiry": "Re: Fee Enquiry",
            "exam_inquiry": "Re: Exam Schedule Enquiry",
            "admission": "Re: Admission Enquiry",
            "result_query": "Re: Result Enquiry",
        }
        subject = subject_map.get(intent, "Re: Student Enquiry")
        body = (f"[EMAIL]\nSubject : {subject}\n\nDear Student,\n\n"
                f"{response}\n\nWarm Regards,\nCollege Admin Bot")
        return body

    @staticmethod
    def format_whatsapp(response: str, **kwargs) -> str:
        return f"[WhatsApp] ✅ {response}"


CHANNEL_FORMATTERS = {
    "cli":       Channel.format_cli,
    "sms":       Channel.format_sms,
    "email":     Channel.format_email,
    "whatsapp":  Channel.format_whatsapp,
}


# ─────────────────────────────────────────────────────────────────
# TOPIC 10 — ANALYTICS ENGINE
# ─────────────────────────────────────────────────────────────────
class Analytics:
    def __init__(self, log_file="chat_analytics.json"):
        self.log_file = log_file
        self.session_start = datetime.datetime.now()
        self.total_queries = 0
        self.answered = 0
        self.unanswered = 0
        self.fallback_count = 0
        self.handover_count = 0
        self.intent_counter = Counter()
        self.topic_counter = Counter()
        self.unanswered_queries = []
        self.response_times = []
        self._load()

    def _load(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file) as f:
                    data = json.load(f)
                self.total_queries  = data.get("total_queries", 0)
                self.answered       = data.get("answered", 0)
                self.unanswered     = data.get("unanswered", 0)
                self.fallback_count = data.get("fallback_count", 0)
                self.handover_count = data.get("handover_count", 0)
                self.intent_counter = Counter(data.get("intent_counter", {}))
                self.topic_counter  = Counter(data.get("topic_counter", {}))
                self.unanswered_queries = data.get("unanswered_queries", [])
            except Exception:
                pass

    def save(self):
        data = {
            "total_queries":     self.total_queries,
            "answered":          self.answered,
            "unanswered":        self.unanswered,
            "fallback_count":    self.fallback_count,
            "handover_count":    self.handover_count,
            "intent_counter":    dict(self.intent_counter),
            "topic_counter":     dict(self.topic_counter),
            "unanswered_queries": self.unanswered_queries[-50:],
            "last_updated":      datetime.datetime.now().isoformat(),
        }
        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=2)

    def log_query(self, query: str, intent: str, topic: str,
                  was_answered: bool, was_fallback: bool,
                  was_handover: bool, response_ms: float):
        self.total_queries += 1
        self.intent_counter[intent] += 1
        if was_answered:
            self.answered += 1
            self.topic_counter[topic] += 1
        else:
            self.unanswered += 1
            self.unanswered_queries.append({
                "query": query,
                "time":  datetime.datetime.now().isoformat()
            })
        if was_fallback:
            self.fallback_count += 1
        if was_handover:
            self.handover_count += 1
        self.response_times.append(response_ms)
        self.save()

    def show_report(self):
        avg_ms = (sum(self.response_times) / len(self.response_times)
                  if self.response_times else 0)
        ans_rate = (self.answered / self.total_queries * 100
                    if self.total_queries else 0)

        print("\n" + "═" * 62)
        print("  📊  CHATBOT ANALYTICS REPORT")
        print("═" * 62)
        print(f"  Session Start    : {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Total Queries    : {self.total_queries}")
        print(f"  Answered         : {self.answered}  ({ans_rate:.1f}%)")
        print(f"  Unanswered       : {self.unanswered}")
        print(f"  Fallbacks        : {self.fallback_count}")
        print(f"  Handovers        : {self.handover_count}")
        print(f"  Avg Response     : {avg_ms:.1f} ms")

        if self.intent_counter:
            print("\n  Top Intents:")
            for intent, count in self.intent_counter.most_common(5):
                bar = "█" * min(count, 20)
                print(f"    {intent:<20} {bar} ({count})")

        if self.topic_counter:
            print("\n  Top FAQ Topics:")
            for topic, count in self.topic_counter.most_common(5):
                bar = "█" * min(count, 20)
                print(f"    {topic:<20} {bar} ({count})")

        if self.unanswered_queries:
            print("\n  Recent Unanswered Queries (for improvement):")
            for item in self.unanswered_queries[-5:]:
                print(f"    → \"{item['query']}\"")

        print("═" * 62)


# ─────────────────────────────────────────────────────────────────
# MAIN CHATBOT ENGINE
# ─────────────────────────────────────────────────────────────────
class StudentFAQChatbot:
    def __init__(self, channel: str = "cli"):
        self.channel = channel.lower()
        self.retriever = TFIDFRetriever()
        self.retriever.build_index()
        self.context = ContextManager()
        self.analytics = Analytics()
        self.consecutive_fallbacks = 0
        print(self._banner())

    def _banner(self) -> str:
        return (
            "\n" + "═" * 62 + "\n"
            "  🎓  COLLEGE STUDENT FAQ CHATBOT\n"
            "  Channel : " + self.channel.upper() + "\n"
            "  Topics  : All 10 NLP & Chatbot Topics Implemented\n"
            "  Commands: 'stats' = analytics | 'history' = chat log\n"
            "            'switch <channel>' | 'help' | 'quit'\n"
            + "═" * 62
        )

    # ── Core Response Logic ─────────────────────────────────────
    def get_response(self, user_input: str) -> str:
        t_start = datetime.datetime.now()

        # — T2: Preprocess
        processed = preprocess(user_input)
        # — T3: Synonym expansion
        expanded = apply_synonyms(processed)
        # — T5: Intent
        intent = classify_intent(user_input)
        # — T6: Entities
        entities = extract_entities(user_input)

        # — T7: Context / follow-up
        if self.context.is_follow_up(user_input) and self.context.last_topic and self.context.last_topic in FAQ_DB:
            topic = self.context.last_topic
            answer = FAQ_DB[topic]["answer"]
            answer += f"\n  💡 (You asked a follow-up — I continued from '{topic}')"
            self._finish(user_input, answer, intent, topic,
                         entities, t_start, answered=True)
            return self._format(answer, entities, intent)

        # — T8: Escalation check
        if needs_handover(user_input):
            self.analytics.handover_count += 1
            answer = ("⚠️  This seems like an urgent matter. "
                      "Please contact the admin office directly:\n"
                      "  📞 +91-22-12345678 | ✉ info@college.edu\n"
                      "  Or visit Room 101, Admin Block. (Mon–Fri 9AM–5PM)")
            self._finish(user_input, answer, intent, "handover",
                         entities, t_start, answered=True, handover=True)
            return self._format(answer, entities, intent)

        # — T1 + T4: TF-IDF Retrieval
        results = self.retriever.retrieve(expanded, top_n=2)
        best_topic, best_score = results[0]

        if best_score >= FALLBACK_THRESHOLD and best_topic in FAQ_DB:
            answer = FAQ_DB[best_topic]["answer"]
            # Personalise with extracted entities
            if entities["courses"]:
                answer += f"\n  📚 Course detected: {', '.join(entities['courses'])}"
            if entities["dates"]:
                answer += f"\n  📅 Date mentioned : {', '.join(entities['dates'])}"
            self.consecutive_fallbacks = 0
            self._finish(user_input, answer, intent, best_topic,
                         entities, t_start, answered=True)
            return self._format(answer, entities, intent)

        # — T8: Fallback
        self.consecutive_fallbacks += 1
        fallback_reply = get_fallback(self.consecutive_fallbacks)
        self._finish(user_input, fallback_reply, "unknown", "fallback",
                     entities, t_start, answered=False, fallback=True)
        return self._format(fallback_reply, entities, "unknown")

    def _finish(self, user_input, answer, intent, topic,
                entities, t_start, answered=True,
                fallback=False, handover=False):
        ms = (datetime.datetime.now() - t_start).total_seconds() * 1000
        self.context.update(user_input, answer, intent, topic, entities)
        self.analytics.log_query(
            user_input, intent, topic,
            answered, fallback, handover, ms
        )

    def _format(self, text: str, entities: dict, intent: str) -> str:
        formatter = CHANNEL_FORMATTERS.get(self.channel, Channel.format_cli)
        return formatter(text, entities=entities, intent=intent)

    # ── Chat History ────────────────────────────────────────────
    def show_history(self):
        print("\n" + "─" * 62)
        print("  📜  CONVERSATION HISTORY")
        print("─" * 62)
        if not self.context.history:
            print("  (No history yet)")
        for i, turn in enumerate(self.context.history, 1):
            print(f"  [{turn['time']}] Turn {i}")
            print(f"  You  : {turn['user']}")
            print(f"  Bot  : {turn['bot'][:80]}...")
            print(f"  Intent: {turn['intent']} | Topic: {turn['topic']}")
            print()
        print("─" * 62)

    # ── REPL ────────────────────────────────────────────────────
    def run(self):
        print("\n  Type your question (or 'help' for options)\n")
        while True:
            try:
                user_input = input("  You > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n  Goodbye!")
                break

            if not user_input:
                continue

            # — Built-in commands
            lower = user_input.lower()

            if lower in ("quit", "exit", "q"):
                print("\n  👋 Thank you for using the College FAQ Bot. Goodbye!")
                self.analytics.show_report()
                break

            elif lower == "stats":
                self.analytics.show_report()

            elif lower == "history":
                self.show_history()

            elif lower == "help":
                print("\n  Available topics: admission, fee, exam, result, library,")
                print("  hostel, holiday, course, attendance, placement, contact")
                print("  Commands: stats | history | switch <channel> | quit\n")

            elif lower.startswith("switch "):
                new_ch = lower.split("switch ", 1)[1].strip()
                if new_ch in CHANNEL_FORMATTERS:
                    self.channel = new_ch
                    print(f"\n  ✅ Channel switched to: {new_ch.upper()}\n")
                else:
                    print(f"\n  ❌ Unknown channel. Options: {', '.join(CHANNEL_FORMATTERS)}\n")

            else:
                response = self.get_response(user_input)
                print(response)


# ─────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("  Select channel: cli | sms | email | whatsapp  (default: cli)")
    try:
        ch = input("  Channel > ").strip().lower() or "cli"
    except (EOFError, KeyboardInterrupt):
        ch = "cli"
    if ch not in CHANNEL_FORMATTERS:
        ch = "cli"
    bot = StudentFAQChatbot(channel=ch)
    bot.run()
