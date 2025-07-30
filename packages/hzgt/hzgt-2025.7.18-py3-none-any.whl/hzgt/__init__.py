# 版本
from .__version import __version__
version = __version__

# core
from .core import *


__all__ = [
    "version",
] + [
    "pic", "restrop",
    "bitconv", "getfsize", "ensure_file", "make_filename",
    "gettime", "vargs",
    "set_log", "ContextLogger", "BoundContextLogger",
    "getip", "validate_ip",
    "AutoConfig",
    "is_admin", "require_admin", "execute_command", "run_as_admin", "check_admin_and_prompt",
]

