# Rencana Integrasi IoT (Tahap 1: Pemanasan ESP32-CAM)

Wah, mantap bos! Papan tanpa solder itu namanya **Breadboard** (papan roti). Karena Anda punya **ESP32-CAM-MB** (modul *programmer* bawaan yang ada colokan Micro-USB nya), kerjaan kita bakal jauh lebih gampang! Anda bahkan **tidak perlu** pakai kabel *jumper* atau *breadboard* untuk sekadar memprogram kamera ini.

Tujuan utama dari integrasi IoT untuk PalmChain nantinya mungkin adalah **mengambil foto buah sawit (TBS)** atau membaca *QR Code* di perkebunan, lalu mengirimkannya ke *database*. Tapi sesuai permintaan, kita akan mulai dari **yang paling ringan dulu**.

## Open Questions

> [!IMPORTANT]
> 1. Apakah di laptop/komputer Anda saat ini sudah terinstal **Arduino IDE**? (Atau Anda menggunakan VSCode + PlatformIO?)
> 2. Kabel yang Anda punya apakah kabel data Micro-USB biasa (seperti charger HP lama)? Pastikan kabel tersebut bisa mentransfer data, bukan cuma sekadar ngecas (kabel *power-only*).

## Proposed Changes (Rencana Aksi)

### Tahap 1.1: Persiapan Perangkat Keras (Hardware)
1. Colokkan modul ESP32-CAM langsung ke atas ESP32-CAM-MB (modul *programmer*). Pastikan arah pin-nya pas dan tidak terbalik (lensa kamera menghadap ke atas, sejajar dengan colokan USB).
2. Hubungkan modul ESP32-CAM-MB ke komputer menggunakan kabel Micro-USB.
3. *Breadboard* dan kabel *jumper* kita simpan dulu untuk nanti kalau kita mau tambah sensor berat (Load Cell) atau sensor lainnya!

### Tahap 1.2: Persiapan *Software* (Arduino IDE)
Jika Anda menggunakan Arduino IDE, saya akan memandu Anda untuk:
1. Memasukkan *URL Board Manager* ESP32 ke dalam pengaturan Arduino IDE.
2. Menginstal *library* khusus untuk papan ESP32.
3. Mengubah pengaturan tipe *board* menjadi `AI Thinker ESP32-CAM`.

### Tahap 1.3: Kode Pemanasan (Hello World IoT)
Sebelum langsung memfoto sawit, kode pertama yang akan kita masukkan (*flash*) adalah **Camera Web Server** bawaan.
- Saya akan memberikan kode *default* yang sudah dimodifikasi dengan WiFi rumah Anda.
- Setelah di-*upload*, ESP32-CAM akan terhubung ke WiFi Anda dan memunculkan alamat IP (contoh: `192.168.1.10`).
- Saat Anda membuka IP tersebut di browser, Anda langsung bisa **melihat hasil tangkapan video kamera secara langsung (*live streaming*)** dari laptop/HP Anda!

## Verification Plan

### Manual Verification
- Jika berhasil, saat Anda membuka alamat IP ESP32-CAM di browser web, akan muncul panel kontrol kamera dengan tombol "Start Stream", dan kamera akan menampilkan video ruangan Anda secara *real-time*.
- Setelah tahap ini sukses, baru kita merancang logika IoT-nya untuk mengambil satu foto dan mengirimkannya ke API *backend* PalmChain kita.
