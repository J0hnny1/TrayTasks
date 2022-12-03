# TrayTasks
Simple python app that uses Google Tasks API and creates a System Tray icon to add, see and remove tasks.

![traytasks menu](https://user-images.githubusercontent.com/64163472/205461313-1b056309-87bf-4386-a99e-66e1a80e2e01.png)
![trayTasks add taskpng](https://user-images.githubusercontent.com/64163472/205461119-99a059dc-7deb-4914-ae2b-f9e1b0aa9b7d.png)

# Installation
Clone the repository.
## Google Tasks api
1. go to https://console.cloud.google.com/ and create a new Project
2. activate the google tasks api
3. go to credentials, select "create credentials" and choose "OAuth client ID"
4. choose application type and name
5. download .json, rename it to credentials.json and move it to the project directory

## Python
* run `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib PyQt6 pyqtdarktheme`
* run trayTasks.py

# Known Issues
* on linux some systray implementations force the use of gtk. With gtk the entries can not be updated leading to a crash 
