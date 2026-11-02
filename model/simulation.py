"""Support Simulation model (issue #8), v2.

All simulation data lives here: the tables, the seed questions, the needs
they point to, and the CPT procedure. The API file only calls these functions.

How it works:
- Each Scenario is a low-stakes, hypothetical question.
- Each Choice adds points to one need (or none).
- findNeed() totals the points and returns the top need.
- Each Need knows where to send the person next.
"""
from sqlalchemy.exc import IntegrityError
from __init__ import app, db

# Always shown on the page, whatever the result
HOTLINE = {
    "name": "National Domestic Violence Hotline",
    "phone": "1-800-799-7233",
    "text": "Text START to 88788",
    "url": "https://www.thehotline.org/",
}


class Need(db.Model):
    """A kind of support someone might need, and where to send them."""
    __tablename__ = 'sim_needs'

    key = db.Column(db.String(32), primary_key=True)  # e.g. "safety"
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link_label = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(512), nullable=False)

    def __init__(self, key, title, message, link_label, link_url):
        self.key = key
        self.title = title
        self.message = message
        self.link_label = link_label
        self.link_url = link_url

    def read(self):
        return {
            "need": self.key,
            "title": self.title,
            "message": self.message,
            "link_label": self.link_label,
            "link_url": self.link_url,
        }


class Scenario(db.Model):
    """One hypothetical question."""
    __tablename__ = 'sim_scenarios'

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, unique=True, nullable=False)
    # One scenario has many choices; deleting a scenario deletes its choices
    choices = db.relationship('Choice', backref='scenario', cascade='all, delete-orphan')

    def __init__(self, prompt):
        self.prompt = prompt

    def read(self):
        # Needs and points are NOT sent to the browser
        return {
            "id": self.id,
            "prompt": self.prompt,
            "choices": [c.read() for c in self.choices],
        }


class Choice(db.Model):
    """One possible answer. need=None means 'no concern'."""
    __tablename__ = 'sim_choices'

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('sim_scenarios.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    need = db.Column(db.String(32), db.ForeignKey('sim_needs.key'), nullable=True)
    points = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, text, need, points):
        self.text = text
        self.need = need
        self.points = points

    def read(self):
        return {"id": self.id, "text": self.text}


# ---------- CPT procedure (sequencing + selection + iteration + list) ----------
def findNeed(choices):
    """choices: list of Choice rows the person picked. Returns (top need, totals)."""
    totals = {"safety": 0, "connection": 0, "rebuilding": 0, "recognizing": 0}
    for choice in choices:                       # iteration
        if choice.need in totals:                # selection (skips "no concern")
            totals[choice.need] = totals[choice.need] + choice.points
    top = "recognizing"                          # default when nothing stands out
    for need in totals:                          # iteration
        if totals[need] > totals[top]:           # selection
            top = need
    return top, totals


def getSimulation():
    scenarios = Scenario.query.order_by(Scenario.id).all()
    return {"scenarios": [s.read() for s in scenarios], "hotline": HOTLINE}


def routeSubmission(choice_ids):
    """Look up the picked choices, find the top need, return where to go."""
    chosen = [db.session.get(Choice, cid) for cid in choice_ids]
    chosen = [c for c in chosen if c is not None]
    if not chosen:
        return None
    top, totals = findNeed(chosen)
    result = db.session.get(Need, top).read()
    result["totals"] = totals
    result["hotline"] = HOTLINE
    return result


# ---------- Seed data ----------
NEEDS = [
    ("recognizing", "Learning the signs",
     "Knowing the signs of an unhealthy relationship helps, whether it's about you "
     "or someone you care about.",
     "Warning signs of abuse",
     "https://www.thehotline.org/identify-abuse/domestic-abuse-warning-signs/"),
    ("safety", "Feeling safe",
     "Some of your answers suggest home might not always feel safe. A safety plan is a "
     "private, step-by-step way to prepare. Advocates can help you make one, any time.",
     "Make a safety plan",
     "https://www.thehotline.org/plan-for-safety/"),
    ("connection", "Staying connected",
     "Some of your answers suggest you might feel cut off from people. Safe Passage "
     "Heals runs weekly counseling and support groups, so you don't have to do this alone.",
     "Safe Passage Heals counseling and support groups",
     "https://safepassageheals.org/our-services"),
    ("rebuilding", "Rebuilding on your own terms",
     "Some of your answers point to money or housing. Safe Passage Heals offers shelter, "
     "emergency resources, and financial literacy and career programs.",
     "Safe Passage Heals shelter and programs",
     "https://safepassageheals.org/our-services"),
]

# (prompt, [(choice text, need or None, points), ...])
SCENARIOS = [
    ("Plans change last minute and dinner is late. At home, that usually means...", [
        ("No big deal. We figure it out.", None, 0),
        ("Someone gets annoyed, but it passes.", "recognizing", 1),
        ("I rush to fix it so nobody gets upset.", "recognizing", 2),
        ("I get nervous about how someone will react.", "safety", 2),
    ]),
    ("When did you last hang out with a friend, just because?", [
        ("This week.", None, 0),
        ("A few weeks ago.", "connection", 1),
        ("I honestly can't remember.", "connection", 2),
        ("Going out usually starts an argument.", "recognizing", 2),
    ]),
    ("After a really bad day, who would you text first?", [
        ("A friend or family member.", None, 0),
        ("Nobody. I'd keep it to myself.", "connection", 2),
        ("I'd want to, but someone checks my phone.", "safety", 2),
    ]),
    ("You need $200 tomorrow for something important. You would...", [
        ("Use my own money or card.", None, 0),
        ("Have to ask someone and explain why.", "rebuilding", 1),
        ("Probably not be able to get it.", "rebuilding", 2),
        ("Not be allowed to. Someone else controls the money.", "rebuilding", 2),
    ]),
    ("How do you usually feel walking through your front door?", [
        ("Relaxed.", None, 0),
        ("Depends on the day.", "recognizing", 1),
        ("On edge, like I'm bracing for something.", "safety", 2),
    ]),
    ("If you had to stay somewhere else for a few nights, you would go to...", [
        ("A friend's or family member's place.", None, 0),
        ("I'm not sure where.", "rebuilding", 1),
        ("There's nowhere I could go.", "rebuilding", 2),
        ("I'd be by myself. There's no one to call.", "connection", 2),
    ]),
    ("After an argument, things usually...", [
        ("Get talked through.", None, 0),
        ("Go quiet for a while.", "recognizing", 1),
        ("Turn into apologies and gifts, then it happens again.", "recognizing", 2),
        ("Leave me feeling scared.", "safety", 2),
    ]),
]


def initSimulation():
    """Create tables and add seed data (skips rows already there)."""
    with app.app_context():
        db.create_all()
        for key, title, message, link_label, link_url in NEEDS:
            if db.session.get(Need, key) is None:
                db.session.add(Need(key, title, message, link_label, link_url))
        db.session.commit()
        for prompt, choices in SCENARIOS:
            if Scenario.query.filter_by(prompt=prompt).first():
                continue
            scenario = Scenario(prompt)
            for text, need, points in choices:
                scenario.choices.append(Choice(text, need, points))
            db.session.add(scenario)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
