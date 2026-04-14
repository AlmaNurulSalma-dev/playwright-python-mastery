# Module 1.3 — Essay Questions

> Jawab dengan bahasa kamu sendiri. Boleh mix Indonesian & English.

---

## Question 1 (Easy)

Jelaskan perbedaan antara `page.fill()` dan `page.type()`.

a. Bagaimana cara kerja masing-masing di balik layar?
b. Berikan 2 contoh real-world scenario dimana kamu HARUS pakai `type()` 
   instead of `fill()`.
c. Kenapa `fill()` lebih baik dari Selenium's `send_keys()` untuk form filling?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. cara kerjanya tu kalo page.fill() dia auto ngisi keseluruhan element yg mau diisi, kayak instant gitu, and .fill() itu lebih faster dan reliable. biasa dipakai untuk yang normal form filling gitu. kalo page.type() tu kayak ada effect ngetiknya, jadi ada delay misal 100 ms atau gimana. trus dia ngetik one character at a time. jadi web nya itu nge react for each character yg ditulis atau diketik itu. contoh pemakaiannya misal di google search, atau bisa juga di seberapa panjang length character dari suatu caption di post social media misal, atau bisa juga untuk kayak mau ngetik username, tapi dia harus unique gitu kan, nah kalo unique, nnti bakal ngehasilin misal "username available!", nah itu juga perlu pakai .type().

b. pakai type() kalo misal mau post di social media, mau bikin caption di suatu post, let say maximum characternya adalah 500 character, nah itu kalo pake .fill() nnti dia ke count characternya susah, karena dia auto ada gitu kan, jadi better pakai .type(). kalo udah reach angka maximumnya, dia auto ada warning gitu ke user.

c. kalau playwright's .fill() tu dia udah auto nge delete value sebelumnya kalo misal ada value, sementara kalo selenium tu dia send_key() nya ngga begitu, dia lebih ke nambah aja, ngga ada auto delete value, so harus manual nambahin .clear().

---

## Question 2 (Medium)

Kamu sedang scraping sebuah website dan menggunakan `page.goto(url)`.

a. Jelaskan 4 pilihan `wait_until` dan urutkan dari tercepat ke terlambat.
b. Kamu scraping website berita yang load articles via AJAX setelah page load. 
   `wait_until` mana yang kamu pilih dan kenapa?
c. Kamu scraping static HTML site (seperti quotes.toscrape.com) dan butuh speed. 
   `wait_until` mana yang kamu pilih dan kenapa?
d. Apa resikonya kalau selalu pakai `networkidle` untuk semua website?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. urutan dari tercepat ke terlambat ada commit, domcontentload (document object model), load, dan networkidle. berikut penjelasannya: pertama ada commit, dia menerima request yang dikirim, biasanya dia cepet banget, yg mana nandain kalo misal udah di received lah requestnya. trus yg kedua ada domcontentload, yg mana dom adalah singkatan dari document object model. jadi misal kan di web kita ngelihatnya html file, nah itu kalo mau scraping, itu data misal class atau id di html, itu computer bukan ngebacanya sebagai html, tapi kayak di convert jadi format dom dulu, kurang lebih kayak json structure gitu, kayak nested. tapi disini hanya html codenya aja yg di convert ke dom, yg mana itu belum include hal-hal resource kayak images, css, dll nah trus wait_until yang ketiga adalah load, kalo tadi di domcontentload dia belum include hal-hal kayak images, dll. nah disini, di load, itu dia nge unduh tu images dll nya. trus yang keempat ada networkidle, yg mana itu dia nunggu sampai 500 ms(default) untuk sampai ngga menerima request apapun, yg menandakan udah selesai prosesnya.

b. oke sebelum itu, mungkin saya akan jelaskan dulu apa itu AJAX, ajax tu adalah asynchronous javascript and xml. yg mana dia teknik untuk nerima dan ngirim data dari server tanpa perlu reload. misal di instagram, kita scroll nih kebawah, muncul tu post baru, tapi halamannya ngga ke reload, nah itu namanya ajax. lalu untuk wait_until yg saya pilih berdasarkan case pada soal adalah networkidle, karena untuk ajax, kan dia perlu dom format untuk scraping dan resources, so udah otomatis dia perlu wait_until yang commit, domcontentload, dan load. trus yaudah last option is networkidle.

c. karena dia static html, dan dia butuh speed, so saya pilih yang domcontentload karena kalau commit kan belum di convert jadi dom format, sehingga gabisa di scrape, so yg paling cepat dan paling mungkin untuk di scrape adalah kalo wait_until nya domcontentload

d. resikonya lama, dia makan waktu, karena default time 500 ms yg saya bilang diawal itu udah gabisa diganti sama kita, itu udah configuration playwright dari sananya. jadi ga efisien waktu, apalagi ngga di semua case tu kita perlu wait_until sampe yg networkidle. oh iya, dan ada resiko lain lagi yaitu real-time polling, nah kan tadi default by playwright nya kan durasi untuk nunggu networkidle tu 500 ms, tapi misal ada case yg dia ngirim request terus2 an tiap ms yg kurang dari 500, nah itu bisa aja requestnya berdatangan terus jadi networkidle ngga selesai2.
---

## Question 3 (Hard)

Bandingkan workflow Selenium vs Playwright untuk scenario berikut:
Kamu harus login ke sebuah website, lalu select sebuah dropdown option,
check sebuah checkbox, hover over sebuah element untuk reveal hidden text,
lalu press Enter untuk submit.

a. Tulis pseudocode (bukan real code, tapi langkah-langkahnya) 
   untuk Selenium DAN Playwright. Tunjukkan berapa banyak imports yang dibutuhkan 
   dan berapa lines of code untuk masing-masing.
b. Playwright punya "actionability checks" sebelum setiap action 
   (visible, stable, enabled, receives events). 
   Jelaskan kenapa ini menghilangkan kebutuhan explicit waits yang 
   harus kamu tulis di Selenium.
c. Checkbox di Selenium menggunakan `click()` yang bersifat toggle. 
   Jelaskan scenario dimana ini bisa menyebabkan bug, 
   dan kenapa Playwright's `check()`/`uncheck()` lebih safe.

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. oke pertama mungkin mulai dari dropdown dulu ya, berikut kalo dropdown di selenium: `Select(element).select_by_value("2")`, dibanding kalo yang di playwright seperti ini: `page.select_option("select", value="2")`. itu bisa dilihat kan bahwa yg playwright lebih jelas parameternya, lebih clear, terstruktur, dan lebih readable. oke trus sekarang kita bahas yang checkboxes, kalo di selenium tu pakenya .click(), yg mana dia sistemnya tu bisa sekalian buat check atau uncheck the box. jadi gini, kalo box nya sebelumnya ke checked, trus kita kasih .click(), nah itu dia bakal ke uncheck. trus kalo sebelumnya ke unchecked, dan kita kasih .click(), itu dia bakal ke check, which itu dia sistemnya kayak toggle gitu, dan dia dangerous. trus move on to hover, kalo di selenium begini: `ActionChains(driver).move_to_element(element).perform()`, sedangkan kalau di playwright begini: page.hover(selector). beda banget kan dari syntaxnya aja, kalo yg selenium jauh lebih panjang, sedangkan yg playwright lebih efisien. untuk pseudocode nya, kalo yg selenium tu kan login, trus ada dropdown, nah di dropdown tu, kalo selenium perlu udah ada elemennya dulu, sesuai sama parameter di codenya, trus checkbox, itu perlu ada logical condition kayak if-else gitu untuk make sure itu bawaan tiap web nya, itu checkbox nya by default ke check atau uncheck. trus lakuin action sesuai kebutuhan casenya. trus hover di selenium tu kan syntaxnya seperti yg sudah saya tulis diatas, yg mana dia perlu hover mouse ke sebuah element, trus perlu nyusun aksinya, dan perlu nentuin targetnya, habis itu perlu pakai .perform() untuk eksekusi itu. habis itu baru deh di enter. nah kalo misal di playwright begini: kan login tu, dia awalnya login, trus ada dropdown kan, nah trus cukup hanya pakai .select_option() dengan parameter mana yg mau di hover dan value nya, trus abis itu untuk checkbox, dia tinggal pake .check() aja untuk check ataupun unchecked, trus untuk hover dia tinggal pakai .hover(selector) aja. yg mana playwright line codenya jauh lebih sedikit dibanding selenium, trus juga proses coding nya juga lebih efisien, lebih mudah di debug, dan meminimalisir resiko unreliability dari suatu sistem. trus untuk angka imports yg dibutuhkan playwright hanya 1, yaitu import playwrightnya aja, sedangkan kalau selenium perlu import seleniumnya sendiri, trus ada webdriver, by, select, actionchains, keys, webdriverwait, expected_conditions, which total ada 8 imports.

b. karena playwright tu sistemnya auto wait si element untuk ready before acting, sedangkan di selenium tidak ada hal seperti itu. di selenium, itu harus banyak import2 untuk bisa make sure element itu ready, sehingga bisa kita interaksi dengan elemen2 itu. ada 4 elemen yg di mention di soal, yg mana elemen2 tersebut merupakan metrics pengecekan gitu lah, elemen2 tersebut yaitu visible, stable, enabled, dan receives events. lets deep dive into it. pertama ada visible, yakni element udah muncul di halaman. trus ada stable, yakni elemen udah ngga bergerak, misal ada animasi slide in, nah itu playwright nunggu sampai element yg dikenai animasi tersebut tuh sampe berhenti dulu. trus ada enabled, yakni element yg ga disabled, karna ga mungkin playwright klik element yg di disabled. trus terakhir ada receives events, yakni element yg ga ketutupan element lain. jadi kalo ada overlay atau modal nutupin, itu playwright gabisa asal klik.

c. `.click()` untuk check and uncheck di selenium rawan menyebabkan bug, karena misal kan kondisi checkbox di web macem2 ya, ada web yg emang udah kasih checked untuk boxnya, ada juga yg belum, nah kondisi itu yg bikin hasil dari `.click()` yg dipunya selenium tu ga pasti dan ngga bisa dikontrol oleh developer. karena sistem togglenya itu kan. itu sangat bergantung ke gimana web yg di scraping. di lain sisi, ada playwright's `check()` dan `uncheck()` yg gimanapun kondisi checkbox di webnya, itu kalo pake `check()` maka bakal tetep ke checked boxnya, dan kalo pake `uncheck()` maka bakal tetep ke unchecked boxnya.

---