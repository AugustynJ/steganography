# steganography
Repo for steganography course AGH UST

Steganografia bazująca na protokole DNS. Bazuje na interpretacji zwracanych odpowiedzi od serwera.

Serwer ma dla klienta przygotowaną wiadomość w formie ciągu bitowów `bits`. 

Komunikacja rozpoczyna się otwarciem ukrytego kanału za pomocą ustalonej domeny np. `start.stegano.com`

Następnie klient zadaje zapytania do serwera DNS i na podstawie zwróconej odpowiedzi (prawidłowości adres ip) interpretuje ciąg bitów.

## Usage

Serwer:
```
sudo venv/bin/python dns_server.py -p 53535 -c 127.0.0.1 --resolver-file resolver.csv
```

Klient:
```
./client.sh -p 53535 --server 127.0.0.1 --client 127.0.0.1 --domains-file domains_mixed.csv --dns-forwarder 8.8.8.8  --resolver-file resolver.csv --secret-site start.stegano.com --agh
```

druga metoda

Klient:
```
./client.sh -p 53535 --server 127.0.0.1 --client 127.0.0.1 --domains-file domains_mixed.csv --dns-forwarder 8.8.8.8  --resolver-file resolver.csv --secret-site start.stegano.com
```