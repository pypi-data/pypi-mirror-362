"""
项目安全日志记录器的主入口
当导入此包时，自动执行安全检测和启动日志记录。
"""
from .security import perform_security_check

# 当导入包时自动执行安全检测
perform_security_check()