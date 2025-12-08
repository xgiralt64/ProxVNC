import urllib.parse

from .utils import * 
from ..proxmoxer.core import ProxmoxAPI
from .connection import WSConnection
from .terminal import TerminalHandler

class ProxVNC:
    def __init__(self, api: "ProxmoxAPI" = None, *, url=None, node=None, user=None, shell_port=None, shell_ticket=None, pve_auth_cookie=None):
        self._store = {}
        if all(x is not None for x in [api]): # Provide only ProxmoxAPI (User, node default)
            self._store["api"] = api
            self._store["url"] = api._store["base_url"]

            if node is not None:
                if node not in [n["node"] for n in api.nodes.get()]:
                    raise ValueError(f"Node '{node}' not found in Proxmox cluster.")
                self._store["node"] = node
            else:
                self._store["node"] = api.nodes.get()[0]["node"] # ex: "pve" by default first node

            self._store["user"] = api.access.users.get()[0]["userid"] # ex: "root@pam"

        elif all(x is not None for x in [url, node, user, shell_port, shell_ticket, pve_auth_cookie]):
            for key, value in [("url", url), ("node", node), ("user", user), ("shell_port", shell_port), ("shell_ticket", shell_ticket), ("pve_auth_cookie", pve_auth_cookie)]:
                self._store[key] = value
                
        else:
            raise ValueError("Provide either ProxmoxAPI or all parameters.")

        self.connection = None
        self.terminal = None

    def connect(self, lxc=None, timeoutHandshake=2):
        api = self._store.get("api")
        wss_url = self._store["url"].replace("https://", "wss://", 1)

        if api:

            pve_cookie, _ = api.get_tokens()
            cookie_header = f"PVEAuthCookie={pve_cookie}"

            if lxc is not None:
                termproxy = api.nodes(self._store["node"]).lxc(lxc).termproxy.post()

                shell_ticket = termproxy["ticket"]
                shell_port = termproxy["port"]
                ws_url = f"{wss_url}/nodes/{self._store['node']}/lxc/{lxc}/vncwebsocket?port={shell_port}&vncticket={urllib.parse.quote_plus(shell_ticket)}"

            else:
                # Connect to the node terminal
                termproxy = api.nodes(self._store["node"]).termproxy.post()

                shell_ticket = termproxy["ticket"]
                shell_port = termproxy["port"]
                ws_url = f"{wss_url}/nodes/{self._store['node']}/vncwebsocket?port={shell_port}&vncticket={urllib.parse.quote_plus(shell_ticket)}"



            self.connection = WSConnection(ws_url, cookie_header)
            self.connection.connect()

            self.connection.ws.send(f"{self._store['user']}:{shell_ticket}\n")
            self.connection.ws.send("1:86:24:")  # resolution

            if not waitHandshake(self.connection.ws, timeoutHandshake):
                raise TimeoutError("Handshake timed out.")
            
            self.connection.startKeepAlive()

            self.terminal = TerminalHandler(self.connection)
        else:

            if lxc is not None:
                ws_url = f"{wss_url}/api2/json/nodes/{self._store['node']}/lxc/{lxc}/vncwebsocket?port={self._store['shell_port']}&vncticket={urllib.parse.quote_plus(self._store['shell_ticket'])}"
            else:
                ws_url = f"{wss_url}/api2/json/nodes/{self._store['node']}/vncwebsocket?port={self._store['shell_port']}&vncticket={urllib.parse.quote_plus(self._store['shell_ticket'])}"
            
            cookie_header=f"PVEAuthCookie={self._store['pve_auth_cookie']}"

            self.connection = WSConnection(ws_url, cookie_header)
            self.connection.connect()

            self.connection.ws.send(f"{self._store['user']}:{self._store['shell_ticket']}\n")
            self.connection.ws.send("1:86:24:")  # resolution

            if not waitHandshake(self.connection.ws, timeoutHandshake):
                raise TimeoutError("Handshake timed out.")
            
            self.connection.startKeepAlive()

            self.terminal = TerminalHandler(self.connection)


# ---------------- Wrappers ----------------
    def execCommand(self, command: str):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        self.terminal.execCommand(command)
    
    def execCommandAsB64(self, command: str, wait_time=0.5):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        self.terminal.execCommandAsB64(command, wait_time)

    def readUntilPrompt(self, termPrompt="root@pve"):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        return self.terminal.readUntilPrompt(termPrompt)

    def readTerm(self, waitTime=0.5):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        return self.terminal.readTerm(waitTime)
    
    def disconnect(self):
        if self.terminal is not None:
            self.connection.disconnect()
            self.connection = None
            self.terminal = None

    def sendInput(self, input_data: str):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        self.terminal.sendInput(input_data)
    
    def sendBinaryInput(self, input_data: bytes):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        self.terminal.sendBinaryInput(input_data)

    def sendFile(self, local_path: str, remote_path: str, wait_time=0.5):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        self.terminal.sendFile(local_path, remote_path, wait_time)