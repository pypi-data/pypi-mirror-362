### 准备

1. 创建虚拟环境

   ```shell
   python -m venv venv
   ```

2. 安装 renderg-sdk

   ```shell
   pip install renderg-sdk
   ```

3. 创建配置文件 `config.json`

   ```shell
   {
     "AUTH_KEY": "*******************",
     "CLUSTER_ID": 27,
     "PROJECT_ID": 21479,
     "ENV_ID": 7715,
     "ZONE_ID": 1003,
     "RAM_LIMIT": "64G"
   }
   ```

- AUTH_KEY 用户身份认证，请联系 [RenderG 渲染农场](https://www.renderg.com/)平台技术支持获取；
- CLUSTER_ID 区域 ID ，一般为固定；
- PROJECT_ID，提交任务默认项目，在客户端项目管理中创建；
- ENV_ID ，提交任务默认环境，在客户端环境管理中创建；
- ZONE_ID，提交任务默认配置，默认请使用 1003；
- RAM_LIMIT，提交任务默认内存配置，64G、128G、256G 可选；

### 分析资产并上传

```python
import os

from renderg_utils import utils, log
from analyze_houdini import AnalyzeHoudini
from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_api.param_check import RenderGParamChecker
from renderg_transfer.RGUpload import RenderGUpload
from renderg_transfer.RGDownload import RenderGDownload


# ========分析资产和设置渲染参数==========

# 1. 读取配置文件并设置工作目录
config = utils.read_json("./config.json")
workspace = config.get("WORKSPACE", os.path.expandvars("%userprofile%/RenderG_WorkSpace"))

# 2. 设置日志模块
log.init_logging(log_dir=utils.get_workspace(workspace), console=True)
logger = log.get_logger()
logger.info("SDK Version: {}".format(utils.get_version()))


# 3.  创建任务信息
api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])

analyze_info = {
    "dcc_file": r"D:\houdini_file\JSBL_lgt_qunji_wmy_v001.hip", # DCC 文件路径
    "dcc_version": "19.0.622", # DCC 版本号
    "api": api, # RenderGAPI 实例
    "project_id": config["PROJECT_ID"],  # 项目ID
    "env_id": config["ENV_ID"],  # 环境ID
    "workspace": workspace,  # 工作目录
    "logger": logger, # 日志记录器
}
# 4. 分析资产列表和场景渲染参数
analyze_obj = AnalyzeHoudini(**analyze_info)
analyze_obj.analyze()
logger.info(analyze_obj.info_path)

# 5. 设置选择参数信息
param_check_obj = RenderGParamChecker(api, analyze_obj)
render_params = {
    "ChunkSize": 1,  # 一机多帧
    "Mark": "",  # 任务备注信息
    "PriorityFrames": "010:",  # 优先渲染帧 例：101:100-108x2 代表渲染首尾帧和100-108步长为2的帧

    "zone_id": config["ZONE_ID"],  # CPU 配置信息
    "ram_limit": config["RAM_LIMIT"],  # 内存配置
}
param_check_obj.set_houdini_render_node({
    "/node/path/to/render": "1001-1100",
    "/node/path/to/render/1": "100-1100",
})

param_check_obj.execute(**render_params)

# ========上传任务并提交==========
# 1. 获取 info.cfg 和 任务 ID 信息
info_path = analyze_obj.info_path
job_id = analyze_obj.job_id

# 2. 配置上传任务信息 
upload_kwargs = {
    "api": api,
    "job_id": job_id,
    "info_path": info_path,
    "line": TransferLines.LINE_UNICOM,
    "speed": 200  # 上传速度限制，单位为 Mbps
}
# 3. 开始上传
renderg_upload = RenderGUpload(**upload_kwargs)
renderg_upload.upload()

# 4. 上传完成，提交任务，开始渲染
submit = api.job.submit_job(job_id)
logger.info(submit["msg"])

# 5. 下载
# 等待任务完成下载
download_kwargs = {
    "api": api,
    "job_id": job_id,
    "download_path": "d:/test",  # 下载保存到本地路径
    "line": TransferLines.LINE_UNICOM,
    "cluster_id": config["CLUSTER_ID"],
    "speed": 500  # 上传速度限制，单位为 Mbps
}
renderg_sync = RenderGDownload(**download_kwargs)
result = renderg_sync.auto_download_after_job_completed()

'''
# 自定义下载
download_others_json = {
    "api": api,
    "job_id": None,
    "download_path": "d:/test",  # 下载保存到本地路径
    "line": TransferLines.LINE_UNICOM,
    "cluster_id": config["CLUSTER_ID"],
    "speed": 3000  # 上传速度限制，单位为 Mbps
}
server_path = {
    "/{job_id}".format(job_id=job_id)
}  # 提供待下载目录列表
renderg_sync = RenderGDownload(**download_others_json)
renderg_sync.custom_download(server_path)
'''
```



