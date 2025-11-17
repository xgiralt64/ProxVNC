from ProxWSVNC.proxmoxer import ProxmoxAPI
from ProxWSVNC import ProxWSVNC

def main():
    
    proxmox = ProxmoxAPI(host="",
                         user="root@pam", 
                         password="",
                         otp=input("OTP: "),
                         verify_ssl=False)
    
    termproxy = proxmox.nodes("pve").termproxy.post()

    shell_ticket = termproxy["ticket"]
    shell_port = termproxy["port"]

    pve_cookie, _ = proxmox.get_tokens()

        
    client = ProxWSVNC(
             url="",
             node="pve",
             shell_port=shell_port,
             shell_ticket=shell_ticket,
             pve_auth_cookie=pve_cookie
            )  
    client.connect()

    while True:
        cmd = input("Enter a command:")
        
        client.execCommand(cmd)
        
        client.readTerm()
        


if __name__ == "__main__":
    main()
