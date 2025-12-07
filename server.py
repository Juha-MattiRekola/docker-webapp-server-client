# Socket=verkkoyhteys(TCP-socket), os=käyttöjärjestelmä, hashlib=tarkistussumman laskemiseen, random=satunnaisteksti 1 kb, string=merkkijonot, ei tarvetta RegExille tässä
import socket, os, hashlib, random, string

# Hostina mikä tahansa osoite, portti 6000
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 6000))

# Luodaan noin 1KB satunnaista tekstiä. Kirjoitetaan tiedostoon /serverdata/random.txt
data = ''.join(random.choices(string.ascii_letters + string.digits, k=1024))
filepath = "/serverdata/random.txt"
with open(filepath, "w") as f:
    f.write(data)

# Lasketaan tarkistussumma. Käytetään SHA-256-algoritmia
checksum = hashlib.sha256(data.encode()).hexdigest()

# Aloitetaan TCP-palvelin, joka lähettää datan ja tarkistussumman yhdistetylle asiakkaalle. Samalla saadaan myös asiakkaan osoite
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Palvelin kuuntelee portissa {PORT}")
    conn, addr = s.accept()
    with conn:
        print("Yhdistetty osoitteesta", addr)
        conn.sendall(data.encode() + b"\n" + checksum.encode())
