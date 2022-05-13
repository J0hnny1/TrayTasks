from __future__ import print_function
from ast import Not
from fileinput import close
import os.path
from turtle import title, up
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import PySimpleGUIQt as sg

global defaultTaskListID


def createService():
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    global service
    service = build('tasks', 'v1', credentials=creds)


def printTaskLists():
    results = service.tasklists().list(maxResults=5).execute()
    global items
    items = results.get('items', [])
    global taskListNames
    taskListNames = []
    global tasklistIds
    tasklistIds = []
    for item in items:
        taskListNames.append(item['title'])
        tasklistIds.append(item['id'])

    global defaultTaskListID
    defaultTaskListID = tasklistIds[0]

    # debugging
    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))


def printTasks():
    if not defaultTaskListID:
        print("Select Task list")
    else:
        results = service.tasks().list(tasklist=defaultTaskListID).execute()
        global itemsTasks
        itemsTasks = results.get('items', [])
        global taskIDs
        taskIDs = []
        global taskNames
        taskNames = []
        for item in itemsTasks:
            if item['status'] == "needsAction":
                taskNames.append(item['title'])
                taskIDs.append(item['id'])

    if not taskNames:
        taskNames.append("No Tasks")
    # debugging
    # if not items:
    #    print('No task lists found.')
    # else:
    #    print('Task lists:')
    #    for item in items:
    #        print(u'{0} ({1})'.format(item['title'], item['id']))



def updateTray():
    printTasks()
    menu_def2 = ['My Menu Def', [taskNames, '---', 'Task Lists',[taskListNames], 'Refresh', 'Add Tasks', 'Exit']]
    tray.Update(menu=menu_def2)


def createWindow():
    sg.theme('Material2')
    layout = [[sg.Text('Enter Task Name')],[sg.Input()],[sg.Text('Enter Task Notes')],[sg.Input()], [sg.CalendarButton(button_text="Select Date")],[sg.OK()] ]
    global window
    window = sg.Window('Enter a number example', layout)

    event, values = window.read()
    global newTaskName, newTaskNotes
    newTaskName = values[0]
    newTaskNotes = values[1]
    #date = values[2]
    #print(date)
    window.close()

    b = values[0]
    if b == "":
        sg.popup_ok_cancel('Task needs a name')
        #sg.popup_error(title="Missing Task Name")
    else:
        service.tasks().insert(tasklist=defaultTaskListID, body={'title': values[0], 'notes': values[1]}).execute()


createService()

printTaskLists()
printTasks()

menu_def = ['My Menu Def', [taskNames, '---', 'Task Lists',[taskListNames], 'Refresh', 'Add Tasks', 'Exit']]
tray = sg.SystemTray(menu=menu_def)

global update
update = False
while update == False:  # The event loop
    menu_item = tray.read()
    
    #if windowExists == True:
    #    event, values = window.read()
        

    for i in range(len(taskListNames)):
        if menu_item == taskListNames[i]:
            defaultTaskListID = tasklistIds[i]
            updateTray()

    for i in range(len(taskNames)):
        if not taskNames[i]:
            print("NO tasks")
        elif menu_item == taskNames[i]:
            taskID = taskIDs[i]
            print(taskIDs[i])
            service.tasks().update(tasklist=defaultTaskListID, task=taskIDs[i], body={'status': 'completed', 'id': taskIDs[i]}).execute()
            updateTray()

    if menu_item == 'Exit':
        break
    elif menu_item == 'Refresh':
        updateTray()
        
    elif menu_item == 'Add Tasks':
        createWindow()
        #name = sg.PopupGetText
        #name = sg.PopupGetText(message="Enter Task Name")
        #print(newTaskName)
        #print(newTaskNotes)
        #updateTray()


