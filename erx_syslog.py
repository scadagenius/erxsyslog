import datetime
import json
import socket
import time

socket_receive_buffer = 4096


class ErxSyslog:
    def __init__(self, helper):
        self.helper = helper

    def monitor(self):
        self.helper.print(self.helper.log_level_debug, "ErxSyslog:monitor(): enter")
        sock = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.helper.config["syslog"]["ip"], self.helper.config["syslog"]["port"]))
            while True:
                data, address = sock.recvfrom(socket_receive_buffer)
                string_data = data.decode('utf-8')
                self.process_edgemax_message_data(string_data)
        except Exception as e:
            if sock is not None:
                sock.close()
            self.helper.print(self.helper.log_level_error, "ErxSyslog:monitor(): Exception " + str(e))
            time.sleep(60)
        self.helper.print(self.helper.log_level_debug, "ErxSyslog:monitor(): exit")

    def process_edgemax_message_data(self, message_data):
        self.helper.print(self.helper.log_level_debug, "ErxSyslog:process_edgemax_message_data(): enter")

        self.helper.log_data(message_data)
        device_item = {}
        pos = message_data.find("dhcpd: DHCPACK on")
        if pos != -1:
            device_list = self.helper.load_device_list()

            words = message_data[pos + 18:].split(" ")
            mac_address = words[2]

            device_item = device_list.get(mac_address)
            if device_item is None:
                device_item = {}

            if device_item.get("counts") is None:
                device_item["counts"] = "0"
            if device_item.get("entity_id") is None:
                device_item["entity_id"] = ""
            device_item["IP"] = words[0]
            device_item["last_connected"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            device_item["counts"] = int(device_item["counts"]) + 1
            device_list[mac_address] = device_item
            self.helper.print(self.helper.log_level_info,
                              "ErxSyslog:process_edgemax_message_data():data: " + json.dumps(device_item))

            if device_item.get("entity_id") is not "":
                self.helper.update_ha_device_tracker(device_item.get("entity_id"), mac_address, "home")

            self.helper.save_device_list(device_list)

        self.helper.print(self.helper.log_level_debug, "ErxSyslog:process_edgemax_message_data(): exit")
        return device_item
