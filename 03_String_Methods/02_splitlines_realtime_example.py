
show_output = '''Ethernet0/0            192.168.4.121   YES NVRAM  up                    up      
Ethernet0/1            unassigned      YES NVRAM  administratively down down    
Ethernet0/2            unassigned      YES NVRAM  administratively down down    
Ethernet0/3            unassigned      YES NVRAM  administratively down down    
Loopback1001           10.1.1.100      YES manual up                    up      
Loopback1002           20.1.1.100      YES manual up                    up 
'''
#
intf_lines = show_output.splitlines()
# print(intf_lines)
for intf in intf_lines:
    intf_details = intf.split()
    if intf_details[1] == 'unassigned':
        continue
    print(f"Interface Name: {intf_details[0]} Interface IP {intf_details[1]}")
#
#######################################################

from pathlib import Path

script_dir = Path(__file__).resolve().parent
output_file = script_dir / "output.txt"

with open(output_file) as text:
    lines = text.readlines()
# print(lines)
    print("Press Enter..", end='')
    for line in lines:
        if input() == '':
            line = line.strip('\n')
            print(line, end='')
print("Completed")