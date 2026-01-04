# ImposterAI: Multi-Agent Social Deduction Engine

**ImposterAI** is a real-time, interactive social deduction game that challenges human players to identify a hidden AI "imposter" in a live chat environment. This project integrates high-speed **WebSockets** with **Generative AI** to create a deceptive, context-aware agent that mimics human conversational patterns.

---

## 🚀 Overview
Building on my experience with NLP-powered parsers and real-time interactive systems, this project explores the boundary between human and machine communication. The system manages concurrent user sessions while orchestrating an AI participant that must defend itself against human suspicion by analyzing conversation history and adapting its tone.

### Key Technical Pillars:
* **Stateful Real-Time Communication:** Uses **FastAPI** and **WebSockets** to handle bi-directional message broadcasting with sub-50ms latency.
* **LLM Orchestration:** Leverages the **Gemini API** with advanced prompt engineering to simulate human-like behavior, slang, and strategic deflection.
* **Sentiment-Driven Logic:** Implements a sentiment analysis layer to help the AI detect when it is being targeted or suspected by other players.
* **Cloud-Native Design:** Fully containerized using **Docker**, ensuring seamless deployment across environments.

---

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, WebSockets
* **Frontend:** Next.js, React, Tailwind CSS
* **AI/ML:** Gemini API, NLP (Natural Language Processing)
* **Data & Cache:** Redis (Message Queuing), MongoDB (Game History)
* **DevOps:** Docker, CI/CD Pipelines

---

## 🧠 System Architecture



1. **The Gateway:** A FastAPI server acts as the central hub, managing WebSocket connections for multiple players per room.
2. **The Imposter:** A background worker monitors the chat stream. When triggered, it queries the **Gemini API** using the conversation history as context to generate a rebuttal.
3. **The Defense Layer:** Incorporates a filtering layer to ensure responses remain within game boundaries while maintaining a high level of strategic deception.

---

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Parth04Dalvi/ImposterAI.git](https://github.com/Parth04Dalvi/ImposterAI.git)
   cd ImposterAI

   Setup Environment Variables (.env):

Code snippet

GEMINI_API_KEY=your_api_key_here
MONGO_URI=your_mongodb_connection_string
Launch with Docker Compose:

Bash

docker-compose up --build
📈 Future Roadmap
Audio Integration: Implementing Voice-to-Text feedback loops to allow verbal interaction with the imposter.

Behavioral Analytics: Creating a dashboard to track "Success Rates" of different AI personalities against human players.

Zero-Trust Security: Implementing identity-based access for game rooms using JWT Authentication.
