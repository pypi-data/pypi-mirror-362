import json


class EnvOperator(object):

    def __init__(self, connect):
        self._connect = connect

    def get_env_list(self):
        params = {
            'software_name': "",
            'software_version': ""
        }
        response = self._connect.post(self._connect.urls.GetEnvList, params)
        return response.get("data")

    def get_env_info_by_id(self, env_id):
        for env_item in self.get_env_list():
            if env_item.get("id") == env_id:
                definition = json.loads(env_item.get('definition'))
                environment_info = {
                    'software_name': env_item.get('software_name'),
                    'software_version': env_item.get('software_version'),
                    'definition': definition,
                    'extra_info': json.loads(env_item.get('extra_info')) if env_item.get('extra_info') else {}
                }
                return environment_info

        return {}
