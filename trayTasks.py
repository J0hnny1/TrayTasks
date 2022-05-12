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

        
    #debugging
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
    
    
    

        
    #debugging
    #if not items:
    #    print('No task lists found.')
    #else:
    #    print('Task lists:')
    #    for item in items:
    #        print(u'{0} ({1})'.format(item['title'], item['id']))


#def createTray():
#    global menu_def
#    menu_def = ['My Menu Def', ['Task Lists', [taskListNames], taskNames,'Print Tasks', 'Exit']]
#    global tray
#    tray = sg.SystemTray(menu=menu_def, filename='/home/jonathan/Applications/Icons/display-brightness-medium-symbolic.svg')

def updateTray():
    tray.Update(menu=menu_def2)
    menu_item2 = tray.read()

createService()

    

printTaskLists()
printTasks()

menu_def = ['My Menu Def', [taskNames,'---','Task Lists', [taskListNames], 'Print Tasks','Debug 1', 'Exit']]
menu_def2 = ['My Menu Def', ['Task Lists', [taskListNames], taskNames,'Print Tasks','Debug 1','Debug 2', 'Exit']]
#global tray
tray = sg.SystemTray(menu=menu_def, data_base64=sg.DEFAULT_BASE64_ICON)


#tray.Close()

def whileLoop():
    global update
    update = False
    while update == False:  # The event loop
        menu_item = tray.read()
        # print(menu_item)
    

        for i in range(len(taskListNames)):
            if menu_item == taskListNames[i]:
                defaultTaskListID = tasklistIds[i]
                # printTasks()
                #print(defaultTaskListID)
            


        if menu_item == 'Exit':
            break
        elif menu_item == 'Print Tasks':
            printTasks()
            print(taskNames)
        elif menu_item == 'Debug 1':
            sg.SystemTray.Hide(self=tray)
            #update = True
            #updateTray()
        
        
        #
        #tray = sg.SystemTray(menu=menu_def, data_base64=sg.DEFAULT_BASE64_ICON)

first = True
if first == True:
    whileLoop()


if update == True:
        tray.Update(menu=menu_def2)
        sg.SystemTray.Update(menu=menu_def2)
        print("update?")
        update = False
        whileLoop()



        
