from ProxVNC.proxmoxer import ProxmoxAPI
from ProxVNC import ProxWSVNC

def main():
    
    proxmox = ProxmoxAPI(host="",
                         user="", 
                         password="",
                         otp=input("OTP: "),
                         verify_ssl=False)
    
    termproxy = proxmox.nodes("pve").termproxy.post()

    shell_ticket = termproxy["ticket"]
    shell_port = termproxy["port"]

    pve_cookie, _ = proxmox.get_tokens()

        
    client = ProxWSVNC(
             url="https://",
             node="pve",
             user="",
             shell_port=shell_port,
             shell_ticket=shell_ticket,
             pve_auth_cookie=pve_cookie
            )  
    client.connect(lxc=104)
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
