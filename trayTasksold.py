# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START tasks_quickstart]
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import PySimpleGUIQt as sg

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']

functionsCreated = False

def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
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

    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    # tasklist hinzufügen
    #service.tasklists().insert(body={'title': 'Pls UwU'}).execute()

    # delete tasklist
    # service.tasklists().delete(tasklist='ZTRydkwzXzVvenZidVh1WA').execute()

    # add task
    service.tasks().insert(tasklist='ZUdyVV94ZmZPbmxqX05GaQ', body={'title': 'Tomodachi Game', 'notes': 'fake squid game', 'due': '2022-05-05T12:20:02.52Z'}).execute()
    # 2022-05-05T00:00:00.000Z

    

    # delete task
    # service.tasks().delete(tasklist='ZUdyVV94ZmZPbmxqX05GaQ',task='TV84ZGxDbC0zVnZNNTVDcQ').execute()

    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))

    printTasks(service)


def printTasks(service):
    tasks_result = service.tasks().list(tasklist='ZUdyVV94ZmZPbmxqX05GaQ').execute()

    tasks = tasks_result.get('items', [])

    print("tasks")
    for item in tasks:
        print(u'{0} ({1})'.format(item['title'], item['id']))
    functionsCreated = True
 
menu_def = ['My Menu Def', ['&Licht An', '&Licht Aus', 'Farbe', '&Maus', ['On::m', 'Off::m', 'Farbe::m'], '&Tastatur', ['On::t', 'Off::t', 'Farbe::t'], 'E&xit']]

tray = sg.SystemTray(menu=menu_def, filename='/home/jonathan/Applications/Icons/display-brightness-medium-symbolic.svg')


while True:  # The event loop
    menu_item = tray.read()
    # print(menu_item)
    if menu_item == 'Exit':
        break
    elif menu_item == 'Farbe':
        printTasks(service)
    # elif menu_item == 'Neu':
    


if __name__ == '__main__':
    main()
# [END tasks_quickstart]

