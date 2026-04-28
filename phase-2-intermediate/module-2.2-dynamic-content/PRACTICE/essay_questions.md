# Module 2.2 — Essay Questions

> Jawab dengan bahasa kamu sendiri. Boleh mix Indonesian & English.

---

## Question 1 (Easy)

Jelaskan perbedaan antara 4 state di `wait_for_selector()`:
`attached`, `detached`, `visible`, `hidden`.

a. Untuk masing-masing state, berikan contoh real-world scenario
   dimana kamu akan menggunakannya.
b. Sebuah element ada di HTML tapi punya `style="display:none"`.
   State mana yang PASS dan mana yang FAIL untuk element ini?
c. Kenapa `state="visible"` lebih aman dibanding `state="attached"`
   untuk scraping? Berikan contoh dimana `attached` bisa menyebabkan
   data kosong.

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. ya jadi ada 4 state di wait_for_selector(), yaitu attached, detached, visible, dan hidden. nah pertama attached, dia tu default nya, trus dia wait untul element exist in document object model (DOM), dia biasanya dipakai untuk waiting for JS to create an element. yang kedua ada detached, dia kebalikannya dari attached, yg mana dia wait until element is removed from DOM, dia biasanya dipakai misal ketika ada modal ditutup dengan element2 nya dihapus dari html. trus yang ketiga ada visible, yg dia wait until element is visible on screen, dia must exist and not be hidden, dan dia digunakan untuk waiting for content to show after loading. trus terakhir ada hidden, dia wait until element is hidden or removed, use for waiting for spinner / loader to disappear.

b. yang pass adalah attached dan hidden. sementara yang fail adalah yang visible dan detached.

c. karena kalo attached, dia bisa aja elemennta hidden, and it doesnt matter, karena itulah dia lebih ngga aman dibanding state visible. contohnya ya tadi misal di dom nya element nya di hide, so itu attached masi keliatan, sementara kalo di visible udah ngga keliatan. 

---

## Question 2 (Medium)

Kamu punya 6 wait strategies: auto-wait, wait_for_selector, wait_for_url,
wait_for_load_state, wait_for_function, dan expect_response.

a. Untuk setiap scenario berikut, pilih wait strategy yang PALING TEPAT
   dan jelaskan kenapa:
   1. Kamu click tombol dan halaman redirect ke URL baru
   2. Kamu click "Load More" dan 10 product baru muncul di bawah
   3. Kamu mau ambil data JSON dari API response langsung
   4. Website punya loading spinner yang hilang setelah data loaded
   5. Kamu mau pastikan semua AJAX calls selesai sebelum scraping

b. Kenapa `wait_for_timeout(3000)` adalah pilihan TERBURUK
   untuk hampir semua scenario di atas?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. 1 = wait_for_url() karena dia ada aktivitas penggantian url dan harus memastikan kalo url nya juga berubah menjadi url baru. 2 = wait_for_selector, karena dia harus click load more button dulu kan itu. 3 = expect_response karena perlu response API. 4 = wait_for_selector dengan state hidden. 5 = wait_for_load_state("networkidle")

b. karena misal timeoutnya udah habis 3000, nah itu dia ngga ngelakuin apa-apa. buruknya dari itu apa? yaitu kalo data ready dalam 0.5 detik, nah itu buang2 waktu 2.5 detik sisanya, boros waktu.

---

## Question 3 (Hard)

Kamu diminta scrape sebuah SPA (Single Page Application) e-commerce
yang punya karakteristik:
- Products di-load via fetch("/api/products?page=1")
- Infinite scroll (scroll down → load more products)
- Setiap product punya tombol "Quick View" yang buka modal via AJAX
- Modal contains detailed info (specs, reviews, price history)
- Loading spinner appears during AJAX calls

a. Gambarkan scraping flow/strategy kamu step by step.
   Sebutkan wait method yang kamu pakai di setiap step.

b. Untuk infinite scroll, tulis pseudocode yang handle:
   - Scroll sampai semua products loaded
   - Detect kapan harus stop scrolling
   - Handle case dimana scroll stuck (no new items for 3 attempts)

c. Untuk "Quick View" modal, apakah kamu:
   - Option A: Click button → wait for modal → scrape HTML dari modal
   - Option B: Catch fetch response → langsung ambil JSON data
   Pilih satu dan jelaskan kenapa lebih baik.

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. jadi pertama pakai wait_for_load_state("networkidle") untuk initial page load dulu kan, dia harus tunggu sampai semua requests selesai, dengan default time nya 500 ms. trus habis itu pakai wait_for_selector dengan state visible untuk check visibility product di layar. trus kemudian pakai wait_for_function untuk count items via JS. kemudian pakai expect_response() untuk ajax. 

more detail:
STEP 1: Initialize Page
  ├─ page.goto("https://ecommerce.example.com")
  ├─ Wait method: wait_for_load_state("networkidle")
  └─ Reason: Tunggu semua initial requests + resources selesai

STEP 2: Check Initial Products Loaded
  ├─ Action: (products sudah di-load via API pada step 1)
  ├─ Wait method: wait_for_selector(".product-item", state="visible")
  └─ Reason: Tunggu sampai produk visible di layar, siap di-scrape

STEP 3: Setup Network Listener (for infinite scroll detection)
  ├─ Action: page.on("response", handler) untuk track API calls
  ├─ Wait method: (event-driven, tidak perlu explicit wait)
  └─ Reason: Setiap kali API respond, listener capture data otomatis

STEP 4: Infinite Scroll Loop
  ├─ Repeat:
  │  ├─ Scroll: page.evaluate("window.scrollBy(0, window.innerHeight * 2)")
  │  ├─ Wait method: expect_response("**/api/products")
  │  │  └─ Reason: Tunggu API response datang setelah scroll trigger
  │  ├─ Check: Listener callback count products
  │  ├─ If no new products × 3 times: BREAK
  │  └─ Else: Loop again
  └─ Exit: When reached bottom (no new products)

STEP 5: For Each Product → Quick View Modal
  ├─ Action: page.click("[data-product-id] .quick-view-btn")
  ├─ Setup: before click, setup with page.expect_response("**/api/products/[id]")
  ├─ Wait method: expect_response (capture API response)
  └─ Reason: Get complete JSON (specs, reviews, priceHistory) directly
  
STEP 6: Extract Data
  ├─ Source: API response.json() (dari expect_response)
  ├─ Data: specs, reviews, price, priceHistory
  └─ No need to wait for modal rendering or parse HTML

b. Untuk handle infinite scroll yang robust, pertama setup network listener SEBELUM scroll loop dimulai. Listener callback akan track setiap API response dari /api/products dan accumulate products ke list. Ketika ada response dengan products kosong atau tidak ada response sama sekali, increment counter untuk no-new-items. Main loop struktur-nya adalah: scroll action → wait untuk API response dengan timeout 3000ms → check apakah product count bertambah → decide apakah lanjut scroll atau stop.
Ada tiga stop conditions yang harus di-handle:

No new items 3 times: Jika 3 consecutive scroll attempts tidak menghasilkan produk baru, berarti kita sudah reach bottom of the page.
5 consecutive timeouts: Jika API tidak respond 5 kali berturut-turut, network probably stuck atau server error, jadi break loop untuk avoid infinite waiting.
Max pages limit: Safety limit (misalnya 100 pages) untuk prevent accidental infinite loops.

Counter reset logic penting: setiap kali ada new products dari API, reset no_new_items_count ke 0 dan juga reset consecutive_timeouts. Ini distinction antara "API responded tapi empty" (no new items +1) vs "API tidak respond" (timeout +1). Dengan logic ini, scraper akan robustly handle network hiccups, slow servers, atau memang sudah reach end of products.

c. Jawabannya adalah Option B karena jauh lebih baik dari berbagai perspektif. Pertama soal timing: Option A memerlukan wait_for_selector(".modal.show", state="visible") untuk tunggu sampai modal muncul, tapi bahkan setelah modal visible, data mungkin belum fully rendered di HTML. Ini perlu arbitary extra wait dengan wait_for_timeout(300) untuk handle CSS animation lag, yang membuat timing tidak reliable. Sebaliknya, Option B menggunakan expect_response() untuk capture exact moment API respond — tidak ada guesswork tentang timing, response datang = data ready, langsung di-parse sebagai JSON.
Kedua soal data completeness: HTML yang di-render di modal hanya show sebagian data. Misalnya reviews hanya tampil 3 yang pertama dengan "Load more" button, berarti harus AJAX lagi untuk get semua reviews. Lebih parah lagi, price history sama sekali tidak ada di HTML — informasi itu hanya di API response. Sebaliknya, API response JSON punya semua data: specs lengkap, reviews semua (tidak truncated), dan priceHistory complete. Jadi Option A = incomplete data, Option B = complete data.
Ketiga soal scalability dan maintainability: Option A slow karena serial execution — click, wait modal visible, wait timeout, scrape, close, repeat untuk setiap 100 products ≈ 60 detik. Option B setup listener bisa parallel dengan Promise.all() untuk click multiple products sekaligus, ambil responses dalam batch — 100 products bisa done dalam 2-3 detik. Plus, Option B lebih robust karena depend pada API contract (jarang berubah) bukan HTML structure (sering berubah). Jika frontend developer ubah CSS class atau HTML layout, Option A scraper langsung break dan butuh rewrite. Option B tetap work karena JSON structure stable di backend.
Jadi kesimpulannya: Option B lebih baik karena tidak ada arbitrary timing, data complete, 30× lebih cepat, dan maintainable — API response adalah single source of truth, bukan rendering artifact dari HTML.
---