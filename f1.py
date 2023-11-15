import paramiko
import time  # Import the 'time' module

# Rest of your code...

# Function to configure syslog
def configure_syslog(ip, username, password, enable_password, syslog_server_ip):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        ssh_shell = ssh.invoke_shell()
        ssh_shell.send("enable\n")
        ssh_shell.send(enable_password + "\n")
        time.sleep(1)  # Ensure time to receive data
        output = ssh_shell.recv(65535).decode('utf-8')

        commands = [
            "conf t",
            f"logging {syslog_server_ip}",  # Replace with the actual syslog server IP
            # Other syslog configuration commands as needed
            "end",
            "write memory"
        ]

        for command in commands:
            ssh_shell.send(command + "\n")
            time.sleep(1)  # Delay to receive output
            output = ssh_shell.recv(65535).decode('utf-8')  # Receive output

        ssh.close()
        print("Syslog configuration completed successfully.")
    except Exception as e:
        print(f"Failed to configure syslog: {e}")

# Function to configure event logging
def configure_event_logging(ip, username, password, enable_password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        ssh_shell = ssh.invoke_shell()
        ssh_shell.send("enable\n")
        ssh_shell.send(enable_password + "\n")
        time.sleep(1)  # Ensure time to receive data
        output = ssh_shell.recv(65535).decode('utf-8')

        commands = [
            "conf t",
            "logging buffered informational",  # Example command to set buffered logging to informational level
            # Other event logging configuration commands as needed
            "end",
            "write memory"
        ]

        for command in commands:
            ssh_shell.send(command + "\n")
            time.sleep(1)  # Delay to receive output
            output = ssh_shell.recv(65535).decode('utf-8')  # Receive output

        ssh.close()
        print("Event logging configuration completed successfully.")
    except Exception as e:
        print(f"Failed to configure event logging: {e}")

# To call the functions:
configure_syslog('192.168.56.101', 'cisco', 'cisco123!', 'class123!', '<your_syslog_server_ip>')
configure_event_logging('192.168.56.101', 'cisco', 'cisco123!', 'class123!')
