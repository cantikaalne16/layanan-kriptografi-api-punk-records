# IMPLEMENTASI KRIPTOGRAFI MENGGUNAKAN AES-256, ED25519, SHA-256, & HS256 PADA LAYANAN PUNK RECORDS BERBASIS FASTAPI
## Ujian Akhir Semester Mata Kuliah Keamanan dan Integritas Data
## Sains Data - Universitas Negeri Surabaya
------------------------------------------------------------------------------
#### Dosen Pengampu: 
##### 1. Hasanuddin Al-Habib, M.Si.
##### 2. Moh. Khoridatul Huda, S.Pd., M.Si., Ph.D.
------------------------------------------------------------------------------
#### Disusun Oleh:
##### 1. Cantika Latifatul Nur Ella (24031554023)
##### 2. Sofia Dwi Kinasih (24031554079)
##### 3. Ilmin Nur Lailiyah (24031554135)

------------------------------------------------------------------------------
### Tahapan:
1. CLIENT SIDE (client.py)
   ├─ Generate Ed25519 key pairs

   │  ├─ sofia079_priv.pem (private key - RAHASIA)
   │  ├─ sofia079.pem (public key - PUSH ke server)
   │  ├─ penerima_priv.pem (private key - RAHASIA)
   │  └─ penerima.pem (public key - PUSH ke server)
   │
   ├─ Sign message dengan private key
   │  └─ Output: signature (hex format)
   │
   ├─ Sign PDF hash
   │  ├─ Hash PDF dengan SHA256
   │  └─ Sign hash dengan private key
   │
   └─ Encrypt PDF dengan AES-256
      └─ Output: encrypted.pdf

3. UPLOAD KE SERVER (api.py)
   ├─ Step 1: Login
   │  ├─ username: sofia079
   │  ├─ password: password123
   │  └─ Response: access_token (JWT)
   │
   ├─ Step 2: Store Public Key
   │  ├─ Upload sofia079.pem ke /store endpoint
   │  └─ Server save di: punkhazard-keys/sofia079.pem
   │
   ├─ Step 3: Upload PDF
   │  ├─ POST ke /upload-pdf
   │  ├─ Data:
   │  │  ├─ username: sofia079
   │  │  ├─ signature: (dari client.py output)
   │  │  └─ file: soaluaskid.pdf
   │  └─ Server:
   │     ├─ Verify signature dengan public key
   │     ├─ Check integritas file
   │     └─ Save ke: uploads/soaluaskid.pdf
   │
   └─ Step 4: Relay Message (Optional)
      ├─ POST ke /relay
      ├─ Data:
      │  ├─ sender: sofia079
      │  ├─ receiver: penerima
      │  ├─ message: (pesan apapun)
      │  └─ signature: (sign message dengan private key)
      └─ Server:
         ├─ Verify signature
         ├─ Check kedua user terdaftar
         └─ Save log ke: data/relay_log.txt

4. OUTPUT & STORAGE
   └─ Server files:
      ├─ punkhazard-keys/
      │  ├─ sofia079.pem (public key)
      │  └─ penerima.pem (public key)
      ├─ uploads/
      │  ├─ soaluaskid.pdf (file yang diupload)
      │  └─ (file lain yang diupload)
      └─ data/
         ├─ relay_log.txt (log relay pesan)
         ├─ messages.txt (data pesan)
         └─ pubkeys.txt (data public keys)
------------------------------------------------------------------------------
## Punk Records-v1
Punk Records-v1 merupakan proyek Ujian Akhir Semester Mata Kuliah Keamanan dan Integritas Data yang mengimplementasikan layanan keamanan berbasis Application Programming Interface (API) menggunakan framework FastAPI. Proyek ini dirancang untuk menerapkan konsep kriptografi modern dalam menjaga kerahasiaan, keaslian, dan integritas data pada proses pertukaran pesan dan dokumen digital.

Sistem ini menggunakan beberapa mekanisme keamanan, yaitu:
1. Autentikasi pengguna berbasis JSON Web Token (JWT)
2. TSignature menggunakan algoritma Ed25519
3. Hashing data menggunakan SHA-256
4. Enkripsi dokumen menggunakan AES-256

Melalui implementasi ini, Punk Records-v1 mampu memastikan bahwa data yang dikirimkan berasal dari pengirim yang sah, tidak mengalami perubahan selama transmisi, serta hanya dapat diakses oleh pengguna yang terautentikasi.

------------------------------------------------------------------------------
## Penjelasan api.py
File api.py merupakan inti dari layanan API keamanan Punk Records-v1 yang dibangun menggunakan framework FastAPI. File ini berfungsi sebagai server utama yang menangani seluruh proses keamanan dan integritas data dalam sistem.

Fungsi utama yang ditangani oleh api.py meliputi:
1. Autentikasi pengguna menggunakan JWT (HS256)
2. Penyimpanan public key pengguna melalui endpoint /store
3. Verifikasi tanda tangan digital melalui endpoint /verify
4. Relay pesan aman antar pengguna melalui endpoint /relay
5. Upload dan verifikasi dokumen PDF melalui endpoint /upload-pdf
6. Endpoint pendukung seperti /health dan / (get_index)

Server menggunakan mekanisme secure session, di mana setiap endpoint sensitif hanya dapat diakses oleh pengguna yang telah terautentikasi dan memiliki token JWT yang valid.

------------------------------------------------------------------------------
## Penjelasan client.py
File client.py berfungsi sebagai sisi klien dalam sistem Punk Records-v1. File ini digunakan untuk:
1. Membuat pasangan kunci public–private menggunakan Ed25519
2. Membuat tanda tangan digital pada pesan atau file PDF
3. Melakukan enkripsi file PDF menggunakan AES-256 (Fernet) sebelum dikirim ke server
File ini mensimulasikan peran pengguna dalam sistem pertukaran data yang aman.

------------------------------------------------------------------------------
## Penjelasan main.py
File main.py merupakan entry point untuk menjalankan server FastAPI yang didefinisikan pada api.py. Server dijalankan menggunakan Uvicorn sebagai ASGI server sehingga API dapat diakses melalui browser maupun Swagger UI.

------------------------------------------------------------------------------
## Penjelasan pyproject.toml 
File pyproject.toml berisi konfigurasi proyek Python dan daftar dependensi yang dibutuhkan, yaitu FastAPI, cryptography, PyJWT, uvicorn.
File ini memastikan proyek dijalankan dengan lingkungan yang konsisten sesuai dengan spesifikasi tugas.

------------------------------------------------------------------------------
## Penjelasan uv.lock
File uv.lock merupakan file dependency lock yang dihasilkan secara otomatis oleh tool uv. File ini menyimpan versi pasti dari seluruh library yang digunakan sehingga mencegah perbedaan versi dependency antar environment. File ini tidak perlu diedit secara manual.

------------------------------------------------------------------------------
