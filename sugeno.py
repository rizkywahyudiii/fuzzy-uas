def sugeno(alpha):
    z = [500, 500, 1500, 1500]
    penyebut = sum(alpha)
    if penyebut == 0:
        return None
    return sum(a * zi for a, zi in zip(alpha, z)) / penyebut