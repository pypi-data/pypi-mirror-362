import os
from renderg_transfer.TransferHelper import TransferConstants, TransferHelper


class AssetsPathHelper:

    @staticmethod
    def get_file_list_for_info_cfg(info_path, job_id):
        source_paths = []
        dest_paths = []

        if os.path.isfile(info_path):
            info_json = TransferHelper.read_json(info_path)
            if info_json:
                source_paths, dest_paths = AssetsPathHelper.__get_file_list_for_info_cfg(
                    job_id, info_json, TransferConstants.ASSETS, info_path)

        return source_paths, dest_paths

    @staticmethod
    def __get_file_list_for_info_cfg(job_id, info_json, key, info_path=None):
        source_paths = []
        dest_paths = []

        assets_list = info_json.get(key)
        for path_dict in assets_list:
            full_path = TransferHelper.handing_local_paths(
                path_dict.get(TransferConstants.FULL_PATH)
            )
            remote_name = TransferHelper.handing_local_paths(
                path_dict.get(TransferConstants.REMOTE_NAME)
            )
            file_type = int(path_dict.get(TransferConstants.FILE_TYPE))
            missing = int(path_dict.get(TransferConstants.MISSING))
            if missing == 0:
                if file_type == 1:
                    source_paths.append(full_path)
                    dest_paths.append(
                        AssetsPathHelper.assemble_server_cfg_path(job_id, full_path)
                    )
                elif file_type == 2:
                    local_paths, server_paths = \
                        AssetsPathHelper.assemble_server_input_path(full_path, remote_name)
                    source_paths.append(local_paths)
                    dest_paths.append(server_paths)

        if os.path.isfile(info_path):
            source_paths.insert(0, info_path)
            dest_paths.insert(0, AssetsPathHelper.assemble_server_cfg_path(job_id, info_path))

        return source_paths, dest_paths

    @staticmethod
    def assemble_server_cfg_path(job_id, path):
        filename = os.path.basename(path)
        cfg_path = 'cfg/{job_id}/{filename}'.format(job_id=job_id, filename=filename)
        return cfg_path.replace('\\', '/')

    @staticmethod
    def assemble_server_input_path(local_path, remote_name):
        norma_path = TransferHelper.handing_local_paths(os.path.normpath(local_path))
        norma_name = TransferHelper.handing_local_paths(os.path.normpath(remote_name))

        split_path = norma_name.split(':')
        if len(split_path) == 2:
            driver = split_path[0].upper().strip('/')
            file = split_path[1].strip('/')
            server_path = 'input/{driver}/{file}'.format(driver=driver, file=file)
        else:
            split_path = norma_name.split('/')
            if len(split_path) >= 2:
                driver_name = split_path[0].split('_')
                if len(driver_name) == 2:
                    driver = driver_name[1].upper().strip('/')
                    file = '/'.join(split_path[1:])
                    file = file.strip('/')
                    server_path = 'input/{driver}/{file}'.format(driver=driver, file=file)
                else:
                    if TransferHelper.is_unc_path(norma_name):
                        server_path = 'input/UNC/{}'.format(norma_name.strip("/"))
                    else:
                        server_path = 'input/{}'.format(norma_name.strip("/"))
            else:
                server_path = os.path.join('input/{}'.format(norma_name.strip("/")))

        return norma_path.replace('\\', '/'), server_path.replace('\\', '/')
