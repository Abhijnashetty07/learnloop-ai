# LearnLoop AI

**A personalised AI tutor that adapts to how each learner actually understands.**
AI Build Challenge 2026 | PS-03: Personalised AI Tutor for Learning AI | Team Alter Ego

**Live demo:** https://learnloop-ai-b2ji.onrender.com
(Free hosting sleeps when idle, so the first load can take a few seconds to a minute.)

## Project Overview

**Problem:** Most AI courses give every learner the same explanation, whatever they already know or exactly where they are stuck. Learners re-watch the same lecture for hours, and many give up at hard topics like backpropagation.

**Solution:** LearnLoop AI is a tutor that responds to how a learner actually understands.
1. The learner picks a concept from a prerequisite map of 18 AI/ML topics.
2. They read a short explanation and answer a check question by typing or speaking.
3. Gemini scores the free-text answer, and the tutor adapts:
   - Confused: re-explains with an everyday analogy.
   - Almost there: asks a follow-up question about the exact missing idea.
   - Mastered: unlocks the next concept.
4. A mastery tracker and a Chart.js dashboard show progress.

**Key features**
- Adaptive explanations (analogy, simpler or deeper) on demand
- Free-text and voice answers
- Prerequisite-aware learning path with a "next up" recommendation
- Live concept tracker (mastered, shaky, locked)
- Session progress chart
- Loopy, a tutor robot that reacts to answers and can read explanations aloud
- Separate progress for each visitor
- Fallback mode: if the AI service is busy, built-in explanations and scoring keep the app running

## Technologies Used
- Python and Flask (backend)
- Google Gemini API (explanations and answer scoring)
- JSON file for the prerequisite concept graph
- Chart.js (progress charts)
- HTML, CSS and JavaScript (frontend)
- Browser Web Speech APIs (voice input and spoken replies)
- GitHub and Render (code hosting and deployment)

## Setup and Installation

**Requirements:** Python 3.10 or newer, Git, and a free Gemini API key from https://aistudio.google.com/apikey

1. Clone the repository:
```
git clone https://github.com/Abhijnashetty07/learnloop-ai.git
cd learnloop-ai
```
2. Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate
```
(On Mac or Linux, use `source venv/bin/activate` instead.)

3. Install the dependencies:
```
pip install -r requirements.txt
```
4. Create a file named `.env` in the project folder and add your own key:
```
GEMINI_API_KEY=your_key_here
```
Without a key, the app still runs in fallback mode with built-in explanations and scoring.

## How to Run

Start the server:
```
python app.py
```
Then open http://127.0.0.1:5000 in Chrome or Edge.

**Using the app:** open the Topics tab and pick the NEXT UP concept, read the explanation on the Learn page, answer by typing or tapping Speak your answer, then check your score and the follow-up question. Turn on Loopy voice to hear explanations. Open the Progress tab for the chart.

## Project Structure
- `app.py` - Flask backend: concept state, unlocking, answer scoring
- `llm.py` - Gemini calls with model fallback
- `concepts.json` - the prerequisite concept graph
- `templates/index.html` - the web interface
- `requirements.txt` - Python dependencies

## Limitations and Next Steps
- Progress is kept in memory and resets when the server restarts.
- Voice input works best in Chrome or Edge.
- Next: test with real learners and compare check-question scores before and after adaptation, grow the concept map, and add learner accounts.
