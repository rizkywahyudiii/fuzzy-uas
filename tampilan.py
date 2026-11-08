import os
import matplotlib.pyplot as plt

FOLDER = "hasil"


def f2(x):
    return "-" if x is None else f"{x:.2f}"


def tampilkan_hasil(hasil):
    """hasil = list of (nama, mamdani, sugeno, tsukamoto). Cetak tabel + buat grafik."""
    os.makedirs(FOLDER, exist_ok=True)

    print("\n=== RINGKASAN HASIL (RPM) ===")
    print(f"{'Uji':<5}{'Mamdani':>10}{'Sugeno':>10}{'Tsukamoto':>12}")
    for nama, m, s, t in hasil:
        print(f"{nama:<5}{f2(m):>10}{f2(s):>10}{f2(t):>12}")

    nama = [h[0] for h in hasil]
    n = len(nama)
    lebar = 0.27
    fig, ax = plt.subplots(figsize=(9, 5))
    for k, (label, warna) in enumerate([("Mamdani", "#1F3A4D"), ("Sugeno", "#C8553D"), ("Tsukamoto", "#8FA7B5")]):
        nilai = [h[k + 1] if h[k + 1] is not None else 0 for h in hasil]
        ax.bar([i + (k - 1) * lebar for i in range(n)], nilai, lebar, label=label, color=warna)
    ax.set_xticks(range(n))
    ax.set_xticklabels(nama)
    ax.set_xlabel("Uji")
    ax.set_ylabel("Kecepatan kipas (RPM)")
    ax.set_title("Perbandingan Mamdani, Sugeno, dan Tsukamoto (uji valid)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FOLDER, "perbandingan_uji.png"), dpi=150)