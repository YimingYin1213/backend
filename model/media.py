"""Media Submissions model (Luke Sanders, issue #14).

All media data lives here: the table, the allowed types, the seed row, and the
CPT procedure. The API file only calls these functions.

How it works:
- Someone submits a media title and type.
- validateSubmission() checks for a missing title, an invalid type, and a
  duplicate title.
- Valid submissions are saved with status "pending" until an admin reviews them.
"""
from datetime import datetime
from __init__ import app, db

ALLOWED_TYPES = ["Photo", "Video", "Article"]
PENDING = "Pending review"


class MediaSubmission(db.Model):
    """One media item someone wants added to the Safe Passage Heals site."""
    __tablename__ = 'media_submissions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, media_type):
        self.title = title
        self.media_type = media_type
        self.status = "pending"

    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "media_type": self.media_type,
            "status": self.status,
        }


# ---------- CPT procedure (sequencing + selection + iteration + list) ----------
def validateSubmission(queue, title, mediaType):
    """queue: list of titles already pending. Returns a result message.
    Adds the title to queue when it is valid."""
    allowedTypes = ALLOWED_TYPES
    typeFound = False
    if title == "":                          # selection
        return "Missing title"
    for allowed in allowedTypes:             # iteration
        if allowed == mediaType:
            typeFound = True
    if not typeFound:                        # selection (Boolean)
        return "Invalid media type"
    for item in queue:                       # iteration
        if item == title:                    # exact match (case-sensitive)
            return "Duplicate submission"
    queue.append(title)
    return PENDING


def getPendingTitles():
    """The queue the procedure checks against: titles still pending review."""
    return [s.title for s in MediaSubmission.query.filter_by(status="pending").all()]


def submitMedia(title, mediaType):
    """Calls the CPT procedure, then saves the submission if it passed."""
    queue = getPendingTitles()
    result = validateSubmission(queue, title, mediaType)
    if result != PENDING:
        return {"accepted": False, "result": result}
    submission = MediaSubmission(title, mediaType)
    db.session.add(submission)
    db.session.commit()
    return {"accepted": True, "result": result, "submission": submission.read()}


def getMediaPage():
    """What the frontend needs: allowed types for the form and the pending list."""
    pending = MediaSubmission.query.filter_by(status="pending").order_by(MediaSubmission.id).all()
    return {"allowed_types": ALLOWED_TYPES, "pending": [s.read() for s in pending]}


# ---------- Seed data ----------
SEED = [("Community Flyer", "Photo")]   # matches test case 4 in issue #14


def initMedia():
    """Create the table and add seed rows (skips ones already there)."""
    with app.app_context():
        db.create_all()
        for title, media_type in SEED:
            if not MediaSubmission.query.filter_by(title=title).first():
                db.session.add(MediaSubmission(title, media_type))
        db.session.commit()
