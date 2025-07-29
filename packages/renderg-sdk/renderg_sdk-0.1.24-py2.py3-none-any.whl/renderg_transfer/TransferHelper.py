
import os
import json
import re
import time
import traceback

import renderg_utils


class TransferConstants:

    ASSETS = 'Assets'
    FULL_PATH = 'FullPath'
    REMOTE_NAME = 'RemoteName'
    FILE_TYPE = 'FileType'
    MISSING = 'missing'


class TransferHelper:

    @staticmethod
    def read_json(file_path):
        encoding_list = ['utf-8-sig', 'utf-8', 'None', 'gb2312']
        for encoding in encoding_list:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    info_json = json.loads(f.read())
                return info_json
            except BaseException as e:
                traceback.print_exc()
        return {}

    @staticmethod
    def is_unc_path(path):
        upc_match = re.search(r'/?/?'
                              r'(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3})'  # ip
                              r'|'
                              r'([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?)'  # 域名
                              r'/.+', path)
        if upc_match:
            return True
        return False

    @staticmethod
    def handing_local_paths(paths):
        """

        Args:
            path: 本地文件路径

        Returns:
            规范路径后的本地文件路径
            :param paths:
        """
        if isinstance(paths, list):
            new_paths = []
            for path in paths:
                norma_path = os.path.normpath(path)
                norma_path.replace('\\', '/')
                new_paths.append(norma_path)
            return new_paths
        else:
            norma_path = os.path.normpath(paths)
            return norma_path.replace('\\', '/')

    @staticmethod
    def get_ascp_executable():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.abspath(os.path.join(current_dir, "../ascp/bin/ascp.exe"))
        return executable

    @classmethod
    def create_file_pair_list_file(cls, workspace, source_paths, dest_paths):
        timestamp = time.time()
        formatted_time = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        file_path = os.path.join(
            workspace, "temp", 'transfer_files_{}.txt'.format(formatted_time)
        )
        renderg_utils.check_path(os.path.dirname(file_path))

        flist = [path for pair in zip(source_paths, dest_paths) for path in pair]
        with open(file_path, 'wb') as pf:
            pf.write('\n'.join(flist).encode('utf-8'))
            pf.write('\n'.encode('utf-8'))
        return file_path

    @classmethod
    def create_ascp_command(cls, cmd_pass, mode, host, port, username,
                            resume_check="2", max_speed=1000, log_dir="", pair_list_file="",
                            source_path=None, dest_path=None):
        ascp_executable = cls.get_ascp_executable()

        cmd = ('{cmd_pass}&& {ascp_dir} -P {port} -O {port} -T -l{speed}m --mode={mode} '
               '-k{resume_check} --policy=fair --overwrite=diff --user={username} -d --host={host} '
               '-Efiles.txt').format(
                username=username, cmd_pass=cmd_pass, ascp_dir=ascp_executable,
                host=host, port=port, speed=max_speed, mode=mode, resume_check=resume_check)
        if log_dir:
            cmd += " -L {log_path}".format(log_path=log_dir)

        if pair_list_file:
            cmd += " --file-pair-list={file_pair_list_path} .".format(file_pair_list_path=pair_list_file)

        if source_path:
            cmd += " {source_path}".format(source_path=source_path)

        if dest_path:
            cmd += " {dest_path}".format(dest_path=dest_path)

        return cmd
