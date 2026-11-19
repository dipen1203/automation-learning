import difflib
from pathlib import Path
import time
from paramiko import client, ssh_exception
import socket
import datetime
import webbrowser

script_dir = Path(__file__).parent
file_path = script_dir / "show_run.txt"

with open(file_path, 'r') as conf_file:
    new_cmd = conf_file.readlines()

def cisco_cmd_executor(hostname, commands, username, password):
    try:
        print(f"Connecting to the device {hostname}..")
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        current_conf_file = script_dir / f"{now}_{hostname}.txt"

        ssh_client = client.SSHClient()
        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=22, username=username, password=password, look_for_keys=False,
                           allow_agent=False)

        print(f"Connected to the device {hostname}")
        device_access = ssh_client.invoke_shell()
        device_access.send("terminal len 0\n")
        time.sleep(1)
        device_access.recv(65535)  # Clear login banner and terminal len output

        with open(current_conf_file, 'w') as cmd_data:
            for cmd in commands:
                device_access.send(f"{cmd.strip()}\n")
                time.sleep(2)
                output = device_access.recv(65535).decode()
                # Strip the first line (echoed command) and last line (router prompt)
                clean_lines = output.splitlines()[1:-1]
                clean_output = "\n".join(clean_lines) + "\n"
                cmd_data.write(clean_output)
                print(clean_output, end='')

        ssh_client.close()
        print("\nDisconnected from the device")

        # Read device-specific golden config (e.g., golden_192.168.4.111.txt)
        golden_file = script_dir / f"golden_conf.txt"
        with open(golden_file) as ref:
            ref_data = ref.readlines()

        with open(current_conf_file) as curr:
            curr_data = curr.readlines()

        conf_compare = difflib.HtmlDiff().make_file(fromlines=ref_data,
                                                    tolines=curr_data,
                                                    fromdesc="Golden Config",
                                                    todesc="Current Config")

        diff_file = script_dir / f"diff_{hostname}.html"
        with open(diff_file, 'w') as new_diff:
            new_diff.write(conf_compare)

        webbrowser.open_new_tab(diff_file.as_uri())

    except ssh_exception.NoValidConnectionsError:
        print("SSH Port not reachable")
    except socket.gaierror:
        print("Check the hostname")
    except ssh_exception.AuthenticationException:
        print("Authentication failed, check credentials")
    except Exception as e:
        print(f"Exception Occurred: {e}")

cisco_cmd_executor('192.168.4.111', new_cmd, 'admin', 'admin')
cisco_cmd_executor('192.168.4.121', new_cmd, 'admin', 'admin')
