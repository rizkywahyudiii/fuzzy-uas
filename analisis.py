import os
import time
import matplotlib.pyplot as plt
from dasar import fuzzifikasi, aktivasi_aturan
from mamdani import mamdani
from sugeno import sugeno
from tsukamoto import tsukamoto

FOLDER = "hasil"
ULANG = 200  # pengulangan untuk rata-rata waktu


def analisis_interval():
    """Analisis no. 3: interval centroid 1, 5, 10 RPM pada kondisi D."""
    alpha = aktivasi_aturan(fuzzifikasi(33, 65))
    acuan = mamdani(alpha, 1)
    print("\n=== ANALISIS 3: INTERVAL CENTROID (kondisi D) ===")
    print(f"{'Interval':>9}{'Titik':>8}{'Mamdani (RPM)':>16}{'Selisih vs 1':>14}{'Waktu rata-rata (ms)':>24}")
    for step in (1, 5, 10):
        mulai = time.perf_counter()
        for _ in range(ULANG):
            hasil = mamdani(alpha, step)
        waktu_ms = (time.perf_counter() - mulai) / ULANG * 1000
        titik = len(range(500, 1501, step))
        print(f"{step:>9}{titik:>8}{hasil:>16.4f}{hasil - acuan:>14.4f}{waktu_ms:>24.4f}")


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
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(suhu, m, marker="o", label="Mamdani", color="#1F3A4D")
    ax.plot(suhu, s, marker="s", label="Sugeno", color="#C8553D")
    ax.plot(suhu, t, marker="^", label="Tsukamoto", color="#8FA7B5")
    ax.set_xlabel("Suhu (°C)")
    ax.set_ylabel("Kecepatan kipas (RPM)")
    ax.set_title("Pengaruh suhu pada kelembapan 65%")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FOLDER, "suhu_kelembapan65.png"), dpi=150)


def jalankan_analisis():
    analisis_interval()
    analisis_suhu()


if __name__ == "__main__":
    jalankan_analisis()
    plt.show()