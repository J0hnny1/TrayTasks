from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qdarktheme
from connection import *

# create api service and get tasks / lists
service = createService()
task_lists = getTaskListsFromAPI()
default_list = list(task_lists.values())[0]
tasks = getTasksFromAPI(default_list)
# debugging
print(tasks)

# print lists to menus
def updateTasklists():
    task_lists = getTaskListsFromAPI()
    for item in task_lists.keys():
        action = tasklistsMenu.addAction(item)
        action.triggered.connect(
            lambda chk, item=item: taskListPressed(item))


def updateTasks():
    tasks = getTasksFromAPI(default_list)
    if not tasks:
        no = QAction("No Tasks")
        tasksMenu.addAction(no)
    else:
        for item in tasks.keys():
            action = tasksMenu.addAction(item)
            action.triggered.connect(
            lambda chk, item=item: taskPressed(item))


def taskPressed(item):
    print(item)
    print(tasks.get(item))
    # print(thisdict.get(p))
    finishTask(tasks.get(item), item, default_list)

    getTasksFromAPI(default_list)
    refreshMenu()
   # addControlsToMenu()

def taskListPressed(item):
    print("TaskList Pressed: " + task_lists.get(item))
    global default_list
    default_list = task_lists.get(item)
    refreshMenu()

def addControlsToMenu():
    tasksMenu.addSeparator()
    tasksMenu.addMenu(tasklistsMenu)

    # refresh
    refresh.triggered.connect(lambda: refreshMenu())
    tasksMenu.addAction(refresh)
    
    # To quit the app
    quit.triggered.connect(app.quit)
    tasksMenu.addAction(quit)

def refreshMenu():
    print("Def T ID: " + default_list)
    tasksMenu.clear()
    tasklistsMenu.clear()

    updateTasklists()
    updateTasks()
    addControlsToMenu()
   


# create application
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
app.setStyleSheet(qdarktheme.load_stylesheet())

# Adding an icon
icon = QIcon("check-mark-8-256.png")

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Creating the options
tasksMenu = QMenu()
tasklistsMenu = QMenu()
tasklistsMenu.setTitle("Tasklists")
# Control Options
refresh = QAction("Refresh")
quit = QAction("Quit")
# print tasks and lists to menu
# updateTasklists()
# updateTasks()

refreshMenu()

"""
refresh = QAction("Refresh")
refresh.triggered.connect(lambda: refreshMenu())
tasksMenu.addAction(refresh)
# To quit the app
quit = QAction("Quit")
quit.triggered.connect(app.quit)
tasksMenu.addAction(quit)

"""

tray.setContextMenu(tasksMenu)
app.exec()
