from scapy.all import IP, TCP, send, sniff

def send_packet(ip: str, ttl: int):
    ip_packet = IP(dst=ip)
    ip_packet.ttl = ttl
    tcp_packet = TCP(dport=2137)

    packet = ip_packet/tcp_packet
    packet.show()
    send(packet)
    return

def read_packet(packet):
    print(f"Just handled packet with {packet[IP].ttl} TTL")
    return

def handle_packet(iface: str):
    sniff(filter="tcp port 2137 and not tcp[13] & 16 != 0", 
          prn=read_packet, iface=iface, count=64, timeout=10)

handle_packet("lo")