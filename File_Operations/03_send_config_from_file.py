import os
from pathlib import Path
import sys
import time
import traceback
from paramiko import client, ssh_exception
from getpass import getpass
import socket

# username = 'admin'
# password = 'admin'
# csr_cmd = ['show run']

script_dir = Path(__file__).resolve().parent
config_file = script_dir / "config2.txt"
output_file = script_dir / "output2.txt"
os.chdir(Path(__file__).resolve().parent)

with open(config_file, 'r') as conf_file:
    new_cmd = conf_file.readlines()
print(new_cmd)

def cisco_cmd_executor(hostname, commands, username, password):
    try:
        print(f"Connecting to the device {hostname}..")
        # now = datetime.datetime.now().replace(microsecond=0)
        # current_conf_file = f"{now}_{hostname}.txt"
        ssh_client = client.SSHClient()
        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=22, username=username, password=password, look_for_keys=False,
                           allow_agent=False)

        print(f"Connected to the device {hostname}")
        device_access = ssh_client.invoke_shell()
        device_access.send("terminal len 0\n")
        time.sleep(1)

        with open(output_file, 'a') as cmd_data:
            cmd_data.write(f"\n\n--- Output for {hostname} ---\n")
            for cmd in commands:
                device_access.send(f"{cmd.strip()}\n")
                time.sleep(1)
                output = device_access.recv(65535)
                cmd_data.write(output.decode())
                print(output.decode(), end='')
        ssh_client.close()
    except ssh_exception.NoValidConnectionsError:
        print("SSH Port not reachable")
    except socket.gaierror:
        print("Check the hostname")
    except ssh_exception.AuthenticationException:
        print("Authentication failed, check credentials")

    except:
        print("Exception Occurred")
        print(sys.exc_info())
        # traceback.print_exception(*sys.exc_info())

cisco_cmd_executor('192.168.4.111', new_cmd, 'admin', 'admin')
cisco_cmd_executor('192.168.4.121', new_cmd, 'admin', 'admin')

