## KONTEN (wajib)
- selalu download kit baru
- Lihat top 5 leaderboard sebagai referensi visual, lalu riset mandiri dari sumber publik.
- Urutkan berita berdasarkan topik paling hangat.
- Komposisi: 3 kartu utama, 8 kartu kecil, sisanya masuk daftar di samping peta.
- Tabel kotak — koordinat + ukuran semua elemen, plus jarak antar blok (4px / 4px / 10px).
- Kartu — utama 326×188, kecil 244×160 dengan ilustrasi di atas ±3/4 kartu + badge.
- Peta — area 372×186, aturan titik/badge/legenda/caption.
- Daftar — 19 entri, 2 kolom × 10 baris.
- DATE CHECK — kotak 1000×28, badge merah 50×22, dua baris isi mulai x=76 (sejajar, tidak turun ke bawah badge), baris 2 tanpa tanggal, tanpa alasan, SOURCE di luar kotak.
- ilustrasi card kecil berada di atas card.3/4 di pake ilustrasi dan badge
- Setiap ilustrasi harus menunjukkan **lokasi + waktu + apa yang terjadi**, cukup detail untuk dipahami hanya dari gambar. Jika sulit dibuat ilustrasi yang benar, ganti beritanya.
- Semua berita harus benar-benar berasal dari tanggal bounty. Sertakan DATE CHECK berisi berita yang sengaja tidak dimasukkan beserta alasannya.

## VISUAL (wajib)
- Peta dunia asli yang diperkecil dan jelas. Nomor berita memakai titik + panah/garis agar tidak bertumpuk. Warna nomor mengikuti 7 warna region (samakan skema warna dengan entri top 5). **Ikuti spesifikasi lengkap di `#PETA`** (data GeoJSON, proyeksi, titik, panah, penempatan badge, legenda, dan audit peta).
- **Ruang yang tersedia harus diisi oleh isi**, bukan hanya kotaknya: ilustrasi dan teks ikut membesar. Dilarang ada kartu utama maupun kartu kecil yang kosong / menyisakan ruang besar.
- Cek apakah teks menimpa garis atau terpotong; perbaiki jika iya.
- cek apakah text pada badge di ilustrasi tidak tepat berada di tengah badge ,perbaiki
- Teks kecil tidak boleh terpotong di tengah kalimat.
- cek lagi apakah ilustrasi mengambarkan kejadian dan tempat semakin detail semakin baik
- DATE CHECK dan sumber digeser ke bawah **bersamaan sebagai satu blok**, dengan margin kecil dari tepi bawah.

## CARA KERJA & VERIFIKASI
- Kerjakan sendiri di direktori kerja yang ditentukan.
- Lakukan audit 3× dengan urutan ini:
  1. **Geometri**: overflow, elemen keluar frame, text menimpa garis.
  2. **Semantik**: nomor 1..N muncul tepat sekali, warna region sesuai lokasi/legenda, nomor peta dan daftar cocok dengan beritanya, tidak ada kalimat terpotong, semua berita bertanggal bounty.
  3. **Ukur 300px**: resize ke 300×300, lalu ukur ukuran font tiap elemen setelah diskalakan. Jangan hanya mengandalkan "kelihatan terbaca" — lapork angkanya.
- Jika ada syarat yang tidak bisa dipenuhi atau ada konflik antar syarat, **tanya dulu**, jangan memutuskan sendiri.
- Push repo, perbarui bundle transcript, isi:about,deskripsi,readme.md lalu **tunggu persetujuan submit**.
- Laporkan hasil audit dalam bentuk tabel ringkas sebelum meminta izin submit.
- 
---

## Catatan untuk agent
Instruksi di atas adalah kontrak. Jangan mengganti jumlah berita, warna region, atau struktur kartu tanpa bertanya.
"Lega" berarti isi kartu ikut membesar, bukan sekadar kotaknya diperpanjang atau teks dipangkas.



# Spesifikasi peta — untuk bounty news-image apa pun

Blok generik ini disisipkan ke prompt bounty news-image tanggal berapa pun
(20261122, 20261123, …). Tidak menyebut entri atau versi tertentu.

---

## PETA ("WHERE IT HAPPENED")
Gambar panel peta dunia yang **realistis tetapi mudah dibaca sebagai indeks berita**.

### Data & proyeksi
- Gambar benua dari file GeoJSON Natural Earth (`world110.geojson`) yang tersedia di direktori kerja. Lewati Antarctica. Dilarang menggambar benua secara manual atau memakai bentuk perkiraan.
- Proyeksi equirectangular: `x = x0 + (lon+180)/360*lebar`, `y = y0 + (LAT_ATAS-lat)/(LAT_ATAS-LAT_BAWAH)*tinggi`, dengan `LAT_ATAS=83`, `LAT_BAWAH=-58`.
- Samudra `#D8E8F1`, daratan `#EADCB9`, garis pantai `#B8A175`, graticule tiap 30° warna `#C6DEEA`.
- Panel diberi judul **"WHERE IT HAPPENED"** dan pinggir halus.

### Titik, garis, nomor — prioritas utama
- **Titik lokasi**: lingkaran kecil (radius ≈2–3px pada kanvas 1024px) tepat pada koordinat lon/lat berita, diisi warna region, pinggir putih. Titik ini tidak boleh diganti atau ditutup oleh badge nomor.
- **Garis **: bila badge tidak bisa diletakkan tepat di titik, tarik garis tipis dari titik ke badge dan beri panah kecil di ujungnya, supaya jelas arah koordinatnya. Garis tidak boleh memotong teks, badge, atau garis lain.
- **Badge nomor**: lingkaran kecil (radius ≈6–7px), isi warna region, pinggir putih, nomor **terpusat di tengah** (pakai anchor `mm`; jangan `ma`, karena itu membuat angka keluar dari lingkaran).
- **Penempatan**: greedy — coba radius 0, 8, 15, 23, 32, 42px di sekitar titik; tolak kandidat yang jaraknya < `2*radius+3` dari badge lain. Offset maksimal dari titik ≈42px. Jika tidak ada ruang, perbesar panel atau perkecil badge — jangan biarkan badge bertumpuk, dan jangan memindahkan nomor ke laut hanya untuk menghindari tabrakan.
- Nomor 1..N muncul tepat sekali dan warnanya cocok dengan region berita di kartu/daftar.

### Warna 7 region (samakan dengan legenda di bagian atas gambar)
Eropa biru · Timur Tengah oranye · Afrika hijau · Asia merah · Amerika ungu · Oseania teal · World abu.

### Legenda & caption
- Letakkan legenda 7 region (warna + jumlah berita) di dalam panel peta.
- Caption kecil: "Each number is the story with that number on this page. Dots mark the exact place; line/garis join each dot to its number."

### Audit peta (laporkan dalam tabel)
1. Jumlah badge = jumlah berita; nomor 1..N tepat sekali.
2. Jarak minimum antar badge ≥ `2*radius` (tidak ada tumpang tindih).
3. Offset maksimum badge dari titik asal ≤42px.
4. Cek manual 5 koordinat: titik benar-benar pada lokasi berita.
5. Warna badge = warna region berita.
6. Nomor terbaca di tengah badge, tidak terpotong.
7. Peta realistis: garis pantai mengikuti GeoJSON, graticule terlihat.

---

## Catatan
Yang dinilai bukan keindahan benua, melainkan **keterbacaan koordinat**: pembaca harus bisa menunjuk titik, mengikuti panah, membaca nomor, lalu menemukan beritanya di daftar.
