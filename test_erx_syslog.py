from unittest import TestCase
from erx_helper import ErxHelper
from erx_syslog import ErxSyslog


class TestEdgemaxSyslog(TestCase):
    def test_process_edgemax_message_data_valid(self):
        config_folder = "./"
        self.helper = ErxHelper(config_folder)
        self.syslog = ErxSyslog(self.helper)

        # valid data
        data_str = "<30>Feb 10 00:01:43 ubnt dhcpd: DHCPACK on 192.168.1.19 to 11:22:33:44:55:66 via switch0"
        self.syslog.process_edgemax_message_data(data_str)

        # invalid data
        data_str = "<30>Feb 10 00:01:43 ubnt dhcpd: DHCPACK off 192.168.1.19 to 11:22:33:44:55:66 via switch0"
        self.syslog.process_edgemax_message_data(data_str)

        # valid data
        data_str = "<30>Feb 10 00:01:43 ubnt dhcpd: DHCPACK on 192.168.1.19 to 11:22:33:44:55:67 via switch0"
        self.syslog.process_edgemax_message_data(data_str)
