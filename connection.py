import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

global defaultTaskListID

def createService():
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    credentials = None

    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    global service
    service = build('tasks', 'v1', credentials=credentials)
    return service


def getTaskListsFromAPI(tasklists_dict=None):
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
        tasklists_dict = {
            item['title']: item['id']
        }

    for i in range(len(taskListNames)):
        tasklists_dict[taskListNames[i]] = tasklistIds[i]

    # from_tasklist=tasklistIds[0]
    setDefTaskList(tasklistIds[0])

    # debugging
    if not items:
        print('No task lists found.')

    return tasklists_dict


def getTasksFromAPI(fromTaskList, tasks_dict=None):
    global defaultTaskListID
    results = service.tasks().list(tasklist=fromTaskList).execute()
    global itemsTasks

    itemsTasks = results.get('items', [])
    global taskIDs
    taskIDs = []
    global taskNames
    taskNames = []

    for item in itemsTasks:
        if item['status'] == "needsAction":
            if item['title'] == "":
                taskListNames.append("Nameless Task")
                taskIDs.append(item['id'])
            else:
                tasks_dict = {
                    item['title']: item['id']
                }
                taskNames.append(item['title'])
                taskIDs.append(item['id'])

    for i in range(len(taskNames)):
        tasks_dict[taskNames[i]] = taskIDs[i]

    return tasks_dict


def setDefTaskList(tasklist_set):
    global defaultTaskListID 
    defaultTaskListID = tasklist_set

def getDefTaskList():
    global defaultTaskListID
    return defaultTaskListID

def finishTask(task_id, task_title, task_list):
 service.tasks().update(tasklist=task_list, task=task_id,
                        body={'status': 'completed', 'id': task_id, 'title': task_title}).execute()
