# Module 2.1 — Essay Questions

> Jawab dengan bahasa kamu sendiri. Boleh mix Indonesian & English.

---

## Question 1 (Easy)

Jelaskan perbedaan antara 5 text extraction methods di Playwright:
`text_content()`, `inner_text()`, `inner_html()`, `input_value()`, dan `all_text_contents()`.

a. 

b. Kenapa `text_content()` pada `<input>` element return string kosong?
   Method mana yang harus dipakai?
c. Kapan kamu pakai `all_text_contents()` instead of loop manual dengan
   `text_content()` satu-satu?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. 
textContent() — Raw text including hidden (display: none)

Best for: Extracting semua text (visible + hidden)
Include whitespace & newlines


innerText() — Only visible text (rendered)

Best for: Text seperti yang dilihat user
Respect CSS rendering


innerHtml() — HTML markup (bukan text!)

Best for: Parse kompleks dengan cheerio/jsdom
Return string HTML


inputValue() — <input> & <textarea> values ONLY

Best for: Form fields, hidden inputs
HARUS untuk extract dari input!


allTextContents() — Array dari multiple elements

Best for: Batch extraction (10+ items)
10-40x lebih cepat dari loop manual

b. karena value nya ada di attribute, bukan di antara tag nya gitu. jadi gabisa ngambil valuenya. 

c. selalu pakai all_text_contents() untuk multiple elements. Gunakan manual loop HANYA kalau perlu logic kompleks per-item. Untuk extract pure text? allTextContents() always wins.

---

## Question 2 (Medium)

Kamu sedang scraping sebuah website dan menemukan HTML berikut:

```html

  
    
    Super Laptop Pro...
  
  $1104.99
  

```

a. Kamu mau dapetin nama produk LENGKAP. Apakah kamu pakai
   `.locator(".name").text_content()` atau `.locator("a").get_attribute("title")`?
   Kenapa?
b. Kamu mau dapetin harga asli sebelum diskon. Dari mana kamu extract-nya?
   Tulis code Playwright-nya.
c. Rating "Four" tersimpan di CSS class. Tulis code untuk extract
   rating dan convert ke angka.
d. Sebutkan SEMUA data yang bisa kamu extract dari HTML ini
   menggunakan `get_attribute()`. Minimal 8 attributes.

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. pakai yang `.locator("a").get_attribute("title")` karena lebih tahan terhadap perubahan id html nya. jadi sistem scrapingnya bisa lebih robust. dan html juga menampilkan text truncated dengan "..." (text-overflow: ellipsis). Teks lengkap ada di title attribute.

b. Harga asli ada di `data-original` attribute dari `.price` span, bukan di `<s>` tag (tidak ada di HTML soal).

```python
original_price = page.locator(".price").get_attribute("data-original")
# → "1299.99"
```

c. Tidak ada `data-rating` di HTML soal — rating tersimpan di CSS class `"star-rating Four"`. Parse class-nya:

```python
rating_class = page.locator(".star-rating").get_attribute("class")
rating_word = rating_class.split(" ")[-1]  # → "Four"
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
rating_num = rating_map[rating_word]  # → 4
```

d. Attributes yang benar-benar ada di HTML soal (tidak boleh mengarang):

- Dari `div.product-card`: `class`, `data-product-id`, `data-category`
- Dari `a`: `href`, `title`
- Dari `span.price`: `class`, `data-original`, `data-discount`
- Dari `span.star-rating`: `class`

Yang **tidak** ada: `data-rating`, `data-sku`, `id` — jangan include kalau tidak ada di HTML.
---

## Question 3 (Hard)

Kamu diminta memilih antara Playwright methods vs `page.evaluate()` (JavaScript)
untuk berbagai extraction tasks.

a. Untuk setiap task berikut, jelaskan apakah kamu pakai Playwright method
   atau evaluate(), dan kenapa:
   1. Mengambil text dari `<span class="price">$29.99</span>`
   2. Mengambil warna background sebuah element (computed CSS)
   3. Mengambil data dari `window.__NEXT_DATA__` (JS variable di halaman)
   4. Menghitung jumlah element `.product` di halaman
   5. Scroll ke bawah halaman 1000 pixel

b. Tulis contoh code `page.evaluate()` yang extract structured data
   (nama + harga) dari multiple `.product` elements sekaligus,
   dan jelaskan kenapa ini bisa lebih CEPAT dibanding
   loop Playwright locator satu-satu.

c. Apa resiko/kelemahan terlalu bergantung pada `evaluate()`
   dibanding Playwright methods? Sebutkan 2 resiko.

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. 

1. Mengambil text dari <span class="price">$29.99</span>
Pilihan: Playwright method (locator().textContent())
javascriptconst price = await page.locator('span.price').textContent();
Kenapa:

Simple text extraction → Playwright built-in sudah cukup
Tidak perlu JavaScript complexity
Lebih readable dan maintainable


2. Mengambil warna background (computed CSS)
Pilihan: page.evaluate()
javascriptconst bgColor = await page.evaluate(() => {
  return window.getComputedStyle(document.querySelector('.element')).backgroundColor;
});
Kenapa:

Computed CSS memerlukan getComputedStyle() (JavaScript API)
Playwright locators tidak bisa langsung akses computed styles
evaluate() paling praktis untuk browser-native APIs


3. Mengambil data dari window.__NEXT_DATA__
Pilihan: page.evaluate()
javascriptconst nextData = await page.evaluate(() => {
  return window.__NEXT_DATA__;
});
Kenapa:

Variabel global JavaScript hanya accessible via evaluate()
Ini adalah common pattern untuk Next.js SSR data extraction
Playwright methods tidak bisa reach ke window object


4. Menghitung jumlah element .product
Pilihan: Playwright method (locator().count())
javascriptconst count = await page.locator('.product').count();
Kenapa:

Counting adalah DOM operation sederhana
Playwright built-in method dedicated untuk ini
Tidak perlu evaluate overhead


5. Scroll ke bawah 1000 pixel
Pilihan: Playwright method (page.evaluate() OR page.mouse.wheel())
javascript// Option 1: Direct evaluation
await page.evaluate(() => {
  window.scrollBy(0, 1000);
});

// Option 2: Playwright mouse wheel (lebih ekspresif)
await page.mouse.wheel(0, 1000);
Kenapa:

Scroll adalah action yang butuh JavaScript
Keduanya valid, tapi page.mouse.wheel() lebih semantic
evaluate() juga OK kalau prefer explicit control

b. const products = await page.evaluate(() => {
  // Extract ALL products sekaligus di dalam JavaScript context
  return Array.from(document.querySelectorAll('.product')).map(element => ({
    name: element.querySelector('.product-name')?.textContent?.trim(),
    price: element.querySelector('.product-price')?.textContent?.trim(),
    url: element.querySelector('a')?.href,
  }));
});

console.log(products);
// Output:
// [
//   { name: 'Laptop Pro', price: '$999.99', url: '...' },
//   { name: 'Mouse', price: '$29.99', url: '...' },
//   { name: 'Keyboard', price: '$79.99', url: '...' }
// ]



c. Resiko #1: Read-Only, Tidak Ada Interaction

evaluate() hanya bisa extract data, tidak bisa click/fill/scroll
Kalau butuh trigger event (misal: "Load More" button), harus pakai Playwright methods dulu
Risiko: Extract data sebelum async loading selesai

Resiko #2: Silent Failures & Brittle Selectors

Kalau selector salah, tidak ada error — cuma return empty string
Tidak ada validation bahwa data benar-benar ada
Testing & debugging jadi susah (error terjadi di browser context)

---