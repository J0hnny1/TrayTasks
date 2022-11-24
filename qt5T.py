from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qdarktheme
from connection import *

service = createService()
task_lists = printTaskLists()
# print("lists: ")
# print(task_lists)
default_list = list(task_lists.values())[0]
# print("Def: " + default_list)
tasks = printTasks()
print(tasks)

def updateTasklists():
    for item in task_lists.keys():
        action = tasklistsMenu.addAction(item)
        action.triggered.connect(
            lambda chk, item=item: taskPressed(item))


def updateTasks():
    for item in tasks.keys():
        action = tasksMenu.addAction(item)
        action.triggered.connect(
            lambda chk, item=item: taskPressed(item))


# create service


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
# menu.addSeparator()

lists = QListView()

createService()
printTaskLists()
updateTasklists()
printTasks(default_list)
updateTasks()



testItems = ['itemA', 'itemB', 'itemC']


def taskPressed(p):
    print(p)
    print(tasks.get((p)))
    # print(thisdict.get(p))
    finishTask()

    printTasks()
    updateTasks()


for item in testItems:
    action = tasksMenu.addAction(item)
    action.triggered.connect(
        lambda chk, item=item: taskPressed(item))

tasksMenu.addSeparator()
tasksMenu.addMenu(tasklistsMenu)
refresh = QAction("Refresh")

tasksMenu.addAction(refresh)
# To quit the app
quit = QAction("Quit")
quit.triggered.connect(app.quit)
tasksMenu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(tasksMenu)

app.exec()
