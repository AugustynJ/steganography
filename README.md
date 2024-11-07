# steganography
Repo for steganography course AGH UST

Steganografia bazująca na modyfikowaniu rozmiaru wiadomości. 

Jeśli pakiet jest większy od 2000 bitów, to jest to interpretowane jako bit 1, jeśli mniejszy to 0.

## Usage

Uruchomienie nasłuchiwania serwera:

```
sudo python3 receiver.py 127.0.0.1 12345
```

Wysyłanie wiadomości ukrytym kanałem:

```
sudo python3 sender.py 127.0.0.1 12345 bits
```