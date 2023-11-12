import telnetlib
import paramiko
import difflib
import os

# ... (previous code remains unchanged)

# Placeholder for Telnet running configuration
running_config_telnet = None

# Function to compare with start-up configuration
def compare_with_startup_config():
    if running_config_telnet is not None:
        startup_config_file_path = os.path.join(offline_config_path, startup_config_file)
        if os.path.exists(startup_config_file_path):
            with open(startup_config_file_path, 'r') as startup_file:
                startup_config = startup_file.read()

            # Compare the running configuration with the startup configuration
            diff_startup = list(difflib.unified_diff(running_config_telnet.splitlines(), startup_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Startup Configuration:')
            for line in diff_startup:
                print(line)
        else:
            print(f'Startup config file not found: {startup_config_file_path}')
    else:
        print('Run Telnet or SSH first to fetch running configuration.')

# Function to compare with local offline version
def compare_with_offline_version():
    global running_config_telnet  # Make sure to use the global variable
    if running_config_telnet is not None:
        offline_config_file_path = os.path.join(offline_config_path, offline_config_file)
        if os.path.exists(offline_config_file_path):
            with open(offline_config_file_path, 'r') as offline_file:
                offline_config = offline_file.read()

            # Compare the running configuration with the offline version
            diff_offline = list(difflib.unified_diff(running_config_telnet.splitlines(), offline_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Offline Version:')
            for line in diff_offline:
                print(line)
        else:
            print(f'Offline config file not found: {offline_config_file_path}')
    else:
        print('Run Telnet or SSH first to fetch running configuration.')

# ... (the rest of the code remains unchanged)
