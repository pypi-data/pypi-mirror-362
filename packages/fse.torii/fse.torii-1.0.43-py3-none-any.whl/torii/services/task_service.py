import time
import webbrowser

from torii.exception import ToriiException
from torii.services.torii_service import ToriiService
from torii.data import Task, Picom


class TaskService(ToriiService):

    def __init__(self, torii):
        """
        Create the task service
        """
        ToriiService.__init__(self, torii=torii, name='tasks', object_class=Task)

    def refresh(self, task):
        task = super(TaskService, self).refresh(task)

        return task

    def new(self, create=True, **kwargs):
        # by default, create the task in the current container
        if 'parent' not in kwargs and self._torii.current_container:
            kwargs['parent'] = self._torii.current_container.id

        return ToriiService.new(self, create=create, **kwargs)


    def create(self, task=None, template=None):

        if task is None :
            if template is not None:
                if not isinstance(template, Task):
                    # try to find the template by name
                    template = self.get(name=template, status='TEMPLATE')

                task = Task(template)
                task.status = 'UNKNOWN'
            else:
                raise ToriiException('Cannot create task without template')

        # use the default container if necessary/possible
        if (not hasattr(task, 'parent') or not task.parent) and self._torii.current_container:
            task.parent = self._torii.current_container.id

        return ToriiService.create(self, task)


    def validate(self, task):
        """
        Validate a task

        :param task: the task to be validated
        :return:
        """
        data = {
            'task': task.to_json(),
            'save': True
        }

        if task.has_changed():
            data['previousTask'] = task.orig

        json = self.request('POST', path='{0}/validate'.format(task.id), json=data)
        task.from_json(json)
        return task


    def submit(self, task):
        """
        Submit a task

        :param task: the task to submit
        :return:
        """
        if task.has_changed():
            self.update(task)

        return self.action('submit', task)

    def lowla(self, task, **kwargs):
        """
        Submit a Low Latency task on a running LowLa Engine

        :param task: the task to submit
        :return:
        """

        return self.action('lowla', task, send_payload=True, update=False, cast=Task, params=kwargs)


    def clone(self, task, parent=None):
        """
        Clone a task

        :param task: the task to clone
        :return:
        """

        if task.has_changed():
            self.update(task)

        # by default, create the task in the current container
        if parent :
            params = {'parentId': parent.id}
        else:
            params = {'parentId': self._torii.current_container.id}

        clone = self.action(action='clone', obj=task,
                            send_payload=False, update=False,
                            params=params,
                            cast=Task, service=self)

        # refresh the task (its cloned counter have changed)
        task.refresh()

        return clone

    def picomize(self, task):
        """
        Picomize a hierarchical task

        :param task: the task to picomize
        :return:
        """
        if task.has_changed():
            self.update(task)

        picom = self.action(action='picomize', obj=task,
                            send_payload=False, update=False,
                            cast=Picom, service=self)

        return picom

    def command(self, task, commandId, commandOption=None):
        """
        Throw a task command

        :param task: the task
        :param commandId: the command type
        :param commandOption: the options of the command if any
        :return:
        """

        if task.has_changed():
            self.update(task)

        params = {'commandId': commandId, 'commandOption': commandOption}
        return self.action('taskCommand', task, params=params, send_payload=False, update=False)


    def job_command(self, task, jobIdx, commandId, commandOption=None):
        """
        Throw a job command

        :param task: the task
        :param jobIdx: the job index
        :param commandId: the command type
        :param commandOption: the options of the command if any
        :return:
        """

        if task.has_changed():
            self.update(task)

        params = {'jobId': task.jobs[jobIdx]._id, 'commandId': commandId, 'commandOption': commandOption}
        return self.action('jobCommand', task, params=params, send_payload=False, update=False)


    def job_command(self, task, jobIdx, commandId, commandOption=None):
        """
        Throw a job command

        :param task: the task
        :param jobIdx: the job index
        :param commandId: the command type
        :param commandOption: the options of the command if any
        :return:
        """

        if task.has_changed():
            self.update(task)

        params = {'jobId': task.jobs[jobIdx]._id, 'commandId': commandId, 'commandOption': commandOption}
        return self.action('jobCommand', task, params=params, send_payload=False, update=False)

    def kill(self, task):
        return self.command(task, 'kill')

    def pause(self, task):
        return self.command(task, 'hold')

    def resume(self, task):
        return self.command(task, 'release')


    def get_all_status(self, task=None, parent=None, root=None, status=None):
        if isinstance(task, str):
            tasks = [self.get(id)]
        elif isinstance(task, Task):
            task.refresh()
            tasks = [task]
        elif isinstance(parent, (Task, str)):
            tasks = self.list(parent=parent)
        elif isinstance(root, (Task, str)):
            tasks = self.list(root = root)
        elif self._torii.current_container:
            tasks = self.list(parent=self._torii.current_container)
        else:
            raise ToriiException('Bad parameter, check_active requires task, parent or root being Task or str')

        return [task.status for task in tasks]


    def check_status(self, task=None, parent=None, root=None, status=None):
        """
        Check if a task or the children or the descendants are active

        by default, if no argument is provided the service will check the children of the current container

        :param task: the task to check (id or Task)
        :param parent: the parent of the tasks to check (id or Task)
        :param root: the root of the tasks to check (id or Task)
        :param status: the status against which the task(s) is checked
        :return: True or False
        """

        stati = self.get_all_status(self, task, parent, root, status)
        return all([Task.is_status(s, status) for s in stati])


    def check_active(self, task=None, parent=None, root=None, status=None):
        """
        Check if a task or a group of tasks are active
        """
        return self.check_status(task, parent, root, Task.ACTIVE_STATUS)

    def check_complete(self, task=None, parent=None, root=None, status=None):
        """
        Check if a task or a group of tasks are complete
        """
        return self.check_status(task, parent, root, Task.COMPLETE_STATUS)


    def wait(self, task=None, parent=None, root=None, period=None, timeout=None, status=Task.COMPLETE_STATUS):
        """
        Wait while the task or the children or the descendants are active
        :param task: the task to check (id or Task)
        :param parent: the parent of the tasks to check (id or Task)
        :param root: the root of the tasks to check (id or Task)
        :param period: the polling period
        :param timeout: the max time to wait
        :param status: the status or list of status to wait for
        :return: True if all the tasks have finished
        """
        if period is None:
            period = 2

        start_time = time.time()

        while True:
            stati = self.get_all_status(task=task, parent=parent, root=root)
            if all(Task.status_equal(s, status) for s in stati):
                return True
            elif all(Task.status_equal(s, Task.COMPLETE_STATUS) for s in stati):
                # the goal is not matched no more task is active
                return False

            waited_time = int(time.time() - start_time)
            if timeout and waited_time > timeout:
                return False

            self._logger.debug('Wait for tasks (waited_time = {0})'.format(waited_time))
            time.sleep(period)


    def get_records(self, task, max_records=100, increment=True):
        """
        Get the list of records for a given tasks.

        :param task:
        :param max_records:
        :param increment:
        :return:
        """

        if increment and task._last_record_step:
            records = self._torii.graph.get_records(task=task,
                                                    min_step=task._last_record_step + 1,
                                                    max_records=max_records,
                                                    get_last=False)

        else:
            records = self._torii.graph.get_records(task=task,
                                                    min_step=0,
                                                    max_records=max_records,
                                                    get_last=False)

        if records:
            task._last_record_step = int(records[-1].step)

        return records


    def get_viewer_url(self, task):
        """
        Get the URL of the standalone task viewer
        :param task:
        :return:
        """
        # url = '{0}/js/desktop/main-desktop.html?start_tool=taskViewer&id={1}&sessioId={3}'\
        #     .format(self._torii.properties['base_url'], task.id, self._torii.session.id)

        url = '{0}/js/desktop/main-desktop.html?start_tool=taskViewer&id={1}&type={2}&sessionId={3}'\
            .format(self._torii.properties['base_url'],
                    task.application.id, 'application', self._torii.session.id)
        return url


    def get_mapper_url(self, container):
        """
        Get the URL of the standalone task viewer
        :param task:
        :return:
        """
        # https://10.140.9.23:8443/torii/js/desktop/main-desktop.html?start_tool=process_mapper_98895ca2&processMap=5b3e0a5e897b9b3b4e5840d4

        url = '{0}/js/desktop/main-desktop.html?start_tool=process_mapper_98895ca2&processMap={1}&sessionId={2}'\
            .format(self._torii.properties['base_url'],
                    container.id,
                    self._torii.session.id)
        return url


    def open_viewer(self, task):
        """
        Open the standalone task viewer
        :param task:
        :return:
        """
        webbrowser.open_new(self.get_viewer_url(task))


    def open_container_mapper(self, task):
        """
        Open the standalone mapper on the task container
        :param task:
        :return:
        """

        container = self.get(task.root)
        webbrowser.open_new(self.get_mapper_url(container))

    def apply_profile(self, profile_id, task_id):
        try:
            return self._object_class(self.request_post(path='{0}/loadProfile/{1}'.format(task_id, profile_id)), self)
        except ToriiException:
            raise
        except Exception:
            raise ToriiException('Failed to apply the profile {0} on task {1})'.format(profile_id, task_id))

    def get_task_by_id(self, task_id, include=None):
        return self.get(id=task_id, include=include, cast=False)
