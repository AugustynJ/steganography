# Steganografia

Program został stworzony jako projekt z przedmiotu ,,Steganografia" realizowanego na 7 semestrze Cyberbezpieczństwa. 

Główny moduł programu został napisany z użyciem frameworku `Flask` w języku python wraz z użyciem szablonów języka `HTML/CSS`. opisuje on metody komunikacji z uzyciem steganografii sieciowej. Aplikacja zawiera przyjazny dla użytkownika interfejs graficzny oraz panel z opisem pomocy dla korzystającego.

Z założenia komunikacja odbywa się z użyciem portu `localhost`, lecz została także przystosowana do komunikacji między dwoma odrębnymi maszynami. Preferowany system hosta to Linux.

Aby uruchomić aplikację należy wpierw pobrać niezbędne do działania biblioteki poleceniem:
```bash
pip install -r requirements.txt
```
a następnie uruchomić serwer komendą:
```bash
/bin/python3 app.py
```
powyższe polecenia należy uruchomić z poziomu admina (sudo).
