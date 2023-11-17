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
