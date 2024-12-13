import sys
import os
import subprocess
import hashlib
import time
from colorama import init, Fore, Style

# Initialize colorama
init()

# Define color codes
green = Fore.GREEN
end = Style.RESET_ALL
red = Fore.RED
blue = Fore.BLUE
yellow = Fore.YELLOW
purple = Fore.MAGENTA
cyan = Fore.CYAN
white = Fore.WHITE

# Check usage 
if len(sys.argv) != 3:
    print ("Usage: python3 test_hashcat.py <file_with_hashes> <path to wordlist>")
    sys.exit(1)

file = sys.argv[1]
wordlist = sys.argv[2]


# Check if file exists
if not os.path.isfile(file): #Check for file    
    print(f"{red}[-] Error : The specified file {file} could not be found.{end}") # return error if file not there
    sys.exit(1)

# Define hashfile as sys.argv 1


def get_hashes(file):
    hash_list = [] # initialize list to store files
    with open (file, 'r', encoding="latin-1") as f: # Open the file        
        contents_of_file = f.read().splitlines() # Read the file and remove \n
        for line in contents_of_file: # Loops through each line 
            if ":" in line: # Locates the seperator for the hashes which in this case is :
                value = str(line.split(":", 1)[1]) # line.split splits each line in to two parts and retrieves the hash_value which is the second part [1] signifies 2. The first 1 limits the split t just once so if a : colon were to occur again it won't error
            hash_list.append(value) # append each has to the list
        return hash_list




        #return hash_list# its here so it doesnt print it according to the number of hashes...don't let it be stuck in the for loop
        

print (f"{blue}[*] Generating hash list{end}")
hashes = get_hashes(file) # get the hashes in the list format

for hash in hashes: # loops through the hashes in the list
    test = subprocess.run(['hashid', hash], capture_output = True, text = True) # analyzes the hashes
if "MD5" or "NTLM" in test.stdout: # Determines hash type
    print(f"{blue}[*] Detected hash format MD5 or NTLM{end}")
else: # If hash not supported - exit
    print(f"{red}[-] Unsupported hash format{end}")
    sys.exit(1)

def md5_wordlist(wordlist): # hash each word in the wordlist and compare it
    word_list = []
    with open(wordlist, 'r', encoding="latin-1") as w: # open wordlist
        wordlist_content = w.read().splitlines() # read wordlist
        for line in wordlist_content:# Loop through each line in file wordlist
            md5_hash = hashlib.md5() # initialize md5
            md5_hash.update(line.encode('utf-8'))# encode it
            md5_result = md5_hash.hexdigest()# output it in hex format
            word_list.append([line, md5_result])# append hash in ['name':'hash"] format, making it easier to loop through and find specific
        return word_list # return list
        



final_wordlist = md5_wordlist(wordlist)  # get ['name': 'hash'] output to a list and call it final_wordlist
time.sleep(1.5)
print(f"{blue}[*] Analyzing wordlist{end}")

time.sleep(2)
def check_hashes(hashes, final_wordlist):
    for x in final_wordlist: # loops through final wordlist
        if x[1] in hashes: # if the value of hash in ['name': 'hash"] from final_wordlist in hashes get the password
            print(f"{green}[+] Cracked hash", x[1], "as:", x[0]) # print it
            time.sleep(2)






# print("hashes:", hashes)
# print("final_wordlist:", final_wordlist)
check_hashes(hashes, final_wordlist) #check hashes













    



