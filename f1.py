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
output_file = 'running_config.txt'  # Name of the local file to save the running configuration
offline_config_file = 'offline_config.txt'  # Name of the local file to save the offline configuration

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

# Telnet session using the function
running_config_telnet = telnet_session(ip_address, username, password, enable_password, 'show running-config')

if running_config_telnet is not None:
    print('Telnet Session:')
    print(f'Successfully connected to: {ip_address}')
    print(f'Username: {username}')

    # Save the Telnet running configuration to a local file
    with open(output_file, 'w') as file:
        file.write(running_config_telnet)

    print('Running configuration saved to', output_file)
    print('------------------------------------------------------')

# SSH session using paramiko
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

# Load the offline configuration
if os.path.exists(offline_config_file):
    with open(offline_config_file, 'r') as offline_file:
        offline_config = offline_file.read()

    # Compare the running configuration with the offline version
    diff_running_vs_offline = list(difflib.unified_diff(running_config_telnet.splitlines(), offline_config.splitlines()))

    print('Differences between the current running configuration and the offline version:')
    for line in diff_running_vs_offline:
        if line.startswith('  '):
            continue  # Unchanged line
        elif line.startswith('- '):
            print(f'Removed: {line[2:]}')  # Line only in the offline config
        elif line.startswith('+ '):
            print(f'Added: {line[2:]}')  # Line only in the running config
else:
    print(f'Offline config file not found: {offline_config_file}')

# Compare the running configuration with the startup configuration
startup_config_file = 'startup_config.txt'  # Replace with the path to the startup configuration file
if os.path.exists(startup_config_file):
    with open(startup_config_file, 'r') as startup_file:
        startup_config = startup_file.read()

    diff_running_vs_startup = list(difflib.unified_diff(running_config_telnet.splitlines(), startup_config.splitlines()))

    print('Differences between the current running configuration and the startup configuration:')
    for line in diff_running_vs_startup:
        if line.startswith('  '):
            continue  # Unchanged line
        elif line.startswith('- '):
            print(f'Removed: {line[2:]}')  # Line only in the startup config
        elif line.startswith('+ '):
            print(f'Added: {line[2:]}')  # Line only in the running config
else:
    print(f'Startup config file not found: {startup_config_file}')
