import json
import os
import sys
from os.path import expanduser

import netifaces
from mpt import settings
from simple_term_menu import TerminalMenu

from mpt import logger

from colorama import Fore, Back, Style


CONFIG = 'settings.json'
CONFIG_DIR = '.mpt'
CONFIG_ITEMS = {'access-point', 'application-label', 'pentest-dir', 'app', 'package-name', 'proxy', 'install-dir'}
PROXY_PORT = '8080'
PROXY_SERVER = '127.0.0.1'
ACCESS_POINT_IP = '192.168.75.1'


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class Config:

    def __init__(self):
        self.log = logger.getLogger()
        config_dir = os.path.join(settings.HOME_FOLDER, CONFIG_DIR)
        if not os.path.isdir(config_dir):
            self.log.debug("Config directory {config_dir} does not exits")
            os.makedirs(config_dir, exist_ok=True)
            self.log.info("Config directory {config_dir} created")

        self.config_path = os.path.join(config_dir, CONFIG)
        self.config_dict = self.load()


    # TODO Refactor this code. Method yes_no is a copy from tmp.functions
    def yes_no(self, message):
        options = ["Yes", "No"]
        terminal_menu = TerminalMenu(options, title=message)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            return True
        else:
            return False

    def print(self):
        """
    Print configuration file
    """
        self.log.info(f"Configuration file: {self.config_path}")
        config_json = json.dumps(self.config_dict, indent=4)
        print(config_json)

    def update(self, config_name, config_value):
        """
    Update configuration file to the following structure
    @see __write_config for more details

    :param config_name:
    :param config_value:
    :return:
    """
        if not os.path.isfile(self.config_path):
            self.log.error(f"Configuration file {self.config_path} missing")
            sys.exit(3)

        if config_name in CONFIG_ITEMS:

            self.config_dict.update({config_name: config_value})
            self.__write_config(self.config_dict)
            self.config_dict = self.load()
            self.log.info(f"Updated config: {config_name}")
        else:
            self.log.error(
                f"Configuration error: Key \"{config_name}\" not found. Skip adding value \"{config_value}\"")

    def __write_config(self, config_dict):
        """
    # private method

      # configuration file
      {
        "pentest-dir": "/path/to/pentest-YYYY-MM-DD",
        "app": "app/file.apk",
        "install-dir": "tools/MOBILE/"
        "package-name": "com.example.app",
        "proxy": {
            "host": "127.0.0.1",
            "port": "8080"
        }
      }

    Write python dict object as json config file
    :param config_dict:
    :return:
    """

        # set default values
        for conf in config_dict.keys():
            if conf not in CONFIG_ITEMS:
                self.log.error(f"Unknown config key \"{conf}\". Configuration writing not possible")
                sys.exit(1)

        # write config file
        with open(self.config_path, 'w') as json_file:
            self.log.debug(f"Writing config dict to file: {config_dict}")
            # pretty json
            json.dump(config_dict, json_file, indent=4, sort_keys=True)
            json_file.close()

        if os.path.isfile(self.config_path):
            self.log.debug(f"Configuration file {self.config_path} updated")

    def load(self):
        """
    Loads configuration json file from path and return a dict

    :return:
    """

        self.config_dict = {}

        # load existing config file
        if os.path.isfile(self.config_path):

            with open(self.config_path, 'r') as json_file:
                self.config_dict = json.load(json_file)
                json_file.close()

                # set default value, after version update if the configuration does not exist
                for conf in CONFIG_ITEMS:
                    if conf not in self.config_dict.keys():
                        self.log.warn(f"config key \"{conf}\" not found. Set default value.")
                        self.update(conf, "")

                # load pretty json
                # config_json = json.dumps(config_dict, indent=4)
                # print(config_json)
                return self.config_dict

        # create a new config file
        else:

            # set default values
            self.log.info(f'Configuration file {self.config_path} missing. Init a new config ...')

            # set default installation folder
            self.set_tool_folder()

            # set default properties
            for conf in CONFIG_ITEMS:
                if conf not in self.config_dict.keys():
                    self.log.debug(f"config key \"{conf}\" not found. Set default value.")
                    self.config_dict.update({conf: ""})

            self.config_dict.update({'proxy': {'host': PROXY_SERVER, 'port': PROXY_PORT}})
            # access point configuration is set in console.configure_access_point()

            self.__write_config(self.config_dict)
            self.log.debug(f'Configuration file {self.config_path} created')

    def load_config(self, setting_name):

        self.load()
        # check settings_name as key
        for conf in self.config_dict.keys():
            if conf not in CONFIG_ITEMS:
                self.log.error(f"Unknown config key \"{conf}\". Loading key failed")
                self.log.warn(f"in case you are not able to start the application try to update with command 'mpt --update' or "
                              f"try to delete configuration file {self.config_path} and start the application again")
                sys.exit(1)

        self.log.debug(f"Loading config \"{setting_name}\" from {self.config_path}")

        try:
            return self.config_dict[setting_name]
        except KeyError:
            return None

    def set_tool_folder(self):

        # define MOBILE_FOLDER variable and create this folder, if not exists

        tool_dir = settings.DEFAULT_MOBILE_FOLDER
        self.log.info("Please set a default installation folder for tools")

        use_tool_dir = self.yes_no(
            'Would you use this directory \"{}\" ? '.format(tool_dir))

        if not use_tool_dir:
            tool_dir = self.get_custom_tool_dir(tool_dir)

        if os.path.isdir(tool_dir):
            self.config_dict.update({'install-dir': tool_dir})
        else:
            self.log.warn(f"Folder \"{tool_dir}\" does not exists and will be created")
            try:
                os.makedirs(tool_dir)
                self.config_dict.update({'install-dir': tool_dir.strip()})
            except OSError as e:
                self.log.error(f"Folder {tool_dir} could not be created")
                self.set_tool_folder()

    def get_custom_tool_dir(self, tool_dir):
        r = 0
        while True:
            tmp_tool_dir = input("Please put absolute path to installation folder for tools: ")

            use_tool_dir = self.yes_no('Would you use this directory {} ? '.format(tmp_tool_dir))
            if use_tool_dir:
                if not tmp_tool_dir.startswith("/"):
                    self.log.warn("that is not absolute path, select another folder")
                    return self.get_custom_tool_dir(tmp_tool_dir)
                else:
                    return tmp_tool_dir
            else:
                return self.get_custom_tool_dir(tmp_tool_dir)

    def get_uniq_ip_for_ap(self, ip, interface_ips):
        if ip not in interface_ips:
            return ip
        else:
            # generate a new ip 192.168. <int>+1 .1
            ip_new_inc = ip.split('.')
            ip_new_inc[2] = str(int(ip_new_inc[2]) + 1)
            ip_new = '.'.join(ip_new_inc)
            return self.get_uniq_ip_for_ap(ip_new, interface_ips)

    def get_default_access_point_ip(self):

        interfaces = netifaces.interfaces()
        interfaces.remove('lo')

        interface_ips = []
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)

            if netifaces.AF_INET in addrs.keys():
                interface_ips.append(addrs[netifaces.AF_INET][0]['addr'])

        return self.get_uniq_ip_for_ap(ACCESS_POINT_IP, interface_ips)

