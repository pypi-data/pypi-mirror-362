from torii.data import Struct
from torii.exception import ToriiException
from torii.data.torii_object import ToriiObject


class Application(ToriiObject):

    _DICT_ENTRIES = ['phaseScripts', 'clusterScripts']

    def __init__(self, json, service, details=False):
        ToriiObject.__init__(self, json, service)

        self._details = details


    def has_details(self):
        return self._details

    def __assert_configurable(self):
        if not self._details:
            raise ToriiException('Cannot configure application without details')

    def __str__(self):
        """ String converter """
        if hasattr(self, 'name') and self.name and hasattr(self, 'version') and self.version:
            return '{2} {0}:{1}'.format(self.name, self.version, type(self))
        else :
            return '{1} {0}'.format(self.id, type(self))

    def clear_clusters(self):
        """
        Clears the cluster configuration
        :return:
        """
        self.__assert_configurable()
        self.clusters = []
        self.clusterScripts = {}

    def set_cluster(self, cluster, environment=None):
        """
        Tells that the application cannot run on a given cluster
        :param cluster: the cluster to unset
        :param environment: the configuration script
        :return:
        """
        self.__assert_configurable()

        self.clusters = [ref for ref in self.clusters if ref.id != cluster.id]
        self.clusters.append(cluster.ref)

        if environment is not None:
            self.clusterScripts[cluster.id] = environment
        else:
            self.clusterScripts.pop(cluster.id, None)


    def unset_cluster(self, cluster):
        """
        Tells that the application cannot run on a given cluster
        :param cluster: the cluster to unset
        :return:
        """
        self.__assert_configurable()

        if isinstance(cluster, ToriiObject):
            id = cluster.id
        else:
            id = cluster

        self.clusters = [ref for ref in self.clusters if ref.id != id]


    def set_phase(self, name, script=None, cardinality=None, **kwargs):
        """
        Configure a  phase

        :param name:
        :param script:
        :param cardinality:
        :param kwargs:
        :return:
        """
        self.__assert_configurable()

        phase = next(phase for phase in self.phases if phase.name == name)
        if not phase:
            phase = Struct({'name': name})
            self.phases.append(phase)

        # activate the phase if its cardinality has been
        if cardinality is None and hasattr(phase, 'cardinality') and phase.cardinality == 0:
            phase.cardinality = 1

        if kwargs:
            for key, value in kwargs.items():
                setattr(phase, key, value)


        if script is not None:
            self.phaseScripts[name] = script
        else:
            self.phaseScripts.pop(name, None)


    def unset_phase(self, name):
        """
        Make sure the phase is not executed when the application is run
        :param name:
        :return:
        """
        self.__assert_configurable()

        phase = next(phase for phase in self.phases if phase.name == name)
        if phase:
            setattr(phase, 'cardinality', 0)
