# 🍎 Deteksi Kualitas Buah Menggunakan Pengolahan Citra Digital

> Project UAS Mata Kuliah Pengolahan Citra Digital  
> Program Studi Teknik Informatika  
> Semester Gasal TA 2025/2026

---

## 👤 Identitas

| Keterangan | Detail |
|---|---|
| Nama | Fitri Ramadhani |
| NIM | 312410085 |
| Kelas | I241A |
| Dosen | Dr. Muhamad Fatchan., S.Kom., M.Kom |
| Mata Kuliah | Pengolahan Citra Digital |

---

## 📌 Deskripsi Project

Aplikasi desktop berbasis **Python + Tkinter** yang mampu mendeteksi kualitas buah (Bagus atau Busuk) menggunakan teknik-teknik **Pengolahan Citra Digital**. Aplikasi memproses gambar buah secara otomatis melalui beberapa tahapan dan menampilkan hasilnya secara visual dalam satu antarmuka yang modern dan profesional.

---

## ✅ Fitur & Teknik yang Diimplementasikan

| No | Teknik | Status |
|---|---|---|
| 1 | Konversi RGB ke Grayscale | ✅ |
| 2 | Konversi RGB ke Biner (Thresholding Otsu) | ✅ |
| 3 | Histogram Equalization | ✅ |
| 4 | Gaussian Filter (Noise Reduction) | ✅ |
| 5 | Edge Detection — Canny | ✅ |
| 6 | Segmentasi Citra (Adaptive Thresholding) | ✅ |
| 7 | Analisis Warna HSV | ✅ |
| 8 | GUI Berbasis Tkinter | ✅ |
| 9 | Klasifikasi Kualitas Buah | ✅ |

---

## 🛠️ Teknologi yang Digunakan

- **Python 3.x**
- **OpenCV**  pemrosesan citra (grayscale, blur, edge, segmentasi)
- **NumPy**  operasi matriks dan array
- **Pillow (PIL)**  konversi gambar untuk ditampilkan di Tkinter
- **Tkinter**  GUI desktop

---

## 📦 Instalasi

### 1. Pastikan Python 3 sudah terinstal
```bash
python --version
```

### 2. Install library yang dibutuhkan
```bash
pip install opencv-python numpy pillow
```

> Tkinter sudah termasuk bawaan Python, tidak perlu install terpisah.

---

## 🚀 Cara Menjalankan

```bash
python deteksi_kualitas_buah.py
```

---

## 🗂️ Struktur Folder

```
uas/
│
├── uas_pc_deteksi_buah.py    # File utama aplikasi
├── README.md                   # Dokumentasi ini
│
└── dataset_buah/               # Folder dataset (siapkan sendiri)
    ├── bagus/                  # 10 gambar buah bagus
    │   ├── buah_bagus_01.jpg
    │   ├── buah_bagus_02.jpg
    │   └── ...
    └── busuk/                  # 10 gambar buah busuk
        ├── buah_busuk_01.jpg
        ├── buah_busuk_02.jpg
        └── ...
```

---

## 🖥️ Cara Menggunakan Aplikasi

1. **Jalankan** program dengan perintah di atas
2. Klik tombol **📂 Upload Gambar** → pilih gambar buah dari folder
3. Klik tombol **⚙️ Proses** → aplikasi memproses gambar secara otomatis
4. Lihat **7 visualisasi** hasil proses di panel kanan
5. Lihat **hasil analisis** di panel kiri (status, persentase busuk, HSV, waktu proses)
6. Klik **🔄 Reset** untuk memulai dengan gambar baru
7. Klik **✖ Keluar** untuk menutup aplikasi

---

## 📊 Alur Pipeline Pengolahan Citra

```
Gambar Input (JPG/PNG)
        │
        ▼
┌─────────────────┐
│  1. Grayscale   │  Konversi warna BGR → Abu-abu
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  2. Hist. Equalize   │  Peningkatan kontras citra
└────────┬─────────────┘
         │
         ▼
┌──────────────────┐
│  3. Gaussian     │  Filter noise (kernel 5×5)
│     Blur         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  4. Thresholding │  Konversi ke citra biner (Otsu)
│     (Biner)      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  5. Canny Edge   │  Deteksi tepi objek buah
│     Detection    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  6. Segmentasi   │  Isolasi area gelap/busuk
│     HSV Mask     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  7. Analisis HSV │  Hitung rata-rata H, S, V
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  8. Klasifikasi  │  Buah Bagus / Buah Busuk
└──────────────────┘
```

---

## 🔍 Aturan Klasifikasi

| Kondisi | Hasil |
|---|---|
| Area gelap ≤ 25% dan V_mean ≥ 70 | 🟢 **Buah Bagus** |
| Area gelap > 25% | 🔴 **Buah Busuk** |
| V_mean < 70 (gambar sangat gelap) | 🔴 **Buah Busuk** |
| S_mean < 20 dan V_mean < 90 (pucat + gelap) | 🔴 **Buah Busuk** |

---

## 📈 Contoh Output Analisis

```
Status          :  Buah Bagus 🟢
Persentase Busuk:  8.3%
Kesehatan       :  91.7%
H (Hue)         :  18.4
S (Saturation)  :  140.2
V (Value)       :  178.6
Waktu Proses    :  0.034s
```

---

## 📁 Dataset

- Total gambar: **24 gambar**
  - 12 gambar buah **bagus** (segar, tidak ada bercak)
  - 12 gambar buah **busuk** (ada bercak hitam/coklat, layu)
- Format yang didukung: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`
- Tema dataset: buah-buahan (apel, jeruk, pisang, mangga, dll.)

---

## 📝 Struktur Kode

```
deteksi_kualitas_buah.py
│
├── SECTION 1  : Import Library
├── SECTION 2  : Konfigurasi Warna & Tema GUI
├── SECTION 3  : Class FruitQualityApp (Main GUI)
├── SECTION 4  : Builder Layout GUI
├── SECTION 5  : Fungsi Upload Gambar
├── SECTION 6  : Fungsi Preprocessing (Grayscale + Hist EQ)
├── SECTION 7  : Fungsi Filtering (Gaussian Blur)
├── SECTION 8  : Fungsi Edge Detection (Canny)
├── SECTION 9  : Fungsi Segmentasi (Thresholding + Mask)
├── SECTION 10 : Fungsi Analisis HSV
├── SECTION 11 : Fungsi Klasifikasi Kualitas Buah
├── SECTION 12 : Fungsi Proses Utama (Pipeline)
├── SECTION 13 : Fungsi Tampil Hasil Proses
├── SECTION 14 : Fungsi Update Analisis GUI
├── SECTION 15 : Fungsi Reset
├── SECTION 16 : Fungsi Utilitas
└── SECTION 17 : Entry Point (main)
```

---

## ⚠️ Catatan

- Pastikan gambar buah memiliki latar belakang yang relatif kontras
- Untuk hasil terbaik, gunakan gambar dengan pencahayaan yang cukup
- Semua proses berjalan dalam **satu file Python** tanpa dependensi eksternal selain library yang disebutkan

---

## 📜 Lisensi

Project ini dibuat untuk keperluan akademik UAS Pengolahan Citra Digital  
Universitas Pelita Bangsa © 2026
