# Sistem Logika Fuzzy Kipas Laboratorium

Program ini menghitung rekomendasi kecepatan kipas (*rotations per minute* / RPM) berdasarkan suhu ($20 - 40\ ^\circ\text{C}$) dan kelembapan udara ($40 - 80\ \%$). Hasil inferensi dibandingkan secara komprehensif menggunakan tiga metode logika fuzzy: **Mamdani**, **Sugeno (Orde-0)**, dan **Tsukamoto**.

---

## 📁 Struktur Proyek

* `dasar.py`: Modul fungsi keanggotaan (fuzzifikasi), evaluasi aturan AND ($\alpha$-predikat), dan validasi rentang masukan.
* `mamdani.py`: Implementasi inferensi Mamdani (metode defuzzifikasi Centroid diskret).
* `sugeno.py`: Implementasi inferensi Sugeno orde-0 (konsekuen crisp + rata-rata terbobot).
* `tsukamoto.py`: Implementasi inferensi Tsukamoto (konsekuen fungsi monoton linear + rata-rata terbobot).
* `tampilan.py`: Modul visualisasi diagram batang hasil pengujian skenario A–G.
* `main.py`: Antarmuka CLI utama untuk eksekusi skenario batch dan interaktif manual.
* `analisis.py`: Modul eksperimen lanjutan (benchmark interval centroid dan analisis respon suhu).
* `test_fuzzy.py`: Pengujian unit (*unit testing*) mandiri untuk seluruh modul program.
* `perhitungan_manual.md`: Dokumentasi pembuktian matematis hitungan tangan langkah-demi-langkah.
* `revisi.md`: Lembar tindak lanjut evaluasi dosen dan jawaban resmi pertanyaan evaluasi.
* `hasil/`: Direktori penyimpanan otomatis grafik visualisasi (PNG).

---

## 🚀 Cara Menjalankan

### 1. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Uji Batch dan Generate Grafik Perbandingan
```bash
python main.py
```
Perintah ini akan menjalankan Uji A–G (valid) dan H–I (ditolak), mencetak tabel ringkasan ke konsol terminal, dan menyimpan grafik ke `hasil/perbandingan_uji.png`.

### 3. Menjalankan Mode Input Interaktif Manual
```bash
python main.py --manual
```

### 4. Menjalankan Analisis Eksperimen, Visualisasi Himpunan Fuzzy, & Benchmark
```bash
python analisis.py
```
Perintah ini akan menghasilkan:
* `hasil/fungsi_keanggotaan.png` (Kurva keanggotaan Suhu, Kelembapan, dan Kecepatan Kipas)
* `hasil/benchmark_centroid.png` (Perbandingan waktu komputasi & akurasi interval 1, 5, 10 RPM)
* `hasil/suhu_kelembapan65.png` (Analisis respon monotonisitas ketiga metode terhadap perubahan suhu)

### 5. Menjalankan Unit Testing Otomatis
```bash
python -m unittest test_fuzzy.py
```

---

## 👥 Tugas UAS Logika Fuzzy — Kelompok 4

1. **Rizky Wahyudi** — 4233250024
2. **John Bush** — 4233250016
3. **Khildan Rifal Aziz** — 4233550035
4. **Neysa Talitha Jehian** — 4233550031
5. **Febrina Suleho** — 4232250002
6. **Iwan Agi Berutu** — 4233550039
7. **Windy Aulia** — 4231250021
