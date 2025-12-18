# =========================================
# CLIENT SIDE – 1 RUN, 2 USER (SENDER+RECEIVER)
# =========================================

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
from pathlib import Path
import os

# =========================================
# KONFIGURASI USER
# =========================================
SENDER = "sofia079"
RECEIVER = "penerima"

KEY_DIR = "punkhazard-keys"
PDF_FILE = "soaluaskid.pdf"

# =========================================
# UTIL: BUAT / LOAD KEY
# =========================================
def load_or_create_key(username):
    os.makedirs(KEY_DIR, exist_ok=True)

    priv_path = f"{KEY_DIR}/{username}_priv.pem"
    pub_path = f"{KEY_DIR}/{username}.pem"

    if not os.path.exists(priv_path):
        print(f"[+] Membuat key untuk {username}")

        priv = Ed25519PrivateKey.generate()
        pub = priv.public_key()

        with open(priv_path, "wb") as f:
            f.write(
                priv.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption()
                )
            )

        with open(pub_path, "wb") as f:
            f.write(
                pub.public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

        return priv

    print(f"[*] Key {username} sudah ada")
    with open(priv_path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


# =========================================
# 1. BUAT KEY 2 USER
# =========================================
sender_priv = load_or_create_key(SENDER)
receiver_priv = load_or_create_key(RECEIVER)

print("\n[✓] Key sender & receiver siap\n")

# =========================================
# 2. SIGN MESSAGE (RELAY + VERIFY)
# =========================================
message = "Halo, semoga selalu diberi kemudahan dan kelancaran"
signature = sender_priv.sign(message.encode())

print("=== DATA UNTUK SWAGGER (/relay atau /verify) ===")
print("sender   :", SENDER)
print("receiver :", RECEIVER)
print("message  :", message)
print("signature:", signature.hex())

# =========================================
# 3. SIGN PDF (YORK + PYTHAGORAS)
# =========================================
pdf_bytes = Path(PDF_FILE).read_bytes()

digest = hashes.Hash(hashes.SHA256())
digest.update(pdf_bytes)
pdf_hash = digest.finalize()

pdf_signature = sender_priv.sign(pdf_hash)

print("\n=== DATA TANDA TANGAN PDF ===")
print("username :", SENDER)
print("signature:", pdf_signature.hex())

# =========================================
# 4. ENKRIPSI PDF (SYMMETRIC – PYTHAGORAS)
# =========================================
aes_key = Fernet.generate_key()
cipher = Fernet(aes_key)
encrypted_pdf = cipher.encrypt(pdf_bytes)

with open("encrypted.pdf", "wb") as f:
    f.write(encrypted_pdf)

print("\n=== ENKRIPSI PDF ===")
print("AES KEY :", aes_key.decode())
print("File    : encrypted.pdf")
