import math

T_MIN, T_MAX = 20, 40
H_MIN, H_MAX = 40, 80


def _ke_angka(nilai, nama):
    try:
        x = float(str(nilai).strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"{nama} '{nilai}' bukan angka.")
    if not math.isfinite(x):
        raise ValueError(f"{nama} '{nilai}' bukan angka yang valid.")
    return x


def validasi_input(suhu, lembap):
    """Periksa tipe dan rentang. Mengembalikan (T, H) atau raise ValueError."""
    T = _ke_angka(suhu, "Suhu")
    H = _ke_angka(lembap, "Kelembapan")
    if not (T_MIN <= T <= T_MAX):
        raise ValueError(f"Suhu {T} di luar rentang {T_MIN}-{T_MAX} °C.")
    if not (H_MIN <= H <= H_MAX):
        raise ValueError(f"Kelembapan {H} di luar rentang {H_MIN}-{H_MAX} %.")
    return T, H


def fuzzifikasi(T, H):
    return {
        "T_rendah": (40 - T) / 20,
        "T_tinggi": (T - 20) / 20,
        "H_rendah": (80 - H) / 40,
        "H_tinggi": (H - 40) / 40,
    }


def aktivasi_aturan(mu):
    """Return [a1, a2, a3, a4], AND = minimum."""
    return [
        min(mu["T_rendah"], mu["H_rendah"]),  # R1 -> Lambat
        min(mu["T_rendah"], mu["H_tinggi"]),  # R2 -> Lambat
        min(mu["T_tinggi"], mu["H_rendah"]),  # R3 -> Cepat
        min(mu["T_tinggi"], mu["H_tinggi"]),  # R4 -> Cepat
    ]