# SeatHistoryGeek
Pulling ticket prices and availability from SeatGeek to chart over time and see when is the best time to purchase tickets.


### Warning
SeatGeek has modified their API on `2024-05-16 18:42:00.000000+00:00` (as that is the last time I successfully made and interpreted a request to/from them).

This repo needs some [TLC](https://www.urbandictionary.com/define.php?term=TLC) to continue logging data...

## Developing

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/mattpopovich/SeatHistoryGeek)

If you have VS Code and Docker installed, click the above link to open VS Code and automatically install the *Dev Containers* extension (if needed), clone the source code into a container volume, and spin up a dev container for use.

## Logging Data
1. Obtain [SeatGeek API credentials](https://seatgeek.com/account/develop)
1. Store credentials in [`config.cfg`](/config.cfg)
1. Run `while true; do python3 main.py; sleep 3210; done`

## Visualizing Data
1. Log data via the instructions above
1. Run `python3 dash_example.py`
    - Go to the IP address specified in the logs (Ex. http://0.0.0.0:8050)
    - You should see a blank graph with a text box on top
      - If not, refresh (not sure why this doesn't work sometimes)
    - Click on the text box to then scroll (or type) to find the event of interest
