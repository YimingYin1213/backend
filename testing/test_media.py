"""Tests for validateSubmission (Luke Sanders, issue #14).

Run from the backend folder:  python testing/test_media.py
Tests the procedure directly, so no server or database is needed.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.media import validateSubmission

# (description, queue, title, mediaType, expected result)
TESTS = [
    ("1. valid submission",  ["Community Flyer"], "Workshop Recap",  "Photo",   "Pending review"),
    ("2. missing title",     ["Community Flyer"], "",                "Photo",   "Missing title"),
    ("3. invalid type",      ["Community Flyer"], "New Workshop",    "Music",   "Invalid media type"),
    ("4. duplicate title",   ["Community Flyer"], "Community Flyer", "Photo",   "Duplicate submission"),
    ("5. empty queue",       [],                  "New Resource",    "Article", "Pending review"),
    ("6. capitalization",    ["Community Flyer"], "community flyer", "Photo",   "Pending review"),
]

passed = 0
for name, queue, title, media_type, expected in TESTS:
    actual = validateSubmission(list(queue), title, media_type)
    ok = actual == expected
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {name}: got '{actual}', expected '{expected}'")
print(f"\n{passed}/{len(TESTS)} passed")
# Test 6 shows the first version compares titles exactly, so different
# capitalization is NOT caught as a duplicate (the issue's planned follow-up).
