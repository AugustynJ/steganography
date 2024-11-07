import socket

PORT = 4444
IP = "127.0.0.1"

def decode_message(data: bytes, port: int):
    port = port.to_bytes(2, 'big')
    key = (port * (len(data)//len(port) + 1))[:len(data)]
    result = bytes([m ^ k for m, k in zip(data, key)])
    return result.decode()

def receive_message (port: int, IP: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.settimeout(10)
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
    
    message = decode_message(data, port)
    return message

if __name__ == "__main__":
    print(receive_message(PORT, IP))