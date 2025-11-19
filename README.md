# ProxVNC

ProxVNC allows connecting and executing arbitrary commands direcly to a proxmox node/lxc via vnc websocket.

### Installation

This package can be installed via Pypi.

`pip install ProxVNC `

### Usage information

See Examples folder for more working examples.

#### Connecting via proxmoxer package:

First create an object to connect to your proxmox server. For more info read [PROXMOXER](https://proxmoxer.github.io/docs/latest/) documentation. **All auth methods are supported**. If you use an **Api token** you must set the perms to `[Sys.console]`

```python
from ProxVNC.proxmoxer import ProxmoxAPI
from ProxVNC import ProxVNC
  
proxmox = ProxmoxAPI(host="<proxmox_host:port>", # ex: 10.0.0.1:8006
                         user="<username@realm>", # ex: "root@pam"
                         password="<password>",
                         otp=input("OTP: "),
                         verify_ssl=False)
```

Create a ProxVNC object and give the proxmoxer connection via the api parameter, optionaly you can specify to which node connect.

```python
    client = ProxVNC(api=proxmox, node="pve") # specify node if needed, otherwise first node is used by default
  
    client.connect()  
```

You are now conected! Here there is a simple code to interact with the terminal

```python
    print(client.readTerm())
    # --- Interact with terminal ---
    while True:
        cmd = input("Enter a command: ")

        if cmd.lower() in ["exit", "quit"]: # Keywords to exit
            break

        client.execCommand(cmd) # Execute the command
  
        print(client.readTerm()) # Read the terminal

    client.disconnect() # Don't forget to disconnect when you're done
```

#### Connecting direcly with shell ticket:

You can also connect to the VNC terminal direcly **POSTing to the termproxy Proxmox endpoint**

In this example PROXMOXER will be used to call Proxmox API endpoints but you can use the requests or another package.

```python
    proxmox = ProxmoxAPI(host="<proxmox_host:port>", # ex: 10.0.0.1:8006
                         user="", # ex: "root@pam"
                         password="<password>",
                         otp=input("OTP: "),
                         verify_ssl=False)
  
    termproxy = proxmox.nodes("pve").termproxy.post() # POST to termproxy with the node you want to connect to
  
    # Get shell ticket and port
    shell_ticket = termproxy["ticket"] 
    shell_port = termproxy["port"]

    pve_cookie, _ = proxmox.get_tokens() # Get cookie token
```

When you have all the required data, you can create the ProxVNC Object with all the params.

```python
    client = ProxVNC(
             url="https://<proxmox_host:port>",
             node="pve",
             user="<username@realm>",
             shell_port=shell_port,
             shell_ticket=shell_ticket,
             pve_auth_cookie=pve_cookie
            )  

     client.connect()
```

And now you can start sending and reciving commands.
