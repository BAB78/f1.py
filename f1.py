import paramiko
import difflib
import time

# Define router credentials and IP
router_ip = '192.168.56.30'
router_username = 'cisco'
router_password = 'cisco123!'

# Function to fetch router configuration via SSH
def fetch_config():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=router_username, password=router_password)

        # Sending commands to fetch running configuration
        ssh_shell = ssh_client.invoke_shell()
        ssh_shell.send('terminal length 0\n')
        ssh_shell.send('show running-config\n')
        time.sleep(2)
        running_config = ssh_shell.recv(65535).decode('utf-8')

        ssh_client.close()
        return running_config
    except Exception as e:
        print(f"Failed to fetch configuration: {e}")
        return None

# Function to compare running config with startup config
def compare_with_startup_config():
    # Read startup configuration file
    try:
        with open('startup_config.txt', 'r') as file:
            startup_config = file.read()

        if startup_config:
            # Compare running with startup configuration
            diff = difflib.unified_diff(running_config.splitlines(), startup_config.splitlines())
            differences_found = False
            print("\ni. Differences between running config and startup config:")
            for line in diff:
                differences_found = True
                print(line)
            if not differences_found:
                print("No differences found between running config and startup config.")
        else:
            print("Startup config file not found.")
    except FileNotFoundError:
        print("Startup config file not found.")

# Function to compare running config with local offline config
def compare_with_local_offline_config(running_config):
    # Read local offline configuration file
    try:
        with open('stored_offline_config.txt', 'r') as file:
            stored_offline_config = file.read()

        if stored_offline_config:
            # Compare running with stored offline configuration
            diff = difflib.unified_diff(running_config.splitlines(), stored_offline_config.splitlines())
            differences_found = False
            print("\nii. Differences between running config and local offline config:")
            for line in diff:
                differences_found = True
                print(line)
            if not differences_found:
                print("No differences found between running config and local offline config.")
        else:
            print("Local offline config file not found.")
    except FileNotFoundError:
        print("Local offline config file not found.")

# Function to compare running config against hardening advice
def compare_with_hardening_advice(running_config):
    # Read hardening advice file
    try:
        with open('hardening_advice.txt', 'r') as file:
            hardening_advice = file.read()

        if hardening_advice:
            # Compare running with hardening advice
            diff = difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines())
            differences_found = False
            print("\niii. Differences between running config and hardening advice:")
            for line in diff:
                differences_found = True
                print(line)
            if not differences_found:
                print("No differences found between running config and hardening advice.")
        else:
            print("Hardening advice not found.")
    except FileNotFoundError:
        print("Hardening advice file not found.")

# Function to configure syslog on the router
def configure_syslog():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=router_username, password=router_password)

        ssh_shell = ssh_client.invoke_shell()
        ssh_shell.send('enable\n')
        ssh_shell.send('cisco123!\n')
        time.sleep(1)
        ssh_shell.send('conf t\n')
        ssh_shell.send('logging 192.168.56.101\n')  # Replace with actual syslog server IP
        time.sleep(1)
        ssh_shell.send('end\n')
        ssh_shell.send('write memory\n')
        ssh_client.close()

        print("\niv. Syslog configuration completed successfully.")
    except Exception as e:
        print(f"Failed to configure syslog: {e}")

# Fetch running configuration
running_config = fetch_config()
if running_config:
    compare_with_startup_config()
    compare_with_local_offline_config(running_config)
    compare_with_hardening_advice(running_config)
    configure_syslog()
