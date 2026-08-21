# 🌴 PalmChain: Project Master Document
**Lomba Riset Sawit Tingkat Mahasiswa - BPDPKS 2026**

---

## 🎯 1. Konteks & Goal Proyek
* **Konteks Masalah:** Rantai pasok kelapa sawit di tingkat hulu (*first-mile*, dari petani swadaya ke pengepul) masih sangat tersentralisasi dan dicatat secara manual. Hal ini memunculkan *trust issue*, rentan manipulasi data (fraud/tengkulak), dan menyebabkan *blind spot* pada ketertelusuran asal lahan. Ditambah lagi, adanya regulasi global seperti **EUDR** mensyaratkan bukti geolokasi yang ketat.
* **Goal Utama:** Membangun purwarupa (MVP) sistem ketertelusuran (*traceability*) *end-to-end* yang murah dan mudah digunakan untuk industri sawit. Sistem ini memastikan data fisik di lapangan ditangkap otomatis, dikunci secara permanen agar tidak bisa diubah (*tamper-proof*), dan dapat diakses dengan mudah oleh petani/auditor menggunakan asisten AI berbasis *chat*.

## 🏷️ 2. Usulan Judul Riset
> *"PalmChain: Integrasi IoT, EVM Blockchain (Hardhat), dan AI Chatbot (RAG) untuk Ketertelusuran First-Mile Kelapa Sawit Guna Merespons Regulasi EUDR"*

## 📖 3. Latar Belakang & Studi Kasus (Source)
Sistem dibangun berdasarkan keresahan pada kasus-kasus nyata di lapangan:
* **Kasus Manipulasi Timbangan/Kualitas:** Pengepul nakal sering mengakali catatan berat timbangan atau memalsukan *grade* Tandan Buah Segar (TBS) yang merugikan petani swadaya.
* **Kasus Pencucian Buah (Fruit Laundering):** Buah sawit yang ditanam di kawasan hutan terlarang dicampur dengan buah legal di tingkat pengepul, sehingga pabrik tidak bisa melacak asal-usul aslinya.

## ⚙️ 4. Step Penting Produk (Core Pipeline)
Alur data berjalan secara linear dengan integrasi 3 teknologi utama:

1. **📱 IoT (Data Acquisition):** 
   * Mengambil data secara otomatis di kebun/pengepul untuk mematikan celah *human error* atau *input* manual.
2. **⛓️ BLOCKCHAIN (Data Storage & Integrity):** 
   * Menerima data dari IoT dan menyimpannya ke dalam *ledger* terdistribusi menggunakan *Smart Contract*. Data yang masuk bersifat permanen (*immutable*).
3. **🤖 AI (Data Extraction & Interaction):** 
   * Asisten virtual (*Chatbot*) bagi pihak internal/eksternal untuk menanyakan data (contoh: *"Berapa total pasokan sawit dari Koperasi A minggu ini?"*). AI akan mengekstraksi data dari *Blockchain* dan menjawab dengan bahasa manusia.

## 🛠️ 5. Tech Stack & Tools (Sesuai Catatan Dosen)

### A. Komponen IoT (Fokus: Murah & Feasible)
* **Microcontroller:** ESP32 (Sangat murah, sudah ada WiFi/Bluetooth).
* **Modul GPS:** Neo-6M GPS (Untuk mendapatkan data geolokasi kebun yang valid sesuai syarat EUDR).
* **Digital Load Cell (Timbangan Digital):** Sensor berat 100kg-500kg untuk mendeteksi berat sawit secara otomatis tanpa diketik.
* **Kamera (Opsional/Sesuai Arahan):** ESP32-CAM. Sesuai catatan dosen ("cuman butuh kamera aja"), kamera bisa dipakai untuk *Computer Vision* sederhana (klasifikasi kematangan buah berdasar warna) atau sekadar mengambil bukti foto fisik saat penimbangan.

### B. Komponen Blockchain
* **EVM Blockchain (Hardhat):** Lingkungan pengembangan lokal yang sangat ringan dan cepat untuk mensimulasikan jaringan Ethereum.
* **Smart Contract (Solidity):** Menulis logika bisnis dan penyimpanan data aset sawit yang terdesentralisasi dan tidak bisa diubah (immutable).
* **Ethers.js / Web3:** Pustaka untuk menghubungkan frontend/AI dengan smart contract.

### C. Komponen AI & Chatbot
* **LLM (Large Language Model):** DeepSeek API (Model murah, pintar *coding* & logika, *open-source friendly*).
* **RAG & Tool Calling:** Arsitektur AI agar Chatbot merujuk pada "data internal" sebelum menjawab. AI akan berinteraksi langsung dengan *Smart Contract* EVM untuk mengambil data sawit.
* **Tavily (Search API):** Agen *browsing* AI. Diintegrasikan ke Chatbot agar AI bisa mencari informasi eksternal *real-time* (Contoh user nanya: *"Berapa harga referensi CPO global hari ini?"* -> AI menggunakan Tavily untuk *search* web, lalu menjawab).

---
*Document generated for Antigravity Workspace.*