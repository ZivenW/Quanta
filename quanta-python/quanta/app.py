import os
import uuid

from flask import Flask, jsonify, render_template, request

import content
import engine

app = Flask(__name__)
QUESTIONS = {}  # qid -> soal lengkap (dengan kunci jawaban), hanya di memori server

SYSTEM = ("You are Muon, a friendly cat physics tutor inside a learning app. Answer in the student's language, "
          "in at most 4 short sentences. Give hints and the next step, never the final numeric answer. "
          "Stay on electricity and physics only.")
NOKEY = {"id": "Muon belum terhubung ke AI. Atur ANTHROPIC_API_KEY lalu jalankan ulang server. Sementara itu, coba petunjuk di atas ya.",
         "en": "Muon is not connected to the AI yet. Set ANTHROPIC_API_KEY and restart the server. For now, try the hints above."}
FAIL = {"id": "Muon lagi gagal menjawab. Coba lagi sebentar lagi.", "en": "Muon couldn't answer just now. Please try again shortly."}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/bab1")
def bab1():
    return jsonify(babs=content.BABS, ch=content.CHAPTERS)


@app.post("/api/question")
def question():
    d = request.get_json(force=True)
    p, n = d["p"], d["n"]
    c = engine.choose_concept(p, n, d.get("allowed", [0, 1, 2, 3]), d.get("phase", "prac"))
    q = content.make(c, engine.fuzzy_level(p[c]))
    qid = uuid.uuid4().hex[:10]
    QUESTIONS[qid] = q
    if len(QUESTIONS) > 800:
        QUESTIONS.pop(next(iter(QUESTIONS)))
    pub = {k: v for k, v in q.items() if k not in ("ans", "ex")}
    pub["qid"] = qid
    return jsonify(pub)


@app.post("/api/answer")
def answer():
    d = request.get_json(force=True)
    q = QUESTIONS.get(d.get("qid"))
    if not q:
        return jsonify(error="expired"), 410
    if q["kind"] == "mc":
        ok, shown = d["value"] == q["ans"], q["ans"]
    else:
        try:
            v = float(str(d["value"]).replace(",", "."))
        except ValueError:
            return jsonify(error="nan"), 400
        ok, shown = abs(v - q["ans"]) <= max(0.04 * abs(q["ans"]), 1e-9), q["ans"]
    return jsonify(ok=ok, ex=q["ex"], c=q["c"], ans=shown, p=engine.bkt_update(d["p"], ok, q["kind"]))


@app.post("/api/ask")
def ask():
    d = request.get_json(force=True)
    lang = d.get("lang", "id")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return jsonify(text=NOKEY.get(lang, NOKEY["id"]), live=False)
    try:
        import anthropic
        r = anthropic.Anthropic().messages.create(
            model=os.environ.get("QUANTA_MODEL", "claude-haiku-5-5"), max_tokens=250, system=SYSTEM,
            messages=[{"role": "user", "content": f"Question: {str(d.get('question', ''))[:400]}\nStudent says: {str(d.get('msg', ''))[:300]}"}])
        return jsonify(text=r.content[0].text, live=True)
    except Exception:
        return jsonify(text=FAIL.get(lang, FAIL["id"]), live=False)


if __name__ == "__main__":
    app.run(debug=True)
