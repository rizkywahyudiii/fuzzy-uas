# Catatan Revisi, Masukan Evaluator, dan Tindak Lanjut Progres
**Topik:** Implementasi dan Perbandingan Mamdani, Sugeno, dan Tsukamoto untuk Kipas Laboratorium  
**Kelompok 4 — Tugas UAS Logika Fuzzy**  
**Status Capaian Progres:** **95% (Hampir Selesai / Siap Laporan Final)**

---

## 1. Kelebihan Proyek yang Diakui
- [x] Struktur program modular: `dasar.py`, `mamdani.py`, `sugeno.py`, `tsukamoto.py`, `tampilan.py`, dan `main.py`.
- [x] Skenario pengujian komprehensif (Uji A–G valid serta mekanisme penolakan input invalid H–I).
- [x] Validasi input ketat (rentang batas dan tipe data numerik).

---

## 2. Tindak Lanjut Temuan & Masukan Dosen/Reviewer

### a. Penyelesaian Analisis Eksperimen
* **Status:** **SELESAI (100%)**
* **Implementasi:**
  * Grafik perbandingan metode untuk seluruh skenario uji A–G telah dibuat otomatis melalui modul `tampilan.py` (`hasil/perbandingan_uji.png`).
  * Visualisasi kurva fungsi keanggotaan input (Suhu & Kelembapan) dan output (RPM) telah diimplementasikan (`hasil/fungsi_keanggotaan.png`).
  * Analisis respon suhu terhadap output RPM pada kelembapan 65% telah digenerate (`hasil/suhu_kelembapan65.png`).
  * Perhitungan manual lengkap langkah-demi-langkah terdokumentasi di [perhitungan_manual.md](perhitungan_manual.md).

### b. Benchmark Centroid (Interval 1, 5, dan 10 RPM)
* **Status:** **SELESAI (100%)**
* **Implementasi:**
  * Dijalankan pada kondisi Uji D ($T = 33^\circ\text{C}, H = 65\%$) dengan pengulangan 200x untuk kestabilan pengukuran waktu.
  * Hasil benchmark:
    * **Interval 1 RPM** (1001 titik): Output = 1068.2826 RPM, Waktu = ~0.570 ms (Acuan baseline).
    * **Interval 5 RPM** (201 titik): Output = 1068.5723 RPM, Selisih = +0.2897 RPM (0.027%), Waktu = ~0.116 ms (**~5x lebih cepat**).
    * **Interval 10 RPM** (101 titik): Output = 1068.9340 RPM, Selisih = +0.6514 RPM (0.061%), Waktu = ~0.058 ms (**~9.8x lebih cepat**).
  * Grafik komparasi performa tersimpan di `hasil/benchmark_centroid.png`.

### c. Validasi Program Modular (Unit Testing Independen)
* **Status:** **SELESAI (100%)**
* **Implementasi:**
  * Dibuat file pengujian otomatis `test_fuzzy.py` dengan 19 test case menggunakan framework `unittest`.
  * Memvalidasi fungsi validasi input, fuzzifikasi, aktivasi aturan, dan ketiga modul defuzzifikasi secara mandiri dan terisolasi.
  * Menjamin konsistensi deterministik keluaran program (100% test lulus).

### d. Dasar Rekomendasi Pemilihan Metode
* **Status:** **SELESAI (100%)**
* **Kriteria Pemilihan yang Ditetapkan:**
  1. **Karakteristik Respons & Monotonisitas**: Mamdani dan Sugeno selalu monotonik terhadap kenaikan suhu, sedangkan Tsukamoto mengalami fenomena non-monotonik lokal pada rentang suhu tertentu ($20-24^\circ\text{C}$ dan $36-40^\circ\text{C}$).
  2. **Kelancaran Kendali (*Smoothness*)**: Mamdani menghasilkan kurva perubahan kecepatan paling halus dan realistis bagi motor kipas.
  3. **Beban Komputasi**: Sugeno dan Tsukamoto memiliki komputasi instan ($O(1)$), sementara Mamdani membutuhkan diskretisasi integral centroid ($O(N)$). Namun, dengan interval 10 RPM, waktu Mamdani terpangkas menjadi hanya 0.058 ms.
* **Rekomendasi Final:**
  * **Metode Utama**: **Mamdani (dengan interval diskretisasi 5 atau 10 RPM)** direkomendasikan sebagai pilihan utama sistem kendali kipas laboratorium guna menjamin pergerakan motor yang stabil, adaptif, dan halus.
  * **Alternatif Embedded Murah**: **Sugeno Orde-0** direkomendasikan bila sistem ditanamkan pada mikrokontroler 8-bit berdaya rendah dengan memori sangat terbatas.

---

## 3. Jawaban Resmi Pertanyaan untuk Kelompok 4

### 1. Mengapa program perlu dipisahkan menjadi beberapa modul?
> **Jawaban:** Pemisahan program (`dasar.py`, `mamdani.py`, `sugeno.py`, `tsukamoto.py`, `tampilan.py`, `main.py`) menerapkan prinsip rekayasa perangkat lunak *Separation of Concerns* (Pemisahan Tanggung Jawab) dan *Single Responsibility Principle*. Keuntungannya:
> 1. Logika fuzzifikasi dan rule-base terisolasi dari algoritma defuzzifikasi.
> 2. Penambahan metode fuzzy baru dapat dilakukan tanpa mengubah modul inti lainnya.
> 3. Memungkinkan pengujian unit secara mandiri (*isolated unit testing*).

### 2. Apa keuntungan menggunakan centroid interval 10 RPM dibandingkan 1 RPM?
> **Jawaban:** Keuntungan utamanya adalah **peningkatan efisiensi komputasi hingga ~9.8 kali lipat** (dari ~0.570 ms turun menjadi ~0.058 ms) dengan **pengorbanan akurasi yang sangat minimal** (selisih hanya +0.6514 RPM atau deviasi relatif < 0.06%). Dalam aplikasi fisik kipas laboratorium, perbedaan 0.65 RPM sama sekali tidak memengaruhi performa aerodinamika kipas dan berada jauh di bawah toleransi mekanik aktuator.

### 3. Bagaimana menguji masing-masing modul secara independen?
> **Jawaban:** Pengujian independen dilakukan melalui modul `test_fuzzy.py`. Setiap modul diuji tanpa ketergantungan modul lain:
> 1. `dasar.py` diuji dengan melewatkan input batas dan memverifikasi keluaran derajat keanggotaan $\mu$ serta $\alpha$-predikat.
> 2. Modul defuzzifikasi (`mamdani.py`, `sugeno.py`, `tsukamoto.py`) diuji langsung dengan array bobot $\alpha$ sintetik (misal: $\alpha$ seimbang $[0.5, 0.5, 0.5, 0.5]$ untuk memverifikasi nilai tengah 1000 RPM, dan $\alpha$ ekstrem untuk memverifikasi batas 500 RPM / 1500 RPM).

### 4. Bagaimana membuktikan bahwa hasil program benar?
> **Jawaban:** Kebenaran program dibuktikan secara ilmiah melalui dua metode verifikasi:
> 1. **Perhitungan Manual (*Hand Calculation Cross-Check*)**: Melakukan perhitungan matematis analitis dari awal hingga akhir pada skenario representatif (Uji C dan Uji D di `perhitungan_manual.md`). Hasil hitungan manual terbukti identik hingga 2 digit desimal dengan keluaran program.
> 2. **Pemeriksaan Sifat Batas & Simetri**: Pada kondisi input seimbang ($T=30^\circ\text{C}, H=60\%$), ketiga metode secara teoritis dan praktis menghasilkan tepat $1000.00\ \text{RPM}$. Pada input minimum ($T=20^\circ\text{C}, H=40\%$) menghasilkan nilai batas bawah, dan pada input maksimum ($T=40^\circ\text{C}, H=80\%$) menghasilkan nilai batas atas.

---

## 4. Rincian Sisa 5% Menuju 100% (Tahap Akhir)
- [x] Integrasi kode, modul visualisasi, analisis eksperimen, benchmark, unit test, dan perhitungan manual (Selesai).
- [ ] Penggabungan materi ke dalam dokumen PDF laporan resmi UAS dan slide deck presentasi final kelompok.
