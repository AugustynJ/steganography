import time
import sys
import threading
from scapy.all import sniff, ICMP, IP

last_packet_time = None
received_bits = []
final_message = ""
timeout_duration = 20

def bits_to_ascii(bits):
    byte = ''.join(bits)
    ascii_char = chr(int(byte, 2))
    return ascii_char

def packet_handler(packet, target_ip):
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

def timeout_monitor():
    global last_packet_time, final_message
    while True:
        if last_packet_time is not None:
            current_time = time.time()
            if current_time - last_packet_time > timeout_duration:
                print(f"No ICMP packets received in the last {timeout_duration} seconds.")
                print(f"Final message: {final_message}")
                sys.exit(1)
        time.sleep(1)

def main(target_ip):
    print(f"Listening for ICMP packets directed to {target_ip}...")
    monitor_thread = threading.Thread(target=timeout_monitor, daemon=True)
    monitor_thread.start()
    sniff(filter=f"icmp and dst host {target_ip}", prn=lambda pkt: packet_handler(pkt, target_ip))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <your_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    main(target_ip)
