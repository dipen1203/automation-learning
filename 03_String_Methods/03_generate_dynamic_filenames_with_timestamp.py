import datetime
from pathlib import Path

script_dir = Path(__file__).parent
file_path = script_dir / "show_commands.txt"

with open(file_path) as sh_cmd:
    commands = sh_cmd.readlines()
time_seq_no_commands = enumerate(commands, start=1)
# print(commands)
now = datetime.datetime.now().replace(microsecond=0)
for cmd in time_seq_no_commands:
    file_name = f"{str(now).replace(' ',':')}_{str(cmd[0]).zfill(2)}_{cmd[1].replace(' ','_').strip()}.txt"
    
    output_file = script_dir / file_name # this will create a file in the same directory as the script
    
    with open(output_file, 'w') as cmd_data:
        cmd_data.write('test_data')