# QUANTA (Python / Flask)

Aplikasi belajar Fisika adaptif: tes awal, materi dengan simulasi, latihan kilat, tes akhir, lalu piagam. Dwibahasa (ID/EN).

## Menjalankan
```bash
pip install -r requirements.txt
cd quanta
python app.py          # buka http://127.0.0.1:5000
```

## Maskot AI (Muon)
Dua petunjuk pertama berasal dari bank soal (gratis). Pertanyaan bebas ke AI hanya muncul sesudahnya, hanya pada latihan (tidak saat tes), dan dibatasi 3 kali per siswa.
Untuk mengaktifkan jawaban AI: `set ANTHROPIC_API_KEY=...` (Windows) atau `export ANTHROPIC_API_KEY=...`, lalu jalankan ulang. Model dapat diganti lewat `QUANTA_MODEL`.

## Struktur
| Berkas | Isi |
|---|---|
| `engine.py` | HMM/BKT (peluang paham), logika fuzzy (tingkat kesulitan), logika prasyarat bab |
| `content.py` | Materi dwibahasa dan generator soal berangka acak |
| `app.py` | Server Flask dan API |
| `templates/index.html` | Seluruh antarmuka: halaman awal, simulasi, maskot, piagam |

## Menambah bab
Tambahkan templat soal di `content.py` (daftar `TEMPLATES`) dan pelajaran di `BAB1`, lalu perluas `STEPS` di `index.html`.
