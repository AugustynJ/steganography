#!/bin/bash

#set -x

function usage() {
    echo "Użycie: $0 --server <adres_ip_serwera> --client <adres_ip_klienta> -p <port> --secret-site <secret_site> --dns-forwarder <dns_forwarder> --domains-file <domains_file>"
    echo "  --server <server_ip>     : Adres IP serwera"
    echo "  --client <client_ip>     : Adres IP specjalnego klienta"
    echo "  -p <port>                : Numer portu"
    echo "  --secret-site <secret_site> : Strona rozpoczynająca mechanizm steganografii"
    echo "  --dns-forwarder <dns_forwarder> : Adres IP forwardera DNS"
    echo "  --domains-file <domains_file>            : Plik z nazwami domen"
    echo "  --resolver-file <file>   : Plik z adresami ip domen"
    echo "  --stealth                : Ustaw flagę stealth na true w celu wprowadzenia opóźnień i zmniejszenia prawdopodobieństwa wykrycia"    
    echo "  --agh                    : Ustaw flagę agh_flag na true. Zapytania DNS tylko o domenę agh.edu.pl"    
    exit 1
}

server_ip=""
port=""
secret_site=""
dns_forwarder=""
domains_file=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --server)
            if [[ -n $2 && ! $2 =~ ^- ]]; then
                server_ip="$2"
                shift 2
            else
                echo "Error: --server requires an argument."
                usage
            fi
            ;;
        --client)
            if [[ -n $2 && ! $2 =~ ^- ]]; then
                special_client_ip="$2"
                shift 2
            else
                echo "Error: --client requires an argument."
                usage
            fi
            ;;
        -p)
            if [[ -n $2 && ! $2 =~ ^- ]]; then
                port="$2"
                shift 2
            else
                echo "Error: -p requires an argument."
                usage
            fi
            ;;
        --secret-site)
            if [[ -n $2 && ! $2 =~ ^- ]]; then
                secret_site="$2"
                shift 2
            else
                echo "Default site will be: start.stegano.com"
                secret_site="start.stegano.com"
            fi
            ;;
        --dns-forwarder)
            if [[ -n $2 && ! $2 =~ ^- ]]; then
                dns_forwarder="$2"
                shift 2
            else
                echo "Default dns server: 8.8.8.8"
                dns_forwarder="8.8.8.8"
            fi
            ;;
        --domains-file)
            if [[ -n $2 && ! $2 =~ ^- ]]; then
                domains_file="$2"
                shift 2
            else
                echo "Default domains file: domains.csv"
                domains_file="domains.csv"
            fi
            ;;
        --resolver-file)
            if [[ -n $2 && ! $2 =~ ^- ]]; then
                resolver_file="$2"
                shift 2
            else
                echo "Default resolver file: resolver"
                resolver_file="resolver.csv"
            fi
            ;;
        --stealth)
            stealth_flag=true
            shift
            ;;
        --agh)
            agh_flag=true
            shift
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
            ;;
    esac
done

# Funkcja konwertująca ciąg binarny na tekst
binary_to_text() {
    local binary_string=$1
    local text=""

    if (( ${#binary_string} % 8 != 0 )); then
        echo "Error: długość ciągu binarnego nie jest wielokrotnością 8."
        return 1
    fi

    for (( i=0; i<${#binary_string}; i+=8 )); do
        byte=${binary_string:i:8}
        decimal=$((2#$byte))
        text+=$(printf "\\$(printf '%03o' $decimal)")
    done

    echo "$text"
}

# Funkcja do podkreślania kolorem błędów w transmisji
highlight_difference() {
    local str1="$1"
    local str2="$2"
    local length=${#str1}
    local output=""

    for ((i=0; i<length; i++)); do
        if [[ "${str1:$i:1}" != "${str2:$i:1}" ]]; then
            output+="\e[31m${str2:$i:1}\e[0m"
        else
            output+="${str2:$i:1}"
        fi
    done

    echo -e "$output"
}

error_rate() {
    local result="$1"
    local correct_result="$2"
    local total_bits=${#correct_result}
    local wrong_bits=0

    for (( i=0; i<total_bits; i++ )); do
        if [[ "${result:i:1}" != "${correct_result:i:1}" ]]; then
            ((wrong_bits++))
        fi
    done

    echo "Współczynnik błędów wynosi: $wrong_bits / $total_bits = $(bc -l <<< "$wrong_bits / $total_bits")"
}

# Funkcja do ładowania pliku z domenami do tablicy
load_domains() {
    mapfile -t domains < <(grep -v '^\s*$' "$1")
    total_lines=${#domains[@]}
}

# Funkcja do wyboru losowej domeny
select_random_domain() {
    local random_index=$((RANDOM % total_lines))
    echo "${domains[random_index]}" | cut -d ',' -f2 | tr -d '\r'
}

# Wyświetlenie podanych wartości
# echo "Server IP: $server_ip"
# echo "Client IP: $client_ip"
# echo "Port: $port"
# echo "Secret Site: $secret_site"
# echo "DNS Forwarder: $dns_forwarder"
# echo "DNS resolver file: $resolver_file"
# echo "Domains File: $domains_file"
# echo "AGH flag: $agh_flag"

result=""

load_domains "$domains_file"

start_time=$(date +%s.%N)

# Początkowe zapytanie DNS, otwarcie ukrytego kanału
# echo "Otwarcie ukrytego kanalu z zapytaniem o domenę ${secret_site}"
start_covert_channel=$(dig +short @"${server_ip}" -p "${port}" "${secret_site}")


# Odpytywanie o domeny
while : ; do
    if [[ "$agh_flag" =  true ]]; then
        domain="agh.edu.pl"             # Gwarantuje 100% poprawności
        correct_ip="149.156.96.150"
    else
        domain=$(select_random_domain)
    fi
    correct_ip=""
    covert_channel_ip=""
    # echo "Tworzenie zapytania o domenę: ${domain}"
    while [[ -z $correct_ip ]]; do
        if [[ "$stealth_flag" =  true ]]; then
            sleep $(shuf -i 0-50 -n 1 | awk '{print $1/10}')
        fi
    correct_ip=$(grep -E "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+,${domain}$" "${resolver_file}" | awk -F "," '{print $1}' | head -n 1)
        # Jeśli domena nie została znaleziona w pliku resolver, wykonuje forward zapytania do innego serwera dns
        if [ -z "$correct_ip" ]; then    
            correct_ip=$(dig +short @"${dns_forwarder}" "${domain}" | sort | head -n 1)
            #echo "Wykonano zapytanie do serwera dns ${dns_forwarder} o domene ${domain} i zwrócono adres ip ${correct_ip}"
        fi
        if [[ -z $correct_ip ]]; then
            # echo "Nie znaleziono adresu ip dla tej domeny ${domain}. Próbuję jeszcze raz..."

            domain=$(select_random_domain)
        fi
    done
    
    # Odpowiedź od kontrolowanego serwera DNS
    while [[ -z $covert_channel_ip ]]; do
        covert_channel_ip=$(dig +short @"${server_ip}" -p "${port}" "${domain}" | sort | head -n 1) 
    done

    # echo "Zwrócony adres z resolver lub forwarder: $correct_ip"
    # echo "Zwrócony adres prze kontrolowany serwer: $covert_channel_ip"

    # Porównywanie odpowiedzi DNS od kontrolowanego serwera
    if [[ "$covert_channel_ip" == "$special_client_ip" ]]; then
        echo "Zamknięto ukryty kanał" 
        break 
    elif [[ "$covert_channel_ip" == "$correct_ip" ]]; then
        result+="1"
    elif [[ -z "$covert_channel_ip" && -z "$correct_ip" ]]; then
        result+="1"
    else
        result+="0"
    fi

    #sleep 1
done

end_time=$(date +%s.%N)

# DEBUG
echo "Otrzymany wynik porównań: $result"
correct_result=$(cat bits)
if [[ "$result" !=  "$correct_result" ]]; then
    echo "Powinno być: $(highlight_difference "$correct_result" "$result")"
    
fi

error_rate "$result" "$correct_result"

tekst=$(binary_to_text "$result")
echo "Sekretna wiadomość: ${tekst}"

bit_length=${#correct_result}
duration=$(echo "$end_time - $start_time" | bc)
throughput=$(echo "$bit_length / $duration" | bc)

echo "-----------------------------------"
echo "Długość ciągu bitów: $bit_length"
echo "Czas trwania ukrytego kanału: $duration"
echo "Przepustowość wynosi $throughput bitów na sekundę"
echo "-----------------------------------"