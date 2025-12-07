# Importataan muuten samat kirjastot kuin serverissä, mutta ei tarvita randomia ja stringiä. Ei tarvitse tehdä hölynpölytekstiä
import socket, os, hashlib

# Määritellään serverin osoite ja portti, joihin yhdistetään
SERVER = os.environ.get("SERVER", "server")
PORT = int(os.environ.get("PORT", 6000))

# Yhdistetään palvelimeen ja vastaanotetaan data sekä tarkistussumma
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER, PORT))
    received = s.recv(8192).decode()

# Erotellaan data ja tarkistussumma. Tiedosto tallennetaan /clientdata/received.txt -sijaintiin
data, checksum = received.split("\n")
filepath = "/clientdata/received.txt"

# Kirjoitetaan vastaanotettu data tiedostoon, aiemmin annettuun polkuun
with open(filepath, "w") as f:
    f.write(data)

# Lasketaan SHA-256 checksum vastaanotetusta datasta
local_checksum = hashlib.sha256(data.encode()).hexdigest()
if local_checksum == checksum:
    print("Tiedoston siirto onnistui, SHA-256 tarkistussumma täsmää. Onnittelut!")
else:
    print("Tarkistussumma ei täsmää")
