import telnetlib
import paramiko
import difflib
import os
import time

# Define common variables
router_ip = '192.168.56.101'
router_username = 'cisco'
router_password = 'cisco123!'
enable_password = 'class123!'
output_file = 'running_config.txt'
offline_config_file = 'startup_config.txt'
running_config_telnet = None
running_config_ssh = None

# Function to handle Telnet login and command execution
def telnet_session(ip, user, passwd, enable_pass, command):
    try:
        tn = telnetlib.Telnet(ip)
        tn.read_until(b'Username: ', timeout=10)
        tn.write(user.encode('utf-8') + b'\n')
        tn.read_until(b'Password: ', timeout=10)
        tn.write(passwd.encode('utf-8') + b'\n')
        tn.read_until(b'Password: ', timeout=10)
        tn.write(enable_pass.encode('utf-8') + b'\n')

        # Add the "terminal length 0" command to disable paging
        tn.write(b'terminal length 0\n')

        # Send a command to output the running configuration
        tn.write(command.encode('utf-8') + b'\n')

        # Read until you find the end pattern or timeout
        running_config_telnet = tn.read_until(b'end\r\n\r\n', timeout=30).decode('utf-8')

        # Close Telnet session
        tn.write(b'quit\n')
        tn.close()

        return running_config_telnet
    except Exception as e:
        print(f'Telnet Session Failed: {e}')
        return None

# Function to handle SSH login and command execution
def ssh_session(ip, user, passwd, enable_pass, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=user, password=passwd, look_for_keys=False, allow_agent=False)
        ssh_shell = ssh.invoke_shell()

        # Enter enable mode
        ssh_shell.send('enable\n')
        ssh_shell.send(enable_pass + '\n')

        # Send a command to output the startup configuration
        ssh_shell.send('terminal length 0\n')  # Disable paging for SSH as well
        ssh_shell.send('show startup-config\n')
        running_config_ssh = ssh_shell.recv(65535).decode('utf-8')

        # Save the SSH startup configuration to a local file
        with open(offline_config_file, 'w') as file:
            file.write(running_config_ssh)

        # Exit enable mode
        ssh_shell.send('exit\n')

        # Close SSH session
        ssh.close()
        return running_config_ssh
    except Exception as e:
        print(f'SSH Session Failed: {e}')
        return None

# Function to run Telnet and save the running configuration
def run_telnet():
    global running_config_telnet
    running_config_telnet = telnet_session(router_ip, router_username, router_password, enable_password, 'show running-config')
    if running_config_telnet:
        with open(output_file, 'w') as file:
            file.write(running_config_telnet)
        print('Running configuration saved to', output_file)
    else:
        print('Failed to retrieve running configuration via Telnet.')

# Function to run SSH and save the running configuration
def run_ssh():
    global running_config_ssh
    running_config_ssh = ssh_session(router_ip, router_username, router_password, enable_password, 'show running-config')
    if running_config_ssh:
        with open(output_file, 'w') as file:
            file.write(running_config_ssh)
        print('Running configuration saved to', output_file)
    else:
        print('Failed to retrieve running configuration via SSH.')

# Function to compare with startup configuration
def compare_with_startup_config():
    global running_config_telnet, running_config_ssh
    # Similar to previous version, but compare running_config_telnet and running_config_ssh with startup_config_file

# Function to compare with local offline version
def compare_with_local_offline_version():
    global running_config_telnet, running_config_ssh
    # Similar to previous version, but compare running_config_telnet and running_config_ssh with offline_config_file

# Function to compare running config against hardening advice
def compare_with_hardening_advice():
    global running_config_telnet, running_config_ssh
    # Similar to previous version, but compare running_config_telnet and running_config_ssh with hardening_advice_file

# Function to configure event logging
def configure_syslog():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(router_ip, username=router_username, password=router_password)
        ssh_shell = ssh.invoke_shell()
        ssh_shell.send('enable\n')
        ssh_shell.send(enable_password + '\n')
        time.sleep(1)
        ssh_shell.send('conf t\n')
        ssh_shell.send('logging <syslog_server_ip>\n')  # Replace with actual syslog server IP
        time.sleep(1)
        ssh_shell.send('end\n')
        ssh_shell.send('write memory\n')
        ssh.close()
        print("Syslog configuration completed successfully.")
    except Exception as e:
        print(f"Failed to configure syslog: {e}")

# Function to display menu and execute selected option
def display_menu():
    while True:
        print('\nMenu:')
        print('1. Telnet')
        print('2. SSH')
        print('3. Compare the current running configuration with the start-up configuration')
        print('4. Compare the current running configuration with a local offline version')
        print('5. Compare the current running configuration against Cisco device hardening advice')
        print('6. Configure syslog for event logging and monitoring')
        print('7. Exit')

        choice = input('Enter your choice (1-7): ')

        if choice == '1':
            run_telnet()
        elif choice == '2':
            run_ssh()
        elif choice == '3':
            compare_with_startup_config()
        elif choice == '4':
            compare_with_local_offline_version()
        elif choice == '5':
            compare_with_hardening_advice()
        elif choice == '6':
            configure_syslog()
        elif choice == '7':
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 7.')

# Main execution
display_menu()
