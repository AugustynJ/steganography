from scapy.all import IP, TCP, send, sniff

PORT = 2137
IP_DST = "127.0.0.1"
ttl_values = []

def bytes_to_bits (message: bytes):
    return ''.join(format(byte, '08b') for byte in message)

def send_packet(ip: str, ttl: int):
    ip_packet = IP(dst=ip)
    ip_packet.ttl = ttl
    tcp_packet = TCP(dport=PORT)

    packet = ip_packet/tcp_packet
    packet.show()
    send(packet)
    return

def compute_ttl_values(message: str):
    bits = bytes_to_bits(message.encode())
    ttl_list = []
    for i in range (0, len(bits), 4):
        number = int(bits[i:i+4], 2)
        ttl_list.append(number)
    return ttl_list

def send_message(message: int, ip: str):
    ttl_list = compute_ttl_values(message)
    for element in ttl_list:
        send_packet(ip, element)






def ttls_to_bits(ttl_list: list):
    res = ""
    for ttl in ttl_list:
        res += format(ttl, f'04b')
    return res

def ttls_to_msg(ttl_list: list):
    bits = ttls_to_bits(ttl_list)
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