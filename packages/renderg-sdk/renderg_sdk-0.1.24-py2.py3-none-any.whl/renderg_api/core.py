import os

from renderg_api.connect import Connect
from renderg_api.operators import UserOperator, TaskOperator, JobOperator, ProjectOperator, EnvOperator, \
    TransferOperator
from renderg_api.mqConnect import MqConnect


class RenderGAPI(object):

    def __init__(self, auth_key=None, protocol='https', domain="client.renderg.com:6443", cluster_id=None):
        auth_key = auth_key or os.getenv("RENDERG_AUTH_KEY")
        if not auth_key:
            raise TypeError(
                'Required "auth_key" not specified. Pass as argument or set '
                'in environment variable RENDERG_AUTH_KEY.'
            )

        self._connect = Connect(auth_key, protocol, domain, cluster_id)

        self.user = UserOperator(self._connect)
        self.job = JobOperator(self._connect)
        self.task = TaskOperator(self._connect)
        self.project = ProjectOperator(self._connect)
        self.env = EnvOperator(self._connect)
        self.transfer = TransferOperator(self._connect)
        self.mqConnect = MqConnect(auth_key)

    def generate_job(self, dcc_file_path, project_name=None, env_name=None):
        pass

    def set_hardware_config(self, job_id, zone=None, ram=None):
        self.job.set_job_config(job_id, zone, ram)
