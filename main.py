import subprocess
import re
import os
from colorama import Style, Fore

print("-" * 50)
interface = input("> Enter interface name to change IP address for: ") #"eth0"
new_ip = input("> Enter IP new address: ") #"192.168.1.128"
subnet_mask = input("> Enter subnet mask: ") #"255.255.255.0"
print("-" * 50)

ip_regex = r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
ifconfig_output = subprocess.run(['ifconfig', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
current_ip_match = re.search(ip_regex, ifconfig_output.stdout)
if current_ip_match:
    current_ip = current_ip_match.group(1)
    print(Fore.BLUE +"[+] Current IP address:", current_ip+ Style.RESET_ALL)
else:
    print(Fore.RED +"[-] Failed to get current IP address, error message:", ifconfig_output.stderr+ Style.RESET_ALL)
    exit()

if current_ip == new_ip:
    print(Fore.YELLOW +"[!] The new IP address is the same as the current IP address."+ Style.RESET_ALL)
    exit()

cmd = f"ifconfig {interface} {new_ip} netmask {subnet_mask} up"
try:
    #subprocess.run([f"sudo {cmd}"])#, check=True
    os.system(f"sudo {cmd}")
    print(Fore.GREEN +"[+] IP address changed successfully"+ Style.RESET_ALL)
except OSError as e:
#except subprocess.CalledProcessError as e:
    if "permission denied" in e.stderr:
        print(Fore.RED +"[-] Failed to change IP address: insufficient privileges."+ Style.RESET_ALL)
    elif "invalid argument" in e.stderr:
        print(Fore.RED +"[-] Failed to change IP address: invalid IP address format."+ Style.RESET_ALL)
    else:
        print(Fore.RED +"[-] Failed to change IP address:", e.stderr+ Style.RESET_ALL)

ifconfig_output = subprocess.run(['ifconfig', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
new_ip_match = re.search(ip_regex, ifconfig_output.stdout)
if new_ip_match:
    new_ip = new_ip_match.group(1)
    print(Fore.BLUE +"[+] New IP address:", new_ip+ Style.RESET_ALL)
else:
    print(Fore.RED +"[-] Failed to get new IP address, error message:", ifconfig_output.stderr+ Style.RESET_ALL)
