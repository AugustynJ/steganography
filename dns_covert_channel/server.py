import socket
import argparse
from dnslib import DNSRecord, DNSHeader, RR, A, QTYPE
import secrets

SERVER_IP = "0.0.0.0"  
SECRET_DOMAIN = "start.stegano.com"

# Funkcja do generowania losowego adresu ip
def generate_random_ip(existing_ip):
    while True:
        random_bytes = secrets.token_bytes(4)
        random_ip = ".".join(str(b) for b in random_bytes)
        if random_ip != existing_ip:
            return random_ip


# Funkcja do tworzenia odpowiedzi DNS
def create_dns_reply(request, ip_adress):
    dns_reply = DNSRecord(
        DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q
    )
    dns_reply.add_answer(RR(request.q.qname, QTYPE.A, ttl=3600, rdata=A(ip_adress)))
    return dns_reply


# Funkcja do wczytania adresów ip i nazw domen do słownika {domena: ip}
def load_resolver_file(resolver_file):
    resolver_dict = {}
    with open(resolver_file, "r") as file:
        for line in file:
            ip, stored_domain = line.strip().split(",")
            resolver_dict[stored_domain] = ip
    return resolver_dict


# Funkcja do zwrócenia adresu ip domeny przeszukując utworzony słownik {domena: ip}
def get_ip_for_domain_from_resolver(domain, resolver_dict):
    ip = resolver_dict.get(domain)
    if ip:
        #print(f"Znaleziono domenę {domain} w pamięci. Adres ip {ip}")
        return ip
    return None


# Funkcja do utworzenia odpowiedzi DNS korzystając z pamięci. W przeciwnym wypadku przekazuje zapytanie do innego serwera DNS
def create_reply_using_resolver(request, qname, data, forwarder):
    resolver_domain_ip = get_ip_for_domain_from_resolver(qname, resolver_dict)
    if resolver_domain_ip:
        reply = create_dns_reply(request, resolver_domain_ip)
    else:
        reply = forward_request(data, forwarder)
    return reply


# Obsługa zapytania DNS
def handle_request(data, addr, special_client, forwarder, bits_file):
    global bit_index
    global steganography_flag
    global bits_chain
    try:
        #print("")
        request = DNSRecord.parse(data)
        qname = str(request.q.qname).rstrip(".")
        client_ip = addr[0]
        reply = None

        print(f"Otrzymano zapytanie DNS od {client_ip} dla domeny {qname}")

        if client_ip == special_client:
            # Otwarcie ukrytego kanału steganograficznego
            if qname == SECRET_DOMAIN and steganography_flag == False:
                bits_chain = bits_file.strip()
                print(
                    f"Otrzymano zapytanie o otworzenie ukrytego kanału od {special_client}"
                )
                steganography_flag = True
            elif steganography_flag:
                if bit_index < len(bits_chain):
                    bit = bits_chain[bit_index]
                    bit_index += 1

                    if bit == "1":
                        # Zwrócenie prawidłowego adresu ip
                        create_reply_using_resolver(request, qname, data, forwarder)
                    else:
                        correct_reply = create_reply_using_resolver(
                            request, qname, data, forwarder
                        )
                        correct_ip = str(correct_reply.rr).split()[-1]

                        random_ip = generate_random_ip(correct_ip)

                        # Zwrócenie fałszywego adresu ip
                        reply = create_dns_reply(request, random_ip)

                else:
                    print("Zamknięto ukryty kanał")

                    # Zwracanie adresu IP specjalnego klienta po zakończeniu przesyłania ukrytej wiadomości
                    reply = create_dns_reply(request, special_client)
                    steganography_flag = False
                    bit_index = 0
            else:
                reply = None

        if reply is None:
            # Zwrócenie prawidłowego adresu ip dla wszystkich innych klientów
            reply = create_reply_using_resolver(request, qname, data, forwarder)

        return reply.pack()
    except Exception as e:
        print(f"Błąd przetwarzania zapytania: {e}")
        return None


# Funkcja do przesyłania zapytania do innego serwera DNS
def forward_request(data, forwarder):
    dns_record = DNSRecord.parse(data)
    response = dns_record.send(forwarder, 53, timeout=5)
    return DNSRecord.parse(response)


# Funkcja uruchamiająca serwer
def start_server(port, special_client, forwarder, bits_file):
    global steganography_flag
    global bit_index
    steganography_flag = False
    bit_index = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, port))
    print(f"Serwer DNS działa na {SERVER_IP}:{port}")

    # Przesyłanie odpowiedzi DNS do klienta
    while True:
        data, addr = sock.recvfrom(512)
        response = handle_request(data, addr, special_client, forwarder, bits_file)
        if response:
            sock.sendto(response, addr)


# Funkcja analizatora argumentów
def parse_arguments():
    parser = argparse.ArgumentParser(description="Analizator argumentów")

    parser.add_argument(
        "-p", "--server-port", type=int, default=5353, help="Port serwera dns"
    )
    parser.add_argument(
        "-c", "--client", type=str, required=True, help="Adres ip specjalnego klienta"
    )
    parser.add_argument(
        "-f",
        "--forwarder",
        type=str,
        default="8.8.8.8",
        help="Adres ip specjalnego klienta",
    )
    parser.add_argument(
        "-b",
        "--bits-file",
        type=str,
        default="bits",
        help="Ścieżka do pliku z ukrytą wiadomością",
    )
    parser.add_argument(
        "-s",
        "--secret-domain",
        type=str,
        default="start.stegano.com",
        help="Nazwa domeny otwierającej ukryty kanał",
    )
    parser.add_argument(
        "-r",
        "--resolver-file",
        type=str,
        default="resolver.csv",
        help="Ścieżka do lokalnego pliku z adresami ip domen",
    )
    args = parser.parse_args()

    return args


def message_to_bitstring(message: str) -> str:
    return ''.join(f'{ord(char):08b}' for char in message)

def prepare_message(bits_message):
    FORWARDER = "8.8.8.8"
    SPECIAL_CLIENT_IP = "127.0.0.1"
    PORT = 3333
    bits = message_to_bitstring(bits_message)
    RESOLVER_FILE = "dns_covert_channel/resolver.csv"
    
    SERVER_IP = "0.0.0.0"
    print("Przed resolver.")
    global resolver_dict
    resolver_dict = load_resolver_file(RESOLVER_FILE)
    print("Rozpoczynanie nasłuchiwania na zapytania DNS.")
    start_server(PORT, SPECIAL_CLIENT_IP, FORWARDER, bits)

