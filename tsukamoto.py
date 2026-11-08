def tsukamoto(alpha):
    a1, a2, a3, a4 = alpha
    z = [1500 - 1000 * a1, 1500 - 1000 * a2,   # Lambat
         500 + 1000 * a3, 500 + 1000 * a4]     # Cepat
    penyebut = sum(alpha)
    if penyebut == 0:
        return None
    return sum(a * zi for a, zi in zip(alpha, z)) / penyebut