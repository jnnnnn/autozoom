This python script will read your google calendar once per hour and automatically open scheduled zoom meetings when they start.

## Setup

0. Install python
1. Install dependencies: `pip install -r requirements.txt`
2. Enable your google calendar API and get `credentials.json` by following https://developers.google.com/calendar/quickstart/python

## Running

Run `autozoom.py`. It will run forever, opening zooms when they start. Kill it at any time by closing the console window.
