import os
import imp
import abc
from .task import Task

task_dirs = os.environ.get('TASKSTACK_TASK_DIRS')
PYTHON_EXTENSIONS = ('.py', )

def get_task_classes():
    task_classes = {}

    for task_dir in task_dirs.split(';'):
        for dirpath, dirnames, filenames in os.walk(task_dir):
            for filename in filenames:
                basename, ext = os.path.splitext(filename)

                if not ext in PYTHON_EXTENSIONS:
                    continue

                filepath = os.path.join(dirpath, filename)
                module = imp.load_source(basename, filepath)

                for name, obj in module.__dict__.items():
                    if not isinstance(obj, type):
                        continue

                    if not Task in obj.__mro__:
                        continue

                    task_classes[obj.__name__] = obj

    return task_classes

class TaskList(object):
    
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.__parameters = {}
        self.__tasks = []
        self.__task_classes = get_task_classes()

    def get_parameters(self):
        return self.__parameters

    def set_parameters(self, **parameters):
        task_classes = get_task_classes()

        for task_name, task_parameters in parameters.items():
            self.add_task(task_name=task_name, parameters=task_parameters)

    def add_task(self, task=None, task_name='', parameters={}):
        if not task:
            task_class = self.__task_classes.get(task_name)

            if not task_class:
                print('TaskStackError: Task [{}] does not exist.'.format(task_name))
                return

            task = task_class()

        if not isinstance(parameters, dict):
            print('TaskStackError: Parameters must be dictionary.'.format(task_name))
            return

        task.set_parameters(**parameters)
        self.__tasks.append(task)

    def execute(self):
        for task in self.__tasks:
            task.execute()