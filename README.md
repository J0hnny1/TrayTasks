# TrayTasks
Simple python app that uses Google Tasks API and creates a System Tray icon to add, see and remove tasks.

# Installation
Clone the repository.
## Google Tasks api
1. go to https://console.cloud.google.com/ and create a new Project
2. activate the google tasks api
3. go to credentials, select "create credentials" and choose "OAuth client ID"
4. choose application type and name
5. download .json, rename it to credentials.json and move it to the project directory

## Python
* run `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pysimpleguiqt`
* run trayTasks.py

# Known Issues
* script can not run if empty tasks are in a tasklist
* on linux some systray implementations force the use of gtk. With gtk the entries can not be updated leading to a crash 
