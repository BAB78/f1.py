def apply_hardening(ip, username, password, enable_password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Enter enable mode
        ssh_shell = ssh.invoke_shell()
        ssh_shell.send("enable\n")
        ssh_shell.send(enable_password + "\n")
        output = ssh_shell.recv(65535).decode('utf-8')

        # Configuration commands for hardening
        commands = [
            "conf t",
            "ip access-list standard SSH-ACL",
            "permit <your_admin_IP>",  # Replace <your_admin_IP> with your actual IP
            "exit",
            "line vty 0 15",
            "access-class SSH-ACL in",
            "transport input ssh",
            # Other hardening commands as needed
            "end",
            "write memory"  # Save configuration
        ]

        for command in commands:
            ssh_shell.send(command + "\n")
            output = ssh_shell.recv(65535).decode('utf-8')

        ssh.close()
        print("Hardening configuration applied successfully.")
    except Exception as e:
        print(f"Failed to apply hardening: {e}")



def configure_syslog(ip, username, password, enable_password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Enter enable mode
        ssh_shell = ssh.invoke_shell()
        ssh_shell.send("enable\n")
        ssh_shell.send(enable_password + "\n")
        output = ssh_shell.recv(65535).decode('utf-8')

        # Configuration commands to set syslog server IP and other settings
        commands = [
            "conf t",
            "logging <syslog_server_ip>",  # Replace <syslog_server_ip> with the actual syslog server IP
            # Other syslog configuration commands as needed
            "end",
            "write memory"  # Save configuration
        ]

        for command in commands:
            ssh_shell.send(command + "\n")
            output = ssh_shell.recv(65535).decode('utf-8')

        ssh.close()
        print("Syslog configuration completed successfully.")
    except Exception as e:
        print(f"Failed to configure syslog: {e}")

def configure_event_logging(ip, username, password, enable_password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Enter enable mode
        ssh_shell = ssh.invoke_shell()
        ssh_shell.send("enable\n")
        ssh_shell.send(enable_password + "\n")
        output = ssh_shell.recv(65535).decode('utf-8')

        # Configuration commands to enable event logging
        commands = [
            "conf t",
            "logging buffered informational",  # Example command to set buffered logging to informational level
            # Other event logging configuration commands as needed
            "end",
            "write memory"  # Save configuration
        ]

        for command in commands:
            ssh_shell.send(command + "\n")
            output = ssh_shell.recv(65535).decode('utf-8')

        ssh.close()
        print("Event logging configuration completed successfully.")
    except Exception as e:
        print(f"Failed to configure event logging: {e}")
