#!/usr/bin/python3
from datetime import datetime, timedelta, timezone
import pickle
import os.path
import re
import time
import logging
import webbrowser

try:
    logging.basicConfig(format="%(asctime)s %(message)s", level="INFO")
    logger = logging.getLogger()
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except:
    print(
        """Import dependencies failed. You need to run the following command:

        pip install -r requirements.txt
        
        """
    )
    exit()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CHECK_INTERVAL_MINUTES = 10


def getcreds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print(
                    """Visit this page and click "create credentials" to obtain a credentials.json file:
                https://developers.google.com/calendar/quickstart/python
                """
                )
                exit()
            creds = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            ).run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def getNextEvent(events):
    for event in events:
        title = event.get("summary", "<no summary>")
        logger.info(f"Inspecting event '{title}'")
        zoomlink = getzoomlink(event)
        if not zoomlink:
            logger.info(f"zoomlink not found, skipping")
            continue
        waittime = timeuntilstart(event)
        if waittime.total_seconds() < 0:
            logger.info(f"event has already started, skipping")
            continue
        return zoomlink, waittime
    else:
        logger.info(f"Checked {len(events)} events!")
        return "", timedelta(days=1)


def main():
    service = build("calendar", "v3", credentials=getcreds())

    while True:
        zoomlink, waittime = getNextEvent(getevents(service))
        if zoomlink and waittime.total_seconds() < CHECK_INTERVAL_MINUTES * 60:
            logger.info(f"zoom-linked event starting in {waittime}...")
            # connecting takes about seven seconds, so start connecting early
            time.sleep(waittime.total_seconds())
            logger.info(f"connecting now, link is {zoomlink}")
            webbrowser.open(zoomlink)
        else:
            logger.info(
                f"event is {waittime} away, will check again in {CHECK_INTERVAL_MINUTES} minutes."
            )
            time.sleep(CHECK_INTERVAL_MINUTES * 60)


def getevents(service, N=10):
    # Call the Calendar API
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    try:
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=N,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
    except Exception as e:
        print(e)
        return []

    print(f"Retrieved {len(events)} events.")
    return events


def getzoomlink(event):
    text = ""
    # logger.info(str(event))
    for field in [
        "location",
        "summary",
        "description",
        "hangoutLink",
        "conferenceData",
    ]:
        text += str(event.get(field, "")) + " "
    matches = re.findall(r"https://[A-Za-z0-9.-]+.zoom.us/j/[A-Za-z0-9?=]+", text)
    matches += re.findall(r"https://meet.google.com/[a-zA-Z0-9_-]+", text)
    return matches[0] if matches else None


def timeuntilstart(event):
    start = datetime.fromisoformat(
        event["start"].get("dateTime", event["start"].get("date"))
    )
    return start - datetime.now(timezone.utc)


if __name__ == "__main__":
    main()
