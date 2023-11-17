Enter your choice (1-3): 1       
Comparing running config with hardening advice...
Traceback (most recent call last):
  File "task.py", line 107, in <module>
    display_menu()
  File "task.py", line 98, in display_menu
    compare_with_hardening_advice()
  File "task.py", line 45, in compare_with_hardening_advice
    with open('hardening_advice.txt', 'r') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'hardening_advice.txt'




import telnetlib
import difflib

# Define common variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
enable_password = 'cisco123!'

# Function to handle Telnet login and command execution
def telnet_session(ip, user, passwd, enable_pass, command):
    try:
        tn = telnetlib.Telnet(ip)
        tn.read_until(b'Username: ', timeout=10)
        tn.write(user.encode('utf-8') + b'\n')
        tn.read_until(b'Password: ', timeout=10)
        tn.write(passwd.encode('utf-8') + b'\n')
        tn.read_until(b'>', timeout=10)
        tn.write(b'enable\n')
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

    if running_config:
        diff = difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines())
        diff_result = '\n'.join(diff)
        if len(diff_result) > 0:
            print("Differences found with hardening advice:")
            print(diff_result)
        else:
            print("No differences found with hardening advice.")
    else:
        print("Failed to retrieve the running configuration.")

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
        
        print("Syslog configured successfully for event logging and monitoring.")
        tn.close()
    except Exception as e:
        print(f"Error configuring syslog: {e}")

# Function to display menu and execute selected option
def display_menu():
    while True:
        print('\nMenu:')
        print('1. Compare the current running configuration against Cisco device hardening advice')
        print('2. Configure syslog for event logging and monitoring')
        print('3. Exit')

        choice = input('Enter your choice (1-3): ')

        if choice == '1':
            compare_with_hardening_advice()
        elif choice == '2':
            configure_syslog()
        elif choice == '3':
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 3.')

# Main execution
display_menu()
