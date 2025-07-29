import codecs
import copy
import json
import logging
import os
import subprocess
import sys
import traceback
import uuid

PY_VERSION = sys.version_info[0]
__version__ = '0.1.23'


def get_workspace(workspace=None):
    if workspace and os.path.isabs(workspace):
        return workspace
    else:
        return os.path.join(os.getenv("USERPROFILE"), "RenderG_WorkSpace")


def read_json(json_path, encoding='utf-8'):
    if os.path.exists(json_path):
        with codecs.open(json_path, 'r', encoding=encoding) as f:
            data = json.load(f)
        return data


def write_json(file_path, data, encoding="utf-8", ensure_ascii=True):
    with codecs.open(file_path, 'w', encoding=encoding) as f:
        if PY_VERSION == 3:
            json.dump(data, f, ensure_ascii=ensure_ascii, indent=4)
        else:
            f.write(str(json.dumps(data, ensure_ascii=ensure_ascii, indent=4)))


def check_path(path):
    """
    check the system path, create path if it's not exists

    :param path: a system path
    :return: None
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def run_cmd(cmd, shell=False, env=None):
    logger = logging.getLogger("run_cmd")
    if PY_VERSION == 2:
        cmd = str(cmd).encode(sys.getfilesystemencoding())

    current_env = env

    if env and hasattr(env, "items"):
        current_env = copy.deepcopy(os.environ)
        for k, v in env.items():
            if k.lower() == 'path':
                current_env[k] = current_env[k].rstrip(os.pathsep) + os.pathsep + v
            else:
                current_env[k] = v

    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell, env=current_env)
    while popen.poll() is None:
        result_line = popen.stdout.readline().strip()
        if result_line:
            logger.info(result_line.decode('utf-8', 'ignore'))

    stdout, stderr = popen.communicate()
    return popen.returncode, stderr


def get_dcc_file_version(file_path, regex):
    version = ''

    with open(file_path, 'rb') as read_obj:
        while True:
            line = read_obj.readline()
            if not line:
                break
            try:
                line = line.decode('utf-8', 'ignore')
            except BaseException as err:
                pass

            res = regex.search(line)
            if res:
                ver = res.groupdict()
                version = ver.get('version').strip()
                break
    return version


def get_version():
    return __version__


def get_pc_ip():
    try:
        try:
            return [
                ip for ip in os.popen(r'C:\Windows\System32\route print').readlines()
                if ' 0.0.0.0 ' in ip
            ][0].split()[-2]
        except BaseException as err:
            import socket
            return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        return '0.0.0.0'


def get_pc_version():
    try:
        import platform
        return platform.platform()
    except Exception as err:
        return ''


def get_pc_name():
    try:
        return f'{os.getlogin()}'
    except Exception as e:
        return 'SYSTEM'


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


class SceneType:
    max = '3dsmax'
    maya = 'maya'
    houdini = 'houdini'
    clarisse = 'clarisse'
    c4d = 'c4d'
    katana = 'katana'
    blender = 'blender'

    @staticmethod
    def get_scene_file_type(scene_name):
        try:
            scene_type = os.path.splitext(scene_name.lower())[1]
            if scene_type in ['.ma', '.mb']:
                return SceneType.maya
            elif scene_type in ['.hip']:
                return SceneType.houdini
            elif scene_type in ['.project']:
                return SceneType.clarisse
            elif scene_type in ['.max']:
                return SceneType.max
            elif scene_type in ['.c4d']:
                return SceneType.c4d
            elif scene_type in ['.katana']:
                return SceneType.katana
            elif scene_type in ['.blend']:
                return SceneType.blender
        except Exception as e:
            traceback.print_exc()
        return ''
