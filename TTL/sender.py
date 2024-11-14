from scapy.all import IP, TCP, send, sniff

PORT = 2137
IP_DST = "192.168.104.212"
# IP_DST = "127.0.0.1"
DISTANCE = 1

def bytes_to_bits (message: bytes):
    return ''.join(format(byte, '08b') for byte in message)

def send_packet(ip: str, ttl: int):
    ip_packet = IP(dst=ip)
    ip_packet.ttl = ttl
    tcp_packet = TCP(dport=PORT)

    packet = ip_packet/tcp_packet
    # packet.show()
    send(packet, verbose=0)
    return

def read_packet(packet):
    print(f"Just handled packet with {packet[IP].ttl} TTL")
    return

def handle_packet(iface: str):
    sniff(filter="tcp port {PORT} and not tcp[13] & 16 != 0", 
          prn=read_packet, iface=iface, count=64, timeout=10)

def compute_ttl_values(message: str):
    bits = bytes_to_bits(message.encode())
    ttl_list = []
    for i in range (0, len(bits), 4):
        number = int(bits[i:i+4], 2)
        ttl_list.append(number + DISTANCE)
    return ttl_list

def send_message(message: int, ip: str):
    ttl_list = compute_ttl_values(message)
    for element in ttl_list:
        send_packet(ip, element)

