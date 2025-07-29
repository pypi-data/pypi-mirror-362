from renderg_api.connect import Connect


class TransferOperator(object):

    def __init__(self, connect: 'Connect'):
        self._connect = connect

    def _get_transfer_lines(self):
        return self._connect.get(self._connect.urls.GetTransferLine).get('data')

    def get_transfer_line(self, line_id):
        host = ''
        port = 0

        transfer_lines = self._get_transfer_lines()
        lines = transfer_lines.get(str(self._connect.cluster_id))
        if lines:
            for line in lines:
                if line.get("ISP_id") == line_id:
                    host = line.get('transfer_plus_host')
                    port = line.get('transfer_plus_port')
        if not host or not port:
            raise TypeError('Required "host" or "port" not specified. host: "{}", port: "{}"'.format(host, port))
        return host, port

    def get_transfer_config(self, job_id):
        params = {'job_id': str(job_id)}
        return self._connect.post(self._connect.urls.GetTransferConfig, params).get('data')

    def get_transfer_cluster(self, cluster_id):
        params = {'cluster_id': str(cluster_id)}
        data = self._connect.post(self._connect.urls.GetTransferByCluster, params).get('data')
        return data
