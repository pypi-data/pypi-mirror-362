
class UserOperator(object):

    def __init__(self, connect):
        self._connect = connect

    def get_cluster_list(self):
        response = self._connect.get(self._connect.urls.GetClusterList)
        return response.get("collection", [])

    def get_zone_list(self):
        response = self._connect.get(self._connect.urls.GetZoneList)
        return response
