# Module 1.2 — Essay Questions

> Jawab dengan bahasa kamu sendiri. Boleh mix Indonesian & English.

---

## Question 1 (Easy)

Jelaskan 3-layer model Playwright (Browser → Context → Page) 
menggunakan analogi gedung apartment:

- Browser = ?
- Context = ?  
- Page = ?

Lalu jelaskan: apa yang "shared" dan apa yang "isolated" di tiap layer?
Kenapa design ini lebih efisien dibanding Selenium yang harus buka 
browser baru untuk setiap user session?

### Answer:
<!-- Tulis jawaban kamu di sini -->

oke jadi untuk browser sendiri, itu analoginya kayak gedung apartment nya, trus kalo context tu ibarat lantai apartmentnya, lantai 1, 2, 3, and so on. trus kalo page itu ibarat kamar atau ruangan apartment nya. jadi browser ni berisi context and page, yg mana tiap context tu akan ter-isolated dengan context yg lain, jadi ga punya misal kayak session atau cookie yg sama gitu. trus tapi kalo di dalam context yg sama, itu kan terdiri dari pages, nah pages ini saling shared gitu, misal shared cookie gitu. dan design browser-context-page di playwright ini lebih efisien daripada di selenium karena kalo di selenium tu gabisa bikin context, jadi kalo mau sesuatu yg isolated, itu harus bikin browser baru, which its heavy. untuk perbandingan, misal kalo di playwright tu dia untuk 10 users berbeda, dia kan masing-masing user harus terisolasi ya dari user lainnya, nah cukup bikin 1 browser saja, trus bikin 10 context berbeda, trus baru deh diisi page di masing-masing contextnya. nah sementara kalo selenium tu dengan case yg sama, dia membutuhkan 10 browser berbeda, ngga efisien sekali, dan pasti computing cost nya makan banyak dibanding kalo pakai playwright.

---

## Question 2 (Medium)

Perhatikan dua code snippet berikut:

**Snippet A:**
```python
browser = p.chromium.launch()
page1 = browser.new_page()
page2 = browser.new_page()
```

**Snippet B:**
```python
browser = p.chromium.launch()
context = browser.new_context()
page1 = context.new_page()
page2 = context.new_page()
```

a. Apa perbedaan antara Snippet A dan Snippet B?
   Berapa context yang tercipta di masing-masing snippet?
b. Di Snippet A, apakah page1 dan page2 share cookies? Kenapa?
c. Di Snippet B, apakah page1 dan page2 share cookies? Kenapa?
d. Kapan kamu akan pilih approach A vs approach B?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. di snippet A, itu dia membuat satu browser chromium dan 2 page. dan di snippet A kan ngga ada pembuatan new context secara eksplisit ya, tapi itu aslinya ada ngebuat dua context, bisa dilihat dari pembuatan new_page sebanyak 2 kali, yg mana berarti pembuatan context nya juga sebanyak 2 kali. jadi dia kayak shortcut gitu lah. nah trus kalo yang snippet B, dia bikin satu browser chromium, bikin satu context, dan 2 pages. nah kalo di snippet B ini dia secara eksplisit dibuat si contextnya.

b. tidak share cookies karena mereka ada di dua context yang berbeda.

c. share cookies karena mereka ada di satu context yang sama

d. akan pilih approach A jika memang hanya dibutuhkan satu context saja untuk keseluruhannya, jadi ya gaperlu yg dideklarasikan atau ditulis secara eksplisit. trus saya akan pilih approach B kalo di keseluruhan code nya kira-kira bakal ada lebih dari satu context. untuk code nya lebih readable. dan kalo mau yg auto isolated, bisa pakai yg snippet A, kalo yg shared cookies pakai yg approach B.

---

## Question 3 (Hard)

Kamu diminta membuat automation tool untuk sebuah e-commerce website yang perlu:
- Login sebagai admin DAN sebagai regular user BERSAMAAN
- Admin membuka dashboard (1 tab) dan halaman orders (1 tab)
- Regular user membuka homepage (1 tab) dan product page (1 tab)
- Kedua user TIDAK BOLEH saling interfere (cookies harus isolated)

a. Gambarkan hierarchy yang kamu akan buat 
   (berapa browser, berapa context, berapa page, dan apa isi masing-masing).
   Gunakan format tree seperti ini:

   Browser
   ├── Context: ???
   │   ├── Page: ???
   │   └── Page: ???
   └── Context: ???
      ├── Page: ???
      └── Page: ???

b. Kenapa kamu TIDAK bisa pakai `browser.new_page()` untuk semua 4 pages?
   Apa yang akan terjadi kalau kamu pakai itu?

c. Apakah kamu perlu menutup contexts secara explicit, 
   atau cukup `browser.close()` di akhir? Jelaskan trade-off nya.

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. berikut tree structure untuk arsitektur garis besarnya:
   Browser
   ├── Context: as admin
   │   ├── Page: dashboard page
   │   └── Page: order page
   ├── Context: as regular user
       ├── Page: homepage
       └── Page: product page
   
b. karena kan requirement case nya butuh 2 user, yaitu regular user and admin. karena itu kita butuh 2 context berbeda. dan bisa dengan .new_context() nya sebanyak 2 kali, dan harus eksplisit, kenapa? karena inside every context, kita punya 2 pages untuk masing-masingnya. so kalo bikin dengan call .new_page() sebanyak 4 kali, nnti terlalu isolated, padahal 2 pages di admin, perlu dalam satu isolasi yg sama, dan 2 pages regular user juga perlu dalam satu isolasi yg sama. di soal 3B essay ini ditanyakan kenapa tidak bisa pakai `browser.new_page()` untuk semua 4 pages, jawabannya karena kalo shortcut gitu modelnya, itu dia hanya akan bikin satu context saja per call bikin new page, sebetulnya bisa aja call new_page() sebanyak 4 kali, tapi tidak efisien dan kurang readable dibanding kalo langsung eksplisit new_context().

c. perlu tidaknya menutup context secara explicit actually depends on apa kebutuhannya. misal dia cuma punya satu context, yaudah gaperlu secara explicit dibilang si menutup context nya itu. cukup browser.close() aja karena dia udah auto nutup yang hierarki dibawahnya, which is nutup contexts dan pages juga. trus tapi kalo dia di satu browser ada beberapa context, itu bisa aja misal kita ada kebutuhan untuk nge close yang context1, tapi yg context2 belum mau, nah itu bisa ditulis secara explicit aja di kodenya. trus terkait memory, kalo ngga di declare explicitly, itu bakal boros memory semisal ada contexts yang sudah selesai dipakai tapi belum di close.

---