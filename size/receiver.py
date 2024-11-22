import socket
import sys

def better_bits_to_ascii(bit_list):
    bit_string = ''.join(bit_list)
    characters = [
        chr(int(bit_string[i:i+8], 2))
        for i in range(0, len(bit_string), 8)
    ]
    return ''.join(characters)

def bits_to_ascii(bits):
    byte = ''.join(bits)
    ascii_char = chr(int(byte, 2))
    return ascii_char

def start_server(host, port):
    received_bits = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.settimeout(10)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            try:
                data, addr = server_socket.recvfrom(4096)  # Maksymalna wielkość bufora to 4096 bajtów
                data_size_bits = len(data) * 8  # Konwersja na bity

                if data_size_bits >= 2000:
                    bit = '1'
                    received_bits.append(bit)
                else:
                    bit = '0'
                    received_bits.append(bit)
                print(f"Received from {addr}: size = {data_size_bits} bits, interpreted bit = {bit}")

            except socket.timeout:
                print(received_bits)
                return better_bits_to_ascii(received_bits)

    except KeyboardInterrupt:
        print("\nServer stopped.")
        print("Odebrana ukryta wiadomość:")
        print(received_bits)
        return received_bits
    finally:
        server_socket.close()

if __name__ == "__main__":
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    start_server(server_host,server_port)
