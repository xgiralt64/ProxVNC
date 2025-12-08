<p>
  <img src="assets/logo.png" alt="logo" width="250"/>
</p>

ProxVNC allows connecting and executing arbitrary commands directly on a Proxmox node/LXC via VNC WebSocket.

## Installation

This package can be installed via PyPI:

`pip install ProxVNC`

## Usage information

See the Examples folder for additional working examples.

#### Connecting via proxmoxer package:

First, create an object to connect to your Proxmox server. For more info read [PROXMOXER](https://proxmoxer.github.io/docs/latest/) documentation. **All authentication methods are supported.**. If you use an **Api token** you must set the permission to `[Sys.console]`

```python
from ProxVNC.proxmoxer import ProxmoxAPI
from ProxVNC import ProxVNC
  
proxmox = ProxmoxAPI(host="<proxmox_host:port>", # ex: 10.0.0.1:8006
                         user="<username@realm>", # ex: "root@pam"
                         password="<password>",
                         otp=input("OTP: "),
                         verify_ssl=False)
```

Create a ProxVNC object and pass the proxmoxer connection via the `api` parameter.
Optionally, specify which node to connect to.

```python
    client = ProxVNC(api=proxmox, node="pve") # specify node if needed, otherwise first node is used by default
  
    client.connect()  
```

You are now connected! Here is a simple example of interacting with the terminal:

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

Use `execCommandAsB64(command: str, wait_time=0.5)` instead of `execCommand()` for complex or large commands. It encodes the command in Base64 and sends it with an optional delay to ensure reliable execution.

#### Connecting direcly with a shell ticket:

You can also connect to the VNC terminal directly by **POSTing to the Proxmox termproxy endpoint**

In this example, PROXMOXER is used to call Proxmox API endpoints, but you can use requests or another package.

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

Once you have the required data, create the ProxVNC object manually:

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

You can now start sending and receiving commands.

#### Sending files:

Using the `sendFile(local_path: str, remote_path: str, wait_time=0.5)` method, you can upload files to a specific location on your Proxmox node or LXC container.

```python
    client.sendFile("testSend.txt", "/root/testReceive.txt")

```

## Contributing

We welcome contributions! Here’s how you can help:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure the code is clean and well-documented.
3. Test your changes thoroughly before submitting.
4. Open a pull request with a clear description of your changes.

Please follow [PEP8](https://peps.python.org/pep-0008/) coding style and include examples if applicable.
