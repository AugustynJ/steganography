import time
from scapy.all import sniff, ICMP, IP

last_packet_time = None
received_bits = []
final_message = ""
timeout_duration = 10


def bits_to_ascii(bits):
    byte = ''.join(bits)
    ascii_char = chr(int(byte, 2))
    return ascii_char


def packet_handler(packet, target_ip="127.0.0.1"):
    global last_packet_time, received_bits, final_message

    if packet.haslayer(ICMP) and packet[ICMP].type == 8 and packet[IP].dst == target_ip:  # Echo Request (ping)
        current_time = time.time()

        if last_packet_time is not None:
            delay = current_time - last_packet_time

            if 0.9 <= delay <= 1.1:
                print(f"Received packet with 1 second delay (bit 0)")
                received_bits.append('0')

            elif 1.9 <= delay <= 2.1:
                print(f"Received packet with 2 seconds delay (bit 1)")
                received_bits.append('1')

            if len(received_bits) >= 8:
                byte_bits = received_bits[:8]
                ascii_char = bits_to_ascii(byte_bits)
                final_message += ascii_char
                print(f"Current message: {final_message}")
                received_bits = received_bits[8:]

        last_packet_time = current_time


def receive_message(target_ip, interface):
    global last_packet_time, final_message

    print(f"Listening for ICMP packets directed to {target_ip} on interface {interface}...")

    last_packet_time = time.time()
    while True:
        sniff(filter=f"icmp and dst host {target_ip}",
              iface=interface,
              prn=lambda pkt: packet_handler(pkt, target_ip),
              timeout=2)

        if time.time() - last_packet_time > timeout_duration:
            print(f"No ICMP packets received in the last {timeout_duration} seconds.")
            print(f"Final message: {final_message}")
            break
    return final_message


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python server.py <your_ip> <interface>")
        sys.exit(1)

    target_ip = sys.argv[1]
    interface = sys.argv[2]
    print(receive_message(target_ip, interface))
