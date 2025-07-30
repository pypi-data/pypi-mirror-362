import json
import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler
from typing import Optional, Union, Dict, Any, List

from hzgt.core import ensure_file, vargs, restrop, make_filename

LOG_LEVEL_DICT = {
    0: logging.NOTSET,
    1: logging.DEBUG,
    2: logging.INFO,
    3: logging.WARNING,
    4: logging.ERROR,
    5: logging.CRITICAL,

    logging.NOTSET: logging.NOTSET,
    logging.DEBUG: logging.DEBUG,
    logging.INFO: logging.INFO,
    logging.WARNING: logging.WARNING,
    logging.ERROR: logging.ERROR,
    logging.CRITICAL: logging.CRITICAL,

    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "fatal": logging.CRITICAL,
    "critical": logging.CRITICAL,

    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "FATAL": logging.CRITICAL,
    "CRITICAL": logging.CRITICAL,
}

LEVEL_NAME_DICT = {
    0: "NOTSET",
    1: "DEBUG",
    2: "INFO",
    3: "WARNING",
    4: "ERROR",
    5: "CRITICAL",

    logging.NOTSET: "NOTSET",
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL",

    "notset": "NOTSET",
    "debug": "DEBUG",
    "info": "INFO",
    "warn": "WARNING",
    "warning": "WARNING",
    "error": "ERROR",
    "fatal": "CRITICAL",
    "critical": "CRITICAL",

    "NOTSET": "NOTSET",
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "WARN": "WARNING",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "FATAL": "CRITICAL",
    "CRITICAL": "CRITICAL",
}


class __ContextFilter(logging.Filter):
    """添加额外上下文信息的日志过滤器"""

    def __init__(self, extra_fields: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.extra_fields = extra_fields or {}

    def filter(self, record):
        # 添加基础上下文信息
        record.pid = os.getpid()
        record.thread_id = threading.get_ident()
        record.thread_name = threading.current_thread().name
        record.module_path = os.path.abspath(sys.argv[0])

        # 创建上下文字符串
        ctx_items = []

        # 添加自定义字段
        for key, value in self.extra_fields.items():
            setattr(record, key, value)
            ctx_items.append(f"{key}={value}")

        # 添加来自日志调用的上下文
        ctx_attrs = [attr for attr in dir(record) if attr.startswith("ctx_")]
        for attr in ctx_attrs:
            value = getattr(record, attr)
            # 去掉 ctx_ 前缀
            clean_key = attr[4:]
            ctx_items.append(f"{clean_key}={value}")

        # 设置上下文字符串属性
        record.ctx_str = ", ".join(ctx_items) if ctx_items else "None"

        return True


class __JSONFormatter(logging.Formatter):
    """结构化JSON日志格式化器 - 分离原始字段和上下文字段"""

    def __init__(self, *args, **kwargs):
        self.include_fields = kwargs.pop("include_fields", None)
        self.exclude_fields = kwargs.pop("exclude_fields", None)
        super().__init__(*args, **kwargs)

    def format(self, record):
        # 创建基础日志字典（原始日志字段）
        base_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "file": record.filename,
            "line": record.lineno,
            "function": record.funcName,
            "pid": getattr(record, "pid", os.getpid()),
            "thread_id": getattr(record, "thread_id", threading.get_ident()),
            "thread_name": getattr(record, "thread_name", threading.current_thread().name),
        }

        # 添加异常信息
        if record.exc_info:
            base_record["exception"] = self.formatException(record.exc_info)

        # 创建上下文字典（用户传入的字段）
        context_record = {}

        # 收集所有 ctx_ 前缀的字段
        for attr in dir(record):
            if attr.startswith("ctx_"):
                # 去掉 ctx_ 前缀
                clean_key = attr[4:]
                # 排除特殊字段（如 ctx_str）
                if clean_key not in ["str", "json_enabled", "log_level", "log_path"]:
                    value = getattr(record, attr)
                    context_record[clean_key] = value

        # 处理 ctx_str 字段（如果存在）
        if hasattr(record, "ctx_str") and record.ctx_str and record.ctx_str != "None":
            # 解析 ctx_str 为键值对
            try:
                for item in record.ctx_str.split(", "):
                    if "=" in item:
                        key, value = item.split("=", 1)
                        # 只添加不在 context_record 中的键
                        if key not in context_record:
                            context_record[key] = value
            except Exception as e:
                context_record["ctx_str_parse_error"] = f"Error parsing ctx_str: {str(e)}"
                context_record["ctx_str"] = record.ctx_str

        # 创建最终日志记录
        log_record = {
            "log": base_record,  # 原始日志字段
            "context": context_record  # 用户传入的上下文字段
        }

        # 字段过滤
        if self.include_fields:
            # 分别过滤基础日志字段和上下文字段
            filtered_base = {k: v for k, v in base_record.items() if k in self.include_fields}
            filtered_context = {k: v for k, v in context_record.items() if k in self.include_fields}
            log_record = {"log": filtered_base, "context": filtered_context}

        if self.exclude_fields:
            # 分别排除基础日志字段和上下文字段
            filtered_base = {k: v for k, v in base_record.items() if k not in self.exclude_fields}
            filtered_context = {k: v for k, v in context_record.items() if k not in self.exclude_fields}
            log_record = {"log": filtered_base, "context": filtered_context}

        return json.dumps(log_record, ensure_ascii=False)


@vargs({"level": set(LOG_LEVEL_DICT.keys())})
def set_log(
        name: Optional[str] = None,
        fpath: Optional[str] = "logs",
        fname: Optional[str] = None,
        level: Union[int, str] = 2,
        # 控制台日志配置
        console_enabled: bool = True,
        console_format: Optional[str] = None,
        # 文件日志配置
        file_enabled: bool = True,
        file_format: Optional[str] = None,
        # 结构化日志配置
        json_enabled: bool = False,
        json_include_fields: Optional[List[str]] = None,
        json_exclude_fields: Optional[List[str]] = None,
        # 通用配置
        datefmt: str = "%Y-%m-%d %H:%M:%S",
        maxBytes: int = 2 * 1024 * 1024,
        backupCount: int = 3,
        encoding: str = "utf-8",
        force_reconfigure: bool = False,
        # 上下文信息
        context_fields: Optional[Dict[str, Any]] = None,
        # 自定义处理器
        custom_handlers: Optional[List[logging.Handler]] = None
) -> logging.Logger:
    """
    创建或获取高级日志记录器，支持控制台、文件和JSON日志输出

    :param name: 日志器名称，None 表示根日志器
    :param fpath: 日志文件存放目录路径（默认同目录的logs目录里）
    :param fname: 日志文件名（默认："{name}.log"）
    :param level: 日志级别（默认: 2/INFO）

    :param console_enabled: 是否启用控制台日志（默认：True）
    :param console_format: 控制台日志格式（默认：结构化文本格式）

    :param file_enabled: 是否启用文件日志（默认：True）
    :param file_format: 文件日志格式（默认：详细文本格式）

    :param json_enabled: 是否启用JSON日志（默认：False）
    :param json_include_fields: JSON日志包含字段（默认：全部）
    :param json_exclude_fields: JSON日志排除字段（默认：无）

    :param datefmt: 日期格式（默认："%Y-%m-%d %H:%M:%S"）
    :param maxBytes: 日志文件最大字节数（默认：2MB）
    :param backupCount: 备份文件数量（默认：3）
    :param encoding: 文件编码（默认：utf-8）
    :param force_reconfigure: 强制重新配置现有日志器（默认：False）

    :param context_fields: 额外上下文字段（字典格式）
    :param custom_handlers: 自定义日志处理器列表

    :return: 配置好的日志记录器
    """
    # 获取日志器
    logger = logging.getLogger(name)

    # 检查是否已有处理器，避免重复添加
    if logger.handlers and not force_reconfigure:
        logger.setLevel(LOG_LEVEL_DICT[level])
        return logger

    # 清理现有处理器（如果需要重新配置）
    if force_reconfigure:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    # 设置日志级别
    logger.setLevel(LOG_LEVEL_DICT[level])
    logger.propagate = False  # 防止日志传播到根日志器

    # 添加上下文过滤器
    context_filter = __ContextFilter(context_fields)
    logger.addFilter(context_filter)

    # 默认日志格式
    if console_format is None:
        console_format = (
                restrop("[%(asctime)s] ", f=6) +
                restrop("[%(threadName)s] ", f=5) +
                restrop("[%(filename)s:%(lineno)-4d] ", f=4) +
                restrop("[%(levelname)-7s] ", f=3) +
                f"%(message)s" +
                restrop(" [%(ctx_str)s]", f=2)
        )

    if file_format is None:
        file_format = (
            "[%(asctime)s] " +
            "[%(threadName)s] " +
            "[%(filename)s:%(lineno)d] " +
            "%(levelname)-7s " +
            "%(message)s" +
            " [%(ctx_str)s]"  # 添加上下文信息
        )

    # 创建控制台处理器（如果启用）
    if console_enabled:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(console_format, datefmt=datefmt))
        logger.addHandler(stream_handler)

    # 创建文件处理器（如果启用）
    if file_enabled and fpath:
        # 确定日志文件名
        log_name = make_filename(name, fname=fname, suffix=".log")
        logfile = os.path.join(fpath, log_name)

        # 确保日志文件存在
        ensure_file(logfile)

        # 创建旋转文件处理器
        file_handler = RotatingFileHandler(
            filename=logfile,
            encoding=encoding,
            maxBytes=maxBytes,
            backupCount=backupCount
        )
        file_handler.setFormatter(logging.Formatter(file_format, datefmt=datefmt))
        logger.addHandler(file_handler)

    # 创建JSON日志处理器（如果启用）
    if json_enabled:
        # 确定JSON日志文件名
        json_log_name = make_filename(name, fname=fname,
                                      suffix=".json.log")  # 命名优先级 json_filename > fname > name
        json_logfile = os.path.join(fpath, json_log_name)

        # 确保日志文件存在
        ensure_file(json_logfile)

        # 创建JSON文件处理器
        json_handler = RotatingFileHandler(
            filename=json_logfile,
            encoding=encoding,
            maxBytes=maxBytes,
            backupCount=backupCount
        )

        # 设置JSON格式化器
        json_formatter = __JSONFormatter(
            datefmt=datefmt,
            include_fields=json_include_fields,
            exclude_fields=json_exclude_fields
        )
        json_handler.setFormatter(json_formatter)
        logger.addHandler(json_handler)

    # 添加自定义处理器
    if custom_handlers:
        for handler in custom_handlers:
            logger.addHandler(handler)

    # 记录配置信息
    logger.debug("日志器配置完成", extra={
        "ctx_log_level": LEVEL_NAME_DICT[level],
        "ctx_log_path": fpath,
        "ctx_json_enabled": json_enabled
    })

    return logger


class ContextLogger:
    """
    带上下文的日志记录工具类

    提供带上下文信息的日志记录方法，支持结构化日志字段
    """

    @staticmethod
    def log(
            logger: logging.Logger,
            level: Union[int, str],
            message: str,
            context: Optional[Dict[str, Any]] = None,
            exc_info: Optional[Union[bool, BaseException]] = None,
            stack_info: bool = False,
            stacklevel: int = 4  # 修改为4，跳过更多封装层
    ) -> None:
        """
        带上下文的日志记录方法

        :param logger: 日志记录器实例
        :param level: 日志级别
        :param message: 日志消息
        :param context: 上下文数据（字典）
        :param exc_info: 异常信息（True 或 Exception 实例）
        :param stack_info: 是否包含堆栈信息
        :param stacklevel: 堆栈级别（设置为4跳过封装层）
        """
        extra = {}
        if context:
            # 添加ctx_前缀以避免与日志记录字段冲突
            for key, value in context.items():
                extra[f"ctx_{key}"] = value

        log_level = LOG_LEVEL_DICT[level]
        logger.log(
            log_level,
            message,
            extra=extra,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel  # 传递堆栈级别
        )

    @staticmethod
    def debug(
            logger: logging.Logger,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        DEBUG级别带上下文的日志记录

        :param logger: 日志记录器实例
        :param message: 日志消息
        :param context: 上下文数据（字典）
        """
        # 显式设置堆栈级别为4

        ContextLogger.log(logger, logging.DEBUG, message, context, **kwargs)

    @staticmethod
    def info(
            logger: logging.Logger,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        INFO级别带上下文的日志记录

        :param logger: 日志记录器实例
        :param message: 日志消息
        :param context: 上下文数据（字典）
        """

        ContextLogger.log(logger, logging.INFO, message, context, **kwargs)

    @staticmethod
    def warning(
            logger: logging.Logger,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        WARNING级别带上下文的日志记录

        :param logger: 日志记录器实例
        :param message: 日志消息
        :param context: 上下文数据（字典）
        """

        ContextLogger.log(logger, logging.WARNING, message, context, **kwargs)

    @staticmethod
    def error(
            logger: logging.Logger,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        ERROR级别带上下文的日志记录

        :param logger: 日志记录器实例
        :param message: 日志消息
        :param context: 上下文数据（字典）
        """

        ContextLogger.log(logger, logging.ERROR, message, context, **kwargs)

    @staticmethod
    def critical(
            logger: logging.Logger,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        CRITICAL级别带上下文的日志记录

        :param logger: 日志记录器实例
        :param message: 日志消息
        :param context: 上下文数据（字典）
        """

        ContextLogger.log(logger, logging.CRITICAL, message, context, **kwargs)

    @classmethod
    def with_logger(cls, logger: logging.Logger) -> 'BoundContextLogger':
        """
        创建绑定到特定日志记录器的上下文日志记录器

        :param logger: 要绑定的日志记录器实例
        :return: 绑定后的上下文日志记录器
        """
        return BoundContextLogger(logger)


class BoundContextLogger:
    """
    绑定到特定日志记录器的上下文日志记录器
    """

    def __init__(self, logger: logging.Logger):
        """
        初始化绑定上下文日志记录器

        :param logger: 绑定的日志记录器实例
        """
        self.logger = logger

    def log(
            self,
            level: Union[int, str],
            message: str,
            context: Optional[Dict[str, Any]] = None,
            exc_info: Optional[Union[bool, BaseException]] = None,
            stack_info: bool = False,
            stacklevel: int = 4  # 调用堆栈层次
    ) -> None:
        """
        带上下文的日志记录方法

        :param level: 日志级别
        :param message: 日志消息
        :param context: 上下文数据（字典）
        :param exc_info: 异常信息（True 或 Exception 实例）
        :param stack_info: 是否包含堆栈信息
        :param stacklevel: 堆栈级别（设置为3跳过一层封装）
        """
        ContextLogger.log(
            self.logger,
            level,
            message,
            context,
            exc_info,
            stack_info,
            stacklevel
        )

    def debug(
            self,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        DEBUG级别带上下文的日志记录

        :param message: 日志消息
        :param context: 上下文数据（字典）
        """
        self.log(logging.DEBUG, message, context, **kwargs)

    def info(
            self,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        INFO级别带上下文的日志记录

        :param message: 日志消息
        :param context: 上下文数据（字典）
        """
        self.log(logging.INFO, message, context, **kwargs)

    def warning(
            self,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        WARNING级别带上下文的日志记录

        :param message: 日志消息
        :param context: 上下文数据（字典）
        """

        self.log(logging.WARNING, message, context, **kwargs)

    def error(
            self,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        ERROR级别带上下文的日志记录

        :param message: 日志消息
        :param context: 上下文数据（字典）
        """

        self.log(logging.ERROR, message, context, **kwargs)

    def critical(
            self,
            message: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> None:
        """
        CRITICAL级别带上下文的日志记录

        :param message: 日志消息
        :param context: 上下文数据（字典）
        """

        self.log(logging.CRITICAL, message, context, **kwargs)


