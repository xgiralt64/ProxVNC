from ProxVNC.proxmoxer import ProxmoxAPI
from ProxVNC import ProxVNC

def main():
    
    proxmox = ProxmoxAPI(host="",
                         user="", 
                         password="",
                         otp=input("OTP: "),
                         verify_ssl=False)
    
    lxc = 104 # LXC container ID
    
    termproxy = proxmox.nodes("pve").lxc(lxc).termproxy.post()

    shell_ticket = termproxy["ticket"]
    shell_port = termproxy["port"]

    pve_cookie, _ = proxmox.get_tokens()

        
    client = ProxVNC(
             url="https://",
             node="pve",
             user="",
             shell_port=shell_port,
             shell_ticket=shell_ticket,
             pve_auth_cookie=pve_cookie
            )  
    client.connect(lxc=lxc) # Connect to LXC container
    print(client.readTerm())

    while True:
        cmd = input("Enter a command:")

        if cmd.lower() in ["exit", "quit"]:
            break

        client.execCommand(cmd)
        
        print(client.readTerm())
        

    client.disconnect()

if __name__ == "__main__":
    main()
