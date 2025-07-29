import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

# 默认日志级别
DEFAULT_LOG_LEVEL = logging.INFO

# 默认日志格式
DEFAULT_LOG_FORMAT = '%(asctime)s [%(levelname)s] - %(message)s'

# 默认日期格式
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 默认日志文件大小限制 (10MB)
DEFAULT_MAX_BYTES = 10 * 1024 * 1024

# 默认日志文件备份数量
DEFAULT_BACKUP_COUNT = 5

# 日志级别映射
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# 全局日志配置
_log_initialized = False
_default_logger = None


def setup_logger(name=None, level=None, log_file=None, console=True, 
                format_str=DEFAULT_LOG_FORMAT, date_format=DEFAULT_DATE_FORMAT,
                max_bytes=DEFAULT_MAX_BYTES, backup_count=DEFAULT_BACKUP_COUNT):
    """
    设置并返回一个配置好的日志记录器
    
    Args:
        name (str, optional): 日志记录器名称，默认为None使用根记录器
        level (str/int, optional): 日志级别，可以是字符串('debug', 'info'等)或日志级别常量
        log_file (str, optional): 日志文件路径，如果不提供则不记录到文件
        console (bool, optional): 是否输出到控制台，默认为True
        format_str (str, optional): 日志格式字符串
        date_format (str, optional): 日期格式字符串
        max_bytes (int, optional): 日志文件最大字节数
        backup_count (int, optional): 备份文件数量
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 获取日志级别
    if level is None:
        level = DEFAULT_LOG_LEVEL
    elif isinstance(level, str):
        level = LOG_LEVELS.get(level.lower(), DEFAULT_LOG_LEVEL)
    
    # 获取或创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 清除现有处理器
    for handler in logger.handlers[:]:  
        logger.removeHandler(handler)
    
    # 创建格式化器
    formatter = logging.Formatter(format_str, date_format)
    
    # 添加控制台处理器
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 添加文件处理器
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 创建滚动文件处理器
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def init_logging(level=None, log_dir=None, console=True):
    """
    初始化全局日志配置
    
    Args:
        level (str/int, optional): 日志级别
        log_dir (str, optional): 日志目录，如果提供则会在该目录下创建日志文件
        console (bool, optional): 是否输出到控制台
    """
    global _log_initialized, _default_logger
    
    # 如果已经初始化，则不再重复初始化
    if _log_initialized:
        return
    
    # 设置日志文件路径
    log_file = None
    if log_dir:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = time.strftime('%Y%m%d', time.localtime())
        log_file = os.path.join(log_dir, f'log/renderg_sdk_{timestamp}.log')
    
    # 设置根日志记录器
    _default_logger = setup_logger(
        name=None,  # 使用根记录器
        level=level,
        log_file=log_file,
        console=console
    )
    
    _log_initialized = True


def get_logger(name=None, log_dir=None, console=True):
    """
    获取一个日志记录器
    
    Args:
        name (str, optional): 日志记录器名称，默认为None使用根记录器
        log_dir (str, optional): 日志目录，如果提供则会在该目录下创建日志文件
        console (bool, optional): 是否输出到控制台

    Returns:
        logging.Logger: 日志记录器
    """
    global _log_initialized, _default_logger
    
    # 如果尚未初始化，则使用默认配置初始化
    if not _log_initialized:
        init_logging(log_dir=log_dir, console=console)
    
    # 如果请求的是根记录器，则返回默认记录器
    if name is None:
        return _default_logger
    
    # 否则返回指定名称的记录器
    return logging.getLogger(name)


# 便捷函数
def debug(msg, *args, **kwargs):
    get_logger().debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    get_logger().info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    get_logger().warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    get_logger().error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    get_logger().critical(msg, *args, **kwargs)


# 别名
warn = warning