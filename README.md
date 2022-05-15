# TrayTasks
Simple python app that uses Google Tasks API and creates a System Tray icon to add, see and remove tasks.


# Known Issues
* script can not run if empty tasks are in a tasklist
* on linux some systray implementations force the use of gtk. With gtk the entries can not be updated leading to a crash 
