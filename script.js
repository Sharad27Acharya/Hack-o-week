class SITNAGPURChatbot {
    constructor() {
        this.messagesArea = document.getElementById('messagesArea');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.newChatButton = document.querySelector('.new-chat-btn');
        this.searchInput = document.querySelector('.search-chats input');
        this.chatList = document.querySelector('.chat-list');
        this.chatListItems = Array.from(document.querySelectorAll('.chat-list-item'));

        this.stopwords = new Set([
            'i', 'me', 'my', 'myself', 'we', 'our', 'you', 'your', 'he', 'she',
            'it', 'they', 'what', 'which', 'who', 'this', 'that', 'am', 'is',
            'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'shall', 'can', 'a', 'an', 'the', 'and', 'but',
            'or', 'so', 'if', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'then', 'than', 'also', 'just', 'no', 'not', 'only', 'same',
            'please', 'tell', 'know', 'want', 'need', 'get', 'got', 'like', 'how',
            'when', 'where', 'which', 'give', 'show'
        ]);

        this.synonyms = {
            admissions: ['admission', 'apply', 'application', 'enroll', 'enrollment', 'registration', 'join'],
            courses: ['course', 'courses', 'program', 'programme', 'branch', 'degree', 'curriculum', 'specialization'],
            fees: ['fee', 'fees', 'tuition', 'cost', 'payment', 'expense', 'amount'],
            scholarships: ['scholarship', 'waiver', 'concession', 'financial aid', 'aid'],
            exams: ['exam', 'exams', 'test', 'assessment', 'midsem', 'mid-term', 'endsem', 'hall ticket'],
            timetable: ['timetable', 'schedule', 'calendar', 'routine', 'timings'],
            placement: ['placement', 'placements', 'job', 'recruitment', 'package', 'career', 'internship'],
            hostel: ['hostel', 'accommodation', 'dorm', 'dormitory', 'room', 'mess'],
            facilities: ['facility', 'facilities', 'library', 'sports', 'lab', 'wifi', 'campus'],
            contact: ['contact', 'phone', 'email', 'address', 'reach', 'office', 'helpline'],
            attendance: ['attendance', 'absent', 'present', 'leave', 'proxy'],
            result: ['result', 'results', 'marks', 'grade', 'cgpa', 'gpa', 'score'],
            greeting: ['hi', 'hello', 'hey', 'namaste'],
            farewell: ['bye', 'goodbye', 'thanks', 'thankyou', 'thank']
        };

        this.intentPatterns = {
            greeting: [/\b(hi|hello|hey|namaste)\b/i],
            farewell: [/\b(bye|goodbye|thanks|thank you|see you)\b/i],
            admissions: [/\b(admission|apply|application|enroll|join)\b/i],
            courses: [/\b(course|program|branch|degree|curriculum)\b/i],
            fees: [/\b(fee|fees|tuition|cost|payment|expense)\b/i],
            scholarships: [/\b(scholarship|waiver|concession|financial aid)\b/i],
            exams: [/\b(exam|test|assessment|hall ticket|paper)\b/i],
            timetable: [/\b(timetable|schedule|calendar|routine|timings)\b/i],
            hostel: [/\b(hostel|accommodation|dorm|room|mess)\b/i],
            placement: [/\b(placement|job|career|package|internship|recruit)\b/i],
            facilities: [/\b(facility|facilities|library|sports|lab|campus|wifi)\b/i],
            contact: [/\b(contact|phone|email|address|office|helpline)\b/i],
            attendance: [/\b(attendance|absent|present|leave|proxy)\b/i],
            result: [/\b(result|marks|grade|cgpa|gpa|score)\b/i]
        };

        this.datePatterns = [
            /\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b/gi,
            /\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b/gi,
            /\b(?:today|tomorrow|next week|next month|monday|tuesday|wednesday|thursday|friday|saturday)\b/gi,
            /\b\d{4}\b/g
        ];

        this.coursePatterns = [
            /\b(?:b\.?tech|m\.?tech|mba|phd|ai\s*&?\s*ml|data science|computer science|mechanical|civil|electrical|electronics)\b/gi,
            /\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth)\s+(?:year|semester|sem)\b/gi,
            /\b(?:[1-8](?:st|nd|rd|th)\s+(?:year|semester|sem))\b/gi
        ];

        this.handoverKeywords = [
            'urgent', 'emergency', 'complaint', 'grievance', 'harassment',
            'principal', 'dean', 'fraud', 'serious issue', 'not working'
        ];

        this.fallbackResponses = [
            "I'm not fully sure about that yet. Could you rephrase it or ask about admissions, fees, exams, hostel, placements, or contact details?",
            "That looks outside my strongest FAQ topics. I can reliably help with admissions, timetable, scholarships, fees, exams, hostel, and placements.",
            "I couldn't find a confident answer. If this is urgent, I can point you to the right office or helpdesk."
        ];

        this.fallbackIndex = 0;
        this.consecutiveFallbacks = 0;
        this.context = {
            lastIntent: null,
            lastTopic: null,
            lastEntities: { dates: [], courses: [] },
            history: []
        };
        this.analytics = this.loadAnalytics();

        this.knowledgeBase = {
            admissions: {
                title: 'Admissions 2026',
                keywords: ['admissions', 'application', 'eligibility', 'documents', 'deadline', 'entrance'],
                response: `**Admissions Open for 2026-27 Academic Year** 🎓

**Eligibility Criteria:**
• B.Tech: 60% in 10+2 with PCM
• M.Tech: 60% in B.Tech + GATE score
• MBA: 60% in graduation + CAT/MAT score
• PhD: Master's degree with 60% + entrance test

**Important Dates:**
• Application Start: January 15, 2026
• Last Date: March 31, 2026
• Entrance Test: April 15, 2026
• Result Declaration: May 10, 2026

**Required Documents:**
• 10th & 12th mark sheets
• Entrance score card
• ID proof
• Passport-size photographs

Would you like eligibility, documents, or deadlines in a shorter summary?`
            },
            courses: {
                title: 'Courses Offered',
                keywords: ['courses', 'programs', 'btech', 'mtech', 'mba', 'phd', 'specialization'],
                response: `**Academic Programs at SITNAGPUR** 📚

**Undergraduate Programs:**
• Computer Science & Engineering
• Electronics & Communication
• Mechanical Engineering
• Civil Engineering
• Electrical Engineering
• AI & ML
• Data Science

**Postgraduate Programs:**
• M.Tech in AI & ML
• M.Tech in VLSI
• MBA in Technology Management

**Research Programs:**
• PhD in Engineering, Technology, and Applied Sciences

Tell me a branch name if you want course-specific details.`
            },
            fees: {
                title: 'Fee Structure',
                keywords: ['fees', 'tuition', 'payment', 'cost', 'expense', 'money'],
                response: `**Fee Structure for 2026-27** 💰

**Tuition Fees Per Year:**
• B.Tech: ₹1,25,000
• M.Tech: ₹1,00,000
• MBA: ₹1,50,000
• PhD: ₹75,000

**Additional Fees:**
• Hostel: ₹60,000 - ₹85,000/year
• Mess: ₹36,000/year
• Library: ₹5,000/year
• Laboratory: ₹8,000/year

Need a full estimate including hostel and mess?`
            },
            scholarships: {
                title: 'Scholarships',
                keywords: ['scholarship', 'waiver', 'concession', 'merit', 'financial aid'],
                response: `**Scholarship Options** 🏅

• Merit scholarship: up to 100% tuition waiver
• Need-based support: up to 50% fee concession
• Sports quota: up to 75% concession
• Girls scholarship: 10% additional discount
• SC/ST scholarships as per government norms

Scholarship applications are usually reviewed after admission confirmation and document verification.`
            },
            exams: {
                title: 'Exam Information',
                keywords: ['exam', 'hall ticket', 'mid sem', 'end sem', 'paper', 'assessment'],
                response: `**Examination Details** 📝

• Mid-sem exams: March 10-20, 2026
• Final exams: May 5-25, 2026
• Practicals/Viva: April 15-30, 2026
• Supplementary exams: July 10-20, 2026
• Hall tickets are usually released 7 days before exams
• Minimum 75% attendance is required

If you want the full exam routine, ask for the timetable.`
            },
            timetable: {
                title: 'Timetable and Schedule',
                keywords: ['timetable', 'schedule', 'calendar', 'routine', 'timings', 'semester'],
                response: `**Academic Timetable Snapshot** 📅

• Office hours: Mon-Fri, 9:00 AM - 5:00 PM
• Saturday: 9:00 AM - 1:00 PM
• Mid-sem window: March 10-20, 2026
• Final exam window: May 5-25, 2026
• Results are typically published within 15 days after final exams

If you mention your semester or course, I can narrow the answer to that context.`
            },
            hostel: {
                title: 'Hostel and Accommodation',
                keywords: ['hostel', 'accommodation', 'mess', 'room', 'dormitory'],
                response: `**Hostel Facilities** 🏠

• Separate hostels for boys and girls
• Wi-Fi enabled campus
• 24/7 power backup
• Mess facility available
• Common rooms and gym access
• Hostel fee range: ₹60,000 - ₹85,000/year

Hostel seats are limited, so students are advised to apply early after admission confirmation.`
            },
            placement: {
                title: 'Placements',
                keywords: ['placements', 'recruiters', 'internships', 'career', 'package'],
                response: `**Placement Highlights** 💼

• Overall placement rate: 92%
• Average package: ₹8.5 LPA
• Highest package: ₹32 LPA
• Top recruiters: Microsoft, Google, Amazon, Infosys, TCS, L&T
• Internship participation: 85%

Ask for placement stats if you want recruiter or package details in one line.`
            },
            facilities: {
                title: 'Campus Facilities',
                keywords: ['facilities', 'library', 'sports', 'lab', 'wifi', 'medical'],
                response: `**Campus Facilities** 🏛️

• Smart classrooms and advanced labs
• Central library with 50,000+ books
• Research and innovation hub
• Sports complex and gym
• Medical center with ambulance
• Cafeteria, ATM, transport, and 24/7 security

You can ask specifically about the library, hostel, sports, or labs.`
            },
            contact: {
                title: 'Contact Information',
                keywords: ['contact', 'phone', 'email', 'office', 'address', 'helpline'],
                response: `**SITNAGPUR Contact Details** 📞

• Main office: +91 712 280 1234
• Admissions office: +91 712 280 5678
• Email: info@sitnagpur.edu.in
• Admissions email: admissions@sitnagpur.edu.in
• Address: SIT Nagpur, Maharashtra - 440001
• Hours: Mon-Fri, 9 AM - 5 PM

If this is urgent, I can also direct you to the admissions or academic office.`
            },
            attendance: {
                title: 'Attendance Rules',
                keywords: ['attendance', 'leave', 'absent', 'proxy', 'minimum attendance'],
                response: `**Attendance Policy** ✅

• Minimum 75% attendance is mandatory
• Medical leave requires supporting documents
• Shortage of attendance may affect exam eligibility

If you want exam eligibility, I can connect this with the exam rules too.`
            },
            result: {
                title: 'Results',
                keywords: ['result', 'results', 'marks', 'cgpa', 'gpa', 'score'],
                response: `**Result Information** 📊

• Results are usually declared within 15 days after final exams
• Re-evaluation requests are typically accepted for 7 days after result publication
• Students should check the official student portal or academic office notices

If you tell me which semester, I can answer in that context.`
            },
            greeting: {
                title: 'Greeting',
                keywords: ['hi', 'hello', 'hey', 'namaste'],
                response: `Hello! 👋 I’m the SITNAGPUR student FAQ assistant.

I can help with:
• Admissions
• Courses
• Fees and scholarships
• Exam timetable
• Hostel and facilities
• Placements
• Contact details`
            },
            farewell: {
                title: 'Farewell',
                keywords: ['bye', 'goodbye', 'thanks', 'thank'],
                response: `You're welcome! If you need anything else about SITNAGPUR, just ask.`
            }
        };

        this.topicByIntent = {
            admissions: 'admissions',
            courses: 'courses',
            fees: 'fees',
            scholarships: 'scholarships',
            exams: 'exams',
            timetable: 'timetable',
            hostel: 'hostel',
            placement: 'placement',
            facilities: 'facilities',
            contact: 'contact',
            attendance: 'attendance',
            result: 'result',
            greeting: 'greeting',
            farewell: 'farewell'
        };

        this.tfidfIndex = this.buildTfIdfIndex();
        this.init();
    }

    init() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                this.sendMessage();
            }
        });

        document.querySelectorAll('.quick-action-btn').forEach((button) => {
            button.addEventListener('click', (event) => {
                const query = event.currentTarget.dataset.query;
                const label = event.currentTarget.textContent.trim();
                this.addMessage(label, 'user');
                this.respondToQuery(query, true);
            });
        });

        this.chatListItems.forEach((item) => {
            item.addEventListener('click', () => this.setActiveChat(item));
        });

        if (this.newChatButton) {
            this.newChatButton.addEventListener('click', () => this.resetConversation());
        }

        if (this.searchInput) {
            this.searchInput.addEventListener('input', (event) => {
                this.filterChatList(event.target.value);
            });
        }

        this.updateSidebarPreview('How can I help you today?', 'Just now');
    }

    sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) {
            return;
        }

        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.respondToQuery(message);
    }

    respondToQuery(message, isQuickAction = false) {
        this.showTypingIndicator();

        window.setTimeout(() => {
            this.hideTypingIndicator();
            const result = this.getResponse(message, isQuickAction);
            this.addMessage(result.reply, 'bot');
            this.updateSidebarPreview(message, 'Just now');
        }, isQuickAction ? 400 : 900);
    }

    getResponse(rawMessage, isQuickAction = false) {
        const startedAt = performance.now();
        const entities = this.extractEntities(rawMessage);
        const processed = this.preprocess(rawMessage);
        const expanded = this.applySynonyms(processed);
        const intent = this.classifyIntent(rawMessage);
        const intentTopic = this.topicByIntent[intent];

        let topic = intentTopic;
        let reply = '';
        let wasAnswered = true;
        let wasFallback = false;
        let wasHandover = false;

        if (this.needsHandover(rawMessage)) {
            topic = 'contact';
            wasHandover = true;
            reply = `**Escalation Recommended** ⚠️

This looks like an urgent or sensitive issue. Please contact the institute directly:
• Main office: +91 712 280 1234
• Admissions office: +91 712 280 5678
• Email: info@sitnagpur.edu.in

You can also visit the admin office during working hours: Mon-Fri, 9 AM - 5 PM.`;
        } else if (this.isFollowUp(rawMessage) && this.context.lastTopic && !intentTopic) {
            topic = this.context.lastTopic;
            reply = `${this.knowledgeBase[topic].response}

**Follow-up Context Used:** I continued the answer from your previous question about **${this.knowledgeBase[topic].title}**.`;
        } else if (intentTopic && this.knowledgeBase[intentTopic]) {
            topic = intentTopic;
            reply = this.knowledgeBase[intentTopic].response;
        } else {
            const retrieval = this.retrieveTopic(expanded);
            if (retrieval.score >= 0.14) {
                topic = retrieval.topic;
                reply = this.knowledgeBase[topic].response;
            } else {
                wasAnswered = false;
                wasFallback = true;
                topic = 'fallback';
                this.consecutiveFallbacks += 1;
                reply = this.getFallbackReply();
            }
        }

        if (wasAnswered) {
            this.consecutiveFallbacks = 0;
            reply = this.enrichReply(reply, entities, topic, rawMessage);
        }

        this.updateContext(rawMessage, reply, intent, topic, entities);
        this.logAnalytics(rawMessage, intent, topic, wasAnswered, wasFallback, wasHandover, performance.now() - startedAt);

        return { reply, topic };
    }

    preprocess(text) {
        const normalized = text
            .toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();

        const filtered = normalized
            .split(' ')
            .filter((token) => token && !this.stopwords.has(token) && token.length > 1);

        return filtered.join(' ') || normalized;
    }

    applySynonyms(text) {
        return text
            .split(' ')
            .map((word) => {
                const canonical = Object.entries(this.synonyms).find(([, variants]) => variants.includes(word));
                return canonical ? canonical[0] : word;
            })
            .join(' ');
    }

    classifyIntent(text) {
        for (const [intent, patterns] of Object.entries(this.intentPatterns)) {
            if (patterns.some((pattern) => pattern.test(text))) {
                return intent;
            }
        }
        return 'unknown';
    }

    extractEntities(text) {
        const entities = { dates: [], courses: [] };

        this.datePatterns.forEach((pattern) => {
            const matches = text.match(pattern) || [];
            matches.forEach((match) => entities.dates.push(match.trim()));
        });

        this.coursePatterns.forEach((pattern) => {
            const matches = text.match(pattern) || [];
            matches.forEach((match) => entities.courses.push(match.trim()));
        });

        entities.dates = [...new Set(entities.dates)];
        entities.courses = [...new Set(entities.courses)];
        return entities;
    }

    buildTfIdfIndex() {
        const docs = {};
        const documentFrequency = new Map();
        const tfidf = {};
        const allTerms = new Set();

        Object.entries(this.knowledgeBase).forEach(([topic, data]) => {
            const combinedText = `${data.keywords.join(' ')} ${data.response.toLowerCase().replace(/[^\w\s]/g, ' ')}`;
            const tokens = combinedText.split(/\s+/).filter(Boolean);
            docs[topic] = tokens;
            const uniqueTerms = new Set(tokens);

            uniqueTerms.forEach((term) => {
                documentFrequency.set(term, (documentFrequency.get(term) || 0) + 1);
                allTerms.add(term);
            });
        });

        const totalDocs = Object.keys(docs).length;
        Object.entries(docs).forEach(([topic, tokens]) => {
            const termCounts = {};
            tokens.forEach((token) => {
                termCounts[token] = (termCounts[token] || 0) + 1;
            });

            tfidf[topic] = {};
            Array.from(allTerms).forEach((term) => {
                const tf = (termCounts[term] || 0) / tokens.length;
                const idf = Math.log((totalDocs + 1) / ((documentFrequency.get(term) || 0) + 1)) + 1;
                tfidf[topic][term] = tf * idf;
            });
        });

        return { tfidf, documentFrequency, totalDocs };
    }

    retrieveTopic(query) {
        const tokens = query.split(/\s+/).filter(Boolean);
        const counts = {};
        tokens.forEach((token) => {
            counts[token] = (counts[token] || 0) + 1;
        });

        const queryVector = {};
        Object.keys(counts).forEach((term) => {
            const tf = counts[term] / tokens.length;
            const idf = Math.log((this.tfidfIndex.totalDocs + 1) / ((this.tfidfIndex.documentFrequency.get(term) || 0) + 1)) + 1;
            queryVector[term] = tf * idf;
        });

        let bestTopic = 'contact';
        let bestScore = 0;

        Object.entries(this.tfidfIndex.tfidf).forEach(([topic, vector]) => {
            const score = this.cosineSimilarity(queryVector, vector);
            if (score > bestScore) {
                bestTopic = topic;
                bestScore = score;
            }
        });

        return { topic: bestTopic, score: bestScore };
    }

    cosineSimilarity(vectorA, vectorB) {
        const keys = new Set([...Object.keys(vectorA), ...Object.keys(vectorB)]);
        let dot = 0;
        let magnitudeA = 0;
        let magnitudeB = 0;

        keys.forEach((key) => {
            const a = vectorA[key] || 0;
            const b = vectorB[key] || 0;
            dot += a * b;
            magnitudeA += a * a;
            magnitudeB += b * b;
        });

        if (!magnitudeA || !magnitudeB) {
            return 0;
        }

        return dot / (Math.sqrt(magnitudeA) * Math.sqrt(magnitudeB));
    }

    isFollowUp(message) {
        const followUpPatterns = [
            /\b(more|else|also|another|details|explain|elaborate)\b/i,
            /\b(what about|how about|and for)\b/i,
            /^(it|that|this|they|those|these)\b/i
        ];

        const words = message.trim().split(/\s+/);
        return followUpPatterns.some((pattern) => pattern.test(message)) || (words.length <= 3 && Boolean(this.context.lastTopic));
    }

    needsHandover(message) {
        const lower = message.toLowerCase();
        return this.handoverKeywords.some((keyword) => lower.includes(keyword));
    }

    getFallbackReply() {
        if (this.consecutiveFallbacks >= 2) {
            return `I may not be the best source for this specific query yet.

Please contact the helpdesk directly:
• Phone: +91 712 280 1234
• Email: info@sitnagpur.edu.in

Or ask me about admissions, fees, scholarships, exams, hostel, placements, or contact details.`;
        }

        const reply = this.fallbackResponses[this.fallbackIndex % this.fallbackResponses.length];
        this.fallbackIndex += 1;
        return reply;
    }

    enrichReply(reply, entities, topic, rawMessage) {
        const additions = [];

        if (entities.courses.length) {
            additions.push(`**Detected Course Context:** ${entities.courses.join(', ')}`);
        }

        if (entities.dates.length) {
            additions.push(`**Detected Date Context:** ${entities.dates.join(', ')}`);
        }

        if (topic === 'timetable' && !entities.courses.length && /\bsemester|sem|year\b/i.test(rawMessage)) {
            additions.push('**Tip:** mention your course or semester for a more specific timetable response.');
        }

        return additions.length ? `${reply}\n\n${additions.join('\n')}` : reply;
    }

    updateContext(userMessage, botReply, intent, topic, entities) {
        this.context.lastIntent = intent;
        this.context.lastTopic = topic !== 'fallback' ? topic : this.context.lastTopic;
        this.context.lastEntities = entities;
        this.context.history.push({
            user: userMessage,
            bot: botReply,
            intent,
            topic,
            time: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
        });

        if (this.context.history.length > 8) {
            this.context.history.shift();
        }
    }

    loadAnalytics() {
        try {
            const saved = JSON.parse(localStorage.getItem('sitnagpur-chatbot-analytics'));
            return saved || {
                totalQueries: 0,
                answered: 0,
                fallbackCount: 0,
                handoverCount: 0,
                popularTopics: {}
            };
        } catch {
            return {
                totalQueries: 0,
                answered: 0,
                fallbackCount: 0,
                handoverCount: 0,
                popularTopics: {}
            };
        }
    }

    logAnalytics(query, intent, topic, answered, fallback, handover, responseMs) {
        this.analytics.totalQueries += 1;
        if (answered) {
            this.analytics.answered += 1;
        }
        if (fallback) {
            this.analytics.fallbackCount += 1;
        }
        if (handover) {
            this.analytics.handoverCount += 1;
        }
        this.analytics.popularTopics[topic] = (this.analytics.popularTopics[topic] || 0) + 1;
        this.analytics.lastIntent = intent;
        this.analytics.lastResponseMs = Math.round(responseMs);
        this.analytics.lastQuery = query;

        localStorage.setItem('sitnagpur-chatbot-analytics', JSON.stringify(this.analytics));
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        messageDiv.appendChild(avatarDiv);

        const contentWrapper = document.createElement('div');
        contentWrapper.className = 'message-content-wrapper';

        const senderDiv = document.createElement('div');
        senderDiv.className = 'message-sender';
        senderDiv.textContent = sender === 'bot' ? 'SITNAGPUR Assistant' : 'You';
        contentWrapper.appendChild(senderDiv);

        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';

        const formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');

        bubbleDiv.innerHTML = formattedText;
        contentWrapper.appendChild(bubbleDiv);

        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = this.getCurrentTime();
        contentWrapper.appendChild(timeSpan);

        messageDiv.appendChild(contentWrapper);
        this.messagesArea.appendChild(messageDiv);
        this.scrollToBottom();
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    scrollToBottom() {
        this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
    }

    setActiveChat(activeItem) {
        this.chatListItems.forEach((item) => item.classList.remove('active'));
        activeItem.classList.add('active');
    }

    updateSidebarPreview(message, time) {
        const assistantItem = this.chatListItems[0];
        if (!assistantItem) {
            return;
        }

        const preview = assistantItem.querySelector('.chat-details p');
        const timestamp = assistantItem.querySelector('.chat-time');
        const badge = assistantItem.querySelector('.unread-badge');

        if (preview) {
            preview.textContent = message;
        }
        if (timestamp) {
            timestamp.textContent = time;
        }
        if (badge) {
            badge.textContent = String(Math.min(this.analytics.totalQueries + 1, 9));
        }
    }

    filterChatList(term) {
        const query = term.toLowerCase().trim();
        this.chatListItems.forEach((item) => {
            const text = item.textContent.toLowerCase();
            item.style.display = !query || text.includes(query) ? '' : 'none';
        });
    }

    resetConversation() {
        const existingMessages = Array.from(this.messagesArea.querySelectorAll('.message'));
        existingMessages.forEach((message) => message.remove());

        this.context = {
            lastIntent: null,
            lastTopic: null,
            lastEntities: { dates: [], courses: [] },
            history: []
        };
        this.consecutiveFallbacks = 0;
        this.addMessage(
            `👋 Welcome back to the SITNAGPUR student chatbot.

You can test:
• preprocessing and synonym matching
• timetable, hostel, scholarship, and fee FAQs
• follow-up questions like "What about hostel?" or "For third year?"`,
            'bot'
        );
        this.updateSidebarPreview('New conversation started', 'Just now');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SITNAGPURChatbot();
});
