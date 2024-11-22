import socket
import random
import sys

def read_bits_from_file(filename):
    with open(filename, 'r') as file:
        bits = file.read().strip()
    return bits

def send_packet(client_socket, server_address, bit):
    if bit == '1':
        data_size_bits = random.randint(2000, 2500)
    else:
        data_size_bits = random.randint(500, 1500)

    data_size_bytes = data_size_bits // 8
    data = b'x' * data_size_bytes

    client_socket.sendto(data, server_address)
    print(f"Sent bit {bit} as packet size {data_size_bits} bits (actual bytes: {data_size_bytes})")

def start_client(server_host, server_port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_host, server_port)
    
    bits = read_bits_from_file(filename)

    for bit in bits:
        send_packet(client_socket, server_address, bit)

    client_socket.close()

if __name__ == "__main__":
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]
    
    start_client(server_host, server_port, filename)
