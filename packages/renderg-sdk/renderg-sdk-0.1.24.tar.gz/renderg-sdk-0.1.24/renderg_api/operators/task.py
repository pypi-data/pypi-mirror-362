from renderg_api.connect import Connect
from renderg_api.constants import ControlType


class TaskOperator(object):

    def __init__(self, connect: 'Connect'):
        self._connect = connect

    def _control_task(self, job_id, control_type, task_id_list: 'list' = None):
        """Control tasks in a job.
        Args:
            job_id (int): The ID of the job containing the tasks.
            control_type (ControlType): The type of control operation to perform.
            task_id_list (list, optional): A list of task IDs to control.
                Example:
                    [234617690, 234617691]
        Returns:
            dict: The response from the control operation.
        """

        params = {
            'job_id': job_id,
            'task_array': task_id_list or [],
            "type": control_type
        }
        return self._connect.post(self._connect.urls.ControlTask, params)

    def start_task(self, job_id, task_id_list=None):
        return self._control_task(job_id=job_id, control_type=ControlType.START, task_id_list=task_id_list or [])

    def stop_task(self, job_id, task_id_list=None):
        return self._control_task(job_id=job_id, control_type=ControlType.SUSPEND, task_id_list=task_id_list or [])

    def requeue_task(self, job_id, task_id_list=None):
        return self._control_task(job_id=job_id, control_type=ControlType.REQUEUE, task_id_list=task_id_list or [])

    def __get_task_list(self, page=0, count=20, json_params=None):
        """
        Retrieve a paginated list of tasks.

        Args:
            page (int): The page number to retrieve. Defaults to 1.
            count (int): The number of tasks per page. Defaults to 20.
            json_params (dict, optional): Additional filtering parameters for the task list.
                Example:
                    {
                        "desc": true,
                        "job_farm_id": "",
                        "sort": "",
                        "stat": "",
                        "frame": null,
                        "job_id": 6666666
                    }

        Returns:
            dict: The response containing the task list and pagination details.
        """
        url_params = {
            'page': page,
            'count': count
        }
        if json_params is None:
            json_params = {}
        if not isinstance(json_params, dict):
            raise TypeError('json_params must be a dict, got {}'.format(type(json_params)))

        return self._connect.post(self._connect.urls.GetTaskList, data=json_params, params=url_params)

    def get_task_list_by_job_id(self, job_id, page=0, count=20):
        json_params = {
            'job_id': job_id
        }
        return self.__get_task_list(page=page, count=count, json_params=json_params)
