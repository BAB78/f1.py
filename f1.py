import paramiko
import difflib
import time

router_ip = '192.168.56.30'
router_username = 'cisco'
router_password = 'cisco123!'
syslog_server_ip = '192.168.56.101'  # Replace with the syslog server IP

# Function to fetch router configuration via SSH
def fetch_config():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=router_username, password=router_password)

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

# Fetch running and startup configs
running_config = fetch_config()
if running_config:
    with open('running_config.txt', 'w') as file:
        file.write(running_config)

# Load stored offline config
try:
    with open('stored_offline_config.txt', 'r') as file:
        stored_offline_config = file.read()

    # Compare running with stored offline config
    if stored_offline_config:
        diff = difflib.unified_diff(running_config.splitlines(), stored_offline_config.splitlines())
        print("Differences between running config and stored offline config:")
        for line in diff:
            print(line)
    else:
        print("Stored offline config not found.")
except FileNotFoundError:
    print("Stored offline config file not found.")

# Function to compare running config against hardening advice
def compare_with_hardening_advice():
    # Load hardening advice from a file or Moodle page
    try:
        with open('hardening_advice.txt', 'r') as file:
            hardening_advice = file.read()

        if hardening_advice:
            diff = difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines())
            print("Differences between running config and hardening advice:")
            for line in diff:
                print(line)
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
        ssh_shell.send(f'logging {syslog_server_ip}\n')  # Replace with actual syslog server IP
        time.sleep(1)
        ssh_shell.send('end\n')
        ssh_shell.send('write memory\n')
        ssh_client.close()

        print("Syslog configuration completed successfully.")
    except Exception as e:
        print(f"Failed to configure syslog: {e}")

# Compare running config against hardening advice
compare_with_hardening_advice()

# Configure syslog on the router
configure_syslog()
