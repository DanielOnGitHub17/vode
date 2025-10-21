# VODE - AI-Powered Technical Interview Platform

## 📋 Table of Contents
- [What is VODE?](#what-is-vode)
- [Architecture & Technology](#architecture--technology)
- [How It Was Built](#how-it-was-built)
- [Features](#features)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [What's Next](#whats-next)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 What is VODE?

**VODE** (Virtual Online Developer Examination) is an AI-powered technical interview platform that conducts real-time coding interviews with candidates. It uses advanced AI models to:

- **Generate Questions**: Creates dynamic coding problems tailored to difficulty levels and topics
- **Provide Real-Time Feedback**: Gives intelligent, context-aware coaching during the interview
- **Evaluate Performance**: Scores candidates based on correctness, approach, communication, and code quality
- **Record Interviews**: Captures screen, candidate video, and audio for review
- **Maintain Conversation History**: Keeps track of the entire interview for consistent feedback

### Key Differentiators
- 🤖 **AI-Powered**: Uses Google Gemini 2.0 Flash Lite for intelligent questioning and feedback
- 🎥 **Dual Recording**: Captures both screen and candidate camera feeds separately
- ☁️ **Cloud Storage**: Integrates with Cloudflare Stream for video storage
- 🔊 **Voice Feedback**: Uses ElevenLabs for natural-sounding audio responses
- 💬 **Real-Time Chat**: Live interaction with AI interviewer
- 📊 **Performance Analytics**: Detailed scoring and feedback

---

## 🏗️ Architecture & Technology

### Tech Stack

**Backend**
- **Framework**: Django 5.2.7 (Python)
- **Database**: SQLite (local) / PostgreSQL (production)
- **AI/ML**: Google Generative AI (Gemini 2.0 Flash Lite)
- **Audio**: ElevenLabs Text-to-Speech API
- **Server**: Gunicorn (production) with Whitenoise for static files
- **Deployment**: Heroku

**Frontend**
- **HTML/CSS/JavaScript**: Vanilla JS with Bootstrap 5
- **Editor**: Code editor with syntax highlighting
- **Media Recording**: MediaRecorder API for screen/video capture
- **Audio Visualization**: Custom sine-wave pulse animation
- **WebRTC**: For permission requests and stream handling

**Infrastructure**
- **Version Control**: Git/GitHub
- **Video Storage**: Cloudflare Stream API
- **Environment Variables**: python-dotenv

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Browser)                      │
│  - Interview Interface (code editor, chat, video)           │
│  - Recording Manager (screen + camera)                      │
│  - Real-time Chat UI                                        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                    Django Backend                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Interview Views                                        │ │
│  │ - interview/views.py: Main interview logic            │ │
│  │ - cand/views.py: Candidate dashboard                  │ │
│  │ - recruit/views.py: Recruiter dashboard              │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Services Layer (Orchestration)                        │ │
│  │ - interview_orchestrator.py: Coordinates services    │ │
│  │ - gemini_service.py: AI question & feedback gen       │ │
│  │ - elevenlabs_service.py: Text-to-speech conversion   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Models (Database Schema)                              │ │
│  │ - Interview, Question, Round, Role                    │ │
│  │ - Candidate, Recruiter, SWE                          │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Gemini API  │ │ ElevenLabs   │ │ Cloudflare   │
│  (Question   │ │ (TTS Audio)  │ │ Stream       │
│   & Feedback)│ │              │ │ (Videos)     │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## 🛠️ How It Was Built

### Phase 1: Foundation (Models & Database)
1. Created Django apps: `cand`, `interview`, `recruit`, `swe`
2. Designed database models:
   - User roles (Candidate, Recruiter, SWE)
   - Interview workflow (Round → Interview → Question)
   - Interview metadata (difficulty, topics, time limits)

### Phase 2: Interview Engine
1. Integrated Google Gemini API for:
   - Dynamic question generation (with context awareness)
   - Real-time AI coaching feedback
   - Performance scoring and evaluation
2. Set up ElevenLabs for text-to-speech conversion

### Phase 3: Frontend Development
1. Built interview interface with:
   - Real-time code editor
   - Chat system for Q&A
   - Permission management for camera/microphone/screen
2. Implemented dual video recording:
   - Screen recording with system audio
   - Candidate video with audio
3. Created visual feedback (animated circles with audio sync)

### Phase 4: Video Recording & Upload
1. Implemented MediaRecorder API for dual recordings
2. Integrated Cloudflare Stream for video storage
3. Added Bearer token authentication for uploads
4. Created fallback mechanisms for upload failures

### Phase 5: Production Deployment
1. Added Heroku deployment configuration:
   - Procfile (gunicorn + release tasks)
   - runtime.txt (Python version specification)
   - requirements.txt (dependencies)
2. Configured PostgreSQL for production database
3. Set up Whitenoise for static file serving
4. Added environment-based security settings

### Phase 6: Error Handling & Resilience
1. Implemented graceful degradation:
   - If audio generation fails, still return text feedback
   - If Gemini fails, return fallback messages
   - Always return reasoning even if score generation fails
2. Added comprehensive error logging
3. Separated concerns with independent try blocks

---

## ✨ Features

### Current Features
- ✅ Dynamic AI-generated interview questions
- ✅ Real-time AI coaching and feedback
- ✅ Live chat with AI interviewer
- ✅ Dual video recording (screen + camera)
- ✅ Cloudflare video upload integration
- ✅ AI-based performance scoring
- ✅ Candidate dashboard with completed interviews
- ✅ Admin panel for management
- ✅ Mobile-responsive UI

### In Development
- 🔄 Code execution/testing in browser
- 🔄 Advanced analytics dashboard
- 🔄 Interview scheduling system
- 🔄 Multi-language support
- 🔄 Interview templates/presets

### Planned Features
- 📋 Behavioral interview mode
- 📋 System design interview mode
- 📋 Team collaboration features
- 📋 Integration with ATS systems
- 📋 Advanced reporting and insights

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip or conda
- Git
- (Optional) PostgreSQL for production

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/DanielOnGitHub17/vode.git
cd vode
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env with your values:
# - GEMINI_API_KEY=your_key
# - ELEVENLABS_API_KEY=your_key
# - SECRET_KEY=your_secret
```

#### 5. Run Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

#### 7. Start Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

### Heroku Deployment

See [HEROKU_DEPLOYMENT.md](./HEROKU_DEPLOYMENT.md) for detailed instructions.

Quick summary:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:essential-0
heroku config:set GEMINI_API_KEY=your_key
heroku config:set ELEVENLABS_API_KEY=your_key
git push heroku main
heroku run python manage.py migrate
```

---

## 📁 Project Structure

```
vode/
├── cand/                           # Candidate app
│   ├── models.py                   # Candidate model
│   ├── views.py                    # Dashboard view
│   └── migrations/
├── interview/                      # Core interview app
│   ├── models.py                   # Interview, Question, Round models
│   ├── views.py                    # Interview endpoints
│   ├── services/
│   │   ├── gemini_service.py       # AI question & feedback generation
│   │   ├── elevenlabs_service.py   # Text-to-speech
│   │   └── interview_orchestrator.py # Service coordination
│   ├── mocks.py                    # Mock questions & prompts
│   ├── migrations/
│   └── urls.py
├── recruit/                        # Recruiter app
│   ├── models.py
│   └── views.py
├── swe/                            # SWE/Admin app
│   ├── models.py
│   └── views.py
├── static/                         # Static files
│   ├── interview/
│   │   ├── recorder.js             # Video recording logic
│   │   ├── permissions.js          # Permission handling
│   │   ├── page.js                 # Chat & UI
│   │   ├── api.js                  # API calls
│   │   ├── watch.js                # Event handlers
│   │   ├── end.js                  # End page animation
│   │   ├── custom.css              # Interview styles
│   │   └── end.css                 # End page styles
│   ├── styles.css                  # Global styles
│   └── cand/
│       └── custom.css
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── cand/
│   │   └── index.html              # Candidate dashboard
│   └── interview/
│       ├── index.html              # Interview page
│       └── end.html                # End page
├── vode/                           # Main project settings
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # URL routing
│   ├── asgi.py                     # ASGI config
│   └── wsgi.py                     # WSGI config
├── manage.py                       # Django CLI
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku process definition
├── runtime.txt                     # Python version
├── .env.example                    # Environment variables template
├── app.json                        # Heroku app config
└── README.md                       # This file
```

---

## 🔌 API Endpoints

### Interview Endpoints

#### Get Interview Page
```
GET /interview/{id}/
Returns: Interview page with question and controls
```

#### Submit Code/Audio for Feedback
```
POST /interview/api/get-response/
Body: {
  "interview_id": int,
  "code": string,
  "audio_transcript": string
}
Returns: {
  "reasoning": string,
  "audio": base64_string,
  "success": boolean
}
```

#### End Interview
```
POST /interview/api/end-interview/
Body: {
  "interview_id": int
}
Returns: {
  "score": 0-100,
  "feedback": string,
  "message": string,
  "success": boolean
}
```

#### View End Page
```
GET /interview/{id}/end/
Params: screen_video=url, candidate_video=url
Returns: End page with audio visualization
```

### Candidate Endpoints

#### Dashboard
```
GET /candidate/
Returns: Candidate dashboard with pending & completed interviews
```

### Admin Endpoints

#### Admin Panel
```
GET /admin/
Access Django admin interface
```

---

## ⚙️ Configuration

### Environment Variables

**Required (API Keys)**
```
GEMINI_API_KEY=your_google_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

**Django Settings**
```
SECRET_KEY=your_django_secret_key
DEBUG=False (production) / True (development)
```

**Optional (Video Storage)**
```
CLOUDFLARE_API_KEY=your_cloudflare_key
CLOUDFLARE_ACCOUNT_ID=your_account_id
```

### Database Configuration

**Local Development (SQLite)**
```python
# Automatic in settings.py
```

**Production (PostgreSQL)**
```python
# Automatic on Heroku via DATABASE_URL
# Or set manually:
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Security Settings

Production automatically enables:
- HTTPS redirect
- Secure cookies
- CSRF protection
- XSS filtering
- Content-Type validation
- HSTS headers

---

## 🔮 What's Next

### Short-term (1-2 weeks)
- [ ] Add code execution/testing capabilities
- [ ] Implement interview scheduling
- [ ] Add more interview modes (system design, behavioral)
- [ ] Create interview templates

### Medium-term (1 month)
- [ ] Build advanced analytics dashboard
- [ ] Add multi-language support
- [ ] Implement team collaboration features
- [ ] Create mobile app

### Long-term (3+ months)
- [ ] AI-powered interview question library
- [ ] Integration with popular ATS systems
- [ ] Advanced reporting and insights
- [ ] Custom interview workflows
- [ ] Peer review system for SWEs

### Performance Improvements
- [ ] Implement caching for questions
- [ ] Add CDN for static assets
- [ ] Optimize video compression
- [ ] Add background job processing (Celery)

---

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'django'"
```bash
# Activate virtual environment and install dependencies
pip install -r requirements.txt
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

#### API Keys Not Working
```bash
# Check .env file exists in project root
# Verify keys are correct
# Restart server after changing .env
```

#### Video Upload Fails
```
# Check Cloudflare credentials
# Verify video file size < 200MB
# Check network connection
# View logs: heroku logs --tail
```

#### Audio Not Playing
```
# Check browser console for errors
# Verify ElevenLabs API key is valid
# Check audio format (should be MP3)
# Try different browser
```

### Debug Mode

Enable verbose logging:
```python
# In settings.py
LOGGING['root']['level'] = 'DEBUG'
```

View logs:
```bash
# Local
python manage.py runserver --debug-level DEBUG

# Heroku
heroku logs --tail
```

---

## 📚 Documentation

- [Local Development Guide](./LOCAL_DEVELOPMENT.md)
- [Heroku Deployment Guide](./HEROKU_DEPLOYMENT.md)
- [Heroku Commands Reference](./HEROKU_COMMANDS.md)
- [Django Docs](https://docs.djangoproject.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [ElevenLabs Docs](https://elevenlabs.io/docs)
- [Cloudflare Stream Docs](https://developers.cloudflare.com/stream/)

---

## 🤝 Contributing

### Setup Development Environment
```bash
# Clone and setup (see Getting Started)
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# Commit with descriptive message
git commit -m "feat: description of changes"

# Push and create pull request
git push origin feature/your-feature-name
```

### Code Style
- Python: Follow PEP 8
- JavaScript: Use 2-space indentation
- CSS: Use kebab-case for class names

### Testing
```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test cand

# With coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📄 License

This project is part of HackTX 2025. See LICENSE file for details.

---

## 👥 Team & Credits

- **Daniel** - Lead Developer
- **Enesi** - Lead Developer
- Built for HackTX 2025

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open a GitHub issue
- Contact the development team
- Check troubleshooting guide above

---

**Last Updated**: October 21, 2025  
**Version**: 1.0.0  
**Status**: Active Development
