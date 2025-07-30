import os
from time import sleep

from requests_toolbelt import MultipartEncoder
import json as json_lib

from torii.data import *
from torii.services import Service


class AiService(Service):

    def __init__(self, torii):
        """
        Create the graph service
        """
        Service.__init__(self,
                         torii=torii,
                         name='ai',
                         base_path='artificial_intelligence_c9a0d5e4')



    def start_engine(self,
                     application_name, application_version,
                     model_path, model_server,
                     task_name=None, tags=None):

        payload = {
            'type': 'inferenceInputs',
            'applicationName': application_name,
            'applicationVersion': application_version,
            'modelPath': model_path,
            'serverName': model_server.name if isinstance(model_server, Struct) else model_server,
            'taskName': task_name if task_name else application_name,
            'tags': tags if tags else [],
            'config' : {
                'one_shot': False,
                'input_server': model_server.name if isinstance(model_server, Struct) else model_server
            }
        }

        json = self.request_post(path='inference', json=payload)

        ai_task = Struct(json)
        ai_task.task = Task(json=json['task'], service=self._torii.tasks)

        return ai_task

    def init_proxy(self, engine):

        # Map<String, Object> params = new HashMap<>();
        # params.put("https", false);
        # params.put("port", inferenceEngine.getTask().getRunInfos().get(InferenceEngine.HTTP_PORT_KEY));
        # params.put("path", "/");
        #
        # try {
        #     return this.getRequest(inferenceEngine.getTask().getIdString() + "/" + PROXY_TARGET,
        #             params,
        #             InferenceEngine.class);
        # } catch (Exception e) {
        #     throw new ToriiException("Failed to create proxy for inference engine " + inferenceEngine.getId(), e);
        # }

        sleep(3)
        engine.task.update()
        params = {
            'https': False,
            'port': engine.task.runInfos.http_port,
            'path': '/'
        }

        self.request_get(path='inference/{}/proxy'.format(engine.task.id), params=params)
        engine.task.update()


    def infer(self, engine, images, config=None):


        if not engine.task.proxies:
            self.init_proxy(engine)

        proxy = engine.task.proxies[0]

        if config is None:
            config = {
                'type': 'jpg',
                'confidence_threshold': 0.1
            }

        multipart_data = {'config': json_lib.dumps(config)}
        multipart_data = {}

        i = 0
        for image_path in images:
            key = 'file' + str(i) + os.path.splitext(image_path)[1]
            multipart_data[key] = (os.path.basename(image_path),
                                   open(image_path, 'rb'),
                                   'application/octet-stream')

            i += 1

        multipart_encoder = MultipartEncoder(fields=multipart_data)
        result = self.request_post(path='/proxy/{}/'.format(proxy.id),
                                   data=multipart_encoder,
                                   params=config)

        return Struct(result)