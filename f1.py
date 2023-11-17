import telnetlib
import difflib
import os

# Define common variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
enable_password = 'class123!'
output_file = 'running_config.txt'  # Name of the local file to save the running configuration
offline_config_file = 'startup_config.txt'  # Path to save the startup configuration
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

# Function to compare with hardening advice 
def compare_with_hardening_advice():
    print("Comparing running config with hardening advice...")
    
    with open('hardening_advice.txt', 'r') as f:
        hardening_advice = f.read()

    running_config = telnet_session(ip_address, username, password, enable_password, 'show running-config')

    diff = difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines())

    for line in diff:
        print(line)

# Function to configure syslog
def configure_syslog():
    try:
        tn = telnetlib.Telnet(ip_address)
        tn.read_until(b'Username: ', timeout=10)
        tn.write(username.encode('utf-8') + b'\n')
        tn.read_until(b'Password: ', timeout=10)
        tn.write(password.encode('utf-8') + b'\n')
        tn.read_until(b'>', timeout=10)
        tn.write(b'enable\n')
        tn.read_until(b'Password: ', timeout=10)
        tn.write(enable_password.encode('utf-8') + b'\n')
        
        tn.write(b'configure terminal\n')
        tn.read_until(b'#', timeout=10)
        tn.write(b'logging 192.168.1.100\n')  # Replace with your syslog server IP
        tn.read_until(b'#', timeout=10)
        tn.write(b'end\n')
        tn.read_until(b'#', timeout=10)
        tn.write(b'write memory\n')
        
        print("Syslog configured successfully.")
        tn.close()
    except Exception as e:
        print(f"Error configuring syslog: {e}")

# Function to display menu and execute selected option
def display_menu():
    while True:
        print('\nMenu:')
        print('5. Compare the current running configuration against Cisco device hardening advice')
        print('6. Configure syslog for event logging and monitoring')
        print('7. Exit')

        choice = input('Enter your choice (5-7): ')

        if choice == '5':
            compare_with_hardening_advice()
        elif choice == '6':
            configure_syslog()
        elif choice == '7':
            break
        else:
            print('Invalid choice. Please enter a number between 5 and 7.')

# Main execution
display_menu()
