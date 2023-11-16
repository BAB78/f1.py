
import telnetlib
import paramiko
import difflib
import os
import time

# Define common variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
enable_password = 'class123!'
ssh_username = 'cisco'
ssh_password = 'cisco123!'
output_file = 'running_config.txt'  # Name of the local file to save the running configuration
offline_config_file = 'startup_config.txt'  # Path to save the startup configuration

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
        time.sleep(1)

        print('SSH Session:')
        print(f'Successfully connected to: {ip}')
        print(f'Username: {user}')
        print(f'Password: {passwd}')
        print(f'Enable Password: {enable_pass}')

        # Send a command to output the startup configuration
        ssh_shell.send('terminal length 0\n')  # Disable paging for SSH as well
        ssh_shell.send('show startup-config\n')
        running_config_ssh = ssh_shell.recv(65535).decode('utf-8')

        # Save the SSH startup configuration to a local file
        with open(offline_config_file, 'w') as file:
            file.write(running_config_ssh)

        print('Running configuration saved to', offline_config_file)
        print('------------------------------------------------------')

        # Exit enable mode
        ssh_shell.send('exit\n')
        ssh.close()

        return running_config_ssh
    except Exception as e:
        print(f'SSH Session Failed: {e}')
        return None

# Function to run Telnet and save the running configuration
def run_telnet():
    running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')

    if running_config_telnet is not None:
        print('Telnet Session:')
        print(f'Successfully connected to: {ip_address}')
        print(f'Username: {username}')

        # Save the Telnet running configuration to a local file
        with open(output_file, 'w') as file:
            file.write(running_config_telnet)

        print('Running configuration saved to', output_file)

# Function to run SSH and save the running configuration
def run_ssh():
    running_config_ssh = ssh_session(ip_address, ssh_username, ssh_password, enable_password, 'show running-config')

    if running_config_ssh is not None:
        print('SSH Session:')
        print(f'Successfully connected to: {ip_address}')
        print(f'Username: {ssh_username}')
        print(f'Password: {ssh_password}')
        print(f'Enable Password: {enable_password}')

        # Save the SSH running configuration to a local file
        with open(output_file, 'w') as file:
            file.write(running_config_ssh)

        print('Running configuration saved to', output_file)
        print('------------------------------------------------------')

# Function to compare with startup configuration
def compare_with_startup_config():
    running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')
    running_config_ssh = ssh_session(ip_address, ssh_username, ssh_password, enable_password, 'show running-config')

    if running_config_telnet is not None and running_config_ssh is not None:
        startup_config_file_path = os.path.join(offline_config_file)

        if os.path.exists(startup_config_file_path):
            with open(startup_config_file_path, 'r') as startup_file:
                startup_config = startup_file.read()

            # Compare the running configuration with the startup configuration for Telnet
            diff_telnet = list(difflib.unified_diff(running_config_telnet.splitlines(), startup_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Startup Configuration (Telnet):')
            for line in diff_telnet:
                # Print only the difference, not the file path
                if line.startswith('+ ') or line.startswith('- '):
                    print(line)

            # Compare the running configuration with the startup configuration for SSH
            diff_ssh = list(difflib.unified_diff(running_config_ssh.splitlines(), startup_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Startup Configuration (SSH):')
            for line in diff_ssh:
                # Print only the difference, not the file path
                if line.startswith('+ ') or line.startswith('- '):
                    print(line)

        else:
            print(f'Startup config file not found.')
    else:
        print('Run Telnet or SSH first to fetch the running configuration.')

# Function to compare with local offline version
def compare_with_local_offline_version():
    running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')
    running_config_ssh = ssh_session(ip_address, ssh_username, ssh_password, enable_password, 'show running-config')

    if running_config_telnet is not None and running_config_ssh is not None:
        offline_config_file_path = os.path.join(offline_config_file)

        if os.path.exists(offline_config_file_path):
            with open(offline_config_file_path, 'r') as offline_file:
                offline_config = offline_file.read()

            # Compare the running configuration with the offline configuration for Telnet
            diff_telnet = list(difflib.unified_diff(running_config_telnet.splitlines(), offline_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Offline Configuration (Telnet):')
            for line in diff_telnet:
                # Print only the difference, not the file path
                if line.startswith('+ ') or line.startswith('- '):
                    print(line)

            # Compare the running configuration with the offline configuration for SSH
            diff_ssh = list(difflib.unified_diff(running_config_ssh.splitlines(), offline_config.splitlines()))

            print('------------------------------------------------------')
            print('Comparison with Offline Configuration (SSH):')
            for line in diff_ssh:
                # Print only the difference, not the file path
                if line.startswith('+ ') or line.startswith('- '):
                    print(line)

        else:
            print(f'Offline config file not found.')
    else:
        print('Run Telnet or SSH first to fetch the running configuration.')

# Function to compare running config against hardening advice
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

# Function to configure syslog on the router
def configure_syslog(ip, username, password, enable_password):
    try:
        ssh_client = establish_connection(ip, username, password)
        if ssh_client:
            ssh_shell = ssh_client.invoke_shell()
            ssh_shell.send('enable\n')
            ssh_shell.send(enable_password + '\n')
            time.sleep(1)
            ssh_shell.send(f"logging {syslog_server_ip}")
            ssh_shell.send('end\n')
            ssh_shell.send('write memory\n')
            ssh_client.close()

            print("Syslog configuration completed successfully.")
        else:
            print("Failed to establish SSH connection for syslog configuration.")
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
            syslog_server_ip = input("Enter the IP of the syslog server: ")
            configure_syslog(ip_address, username, password, enable_password, syslog_server_ip)
        elif choice == '7':
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 7.')

# Main execution
display_menu()

