import paramiko
import difflib
import time

router_ip = '192.168.56.30'
router_username = 'cisco'
router_password = 'cisco123!'

# Function to establish an SSH connection
def establish_connection():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=router_username, password=router_password)
        return ssh_client
    except Exception as e:
        print(f"Failed to establish SSH connection: {e}")
        return None

# Function to fetch router configuration via SSH
def fetch_config():
    try:
        ssh_client = establish_connection()
        if ssh_client:
            ssh_shell = ssh_client.invoke_shell()
            ssh_shell.send('terminal length 0\n')
            time.sleep(1)
            ssh_shell.send('show running-config\n')
            time.sleep(2)
            running_config = ssh_shell.recv(65535).decode('utf-8')
            ssh_client.close()
            return running_config
    except Exception as e:
        print(f"Failed to fetch configuration: {e}")
        return None

# Function to compare configurations
def compare_configs(config1, config2, title):
    if config1 and config2:
        diff = difflib.unified_diff(config1.splitlines(), config2.splitlines())
        print(f"Differences between {title}:")
        for line in diff:
            print(line)
    else:
        print(f"Failed to compare {title}.")

# Fetch running configuration
running_config = fetch_config()
if running_config:
    with open('running_config.txt', 'w') as file:
        file.write(running_config)
    print("Running configuration fetched successfully.")
else:
    print("Failed to fetch running configuration.")

# Load stored offline config
with open('stored_offline_config.txt', 'r') as file:
    stored_offline_config = file.read()

# Compare running with stored offline config
compare_configs(running_config, stored_offline_config, "running and stored offline configuration")

# Function to compare running config against hardening advice
def compare_with_hardening_advice():
    # Load hardening advice from a file or Moodle page
    with open('hardening_advice.txt', 'r') as file:
        hardening_advice = file.read()

    compare_configs(running_config, hardening_advice, "running configuration and hardening advice")

# Configure syslog on the router
def configure_syslog():
    try:
        ssh_client = establish_connection()
        if ssh_client:
            ssh_shell = ssh_client.invoke_shell()
            ssh_shell.send('enable\n')
            ssh_shell.send('cisco123!\n')
            time.sleep(1)
            ssh_shell.send('conf t\n')
            ssh_shell.send('logging <syslog_server_ip>\n')  # Replace with actual syslog server IP
            time.sleep(1)
            ssh_shell.send('end\n')
            ssh_shell.send('write memory\n')
            ssh_client.close()

            print("Syslog configuration completed successfully.")
        else:
            print("Failed to establish SSH connection for syslog configuration.")
    except Exception as e:
        print(f"Failed to configure syslog: {e}")

# Compare running config against hardening advice
compare_with_hardening_advice()

# Configure syslog on the router
configure_syslog()
