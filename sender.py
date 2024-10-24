import time
import sys
from scapy.all import IP, ICMP, send

def load_bits(bits_file):
    with open(bits_file, 'r') as f:
        bits = f.read().strip()
    return bits

def send_icmp_packet(ip_address):
    packet = IP(dst=ip_address) / ICMP()
    send(packet, verbose=False)

def main(ip_address, bits_file):
    bits = load_bits(bits_file)
    send_icmp_packet(ip_address)
    for bit in bits:
        if bit == '1':
            time.sleep(2)
            print(f"Sending ICMP packet to {ip_address} after 2s delay (bit = 1).")
            send_icmp_packet(ip_address)
        elif bit == '0':
            time.sleep(1)
            print(f"Sending ICMP packet to {ip_address} after 1s delay (bit = 0).")
            send_icmp_packet(ip_address)
        else:
            print(f"Invalid bit: {bit}, skipping.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <remote_ip> <bits_file>")
        sys.exit(1)

    remote_ip = sys.argv[1]
    bits_file = sys.argv[2]

    main(remote_ip, bits_file)
