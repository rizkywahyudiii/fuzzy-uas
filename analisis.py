import os
import sys
import time
import matplotlib.pyplot as plt
from dasar import fuzzifikasi, aktivasi_aturan
from mamdani import mamdani
from sugeno import sugeno
from tsukamoto import tsukamoto

FOLDER = "hasil"
ULANG = 200  # pengulangan untuk rata-rata waktu


def visualisasi_fungsi_keanggotaan():
    """Memvisualisasikan fungsi keanggotaan input (Suhu & Kelembapan) dan output (RPM)."""
    os.makedirs(FOLDER, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    # 1. Himpunan Fuzzy Suhu (20 - 40 °C)
    t_vals = [t for t in range(20, 41)]
    t_rendah = [(40 - t) / 20 for t in t_vals]
    t_tinggi = [(t - 20) / 20 for t in t_vals]
    axes[0].plot(t_vals, t_rendah, label="Rendah", color="#1F3A4D", linewidth=2)
    axes[0].plot(t_vals, t_tinggi, label="Tinggi", color="#C8553D", linewidth=2)
    axes[0].set_title("Variabel Input: Suhu (°C)", fontweight="bold")
    axes[0].set_xlabel("Suhu (°C)")
    axes[0].set_ylabel("Derajat Keanggotaan (μ)")
    axes[0].set_ylim(-0.05, 1.05)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(loc="center")

    # 2. Himpunan Fuzzy Kelembapan (40 - 80 %)
    h_vals = [h for h in range(40, 81)]
    h_rendah = [(80 - h) / 40 for h in h_vals]
    h_tinggi = [(h - 40) / 40 for h in h_vals]
    axes[1].plot(h_vals, h_rendah, label="Rendah", color="#1F3A4D", linewidth=2)
    axes[1].plot(h_vals, h_tinggi, label="Tinggi", color="#C8553D", linewidth=2)
    axes[1].set_title("Variabel Input: Kelembapan (%)", fontweight="bold")
    axes[1].set_xlabel("Kelembapan (%)")
    axes[1].set_ylabel("Derajat Keanggotaan (μ)")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend(loc="center")

    # 3. Himpunan Fuzzy Output Kipas (500 - 1500 RPM)
    z_vals = [z for z in range(500, 1501, 10)]
    z_lambat = [(1500 - z) / 1000 for z in z_vals]
    z_cepat = [(z - 500) / 1000 for z in z_vals]
    axes[2].plot(z_vals, z_lambat, label="Lambat", color="#1F3A4D", linewidth=2)
    axes[2].plot(z_vals, z_cepat, label="Cepat", color="#C8553D", linewidth=2)
    axes[2].set_title("Variabel Output: Kecepatan (RPM)", fontweight="bold")
    axes[2].set_xlabel("Kecepatan Kipas (RPM)")
    axes[2].set_ylabel("Derajat Keanggotaan (μ)")
    axes[2].set_ylim(-0.05, 1.05)
    axes[2].grid(True, linestyle="--", alpha=0.5)
    axes[2].legend(loc="center")

    fig.suptitle("Fungsi Keanggotaan Logika Fuzzy Kipas Laboratorium", fontsize=13, fontweight="bold")
    fig.tight_layout()
    out_file = os.path.join(FOLDER, "fungsi_keanggotaan.png")
    fig.savefig(out_file, dpi=180)
    plt.close(fig)
    print(f"[INFO] Visualisasi fungsi keanggotaan disimpan ke: {out_file}")


def analisis_interval():
    """Analisis no. 3: interval centroid 1, 5, 10 RPM pada kondisi D."""
    alpha = aktivasi_aturan(fuzzifikasi(33, 65))
    acuan = mamdani(alpha, 1)
    print("\n=== ANALISIS 3: INTERVAL CENTROID (kondisi D) ===")
    print(f"{'Interval':>9}{'Titik':>8}{'Mamdani (RPM)':>16}{'Selisih vs 1':>14}{'Waktu rata-rata (ms)':>24}")
    
    steps = [1, 5, 10]
    waktu_list = []
    selisih_list = []
    hasil_list = []

    for step in steps:
        mulai = time.perf_counter()
        for _ in range(ULANG):
            hasil = mamdani(alpha, step)
        waktu_ms = (time.perf_counter() - mulai) / ULANG * 1000
        titik = len(range(500, 1501, step))
        selisih = hasil - acuan
        waktu_list.append(waktu_ms)
        selisih_list.append(selisih)
        hasil_list.append(hasil)
        print(f"{step:>9}{titik:>8}{hasil:>16.4f}{selisih:>14.4f}{waktu_ms:>24.4f}")

    # Buat grafik benchmark interval centroid
    os.makedirs(FOLDER, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # Subplot 1: Waktu Eksekusi
    bars1 = ax1.bar([str(s) for s in steps], waktu_list, color=["#1F3A4D", "#2E6F7E", "#5B8E7D"], width=0.5, edgecolor="black")
    ax1.set_title("Waktu Komputasi per Eksekusi", fontweight="bold")
    ax1.set_xlabel("Interval Diskretisasi (RPM)", fontweight="bold")
    ax1.set_ylabel("Waktu (ms)", fontweight="bold")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    for b in bars1:
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.015, f"{b.get_height():.3f} ms", ha="center", fontsize=9)

    # Subplot 2: Deviasi Nilai Output
    bars2 = ax2.bar([str(s) for s in steps], selisih_list, color=["#C8553D", "#E07A5F", "#F2CC8F"], width=0.5, edgecolor="black")
    ax2.set_title("Selisih Deviasi terhadap Acuan (1 RPM)", fontweight="bold")
    ax2.set_xlabel("Interval Diskretisasi (RPM)", fontweight="bold")
    ax2.set_ylabel("Selisih (RPM)", fontweight="bold")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    for b in bars2:
        ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.02, f"{b.get_height():+.4f}", ha="center", fontsize=9)

    fig.suptitle("Benchmark Interval Centroid Mamdani (Kondisi Uji D: T=33°C, H=65%)", fontsize=12, fontweight="bold")
    fig.tight_layout()
    out_file = os.path.join(FOLDER, "benchmark_centroid.png")
    fig.savefig(out_file, dpi=180)
    plt.close(fig)
    print(f"[INFO] Grafik benchmark centroid disimpan ke: {out_file}")


def analisis_suhu():
    """Analisis no. 4: suhu 20-40 (langkah 1) pada kelembapan 65%."""
    suhu = list(range(20, 41))
    m, s, t = [], [], []
    for T in suhu:
        alpha = aktivasi_aturan(fuzzifikasi(T, 65))
        m.append(mamdani(alpha)); s.append(sugeno(alpha)); t.append(tsukamoto(alpha))

    print("\n=== ANALISIS 4: SUHU 20-40 °C, KELEMBAPAN 65% ===")
    print(f"{'T':>4}{'Mamdani':>10}{'Sugeno':>10}{'Tsukamoto':>12}")
    for i, T in enumerate(suhu):
        print(f"{T:>4}{m[i]:>10.2f}{s[i]:>10.2f}{t[i]:>12.2f}")

    for nama, data in (("Mamdani", m), ("Sugeno", s), ("Tsukamoto", t)):
        turun = [(suhu[i], suhu[i + 1]) for i in range(len(data) - 1) if data[i + 1] < data[i] - 1e-9]
        status = "selalu naik" if not turun else f"ada penurunan di {turun}"
        print(f"{nama}: {status}")

    os.makedirs(FOLDER, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(suhu, m, marker="o", label="Mamdani", color="#1F3A4D", linewidth=2, markersize=5)
    ax.plot(suhu, s, marker="s", label="Sugeno", color="#C8553D", linewidth=2, markersize=5)
    ax.plot(suhu, t, marker="^", label="Tsukamoto", color="#5B8E7D", linewidth=2, markersize=5)
    ax.set_xlabel("Suhu (°C)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Kecepatan Kipas (RPM)", fontsize=11, fontweight="bold")
    ax.set_title("Analisis Sensitivitas Suhu terhadap Kecepatan Kipas (H = 65%)", fontsize=12, fontweight="bold", pad=10)
    ax.legend(framealpha=0.9)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    out_file = os.path.join(FOLDER, "suhu_kelembapan65.png")
    fig.savefig(out_file, dpi=180)
    plt.close(fig)
    print(f"[INFO] Grafik respon suhu disimpan ke: {out_file}")


def jalankan_analisis():
    visualisasi_fungsi_keanggotaan()
    analisis_interval()
    analisis_suhu()


if __name__ == "__main__":
    jalankan_analisis()
    if "--show" in sys.argv:
        plt.show()
