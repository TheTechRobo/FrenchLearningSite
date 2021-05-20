import flask, random
from flask import abort, render_template, request
from QUESTION_DATABASE import QUESTION_DATABASE
app = flask.Flask(__name__)

class User:
    def __init__(self, options):
        self.options = options
    def GetQuestion(self):
        pos = random.choice(list(self.Questions))
        item = self.Questions[pos]
        Return = {pos:item}
        self.Questions.pop(pos)
        return Return
    def GenQuestion(self):
        print(f"Options: {self.options}")
        print(f"Qset: {self.options['qset']}")
        qset = self.options["qset"]
        self.Questions = QUESTION_DATABASE[self.options["qset"]]
    def LoaQuestion(self):
        questions = (
            {
                "What is the developer?": {"smart": "Ha!", "dumb": "Meanie"},
                "Is this website good?": {"y": "Thank you very much!", "meh": "Thanks...I guess.", "n": "D:"}
            }
        )
        item = random.choice(
            questions.keys()
        )
        return (
            item, questions[item]
        )
    def LenQuestion(self):
        return len(self.Questions)

@app.route("/")
def Index():
    return "hi!"

@app.route("/Quiz")
def Quiz():
    try:
        #todo cleanup
        person = User({"qset": request.args.get("qset"),"q":request.args.get("q")})
        times = request.args.get("q")
    except Exception:
        abort(400)
    person.GenQuestion()
    if times == "inf":
        times = person.LenQuestion()
    try: times = int(times)
    except Exception: abort(400)
    item = person.GetQuestion()
    return item
app.run()
