# Pembuktian Perhitungan Manual Logika Fuzzy
**Kasus: Sistem Rekomendasi Kecepatan Kipas Laboratorium**  
**Kelompok 4 — Tugas UAS Logika Fuzzy**

Dokumen ini menyajikan pembuktian matematis langkah-demi-langkah (*step-by-step manual calculation*) untuk memverifikasi kebenaran dan akurasi implementasi algoritma pada program Python (`dasar.py`, `mamdani.py`, `sugeno.py`, dan `tsukamoto.py`).

---

## 1. Parameter dan Fungsi Keanggotaan

### A. Variabel Masukan (Input)
1. **Suhu Lingkungan ($T$)**: Domain $[20, 40]\ ^\circ\text{C}$
   $$\mu_{T\_rendah}(T) = \frac{40 - T}{20}$$
   $$\mu_{T\_tinggi}(T) = \frac{T - 20}{20}$$

2. **Kelembapan Udara ($H$)**: Domain $[40, 80]\ \%$
   $$\mu_{H\_rendah}(H) = \frac{80 - H}{40}$$
   $$\mu_{H\_tinggi}(H) = \frac{H - 40}{40}$$

### B. Variabel Keluaran (Output)
* **Kecepatan Kipas ($z$)**: Domain $[500, 1500]\ \text{RPM}$
  $$\mu_{Lambat}(z) = \frac{1500 - z}{1000}$$
  $$\mu_{Cepat}(z) = \frac{z - 500}{1000}$$

### C. Basis Aturan Fuzzy (Fuzzy Rule Base)
* **Rule 1 ($R_1$)**: IF Suhu Rendah AND Kelembapan Rendah THEN Kipas Lambat
* **Rule 2 ($R_2$)**: IF Suhu Rendah AND Kelembapan Tinggi THEN Kipas Lambat
* **Rule 3 ($R_3$)**: IF Suhu Tinggi AND Kelembapan Rendah THEN Kipas Cepat
* **Rule 4 ($R_4$)**: IF Suhu Tinggi AND Kelembapan Tinggi THEN Kipas Cepat

Operator fuzzy AND dievaluasi menggunakan fungsi **MIN**:
$$\alpha_i = \min(\mu_A, \mu_B)$$

---

## 2. Studi Kasus 1: Skenario Simetris (Uji C: $T = 30^\circ\text{C}, H = 60\%$)

### Langkah 1: Fuzzifikasi
* Suhu ($T = 30$):
  * $\mu_{T\_rendah}(30) = \frac{40 - 30}{20} = \frac{10}{20} = 0.50$
  * $\mu_{T\_tinggi}(30) = \frac{30 - 20}{20} = \frac{10}{20} = 0.50$
* Kelembapan ($H = 60$):
  * $\mu_{H\_rendah}(60) = \frac{80 - 60}{40} = \frac{20}{40} = 0.50$
  * $\mu_{H\_tinggi}(60) = \frac{60 - 40}{40} = \frac{20}{40} = 0.50$

### Langkah 2: Evaluasi Aturan ($\alpha$-predikat)
* $\alpha_1 = \min(0.50, 0.50) = 0.50 \to \text{Lambat}$
* $\alpha_2 = \min(0.50, 0.50) = 0.50 \to \text{Lambat}$
* $\alpha_3 = \min(0.50, 0.50) = 0.50 \to \text{Cepat}$
* $\alpha_4 = \min(0.50, 0.50) = 0.50 \to \text{Cepat}$
* Total $\sum \alpha_i = 0.50 + 0.50 + 0.50 + 0.50 = 2.00$

### Langkah 3: Defuzzifikasi Sugeno Orde-0
Konsekuen singleton: Lambat = $500\ \text{RPM}$, Cepat = $1500\ \text{RPM}$.
$$z^* = \frac{\sum (\alpha_i \cdot z_i)}{\sum \alpha_i} = \frac{(0.50 \times 500) + (0.50 \times 500) + (0.50 \times 1500) + (0.50 \times 1500)}{2.00}$$
$$z^* = \frac{250 + 250 + 750 + 750}{2.00} = \frac{2000}{2.00} = \mathbf{1000.00\ RPM}$$

### Langkah 4: Defuzzifikasi Tsukamoto
Konsekuen fungsi monoton:
* $R_1 \text{ (Lambat)}: z_1 = 1500 - 1000(0.50) = 1000\ \text{RPM}$
* $R_2 \text{ (Lambat)}: z_2 = 1500 - 1000(0.50) = 1000\ \text{RPM}$
* $R_3 \text{ (Cepat)}: z_3 = 500 + 1000(0.50) = 1000\ \text{RPM}$
* $R_4 \text{ (Cepat)}: z_4 = 500 + 1000(0.50) = 1000\ \text{RPM}$
$$z^* = \frac{\sum (\alpha_i \cdot z_i)}{\sum \alpha_i} = \frac{(0.5 \times 1000) + (0.5 \times 1000) + (0.5 \times 1000) + (0.5 \times 1000)}{2.00} = \mathbf{1000.00\ RPM}$$

### Langkah 5: Defuzzifikasi Mamdani
Karena derajat keanggotaan dan pemotongan bernilai simetris $0.5$ di kedua sisi domain $[500, 1500]$, maka titik berat geometris kurva gabungan (Centroid) jatuh tepat di titik tengah:
$$z^* = \frac{500 + 1500}{2} = \mathbf{1000.00\ RPM}$$

**Verifikasi Program vs Manual Uji C:**
* Mamdani: $1000.00\ \text{RPM}$ (Sesuai 100%)
* Sugeno: $1000.00\ \text{RPM}$ (Sesuai 100%)
* Tsukamoto: $1000.00\ \text{RPM}$ (Sesuai 100%)

---

## 3. Studi Kasus 2: Skenario Asimetris Realistis (Uji D: $T = 33^\circ\text{C}, H = 65\%$)

### Langkah 1: Fuzzifikasi
* Suhu ($T = 33$):
  * $\mu_{T\_rendah}(33) = \frac{40 - 33}{20} = \frac{7}{20} = \mathbf{0.35}$
  * $\mu_{T\_tinggi}(33) = \frac{33 - 20}{20} = \frac{13}{20} = \mathbf{0.65}$
* Kelembapan ($H = 65$):
  * $\mu_{H\_rendah}(65) = \frac{80 - 65}{40} = \frac{15}{40} = \mathbf{0.375}$
  * $\mu_{H\_tinggi}(65) = \frac{65 - 40}{40} = \frac{25}{40} = \mathbf{0.625}$

### Langkah 2: Evaluasi Aturan ($\alpha$-predikat)
* $\alpha_1 = \min(0.35, 0.375) = \mathbf{0.35} \to \text{Lambat}$
* $\alpha_2 = \min(0.35, 0.625) = \mathbf{0.35} \to \text{Lambat}$
* $\alpha_3 = \min(0.65, 0.375) = \mathbf{0.375} \to \text{Cepat}$
* $\alpha_4 = \min(0.65, 0.625) = \mathbf{0.625} \to \text{Cepat}$
* Total bobot $\sum \alpha_i = 0.35 + 0.35 + 0.375 + 0.625 = \mathbf{1.70}$

### Langkah 3: Defuzzifikasi Sugeno Orde-0
Konsekuen singleton: $z_1 = 500, z_2 = 500, z_3 = 1500, z_4 = 1500$.
$$\sum (\alpha_i \cdot z_i) = (0.35 \times 500) + (0.35 \times 500) + (0.375 \times 1500) + (0.625 \times 1500)$$
$$\sum (\alpha_i \cdot z_i) = 175.0 + 175.0 + 562.5 + 937.5 = \mathbf{1850.0}$$
$$z^* = \frac{1850.0}{1.70} = \mathbf{1088.235\dots \approx 1088.24\ RPM}$$

### Langkah 4: Defuzzifikasi Tsukamoto
Menghitung nilai $z_i$ tegas dari tiap aturan monoton:
* $R_1 \text{ (Lambat)}: z_1 = 1500 - (1000 \times 0.35) = 1500 - 350 = \mathbf{1150\ RPM}$
* $R_2 \text{ (Lambat)}: z_2 = 1500 - (1000 \times 0.35) = 1500 - 350 = \mathbf{1150\ RPM}$
* $R_3 \text{ (Cepat)}: z_3 = 500 + (1000 \times 0.375) = 500 + 375 = \mathbf{875\ RPM}$
* $R_4 \text{ (Cepat)}: z_4 = 500 + (1000 \times 0.625) = 500 + 625 = \mathbf{1125\ RPM}$

Menghitung rata-rata terbobot:
$$\sum (\alpha_i \cdot z_i) = (0.35 \times 1150) + (0.35 \times 1150) + (0.375 \times 875) + (0.625 \times 1125)$$
$$\sum (\alpha_i \cdot z_i) = 402.50 + 402.50 + 328.125 + 703.125 = \mathbf{1836.25}$$
$$z^* = \frac{1836.25}{1.70} = \mathbf{1080.147\dots \approx 1080.15\ RPM}$$

### Langkah 5: Defuzzifikasi Mamdani (Centroid)
* Pemotongan kurva (*clipping*):
  * Himpunan Lambat dipotong pada $\alpha_{max\_lambat} = \max(\alpha_1, \alpha_2) = \max(0.35, 0.35) = 0.35$
  * Himpunan Cepat dipotong pada $\alpha_{max\_cepat} = \max(\alpha_3, \alpha_4) = \max(0.375, 0.625) = 0.625$
* Agregasi fungsi keanggotaan gabungan:
  $$\mu_{gabungan}(z) = \max(\min(0.35, \frac{1500-z}{1000}), \min(0.625, \frac{z-500}{1000}))$$
* Evaluasi numerik diskret ($\Delta z = 1$):
  $$z^* = \frac{\sum_{z=500}^{1500} z \cdot \mu(z)}{\sum_{z=500}^{1500} \mu(z)} = \mathbf{1068.28\ RPM}$$

**Verifikasi Program vs Manual Uji D:**
* Mamdani: $1068.28\ \text{RPM}$ (Sesuai 100%)
* Sugeno: $1088.24\ \text{RPM}$ (Sesuai 100%)
* Tsukamoto: $1080.15\ \text{RPM}$ (Sesuai 100%)

---

## 4. Kesimpulan Pembuktian
Seluruh hasil pengujian manual terbukti **100% identik dan konsisten** dengan hasil komputasi pada skrip Python, membuktikan bahwa formulasi matematis di balik kode program telah valid tanpa cacat logika.
