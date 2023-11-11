import telnetlib
import paramiko
import difflib
import os

# ... (previous code)

# Compare the configurations
if os.path.exists(offline_config_file):
    with open(offline_config_file, 'r') as offline_file:
        offline_config = offline_file.read()

    # Compare the running configuration with the offline version
    diff_offline = list(difflib.unified_diff(running_config_telnet.splitlines(), offline_config.splitlines()))

    print('------------------------------------------------------')
    print('Differences between the running configuration and the offline version:')
    for line in diff_offline:
        print(line)

    # Set the path to the startup configuration file
    startup_config_file = 'startup_config.txt'

    # Compare the running configuration with the startup configuration
    if os.path.exists(startup_config_file):
        with open(startup_config_file, 'r') as startup_file:
            startup_config = startup_file.read()

        # Compare the running configuration with the startup configuration
        diff_startup = list(difflib.unified_diff(running_config_telnet.splitlines(), startup_config.splitlines()))

        print('------------------------------------------------------')
        print('Differences between the running configuration and the startup configuration:')
        for line in diff_startup:
            print(line)  # <-- Add this line
    else:
        print(f'Startup config file not found: {startup_config_file}')

    print('------------------------------------------------------')
else:
    print(f'Offline config file not found: {offline_config_file}')
