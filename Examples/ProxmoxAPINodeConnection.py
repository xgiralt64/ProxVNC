from ProxVNC.proxmoxer import ProxmoxAPI
from ProxVNC import ProxVNC

def main():
    # --- ProxmoxAPI ---
    
    proxmox = ProxmoxAPI(host="",
                         user="", 
                         password="",
                         otp=input("OTP: "),
                         verify_ssl=False)
        
    client = ProxVNC(api=proxmox, node="pve")
    client.connect(timeoutHandshake=2)
    print(client.readTerm())

    while True:
        cmd = input("Enter a command: ")

        if cmd.lower() in ["exit", "quit"]:
            break

        client.execCommand(cmd)
        
        print(client.readTerm())
        

    client.disconnect()

if __name__ == "__main__":
    main()
