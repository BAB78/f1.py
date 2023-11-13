from netmiko import ConnectHandler
import difflib

# Define the router details
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'your_enable_password',  # Replace with your actual enable password
}

# Connect to the router
net_connect = ConnectHandler(**router)
net_connect.enable()

# Function to fetch running configuration
def get_running_config():
    running_config = net_connect.send_command("show running-config")
    return running_config

# Function to fetch startup configuration
def get_startup_config():
    startup_config = net_connect.send_command("show startup-config")
    return startup_config

# Function to compare configurations and display differences
def compare_configurations(config1, config2):
    diff = difflib.unified_diff(config1.splitlines(), config2.splitlines())
    print('\n'.join(diff))

# Task 1: Compare running config with startup config
running_config = get_running_config()
startup_config = get_startup_config()
print("\nTask 1: Compare running config with startup config")
compare_configurations(running_config, startup_config)

# Task 2: Compare running config with local offline version
# (Assuming you have a local file named 'offline_config.txt')
with open('offline_config.txt', 'r') as offline_file:
    offline_config = offline_file.read()

print("\nTask 2: Compare running config with local offline version")
compare_configurations(running_config, offline_config)

# Task 3: Placeholder for comparing with Cisco device hardening advice
print("\nTask 3: Placeholder for comparing with Cisco device hardening advice")

# Task 4: Configure syslog for event logging and monitoring
syslog_commands = [
    'logging buffered 8192 informational',
    'logging trap informational',
    'logging host 192.168.1.2',  # Replace with your syslog server IP
]

net_connect.send_config_set(syslog_commands)
print("\nTask 4: Syslog configuration applied")

# Disconnect from the router
net_connect.disconnect()
