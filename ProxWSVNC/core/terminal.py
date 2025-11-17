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
        buffer = b""
        last_data_time = time.time()

        while True:
            rlist, _, _ = select.select([self.ws_connection.ws.sock], [], [], 0)
            if rlist:
                try:
                    data = self.ws_connection.ws.recv()
                    if data:
                        buffer += data
                        print(data.decode("utf-8", errors="ignore"))
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
