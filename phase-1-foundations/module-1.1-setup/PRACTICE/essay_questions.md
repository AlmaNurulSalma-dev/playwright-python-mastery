# Module 1.1 — Essay Questions

> Jawab dengan bahasa kamu sendiri. Boleh mix Indonesian & English.
> Tujuannya bukan hafalan — tapi buktikan kamu PAHAM konsepnya.

---

## Question 1 (Easy)

Jelaskan perbedaan antara `from playwright.sync_api import sync_playwright as p` 
dan `with sync_playwright() as p:`. 

Kenapa kita menggunakan `with` statement untuk Playwright? 
Apa yang terjadi kalau script kamu ERROR di tengah-tengah eksekusi 
dan kamu TIDAK menggunakan `with`? Berikan analogi real-world untuk menjelaskan.

### Answer:
<!-- Tulis jawaban kamu di sini -->
kalo `from playwright.sync_api import sync_playwright as p` itu hanya untuk rename nama library nya aja menjadi p.
nah kalo `with sync_playwright() as p:` itu dia untuk kayak ngebuka session gitu, jadi dia udah auto ngebuka dan auto close penggunaan lib dan modulenya itu selagi masih ada indentationnya di dalam with statement itu. pake with statement untuk library atau module yg butuh ada opening and closingnya gitu, nnti bisa di check lagi di documentation lib yg mau dipakai. kita menggunakan with statement untuk playwright karena dia butuh action untuk open or launch dan close or stop the browser kan. tidak menggunakan with statement juga bisa menyebabkan resource leak, jadi scriptnya tetap jalan sampai selesai, tapi browsernya tetap hidup di background, karena bisa jadi kita lupa write p.stop(), jadi chromium masih berjalan di background seperti yg tadi sudah dijelaskan. nah kan kalo pake with statement, dia udah ada auto cleanup dengan pakai p.stop() tadi itu, jadi lebih aman dan reliable dari human error juga. 

---

## Question 2 (Medium)

Playwright menyediakan 3 browser engines: Chromium, Firefox, dan WebKit.

a. Apa perbedaan antara Chromium dan Chrome? Kenapa Playwright bundle Chromium, 
   bukan Chrome?
b. Kenapa kemampuan menjalankan WebKit di Windows itu significant? 
   Apa masalah yang dipecahkan dibanding Selenium?
c. Kapan kamu akan menggunakan `channel="chrome"` instead of default Chromium? 
   Berikan satu contoh use case.

### Answer:
<!-- Tulis jawaban kamu di sini -->
a. kalo chrome tu dia bisa built in sync dengan google, dia lebih ada dan lebih banyak proprietary features nya dibanding chromium, chromium lack di bagian itu nya. trus terkait privacy, si chromium tu dia ngga nge track user's activity, sementara kalo chrome kan iya ya untuk ningkatin user experience juga. trus kalo dari sisi security nya, chrome tu udah ada built in nya gitu yg disediain, sementara kalo chromium harus configure it manually. chromium tu open source and free browser gitu. 

b. oke jadi for context, webkit kan engine browsernya safari ya, nah itu kan dipunya sama masoc/ios. so harusnya di windows gabisa jalan begitu aja, dia butuh namanya browser automation tools seperti selenium dan atau playwright. trus tapi kalo selenium tu gabisa buat macos/ios kalo misalnya selenium itu sendiri ngga berjalan diatas macos/ios. dia kayak harus ada configurationnya gitu lah, nah sementara kalo playwright, dia bisa easily access the webkit, jadi dia ga perlu vm nya macos gitu. nah kalo selenium tu cara kerjanya begitu karena dia ngebaca operating system device nya itu, so kalo device kita windows, tapi kita mau webkit, ya itu perlu vm atau semacamnya, which is ribet dibanding playwright yg bisa langsung nge bundles the actual of webkit engine, yg beda dibanding kalo dia berjalan diatas safari, itu tu v=cuma UI wrappernya, dan kalo dalam hal rendering, layout, javascript execution, itu sama kayak kalo di safari. jadi si webkitnya itu, dan dia cara kerjanya ga butuh safari sama sekali, tapi dia juga bukan persis safari, dia bikin versi webkit sendiri gitu, yg mirip kayak aslinya, so udah bisa kelihatan sebagian besar visual dan behavior spesifiknya safari. succintly, problem that has been solved by playwright is safari testing accessibility seperti yg tadi saya jelaskan.

c. dia pake channel="chrome" kalo misalnya butuh yang environment testing yg production-like, yg semirip mungkin dengan yg user gunakan, atau bisa juga pakai itu karena butuh proprietary features nya chrome yg gaada di chromium, atau kalau setup, itu ribet. biar mengurangi gap juga antara yg developer kerjain dengan chromium vs apa yg user lihat di chrome. contoh usecasenya setelah saya cari tau, itu ada beberapa proprietary features yg ada di chrome dan gaada di chromium seperti salah satunya widevine cdm (drm), itu adalah sistem proteksi untuk streaming platfrom kayak netflix gitu. dan tanpa drm ini, nnti web player gabisa play konten protected.

---

## Question 3 (Hard)

Kamu diminta membuat web scraper untuk perusahaan yang harus berjalan di server 
Linux tanpa GUI (no monitor, no display). Scraper ini harus:
- Berjalan otomatis setiap jam
- Secepat mungkin
- Tetap bisa di-debug ketika ada error
- Mengumpulkan data dari website yang tampilannya berbeda di mobile vs desktop

Berdasarkan apa yang kamu pelajari di Module 1.1, jelaskan:
a. Mode apa yang kamu pilih (headless/headful) dan kenapa?
b. Bagaimana strategi debugging kamu jika scraper error di production?
   (hint: pikirkan tentang screenshot, slow_mo, dan kapan switch mode)
c. Bagaimana cara kamu handle perbedaan tampilan mobile vs desktop? 
   Jelaskan approach-nya dan method/parameter apa yang dipakai.

### Answer:
<!-- Tulis jawaban kamu di sini -->
a. mode yg saya pilih adalah headless karena itu kan requirementnya ngga butuh di display, so headless aja, dan juga kalo headless tu speed nya lebih cepat, so untuk efisiensi waktu juga.

b. oke, saya barusan baca kalo kan tadi di nomor 3A, saya jawab pakai headless ya, dan headless=True ternyata masih bisa di screenshot karena rendering engine nya tetap aktif penuh, jadi tetap di screenshot untuk bisa memudahkan proses debugging. trus perlu pakai slow_mo, yg mana slow_mo digunakan untuk memberi jeda di setiap action yg dilakukan di automasi kegiatan scraping ini, misalnya action click, ketik, navigate, dan lainnya, jadi kayak dikasih delay gitu. dan di set durasi slow_mo nya menjadi nilai yg ideal berdasarkan use casenya, kalo most of the cases, biasanya durasi waktu nya 200-500 ms. and btw slow_mo ini, karena requirement kita di soal tu harus berjalan secepat mungkin, so dia bisa di set dengan tidak dipakai di semua kondisi, jadi by default gausa pakai slow_mo, itu hanya dipakai di proses debugging yg memang butuh sekali untuk melihat proses dengan durasi yg lebih lama atau pace yg lebih lambat. trus kalo misal dengan kedua cara tadi, yaitu screenshot dan slow_mo belum membantu, bisa di switch mode nya dari yg tadinya headless=True menjadi headless=False supaya bisa terlihat dengan jelas proses scrapingnya seperti apa supaya terlihat end to end prosesnya dan bisa lebi hmudah diketahui penyebab masalahnya apa.

c. yang pertama adalah harus tau dulu configuration devicenya, baik itu mobile ataupun deksop, trus bikin list yg isinya dictionary, yg mana masing-masing dictionary mengandung config untuk masing2 device, berarti in this case we need to make 2 dicts kan. trus ya biasa nge looping si list tadi, di dalam loop nya ada launch the browser, misal chromium, trus buat logical condition kayak if-else gitu, fungsinya untuk misal mana yang mobile dan mana yg desktop, dan untuk masing-masing device tadi, kita buat context berbeda, nah baru habis itu bikin new page untuk masing-masing contextnya. then arahin ke url web yg mau di scrape. gitu sih kurang lebih. oiya btw di list config yg untuk devices tadi, itu kan isinya dict, nah dict kan isinya key value gitu, nah itu disitu parameter2 nya ada device name, viewport nya apakah None apakah ada valuenya (width and height), trus devicenya, yg mana pake property dari playwright bernama .devices, atau bisa juga kalo devicenya None. a lil bit of fyi, property tu beda sama method, kalo method syntaxnya pake parentheses, kalo property ngga.


---