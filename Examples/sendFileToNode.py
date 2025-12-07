from ProxVNC.proxmoxer import ProxmoxAPI
from ProxVNC import ProxVNC
import time

def main():
    # --- ProxmoxAPI ---
    
    proxmox = ProxmoxAPI(host="<proxmox_host:port>", # ex: 10.0.0.1:8006
                         user="<username@realm>", # ex: "root@pam"
                         password="<password>",
                         otp=input("OTP: "),
                         verify_ssl=False)
        
    client = ProxVNC(api=proxmox, node="pve") # specify node if needed, otherwise first node is used by default
    
    client.connect()
    
    print(client.readTerm())
    # --- Send a file ---

    client.sendFile("testSend.txt", "/root/testReceive.txt")

    client.disconnect()

if __name__ == "__main__":
    main()
