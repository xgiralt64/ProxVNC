from ProxWSVNC.proxmoxer import ProxmoxAPI
from ProxWSVNC import ProxWSVNC

def main():
    # --- ProxmoxAPI ---
    
    proxmox = ProxmoxAPI(host="", #De vegades no funciona 
                         user="root@pam", 
                         password="",
                         otp=input("OTP: "),
                         verify_ssl=False)
        
    client = ProxWSVNC(api=proxmox)
    client.connect()

    while True:
        cmd = input("Enter a command:")

        client.execCommand(cmd)
        
        client.readTerm()
        


if __name__ == "__main__":
    main()
