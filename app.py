import flask, random
from flask import abort, render_template, request
try:
    from QUESTION_DATABASE import QUESTION_DATABASE
except ImportError:
    print("WARNING: Could not load QUESTION_DATABASE file! Proceeding with defaults.")
    QUESTION_DATABASE = {"hi":{"hi": "bye"}}
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
    def Proptions(self):
        if self.options["q"] == "inf":
            self.options["q"] = self.LenQuestion()
        self.options["q"] = int(self.options["q"])
        self.GenQuestion()
        self.ElapsedTimes = 0
        self.Score = 0
        self.MissedQuestions = []
        self.GoodQuestions = []
        self.Feedback = {}

@app.route("/")
def Index():
    return "hi!"

@app.route("/Quiz")
def Quiz():
    try:
        person = User({"qset": request.args.get("qset"),"q":request.args.get("q")})
        person.Proptions()
    except Exception: abort(400)
    item = person.GetQuestion()
    return item #use render_template here
app.run()
