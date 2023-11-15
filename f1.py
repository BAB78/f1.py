import paramiko
import difflib
import os
import time

# All your functions and variables...

# Function to compare with hardening advice
def compare_with_hardening_advice():
    try:
        # Fetch running configuration
        running_config = fetch_config()

        with open('hardening_advice.txt', 'r') as file:
            hardening_advice = file.read()

        if running_config and hardening_advice:
            diff = difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines())
            differences_found = False
            print("Differences between running config and hardening advice:")
            for line in diff:
                differences_found = True
                print(line)
            if not differences_found:
                print("No differences found between running config and hardening advice.")
        else:
            print("Failed to compare with hardening advice.")
    except FileNotFoundError:
        print("Hardening advice file not found.")

# Configure syslog on the router
def configure_syslog(ip, username, password, enable_password):
    try:
        ssh_client = establish_connection(ip, username, password)
        if ssh_client:
            ssh_shell = ssh_client.invoke_shell()
            ssh_shell.send('enable\n')
            ssh_shell.send(enable_password + '\n')
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
configure_syslog(ip_address, username, password, enable_password)
