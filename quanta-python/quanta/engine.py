"""Mesin AI QUANTA.

1) HMM / Bayesian Knowledge Tracing: status tersembunyi "paham" vs "belum",
   observasi = jawaban benar/salah (dengan peluang tebakan dan salah-ceroboh).
2) Logika fuzzy (Sugeno): peluang paham -> tingkat kesulitan soal berikutnya.
3) Logika prasyarat: bab n hanya terbuka jika bab n-1 lulus.
"""
SLIP, LEARN = 0.10, 0.12
GUESS = {"mc": 0.25, "num": 0.05}


def bkt_update(p, ok, kind):
    """Perbarui peluang paham setelah satu jawaban (filtering HMM satu langkah)."""
    g = GUESS[kind]
    if ok:
        post = p * (1 - SLIP) / (p * (1 - SLIP) + (1 - p) * g)
    else:
        post = p * SLIP / (p * SLIP + (1 - p) * (1 - g))
    return post + (1 - post) * LEARN  # transisi: bisa belajar antar soal


def fuzzy_level(p):
    """Rendah->1,2  Sedang->2,4  Tinggi->3,8 (rata-rata berbobot derajat keanggotaan)."""
    low = max(0.0, (0.5 - p) / 0.5)
    high = max(0.0, (p - 0.5) / 0.5)
    mid = max(0.0, 1 - abs(p - 0.5) / 0.25)
    return (low * 1.2 + mid * 2.4 + high * 3.8) / (low + mid + high)


def choose_concept(p, n, allowed, phase):
    """Tes awal: ratakan dulu cakupan konsep. Selain itu: konsep terlemah."""
    if phase == "pre":
        return min(allowed, key=lambda c: (n[c], p[c]))
    return min(allowed, key=lambda c: p[c])


def unlocked(done, bab):
    return bab == 0 or (bab - 1) in done
