import socket
import json
import time
import argparse

HOST = "127.0.0.1"
PORT = 54321
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345             # public as a start value

def bytes_to_list (message: bytes):
    bits = []
    for byte in message:
        bits.extend([int(bit) for bit in f'{byte:08b}'])
    return bits

def recv_initial_values ():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.connect((SERVER_HOST, SERVER_PORT))

    init_values = json.loads(s.recv(1024).decode())
    p_0 = init_values["p_0"]
    factor = init_values["factor"]
    delta = init_values["delta"]
    MOD = init_values["MOD"]
    TIMEOUT = init_values["TIMEOUT"]
    s.close()
    return p_0, factor, delta, MOD, TIMEOUT

def compute_next_port (last_port: int, factor: int, delta: int, MOD: int):
    next_port = (last_port * factor) % MOD
    if next_port < 1025 or next_port > 65535:
        next_port += delta
        next_port %= MOD
    
    return next_port

def send_msg_to_server (message: bytes, last_port: int, factor: int, delta: int, MOD:int, TIMEOUT: int):
    msg_bits = bytes_to_list(message)
    for bit in msg_bits:
        next_port = compute_next_port(last_port, factor, delta, MOD)

        print("c", next_port)
        if bit == 0:
            time.sleep(TIMEOUT)
            last_port = next_port
            continue

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        time.sleep(0.01)             # to be sure server is listening before client is trying to connect
        s.connect((SERVER_HOST, next_port))
        s.sendall("MSG".encode())
        s.close()

        last_port = next_port

def send_file_to_server(path: str, last_port: int, factor: int, delta: int, MOD: int):
    with open(path, 'rb') as file:
        while True:
            next_port = compute_next_port(last_port)
            chunk = file.read(1024)        # reading 1MB = 1024kB = 1024 * 1024 B
            if not chunk:
                print("File was sent")
                return

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            time.sleep(0.01)             # to be sure server is listening before client is trying to connect
            s.connect((SERVER_HOST, next_port))
            s.sendall(chunk)
            s.close()

            
            last_port = next_port



def parse_args():
    parser = argparse.ArgumentParser(description = "Parse for client.")
    parser.add_argument('-f', '--file', type=str, help="Path to file")
    parser.add_argument('-m', '--message', type=str, help="Message to send")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    p_0, factor, delta, MOD, TIMEOUT = recv_initial_values()

    if args.message is not None:
        if args.file is not None:
            print("Too many arguments!")
            exit(0)
        message = args.message
        message = message.encode()
        send_msg_to_server(message, p_0, factor, delta, MOD, TIMEOUT)
    elif args.file is not None:
        send_file_to_server(args.file, p_0, factor, delta, MOD)
    
        

