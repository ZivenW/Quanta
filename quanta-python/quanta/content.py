"""Materi dan generator soal (dwibahasa). Setiap templat soal menghasilkan soal baru dengan angka acak."""
import random
import re

QE = 1.602e-19
R = random.randint


def B(i, e):
    return {"id": i, "en": e}


def D(s, lang):
    """Angka desimal: koma untuk Indonesia, titik untuk Inggris."""
    return re.sub(r"(?<=\d)\.(?=\d)", ",", s) if lang == "id" else s


def two(fn):
    return {lang: D(fn(lang), lang) for lang in ("id", "en")}


def fm(x):
    a = abs(x)
    return f"{x:.0f}" if a >= 100 else f"{x:.1f}" if a >= 10 else f"{x:.2f}"


def mc(c, lv, q, right, wrong, ex, hints):
    o = [right] + wrong
    random.shuffle(o)
    return dict(c=c, l=lv, kind="mc", t=q, opts=o, ans=o.index(right), ex=ex, hints=hints)


def num(c, lv, q, ans, unit, ex, hints):
    return dict(c=c, l=lv, kind="num", t=q, ans=ans, unit=unit, ex=ex, hints=hints)


def t_like():
    return mc(0, 1,
        B("Dua benda bermuatan sama tanda didekatkan. Apa yang terjadi?", "Two objects with the same sign of charge are brought close. What happens?"),
        B("Saling tolak", "They repel"),
        [B("Saling tarik", "They attract"), B("Tidak ada gaya", "No force"), B("Bergantung pada massa", "Depends on their mass")],
        B("Muatan sejenis tolak-menolak, muatan berlawanan tarik-menarik.", "Like charges repel; opposite charges attract."),
        [B("Bayangkan dua kutub magnet yang sama.", "Think of two identical magnet poles."), B("Sejenis tolak, berlawanan tarik.", "Like repels, opposite attracts.")])


def t_elec():
    n = R(2, 9)
    v = n * 1e12 * QE * 1e6
    return num(0, 2,
        two(lambda l: f"Sebuah benda kelebihan {n}×10¹² elektron. Berapa besar muatannya (µC)?" if l == "id" else f"An object has {n}×10¹² extra electrons. What is its charge (µC)?"),
        v, "µC", two(lambda l: f"Q = N·e = {n}×10¹² × 1.6×10⁻¹⁹ C = {fm(v)} µC"),
        [B("Muatan = jumlah elektron × muatan satu elektron.", "Charge = number of electrons × charge of one electron."), B("e = 1,6×10⁻¹⁹ C dan 1 µC = 10⁻⁶ C.", "e = 1.6×10⁻¹⁹ C and 1 µC = 10⁻⁶ C.")])


def t_scale():
    n = R(2, 4)
    return mc(1, 1,
        two(lambda l: f"Jarak antara dua muatan dijadikan {n} kali semula. Gaya Coulomb menjadi…" if l == "id" else f"The distance between two charges is multiplied by {n}. The Coulomb force becomes…"),
        two(lambda l: f"1/{n*n} kali" if l == "id" else f"1/{n*n} as large"),
        [two(lambda l: f"1/{n} kali" if l == "id" else f"1/{n} as large"), two(lambda l: f"{n*n} kali" if l == "id" else f"{n*n} times as large"), two(lambda l: f"{n} kali" if l == "id" else f"{n} times as large")],
        B("F sebanding dengan 1/r², jadi jarak dikali n membuat gaya dibagi n².", "F is proportional to 1/r², so distance × n divides the force by n²."),
        [B("Lihat pangkat r pada rumus Coulomb.", "Look at the power of r in Coulomb's law."), B("F ∝ 1/r²", "F ∝ 1/r²")])


def t_coulomb():
    a, b, r = R(2, 9), R(2, 9), R(10, 40)
    F = 89.9 * a * b / (r * r)
    return num(1, 2,
        two(lambda l: f"Dua muatan {a} µC dan {b} µC terpisah {r} cm di udara. Berapa gaya Coulomb di antara keduanya (N)?" if l == "id" else f"Two charges, {a} µC and {b} µC, are {r} cm apart in air. What is the Coulomb force between them (N)?"),
        F, "N", two(lambda l: f"F = kq₁q₂/r² = 8.99×10⁹ × ({a}×10⁻⁶)({b}×10⁻⁶) / ({r}×10⁻²)² = {fm(F)} N"),
        [B("Ubah dulu µC ke C dan cm ke m.", "Convert µC to C and cm to m first."), B("F = k·q₁·q₂ / r² dengan k = 8,99×10⁹.", "F = k·q₁·q₂ / r² with k = 8.99×10⁹.")])


def t_net():
    q, a, b, d = R(2, 5), R(4, 9), R(1, 3), R(8, 20)
    F = 89.9 * q * (a - b) / (d * d)
    return num(1, 4,
        two(lambda l: f"Tiga muatan sejenis segaris, berurutan {a} µC, {q} µC, dan {b} µC, dengan jarak {d} cm antar-muatan. Berapa besar gaya total pada muatan {q} µC di tengah (N)?" if l == "id" else f"Three like charges on a line, in order {a} µC, {q} µC, {b} µC, spaced {d} cm apart. What is the net force on the middle {q} µC charge (N)?"),
        F, "N", two(lambda l: f"Dua gaya tolak berlawanan arah: F = kq({a} − {b})×10⁻⁶ / d² = {fm(F)} N" if l == "id" else f"Two repulsive forces in opposite directions: F = kq({a} − {b})×10⁻⁶ / d² = {fm(F)} N"),
        [B("Gambar arah kedua gaya pada muatan tengah.", "Draw the direction of both forces on the middle charge."), B("Searah dijumlah, berlawanan dikurangi.", "Same direction add, opposite directions subtract.")])


def t_field():
    q, r = R(2, 9), R(10, 40)
    E = 89900 * q / (r * r)
    return num(2, 2,
        two(lambda l: f"Muatan titik {q} µC. Berapa besar medan listrik pada jarak {r} cm (kN/C)?" if l == "id" else f"A point charge of {q} µC. What is the electric field magnitude at {r} cm (kN/C)?"),
        E, "kN/C", two(lambda l: f"E = kq/r² = 8.99×10⁹ × {q}×10⁻⁶ / ({r}×10⁻²)² = {fm(E)} kN/C"),
        [B("Medan titik: E = kq/r².", "Point charge field: E = kq/r²."), B("Hasil dalam N/C, bagi 1000 untuk kN/C.", "The result is in N/C; divide by 1000 for kN/C.")])


def t_dipole():
    q, d = R(2, 9), R(10, 30)
    E = 8 * 89900 * q / (d * d)
    return num(3, 3,
        two(lambda l: f"Muatan +{q} µC dan −{q} µC terpisah {d} cm. Berapa besar medan listrik di titik tengah keduanya (kN/C)?" if l == "id" else f"Charges +{q} µC and −{q} µC are {d} cm apart. What is the field magnitude at the midpoint (kN/C)?"),
        E, "kN/C", two(lambda l: f"Kedua medan searah (menuju −q): E = 2kq/(d/2)² = 8kq/d² = {fm(E)} kN/C" if l == "id" else f"Both fields point toward −q: E = 2kq/(d/2)² = 8kq/d² = {fm(E)} kN/C"),
        [B("Di titik tengah, arah medan dari +q dan −q sama atau berlawanan?", "At the midpoint, do the fields of +q and −q point the same way or opposite?"), B("Searah, jadi dijumlahkan: 2·kq/(d/2)².", "Same way, so add them: 2·kq/(d/2)².")])


def t_zero():
    n, d = R(2, 3), random.choice([30, 40, 60])
    x = n * d / (n + 1)
    return num(3, 4,
        two(lambda l: f"Muatan {n*n}q di x = 0 dan muatan q (sejenis) di x = {d} cm. Pada jarak berapa dari muatan {n*n}q medan totalnya nol (cm)?" if l == "id" else f"Charge {n*n}q sits at x = 0 and a like charge q at x = {d} cm. How far from the {n*n}q charge is the net field zero (cm)?"),
        x, "cm", two(lambda l: f"{n*n}/x² = 1/(d − x)² sehingga x = n·d/(n+1) = {n}×{d}/{n+1} = {fm(x)} cm" if l == "id" else f"{n*n}/x² = 1/(d − x)² so x = n·d/(n+1) = {n}×{d}/{n+1} = {fm(x)} cm"),
        [B("Titik nol ada di antara kedua muatan. Samakan besar kedua medan.", "The zero point lies between the charges. Set the two field magnitudes equal."), B("Akarkan kedua sisi: n/x = 1/(d − x).", "Take square roots: n/x = 1/(d − x).")])


TEMPLATES = [(0, 1, t_like), (0, 2, t_elec), (1, 1, t_scale), (1, 2, t_coulomb), (1, 4, t_net), (2, 2, t_field), (3, 3, t_dipole), (3, 4, t_zero)]


def make(c, level):
    pool = [(lv, f) for cc, lv, f in TEMPLATES if cc == c]
    best = min(abs(lv - level) for lv, _ in pool)
    return random.choice([f for lv, f in pool if abs(lv - level) == best])()


BABS = [B("Muatan & Medan Listrik", "Electric Charge & Field"), B("Tegangan & Arus", "Voltage & Current"), B("Hambatan & Kapasitansi", "Resistance & Capacitance"), B("Rangkaian", "Circuits"), B("Medan Magnet", "Magnetic Fields")]

BAB1 = {"babs": BABS, "lessons": [
    {"title": B("Muatan dan Hukum Coulomb", "Charge and Coulomb's Law"), "sim": {"force": True, "probe": False}, "blocks": [
        {"h": B("Apa itu muatan?", "What is charge?"), "p": B(
            "Muatan adalah sifat dasar materi, ada dua jenis: <b>positif</b> dan <b>negatif</b>. Muatan sejenis tolak-menolak, berlawanan tarik-menarik. Muatan itu <b>terkuantisasi</b>: Q = N·e dengan e = 1,602×10⁻¹⁹ C, dan jumlah muatan total pada sistem tertutup selalu <b>kekal</b>.",
            "Charge is a basic property of matter, and it comes in two kinds: <b>positive</b> and <b>negative</b>. Like charges repel, opposite charges attract. Charge is <b>quantized</b>: Q = N·e with e = 1.602×10⁻¹⁹ C, and the total charge of a closed system is always <b>conserved</b>.")},
        {"h": B("Hukum Coulomb", "Coulomb's law"), "p": B(
            "<b>F = k·|q₁q₂| / r²</b>, dengan k = 8,99×10⁹ N·m²/C². Gaya bekerja sepanjang garis penghubung kedua muatan, besarnya sama dan arahnya berlawanan (Hukum III Newton). Jarak dua kali lebih besar membuat gaya jadi seperempat.",
            "<b>F = k·|q₁q₂| / r²</b>, with k = 8.99×10⁹ N·m²/C². The force acts along the line joining the charges, equal in size and opposite in direction (Newton's third law). Doubling the distance makes the force one quarter.")},
        {"h": B("Banyak muatan", "Many charges"), "p": B(
            "Gaya total adalah jumlah <b>vektor</b> dari gaya tiap muatan (superposisi). Pada satu garis lurus, gaya searah dijumlahkan dan yang berlawanan dikurangkan.",
            "The net force is the <b>vector</b> sum of the force from each charge (superposition). On a straight line, forces in the same direction add and opposite ones subtract.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 1, "p": B(
            "Dua bola logam identik bermuatan q₁ dan q₂ disentuhkan, lalu dipisahkan lagi pada jarak semula. Muatan tiap bola menjadi (q₁ + q₂)/2 karena muatan kekal. Bandingkan gaya sebelum dan sesudah. Kapan gayanya bertambah, dan kapan berubah dari tarik menjadi tolak?",
            "Two identical metal spheres with charges q₁ and q₂ touch, then return to the original separation. Each now carries (q₁ + q₂)/2 because charge is conserved. Compare the force before and after. When does it grow, and when does it flip from attraction to repulsion?")}]},
    {"title": B("Medan Listrik dan Superposisi", "Electric Field and Superposition"), "sim": {"force": False, "probe": True}, "blocks": [
        {"h": B("Medan listrik", "Electric field"), "p": B(
            "Medan listrik didefinisikan <b>E = F/q₀</b>, yaitu gaya per muatan uji positif. Untuk muatan titik, <b>E = kq/r²</b>. Arahnya menjauhi muatan positif dan menuju muatan negatif.",
            "The electric field is defined as <b>E = F/q₀</b>, the force per positive test charge. For a point charge, <b>E = kq/r²</b>. It points away from positive charges and toward negative ones.")},
        {"h": B("Superposisi medan", "Superposition of fields"), "p": B(
            "Medan total di suatu titik adalah jumlah vektor medan tiap muatan. Di titik tengah dua muatan sama +q, medannya nol karena saling meniadakan. Di titik tengah +q dan −q, medannya searah sehingga besarnya <b>8kq/d²</b>.",
            "The net field at a point is the vector sum of each charge's field. At the midpoint of two equal +q charges the field is zero because they cancel. At the midpoint of +q and −q the fields point the same way, giving <b>8kq/d²</b>.")},
        {"h": B("Titik medan nol", "Zero-field point"), "p": B(
            "Untuk dua muatan sejenis, ada satu titik di antaranya tempat medan total nol, lebih dekat ke muatan yang lebih kecil. Jika muatannya n²q dan q, titik itu berjarak <b>n·d/(n+1)</b> dari muatan yang besar.",
            "For two like charges there is one point between them where the net field is zero, nearer the smaller charge. For charges n²q and q it lies <b>n·d/(n+1)</b> from the larger one.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 3, "p": B(
            "Untuk muatan +4q dan −q, di manakah medan totalnya nol? Mengapa titik itu berada di luar segmen penghubung, di sisi muatan yang lebih kecil?",
            "For charges +4q and −q, where is the net field zero? Why does that point lie outside the segment joining them, on the side of the smaller charge?")}]}]}


# ---------------- Bab 2: Tegangan & Arus (konsep global 4 sampai 7) ----------------
def X(i, e):
    return B(D(i, "id"), D(e, "en"))


def t_dirp():
    return mc(4, 1, B("Muatan positif dilepas diam di dalam medan listrik. Ia akan bergerak menuju…", "A positive charge is released from rest in an electric field. It moves toward…"),
        B("Potensial yang lebih rendah", "Lower potential"), [B("Potensial yang lebih tinggi", "Higher potential"), B("Tetap diam", "It stays at rest"), B("Tegak lurus garis medan", "Perpendicular to the field lines")],
        B("Gaya searah medan, dan medan menunjuk ke potensial yang menurun. Energi potensial turun, energi kinetik naik.", "The force points along the field, and the field points toward falling potential. Potential energy drops, kinetic energy rises."),
        [B("Ke arah mana gaya pada muatan positif?", "Which way is the force on a positive charge?"), B("Searah medan, dan medan menunjuk ke potensial yang lebih rendah.", "Along the field, and the field points toward lower potential.")])


def t_ue():
    q, v = R(2, 9), R(20, 90)
    return num(4, 2, X(f"Muatan {q} µC dipindahkan melalui beda potensial {v} V. Berapa perubahan energi potensial listriknya (µJ)?", f"A {q} µC charge moves through a potential difference of {v} V. What is the change in its potential energy (µJ)?"),
        q * v, "µJ", X(f"ΔU = qΔV = {q}×10⁻⁶ × {v} = {fm(q * v)} µJ", f"ΔU = qΔV = {q}×10⁻⁶ × {v} = {fm(q * v)} µJ"),
        [B("Gunakan ΔU = q·ΔV.", "Use ΔU = q·ΔV."), B("1 µC × 1 V = 1 µJ.", "1 µC × 1 V = 1 µJ.")])


def t_ev():
    return mc(5, 1, B("Satu elektronvolt (1 eV) adalah…", "One electronvolt (1 eV) is…"),
        B("Energi elektron setelah melewati beda potensial 1 V", "The energy of an electron after crossing a 1 V potential difference"),
        [B("Satuan muatan listrik", "A unit of electric charge"), B("Arus satu elektron per detik", "A current of one electron per second"), B("Beda potensial milik satu elektron", "The potential difference of one electron")],
        B("1 eV = e × 1 V ≈ 1,6×10⁻¹⁹ J. Satuan ini untuk energi, bukan tegangan atau muatan.", "1 eV = e × 1 V ≈ 1.6×10⁻¹⁹ J. It is a unit of energy, not of voltage or charge."),
        [B("Lihat gabungan e (muatan) dan V (volt): hasilnya energi.", "Combine e (charge) and V (volts): the product is energy."), B("ΔU = qΔV dengan q = e dan ΔV = 1 V.", "ΔU = qΔV with q = e and ΔV = 1 V.")])


def t_speed():
    v = R(1, 4) * 100
    s = (2 * QE * v / 9.109e-31) ** 0.5 / 1e6
    return num(5, 3, X(f"Elektron dari keadaan diam dipercepat melalui beda potensial {v} V. Berapa kecepatannya (×10⁶ m/s)?", f"An electron starting at rest is accelerated through {v} V. What is its speed (×10⁶ m/s)?"),
        s, "×10⁶ m/s", X(f"½mv² = eV sehingga v = √(2eV/m) = √(2 × 1.6×10⁻¹⁹ × {v} / 9.11×10⁻³¹) = {fm(s)}×10⁶ m/s", f"½mv² = eV so v = √(2eV/m) = √(2 × 1.6×10⁻¹⁹ × {v} / 9.11×10⁻³¹) = {fm(s)}×10⁶ m/s"),
        [B("Energi potensial yang hilang menjadi energi kinetik.", "The potential energy lost becomes kinetic energy."), B("eV = ½mv², dengan m = 9,11×10⁻³¹ kg.", "eV = ½mv², with m = 9.11×10⁻³¹ kg.")])


def t_vpt():
    q, r = R(2, 9), R(10, 40)
    v = 899 * q / r
    return num(6, 2, X(f"Muatan titik {q} µC. Berapa potensial listrik pada jarak {r} cm (kV)?", f"A point charge of {q} µC. What is the electric potential at {r} cm (kV)?"),
        v, "kV", X(f"V = kq/r = 8.99×10⁹ × {q}×10⁻⁶ / ({r}×10⁻²) = {fm(v)} kV", f"V = kq/r = 8.99×10⁹ × {q}×10⁻⁶ / ({r}×10⁻²) = {fm(v)} kV"),
        [B("Potensial muatan titik: V = kq/r (tanpa kuadrat).", "Point-charge potential: V = kq/r (no square)."), B("Hasil dalam volt, bagi 1000 untuk kV.", "The result is in volts; divide by 1000 for kV.")])


def t_vzero():
    return mc(6, 3, B("Muatan +q dan −q terpisah jarak d. Berapa potensial listrik di titik tengah keduanya?", "Charges +q and −q are a distance d apart. What is the electric potential at their midpoint?"),
        B("Nol, meskipun medannya tidak nol", "Zero, even though the field is not zero"),
        [B("kq/d", "kq/d"), B("2kq/d", "2kq/d"), B("Sama dengan besar medannya", "Equal to the field magnitude")],
        B("Potensial adalah skalar: +kq/(d/2) dan −kq/(d/2) saling meniadakan. Medannya justru searah dan menjumlah.", "Potential is a scalar: +kq/(d/2) and −kq/(d/2) cancel. The fields, however, point the same way and add."),
        [B("Potensial dijumlah tanpa arah. Perhatikan tanda tiap muatan.", "Potentials add without direction. Watch the sign of each charge."), B("+kq/r dan −kq/r di jarak yang sama.", "+kq/r and −kq/r at the same distance.")])


def t_vsum():
    a, b, d = R(2, 6), R(2, 6), 2 * R(10, 20)
    v = 899 * (a + b) / (d / 2)
    return num(6, 4, X(f"Muatan {a} µC dan {b} µC (sejenis) terpisah {d} cm. Berapa potensial listrik di titik tengah keduanya (kV)?", f"Charges of {a} µC and {b} µC (same sign) are {d} cm apart. What is the electric potential at their midpoint (kV)?"),
        v, "kV", X(f"V = k({a} + {b})×10⁻⁶ / ({d}/2 ×10⁻²) = {fm(v)} kV", f"V = k({a} + {b})×10⁻⁶ / ({d}/2 ×10⁻²) = {fm(v)} kV"),
        [B("Jarak ke tiap muatan adalah setengah d.", "The distance to each charge is half of d."), B("Jumlahkan kq/r dari kedua muatan.", "Add kq/r from both charges.")])


def t_dirI():
    return mc(7, 1, B("Pada kawat logam, arah arus konvensional dibandingkan arah gerak elektron adalah…", "In a metal wire, the direction of conventional current compared with electron motion is…"),
        B("Berlawanan", "Opposite"), [B("Searah", "The same"), B("Saling tegak lurus", "Perpendicular"), B("Bergantung pada panjang kawat", "Dependent on the wire length")],
        B("Arus konvensional didefinisikan sebagai arah muatan positif. Elektron bermuatan negatif sehingga bergerak berlawanan.", "Conventional current is defined as the direction of positive charge flow. Electrons are negative, so they move the opposite way."),
        [B("Arus konvensional mengikuti muatan positif.", "Conventional current follows positive charge."), B("Elektron bermuatan apa?", "What is the sign of an electron's charge?")])


def t_I():
    q, t = R(6, 48), R(2, 12)
    i = q / t
    return num(7, 2, X(f"Dalam {t} detik mengalir muatan {q} C melalui penampang kawat. Berapa arus rata-rata (A)?", f"In {t} s a charge of {q} C flows through a wire's cross-section. What is the average current (A)?"),
        i, "A", X(f"I = Q/t = {q}/{t} = {fm(i)} A", f"I = Q/t = {q}/{t} = {fm(i)} A"),
        [B("Arus adalah muatan per waktu.", "Current is charge per unit time."), B("I = Q/t, 1 A = 1 C/s.", "I = Q/t, 1 A = 1 C/s.")])


def t_vd():
    i, a = R(2, 10), R(1, 4)
    v = i / (8.5e28 * QE * a * 1e-6) * 1e6
    return num(7, 4, X(f"Kawat tembaga luas penampang {a} mm² dialiri arus {i} A. Dengan n = 8,5×10²⁸ elektron/m³, berapa kecepatan hanyut elektron (µm/s)?", f"A copper wire of cross-section {a} mm² carries {i} A. With n = 8.5×10²⁸ electrons/m³, what is the electron drift speed (µm/s)?"),
        v, "µm/s", X(f"v = I/(neA) = {i} / (8.5×10²⁸ × 1.6×10⁻¹⁹ × {a}×10⁻⁶) = {fm(v)} µm/s", f"v = I/(neA) = {i} / (8.5×10²⁸ × 1.6×10⁻¹⁹ × {a}×10⁻⁶) = {fm(v)} µm/s"),
        [B("Gunakan I = n·e·A·v. Ubah mm² ke m².", "Use I = n·e·A·v. Convert mm² to m²."), B("v = I/(n·e·A); hasil dalam m/s, kalikan 10⁶ untuk µm/s.", "v = I/(n·e·A); the result is in m/s, multiply by 10⁶ for µm/s.")])


TEMPLATES += [(4, 1, t_dirp), (4, 2, t_ue), (5, 1, t_ev), (5, 3, t_speed), (6, 2, t_vpt), (6, 3, t_vzero), (6, 4, t_vsum), (7, 1, t_dirI), (7, 2, t_I), (7, 4, t_vd)]

BAB2 = [
    {"title": B("Energi Potensial dan Beda Potensial", "Potential Energy and Potential Difference"), "sim": {"force": False, "probe": True, "volt": True}, "blocks": [
        {"h": B("Energi potensial listrik", "Electric potential energy"), "p": B(
            "Gaya listrik bersifat <b>konservatif</b>: kerja yang dilakukannya sama dengan penurunan energi potensial, <b>W = −ΔU</b>. Muatan positif yang dilepas dalam medan bergerak ke tempat berenergi potensial lebih rendah, dan energi potensialnya berubah menjadi energi kinetik.",
            "The electric force is <b>conservative</b>: the work it does equals the drop in potential energy, <b>W = −ΔU</b>. A positive charge released in a field moves toward lower potential energy, and that energy becomes kinetic energy.")},
        {"h": B("Beda potensial", "Potential difference"), "p": B(
            "<b>V = U/q</b>, satuannya volt (1 V = 1 J/C). Memindahkan muatan q melalui beda potensial ΔV mengubah energi potensialnya sebesar <b>ΔU = qΔV</b>. Satu elektronvolt adalah energi elektron setelah melewati 1 V, sekitar 1,6×10⁻¹⁹ J. Partikel bermuatan q dan bermassa m yang dipercepat dari diam melalui ΔV mencapai <b>v = √(2qΔV/m)</b>.",
            "<b>V = U/q</b>, measured in volts (1 V = 1 J/C). Moving a charge q through a potential difference ΔV changes its potential energy by <b>ΔU = qΔV</b>. One electronvolt is the energy of an electron after crossing 1 V, about 1.6×10⁻¹⁹ J. A particle of charge q and mass m accelerated from rest through ΔV reaches <b>v = √(2qΔV/m)</b>.")},
        {"h": B("Potensial muatan titik", "Potential of a point charge"), "p": B(
            "<b>V = kq/r</b>. Potensial adalah besaran <b>skalar</b>, jadi potensial banyak muatan dijumlahkan secara aljabar biasa tanpa memikirkan arah. Permukaan ekuipotensial selalu tegak lurus terhadap garis medan.",
            "<b>V = kq/r</b>. Potential is a <b>scalar</b>, so the potential of many charges is a plain algebraic sum with no directions. Equipotential surfaces are always perpendicular to the field lines.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 6, "p": B(
            "Pada muatan +q dan −q, potensial di titik tengah nol tetapi medannya tidak nol. Jelaskan mengapa keduanya bisa berbeda. Lalu, untuk muatan +2q di x = 0 dan −q di x = d, cari semua titik pada garis hubung yang potensialnya nol.",
            "For charges +q and −q, the potential at the midpoint is zero but the field is not. Explain why they can differ. Then, for +2q at x = 0 and −q at x = d, find every point on the line joining them where the potential is zero.")}]},
    {"title": B("Arus Listrik", "Electric Current"), "sim": {"cur": True}, "blocks": [
        {"h": B("Arus dan arahnya", "Current and its direction"), "p": B(
            "<b>I = dQ/dt</b>, satuannya ampere (1 A = 1 C/s). Arah arus konvensional adalah arah gerak muatan positif, sehingga di kawat logam arahnya <b>berlawanan</b> dengan gerak elektron.",
            "<b>I = dQ/dt</b>, measured in amperes (1 A = 1 C/s). Conventional current points in the direction positive charge would move, so in a metal wire it is <b>opposite</b> to the motion of the electrons.")},
        {"h": B("Kecepatan hanyut", "Drift speed"), "p": B(
            "Pada penghantar berlaku <b>I = n·e·A·v</b>, dengan n rapat elektron bebas dan A luas penampang. Di tembaga, arus 5 A pada kawat 2 mm² hanya menghasilkan kecepatan hanyut sekitar 0,18 mm/s.",
            "In a conductor <b>I = n·e·A·v</b>, where n is the free-electron density and A the cross-section. In copper, 5 A in a 2 mm² wire gives a drift speed of only about 0.18 mm/s.")},
        {"h": B("Muatan yang mengalir", "Charge that flows"), "p": B(
            "Untuk arus tetap, muatan yang melewati penampang dalam waktu t adalah <b>Q = I·t</b>. Pada simulasi, jumlah elektron yang melewati garis putus-putus tiap detik bertambah sebanding dengan arus.",
            "For a steady current, the charge passing a cross-section in time t is <b>Q = I·t</b>. In the simulation, the number of electrons crossing the dashed line each second grows in proportion to the current.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 7, "p": B(
            "Jika elektron hanyut begitu lambat, mengapa lampu menyala seketika saat saklar ditutup? Perkirakan berapa lama sebuah elektron perlu untuk menempuh kawat sepanjang 1 m dengan kecepatan hanyut di atas.",
            "If electrons drift so slowly, why does a lamp light instantly when the switch closes? Estimate how long one electron needs to travel 1 m of wire at the drift speed above.")}]}]

CHAPTERS = [BAB1["lessons"], BAB2]


# ---------------- Bab 3 sampai 5 (konsep global 8 sampai 19) ----------------
def T(c, lv):
    def deco(f):
        TEMPLATES.append((c, lv, f))
        return f
    return deco


def N(c, lv, qi, qe, ans, unit, ex, form, hi, he):
    return num(c, lv, X(qi, qe), ans, unit, X(ex, ex), [B(hi, he), X(form, form)])


def M(c, lv, qi, qe, right, wrong, exi, exe, hi, he, form):
    return mc(c, lv, B(qi, qe), B(*right), [B(*w) for w in wrong], B(exi, exe), [B(hi, he), B(form, form)])


# --- Bab 3: Hambatan & Kapasitansi ---
@T(8, 1)
def _():
    return M(8, 1, "Panjang sebuah kawat dijadikan dua kali (luas penampang tetap). Hambatannya menjadi…", "A wire's length is doubled (same cross-section). Its resistance becomes…", ("2 kali", "2 times"), [("Setengahnya", "Half"), ("4 kali", "4 times"), ("Tetap", "Unchanged")], "R = ρL/A, jadi R sebanding dengan L.", "R = ρL/A, so R is proportional to L.", "Lihat posisi L pada rumus hambatan.", "Look at where L sits in the resistance formula.", "R = ρL/A")


@T(8, 2)
def _():
    L, A = R(5, 50), R(1, 4)
    r = 17 * L / A
    return N(8, 2, f"Kawat tembaga (ρ = 1.7×10⁻⁸ Ω·m) panjang {L} m, luas penampang {A} mm². Berapa hambatannya (mΩ)?", f"A copper wire (ρ = 1.7×10⁻⁸ Ω·m) is {L} m long with a {A} mm² cross-section. What is its resistance (mΩ)?", r, "mΩ", f"R = ρL/A = 1.7×10⁻⁸ × {L} / ({A}×10⁻⁶) = {fm(r)} mΩ", "R = ρL/A", "Ubah mm² ke m² lebih dulu.", "Convert mm² to m² first.")


@T(9, 2)
def _():
    r, i = R(2, 20), R(2, 9)
    return N(9, 2, f"Hambatan {r} Ω dialiri arus {i} A. Berapa daya yang berubah menjadi panas (W)?", f"A {r} Ω resistor carries {i} A. How much power is dissipated as heat (W)?", i * i * r, "W", f"P = I²R = {i}² × {r} = {fm(i*i*r)} W", "P = I²R", "Daya resistor dari arus dan hambatan.", "Resistor power from current and resistance.")


@T(9, 4)
def _():
    return M(9, 4, "Kawat berhambatan R diregangkan hingga panjangnya dua kali (volume tetap). Hambatannya menjadi…", "A wire of resistance R is stretched to twice its length (same volume). Its resistance becomes…", ("4R", "4R"), [("2R", "2R"), ("R/2", "R/2"), ("R", "R")], "Volume tetap: L dua kali berarti A setengah, jadi R = ρL/A naik 2 × 2 = 4 kali.", "Same volume: twice L means half A, so R = ρL/A grows by 2 × 2 = 4.", "Kalau panjang naik, apa yang terjadi pada luas penampang?", "When length grows, what happens to the cross-section?", "V = A·L tetap")


@T(10, 1)
def _():
    return M(10, 1, "Jarak antar keping kapasitor keping sejajar dijadikan dua kali (luas tetap). Kapasitansinya menjadi…", "The plate separation of a parallel-plate capacitor is doubled (same area). Its capacitance becomes…", ("Setengahnya", "Half"), [("2 kali", "2 times"), ("4 kali", "4 times"), ("Tetap", "Unchanged")], "C = ε₀A/d, jadi C berbanding terbalik dengan d.", "C = ε₀A/d, so C is inversely proportional to d.", "Lihat posisi d pada rumus C.", "Look at where d sits in the formula for C.", "C = ε₀A/d")


@T(10, 2)
def _():
    a, d = R(20, 100), R(1, 5)
    c = 0.8854 * a / d
    return N(10, 2, f"Kapasitor keping sejajar berluas {a} cm² dan berjarak {d} mm (udara). Berapa kapasitansinya (pF)?", f"A parallel-plate capacitor has plates of {a} cm² spaced {d} mm apart (air). What is its capacitance (pF)?", c, "pF", f"C = ε₀A/d = 8.85×10⁻¹² × {a}×10⁻⁴ / ({d}×10⁻³) = {fm(c)} pF", "C = ε₀A/d, ε₀ = 8.85×10⁻¹² F/m", "Ubah cm² ke m² dan mm ke m.", "Convert cm² to m² and mm to m.")


@T(10, 3)
def _():
    c, v = R(2, 9), R(6, 24)
    u = 0.5 * c * v * v
    return N(10, 3, f"Kapasitor {c} µF diisi hingga {v} V. Berapa energi yang tersimpan (µJ)?", f"A {c} µF capacitor is charged to {v} V. How much energy does it store (µJ)?", u, "µJ", f"U = ½CV² = ½ × {c}×10⁻⁶ × {v}² = {fm(u)} µJ", "U = ½CV²", "Energi kapasitor dari C dan V.", "Capacitor energy from C and V.")


@T(11, 2)
def _():
    a, b = R(2, 9), R(2, 9)
    c = a * b / (a + b)
    return N(11, 2, f"Kapasitor {a} µF dan {b} µF dihubungkan seri. Berapa kapasitansi ekuivalennya (µF)?", f"A {a} µF and a {b} µF capacitor are connected in series. What is the equivalent capacitance (µF)?", c, "µF", f"1/C = 1/{a} + 1/{b} → C = {fm(c)} µF", "1/C = 1/C₁ + 1/C₂", "Seri: jumlahkan kebalikannya.", "In series, add the reciprocals.")


@T(11, 4)
def _():
    a, b, v = R(2, 9), R(2, 9), R(6, 24)
    x = v * b / (a + b)
    return N(11, 4, f"Kapasitor {a} µF dan {b} µF diseri pada baterai {v} V. Berapa tegangan pada kapasitor {a} µF (V)?", f"A {a} µF and a {b} µF capacitor in series are connected to a {v} V battery. What is the voltage across the {a} µF capacitor (V)?", x, "V", f"Muatan sama: V₁ = V·C₂/(C₁ + C₂) = {v} × {b}/({a} + {b}) = {fm(x)} V", "Q sama: V₁ = Q/C₁", "Pada rangkaian seri, muatan tiap kapasitor sama.", "In series, each capacitor holds the same charge.")


BAB3 = [
    {"title": B("Hambatan dan Hukum Ohm", "Resistance and Ohm's Law"), "sim": {"g": "ohm"}, "blocks": [
        {"h": B("Hambatan jenis", "Resistivity"), "p": B("<b>R = ρL/A</b>: hambatan naik dengan panjang L dan turun dengan luas penampang A. Nilai ρ bergantung bahan (tembaga sekitar 1,7×10⁻⁸ Ω·m).", "<b>R = ρL/A</b>: resistance grows with length L and falls with cross-section A. ρ depends on the material (copper is about 1.7×10⁻⁸ Ω·m).")},
        {"h": B("Hukum Ohm dan daya", "Ohm's law and power"), "p": B("<b>V = IR</b> untuk penghantar ohmik. Daya yang berubah menjadi panas: <b>P = IV = I²R = V²/R</b>.", "<b>V = IR</b> for an ohmic conductor. Power dissipated as heat: <b>P = IV = I²R = V²/R</b>.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 9, "p": B("Kawat diregangkan sampai panjangnya dua kali tanpa mengubah volume. Mengapa hambatannya menjadi empat kali, bukan dua kali?", "A wire is stretched to twice its length at constant volume. Why does its resistance become four times larger, not two?")}]},
    {"title": B("Kapasitor", "Capacitors"), "sim": {"g": "cap"}, "blocks": [
        {"h": B("Kapasitansi dan energi", "Capacitance and energy"), "p": B("<b>Q = CV</b>. Keping sejajar: <b>C = ε₀A/d</b>, ε₀ = 8,85×10⁻¹² F/m. Energi tersimpan <b>U = ½CV²</b>. Dielektrik memperbesar C sebesar faktor κ.", "<b>Q = CV</b>. Parallel plates: <b>C = ε₀A/d</b>, ε₀ = 8.85×10⁻¹² F/m. Stored energy is <b>U = ½CV²</b>. A dielectric multiplies C by a factor κ.")},
        {"h": B("Seri dan paralel", "Series and parallel"), "p": B("Paralel: <b>C = C₁ + C₂</b> (tegangan sama). Seri: <b>1/C = 1/C₁ + 1/C₂</b> (muatan sama), dan tegangan terbagi berbanding terbalik dengan C.", "Parallel: <b>C = C₁ + C₂</b> (same voltage). Series: <b>1/C = 1/C₁ + 1/C₂</b> (same charge), and the voltage splits in inverse proportion to C.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 11, "p": B("Dua kapasitor identik, satu terisi dan satu kosong, dihubungkan paralel. Muatan terbagi rata, tetapi energi total turun menjadi setengah. Ke mana energi yang hilang?", "Two identical capacitors, one charged and one empty, are connected in parallel. The charge splits evenly, yet the total energy halves. Where did the energy go?")}]}]


# --- Bab 4: Rangkaian ---
@T(12, 1)
def _():
    return M(12, 1, "Baterai nyata yang mengalirkan arus punya tegangan terminal yang, dibanding GGL-nya…", "A real battery delivering current has a terminal voltage that, compared with its emf, is…", ("Lebih kecil", "Smaller"), [("Lebih besar", "Larger"), ("Sama", "Equal"), ("Nol", "Zero")], "V = ε − Ir: sebagian tegangan hilang pada hambatan dalam.", "V = ε − Ir: some voltage is lost across the internal resistance.", "Baterai punya hambatan di dalamnya.", "A battery has resistance inside it.", "V = ε − Ir")


@T(12, 2)
def _():
    e, r, i = R(6, 12), R(2, 10) / 10, R(1, 3)
    v = e - i * r
    return N(12, 2, f"Baterai GGL {e} V dan hambatan dalam {r:.1f} Ω mengalirkan arus {i} A. Berapa tegangan terminalnya (V)?", f"A battery with emf {e} V and internal resistance {r:.1f} Ω delivers {i} A. What is its terminal voltage (V)?", v, "V", f"V = ε − Ir = {e} − {i} × {r:.1f} = {fm(v)} V", "V = ε − Ir", "Kurangi GGL dengan penurunan tegangan di dalam.", "Subtract the internal voltage drop from the emf.")


@T(13, 2)
def _():
    a, b, v = R(2, 10), R(2, 10), R(6, 24)
    i = v / (a + b)
    return N(13, 2, f"Resistor {a} Ω dan {b} Ω diseri pada baterai {v} V. Berapa arusnya (A)?", f"A {a} Ω and a {b} Ω resistor in series are connected to a {v} V battery. What is the current (A)?", i, "A", f"I = V/(R₁ + R₂) = {v}/({a} + {b}) = {fm(i)} A", "R = R₁ + R₂", "Seri: hambatan dijumlahkan.", "In series, resistances add.")


@T(13, 3)
def _():
    a, b = R(2, 12), R(2, 12)
    r = a * b / (a + b)
    return N(13, 3, f"Resistor {a} Ω dan {b} Ω dihubungkan paralel. Berapa hambatan ekuivalennya (Ω)?", f"A {a} Ω and a {b} Ω resistor are connected in parallel. What is the equivalent resistance (Ω)?", r, "Ω", f"1/R = 1/{a} + 1/{b} → R = {fm(r)} Ω", "1/R = 1/R₁ + 1/R₂", "Paralel: jumlahkan kebalikannya.", "In parallel, add the reciprocals.")


@T(13, 4)
def _():
    r = R(2, 12)
    return N(13, 4, f"Tiga resistor identik {r} Ω: dua dipasang paralel, lalu diseri dengan yang ketiga. Berapa hambatan totalnya (Ω)?", f"Three identical {r} Ω resistors: two in parallel, then in series with the third. What is the total resistance (Ω)?", 1.5 * r, "Ω", f"R = {r}/2 + {r} = {fm(1.5*r)} Ω", "Dua paralel identik = R/2", "Hitung bagian paralelnya dulu.", "Work out the parallel part first.")


@T(14, 2)
def _():
    e1, e2, a, b = R(10, 24), R(2, 8), R(2, 8), R(2, 8)
    i = (e1 - e2) / (a + b)
    return N(14, 2, f"Baterai {e1} V dan {e2} V dipasang berlawanan dalam satu loop dengan resistor {a} Ω dan {b} Ω (hambatan dalam diabaikan). Berapa arusnya (A)?", f"Batteries of {e1} V and {e2} V oppose each other in one loop with {a} Ω and {b} Ω resistors (internal resistance ignored). What is the current (A)?", i, "A", f"I = (ε₁ − ε₂)/(R₁ + R₂) = ({e1} − {e2})/({a} + {b}) = {fm(i)} A", "Σ ΔV = 0 sepanjang loop", "Hukum loop: GGL searah dan berlawanan saling mengurangi.", "Loop rule: opposing emfs subtract.")


@T(14, 3)
def _():
    a, b = R(2, 6), R(3, 8)
    c = R(1, a + b - 1)
    return N(14, 3, f"Di sebuah titik cabang, arus {a} A dan {b} A masuk, dan {c} A keluar lewat satu cabang. Berapa arus di cabang keluar lainnya (A)?", f"At a junction, {a} A and {b} A flow in and {c} A flows out through one branch. What is the current in the other outgoing branch (A)?", a + b - c, "A", f"I = {a} + {b} − {c} = {a+b-c} A", "Σ I masuk = Σ I keluar", "Muatan kekal di titik cabang.", "Charge is conserved at a junction.")


@T(15, 1)
def _():
    return M(15, 1, "Pada t = τ = RC, kapasitor yang sedang diisi mencapai kira-kira…", "At t = τ = RC, a charging capacitor reaches about…", ("63% tegangan akhir", "63% of the final voltage"), [("50% tegangan akhir", "50% of the final voltage"), ("86% tegangan akhir", "86% of the final voltage"), ("100% tegangan akhir", "100% of the final voltage")], "V = ε(1 − e⁻¹) ≈ 0,63ε.", "V = ε(1 − e⁻¹) ≈ 0.63ε.", "Masukkan t = τ ke rumus pengisian.", "Put t = τ into the charging formula.", "V = ε(1 − e^(−t/τ))")


@T(15, 2)
def _():
    r, c = R(1, 10), R(1, 10)
    return N(15, 2, f"Kapasitor {c} µF diisi lewat resistor {r} kΩ. Berapa konstanta waktunya (ms)?", f"A {c} µF capacitor charges through a {r} kΩ resistor. What is its time constant (ms)?", r * c, "ms", f"τ = RC = {r}×10³ × {c}×10⁻⁶ = {r*c} ms", "τ = RC", "Kalikan R dan C dalam satuan dasar.", "Multiply R and C in base units.")


@T(15, 3)
def _():
    r, c, n, e = R(1, 10), R(1, 10), R(1, 3), R(6, 12)
    v = e * (1 - 2.718281828 ** -n)
    return N(15, 3, f"Kapasitor {c} µF diisi lewat {r} kΩ dari baterai {e} V. Berapa tegangannya setelah {n * r * c} ms (V)?", f"A {c} µF capacitor charges through {r} kΩ from a {e} V battery. What is its voltage after {n * r * c} ms (V)?", v, "V", f"τ = {r*c} ms, t = {n}τ → V = {e}(1 − e^−{n}) = {fm(v)} V", "V = ε(1 − e^(−t/τ))", "Cari τ dulu, lalu bandingkan dengan t.", "Find τ first, then compare it with t.")


BAB4 = [
    {"title": B("Rangkaian Seri, Paralel, dan Kirchhoff", "Series, Parallel and Kirchhoff"), "sim": {"g": "ser"}, "blocks": [
        {"h": B("GGL, seri, dan paralel", "Emf, series and parallel"), "p": B("Baterai nyata: tegangan terminal <b>V = ε − Ir</b>. Seri: <b>R = R₁ + R₂</b> (arus sama). Paralel: <b>1/R = 1/R₁ + 1/R₂</b> (tegangan sama).", "A real battery: terminal voltage <b>V = ε − Ir</b>. Series: <b>R = R₁ + R₂</b> (same current). Parallel: <b>1/R = 1/R₁ + 1/R₂</b> (same voltage).")},
        {"h": B("Hukum Kirchhoff", "Kirchhoff's laws"), "p": B("<b>Titik cabang</b>: arus masuk sama dengan arus keluar (muatan kekal). <b>Loop</b>: jumlah beda potensial sepanjang loop tertutup nol (energi kekal).", "<b>Junction</b>: current in equals current out (charge conservation). <b>Loop</b>: the potential differences around a closed loop sum to zero (energy conservation).")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 13, "p": B("Tiga resistor identik R dirangkai dengan segala cara yang mungkin. Sebutkan semua hambatan total yang bisa diperoleh.", "Three identical resistors R are connected in every possible way. List every total resistance you can obtain.")}]},
    {"title": B("Rangkaian RC", "RC Circuits"), "sim": {"g": "rc"}, "blocks": [
        {"h": B("Pengisian", "Charging"), "p": B("Saat diisi lewat R: <b>V_C = ε(1 − e^(−t/τ))</b> dengan <b>τ = RC</b>. Pada t = τ, tegangan kapasitor mencapai sekitar 63% nilai akhirnya.", "While charging through R: <b>V_C = ε(1 − e^(−t/τ))</b> with <b>τ = RC</b>. At t = τ the capacitor reaches about 63% of its final voltage.")},
        {"h": B("Pengosongan", "Discharging"), "p": B("Saat dikosongkan: <b>V_C = V₀·e^(−t/τ)</b>. Arus ikut meluruh dengan τ yang sama. Setelah sekitar 5τ, kapasitor praktis penuh atau kosong.", "While discharging: <b>V_C = V₀·e^(−t/τ)</b>. The current decays with the same τ. After about 5τ the capacitor is effectively full or empty.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 15, "p": B("Kapasitor 1000 µF bertegangan 12 V dikosongkan lewat resistor 10 kΩ. Berapa lama sampai tegangannya turun menjadi 1 V? Gunakan logaritma natural.", "A 1000 µF capacitor at 12 V discharges through a 10 kΩ resistor. How long until its voltage falls to 1 V? Use the natural logarithm.")}]}]


# --- Bab 5: Medan Magnet ---
@T(16, 1)
def _():
    return M(16, 1, "Muatan bergerak sejajar dengan arah medan magnet. Gaya magnet padanya…", "A charge moves parallel to the magnetic field. The magnetic force on it is…", ("Nol", "Zero"), [("Maksimum", "Maximum"), ("Searah kecepatan", "Along its velocity"), ("Searah medan", "Along the field")], "F = qvB sin θ, dan θ = 0 membuat sin θ = 0.", "F = qvB sin θ, and θ = 0 gives sin θ = 0.", "Perhatikan sudut antara v dan B.", "Look at the angle between v and B.", "F = qvB sin θ")


@T(16, 2)
def _():
    q, v, b = R(2, 9), R(1, 9) * 100, R(2, 9)
    f = q * v * b * 1e-3
    return N(16, 2, f"Muatan {q} µC bergerak {v} m/s tegak lurus medan magnet {b} mT. Berapa gaya magnetnya (µN)?", f"A {q} µC charge moves at {v} m/s perpendicular to a {b} mT magnetic field. What is the magnetic force (µN)?", f, "µN", f"F = qvB = {q}×10⁻⁶ × {v} × {b}×10⁻³ = {fm(f)} µN", "F = qvB", "Tegak lurus berarti sin θ = 1.", "Perpendicular means sin θ = 1.")


@T(16, 3)
def _():
    v, b = R(2, 9), R(1, 4)
    r = 5.686 * v / b
    return N(16, 3, f"Elektron berkecepatan {v}×10⁶ m/s masuk tegak lurus medan {b} mT. Berapa jari-jari lintasannya (mm)?", f"An electron at {v}×10⁶ m/s enters perpendicular to a {b} mT field. What is the radius of its path (mm)?", r, "mm", f"r = mv/(eB) = 9.11×10⁻³¹ × {v}×10⁶ / (1.6×10⁻¹⁹ × {b}×10⁻³) = {fm(r)} mm", "r = mv/(qB)", "Gaya magnet berperan sebagai gaya sentripetal.", "The magnetic force acts as the centripetal force.")


@T(16, 4)
def _():
    return M(16, 4, "Kecepatan partikel bermuatan dalam medan magnet seragam (tegak lurus medan) dijadikan dua kali. Periode putarnya menjadi…", "The speed of a charged particle in a uniform magnetic field (perpendicular to it) is doubled. Its orbital period becomes…", ("Tetap", "Unchanged"), [("Dua kali", "Twice"), ("Setengahnya", "Half"), ("Empat kali", "Four times")], "T = 2πm/(qB) tidak bergantung pada v: jari-jari ikut dua kali, kelilingnya juga.", "T = 2πm/(qB) does not depend on v: the radius doubles too, and so does the circumference.", "Bagaimana r berubah ketika v berubah?", "How does r change when v changes?", "T = 2πr/v = 2πm/(qB)")


@T(17, 1)
def _():
    return M(17, 1, "Dua kawat sejajar dialiri arus searah. Keduanya akan…", "Two parallel wires carry currents in the same direction. They will…", ("Saling tarik", "Attract each other"), [("Saling tolak", "Repel each other"), ("Tidak berinteraksi", "Not interact"), ("Berputar", "Rotate")], "Arus searah menimbulkan gaya tarik-menarik.", "Currents in the same direction attract.", "Medan satu kawat memberi gaya pada arus kawat lainnya.", "One wire's field exerts a force on the other wire's current.", "F/L = μ₀I₁I₂/(2πd)")


@T(17, 2)
def _():
    b, i, l = R(20, 80), R(2, 9), R(10, 40)
    f = b * i * l * 1e-2
    return N(17, 2, f"Kawat {l} cm dialiri arus {i} A tegak lurus medan magnet {b} mT. Berapa gaya padanya (mN)?", f"A {l} cm wire carrying {i} A is perpendicular to a {b} mT field. What is the force on it (mN)?", f, "mN", f"F = BIL = {b}×10⁻³ × {i} × {l}×10⁻² = {fm(f)} mN", "F = BIL", "Ubah mT ke T dan cm ke m.", "Convert mT to T and cm to m.")


@T(17, 3)
def _():
    a, b, d = R(2, 9), R(2, 9), R(2, 10)
    f = 20 * a * b / d
    return N(17, 3, f"Dua kawat lurus sejajar berarus {a} A dan {b} A, berjarak {d} cm. Berapa gaya per satuan panjang (µN/m)?", f"Two long parallel wires carry {a} A and {b} A, {d} cm apart. What is the force per unit length (µN/m)?", f, "µN/m", f"F/L = μ₀I₁I₂/(2πd) = 2×10⁻⁷ × {a} × {b} / ({d}×10⁻²) = {fm(f)} µN/m", "F/L = μ₀I₁I₂/(2πd)", "μ₀/2π = 2×10⁻⁷ T·m/A.", "μ₀/2π = 2×10⁻⁷ T·m/A.")


@T(18, 2)
def _():
    i, r = R(2, 9), R(2, 10)
    b = 20 * i / r
    return N(18, 2, f"Kawat lurus panjang berarus {i} A. Berapa besar medan magnet pada jarak {r} cm (µT)?", f"A long straight wire carries {i} A. What is the magnetic field at {r} cm (µT)?", b, "µT", f"B = μ₀I/(2πr) = 2×10⁻⁷ × {i} / ({r}×10⁻²) = {fm(b)} µT", "B = μ₀I/(2πr)", "Medan kawat lurus berbanding terbalik dengan r.", "A straight wire's field is inversely proportional to r.")


@T(18, 3)
def _():
    i, r = R(2, 9), R(2, 10)
    b = 62.83 * i / r
    return N(18, 3, f"Loop kawat melingkar berjari-jari {r} cm dialiri arus {i} A. Berapa medan magnet di pusatnya (µT)?", f"A circular wire loop of radius {r} cm carries {i} A. What is the magnetic field at its center (µT)?", b, "µT", f"B = μ₀I/(2R) = 4π×10⁻⁷ × {i} / (2 × {r}×10⁻²) = {fm(b)} µT", "B = μ₀I/(2R)", "μ₀ = 4π×10⁻⁷ T·m/A.", "μ₀ = 4π×10⁻⁷ T·m/A.")


@T(19, 1)
def _():
    return M(19, 1, "Di dalam solenoid ideal yang panjang, medan magnetnya…", "Inside a long ideal solenoid, the magnetic field is…", ("Hampir seragam dan sejajar sumbu", "Nearly uniform and parallel to the axis"), [("Nol", "Zero"), ("Melingkar mengelilingi sumbu", "Circular around the axis"), ("Makin besar ke tepi", "Larger toward the edge")], "Hukum Ampere pada loop persegi panjang menunjukkan B = μ₀nI, seragam di dalam.", "Ampère's law on a rectangular loop gives B = μ₀nI, uniform inside.", "Bayangkan banyak loop berjajar menguatkan satu sama lain di dalam.", "Picture many loops reinforcing one another inside.", "B = μ₀nI")


@T(19, 2)
def _():
    n, i = R(5, 20), R(1, 5)
    b = 0.12566 * n * i
    return N(19, 2, f"Solenoid dengan {n} lilitan per cm dialiri arus {i} A. Berapa medan magnet di dalamnya (mT)?", f"A solenoid with {n} turns per cm carries {i} A. What is the field inside it (mT)?", b, "mT", f"B = μ₀nI = 4π×10⁻⁷ × {n*100} × {i} = {fm(b)} mT", "B = μ₀nI", "Ubah lilitan per cm menjadi per meter.", "Convert turns per cm to turns per metre.")


@T(19, 4)
def _():
    a, b = R(5, 12), R(2, 4)
    s = 1.2566 * (a - b)
    return N(19, 4, f"Sebuah loop Ampere melingkupi dua kawat berarus {a} A dan {b} A dengan arah berlawanan. Berapa nilai ∮B·dl (µT·m)?", f"An Amperian loop encloses two wires carrying {a} A and {b} A in opposite directions. What is ∮B·dl (µT·m)?", s, "µT·m", f"∮B·dl = μ₀(I₁ − I₂) = 4π×10⁻⁷ × ({a} − {b}) = {fm(s)} µT·m", "∮B·dl = μ₀I_enc", "Arus berlawanan arah saling mengurangi.", "Currents in opposite directions subtract.")


BAB5 = [
    {"title": B("Gaya Magnet pada Muatan", "Magnetic Force on Charges"), "sim": {"g": "mag"}, "blocks": [
        {"h": B("Gaya magnet", "Magnetic force"), "p": B("<b>F = qv × B</b>, besarnya <b>qvB sin θ</b>. Gaya selalu tegak lurus kecepatan, sehingga <b>tidak melakukan kerja</b>: ia hanya membelokkan lintasan.", "<b>F = qv × B</b>, with magnitude <b>qvB sin θ</b>. The force is always perpendicular to the velocity, so it <b>does no work</b>: it only bends the path.")},
        {"h": B("Gerak melingkar", "Circular motion"), "p": B("Untuk v ⊥ B, lintasannya lingkaran dengan <b>r = mv/(qB)</b> dan periode <b>T = 2πm/(qB)</b>, yang tidak bergantung pada kecepatan.", "For v ⊥ B the path is a circle with <b>r = mv/(qB)</b> and period <b>T = 2πm/(qB)</b>, which does not depend on speed.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 16, "p": B("Medan magnet tidak bisa menambah energi kinetik partikel, tetapi siklotron tetap bisa mempercepatnya. Apa yang melakukan kerja, dan mengapa periode putaran yang tetap membuatnya mungkin?", "A magnetic field cannot raise a particle's kinetic energy, yet a cyclotron still accelerates particles. What does the work, and why does the constant orbital period make it possible?")}]},
    {"title": B("Arus, Medan, dan Hukum Ampere", "Currents, Fields and Ampère's Law"), "sim": {"g": "wire"}, "blocks": [
        {"h": B("Gaya pada kawat", "Force on wires"), "p": B("<b>F = BIL sin θ</b>. Dua kawat sejajar: arus searah <b>tarik-menarik</b>, berlawanan tolak-menolak, dengan <b>F/L = μ₀I₁I₂/(2πd)</b>.", "<b>F = BIL sin θ</b>. Two parallel wires: currents in the same direction <b>attract</b>, opposite directions repel, with <b>F/L = μ₀I₁I₂/(2πd)</b>.")},
        {"h": B("Medan oleh arus dan Hukum Ampere", "Fields from currents and Ampère's law"), "p": B("Kawat lurus: <b>B = μ₀I/(2πr)</b>. Pusat loop: <b>B = μ₀I/(2R)</b>. Solenoid: <b>B = μ₀nI</b>. Hukum Ampere: <b>∮B·dl = μ₀I_enc</b>, hanya arus di dalam loop yang dihitung. μ₀ = 4π×10⁻⁷ T·m/A.", "Straight wire: <b>B = μ₀I/(2πr)</b>. Loop center: <b>B = μ₀I/(2R)</b>. Solenoid: <b>B = μ₀nI</b>. Ampère's law: <b>∮B·dl = μ₀I_enc</b>, only currents inside the loop count. μ₀ = 4π×10⁻⁷ T·m/A.")},
        {"h": B("Tantangan olimpiade", "Olympiad challenge"), "c": 19, "p": B("Gunakan hukum Ampere untuk menunjukkan bahwa medan di luar kabel koaksial ideal, dengan arus yang sama besar tetapi berlawanan arah di inti dan selubung, bernilai nol.", "Use Ampère's law to show that the field outside an ideal coaxial cable, with equal and opposite currents in the core and sheath, is zero.")}]}]

CHAPTERS += [BAB3, BAB4, BAB5]
