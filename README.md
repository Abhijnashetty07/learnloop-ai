# LearnLoop AI

**A personalised AI tutor that adapts to how each learner actually understands.**
AI Build Challenge 2026 - PS-03: Personalised AI Tutor for Learning AI - Team Alter Ego

**Live demo:** https://learnloop-ai-b2ji.onrender.com
(Hosted on a free tier, so the first load after idle can take about a minute.)

## The problem
Most AI courses give every learner the same explanation, whatever they already know or exactly where they are stuck. Learners re-watch the same lecture for hours, and many give up at hard topics like backpropagation.

## What LearnLoop AI does
1. The learner picks a concept from a map of 18 AI/ML topics.
2. They read a short explanation and answer a check question by typing or speaking.
3. Gemini scores the free-text answer and adapts:
   - Confused: the tutor re-explains with an everyday analogy.
   - Almost there: it asks a follow-up question about the exact missing idea.
   - Mastered: the next concept unlocks.
4. A mastery tracker and a Chart.js dashboard show progress.

## Features
- Adaptive explanations (analogy, simpler or deeper) on demand
- Free-text and voice answers (browser speech recognition)
- Prerequisite-aware learning path: advanced topics unlock only when the basics are solid
- Live concept tracker: mastered, shaky, locked, plus a "next up" recommendation
- Session progress chart (Chart.js)
- Loopy, a tutor robot that reacts to answers and can read explanations aloud
- Separate progress for each visitor
- Fallback mode: if the AI service is busy, built-in explanations and scoring keep the app running

## Tech stack
Python, Flask, Google Gemini API, Chart.js, plain HTML/CSS/JavaScript, browser Web Speech APIs. Hosted on Render.

## Run it locally
```
git clone https://github.com/Abhijnashetty07/learnloop-ai.git
cd learnloop-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Create a file named `.env` containing your own Gemini API key:
```
GEMINI_API_KEY=your_key_here

```
python app.py
```
Then start the app and open http://127.0.0.1:5000
```
## Project files
- `app.py` - Flask backend: concept state, unlocking, answer scoring
- `llm.py` - Gemini calls with model fallback
- `concepts.json` - the prerequisite concept graph
- `templates/index.html` - the web interface

## Limitations and next steps
- Progress is kept in memory and resets when the server restarts.
- Voice input works best in Chrome or Edge.
- Next: test with 5 to 10 learners and compare check-question scores before and after adaptation, grow the concept map, and add learner accounts.
