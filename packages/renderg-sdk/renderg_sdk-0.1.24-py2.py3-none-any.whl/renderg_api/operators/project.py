
class ProjectOperator(object):

    def __init__(self, connect):
        self._connect = connect

    def get_project_list(self):
        response = self._connect.get(self._connect.urls.GetProjectList)
        return response.get("data")
