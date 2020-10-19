from .autozoom import *

event = {
    "attendees": [
        {
            "email": "jonathan.newnham@iress.com",
            "responseStatus": "accepted",
            "self": True,
        },
    ],
    "created": "2020-01-17T04:29:51.000Z",
    "creator": {"email": "andrew.coulter@iress.com"},
    "description": "\n"
    "──────────\n"
    "\n"
    "Bernadette Coyer is inviting you to a scheduled Zoom "
    "meeting. \n"
    "\n"
    "Topic: Bernadette Coyer's Personal Meeting Room\n"
    "\n"
    "Join from PC, Mac, Linux, iOS or Android: "
    "https://iress.zoom.us/j/93142918532?pwd=Um1vMklOdzNuNTZ3NHJJbWNsT3Axdz09\n"
    "\n"
    "Or iPhone one-tap :\n"
    "        United Kingdom: +441314601196,,7844249244#  or "
    "    International numbers available: "
    "https://iress.zoom.us/u/ab8ZGoIk7V",
    "end": {"dateTime": "2020-10-05T09:30:00+11:00"},
    "etag": '"3202868178846000"',
    "guestsCanModify": True,
    "htmlLink": "https://www.google.com/calendar/event?eid=MjhxNDY0Z29pb25jNXAyNm45Zzg5bGg1Y3FfMjAyMDEwMDRUMjIxNTAwWiBqb25hdGhhbi5uZXduaGFtQGlyZXNzLmNvbQ",
    "iCalUID": "28q464goionc5p26n9g89lh5cq_R20200927T231500@google.com",
    "id": "28q464goionc5p26n9g89lh5cq_20201004T221500Z",
    "kind": "calendar#event",
    "organizer": {"email": "andrew.coulter@iress.com"},
    "originalStartTime": {"dateTime": "2020-10-05T09:15:00+11:00"},
    "recurringEventId": "28q464goionc5p26n9g89lh5cq_R20200927T231500",
    "reminders": {"useDefault": True},
    "sequence": 1,
    "start": {"dateTime": "2020-10-05T09:15:00+11:00"},
    "status": "confirmed",
    "summary": "Ants Standup",
    "updated": "2020-09-30T02:48:09.423Z",
}


def test_zoomlink():
    assert (
        getzoomlink(event)
        == "https://iress.zoom.us/j/93142918532?pwd=Um1vMklOdzNuNTZ3NHJJbWNsT3Axdz09"
    )


def test_timeuntilstart():
    interval = timeuntilstart(event)
    assert isinstance(interval, timedelta)
