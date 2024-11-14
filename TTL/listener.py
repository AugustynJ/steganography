from scapy.all import IP, TCP, send, sniff

PORT = 2137
INTERFACE = 'lo'
ttl_values = []

def ttls_to_bits(ttl_list: list):
    res = ""
    for ttl in ttl_list:
        res += format(ttl, f'04b')
    return res

def ttls_to_msg(ttl_list: list):
    bits = ttls_to_bits(ttl_list)
    print(bits)
    res = ""
    for i in range(0, len(bits), 8):
        res += chr(int(bits[i:i+8], 2))
    return res

def read_packet(packet):
    print(f"Just handled packet with {packet[IP].ttl} TTL")
    ttl_values.append(packet[IP].ttl)
    return

def handle_packets(iface: str):
    sniff(filter=f"tcp port {PORT} and not tcp[13] & 16 != 0", 
          prn=read_packet, iface=iface, count=64, timeout=10)
    return ttls_to_msg(ttl_values)

if __name__ == "__main__":
    print(f"Message from user: {handle_packets(INTERFACE)}")