import flask, random, os, json
from flask import abort, render_template, request, make_response, session, url_for
try:
    from QUESTION_DATABASE import QUESTION_DATABASE
except ImportError:
    print("WARNING: Could not load QUESTION_DATABASE file! Proceeding with defaults.")
    QUESTION_DATABASE = {"hi":{"hi": "bye", "hi2": "bye3"}, "dd": {"hi": 4}}
app = flask.Flask(__name__)
app.secret_key = os.urandom(42)

class NopeError(Exception):
    pass

@app.route("/")
def Index():
    finish = """
<h1>Select a Qset.</h1>
<form action="Quiz">
<title>QUIZQUIZQUIZ</title>
"""
    for i in QUESTION_DATABASE.keys():
        finish += f"""
<input type="radio" name="qset" value="{i}">{i}
        """
    finish += """
<h1>Select the Amount of questions.</h1>
<input type="radio" name="q" value="inf">ALL<br>
<button type="submit">Transmit</button>
</form>
    """
    return finish

@app.route("/Quiz")
def Quiz():
    try:
        session['exist']
    except Exception as ename:
        try:
            session['options'] = {"qset": request.args.get("qset"),"q":request.args.get("q")}
            for i in list(session['options']):
                if session['options'][i] is None:
                    raise NopeError
            session['exist'] = True
            session['qset'] = {"load": {"What is the developer?": {"smart": "Ha!", "dumb": "Meanie"}}, "main":QUESTION_DATABASE[session['options']['qset']]}
            print(session['qset'])
            return list(session['qset']['main'])[0]
        except NopeError:
            abort(400)
        except Exception as ename:
            raise
    try:
        pos=random.choice(list(session['qset']['main']))
        item=f"pos:{session['qset']['main'][pos]}"
        del session['qset']['main'][pos]
    except IndexError:
        item = False
    if not item:
        return "All finished! Let's head back, okay?"
    print(session)
    hi = ""
    for i in list(session['qset']['main']):
        hi += i
    return hi#use render_template here
if __name__ == "__main__":
   app.run()
