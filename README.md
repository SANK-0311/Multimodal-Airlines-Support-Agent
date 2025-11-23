# ✈️ ERWIQ Airlines Customer Support Agent

A multimodal AI-powered customer support agent for ERWIQ Airlines, built with OpenAI, Claude, Gemini, and Gradio.


## 🌟 Features

### Multimodal Capabilities
- 💬 **Text Chat** - Natural conversation with context awareness
- 🎤 **Voice Input** - Speak your questions via microphone
- 🔊 **Voice Output** - Listen to responses with text-to-speech
- 🖼️ **Image Generation** - See beautiful Indian destination images

### Function Calling Tools
- 🎫 **Ticket Prices** - Check fares to 12 Indian cities
- ✈️ **Flight Status** - Real-time flight status updates
- 📋 **Booking Lookup** - PNR/booking reference lookup
- 💰 **Refund Processing** - Handle refund requests

### RAG (Retrieval-Augmented Generation)
- 📜 **Policy Search** - Search airline FAQs and policies
- 📚 **Knowledge Base** - 15+ policy documents embedded
- 🎯 **Accurate Answers** - Grounded in actual policies

### Production Features
- 🔄 **Multi-Model Fallback** - OpenAI, Claude, Gemini with automatic failover
- 📊 **Analytics Dashboard** - Track usage and performance
- 📝 **Audit Logging** - Full conversation logging
- 🔔 **Notifications** - Alert on errors and issues

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/erwiq-airlines-agent.git
cd erwiq-airlines-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 5. Run the application
```bash
python app.py
```

### 6. Open in browser
Navigate to `http://localhost:7860`

## 📁 Project Structure
```
Airlines-Agent/
├── app.py                 # Main application (Gradio UI + chat logic)
├── tools.py               # Function calling tools
├── knowledge_base.py      # RAG and policy documents
├── config.py              # Configuration and constants
├── utils.py               # Logging, analytics, notifications
├── knowledge_base.json    # RAG and policy documents in embeddings
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
├── .env                   # environment variables
└── README.md              # This file
```

## 🎯 Sample Queries

### Ticket Prices
- "How much is a business class ticket to Mumbai?"
- "What's the price for economy to Goa?"

### Flight Status
- "Is flight EQ101 on time?"
- "What's the status of EQ404?"

### Booking Lookup
- "Look up booking ABC123"
- "Check my reservation XYZ789"

### Policies
- "What's the baggage allowance?"
- "Can I bring my pet on the plane?"
- "What's your refund policy?"

### Refunds
- "I want to cancel booking ABC123"

### Images
- "Show me what Jaipur looks like"

## 🗺️ Available Routes

| Flight | Route | Departure |
|--------|-------|-----------|
| EQ101 | Mumbai → Delhi | 06:00 |
| EQ202 | Delhi → Bangalore | 09:30 |
| EQ303 | Chennai → Kolkata | 14:15 |
| EQ404 | Hyderabad → Mumbai | 18:45 |
| EQ505 | Bangalore → Goa | 11:00 |
| EQ606 | Pune → Jaipur | 07:30 |
| EQ707 | Kochi → Chennai | 16:00 |
| EQ808 | Ahmedabad → Lucknow | 20:30 |

## 💰 Destinations & Prices (₹)

| City | Economy | Business | First |
|------|---------|----------|-------|
| Mumbai | 4,999 | 12,999 | 24,999 |
| Delhi | 5,499 | 14,999 | 28,999 |
| Bangalore | 4,499 | 11,999 | 22,999 |
| Goa | 5,499 | 13,999 | 26,999 |
| Jaipur | 4,199 | 10,499 | 20,999 |
| Chennai | 4,299 | 10,999 | 21,999 |
| And more... | | | |

## 🚀 Deployment to Render

1. Push your code to GitHub

2. Connect your repo to Render

3. Add environment variables in Render dashboard:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY` (optional)
   - `GOOGLE_API_KEY` (optional)

4. Deploy! Render will use `render.yaml` configuration

## 📊 Tech Stack

- **LLMs**: OpenAI GPT-4o-mini, Claude Sonnet, Gemini Flash
- **Embeddings**: OpenAI text-embedding-3-small
- **Voice**: OpenAI Whisper (STT), OpenAI TTS
- **Images**: DALL-E 3
- **UI**: Gradio 4.0+
- **Deployment**: Render



## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📞 Support

For questions about this project, open a GitHub issue.

---

Built with ❤️ for learning AI/ML engineering

