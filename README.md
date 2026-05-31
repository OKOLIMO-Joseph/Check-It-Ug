# Check-It-Ug
AI-powered misinformation detector for Uganda 🇺🇬 | Fact-check WhatsApp forwards, SMS, and web claims with Gemini AI

# CheckIt UG — Combat misinformation in Uganda with AI

**CheckIt UG** is a free, AI-powered fact-checking platform designed specifically for Uganda. It helps citizens verify suspicious WhatsApp forwards, SMS messages, and online claims using Google's Gemini AI and credible local sources.

## 🎯 Why this matters
Misinformation spreads rapidly on WhatsApp in Uganda, affecting elections, health decisions, and public safety. CheckIt UG provides an accessible tool to fight back—no technical skills required.

## ✨ Features
- **🤖 Free AI fact-checking** using Google Gemini (free tier)
- **🌍 Multi-language support** – English, Luganda, & Runyankole  
- **📱 Multiple channels** – Web app, WhatsApp bot, & SMS
- **⚡ Smart caching** – 6-hour cache for repeated claims
- **📊 Admin dashboard** – Track misinformation trends
- **🔍 Source transparency** – Always shows evidence sources
- **🎨 Modern UI** – Built with Next.js 14 & Tailwind CSS

## 🛠️ Tech Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Recharts
- **Backend**: FastAPI (Python 3.11), PostgreSQL, Redis  
- **AI**: Google Gemini 1.5 Flash (free tier)
- **Messaging**: Twilio (WhatsApp), Africa's Talking (SMS)
- **DevOps**: Docker Compose, GitHub Actions CI/CD

## 🚀 Quick Start
```bash
# Clone the repo
git clone https://github.com/yourusername/checkit-ug.git

# Set up environment
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Launch with Docker
docker-compose up -d

# Open http://localhost:3000
