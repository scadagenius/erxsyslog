import datetime
import sys

from erx_helper import ErxHelper
from erx_syslog import ErxSyslog


class ErxMonitor:
    def __init__(self, config_folder):
        self.helper = ErxHelper(config_folder)
        self.helper.print(self.helper.log_level_info, "ErxMonitor: Starting Edgemax Monitor")
        self.syslog = ErxSyslog(self.helper)

        while True:
            try:
                self.helper.print(self.helper.log_level_debug, "ErxMonitor: Start Edgemax syslog monitor loop")
                self.syslog.monitor()
            except Exception as e:
                self.helper.print(self.helper.log_level_error, "ErxMonitor: Exception: " + str(e) + " at " +
                                  datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
        if not root_path.endswith("/"):
            root_path = root_path + "/"
    else:
        root_path = "/config/"
    print("Config folder: " + root_path)
    main_object = ErxMonitor(root_path)
