# 🎓 StudBud - Your AI Study Companion

Transform your documents into podcasts, flashcards, quizzes, mind maps, and more with the power of AI.

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-blue)](https://deepmind.google/technologies/gemini/)
[![Deepgram](https://img.shields.io/badge/Deepgram-TTS-purple)](https://deepgram.com/)

---

## ✨ Features

### 📚 **Document Management**
- Upload PDF, DOCX, TXT, and image files
- Automatic text extraction with OCR support
- Organize documents in workspaces
- Multi-document analysis

### 💬 **AI Chat**
- Real-time streaming chat with Gemini 2.5 Flash
- Context-aware responses based on your documents
- Chat history saved per workspace
- Ask questions about multiple sources simultaneously

### 🎙️ **Audio Overview (Podcast Generation)**
- Generate podcast-style conversations from your documents
- Two AI hosts (Alex & Sam) discuss your content
- Convert scripts to actual audio with Deepgram TTS
- Download as MP3 files
- Perfect for learning on-the-go

### 🎬 **Video Overview**
- Create video scripts with timestamps
- Visual cues and narration suggestions
- Perfect for content creators
- Export as text files

### 🧠 **Mind Maps**
- Hierarchical visual knowledge structures
- Automatic topic extraction
- Export as JSON or TXT
- Interactive tree view

### 📇 **Flashcards**
- Auto-generate study flashcards
- Flip animation for Q&A format
- Navigate through card deck
- Export all cards at once

### 📝 **Quizzes**
- Multiple-choice question generation
- Instant feedback with explanations
- Track your progress
- Perfect for self-assessment

### 📊 **Reports**
- Comprehensive summaries
- Markdown-formatted output
- Multiple report types (summary, analysis, study guide)
- Export and share

### 🔄 **Download & Share**
- Download any output as TXT, JSON, or MP3
- Copy to clipboard
- Native share API support
- Export chat history

---

## 🎨 Design Philosophy

**Clean. Professional. Aesthetic.**

- 🌊 Soft monotone color palette
- 📐 Balanced 25%-50%-25% layout
- 💎 Light theme with subtle accents
- ✨ Smooth transitions and interactions
- 🎯 Focused on productivity

---

## 🏗️ Architecture

### **Frontend**
- **Framework:** Next.js 14 (React, TypeScript)
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **HTTP Client:** Axios
- **Icons:** Lucide React

### **Backend**
- **Framework:** Flask 3.0 (Python)
- **AI Models:** 
  - Google Gemini 2.5 Flash (text generation)
  - Google Gemini 2.0 Flash Exp (audio/video scripts)
  - Deepgram Aura (text-to-speech)
- **Database:** Supabase (PostgreSQL)
- **Storage:** Supabase Storage
- **Text Extraction:** PyPDF2, python-docx, Pillow, pytesseract

### **API Structure**
```
/api/workspace     - Workspace management
/api/sources       - Document upload & management
/api/studio        - AI generation endpoints
  ├─ /chat                    - Streaming chat
  ├─ /mindmap                 - Mind map generation
  ├─ /flashcards              - Flashcard generation
  ├─ /quiz                    - Quiz generation
  ├─ /report                  - Report generation
  ├─ /audio-overview          - Podcast script
  ├─ /video-overview          - Video script
  └─ /audio-overview/generate-audio - TTS conversion
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.9+
- Node.js 18+
- Supabase account
- Google Gemini API key
- Deepgram API key (optional, for audio)

### **1. Clone Repository**
```bash
git clone <your-repo-url>
cd windsurf-project
```

### **2. Backend Setup**
```bash
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys to .env

# Run backend
python app.py
```

### **3. Frontend Setup**
```bash
cd frontend
npm install

# Create .env.local
cp .env.local.example .env.local
# Add NEXT_PUBLIC_API_URL=http://localhost:5000

# Run frontend
npm run dev
```

### **4. Database Setup**
- Go to Supabase dashboard
- Run the SQL from `backend/database_schema.sql`
- Create storage bucket named "sources"

### **5. Open Application**
```
http://localhost:3000/studio
```

---

## 📖 Detailed Setup

See [SETUP.md](./SETUP.md) for detailed setup instructions including:
- API key acquisition
- Database configuration
- Environment variables
- Troubleshooting

---

## 🚀 Deployment to AWS

Deploy StudBud to production with auto-deployment CI/CD pipeline:

### Quick Options

- **15-minute deploy**: See [QUICK_DEPLOY.md](./QUICK_DEPLOY.md)
- **Automated setup**: Run `./scripts/setup-aws.sh`
- **Complete guide**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Summary**: Check [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md)

### Architecture
- **Backend**: AWS Elastic Beanstalk (Flask/Python)
- **Frontend**: Vercel (Next.js)
- **Database**: AWS RDS PostgreSQL
- **Storage**: AWS S3
- **CI/CD**: GitHub Actions + Vercel auto-deploy

### Why Auto-Deploy?
- ✅ **Fast**: Deploy in 5-10 minutes automatically
- ✅ **Reliable**: Consistent process every time
- ✅ **Safe**: Automated tests before deployment
- ✅ **Easy**: Just `git push` to deploy
- ✅ **Free**: GitHub Actions and Vercel free tiers

See [CICD_COMPARISON.md](./CICD_COMPARISON.md) for auto vs manual deployment comparison.

---

## 🎯 Usage

### **Basic Workflow**

1. **Create Workspace**
   - Automatically created on first visit
   - Or create new ones from dropdown

2. **Upload Documents**
   - Click upload button in Sources panel
   - Select PDF, DOCX, TXT, or images
   - Wait for text extraction

3. **Select Sources**
   - Check boxes next to documents
   - Selected sources used for all AI operations

4. **Generate Content**
   - **Chat:** Ask questions in middle panel
   - **Audio:** Click "Audio Overview" → "Generate Podcast"
   - **Video:** Click "Video Overview"
   - **Mind Map:** Click "Mind Map"
   - **Flashcards:** Click "Flashcards"
   - **Quiz:** Click "Quiz"
   - **Report:** Click "Report"

5. **Download & Share**
   - Every output has download/copy buttons
   - Audio generates playable MP3 files
   - Export for offline use

---

## 🎨 Color Scheme

```css
/* Clean Monotone Aesthetic */
--background: #f8fafc      /* Off-white */
--surface: #ffffff         /* Pure white */
--text-primary: #0f172a    /* Dark slate */
--text-secondary: #475569  /* Medium slate */
--text-tertiary: #94a3b8   /* Light slate */
--border: #e2e8f0          /* Light gray */
--primary: #6366f1         /* Soft indigo */
--accent: #a78bfa          /* Soft purple */
```

---

## 📊 Performance

| Feature | Time | Notes |
|---------|------|-------|
| Chat Response | 2-5s | Streaming |
| Mind Map | 5-10s | JSON generation |
| Flashcards (10) | 8-12s | With Q&A pairs |
| Quiz (5) | 10-15s | With explanations |
| Report | 10-20s | Comprehensive |
| Audio Script | 15-25s | Podcast dialogue |
| Audio TTS | 20-40s | Depends on length |
| Video Script | 15-25s | With timestamps |

---

## 🔧 Tech Stack Details

### **AI Models**
- **Gemini 2.5 Flash:** Chat, mind maps, flashcards, quizzes, reports
- **Gemini 2.0 Flash Exp:** Audio/video overviews (experimental features)
- **Deepgram Aura:** Text-to-speech (multi-voice support)

### **Deepgram Voices**
- **Alex (Female):** aura-asteria-en - Warm and engaging
- **Sam (Male):** aura-arcas-en - Professional and clear

### **Database Schema**
```sql
workspaces      - User workspaces
sources         - Uploaded documents
chat_history    - Chat messages
studio_outputs  - Generated content (mindmaps, flashcards, etc.)
```

### **Storage**
- Supabase Storage bucket: "sources"
- Folders: documents, audio

---

## 🎓 Perfect For

- **Students** - Study materials, exam prep
- **Researchers** - Document analysis, summaries
- **Content Creators** - Video/podcast scripts
- **Teachers** - Educational material generation
- **Professionals** - Report generation, analysis

---

## 🔮 Future Enhancements

- [ ] PDF export for all outputs
- [ ] Custom voice selection
- [ ] Multi-language support
- [ ] Collaboration features
- [ ] Mobile app
- [ ] Voice input for chat
- [ ] Background music for podcasts
- [ ] Video generation from scripts
- [ ] Spaced repetition for flashcards
- [ ] Progress tracking and analytics

---

## 📝 License

MIT License - feel free to use for personal or commercial projects

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- **Google Gemini** - AI text generation
- **Deepgram** - Text-to-speech
- **Supabase** - Database and storage
- **Next.js** - Frontend framework
- **Flask** - Backend framework

---

**Built with ❤️ for students and learners everywhere**

---

## 📸 Screenshots

### Main Interface
Clean 3-panel layout with balanced proportions

### Studio Tools
7 AI-powered tools with soft gradient icons

### Audio Overview
Podcast-style conversation with playable audio

### Mind Map
Hierarchical knowledge visualization

### Flashcards
Interactive flip cards for studying

---

**StudBud - Transform how you study with AI** 🎓✨
