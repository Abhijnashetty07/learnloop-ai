t = open("app.py", encoding="utf-8-sig").read()
old = "STATE = fresh_state()"
assert old in t, "Could not find STATE line"
new = '''import uuid
from flask import g
from werkzeug.local import LocalProxy

SESSIONS = {}


def get_state():
    sid = request.cookies.get("sid") or getattr(g, "new_sid", None)
    if not sid:
        sid = uuid.uuid4().hex
        g.new_sid = sid
    if sid not in SESSIONS:
        SESSIONS[sid] = fresh_state()
    return SESSIONS[sid]


STATE = LocalProxy(get_state)


@app.after_request
def set_sid(resp):
    sid = getattr(g, "new_sid", None)
    if sid:
        resp.set_cookie("sid", sid, max_age=604800, samesite="Lax")
    return resp'''
open("app.py", "w", encoding="utf-8").write(t.replace(old, new, 1))
print("Session patch OK")
