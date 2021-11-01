import sys
import os

tasks_path = os.path.realpath(os.path.join(__file__, r'..\tasks'))
TASK_DIRS = os.environ.get('TASKSTACK_TASK_DIRS')

if TASK_DIRS is None:
    TASK_DIRS = ''

task_dirs = TASK_DIRS.split(';')

if os.path.exists(tasks_path) and not tasks_path in task_dirs:
    task_dirs.append(tasks_path)

TASK_DIRS = ';'.join(task_dirs)
os.environ['TASKSTACK_TASK_DIRS'] = TASK_DIRS 

import core; reload(core)
# import ui; reload(ui) # 常にimportはエラーになる可能性がある