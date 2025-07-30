from torii.data.record import Record
from torii.services import Service


class GraphService(Service):

    def __init__(self, torii):
        """
        Create the graph service
        """
        Service.__init__(self, torii=torii, name='graph')


    def get_records(self, task, min_step=0, max_records=100, get_last=False):
        """
        Get the list of records for a given tasks.

        :param task:        The task
        :param min_step:    The minimum value of the step
        :param max_records: The max number of records to get
        :param get_last:    Give the last records in priority

        :return: a list of records
        """

        params = {
            'stepMin': min_step,
            'nbMax': max_records,
            'last': get_last
        }

        json = self.request_get(path=task.id, params=params)

        return [Record(x) for x in json['taskRecords']]