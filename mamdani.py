def mamdani(alpha, step=1):
    """Centroid diskret z = 500..1500. Hasil = pendekatan numerik
    terhadap centroid kontinu."""
    a1, a2, a3, a4 = alpha
    atas = 0.0
    bawah = 0.0
    for z in range(500, 1501, step):
        lambat = (1500 - z) / 1000
        cepat = (z - 500) / 1000
        mu = max(min(a1, lambat), min(a2, lambat),
                 min(a3, cepat), min(a4, cepat))
        atas += z * mu
        bawah += mu
    if bawah == 0:
        return None
    return atas / bawah