import telnetlib
import difflib
import logging

# Define logger for error handling
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

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
        logging.error(f'Telnet Session Failed: {e}')
        return None

# Function to compare with hardening advice
def compare_with_hardening_advice():
    try:
        with open('configs/hardening_advice.txt', 'r') as f:
            hardening_advice = f.read()

        running_config = telnet_session(ip_address, username, password, enable_password, 'show running-config')

        if running_config:
            diff_result = list(difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines()))

            if diff_result:
                logging.info('Differences found with hardening advice:')
                for line in diff_result:
                    print(line)
            else:
                logging.info("No significant differences found with hardening advice.")
        else:
            logging.error("Failed to retrieve the running configuration.")

    except FileNotFoundError:
        logging.error("Hardening advice file not found. Please check the file path.")

# Function to configure syslog
def configure_syslog():
    logging.info('Configuring syslog...')
    # Implement syslog configuration logic here

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
