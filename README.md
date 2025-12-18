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
## Penjelasan
