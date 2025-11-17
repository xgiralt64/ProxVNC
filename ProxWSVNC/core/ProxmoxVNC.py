import urllib.parse
from ..proxmoxer.core import ProxmoxAPI
from .connection import WSConnection
from .terminal import TerminalHandler

class ProxWSVNC:
    def __init__(self, api: "ProxmoxAPI" = None, *, url=None, node=None, shell_port=None, shell_ticket=None, pve_auth_cookie=None):
        self._store = {}
        if api is not None:
            self._store["api"] = api
            self._store["url"] = api._store["base_url"]
        elif all(x is not None for x in [url, node, shell_port, shell_ticket, pve_auth_cookie]):
            for key, value in [("url", url), ("node", node), ("shell_port", shell_port), ("shell_ticket", shell_ticket), ("pve_auth_cookie", pve_auth_cookie)]:
                self._store[key] = value
        else:
            raise ValueError("Provide either ProxmoxAPI or all parameters.")

        self.connection = None
        self.terminal = None

    def connect(self):
        api = self._store.get("api")
        if api:
            termproxy = api.nodes("pve").termproxy.post()

            wss_url = self._store["url"].replace("https://", "wss://", 1)


            shell_ticket = termproxy["ticket"]
            shell_port = termproxy["port"]

            ws_url = f"{wss_url}/nodes/pve/vncwebsocket?port={shell_port}&vncticket={urllib.parse.quote_plus(shell_ticket)}"
            pve_cookie, _ = api.get_tokens()
            cookie_header = f"PVEAuthCookie={pve_cookie}"

            self.connection = WSConnection(ws_url, cookie_header)
            self.connection.connect()

            self.connection.ws.send(f"root@pam:{shell_ticket}\n")
            self.connection.ws.send("1:86:24:")  # resolution

            self.terminal = TerminalHandler(self.connection)
        else:
            wss_url = self._store["url"].replace("https://", "wss://", 1)

            ws_url = f"{wss_url}/api2/json/nodes/pve/vncwebsocket?port={self._store['shell_port']}&vncticket={urllib.parse.quote_plus(self._store['shell_ticket'])}"
            cookie_header=f"PVEAuthCookie={self._store['pve_auth_cookie']}"

            print(ws_url, cookie_header)

            self.connection = WSConnection(ws_url, cookie_header)
            self.connection.connect()

            self.connection.ws.send(f"root@pam:{self._store['shell_ticket']}\n")
            self.connection.ws.send("1:86:24:")  # resolution

            self.terminal = TerminalHandler(self.connection)


# ---------------- Wrappers ----------------
    def execCommand(self, command: str):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        self.terminal.execCommand(command)

    def readUntilPrompt(self, termPrompt="root@pve"):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        return self.terminal.readUntilPrompt(termPrompt)

    def readTerm(self, waitTime=0.5):
        if self.terminal is None:
            raise RuntimeError("Terminal not initialized. Call connect() first.")
        return self.terminal.readTerm(waitTime)