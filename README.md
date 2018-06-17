# erxsyslog
Syslog for EdgeRouterX

**What is it?**

    SYSLOG application for Ubiquiti EdgeRouter X.
    This Python project listens for data from EdgeRouter X on the configured IP:Port and analyze the data to see when
    a device/client gets connected to the EdgeRouter X.

**Why is it needed?**

    Used to see which device/client gets connected to EdgeRouter X. And (if configured) this application
    will update the particular device tracker's status on Home Assistant (https://www.home-assistant.io/).

**Limitations?**

    1. This version only identifies when a device/client connects to EdgeRouter X. Disconnect is not supported just yet
    2. There may be more which are out of scope for this project.

**What are the requirements?**

    1. Ubiquiti EdgeRouter X (Not tested yet with other variants)
    2. Home Assistant application
    3. Some knowledge to configure EdgeRouter X to send SYSLOG to this application as per documented by Ubiquiti:
       https://help.ubnt.com/hc/en-us/articles/204975904-EdgeRouter-Remote-Syslog-Server-for-System-Logs
       I have tested and verified with following settings:
            Ubiquiti Hardware: EdgeRouter X
            Ubiquiti Software: EdgeOSv1.9.7+hotfix.4
            Ubiquiti System log level: Debug

**What next?**

    In future version I will try to add:
        1. Identify when a device/client disconnects
        2. Create a native component for use with Home Assistant

**Config file:**

    There is a default config.yaml file which must be configured as per your environment setup.
    There are two sections: syslog and home-assistant in the config.yaml.
    syslog section has the details of IP:Port, log files and logging levels.
        IP:Port:
            This is IP address of the device you going to run this application and same IP will go into EdgeRouter X
            SYSLOG configuration mentioned above. This application will keep connection open to listen the information
            provided by the EdgeRouter X.

        logs: Notes following all files will be created under the logs folder. 
            syslog_log: This is RAW data received from the EdgeRouter X and will be stored in daily log file.
                        Default file name will be erx_syslog unless you have changed it.
                        As of now older files will NOT be automatically deleted but in future version it may.
            monitor_log: This is log information of this application such as any error or useful details like device
                        connected.
            device_list: This yaml file has the details of all the device/client connected to the EdgeRouter X since the
                        application first ran. Below are the details what is being logged into this file:

                        11:22:33:44:55:66: # This is MAC address of the device/client reported by the EdgeRouter X
                          IP: 192.168.1.19 # This is IP address of the device/client reported by the EdgeRouter X
                          counts: 1 # Since first run of this application how many times it got (re)connected
                          entity_id: '' # Home Assistant entity id to report the status. By default this will be empty
                                        and will NOT be reported to the Home Assistant until user modifies it to the
                                        proper name. For example you can name it like this:
                                            entity_id: 'my_pixel_phone'
                                        Now when next time device gets (re)connected to EdgeRouter X this application 
                                        will update Home Assistant so it will show as device_tracker.my_pixel_phone and 
                                        you can have automation setup do lot more things! 
                          last_connected: '2018-06-17 15:47:11' # This is Date/Time when it last got connected

    home-assistant section has the details of your running Home Assistant to send the device tracking information.
        url: http://192.168.1.77:8123 # This is your Home Assistant URL/IP without slash (/) at the end
        password: home # This is your Home Assistant password

**What about Docker?**

    This project includes two docker files: dockerfile to build the image and docker-compose.yaml for compose. 
    In future version I may have docker-image which can directly be deployed from docker hub!
