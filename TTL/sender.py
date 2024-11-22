from scapy.all import IP, TCP, send
import psutil
import socket
import subprocess
import argparse

own_ip = []
USED_BITS = 4
port = 1111

def bytes_to_bits (message: bytes):
    return ''.join(format(byte, '08b') for byte in message)

def add_padding(message: str):
    while len(message) % USED_BITS:
        message += '0'
    return message

def get_own_ip ():
    interfaces = psutil.net_if_addrs()
    for _, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:        # only for IPv4
                own_ip.append(address.address)
    return own_ip

def count_hops(IP_DST, port):
    if (IP_DST in own_ip):
        return 0

    command = ["sudo", "traceroute", "-T", "-p", str(port), IP_DST]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    hop_count = len(result.stdout.splitlines()) - 2     # first line is with headings, last is result
    print(hop_count)

    return hop_count

def send_packet(ip: str, ttl: int):
    ip_packet = IP(dst=ip)
    ip_packet.ttl = ttl
    tcp_packet = TCP(dport=port)

    packet = ip_packet/tcp_packet
    # packet.show()
    send(packet, verbose=False)
    return

def compute_ttl_values(message: str):
    bits = bytes_to_bits(message.encode())
    bits = add_padding(bits)
    ttl_list = []
    for i in range (0, len(bits), USED_BITS):
        number = int(bits[i:i+USED_BITS], 2)
        if(not number):
            number += pow(2, USED_BITS)
        ttl_list.append(number)
    return ttl_list

def send_message(message: str, ip: str):
    ttl_list = compute_ttl_values(message)
    for element in ttl_list:
        send_packet(ip, element)
    print("All packets are sent.")
    return

def parse_args():
    parser = argparse.ArgumentParser(description = "Parse for sender.")
    parser.add_argument('-m', '--message', required=True, type=str, help="Type message to send")
    parser.add_argument('-ip', '--ip_dst', required=True, type=str, help="IP of receiver")
    parser.add_argument('-p', '--port', type=int, default=2000, help="Number of port to send packets")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    message = args.message
    port = 2000

    get_own_ip()

    send_message(message, args.ip_dst)