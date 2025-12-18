# File utama API yang menjadi core logic dari layanan keamanan (security service)
# Peran server dijelaskan pada soal
# TIPS: Gunakan file .txt sederhana untuk menyimpan data-data pengguna

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import os
from datetime import datetime
from contextlib import contextmanager
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
#secure session
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta


app = FastAPI(title="Security Service", version="1.0.0")

# SETUP FOLDER
DATA_DIR = "data"
UPLOAD_DIR = "uploads/pdf"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

PUBKEY_FILE = os.path.join(DATA_DIR, "pubkeys.txt")
MESSAGE_FILE = os.path.join(DATA_DIR, "messages.txt")

#TOKEN JWT
#KONFIGURASI JWT
SECRET_KEY = "super-secret-key-kid-uas"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()
#ENPOINT LOGIN
USERS = {
    "sofia079": "password123",
    "penerima": "password123"
}

@app.post("/login")
async def login(username: str, password: str):
    if USERS.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

#VALIDASI TOKEN
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#HEALTH CHECK
# Fungsi contoh untuk memeriksa apakah layanan berjalan dengan baik (health check)
@app.get("/health")
async def health_check():
    return {
        "status": "Security Service is running",
        "timestamp": datetime.now().isoformat()
    }

#ROOT
# Fungsi akses pada lokasi "root" atau "index"
@app.get("/")
async def get_index() -> dict:
	return {
		"message": "Hello world! Please visit http://localhost:8080/docs for API UI."
	}

# Fungsi contoh untuk mengunggah file pdf
# Akses API pada URL http://localhost:8080/upload-pdf
#UPLOAD PDF
@app.post("/upload-pdf")
async def upload_pdf(
    username: str,
    signature: str,
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    pubkey_path = f"punkhazard-keys/{username}.pem"

    if not os.path.exists(pubkey_path):
        raise HTTPException(status_code=404, detail="Public key user tidak ditemukan")

    pdf_bytes = await file.read()

    # HASH PDF
    digest = hashes.Hash(hashes.SHA256())
    digest.update(pdf_bytes)
    pdf_hash = digest.finalize()

    # LOAD PUBLIC KEY
    with open(pubkey_path, "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())

# VERIFY SIGNATURE
    try:
        pub_key.verify(
            bytes.fromhex(signature),
            pdf_hash
        )
    except InvalidSignature:
        raise HTTPException(status_code=400, detail="Signature PDF tidak valid")

    # SIMPAN PDF
    os.makedirs("uploads", exist_ok=True)
    save_path = f"uploads/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(pdf_bytes)

    return {
        "message": "PDF berhasil diverifikasi dan disimpan",
        "user": username,
        "file": file.filename,
        "timestamp": datetime.now().isoformat()
    }
    
# STORE PUBLIC KEY
@app.post("/store")
async def store_pubkey(username: str, pubkey: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    # pesan kembalian ke user (sukses/gagal)
    msg = None

    try:
        contents = await pubkey.read()

        os.makedirs("punkhazard-keys", exist_ok=True)
        save_path = os.path.join("punkhazard-keys", f"{username}.pem")

        with open(save_path, "wb") as f:
            f.write(contents)

        msg = "Public key stored successfully"

    except Exception as e:
        msg = str(e)
    
    # Nilai kembalian berupa dictionary
    # Tambahkan keys dan values sesuai dengan kebutuhan
    return {
        "message": msg,
        "user": username   
    }
    

#VERIFY SIGNATURE
@app.post("/verify")
async def verify(username: str, message: str, signature: str, current_user: str = Depends(get_current_user)):
    pub_key = os.path.join("punkhazard-keys", f"{username}.pem")

    # 1. Cek public key
    if not os.path.exists(pub_key):
        return {"message": "Public key not found"}

    try:
        # 2. Load public key
        with open(pub_key, "rb") as f:
            pub_key = serialization.load_pem_public_key(f.read())

        # 3. Verifikasi signature
        pub_key.verify(
            bytes.fromhex(signature),
            message.encode()
        )

        return {
            "message": "Signature valid",
            "username": username
        }

    except Exception:
        return {
            "message": "Signature invalid",
            "username": username
        }


#RELAY
@app.post("/relay")
async def relay(
    sender: str,
    receiver: str,
    message: str,
    signature: str,
    current_user: str = Depends(get_current_user)
):
    sender_pubkey_path = f"punkhazard-keys/{sender}.pem"
    receiver_pubkey_path = f"punkhazard-keys/{receiver}.pem"

    # 1. Cek user terdaftar
    if not os.path.exists(sender_pubkey_path):
        raise HTTPException(status_code=404, detail="Sender tidak terdaftar")

    if not os.path.exists(receiver_pubkey_path):
        raise HTTPException(status_code=404, detail="Receiver tidak terdaftar")

    # 2. Load public key pengirim
    with open(sender_pubkey_path, "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())

    # 3. Verifikasi signature
    try:
        pub_key.verify(
            bytes.fromhex(signature),
            message.encode()
        )
    except InvalidSignature:
        raise HTTPException(
            status_code=400,
            detail="Signature tidak valid, pesan mungkin telah diubah"
        )

    # 4. Simpan pesan (simulasi relay)
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.now().isoformat()
    with open("data/relay_log.txt", "a") as f:
        f.write(f"[{timestamp}] {sender} -> {receiver}: {message}\n")

    return {
        "message": "Pesan berhasil direlay dan terverifikasi",
        "from": sender,
        "to": receiver,
        "content": message
    }