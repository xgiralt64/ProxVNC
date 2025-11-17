import threading
import time
import websocket
import ssl

class WSConnection:
    def __init__(self, ws_url, cookie_header=None, keep_alive_interval=10):
        self.ws_url = ws_url
        self.cookie_header = cookie_header
        self.keep_alive_interval = keep_alive_interval
        self.ws = None
        self._keep_alive_thread = None
        self._keep_alive_running = False

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(
            self.ws_url,
            sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False},
            cookie=self.cookie_header
        )
        self.start_keep_alive()

    def disconnect(self):
        self.stop_keep_alive()
        if self.ws:
            try:
                self.ws.close()
            except:
                pass
        self.ws = None

    # ------------------ Keep Alive ------------------
    def start_keep_alive(self):
        if self._keep_alive_thread is not None:
            return

        self._keep_alive_running = True

        def run():
            while self._keep_alive_running:
                try:
                    self.ws.send("2")
                except:
                    break
                time.sleep(self.keep_alive_interval)

        self._keep_alive_thread = threading.Thread(target=run, daemon=True)
        self._keep_alive_thread.start()

    def stop_keep_alive(self):
        self._keep_alive_running = False
        self._keep_alive_thread = None
