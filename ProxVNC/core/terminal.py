import select
import time

import websocket

class TerminalHandler:
    def __init__(self, ws_connection):
        self.ws_connection = ws_connection

    def execCommand(self, command: str):
        for char in command:
            self.ws_connection.ws.send("0:1:" + char)
        self.ws_connection.ws.send("0:1:\n")  # Enter

    def sendInput(self, input_data: str):
        for char in input_data:
            self.ws_connection.ws.send("0:1:" + char)

    def sendBinaryInput(self, input_data: bytes):
        for byte in input_data:
            self.ws_connection.ws.send(f"0:1:{chr(byte)}")

    def sendFile(self, local_path: str, remote_path: str, wait_time=0.5):

        import base64

        with open(local_path, "rb") as f:
            b64data = base64.b64encode(f.read()).decode('ascii')

        self.execCommand(f"echo '{b64data}' | base64 -d > {remote_path}")
        time.sleep(wait_time) # Not waiting a delay may cause issues on some systems

    def readUntilPrompt(self, term_prompt="root@pve"):
        buffer = ""
        while True:
            data = self.ws_connection.ws.recv()
            if not data:
                break
            buffer += data.decode("utf-8", errors="ignore")
            if term_prompt in buffer:
                break
        return buffer

    def readTerm(self, wait_time=0.5):
        buffer = ""
        last_data_time = time.time()

        while True:
            rlist, _, _ = select.select([self.ws_connection.ws.sock], [], [], 0)
            if rlist:
                try:
                    data = self.ws_connection.ws.recv()
                    if data:
                        buffer += data.decode("utf-8", errors="ignore")
                        #print(data.decode("utf-8", errors="ignore"))
                        last_data_time = time.time()
                    else:
                        break
                except websocket.WebSocketConnectionClosedException:
                    print("Connection closed")
                    break
            else:
                if time.time() - last_data_time > wait_time:
                    break
                time.sleep(0.01)
        return buffer
