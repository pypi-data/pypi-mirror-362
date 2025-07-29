
import os

from renderg_api.constants import JobStatus
from renderg_transfer.AssetsPathHelper import AssetsPathHelper
from renderg_transfer.TransferHelper import TransferHelper

import renderg_utils


class RenderGUpload:

    def __init__(self, api, job_id, info_path, line, speed, workspace=None, logger=None):
        if logger is None:
            logger = renderg_utils.get_logger()
        self.logger = logger

        self.api = api
        self.transfer_config = api.transfer.get_transfer_config(job_id)
        self.transfer_lines = api.transfer.get_transfer_line(line)
        self.info_path = info_path
        self.job_id = job_id
        if speed is not None:
            self.speed = speed
        else:
            self.speed = 1000
        self.workspace = os.path.join(renderg_utils.get_workspace(workspace), str(self.job_id))
        self.log_path = os.path.join(renderg_utils.get_workspace(workspace), 'log')
        renderg_utils.check_path(self.workspace)
        renderg_utils.check_path(self.log_path)

    def upload(self):
        self.api.job.update_job_status(self.job_id, JobStatus.STATUS_UPLOAD)
        source_paths, dest_paths = AssetsPathHelper.get_file_list_for_info_cfg(self.info_path, self.job_id)

        host, port = self.transfer_lines
        username = self.transfer_config.get("username")
        password = self.transfer_config.get("password")

        file_pair_list_path = TransferHelper.create_file_pair_list_file(
            self.workspace, source_paths, dest_paths
        )

        cmd_pass = "set ASPERA_SCP_PASS={password}".format(password=password)
        cmd = TransferHelper.create_ascp_command(
            cmd_pass=cmd_pass,
            mode="send",
            host=host,
            port=port,
            username=username,
            max_speed=self.speed,
            log_dir=self.log_path,
            pair_list_file=file_pair_list_path
        )
        self.logger.info(cmd)
        code, stderr = renderg_utils.run_cmd(cmd, shell=True)
        self.logger.info("cmd return code: {}".format(code))
        if code != 0:
            raise Exception("{} 上传失败。 error={}".format(self.job_id, stderr.read()))
