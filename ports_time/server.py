import socket
import json
import argparse

HOST = "127.0.0.1"
PORT = 12345        # start port of sequence - public for client

p_0 = 42000         # must be in [1; 65535]
factor = 3
delta = 1026        # recommended 1026
MOD = 65537
TIMEOUT = 0.1         # in seconds

def send_initial_values (init_values):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    client_ip, client_port = addr       # client is connected

    json_init_values = json.dumps(init_values)
    conn.sendall(json_init_values.encode())
    conn.close()

def compute_next_port (last_port: int):
    next_port = (last_port * factor) % MOD
    if next_port < 1025 or next_port > 65535:
        next_port += delta
        next_port %= MOD
    
    return next_port

def reading_msg_from_client (last_port: int):
    message = b''
    curr_byte = []
    while True:
        next_port = compute_next_port(last_port)
        print("s", next_port)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, next_port))
        s.listen()
        s.settimeout(TIMEOUT)

        try:
            conn, addr = s.accept()
            data = conn.recv(1024)
            curr_byte.append(1)
            conn.close()
        except socket.timeout:
            curr_byte.append(0)

        if len(curr_byte) == 8:
            single_byte = ''.join(str(bit) for bit in curr_byte)
            single_byte = bytes([int(single_byte, 2)])
            if single_byte == b'\x00':
                s.close()
                return message.decode()                   # program ends
            else:
                message += single_byte
            curr_byte = []

        last_port = next_port

def reading_file_from_client(last_port):
    with open('output_file', 'wb') as file:
        while True:
            next_port = compute_next_port(last_port)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, next_port))
            s.listen()
            s.settimeout(10)

            # print(f"Received bytes on {next_port} port.")
            try:
                conn, addr = s.accept()
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
                conn.close()
            except socket.timeout:
                print("File was recieved")
                return

            last_port = next_port

def parse_args():
    parser = argparse.ArgumentParser(description = "Parse for server.")
    parser.add_argument('-t', '--type', choices=['f', 'm'], required=True, type=str, help="Type of input, '-f' for file, '-m' for str message")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    init_values = {"p_0": p_0, "factor": factor, "delta": delta, "MOD": MOD, "TIMEOUT": TIMEOUT}
    send_initial_values(init_values)

    if args.type == 'm':
        reading_msg_from_client(p_0)
    elif args.type == 'f':
        reading_file_from_client(p_0)
    