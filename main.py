import sys
from dasar import validasi_input, fuzzifikasi, aktivasi_aturan
from mamdani import mamdani
from sugeno import sugeno
from tsukamoto import tsukamoto

UJI_VALID = [
    ("A", 24, 45), ("B", 28, 55), ("C", 30, 60), ("D", 33, 65),
    ("E", 37, 75), ("F", 20, 40), ("G", 40, 80),
]
UJI_TOLAK = [
    ("H", 45, 65),
    ("I (nonnumerik)", "abc", 60),
]


def f2(x):
    return "-" if x is None else f"{x:.2f}"


def hitung(T, H):
    mu = fuzzifikasi(T, H)
    alpha = aktivasi_aturan(mu)
    return mu, alpha, mamdani(alpha), sugeno(alpha), tsukamoto(alpha)


def tampil_detail(nama, T, H, mu, alpha, m, s, t):
    print(f"\n[Uji {nama}] T={T:g} °C, H={H:g} %")
    print(f"  Suhu       : rendah={mu['T_rendah']:.2f}  tinggi={mu['T_tinggi']:.2f}")
    print(f"  Kelembapan : rendah={mu['H_rendah']:.2f}  tinggi={mu['H_tinggi']:.2f}")
    print("  Alpha      : " + "  ".join(f"R{i+1}={a:.2f}" for i, a in enumerate(alpha)))
    print(f"  Mamdani={f2(m)}  Sugeno={f2(s)}  Tsukamoto={f2(t)} RPM")


def jalankan_batch():
    hasil, ditolak = [], []
    for nama, suhu, lembap in UJI_VALID + UJI_TOLAK:
        try:
            T, H = validasi_input(suhu, lembap)
        except ValueError as e:
            ditolak.append((nama, suhu, lembap, str(e)))
            continue
        mu, alpha, m, s, t = hitung(T, H)
        tampil_detail(nama, T, H, mu, alpha, m, s, t)
        hasil.append((nama, m, s, t))

    print("\n=== RINGKASAN HASIL (RPM) ===")
    print(f"{'Uji':<5}{'Mamdani':>10}{'Sugeno':>10}{'Tsukamoto':>12}")
    for nama, m, s, t in hasil:
        print(f"{nama:<5}{f2(m):>10}{f2(s):>10}{f2(t):>12}")

    print("\n=== INPUT DITOLAK ===")
    for nama, suhu, lembap, pesan in ditolak:
        print(f"Uji {nama}: T={suhu}, H={lembap} -> DITOLAK. {pesan}")


def jalankan_manual():
    suhu = input("Suhu (20-40 °C)       : ")
    lembap = input("Kelembapan (40-80 %)  : ")
    try:
        T, H = validasi_input(suhu, lembap)
    except ValueError as e:
        print(f"ERROR: {e}")
        return
    mu, alpha, m, s, t = hitung(T, H)
    tampil_detail("manual", T, H, mu, alpha, m, s, t)


if __name__ == "__main__":
    if "--manual" in sys.argv:
        jalankan_manual()
    else:
        jalankan_batch()