import configparser
import pathlib
import os
import backend.core.logmessage as logmessage


class Configuration:
    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=None)
        self.logmsg = logmessage.LogMessage()

    def load_configuration(self, config_file):
        if not pathlib.Path(config_file).exists():
            error = f"Configuration file <{config_file}> not found!"
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.CRITICAL,
                logmessage=error,
                func_name="load_configuration",
            )
            return False, error

        self.config.read(config_file, encoding="utf-8")

        return True, None

    def section_values(self, section):
        try:
            return dict(self.config.items(section=section)), None
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.ERROR,
                logmessage=str(error),
                func_name="section_values",
                module_name=os.path.basename(__file__),
            )
            return {}, str(error)

    def string_value(self, section, key):
        try:
            return self.config.get(section=section, option=key), None
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.ERROR,
                logmessage=str(error),
                func_name="string_value",
                module_name=os.path.basename(__file__),
            )
            return None, str(error)

    def bool_value(self, section, key):
        try:
            return self.config.getboolean(section=section, option=key), None
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.ERROR,
                logmessage=str(error),
                func_name="bool_value",
                module_name=os.path.basename(__file__),
            )
            return False, str(error)

    def int_value(self, section, key):
        try:
            return self.config.getint(section=section, option=key), None
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.ERROR,
                logmessage=str(error),
                func_name="int_value",
                module_name=os.path.basename(__file__),
            )
            return 0, str(error)

    def float_value(self, section, key):
        try:
            return self.config.getfloat(section=section, option=key), None
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.ERROR,
                logmessage=str(error),
                func_name="float_value",
                module_name=os.path.basename(__file__),
            )
            return 0, str(error)

    def dict_value(self, section, key):
        try:
            return eval(self.config.get(section=section, option=key)), None
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.ERROR,
                logmessage=str(error),
                func_name="dict_value",
                module_name=os.path.basename(__file__),
            )
            return {}, str(error)

    def create_configfile(self, file_name, sections, keys):
        newfile = configparser.ConfigParser(interpolation=None)
        for section in sections:
            newfile[section] = keys[section]

        try:
            with open(file=file_name, mode="w", encoding="utf-8") as file:
                newfile.write(file)
                file.flush()
                file.close()
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.CRITICAL,
                logmessage=str(error),
                func_name="create_configfile",
                module_name=os.path.basename(__file__),
            )
            return False, str(error)

        return True, None

    def update_configfile(self, file_name, section, values):
        for key in values:
            try:
                self.config.set(section=section, option=key, value=str(values[key]))
            except Exception as error:
                self.logmsg.log_message(
                    loglevel=logmessage.LogLevel.CRITICAL,
                    logmessage=str(error),
                    func_name="update_configfile",
                    module_name=os.path.basename(__file__),
                )
                return False, str(error)

        try:
            with open(file=file_name, mode="w", encoding="utf-8") as file:
                self.config.write(file)
                file.flush()
                file.close()
        except Exception as error:
            self.logmsg.log_message(
                loglevel=logmessage.LogLevel.CRITICAL,
                logmessage=str(error),
                func_name="update_configfile",
                module_name=os.path.basename(__file__),
            )
            return False, str(error)

        return True, None
