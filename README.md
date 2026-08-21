# PalmChain - Traceability Dashboard with AI

PalmChain adalah proyek *Proof of Concept* (PoC) untuk melacak pergerakan aset kelapa sawit dari petani ke pengepul (First-Mile Traceability) guna mendukung kepatuhan regulasi EUDR (European Union Deforestation Regulation). Proyek ini menggunakan teknologi Blockchain (EVM) dan ditenagai oleh asisten AI cerdas melalui Langflow.

## 🌟 Arsitektur Proyek

Proyek ini terdiri dari 3 komponen utama yang saling berinteraksi:
1. **Smart Contracts (`palmchain-contracts/`)**: Kontrak pintar berbasis Solidity yang berjalan di jaringan lokal Hardhat. Berfungsi untuk menyimpan data aset kelapa sawit secara *immutable*.
2. **Web Dashboard (`palmchain-web/`)**: Antarmuka pengguna (UI) modern berbasis Vite, HTML, dan Vanilla JS yang ringan. Tersedia *widget* chat cerdas di pojok kanan bawah.
3. **AI Pipeline (`langflow-components/` & `PalmChain_Flow.json`)**: Alur kecerdasan buatan berbasis Langflow yang menghubungkan pertanyaan bahasa manusia (LLM Gemini) dengan bahasa pemrograman Blockchain (Web3/Python).

## 🚀 Panduan Instalasi dan Menjalankan Proyek

### Prasyarat
Pastikan komputer Anda sudah terinstal:
- **Node.js** (untuk Vite & Hardhat)
- **Python 3.10+** (untuk Langflow)
- **Git**

### Langkah 1: Menjalankan Blockchain Lokal (Hardhat)
1. Buka terminal baru.
2. Masuk ke folder Smart Contract:
   ```bash
   cd palmchain-contracts
   ```
3. Jalankan *node* Hardhat lokal:
   ```bash
   npx hardhat node
   ```
   *(Biarkan terminal ini tetap berjalan)*
4. Buka terminal baru lagi di folder yang sama, lalu tanam (deploy) Smart Contract-nya:
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```
   *Catat alamat Smart Contract (biasanya `0x5FbDB2315678afecb367f032d93F642f64180aa3`) karena akan diisikan ke Langflow nanti.*

### Langkah 2: Menyiapkan Langflow (Asisten AI)
1. Buka terminal baru dan jalankan Langflow (jika belum berjalan):
   ```bash
   langflow run
   ```
2. Buka browser ke `http://127.0.0.1:7860`.
3. Klik tombol **Import** dan pilih file `PalmChain_Flow.json` yang ada di repositori ini.
4. Di *canvas* Langflow, pastikan Anda:
   - Memasukkan API Key Google Gemini Anda di kotak **Language Model**.
   - (Opsional) Mengisi alamat Smart Contract di kotak **EVM Contract Caller** jika berbeda dengan *default*.
5. Klik ikon **Settings (Gerigi)** di pojok kiri bawah Langflow, pilih **API Keys**, buat kunci baru, dan *copy* kuncinya.
6. Tekan tombol petir (Play) di kanan bawah untuk meng-*compile* alur AI.

### Langkah 3: Menjalankan Web Dashboard
1. Buka terminal baru dan masuk ke folder web:
   ```bash
   cd palmchain-web
   ```
2. Buka file `main.js` di dalam editor teks, lalu cari baris 26:
   ```javascript
   const LANGFLOW_API_KEY = "sk-...";
   ```
   Ganti nilai `LANGFLOW_API_KEY` dengan kunci API Langflow yang Anda buat di Langkah 2.
3. Instal *dependency* (jika baru pertama kali):
   ```bash
   npm install
   ```
4. Jalankan server *frontend*:
   ```bash
   npm run dev
   ```
5. Buka `http://localhost:5173` di browser Anda.

## 🧪 Menguji AI di Web
1. Buka web *dashboard* PalmChain.
2. Klik ikon asisten robot di pojok kanan bawah.
3. Ketikkan pertanyaan seperti: 
   - *"Tolong cek di blockchain, berapa berat sawit dan apa grade untuk data dengan Asset ID TBS-20260821-001 ?"*
   - *"Tampilkan daftar seluruh Asset ID yang ada di sistem."*
4. AI akan secara otomatis memanggil fungsi di *blockchain*, menerjemahkannya, dan menampilkan jawabannya di chat!

---

*Dibangun dengan ❤️ menggunakan Hardhat, Vite, Langflow, dan Google Gemini.*
