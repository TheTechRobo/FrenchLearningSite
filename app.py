import flask, random, os, json
from flask import abort, render_template, request, make_response, session
try:
    from QUESTION_DATABASE import QUESTION_DATABASE
except ImportError:
    print("WARNING: Could not load QUESTION_DATABASE file! Proceeding with defaults.")
    QUESTION_DATABASE = {"hi":{"hi": "bye"}, "dd": {"hi": 4}}
app = flask.Flask(__name__)
app.secret_key = os.urandom(42)

@app.route("/")
def Index():
    return "hi!"

@app.route("/Quiz")
def Quiz():
    try:
        session['exist']
    except Exception as ename:
        try:
            session['options'] = {"qset": request.args.get("qset"),"q":request.args.get("q")}
            session['exist'] = True
            session['qset'] = {"load": {"What is the developer?": {"smart": "Ha!", "dumb": "Meanie"}}, "main":QUESTION_DATABASE[session['options']['qset']]}
            print(session['qset'])
        except Exception as ename:
            abort(400)
    try:
        pos=random.choice(list(session['qset']['main']))
        item=f"pos:{session['qset']['main'][pos]}"
        del session['qset']['main'][pos]
    except IndexError:
        item = False
    if not item:
        return "All finished! Let's head back, okay?"
    print(session)
    return f"{item}" #use render_template here
if __name__ == "__main__":
   app.run()
