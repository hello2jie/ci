import os
import logging

log_dir_path = os.path.dirname(__file__)

log_level = logging.DEBUG

normal_log_path = f'{log_dir_path}/logs/debug.log'

warn_log_path = f'{log_dir_path}/logs/warn.log'

error_log_path = f'{log_dir_path}/logs/error.log'


"""
自建日志
"""

# 日志格式管理
formatter = logging.Formatter(
    '%(asctime)s %(process)d %(thread)d %(pathname)s:%(lineno)d %(levelname)s %(message)s')
error_formatter = logging.Formatter((
    '%(asctime)s %(process)d '
    '%(thread)d %(pathname)s '
    '%(pathname)s:%(lineno)d '
    '%(levelname)s %(message)s'
))

logger = logging.getLogger('DubangAssurance_logger')
logger.setLevel(log_level)

# 一般日志存放地址
loghd_info = logging.FileHandler(normal_log_path, encoding='utf-8')
loghd_info.setFormatter(formatter)
loghd_info.setLevel(log_level)


# 警告日志，但文件存放，考虑到，应用存在优化空间，单独存放warn提供优化思路和提前预知隐患bug
logger_single_warn = logging.getLogger("logger_single_warn")
logger_single_warn.setLevel(logging.WARN)
loghd_single_warn = logging.FileHandler(warn_log_path, encoding='utf-8')
loghd_single_warn.setFormatter(formatter)
loghd_single_warn.setLevel(logging.WARN)

# 错误级别以上的日志单独存放，方便查找问题
loghd_error = logging.FileHandler(error_log_path, encoding='utf-8')
loghd_error.setFormatter(error_formatter)
loghd_error.setLevel(logging.ERROR)

# handler管理
logger.addHandler(loghd_info)
# logger.addHandler(filehandler)
logger.addHandler(loghd_single_warn)
logger.addHandler(loghd_error)
