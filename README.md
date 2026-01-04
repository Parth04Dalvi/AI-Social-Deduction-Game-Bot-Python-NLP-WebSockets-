# ImposterAI: Multi-Agent Social Deduction Engine

**ImposterAI** is a real-time, interactive social deduction game that challenges human players to identify a hidden AI "imposter" in a live chat environment. [cite_start]This project integrates high-speed **WebSockets** with **Generative AI** to create a deceptive, context-aware agent that mimics human conversational patterns[cite: 31, 44, 46].

---

## 🚀 Overview
[cite_start]Building on my experience with **NLP-powered parsers** and **real-time audio interaction**, this project explores the boundary between human and machine communication[cite: 44, 48]. The system manages concurrent user sessions while orchestrating a "blind" AI participant that must defend itself against human suspicion in real-time.

### Key Technical Pillars:
* [cite_start]**Stateful Real-Time Communication:** Uses **FastAPI** and **WebSockets** to handle bi-directional message broadcasting with sub-50ms latency[cite: 31, 48].
* [cite_start]**LLM Orchestration:** Leverages the **Gemini API** with advanced prompt engineering to simulate human-like behavior, slang, and strategic deflection[cite: 46].
* [cite_start]**Sentiment-Driven Logic:** Implements a basic sentiment analysis layer to help the AI detect when it is being targeted or suspected[cite: 48, 49].
* [cite_start]**Cloud-Native Design:** Fully containerized using **Docker**, ensuring seamless deployment across environments[cite: 34].

---

## 🛠️ Tech Stack
* [cite_start]**Backend:** Python, FastAPI, WebSockets[cite: 31, 48].
* [cite_start]**Frontend:** Next.js, React, Tailwind CSS[cite: 31, 40].
* [cite_start]**AI/ML:** Gemini API, NLP (Natural Language Processing)[cite: 31, 46, 48].
* [cite_start]**Data & Cache:** Redis (Message Queuing), MongoDB (Game History)[cite: 31, 40].
* [cite_start]**DevOps:** Docker, CI/CD Pipelines[cite: 31, 34, 43].

---

## 🧠 System Architecture
1. **The Gateway:** A FastAPI server acts as the central hub, managing WebSocket connections for up to 10 players per room.
2. **The Imposter:** A background worker monitors the chat stream. [cite_start]When triggered by a "turn" or "suspicion keyword," it queries the **Gemini API** with the last 10 messages as context to generate a rebuttal[cite: 46, 48].
3. [cite_start]**The Defense Layer:** Inspired by my previous work on **bias-aware matching**, the AI uses a filtering layer to ensure responses remain within game boundaries while maintaining a high level of deception[cite: 49].

---

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Parth04Dalvi/ImposterAI.git](https://github.com/Parth04Dalvi/ImposterAI.git)
   cd ImposterAI
