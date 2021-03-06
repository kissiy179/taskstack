# -*- coding: utf-8 -*-
from collections import OrderedDict
import maya.cmds as cmds
import pymel.core as pm
import taskstack.core.task as task

class ExecuteScriptTask(task.Task):
    '''
    記述したスクリプトを実行するタスク
    maya.cmds(cmds), pymel.core(pm)を使用可能
    '''
    
    def get_default_parameters(self):
        return OrderedDict((
            ('Script', 'print(cmds.ls(sl=True))'),
        ))

    def get_parameter_types(self):
        parameter_types = super(ExecuteScriptTask, self).get_parameter_types()
        parameter_types['Script'] = 'multi_line_str'
        return parameter_types
        
    def execute(self):
        super(ExecuteScriptTask, self).execute()
        parameters = self.get_parameters()
        script = parameters.get('Script')
        exec(script)