import os, re, json
from flask import Flask, jsonify, request, send_from_directory
from llm import ask_gemini

app = Flask(__name__)

with open("concepts.json", encoding="utf-8-sig") as f:
    CONCEPTS = json.load(f)
BY_ID = {c["id"]: c for c in CONCEPTS}

PASS_MARK = 70
SHAKY_MARK = 40


def fresh_state():
    return {"user_name": "Abhijna", "best": {}, "history": []}


STATE = fresh_state()


def status_of(c):
    best = STATE["best"].get(c["id"])
    if best is not None:
        return "mastered" if best >= PASS_MARK else "shaky"
    if all(STATE["best"].get(p, 0) >= PASS_MARK for p in c["prerequisites"]):
        return "available"
    return "locked"


def overall_level():
    return round(sum(STATE["best"].values()) / len(CONCEPTS))


def next_up():
    for c in CONCEPTS:
        if status_of(c) == "shaky":
            return c["id"]
    for c in CONCEPTS:
        if status_of(c) == "available":
            return c["id"]
    return None


def verdict_for(score):
    if score >= PASS_MARK:
        return "mastered"
    if score >= SHAKY_MARK:
        return "shaky"
    return "confused"


def build_explain_prompt(c, mode):
    p = "You are a friendly AI tutor for a beginner. Concept: " + c["name"] + ". "
    p += "Reference facts: " + c["explanation"] + " "
    if mode == "analogy":
        p += "The learner is confused. Re-explain using a simple everyday non-technical analogy, under 120 words. "
    elif mode == "deeper":
        p += "The learner is ready for more. Give a deeper explanation with one concrete example, under 150 words. "
    else:
        p += "Give a short, clear explanation, under 100 words. "
    p += "Plain text only, no markdown, no headings."
    return p


def get_explanation(c, mode):
    text = ask_gemini(build_explain_prompt(c, mode))
    if text:
        return text.strip(), "gemini"
    if mode == "analogy":
        return c["analogy"] + " " + c["explanation"], "demo"
    return c["explanation"], "demo"


def demo_score(c, answer):
    words = set(re.findall(r"[a-z]{5,}", answer.lower()))
    ref = set(re.findall(r"[a-z]{5,}", (c["explanation"] + " " + c["analogy"]).lower()))
    overlap = len(words & ref)
    n = len(answer.split())
    score = min(100, overlap * 12 + min(n, 40))
    if n < 4:
        score = min(score, 20)
    if score >= PASS_MARK:
        fb = "Good answer. You covered the key ideas."
    elif score >= SHAKY_MARK:
        fb = "You are on the right track, but add more detail on the core idea."
    else:
        fb = "This needs work. Try again after re-reading the explanation."
    return score, fb, "demo"


def evaluate(c, answer):
    prompt = (
        "You are grading a beginner's answer in an AI tutoring app.\n"
        "Concept: " + c["name"] + "\n"
        "Reference explanation: " + c["explanation"] + "\n"
        "Question: " + c["check_question"] + "\n"
        "Learner answer: " + answer + "\n\n"
        "Score the answer from 0 to 100 for understanding. Be fair to beginners: "
        "correct ideas in simple words deserve 70 or more. "
        "Reply with ONLY a JSON object like "
        '{"score": 75, "feedback": "one or two encouraging sentences", "follow_up": "one short question about the biggest missing idea, empty if nothing is missing"} '
        "and nothing else."
    )
    text = ask_gemini(prompt)
    if text:
        try:
            clean = re.sub(r"```json|```", "", text).strip()
            data = json.loads(clean[clean.find("{"): clean.rfind("}") + 1])
            score = max(0, min(100, int(data["score"])))
            return score, str(data.get("feedback", "")), "gemini", str(data.get("follow_up", ""))
        except Exception as e:
            print("could not read Gemini score:", e)
    s, f, src = demo_score(c, answer)
    return s, f, src, ""


@app.route("/")
def home():
    if os.path.exists(os.path.join("templates", "index.html")):
        return send_from_directory("templates", "index.html")
    return "LearnLoop backend is running. Frontend coming next."


@app.route("/api/state")
def state():
    return jsonify({
        "next": next_up(),
        "user_name": STATE["user_name"],
        "overall": overall_level(),
        "history": STATE["history"],
        "concepts": [
            {"id": c["id"], "name": c["name"], "status": status_of(c),
             "best": STATE["best"].get(c["id"]), "prerequisites": c["prerequisites"]}
            for c in CONCEPTS
        ],
    })


@app.route("/api/start", methods=["POST"])
def start():
    data = request.get_json(force=True)
    c = BY_ID.get(data.get("id"))
    if c is None:
        return jsonify({"error": "Unknown concept"}), 404
    if status_of(c) == "locked":
        return jsonify({"error": "Master the prerequisites first"}), 403
    mode = data.get("mode", "normal")
    text, source = get_explanation(c, mode)
    return jsonify({"id": c["id"], "name": c["name"], "explanation": text,
                    "question": c["check_question"], "source": source})


@app.route("/api/answer", methods=["POST"])
def answer():
    data = request.get_json(force=True)
    c = BY_ID.get(data.get("id"))
    text = (data.get("answer") or "").strip()
    if c is None:
        return jsonify({"error": "Unknown concept"}), 404
    if status_of(c) == "locked":
        return jsonify({"error": "Master the prerequisites first"}), 403
    if not text:
        return jsonify({"error": "Please write an answer first"}), 400

    before = {x["id"]: status_of(x) for x in CONCEPTS}
    score, feedback, source, follow_up = evaluate(c, text)
    verdict = verdict_for(score)
    STATE["best"][c["id"]] = max(STATE["best"].get(c["id"], 0), score)
    after = {x["id"]: status_of(x) for x in CONCEPTS}

    unlocked = [BY_ID[i]["name"] for i in after
                if before[i] == "locked" and after[i] == "available"]
    STATE["history"].append({
        "label": "Checkpoint " + str(len(STATE["history"]) + 1),
        "concept": c["name"], "score": score, "level": overall_level(),
    })

    result = {
        "score": score, "verdict": verdict, "feedback": feedback, "source": source, "follow_up": follow_up,
        "status": after[c["id"]], "unlocked": unlocked, "overall": overall_level(),
        "state_update": c["name"] + " concept is now \"" + after[c["id"]].capitalize() + "\" based on your last answer.",
    }
    if verdict == "confused":
        result["re_explanation"], _ = get_explanation(c, "analogy")
    elif verdict == "mastered":
        result["next_hint"] = "Nice work. Try the next unlocked concept."
    return jsonify(result)


@app.route("/api/reset", methods=["POST"])
def reset():
    STATE.clear()
    STATE.update(fresh_state())
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
