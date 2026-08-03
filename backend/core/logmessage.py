import logging
import logging.config
from enum import Enum

import backend.core.logconfig as logconfig
import systeminfo


class LogLevel(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3


class LogMessage:
    def __init__(self):
        self.message = None
        self.msg_dict = {}
        logconfig.do_config()
        self.logger = logging.getLogger("SLW Testing Suite UI")
        self.sysinfo = systeminfo.SystemInfo()

    @staticmethod
    def substitute_placeholder(logmessage, placeholder_dict):
        substituted_message = logmessage

        for replacement_key in placeholder_dict:
            substituted_message = substituted_message.replace(
                replacement_key, placeholder_dict[replacement_key]
            )

        return substituted_message

    def log_message(
        self,
        loglevel=LogLevel.INFO,
        logmessage=None,
        placeholder_dict=None,
        func_name=None,
        module_name=None,
    ):
        self.message = "(" + module_name + ") " if module_name is not None else "(?) "
        self.message += "(" + func_name + ") " if func_name is not None else "(?) "
        self.message += logmessage if logmessage is not None else "No Message!"

        if placeholder_dict is not None and len(placeholder_dict) > 0:
            self.message = self.substitute_placeholder(self.message, placeholder_dict)

        return self.write_log_message(loglevel)

    def write_log_message(self, log_level):

        if log_level == LogLevel.INFO:
            self.logger.info(self.message, extra={"user": self.sysinfo.user()})
        elif log_level == LogLevel.WARNING:
            self.logger.warning(self.message, extra={"user": self.sysinfo.user()})
        elif log_level == LogLevel.ERROR:
            self.logger.error(self.message, extra={"user": self.sysinfo.user()})
        elif log_level == LogLevel.CRITICAL:
            self.logger.critical(self.message, extra={"user": self.sysinfo.user()})
        else:
            error = f"Wrong Log Level ({log_level})!"
            self.logger.error(error, extra={"user": self.sysinfo.user()})
            return False, error

        return True, None
