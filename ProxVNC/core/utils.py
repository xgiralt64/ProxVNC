import time
import websocket

def waitHandshake(ws, timeout=2):
    """
    Waits to receive exactly b'OK' as the vnc proxmox handshake.
    If it does not arrive before the timeout, returns False.
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            data = ws.recv()
        except websocket.WebSocketTimeoutException:
            #No handsake received yet,
            continue
        except Exception as e:
            print("Error while waiting for handshake: ", e)
            return False

        if data == b'OK':
            return True

    print("Timeout while waiting for handshake.")
    return False