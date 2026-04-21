# Module 1.5 — Essay Questions

> Jawab dengan bahasa kamu sendiri. Boleh mix Indonesian & English.

---

## Question 1 (Easy)

Jelaskan perbedaan antara Python `assert` dan Playwright `expect()`.

a. Apa yang terjadi kalau element belum muncul saat `assert` dipanggil?
b. Apa yang terjadi kalau element belum muncul saat `expect()` dipanggil?
c. Berikan contoh scenario dimana `assert` gagal tapi `expect()` berhasil
   (untuk check yang sama).

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. kalo element belum muncul saat dipanggil, maka akan menghasilkan AssertionError

b. kalo element belum muncul saat expect dipanggil, maka akan memberikan ibaratnya kayak nilai False gitu, karena dia auto wait sampai element exist

c. contoh misal ada element yg ke load nya lama, ntah berat atau gimana, sehingga kalo pake assert, kan ga auto wait, dan dia sekali nyoba aja kan bahasanya, jadi langsung ada AssertionError. sementara kalo pakai expect(), itu karena dia sistemnya ada auto waitnya, maka dia bakal nunggu sampai timeout yg ditentukan, jadi bukan based on how much trial nya, tapi based on waktunya.
---

## Question 2 (Medium)

Playwright punya 3 jenis timeout: action, navigation, dan expect.

a. Jelaskan perbedaan ketiga timeout ini dan apa yang masing-masing kontrol.
b. Kenapa navigation timeout biasanya di-set lebih besar dari action timeout?
c. Gambarkan timeout hierarchy — kalau kamu set `set_default_timeout(10000)` 
   lalu `page.click(selector, timeout=3000)`, timeout mana yang dipakai? Kenapa?
d. Apa yang terjadi kalau kamu set timeout terlalu kecil (misal 500ms)? 
   Dan terlalu besar (misal 120000ms)?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. timeout action tu untuk dia hanya di declare dan hanya berlaku override per action, dia mengontrol click, fill, hover, check, type, etc. trus untuk timeout navigation, dia mengontrol goto, go back, go forward, dan reload. trus kalo timeout expect, dia mengatur semua timeout yg pakai expect assertions, yg mana itu dari function dari playwright juga.

b. karena untuk navigate, basically butuh waktu yg lebih banyak untuk nge load dibanding action.

c. timeout yg dipakai adalah yang 3000, karena timeout default bisa di override oleh timeout action.

d. nge set timeout terlalu kecil bisa menyebabkan flaky result, yaitu hasil yg rapuh nantinya, yang mana dikarenakan karena element belum ready sampai waktu yang ditentukan. trus kalo timeout terlalu besar, itu bisa tidak efisien dari segi waktu, selain itu, misal yg element truly doesnt exist, jadi kita perlu tunggu 120 detik sebelum tau ada error. so debugging jadi sangat lambat.

---

## Question 3 (Hard)

Kamu sedang membuat web scraper yang harus scrape 50 halaman produk 
dari sebuah e-commerce website. Website ini punya karakteristik:
- Halaman awal load cepat (1-2 detik)
- Product images load lambat (3-5 detik)  
- Harga di-load via AJAX setelah page load (1-3 detik)
- Kadang ada popup "Subscribe to newsletter" yang muncul setelah 5 detik
- Server kadang lambat dan butuh 10+ detik untuk respond

a. Jelaskan timeout strategy kamu:
   - set_default_timeout berapa dan kenapa?
   - set_default_navigation_timeout berapa dan kenapa?
   - expect timeout berapa dan kenapa?
b. Untuk harga yang di-load via AJAX, apakah kamu pakai `wait_for_timeout(3000)` 
   atau `expect(price_locator).to_be_visible()`? Jelaskan kenapa.
c. Untuk popup newsletter, bagaimana kamu handle-nya? 
   (hint: apakah kamu wait for it, atau handle kalau muncul?)
d. Kalau total scraping 50 halaman butuh terlalu lama, 
   apa yang bisa kamu optimize dari sisi waiting/timeout?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. set default timeoutnya 4 detik, karena itu average dari keterangan durasi sesuai pada soal kan adalah 3, sementara misal dia ajaxnya butuh 3.1 detik, nah yaudah jadi thresholdnya kita set jadi 4 detik aja. ambil nilai tengahnya. untuk default navigation timeoutnya 13 detik, karena itu waktu yg aman untuk bisa handle goto untuk navigation itu kan. trus untuk expect timeout, mungkin 5 detik, karena di keterangan soal, kan ada popup yang kadang-kadang muncul, sehingga itu butuh pakai expect untuk check apakah popup nya keluar atau nggak.

b. karena dia ajax, so aku bakal pilih yang expect, karena misal ajax nya bisa ke load lebih cepat daripada waktu yang ditentukan, kalo pakai expect kan bisa langsung diproses gitu kan ke step selanjutnya, nah kalo yang wait_for_timeout, itu misal ajax nya udah ke load dari sebelum timeout nya habis, nah itu bakal tidak efisien waktu.

c. untuk popup newsletter, karena keterangan di soalnya adalah dia munculnya kadang-kadang, maka better untuk pake yang expect aja. bisa pakai try except, try pake expect, dan except nya adalah jangan dikasih AssertionError, tapi kayak yaudah dibiarin aja untuk next step scraping webnya. jadi kayak ga terjadi apa-apa.

d. timeout nya di optimize dengan cara set default yang tepat, jangan kelebihan. trus hanya use wait_for_timeout() seminimal mungkin hanya ketika dibutuhkan, karena dia bisa lumayan makan waktu, karena dia time-based, beda sama expect yang juga ada faktor nge check sampe conditionnya True. dan kalo mengingat konsep wait_until, itu kan mau scraping text ya, jadi sudah cukup harusnya hanya sampai tahap domcontentload nah itu bisa pake parameter tersebut nya itu untuk efisiensi juga dengan metrics yang lebih pasti.

---