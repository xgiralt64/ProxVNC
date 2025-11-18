from ProxVNC.proxmoxer import ProxmoxAPI
from ProxVNC import ProxVNC

def main():
    
    proxmox = ProxmoxAPI(host="<proxmox_host:port>", # ex: 10.0.0.1:8006
                         user="", # ex: "root@pam"
                         password="<password>",
                         otp=input("OTP: "),
                         verify_ssl=False)
    
    termproxy = proxmox.nodes("pve").termproxy.post()

    shell_ticket = termproxy["ticket"]
    shell_port = termproxy["port"]

    pve_cookie, _ = proxmox.get_tokens()

        
    client = ProxVNC(
             url="https://<proxmox_host:port>",
             node="pve",
             user="<username@realm>",
             shell_port=shell_port,
             shell_ticket=shell_ticket,
             pve_auth_cookie=pve_cookie
            )  
    client.connect()
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
