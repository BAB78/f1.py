import telnetlib
import paramiko
import difflib
import os

# Define common variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
enable_password = 'class123!'
ssh_username = 'cisco'
ssh_password = 'cisco123!'
offline_config_path = 'devasc/labs/prne'
offline_config_file = 'offline_config.txt'  # Path to the offline configuration file
startup_config_file = 'startup_config.txt'  # Path to the startup configuration file
running_config_telnet = None
running_config_ssh = None

# Function to handle Telnet login and command execution
def telnet_session(ip, user, passwd, enable_pass, command):
    global running_config_telnet
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
    global running_config_ssh
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=user, password=passwd, look_for_keys=False, allow_agent=False)
        ssh_shell = ssh.invoke_shell()

        # Enter enable mode
        ssh_shell.send('enable\n')
        ssh_shell.send(enable_pass + '\n')

        print('SSH Session:')
        print(f'Successfully connected to: {ip}')
        print(f'Username: {user}')
        print(f'Password: {passwd}')
        print(f'Enable Password: {enable_pass}')

        # Send a command to output the running configuration
        ssh_shell.send('terminal length 0\n')  # Disable paging for SSH as well
        ssh_shell.send(command + '\n')
        running_config_ssh = ssh_shell.recv(65535).decode('utf-8')

        # Save the SSH running configuration to a local file
        output_file = 'ssh_running_config.txt'
        with open(output_file, 'w') as file:
            file.write(running_config_ssh)

        print('Running configuration saved to', output_file)
        print('------------------------------------------------------')

        # Exit enable mode
        ssh_shell.send('exit\n')

        # Close SSH session
        ssh.close()
        return running_config_ssh
    except Exception as e:
        print(f'SSH Session Failed: {e}')
        return None

# Placeholder implementations for additional functions. Replace these with your actual code.

def run_telnet():
    global running_config_telnet
    running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')
    print('Telnet Session:')
    print(f'Successfully connected to: {ip_address}')
    print(f'Username: {username}')

    # Save the Telnet running configuration to a local file
    output_file = 'telnet_running_config.txt'
    with open(output_file, 'w') as file:
        file.write(running_config_telnet)

    print('Running configuration saved to', output_file)

def run_ssh():
    global running_config_ssh
    running_config_ssh = ssh_session(ip_address, ssh_username, ssh_password, enable_password, 'show running-config')
    print('SSH Session:')
    print(f'Successfully connected to: {ip_address}')
    print(f'Username: {ssh_username}')
    print(f'Password: {ssh_password}')
    print(f'Enable Password: {enable_password}')

    # Save the SSH running configuration to a local file
    output_file = 'ssh_running_config.txt'
    with open(output_file, 'w') as file:
        file.write(running_config_ssh)

    print('Running configuration saved to', output_file)
    print('------------------------------------------------------')

def compare_with_hardening_advice():
    print("Placeholder for compare_with_hardening_advice function")

def compare_with_startup_config():
    global running_config_telnet, running_config_ssh
    if running_config_telnet is None:
        running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')

    if running_config_ssh is None:
        running_config_ssh = ssh_session(ip_address, ssh_username, ssh_password, enable_password, 'show running-config')

    if running_config_telnet is not None and running_config_ssh is not None:
        startup_config_file_path = os.path.join(offline_config_path, startup_config_file)
        if os.path.exists(startup_config_file_path):
            with open(startup_config_file_path, 'r') as startup_file:
                startup_config = startup_file.read()

            # Compare the running configuration with the startup configuration for Telnet
            diff_telnet = list(difflib.unified_diff(running_config_telnet.splitlines(), startup_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Startup Configuration (Telnet):')
            if not diff_telnet:
                print('No differences found.')
            else:
                for line in diff_telnet:
                    # Print only the difference, not the file path
                    if line.startswith('+ ') or line.startswith('- '):
                        print(line)

            # Compare the running configuration with the startup configuration for SSH
            diff_ssh = list(difflib.unified_diff(running_config_ssh.splitlines(), startup_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Startup Configuration (SSH):')
            if not diff_ssh:
                print('No differences found.')
            else:
                for line in diff_ssh:
                    # Print only the difference, not the file path
                    if line.startswith('+ ') or line.startswith('- '):
                        print(line)

        else:
            print(f'Startup config file not found.')
    else:
        print('Run Telnet or SSH first to fetch running configuration.')

# Function to compare with a local offline version
def compare_with_local_offline_version():
    global running_config_telnet, running_config_ssh
    if running_config_telnet is None:
        running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')

    if running_config_ssh is None:
        running_config_ssh = ssh_session(ip_address, ssh_username, ssh_password, enable_password, 'show running-config')

    offline_config_file_path = os.path.join(offline_config_path, offline_config_file)
    if os.path.exists(offline_config_file_path):
        with open(offline_config_file_path, 'r') as offline_file:
            offline_config = offline_file.read()

        # Compare the running configuration with the local offline version for Telnet
        diff_telnet_offline = list(difflib.unified_diff(running_config_telnet.splitlines(), offline_config.splitlines()))

        print('------------------------------------------------------')
        print('Comparison with Local Offline Version (Telnet):')
        if not diff_telnet_offline:
            print('No differences found.')
        else:
            for line in diff_telnet_offline:
                # Print only the difference, not the file path
                if line.startswith('+ ') or line.startswith('- '):
                    print(line)

        # Compare the running configuration with the local offline version for SSH
        diff_ssh_offline = list(difflib.unified_diff(running_config_ssh.splitlines(), offline_config.splitlines()))

        print('------------------------------------------------------')
        print('Comparison with Local Offline Version (SSH):')
        if not diff_ssh_offline:
            print('No differences found.')
        else:
            for line in diff_ssh_offline:
                # Print only the difference, not the file path
                if line.startswith('+ ') or line.startswith('- '):
                    print(line)

    else:
        print(f'Offline config file not found.')

# Function to configure syslog for event logging and monitoring
def configure_syslog():
    print("Placeholder for configure_syslog function")

# Function to configure event logging
def configure_event_logging():
    print("Placeholder for configure_event_logging function")

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
            configure_event_logging()
        elif choice == '7':
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 7.')

# Main execution
display_menu()
