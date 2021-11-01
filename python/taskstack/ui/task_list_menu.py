from pprint import pprint
from functools import partial
from mayaqt import maya_base_mixin, QtCore, QtWidgets
from . import WIDGET_TABLE
import qtawesome as qta
from ..core import task_list
from ..core import task
close_icon = qta.icon('fa5s.clipboard-list', color='lightgray')

class TaskListMenu(QtWidgets.QMenu):

    triggered = QtCore.Signal(task.Task)

    def __init__(self, *args, **kwargs):
        super(TaskListMenu, self).__init__(*args, **kwargs)
        self.setTearOffEnabled(True)
        self.setTitle('Tasks')
        task_classes = task_list.get_task_classes()
        task_class_names = [cls.__name__ for cls in task_classes.values()]
        max_task_class_name_lens = [len(task_class_name) for task_class_name in task_class_names]
        max_task_class_name_len = max(max_task_class_name_lens) if max_task_class_name_lens else 0
        lbls = ['{}: {}'.format(task_class_names[i].ljust(max_task_class_name_len), task_class.get_doc(first_line_only=True)) for i, task_class in enumerate(task_classes.values())]

        for i, lbl in enumerate(lbls):
            action = QtWidgets.QAction(close_icon, lbl, self)
            task_class = task_classes.values()[i]
            
            if not task_class.is_display_in_list():
                continue

            action.triggered.connect(partial(self.trigger, task_class))
            self.addAction(action)

        if not lbls:
            action = QtWidgets.QAction('No Tasks...', self)
            self.addAction(action)

    def trigger(self, task_name):
        self.triggered.emit(task_name)