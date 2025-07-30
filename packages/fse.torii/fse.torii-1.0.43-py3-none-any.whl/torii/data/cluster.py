import inspect

import re

from torii.data.torii_object import ToriiObject

def fun2script(function):

    imports = ''

    lines = inspect.getsourcelines(function)
    index = 0
    for line in lines[0]:
        if index == 0:
            # parse the function header
            m = re.search('(^ *)def (.*)\((.*)\) *:', line)
            indent = '^' + m.group(1)
            function_name = m.group(2)
            function_args = m.group(3)

            # rewrite the function header without indent
            function_def = 'def {0}({1}):\n'.format(function_name, function_args)
        else:
            # remove the indents
            line = re.sub(indent, '', line)

            # check if the line is an import
            if re.match(' *import .*', line) or re.match(' *from .* import .*', line):
                imports += '{0}\n'.format(line.strip())

            else:
                function_def += line

        index += 1


    # copy the import we found in the function
    script = '{0}\n'.format(imports)

    # add missing import
    if 'PolicyExecutor' not in imports:
        script += '''
from torii.executor import PolicyExecutor
'''

    # add the function definition
    script += '\n{0}\n'.format(function_def)

    # add the main part
    script += '''
if __name__ == "__main__":

'''
    # we consider the first argument of the function as the executor
    # without arg, we assume the task is pasrsed in the funstion
    task = None
    if function_args is not None and function_args.strip():
        args = function_args.split(',')
        task = args[0]
        script += '''
    {0} = PolicyExecutor()
    
    '''.format(task)


    # call the function
    script += '''
    {0}({1})
    '''.format(function_name, task if task else '')

    return script



class Cluster(ToriiObject):

    def __init__(self, json, service=None, details=False):
        ToriiObject.__init__(self, json, service)

    def get_sched_option(self, name):
        """ Get the sched_option object based on its name """
        # get the option from the task
        option = next((option for option in self.scheduler.options
                       if option.label.lower().strip() == name.lower().strip()), None)

        return option

    def get_sched_option_names(self):
        """ Get the sched_option object based on its name """
        return [option.label.lower().strip() for option in self.scheduler.options]


    def set_policy(self, script):
        if callable(script):
            self.policyScript = fun2script(script)
        else:
            self.policyScript = script