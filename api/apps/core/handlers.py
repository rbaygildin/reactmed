import json

from tornado.web import RequestHandler

from apps.core.models import Patient, Instance
from apps.core.utils import DicomJsonEncoder, convert_dicom_to_img
from apps.dicom_ws.serializers import PatientSerializer, InstanceSerializer


class BaseNeurDicomHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def data_received(self, chunk):
        pass

    expected_path_params = None
    path_params = None

    def prepare(self):
        if self.expected_path_params and self.path_args:
            if len(self.expected_path_params) == len(self.path_args):
                self.path_params = {
                    self.expected_path_params[i]: self.path_args[i] for i in range(len(self.expected_path_params))
                }


class BaseJsonHandler(BaseNeurDicomHandler):
    def prepare(self):
        super(BaseJsonHandler, self).prepare()
        if self.request.body:
            try:
                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                self.send_error(400, message='Body is not JSON deserializable')

    def set_default_headers(self):
        super(BaseJsonHandler, self).set_default_headers()
        self.set_header('Content-Type', 'application/json')
        self.set_header('Server', 'NeurDICOM')

    def write(self, chunk):
        try:
            json_data = json.dumps(chunk)
            super(BaseJsonHandler, self).write(json_data)
        except ValueError:
            self.send_error(500, message='Response data is not JSON serializable')


class ModelListHandler(BaseJsonHandler):
    queryset = None
    serializer_class = None

    def get(self, *args, **kwargs):
        if not self.queryset:
            self.send_error(500, message='Model queryset is not defined')
        if not self.serializer_class:
            self.send_error(500, message='Serializer class is not defined')
        serializer = self.serializer_class(self.queryset, many=True)
        self.write(serializer.data)


class ModelListCreateHandler(BaseJsonHandler):
    queryset = None
    serializer_class = None

    def get(self, *args, **kwargs):
        if not self.queryset:
            self.send_error(500, message='Model queryset is not defined')
            return
        if not self.serializer_class:
            self.send_error(500, message='Serializer class is not defined')
            return
        serializer = self.serializer_class(self.queryset, many=True)
        self.write(serializer.data)

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.arguments)
        if serializer.is_valid():
            serializer.save()
            self.write(serializer.data)
        else:
            self.write(serializer.errors)
            self.send_error(500)


class ModelDetailHandler(BaseJsonHandler):
    queryset = None
    serializer_class = None

    def get(self, instance_id, *args, **kwargs):
        if not self.queryset:
            self.send_error(500, message='Model queryset is not defined')
        if not self.serializer_class:
            self.send_error(500, message='Serializer class is not defined')
        serializer = self.serializer_class(self.queryset.get(pk=instance_id))
        self.write(serializer.data)

# class BaseMultipleTypeResponseHandler()