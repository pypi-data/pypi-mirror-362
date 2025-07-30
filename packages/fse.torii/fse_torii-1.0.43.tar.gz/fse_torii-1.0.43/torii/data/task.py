import copy
import sys

from collections.abc import Iterable

from torii.exception import ToriiException
from torii.data.torii_object import ToriiObject, Struct


class Task(ToriiObject):

    STATUS = ['REGISTERED', 'RUNNING', 'PAUSED', 'WAITING', 'SUBMITTING', 'SCHEDULING', 'UNKNOWN', 'FINISHED', 'FAILED', 'CANCELLED']
    ACTIVE_STATUS = ['REGISTERED', 'RUNNING', 'PAUSED', 'WAITING', 'SUBMITTING', 'SCHEDULING', 'UNKNOWN']
    COMPLETE_STATUS = ['FINISHED', 'FAILED', 'CANCELLED']
    FAILURE_STATUS = ['FAILED', 'CANCELLED']

    def __init__(self, json={}, service=None):
        ToriiObject.__init__(self, json, service)

        self._cluster_obj = None
        self._last_record_step = None

    def __str__(self):
        """ String converter """
        if self.num:
            return 'task {0}'.format(self.num)
        else:
            return 'new task'

    @property
    def step(self):
        if hasattr(self, 'runInfos') and hasattr(self.runInfos, 'step'):
            return self.runInfos.step
        else:
            return None

    @classmethod
    def status_equal(cls, status, ref_status):
        if not status or not ref_status:
            return False
        elif isinstance(ref_status, Iterable):
            return status in ref_status
        else:
            return status == ref_status
        pass

    def is_status(self, status, refresh=False):

        """
        Tells if the task status correspond to a given status or list of status
        :param refresh:

        :return True if the task is active
        """
        if refresh:
            self.refresh()

        return Task.status_equal(self.status, status)

    def is_active(self, refresh = False):
        return self.is_status(Task.ACTIVE_STATUS, refresh=refresh)

    def is_complete(self, refresh = False):
        return self.is_status(Task.COMPLETE_STATUS, refresh=refresh)

    def wait(self, period=None, timeout=None, status=COMPLETE_STATUS):
        return self._service.wait(task=self, period=period, timeout=timeout, status=status)

    def _get_input(self, name):
        """ Get the input object based on its name """
        try:
            input = next(input for input in self.inputs if input.name == name)
        except:
            raise ToriiException('Cannot find input {0} in {1}'.format(name, self)).with_traceback(sys.exc_info()[2])

        return input

    def _get_output(self, name):
        """ Get the output object based on its name """
        try:
            output = next(output for output in self.outputs if output.name == name)
        except:
            raise ToriiException('Cannot find output {0} in {1}'.format(name, self)).with_traceback(sys.exc_info()[2])

        return output

    def clear_input(self, name):
        """
        Clear the value or the file list of an input

        :param name: the name of the input
        :return:
        """
        input = self._get_input(name)
        delattr(input, 'value')
        delattr(input, 'files')

    def set_input(self, name, value=None, path=None, server=None, append=True, link=False):
        """
        Set an input value based on its name

        :param name: the name of the input
        :param value: the value to set
        :param path:
        :param server:
        """
        input = self._get_input(name)

        if input.type == 'file':
            if isinstance(value, list):
                setattr(input, 'files', value)
            else:
                if isinstance(value, Struct):
                    file = value
                elif path:
                    # prepare the file description based on path and server
                    file = Struct({
                        'action': 'LINK' if link else 'COPY',
                        'path': path,
                        'server': server.ref if isinstance(server, ToriiObject) else server
                    })
                else:
                    raise ToriiException('Cannot set input \'{0}\' ad payload'.format(name))


                # append or reset the file list
                if append and hasattr(input, 'files') and input.files is not None:
                    input.files.append(file)
                else:
                    setattr(input, 'files', [file])

        elif input.type != "file" and value is not None:
            # careful value attribute may not exist
            setattr(input, 'value', value)
        else:
            raise ToriiException("Parameters does not match the input type")

    def get_input(self, name):
        """
        Get an input value based on its name

        :param name: the name of the input 
        :return: the value
        """
        input = self._get_input(name)\

        if input.type == 'file' and hasattr(input, 'files'):
            return input.files
        elif hasattr(input, 'value'):
            return input.value
        else:
            return None

    def map_input(self, name, task=None, input=None, output=None, mapping=None):
        """
        Map an input value to another task input of output
        :param name:    the input to map
        :param task:    the previous task to map from
        :param input:   the input of the previous task
        :param output:  the output of the previous task
        :param mapping: the raw mapping formula (for complex mapping)
        :return:
        """
        from_input = self._get_input(name)

        if isinstance(task, Task) or isinstance(task, str):
            id = task if isinstance(task, str) else task.id
            if input:
                task._get_input(input)
                from_input.mapping = id + ':' + input
            elif output:
                #task._get_output(output)
                from_input.mapping = id + ':' + output
            else:
                raise ToriiException('Bad payload, missing input/output name')
        elif mapping:
            from_input.mapping = mapping
        else:
            raise ToriiException('Bad payload, missing task + input/output name or a mapping formula')


    def clear_dependencies(self):
        """
        Clear the list of dependencies of the task
        """
        self.conditions = []

    def get_dependencies(self):
        """
        Get the list of dependencies of the task
        """
        return [condition for condition in self.conditions if condition.type == 'dependency']

    def add_dependency(self, task=None, criterion='AFTER_SUCCESS', orMode=False, keepEnvironment=True):
        """
        Add a dependency on one or several tasks
        :param task: the task we depend on
        :param criterion: the validity criterion
        :param orMode: is the dependency necessary or sufficient
        :param keepEnvironment: does the task inherit the context from this dependency
        """

        # we can add several dependencies at once
        if isinstance(task, list):
            for t in task :
                self.add_dependency(t, criterion, orMode, keepEnvironment)

            return
        elif isinstance(task, ToriiObject):
            task = task.ref

        valid_criteria = ['AFTER_ANY', 'AFTER_SUCCESS', 'AFTER_FAILED', 'IN_PARALLEL']
        if criterion not in valid_criteria:
            raise ToriiException('Bad parameter, the criterion must be in : {0}'.format(" ".join(valid_criteria)))
        elif not isinstance(task, Struct):
            raise ToriiException('Bad parameter, the task is invalid')

        condition = Struct({
            'type': 'dependency',
            'taskReference': task,
            'criterion': criterion,
            'keepEnvironment': keepEnvironment,
            'orMode': orMode
        })
        self.conditions.append(condition)

    def get_output(self, name):
        """
        Get an output value based on its name

        :param name: the name of the output 
        :return: the value
        """
        return self._get_output(name).value

    def set_context(self, name, value):
        """
        Set a context value

        :param name: the context property
        :param value: the value to set
        """

        # careful value attribute may not exist
        setattr(self.context, name, value)

    @property
    def cluster_obj(self):
        """
        Get the cache cluster object
        :return:
        """
        if self.cluster is None:
            raise ToriiException('Cluster is not defined on {0}'.format(self))

        if self._cluster_obj is None or self._cluster_obj.id != self.cluster.id:
            self._cluster_obj = self._service._torii.clusters.get(self.cluster.id)

        return self._cluster_obj

    @property
    def sched_options(self):
        if not hasattr(self, 'schedOptions') or self.schedOptions is None:
            self.schedOptions = []

        return self.schedOptions


    def _get_sched_option(self, name):
        """ Get the sched_option object based on its name """
        option = None

        # get the option from the task
        if self.sched_options:
            option = next((option for option in self.sched_options
                           if option.label.lower().strip() == name.lower().strip()), None)

        return option


    def clear_sched_options(self, name):
        """
        Clear the value or the file list of an sched_option

        :param name: the name of the sched_option
        :return:
        """
        self.schedOptions = [option for option in self.sched_options
                             if option.label.lower().strip() != name.lower().strip()]


    def set_sched_option(self, name, value=None):
        """
        Set an sched_option value based on its name

        :param name: the name of the sched_option
        :param value: the value to set
        """

        # get the option from the task if it already exist
        option = self._get_sched_option(name)

        # get the option from the cluster if not
        if option is None and self.cluster_obj is not None:
            option = self.cluster_obj.get_sched_option(name)

            if option is None:
                raise ToriiException('No scheduler option {0} in {1}'.format(name, self.cluster_obj))

            # add a copy of the option to the task
            option = copy.deepcopy(option)
            self.sched_options.append(option)

        # careful value attribute may not exist
        setattr(option, 'value', value)

    def get_sched_option(self, name):
        """
        Get an scheduler option value based on its name

        :param name: the name of the sched_option 
        :return: the value
        """
        option = self._get_sched_option(name)

        if option is not None:
            return option.value
        else:
            return None

    @property
    def cluster(self):
        if hasattr(self, 'context') and hasattr(self.context, 'cluster'):
            return self.context.cluster
        else:
            return None

    def set_cluster(self, cluster):
        if isinstance(cluster, ToriiObject):
            setattr(self.context, 'cluster', cluster.ref)
        elif isinstance(cluster, Struct):
            setattr(self.context, 'cluster', cluster)
        else:
            raise ToriiException('Bad parameter, expecting a ToriiObject or a Reference')

    def set_rundir(self, rundir):
        setattr(self.context, 'runDir', rundir)

    def submit(self):
        return self._service.submit(self)

    def lowla(self, **kwargs):
        return self._service.lowla(self, **kwargs)

    def validate(self):
        return self._service.validate(self)

    def clone(self):
        return self._service.clone(self)

    def picomize(self):
        return self._service.picomize(self)

    def kill(self):
        return self._service.kill(self)

    def pause(self):
        return self._service.pause(self)

    def resume(self):
        return self._service.resume(self)

    def command(self, commandId, commandOption=None):
        return  self._service.command(self, commandId=commandId, commandOption=commandOption)

    def job_command(self, jobIdx, commandId, commandOption=None):
        return  self._service.job_command(self, jobIdx=jobIdx, commandId=commandId, commandOption=commandOption)

    def get_records(self, max_records=100, increment=True):
        return self._service.get_records(self, max_records, increment)

    @property
    def viewer_url(self):
        return self._service.get_viewer_url(self)

    def open_viewer(self):
        self._service.open_viewer(self)

    @property
    def mapper_url(self):
        return self._service.get_mapper_url(self)

    def open_container_mapper(self):
        self._service.open_container_mapper(self)
