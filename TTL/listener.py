from scapy.all import IP, sniff
import argparse

ttl_values = []
USED_BITS = 4

def remove_padding(bits: str):
    return bits[0:len(bits)-(len(bits)%USED_BITS)]

def ttls_to_bits(ttl_list: list):
    res = ""
    for ttl in ttl_list:
        res += format(ttl%pow(2, USED_BITS), f'0{USED_BITS}b')
    return res

def check_doublers(ttl_list: list):
    for i in range (1, len(ttl_list), 2):
        if ttl_list[i] != ttl_list[i-1]:
            return ttl_list
    
    new_list = ttl_list[::2]
    return new_list

def ttls_to_msg(ttl_list: list):
    ttl_list = check_doublers(ttl_list)
    bits = ttls_to_bits(ttl_list)
    bits = remove_padding(bits)
    res = ""
    for i in range(0, len(bits), 8):
        res += chr(int(bits[i:i+8], 2))
    return res

def read_packet(packet):
    print(f"Just handled packet with {packet[IP].ttl} TTL")
    ttl_values.append(packet[IP].ttl)
    return

def handle_packets(iface: str, port: int):
    filter = f"tcp port {port} and not tcp[13] & 16 != 0"

    sniff(filter=filter, prn=read_packet, iface=iface, timeout=10)
    return ttls_to_msg(ttl_values)

def parse_args():
    parser = argparse.ArgumentParser(description = "Parse for sender.")
    parser.add_argument('-i', '--interface', type=str, default="eth0", help="Name of interface receiving")
    parser.add_argument('-p', '--port', type=int, default=2000, help="Number of port receiving packets")
    parser.add_argument('-ip', '--ip', type=str, required=False, help="Sorce IP address")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    print(f"Message from user: {handle_packets(args.interface, args.port)}")