import socket

PORT = 4444
IP = "127.0.0.1"

def send_message(message: bytes, port: int, IP: str):
    message = encode_message(message.encode(), port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    s.sendall(message)
    s.close()
    return

def encode_message(message: bytes, port: int):
    port = port.to_bytes(2, 'big')
    key = (port * (len(message)//len(port) + 1))[:len(message)]
    message = bytes([m ^ k for m, k in zip(message, key)])
    return(message)

if __name__ == "__main__":
    message = "Hello steganography word!"
    
    send_message(message, PORT, IP)