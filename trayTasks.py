import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qdarktheme
from connection import *
from PyQt6.QtCore import QDate, QTime, QDateTime, Qt
import datetime

# create api service and get tasks / lists
service = createService()
task_lists = getTaskListsFromAPI()
default_list = list(task_lists.values())[1]
global tasks
tasks = getTasksFromAPI(default_list)
# debugging
print(tasks)

# print lists to menus

print(QStyleFactory.keys())


def updateTasklists():
    task_lists = getTaskListsFromAPI()
    for item in task_lists.keys():
        action = tasklistsMenu.addAction(item)
        action.triggered.connect(
            lambda chk, item=item: taskListPressed(item))
        if task_lists.get(item) == default_list:
            action.setEnabled(False)


def updateTasks():
    global tasks
    tasks = getTasksFromAPI(default_list)
    print("Tasks updatet from tasklist: " + default_list)
    print("Tasks: ")
    print(tasks)
    try:
        for item in tasks.keys():
            action = tasksMenu.addAction(item)
            action.triggered.connect(
                lambda chk, item=item: taskPressed(item))
    except:
        not tasks
        print("No tasks!")


def taskPressed(item):
    print(item)
    try:
        print(tasks.get(item))
        # print(thisdict.get(p))
        finishTask(tasks.get(item), item, default_list)
    except:
        not tasks
        print("Task pressed but not in dictionary!")
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
    tasksMenu.addAction(add_task_menu)
    add_task_menu.triggered.connect(lambda: addNewTask(app))

    # refresh
    refresh.triggered.connect(lambda: refreshMenu())
    tasksMenu.addAction(refresh)

    # To quit the app
    quit.triggered.connect(app.quit)
    tasksMenu.addAction(quit)


def refreshMenu():
    tasksMenu.clear()
    tasklistsMenu.clear()

    updateTasklists()
    updateTasks()
    addControlsToMenu()


class addTaskWindow(QWidget):
    def __init__(self, parent=None):
        super(addTaskWindow, self).__init__(parent)
        # layout
        layout = QFormLayout()

        self.title_label = QLabel()
        self.title_label.setText("Titel")

        self.task_title = QLineEdit()

        self.task_description = QPlainTextEdit()
        layout.addRow(self.title_label, self.task_title)

        self.description_label = QLabel()
        self.description_label.setText("Description")

        layout.addRow(self.description_label, self.task_description)

        self.date_selector = QDateEdit(calendarPopup=True)
        now = QDate.currentDate()
        self.date_selector.setDate(now.currentDate())

        self.checkBox_date = QCheckBox()
        self.checkBox_date.setText("Date")
        self.checkBox_date.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        # self.checkBox_date.isChecked(True)

        layout.addRow(self.checkBox_date, self.date_selector)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.ok)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.cancel)

        # layout.addRow(self.btn_ok, self.btn_cancel)
        layout.addWidget(self.btn_cancel)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)
        self.setWindowTitle("Add Task")
        self.setWindowIcon(QIcon("check-mark-8-256.png"))
       

    def cancel(self):
        self.close()
        print("Cancel pressed")

    def adDate(self):
        self.dateedit = QDateEdit(calendarPopup=True)

    def ok(self):
        title = self.task_title.text()
        description = self.task_description.toPlainText()

        # , title, default_list, description, pydate
        # try:
        if self.checkBox_date.isChecked():
            date = self.date_selector.dateTime()
            pydate = date.toPyDateTime().isoformat()
            rfc_date = pydate + ".52Z"
            addNewTaskToAPI(title, default_list, description, rfc_date)

        else:
            addNewTaskToAPI(title, default_list, description)
        # except:
        #    pass
        self.close()
        refreshMenu()


def addNewTask(self=None):
   # self.window = traywindow.MainWindow()
   # self.window.show()

    ex = addTaskWindow()
    self.window = ex
    ex.show()

    # text, ok = QInputDialog.getText(self, 'input dialog', 'Is this ok?')


# create application
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
app.setStyleSheet(qdarktheme.load_stylesheet(custom_colors={"primary": "#D0BCFF"}))
# #4c8bf5 #blue

# Adding an icon
icon=QIcon("check-mark-8-256.png")

# Adding item on the menu bar
tray=QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Creating the options
tasksMenu=QMenu()
tasklistsMenu=QMenu()
tasklistsMenu.setTitle("Tasklists")
# Control Options
refresh=QAction("Refresh")
add_task_menu=QAction("Add Task")
quit=QAction("Quit")

# refresh.setEnabled(False)
# refresh.setCheckable(True)
tasksMenu.actions
refreshMenu()


tray.setContextMenu(tasksMenu)
app.exec()
