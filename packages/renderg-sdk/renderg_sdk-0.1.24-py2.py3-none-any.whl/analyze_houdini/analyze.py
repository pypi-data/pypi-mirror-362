import logging
import os
import re

from renderg_api.constants import JobStatus

try:
    import _winreg
    winreg = _winreg
except ImportError:
    import winreg

from renderg_utils.exception import DCCFileNotExistsError
from renderg_utils.exception import DCCExeNotFoundError
from renderg_utils.exception import AnalyzeFailError
from renderg_utils.exception import ErrorCode, WarnCode

import renderg_utils


class AnalyzeHoudini(object):
    def __init__(self,
                 dcc_file,
                 dcc_version,
                 workspace=None,
                 dcc_exe_path=None,
                 api=None,
                 project_id=None,
                 env_id=None,
                 job_id=None,
                 logger=None
                 ):

        if not os.path.isfile(dcc_file):
            raise DCCFileNotExistsError(ErrorCode.DCCFileNotExistsError, dcc_file)

        self.dcc_file = dcc_file
        self.dcc_version = dcc_version
        self.dcc_exe_path = dcc_exe_path
        self.api = api
        self.project_id = project_id
        self.env_id = env_id
        self.job_id = job_id

        if logger is None:
            logger = logging.getLogger()
        self.logger = logger

        if not job_id:
            self.job_id = self.api.job.new_job(self.dcc_file, self.project_id, self.env_id)

        self.workspace = os.path.join(renderg_utils.get_workspace(workspace), str(self.job_id))
        renderg_utils.check_path(self.workspace)

        self.info_path = os.path.join(self.workspace, "info.cfg")
        self.warning_path = os.path.join(self.workspace, "warning.json")

        self.warning_info = {}

    def add_warning(self, warn, *args):
        self.warning_info.update({warn.code(): warn.msg(*args)})
        renderg_utils.write_json(self.warning_path, self.warning_info)

    def check_file_version(self):
        regex = re.compile(r"set -g _HIP_SAVEVERSION = '(?P<version>.*?)'\s")
        version = renderg_utils.get_dcc_file_version(self.dcc_file, regex)
        if version != self.dcc_version:
            self.add_warning(WarnCode.DCCVersionNotMatchWarn, version, self.dcc_version)

    def find_dcc_exe(self):
        dcc_exe_path = ''
        local_dcc_exe_path = r"C:\Program Files\Side Effects Software\Houdini {}\bin\hython.exe".format(self.dcc_version)

        if os.path.isfile(local_dcc_exe_path):
            dcc_exe_path = local_dcc_exe_path
        else:

            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Side Effects Software\Houdini ' + self.dcc_version
                )
                regedit_dcc_exe_path, _ = winreg.QueryValueEx(key, "InstallPath")
                dcc_exe_path = os.path.join(regedit_dcc_exe_path, r'bin\hython.exe')
            except BaseException as err:
                self.logger.warning(err.__str__())
        if not dcc_exe_path or not os.path.isfile(dcc_exe_path):
            raise DCCExeNotFoundError(ErrorCode.DCCExeNotFoundError, self.dcc_version)

        return dcc_exe_path

    def analyze(self, cmd=None, env=None):
        self._update_analyze_status(JobStatus.STATUS_ANALYZE_DOING)

        self.check_file_version()
        if not self.dcc_exe_path:
            self.dcc_exe_path = self.find_dcc_exe()

        if env and hasattr(env, "update"):
            env.update({"PYTHONUTF8": "1"})
        else:
            env = {"PYTHONUTF8": "1"}

        script_path = os.path.join(os.path.dirname(__file__), "houdini/run.py")
        cmd = cmd or [self.dcc_exe_path, script_path, "-input", self.dcc_file, "-output", self.info_path]
        self.logger.info("Running command: {}".format(cmd))

        code, stderr = renderg_utils.run_cmd(cmd, shell=True, env=env)
        if code != 0:
            error_msg = stderr or "analyze exits unexpectedly"
            self._update_analyze_status(JobStatus.STATUS_ANALYZE_FAILED, error_msg)
            raise AnalyzeFailError(ErrorCode.AnalyzeFailError, error_msg)

        if not os.path.isfile(self.info_path):
            error_msg = "info.cfg not found. info_path=".format(self.info_path)
            self._update_analyze_status(JobStatus.STATUS_ANALYZE_FAILED, error_msg)
            raise AnalyzeFailError(ErrorCode.AnalyzeFailError, error_msg)

        self._update_analyze_status(JobStatus.STATUS_ANALYZED)
        return self

    def _update_analyze_status(self, status, msg=""):
        self.api.job.update_job_status(self.job_id, status, msg)
