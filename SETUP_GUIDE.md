# CityFlow Setup Guide

**Quick setup to run the integrated app**

---

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Groq API key (from https://console.groq.com)

---

## Step 1: Get Groq API Key

1. Go to https://console.groq.com
2. Sign up or login
3. Create API key
4. Copy your API key

---

## Step 2: Install Dependencies

```bash
cd d:\Personal\ Product\cityflow
pip install -r requirements.txt
```

This installs:
- Streamlit (frontend)
- LangChain (document processing)
- FAISS (vector database)
- Groq (AI agent)
- All other required packages

---

## Step 3: Build RAG Index

```bash
python scripts/build_faiss_index.py
```

Output should show:
```
FAISS index built successfully. Indexed chunks: XXX
```

---

## Step 4: Run the App

```bash
# Set your API key
export GROQ_API_KEY="your_api_key_here"

# Run the app
streamlit run app.py
```

**On Windows PowerShell:**
```powershell
$env:GROQ_API_KEY = "your_api_key_here"
streamlit run app.py
```

---

## Step 5: Open Browser

Streamlit will automatically open:
```
http://localhost:8501
```

Or open manually in your browser.

---

## Test the App

1. **Click an example question** (fastest test)
   - Click "I want to open a restaurant..."
   - Watch it process
   - See the checklist appear

2. **Try a custom question**
   - Type: "What permits do I need for a home-based food business?"
   - Click Search
   - See structured checklist

3. **Try out-of-scope question**
   - Type: "What's the weather?"
   - See fallback message

---

## Expected Output

Each permit question should show:

```
📋 PERMIT SUMMARY
Overview of what's needed

✅ REQUIRED STEPS
1. Requirement description
   🏢 Department Name
   💰 Rs. X,XXX
   ⏱️ X days
   📚 Source: Document.pdf

2. Next requirement
   ...

⚠️ IMPORTANT NOTES
- Edge case note 1
- Edge case note 2
```

---

## Troubleshooting

### Error: "GROQ_API_KEY not set"
```bash
# Check if key is set
echo $GROQ_API_KEY  (Linux/Mac)
echo $env:GROQ_API_KEY  (Windows PowerShell)

# If empty, set it:
export GROQ_API_KEY="your_key_here"
streamlit run app.py
```

### Error: "FAISS index not found"
```bash
python scripts/build_faiss_index.py
streamlit run app.py
```

### Error: "agent.py not found"
- Make sure you're in the right directory
- Check `ls` or `dir` shows `agent.py`
- Move to project root: `cd d:\Personal\ Product\cityflow`

### App won't start
1. Check Python version: `python --version` (should be 3.8+)
2. Check dependencies: `pip list` (should show streamlit, groq, etc)
3. Check working directory: `pwd` or `cd` to project root

---

## Commands Quick Reference

```bash
# Setup
pip install -r requirements.txt
python scripts/build_faiss_index.py

# Run
export GROQ_API_KEY="your_key"
streamlit run app.py

# Test RAG
python scripts/test_retrieval.py "your question"

# Test Agent
python agent.py

# Test Frontend only
streamlit run app.py  # (requires GROQ_API_KEY set)
```

---

## Demo Script (3-5 minutes)

### Setup (Before Demo)
1. Set GROQ_API_KEY
2. Start the app: `streamlit run app.py`
3. Wait for app to load

### During Demo
1. **Show landing page** (15 sec)
   - Point out CityFlow header
   - Show 4 example questions

2. **Click example** (20 sec)
   - Click "I want to open a restaurant..."
   - Show loading state
   - Show results appearing

3. **Review checklist** (60 sec)
   - Scroll through steps
   - Point out department, cost, timeline
   - Explain source citations
   - Note edge case warnings

4. **Show fallback** (30 sec)
   - Type "What's the weather?"
   - Show fallback message

5. **Conclusion** (15 sec)
   - Emphasize grounding in official docs
   - Clean, professional UI
   - Easy to use

**Total: ~3 minutes**

---

## File Locations

```
d:\Personal Product\cityflow\

Key files:
- app.py                  ← Run this
- agent.py               ← Member 2's AI
- requirements.txt       ← Install from this
- SETUP_GUIDE.md        ← This file
- README_MEMBER3.md     ← Integration details
- INTEGRATION_SUMMARY.md ← Architecture details

Directories:
- src/                  ← Frontend code
- rag/                  ← Member 1's RAG
- scripts/              ← Utilities
- knowledge_base/       ← Government docs
- storage/              ← Generated (FAISS index)
```

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.8+ |
| RAM | 4GB minimum (8GB recommended) |
| Disk | 2GB free (for FAISS index) |
| Internet | Required (for Groq API) |
| API | Groq account with valid key |

---

## Performance Expectations

| Action | Time |
|--------|------|
| App startup | 15-30 seconds (first time) |
| App startup | 5-10 seconds (cached) |
| Per question | 2-5 seconds |
| UI rendering | <1 second |

---

## Success Checklist

After setup, verify:

- [ ] `pip install -r requirements.txt` runs without errors
- [ ] `python scripts/build_faiss_index.py` completes successfully
- [ ] `GROQ_API_KEY` is set
- [ ] `streamlit run app.py` starts without errors
- [ ] Browser opens at http://localhost:8501
- [ ] Landing page displays
- [ ] Click example button works
- [ ] Example question processes
- [ ] Results display with checklist
- [ ] Each step shows cost/department/timeline/source
- [ ] Edge cases appear as notes
- [ ] Out-of-scope question shows fallback

**If all checkmarks pass: You're ready! 🎉**

---

## Getting Help

### Common Issues

**"ModuleNotFoundError: No module named 'streamlit'"**
→ Run: `pip install -r requirements.txt`

**"GROQ_API_KEY not set"**
→ Run: `export GROQ_API_KEY="your_key_here"` then retry

**"FAISS index not found"**
→ Run: `python scripts/build_faiss_index.py`

**"Cannot find agent.py"**
→ Make sure you're in: `d:\Personal Product\cityflow`

**App is slow**
→ Normal on first startup (loads models into memory)

### Still stuck?

1. Check README_MEMBER3.md for integration details
2. Check INTEGRATION_SUMMARY.md for architecture
3. Verify all files exist: `ls -la`
4. Check Python version: `python --version`
5. Check dependencies: `pip list | grep -E "streamlit|groq"`

---

## Next: Testing & Demo

Once setup is working:
1. See INTEGRATION_SUMMARY.md for test scenarios
2. See README_MEMBER3.md for demo script
3. Ready to present! 🚀

---

**Ready to go! Start with: `pip install -r requirements.txt`**
