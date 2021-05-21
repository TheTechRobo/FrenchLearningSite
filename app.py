import flask, random
from flask import abort, render_template, request, make_response
try:
    from QUESTION_DATABASE import QUESTION_DATABASE
except ImportError:
    print("WARNING: Could not load QUESTION_DATABASE file! Proceeding with defaults.")
    QUESTION_DATABASE = {"hi":{"hi": "bye"}, "dd": {"hi": 4}}
app = flask.Flask(__name__)
Sessions = {}
class User:
    def __init__(self, options):
        self.options = options
    def GetQuestion(self):
        try:
            pos = random.choice(list(self.Questions))
        except IndexError:
            return False
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
        self.GenQuestion()
        if self.options["q"] == "inf":
            self.options["q"] = self.LenQuestion()
        self.options["q"] = int(self.options["q"])
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
    resp = make_response() #https://www.askpython.com/python-modules/flask/flask-cookies
    try:
        token = request.cookies.get("FrenchLearnerTtRSession:", None)
        if token is None:
            raise Exception
        Sessions[token]
    except Exception as ename:
        print("token not found.")
        token = str(random.randint(0,99999999999999999999))
        resp.set_cookie('FrenchLearnerTtRSession',token, domain='thetechrobo.pythonanywhere.com')
        try:
            Sessions[token] = User({"qset": request.args.get("qset"),"q":request.args.get("q")})
            Sessions[token].Proptions()
        except Exception as ename:
            abort(400)
    item = Sessions[token].GetQuestion()
    return f"{item}; Token: {token}" #use render_template here
if __name__ == "__main__":
   app.run()
