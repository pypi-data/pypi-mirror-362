import base64
import glob
import json as jsonlib
import os
import re
import shutil

import sys
import tempfile
import zipfile

from torii.exception import ToriiException
from torii.data import *
from torii.data import json_to_struct
from torii.services.torii_service import ToriiService



def _underscore_to_camelcase(value):
    def camelcase():
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(next(c)(x) for x in value.split("_") if x)


def _read_script_content(path, dos2unix=True):
    with open(path, 'r') as file:
        content = file.read()

        if dos2unix:
            content = content.replace('\r\n', '\n')

        return content


def _insert_functions(script, functions):
    result = ''

    in_header = True
    for line in script.splitlines():

        # we look for the first line that is NOT in the header
        if in_header:
            strip_line = line.lstrip()
            header_line = len(strip_line) == 0 \
                          or strip_line.startswith('#') \
                          or strip_line.startswith('import') \
                          or strip_line.startswith('from')

            if not header_line:
                # ... at the end of the header, we insert the function definitions
                in_header = False
                result = result + functions + '\n'

        # we add the lines of the original script one by one
        result = result + line + '\n'

    return result


class ApplicationService(ToriiService):

    def __init__(self, torii):
        """
        Create the application service
        """
        ToriiService.__init__(self, torii=torii, name='applications', object_class=Application)


    def get(self, id=None, details=False, **kwargs):
        if id and details:
            json = self.request_get(path='{0}'.format(id), params={'details':'true'})
            return Application(json, self, details=True)
        elif details:
            application = ToriiService.get(self, **kwargs)
            return self.get(application.id, details=True) if application else None
        else:
            return ToriiService.get(self, id, **kwargs)


    def update(self, application, **kwargs):
        if isinstance(application, Application) and (application.has_details()
                                                     or 'details' in kwargs and kwargs['details']):
            if application.has_changed():
                # update the remote version
                kwargs['editMode'] = True
                json = self.request_post(path='{0}'.format(application.id), json=application.to_json(), params=kwargs)
            else:
                # update local version
                json = self.request_get(path='{0}'.format(application.id))

            if json:
                application.from_json(json)
        else:
            application = ToriiService.update(self, application, editMode=False)

        return application

    def __export_application(self, application, path=None, zip=False):
        try:
            if not application.has_details():
                raise ToriiException('Cannot export {0}, no details'.format(application))

            if zip:
                dir = tempfile.mkdtemp()
            else:
                if not os.path.exists(path):
                    os.makedirs(path)
                dir = path

            # write the application JSON
            json = application.to_json()
            # ... the verbose fields are removed from the json to be written independently
            for field in ['icon', 'clusters', 'clusterScripts', 'phaseScripts', 'validationScript']:
                json.pop(field, None)
            with open(os.path.join(dir, 'definition.json'), 'w+') as outfile:
                jsonlib.dump(json, outfile, indent=4, sort_keys=True)

            # decode and write the application icon
            if hasattr(application, 'icon'):
                try:
                    regex = re.compile('data:image/(?P<type>[a-z]+);base64,(?P<content>.*)')
                    match = regex.match(application.icon)
                    if match:
                        icon_path = os.path.join(dir, 'icon.' + match.groupdict()['type'])
                        with open(icon_path, 'w+b') as outfile:
                            content = base64.b64decode(match.groupdict()['content'])
                            outfile.write(content)
                except:
                    self._logger.warn('Failed to extract icon for {}'.format(application))

            # write the cluster environment scripts
            clusters_dir = os.path.join(dir, 'clusters')
            os.makedirs(clusters_dir)
            for id, script in application.clusterScripts.items():
                try:
                    cluster = self._torii.clusters.get(id)
                    if cluster:
                        with open(os.path.join(clusters_dir, cluster.name), 'w+') as outfile:
                            outfile.write(script)
                except:
                    self._logger.warn('Failed to write cluster environment for {}'.format(application))

            # write the validation scripts
            scripts_dir = os.path.join(dir, 'scripts')
            os.makedirs(scripts_dir)
            if hasattr(application, 'validationScript') and application.validationScript:
                with open(os.path.join(scripts_dir, 'validation.py'), 'w+') as outfile:
                    outfile.write(application.validationScript)

            if hasattr(application, 'interfaceScript') and application.interfaceScript:
                with open(os.path.join(scripts_dir, 'interface.js'), 'w+') as outfile:
                    outfile.write(application.interfaceScript)

            # write the phases scripts
            phases_dir = os.path.join(dir, 'phases')
            os.makedirs(phases_dir)
            for name, script in application.phaseScripts.items():
                if name is 'monitor':
                    # currently the monitor script is still in the phases ... but it should not
                    filepath = os.path.join(scripts_dir, name)
                else:
                    filepath = os.path.join(phases_dir, name)

                with open(filepath, 'w+') as outfile:
                    outfile.write(script)

            if zip:
                # go to the temp dir
                cwd = os.getcwd()
                os.chdir(dir)

                # zip its content
                ziph = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
                for root, dirs, files in os.walk('.'):
                    for file in files:
                        ziph.write(os.path.join(root, file))

                # go back to the current dir
                os.chdir(cwd)

                # and cleanup
                shutil.rmtree(dir)


        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to export {0}\n\t{1}'.format(application, e)).with_traceback(sys.exc_info()[2])


    def __import_application(self, path=None, dos2unix=True):
        try:
            if not os.path.exists(path):
                raise ToriiException('Cannot import application from \'{0}\', no such file or directory'
                                     .format(path))

            if os.path.isdir(path):
                root_dir = path
            else:
                root_dir = tempfile.mkdtemp()

                try:
                    ziph = zipfile.ZipFile(path, 'r')
                    ziph.extractall(root_dir)
                    ziph.close()
                except Exception as e:
                    raise ToriiException('Failed to import application from \'{0}\'\n\t{1}'.format(path, e)).with_traceback(sys.exc_info()[2])

            # the application description can be in a subdirectory
            dir = None
            for root, dirs, files in os.walk(root_dir):
                if 'application.json' in files or 'definition.json' in files:
                    dir = root

            if dir is None:
                raise ToriiException('Cannot find application.json in {0}'.format(path))


            application = self.__import_application_json(dir)

            # consolidate the refrences appearing in the application
            self.__consolidate_application_references(application)

            # configure the clusters environment
            self.__import_application_environement(application, dir, dos2unix)

            # import the phase scripts
            self.__import_application_phases(application, dir, dos2unix)

            # import the other scripts (validation and monitoring)
            self.__import_application_scripts(application, dir, dos2unix)

            # import each module from the modules directory
            modules_dir = os.path.join(dir, 'modules')
            if os.path.isdir(modules_dir):
                for module_name in os.listdir(modules_dir):
                    self.__import_application_module(application,
                                                     module_name,
                                                     os.path.join(modules_dir, module_name),
                                                     dos2unix)

            # get the application icon
            icon_paths = glob.glob(os.path.join(dir, 'icon.*'))
            if icon_paths and os.path.isfile(icon_paths[0]):
                image_type = icon_paths[0].split('.')[-1].lower()
                with open(icon_paths[0], 'rb') as file:
                    content = file.read()
                    if content:
                        application.icon = 'data:image/{0};base64,{1}'\
                            .format(image_type, str(base64.b64encode(content), 'utf8'))

            ### legacy fixes ###
            # create a default phase in case of incoherence
            if 'monitor' in application.phaseScripts \
                    and not any(phase.name == 'monitor' for phase in application.phases):
                application.phases.append(Struct({'name': 'monitor'}))

            # remove the 'valid' attribute from the inputs
            for input in application.inputs:
                if hasattr(input, 'valid'):
                    delattr(input, 'valid')

            return application

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to import application from \'{0}\'\n\t{1}'.format(path, e)).with_traceback(sys.exc_info()[2])


    def __import_application_json(self, dir):
        # read the application JSON
        if  'application.json' in os.listdir(dir):
            json_path = os.path.join(dir, 'application.json')
        elif 'definition.json' in os.listdir(dir) :
            json_path = os.path.join(dir, 'definition.json')
        else:
            raise ToriiException('Cannot import application from, missing definition file in {0}'
                                 .format(dir))

        with open(json_path) as file:
            json = jsonlib.load(file)

        application = Application(json, self, True)

        # get complementary definitions from other json files (inputs.json, )
        extra_json_path = {name.replace('.json', '', 1): os.path.join(dir, name)
                         for name in os.listdir(dir)
                           if name.endswith('.json') and name not in ['application.json', 'definition.json']}
        for name, path in extra_json_path.items():
            # put the compementory description in the corresponding field
            with open(path) as file:
                json = jsonlib.load(file)
                struct = json_to_struct(json)
                field = _underscore_to_camelcase(name)

                setattr(application, field, struct)


        # default
        if not hasattr(application, 'inputs'):
            setattr(application, 'inputs', [])

        return application


    def __import_application_module(self, application, module_name, module_dir, dos2unix):

        module_prefix = module_name + '__'

        # get the inputs from the module
        inputs_path = os.path.join(module_dir, 'inputs.json')
        if os.path.isfile(inputs_path):
            with open(inputs_path) as file:
                json = jsonlib.load(file)
                inputs = json_to_struct(json)

                for input in inputs:
                    if not input.name.startswith(module_prefix):
                        raise ToriiException('Invalid input name \'{0}\' in module \'{1}\' (must start with {2})'
                                             .format(input.name, module_name, module_prefix))

                application.inputs.extend(inputs)

        # append the validation script from the module
        validate_path = os.path.join(module_dir, 'validation.py')
        if os.path.isfile(validate_path):
            validate_functions = _read_script_content(validate_path, dos2unix)
            application.validationScript = _insert_functions(application.validationScript, validate_functions)

        # read the custom layout panels from the module
        panels_path = os.path.join(module_dir, 'custom_layout.json')
        if os.path.isfile(panels_path):
            with open(panels_path) as file:
                json = jsonlib.load(file)
                module_panels = json_to_struct(json)

                # make a map out of the panel or list of panels read from the json
                panel_map = {}
                if isinstance(module_panels, list):
                    for panel in module_panels:
                        panel_map[panel.panelId] = panel
                else:
                    panel_map[module_panels.panelId] = module_panels

                # check that the panel ids correspond to the module
                for panel in panel_map.values():
                    if not panel.panelId.startswith(module_prefix):
                        raise ToriiException('Invalid panel id \'{0}\' in module \'{1}\' (must start with {2})'
                                             .format(panel.panelId, module_name, module_prefix))

                # explore the panels and replace the module panel reference
                def replace_panel_references(panel, list, index):
                    if hasattr(panel, 'panelId') and panel.panelId in panel_map:
                        list[index] = panel_map[panel.panelId]
                    elif hasattr(panel, 'panels'):
                        for i in range(len(panel.panels)):
                            replace_panel_references(panel.panels[i], panel.panels, i)

                replace_panel_references(application.customLayout, None, 0)


    def __import_application_phases(self, application, dir, dos2unix):
        # list the phases scripts
        phases_dir = os.path.join(dir, 'phases')
        if os.path.isdir(phases_dir):
            # get all the files from the 'phases' dir
            phase_files = {os.path.splitext(filename)[0]: os.path.join(phases_dir, filename) for filename in os.listdir(phases_dir)}
        else:
            # or get all the 'app_<phase>' files from the root dir (legacy)
            phase_files = {name.replace('app_', '', 1): os.path.join(dir, name)
                         for name in os.listdir(dir)
                           if name.startswith('app_') and name not in ['validate', 'monitor']}

        # ... and associate the scripts with the phases
        phases = {}
        phase_list = []
        for phase in application.phases:
            if isinstance(phase, Struct):
                phases[phase.name] = phase
                phase_list.append(phase)
            elif isinstance(phase, str):
                # for legacy purpose we reconstitute a phase from a simple name
                #  - only the 'execute' phase uses User Defined Scheduler Options (UDSO)
                #  - we create a simple phase dependency
                phase_obj = Struct({'name': phase,
                                    'udso': (phase == 'execute'),
                                    'dependencies': [phase.name for phase in phase_list[-1:]]})
                phases[phase] = phase_obj
                phase_list.append(phase_obj)
        application.phases = phase_list

        # we don't overwrite 'phaseScripts' directly in case the script were in the Json
        if not hasattr(application, 'phaseScripts') or application.phaseScripts is None:
            application.phaseScripts = {}

        for name, path in phase_files.items():
            application.phaseScripts[name] = _read_script_content(path, dos2unix)

        return phases


    def __import_application_scripts(self, application, dir, dos2unix):
        # read the validation script
        scripts_dir = os.path.join(dir, 'scripts')
        if os.path.isfile(os.path.join(scripts_dir, 'validation.py')):
            application.validationScript = _read_script_content(os.path.join(scripts_dir, 'validation.py'), dos2unix)
        elif 'app_validate' in os.listdir(dir):
            # (legacy case)
            application.validationScript = _read_script_content(os.path.join(dir, 'app_validate'), dos2unix)

        # read the interface script
        if os.path.isfile(os.path.join(scripts_dir, 'interface.js')):
            application.interfaceScript = _read_script_content(os.path.join(scripts_dir, 'interface.js'), dos2unix)

        # and the monitoring script
        if os.path.isfile(os.path.join(scripts_dir, 'monitor')):
            application.phaseScripts['monitor'] = _read_script_content(os.path.join(scripts_dir, 'monitor'), dos2unix)
        elif 'app_monitor' in os.listdir(dir):
            application.phaseScripts['monitor'] = _read_script_content(os.path.join(dir, 'app_monitor'), dos2unix)



    def __import_application_environement(self, application, dir, dos2unix):
        # read the cluster environment scripts
        application.clear_clusters()
        clusters_dir = os.path.join(dir, 'clusters')
        cluster_scripts = {}
        if os.path.isdir(clusters_dir):
            for name in os.listdir(clusters_dir):
                script = _read_script_content(os.path.join(clusters_dir, name), dos2unix)
                cluster_scripts[re.sub('\.env$', '', name)] = script

        # ... and associate the scripts to the local clusters
        application.clusterScripts = {}
        clusters = self._torii.clusters.list()
        for cluster in clusters:
            script = None
            if cluster.id in cluster_scripts:
                script = cluster_scripts[cluster.id]
            elif cluster.name in cluster_scripts:
                script = cluster_scripts[cluster.name]
            elif 'default' in cluster_scripts:
                script = cluster_scripts['default']

            if script is not None:
                application.clusterScripts[cluster.id] = script
            application.clusters.append(cluster.ref)


    def __consolidate_application_references(self, application):
        # update references in users, teams and projects
        for ref_type in ['users', 'teams', 'projects']:
            if hasattr(application, ref_type):
                updated_refs = []

                # for each imported reference we try to find in torii a matching object
                for ref in getattr(application, ref_type):
                    object = None
                    try:
                        if ref.id:
                            object = getattr(self._torii, ref_type).get(ref.id)
                        elif ref.name:
                            object = getattr(self._torii, ref_type).get(name=ref.name)
                    except:
                        # ... if no matching object is found, we consider that the reference can be dropped
                        pass

                    if object is not None:
                        updated_refs.append(object.ref)

                setattr(application, ref_type, updated_refs)
            else:
                setattr(application, ref_type, [])


    def import_application(self, path=None, force=False, duplicate=False, dos2unix=True, **kwargs):
        """

        :param path:
        :return:
        """
        try:
            applications = []
            realPaths = glob.glob(path)

            for realPath in realPaths:
                application = self.__import_application(realPath, dos2unix)
                existing_application = None

                if duplicate:
                    application.clear_id()
                    application.status = 'DRAFT'
                else:
                    try:
                        existing_application = self.get(id=application.id)
                    except:
                        pass

                    if not force and existing_application is not None:
                        raise ToriiException('Cannot import \'{0}\', {1} already exist '.format(realPath, existing_application)
                                             + '(use \'force\' if you want to overwrite it)')

                # set the application fields explicitely specified by the user
                if kwargs:
                    for key, value in kwargs:
                        setattr(application, key, value)


                if existing_application:
                    # keep the authorizations
                    application.users    = existing_application.users
                    application.teams    = existing_application.teams
                    application.projects = existing_application.projects

                    # update the application
                    application.update(force=force, **kwargs)
                else:
                    # create the application
                    application.create(**kwargs)

                applications.append(application)

            if len(applications) == 0:
                raise ToriiException('Path {0} does not correspond to any application'.format(path))
            elif len(applications) == 1:
                return applications[0]
            else:
                return applications

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to import from \'{0}\'\n\t{1}'.format(path, e)).with_traceback(sys.exc_info()[2])

    def export_application(self, id=None, path=None, dir=None, zip=False, **kwargs):
        """
        Export one or more aplications
        :param id: the id of the single application to export
        :param path: the exact path to export to
        :param dir: the directory to export to (not compatible with path)
        :param zip: must we zip the application archive
        :param kwargs: other arguments to identify the applications to export
        :return:
        """

        try:
            # get the application ids to export
            if id is not None:
                ids = [id]
            else:
                ids = [app.id for app in self.list(**kwargs)]

            if len(ids) == 0:
                raise ToriiException('Cannot export, no application matching the parameters')

            if path and len(ids) > 1:
                raise ToriiException('Cannot export, many applications matching the parameters '
                                     'while a path has been specified')

            if not path and not dir:
                dir = os.getcwd()

            for id in ids:
                application = self.get(id=id, details=True)

                if path:
                    current_path = path
                else:
                    filename = '{0}-{1}.{2}'.format(application.name, application.version, application.id)\
                        .lower()\
                        .replace(' ', '_')\
                        .replace('/', '_')

                    if zip:
                        filename += '.zip'

                    current_path = os.path.join(dir, filename)

                self.__export_application(application, current_path, zip)

                return current_path

        except ToriiException:
            raise
        except Exception as e:
            raise ToriiException('Failed to export applications\n\t{1}'.format(application, e)).with_traceback(sys.exc_info()[2])

