import telnetlib
import difflib

# Define common variables
router_ip_address = '192.168.56.101'
router_username = 'cisco'
router_password = 'cisco123!'
enable_password = 'class123!'
hardening_advice_file_path = 'hardening_advice.txt'  # Path to the hardening advice file

# Function to establish a Telnet session and execute commands
def telnet_session(ip, username, password, enable_password, commands):
    try:
        tn = telnetlib.Telnet(ip)
        tn.read_until(b'Username: ', timeout=10)
        tn.write(username.encode('utf-8') + b'\n')
        tn.read_until(b'Password: ', timeout=10)
        tn.write(password.encode('utf-8') + b'\n')
        tn.read_until(b'>', timeout=10)
        tn.write(b'enable\n')
        tn.read_until(b'Password: ', timeout=10)
        tn.write(enable_password.encode('utf-8') + b'\n')

        # Add the "terminal length 0" command to disable paging
        tn.write(b'terminal length 0\n')

        output = ''
        for command in commands:
            tn.write(command.encode('utf-8') + b'\n')
            output += tn.read_until(b'#').decode('utf-8')

        tn.write(b'quit\n')
        tn.close()

        return output
    except Exception as e:
        print(f'Telnet Session Failed: {e}')
        return None

# Function to compare running configuration with hardening advice
def compare_running_config_with_hardening_advice():
    try:
        with open(hardening_advice_file_path, 'r') as f:
            hardening_advice = f.read()

        commands = ['show running-config']

        running_config = telnet_session(router_ip_address, router_username, router_password, enable_password, commands)

        if running_config:
            diff = difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines())
            diff_result = '\n'.join(diff)
            if len(diff_result) > 0:
                print(diff_result)
            else:
                print("No differences found with hardening advice.")
        else:
            print("Failed to retrieve the running configuration.")
    except FileNotFoundError:
        print("Hardening advice file not found. Please check the file path.")

# Function to configure syslog
def configure_syslog():
    try:
        commands = [
            'enable',
            'configure terminal',
            'logging buffered 10240',
            'logging trap debugging',
            'logging source-interface cisco',  # the appropriate interface name
            'logging 192.168.56.101',  # the syslog server IP address
            'end'
        ]

        output = telnet_session(router_ip_address, router_username, router_password, enable_password, commands)
        
        if output:
            print("Syslog configuration applied successfully.")
            print("Event logging and monitoring enabled.")
    except Exception as e:
        print(f"Syslog configuration failed. Error: {e}")

# Main execution
while True:
    print('\nMenu:')
    print('1. Compare the current running configuration against Cisco device hardening advice')
    print('2. Configure syslog for event logging and monitoring')
    print('3. Exit')

    choice = input('Enter your choice (1-3): ')

    if choice == '1':
        compare_running_config_with_hardening_advice()
    elif choice == '2':
        configure_syslog()
    elif choice == '3':
        break
    else:
        print('Invalid choice. Please enter a number between 1 and 3.')
