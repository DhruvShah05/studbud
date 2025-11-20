# 🛠️ StudBud - Complete Setup Guide

This guide will walk you through setting up StudBud from scratch.

---

## 📋 Prerequisites

### **Required**
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **pip** - Python package manager (comes with Python)
- **npm** - Node package manager (comes with Node.js)

### **Accounts Needed**
- **Supabase** - [Sign up](https://supabase.com/)
- **Google AI Studio** - [Get API key](https://makersuite.google.com/app/apikey)
- **Deepgram** (Optional) - [Sign up](https://console.deepgram.com/) for audio features

---

## 🔑 Step 1: Get API Keys

### **1.1 Google Gemini API Key**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)
4. Save it securely

### **1.2 Supabase Credentials**

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project
3. Go to **Settings** → **API**
4. Copy:
   - **Project URL** (e.g., `https://xxx.supabase.co`)
   - **Anon/Public Key** (starts with `eyJ...`)

### **1.3 Deepgram API Key (Optional)**

1. Go to [Deepgram Console](https://console.deepgram.com/)
2. Sign up for free account
3. Go to **API Keys**
4. Create new key
5. Copy the key

---

## 💾 Step 2: Database Setup

### **2.1 Create Supabase Database**

1. In your Supabase project, go to **SQL Editor**
2. Click **New Query**
3. Copy the entire contents of `backend/database_schema.sql`
4. Paste and click **Run**
5. Verify tables created: `workspaces`, `sources`, `chat_history`, `studio_outputs`

### **2.2 Create Storage Bucket**

1. Go to **Storage** in Supabase dashboard
2. Click **New Bucket**
3. Name: `sources`
4. Make it **Public**
5. Click **Create**

### **2.3 Configure Storage Policies**

Run this SQL in SQL Editor:

```sql
-- Allow public access to storage
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING (bucket_id = 'sources');

CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'sources');
```

---

## 🔧 Step 3: Backend Setup

### **3.1 Install Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**If you get errors:**
```bash
# Clear pip cache
pip cache purge

# Try upgrading pip
python -m pip install --upgrade pip

# Install again
pip install -r requirements.txt
```

### **3.2 Create Environment File**

Create `backend/.env`:

```env
# Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# Flask
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Deepgram (Optional - for audio features)
DEEPGRAM=your_deepgram_api_key_here
```

**Generate Flask Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### **3.3 Test Backend**

```bash
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Test health check:**
```bash
curl http://localhost:5000/api/health
```

Should return: `{"status": "healthy"}`

---

## 🎨 Step 4: Frontend Setup

### **4.1 Install Dependencies**

```bash
cd frontend
npm install
```

**If you get errors:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Install again
npm install
```

### **4.2 Create Environment File**

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### **4.3 Test Frontend**

```bash
npm run dev
```

**Expected output:**
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

---

## 🚀 Step 5: Run Application

### **5.1 Start Backend (Terminal 1)**

```bash
cd backend
python app.py
```

Keep this running.

### **5.2 Start Frontend (Terminal 2)**

```bash
cd frontend
npm run dev
```

Keep this running.

### **5.3 Open Application**

Go to: **http://localhost:3000/studio**

---

## ✅ Step 6: Verify Setup

### **6.1 Test Workspace Creation**

1. Open http://localhost:3000/studio
2. Should see "My Workspace" created automatically
3. Check Supabase dashboard → `workspaces` table should have 1 row

### **6.2 Test Document Upload**

1. Click upload button in Sources panel
2. Select a PDF or TXT file
3. Wait for upload and text extraction
4. Document should appear in list
5. Check Supabase → `sources` table should have 1 row
6. Check Supabase Storage → `sources` bucket should have file

### **6.3 Test Chat**

1. Select uploaded document (checkbox)
2. Type a question in chat
3. Should see streaming response
4. Check Supabase → `chat_history` table should have messages

### **6.4 Test Studio Tools**

1. Select document
2. Click "Mind Map" → Should generate hierarchical map
3. Click "Flashcards" → Should generate study cards
4. Click "Quiz" → Should generate questions
5. All outputs saved in `studio_outputs` table

### **6.5 Test Audio (Optional)**

1. Select document
2. Click "Audio Overview" → Generates script
3. Click "Generate Podcast" → Converts to audio (requires Deepgram)
4. Audio player should appear
5. Can play and download MP3

---

## 🐛 Troubleshooting

### **Backend Issues**

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

**Error: "GEMINI_API_KEY not found"**
- Check `.env` file exists in `backend/` folder
- Check key is correct (no quotes, no spaces)

**Error: "Connection refused"**
- Check backend is running on port 5000
- Check no other app using port 5000

**Error: "Supabase connection failed"**
- Check SUPABASE_URL and SUPABASE_KEY in `.env`
- Check Supabase project is active

### **Frontend Issues**

**Error: "npm install failed"**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Error: "Cannot connect to backend"**
- Check backend is running
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check no CORS errors in browser console

**Error: "Page not found"**
- Go to http://localhost:3000/studio (not just localhost:3000)

### **Database Issues**

**Error: "Table does not exist"**
- Run `database_schema.sql` in Supabase SQL Editor
- Check all tables created

**Error: "Storage bucket not found"**
- Create bucket named "sources" in Supabase Storage
- Make it public

**Error: "Permission denied"**
- Run storage policies SQL (see Step 2.3)

### **Deepgram Issues**

**Error: "Deepgram API key not found"**
- Add `DEEPGRAM=your_key` to backend `.env`
- Restart backend

**Error: "Audio generation failed"**
- Check Deepgram account has credits
- Check API key is valid
- Audio feature is optional - other features work without it

---

## 🔄 Update Database Schema

If you need to add audio/video output types:

```sql
ALTER TABLE studio_outputs DROP CONSTRAINT IF EXISTS studio_outputs_output_type_check;

ALTER TABLE studio_outputs ADD CONSTRAINT studio_outputs_output_type_check 
CHECK (output_type IN ('mindmap', 'flashcards', 'quiz', 'report', 'audio_overview', 'video_overview'));
```

---

## 📦 Production Deployment

### **Backend (Heroku/Railway)**

1. Add `Procfile`:
```
web: gunicorn app:app
```

2. Set environment variables in platform dashboard

3. Deploy

### **Frontend (Vercel/Netlify)**

1. Connect GitHub repo
2. Set build command: `npm run build`
3. Set environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy

### **Database**

- Supabase handles scaling automatically
- No additional setup needed

---

## 🔐 Security Notes

### **API Keys**
- Never commit `.env` files to Git
- Use environment variables in production
- Rotate keys regularly

### **Supabase**
- Use Row Level Security (RLS) for production
- Limit storage bucket access
- Enable authentication

### **CORS**
- Update CORS settings in `app.py` for production domain
- Don't use `*` in production

---

## 📊 Monitoring

### **Backend Logs**
```bash
# Check Flask logs
tail -f backend/logs/app.log
```

### **Frontend Logs**
- Check browser console (F12)
- Check Next.js terminal output

### **Database**
- Monitor in Supabase dashboard
- Check query performance
- Monitor storage usage

---

## 🎯 Performance Optimization

### **Backend**
- Use Redis for caching (optional)
- Enable gzip compression
- Use CDN for static files

### **Frontend**
- Enable Next.js image optimization
- Use lazy loading for components
- Minimize bundle size

### **Database**
- Add indexes for frequently queried columns
- Use connection pooling
- Regular vacuum/analyze

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Deepgram Documentation](https://developers.deepgram.com/)

---

## 🆘 Getting Help

1. Check this guide first
2. Check error messages carefully
3. Search GitHub issues
4. Open new issue with:
   - Error message
   - Steps to reproduce
   - Environment details

---

**Setup complete! Enjoy using StudBud! 🎓✨**
Just for vercel