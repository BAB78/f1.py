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

# Placeholder for Telnet running configuration
running_config_telnet = None

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

# Placeholder for SSH running configuration
running_config_ssh = None

# Function to execute SSH session
def run_ssh():
    global running_config_ssh  # Make sure to use the global variable
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=ssh_username, password=ssh_password, look_for_keys=False, allow_agent=False)
        ssh_shell = ssh.invoke_shell()

        # Enter enable mode
        ssh_shell.send('enable\n')
        ssh_shell.send(enable_password + '\n')

        print('SSH Session:')
        print(f'Successfully connected to: {ip_address}')
        print(f'Username: {ssh_username}')
        print(f'Password: {ssh_password}')
        print(f'Enable Password: {enable_password}')

        # Send a command to output the running configuration
        ssh_shell.send('terminal length 0\n')  # Disable paging for SSH as well
        ssh_shell.send('show running-config\n')
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
    except Exception as e:
        print(f'SSH Session Failed: {e}')

# Placeholder for Telnet running configuration
running_config_telnet = None

# Function to execute Telnet session
def run_telnet():
    global running_config_telnet  # Make sure to use the global variable
    running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')

    if running_config_telnet is not None:
        print('Telnet Session:')
        print(f'Successfully connected to: {ip_address}')
        print(f'Username: {username}')

        # Save the Telnet running configuration to a local file
        output_file = 'telnet_running_config.txt'
        with open(output_file, 'w') as file:
            file.write(running_config_telnet)

        print('Running configuration saved to', output_file)
    else:
        print('Telnet session failed.')

# ... (remaining functions remain unchanged)

# Main execution
if __name__ == "__main__":
    while True:
        print('\nMenu:')
        print('1. Telnet')
        print('2. SSH')
        print('3. Compare the current running configuration with the start-up configuration')
        print('4. Compare the current running configuration with a local offline version')
        print('5. Exit')

        choice = input('Enter your choice (1-5): ')

        if choice == '1':
            run_telnet()
        elif choice == '2':
            run_ssh()
        elif choice == '3':
            compare_with_startup_config()
        elif choice == '4':
            compare_with_offline_version()
        elif choice == '5':
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 5.')
