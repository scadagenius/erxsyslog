import datetime
import json
import os
import yaml  # this needs package called PyYAML

from requests import post


class ErxHelper:
    log_level_debug = 1
    log_level_info = 2
    log_level_warning = 3
    log_level_error = 4
    log_level_critical = 5

    def __init__(self, config_folder):
        self.config_folder = config_folder
        self.config = yaml.load(open(self.config_folder + 'config.yaml'))

        self.log_level = 2
        if self.config["syslog"]["logs"]["level"] == "debug":
            self.log_level = 1
        elif self.config["syslog"]["logs"]["level"] == "info":
            self.log_level = 2
        elif self.config["syslog"]["logs"]["level"] == "warning":
            self.log_level = 3
        elif self.config["syslog"]["logs"]["level"] == "error":
            self.log_level = 4
        elif self.config["syslog"]["logs"]["level"] == "critical":
            self.log_level = 5

        self.log_folder = self.config_folder + "logs/"
        self.syslog_log = self.log_folder + self.config["syslog"]["logs"]["syslog_log"]
        self.monitor_log = self.log_folder + self.config["syslog"]["logs"]["monitor_log"]
        self.device_list_file = self.log_folder + self.config["syslog"]["logs"]["device_list"] + ".yaml"

        if not os.path.exists(self.log_folder):
            os.makedirs(self.config_folder + "logs")
            self.print(self.log_level_info, "ErxHelper:__init__(): Creating folder: " + self.log_folder)

    def get_log_level_to_string(self, log_level):
        log_level_str = ": "
        if log_level == self.log_level_debug:
            log_level_str = ":debug: "
        elif log_level == self.log_level_info:
            log_level_str = ":info: "
        elif log_level == self.log_level_warning:
            log_level_str = ":warn: "
        elif log_level == self.log_level_error:
            log_level_str = ":error: "
        elif log_level == self.log_level_critical:
            log_level_str = ":critical: "
        return log_level_str

    def log_data(self, message_data):
        try:
            log_file_name = self.syslog_log + "-" + datetime.datetime.now().strftime('%Y-%m-%d') + ".log"
            log_str = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + message_data

            with open(log_file_name, "a") as log_file:
                log_file.write(log_str + "\n")
        except Exception as e:
            self.print(self.log_level_error, "ErxHelper:log_data():Exception:" + str(e))

    def print(self, log_level, str_print):
        if self.log_level > log_level:
            return
        try:
            log_file_name = self.monitor_log + "-" + datetime.datetime.now().strftime('%Y-%m-%d') + ".log"
            log_str = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + \
                self.get_log_level_to_string(log_level) + str_print

            print(log_str)
            with open(log_file_name, "a") as log_file:
                log_file.write(log_str + "\n")
        except Exception as e:
            print(
                datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + " : ErxHelper:print():Exception: " + str(e))

    def update_ha_device_tracker(self, device_id, mac_address, status):
        self.print(self.log_level_debug, "ErxHelper:update_ha_device_tracker(): enter")

        base_url_post = self.config["home-assistant"]["url"] + "/api/services/device_tracker/see?api_password=" + \
            self.config["home-assistant"]["password"]

        # for safety reason don't print following debug information as it may contain sensitive information
        # for users who has public facing Home Assistant
        # self.print(self.log_level_debug, "ErxHelper:update_ha_device_tracker(): url: " + base_url_post)

        payload = {
            "dev_id": device_id,
            "location_name": status,
            "attributes": {
                "source_type": "script",
                "mac": mac_address
            }
        }
        self.print(self.log_level_info,
                   "ErxHelper:update_ha_device_tracker(): payload: " + str(json.dumps(payload)))

        response = post(base_url_post, data=json.dumps(payload))
        self.print(self.log_level_info, "ErxHelper:update_ha_device_tracker(): response: " + str(response.text))

        self.print(self.log_level_debug, "ErxHelper:update_ha_device_tracker(): exit")

    def load_device_list(self):
        self.print(self.log_level_debug, "ErxHelper:load_device_list(): enter")

        device_list = {}
        try:
            device_list = yaml.load(open(self.device_list_file))
        except IOError as e:
            self.print(self.log_level_error, "ErxHelper:load_device_list():Exception:" + str(e))
        self.print(self.log_level_debug, "ErxHelper:load_device_list(): exit")

        return device_list

    def save_device_list(self, device_list):
        self.print(self.log_level_debug, "ErxHelper:save_device_list(): enter")

        try:
            yaml.dump(device_list, open(self.device_list_file, "w"), default_flow_style=False)
        except IOError as e:
            self.print(self.log_level_error, "ErxHelper:save_device_list():Exception:" + str(e))

        self.print(self.log_level_debug, "ErxHelper:save_device_list(): exit")
