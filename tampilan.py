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
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    metode_cfg = [
        ("Mamdani", "#1F3A4D"),
        ("Sugeno", "#C8553D"),
        ("Tsukamoto", "#5B8E7D"),
    ]

    for k, (label, warna) in enumerate(metode_cfg):
        nilai = [h[k + 1] if h[k + 1] is not None else 0 for h in hasil]
        posisi = [i + (k - 1) * lebar for i in range(n)]
        bars = ax.bar(posisi, nilai, lebar, label=label, color=warna, edgecolor="black", linewidth=0.5)
        
        # Tambahkan label angka di atas setiap bar
        for bar, val in zip(bars, nilai):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 15,
                    f"{val:.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    rotation=0
                )

    ax.set_xticks(range(n))
    ax.set_xticklabels([f"Uji {nm}" for nm in nama], fontweight="bold")
    ax.set_xlabel("Skenario Pengujian", fontsize=11, fontweight="bold")
    ax.set_ylabel("Kecepatan Kipas (RPM)", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 1750)
    ax.set_title("Perbandingan Hasil Defuzzifikasi: Mamdani vs Sugeno vs Tsukamoto", fontsize=12, fontweight="bold", pad=12)
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    
    fig.tight_layout()
    output_path = os.path.join(FOLDER, "perbandingan_uji.png")
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    print(f"\n[INFO] Grafik perbandingan berhasil disimpan ke: {output_path}")
