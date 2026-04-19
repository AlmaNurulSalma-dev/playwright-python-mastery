# Module 1.4 — Essay Questions

> Jawab dengan bahasa kamu sendiri. Boleh mix Indonesian & English.

---

## Question 1 (Easy)

Jelaskan perbedaan antara "selector" dan "locator" di Playwright.

a. Apa itu selector? Berikan 3 contoh.
b. Apa itu locator? Apa yang membuatnya berbeda dari selector?
c. Sebutkan 3 keunggulan locator dibanding langsung pakai selector di action.

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. selector adalah kayak address nya suatu element gitu. elemen yg di target. untuk kasih tau ke playwright kita mau targetin element yg mana. contohnya kayak text=Submit, #username, dan placeholder=Email. dan lain sebagainya.

b. locator adalah object yg megang si selector. jadi kayak di assign ke dalam suatu variable. jadi dia reusable. btw a lil bit of fyi, si locator ini lazy, jadi dia ngga langsung cari element pas dibuat, dia baru cari element pas kita suruh dia untuk do something with that element. jadi bagus, efisien gitu.lebih stabil juga dia.

c. dia reusable, lazy, dan dia lebih readable dan lebih singkat juga syntaxnya, writable kah namanya?

---

## Question 2 (Medium)

Playwright merekomendasikan priority order untuk locator methods:
`get_by_role > get_by_label > get_by_placeholder > get_by_text > CSS > XPath`

a. Kenapa `get_by_role()` di-prioritaskan di atas CSS selector?
   Berikan contoh scenario dimana CSS selector break tapi get_by_role() tetap work.
b. Kapan kamu HARUS pakai CSS selector atau XPath meskipun ada get_by_ methods?
   Berikan 2 contoh.
c. Apa itu "locator strictness"? Kenapa Playwright throw error kalau 
   locator match lebih dari 1 element? Bagaimana cara handle-nya?

### Answer:
<!-- Tulis jawaban kamu di sini -->

a. karena dia readable, dan dia stabil, dikarenakan parameternya yg dipunya, lebih stabil jikalau misal ada perubahan tag atau apa gitu di css or html nya, maka dari itu dia lebih tahan terhadap perubahan yg ada di css or html. contoh css selector break tapi get_by_role() tetap work adalah ketika misal ada nama class atau id yg berubah, itu kan kalo css selector tu langsung break ya, karena dia parameternya ya nama id atau class salah satunya, nah kalo pake get_by_role() tu bisa lebih tahan, karena pakai parameter name elementnya, dan name tu lebih jarang berubah dibanding id ataupun class. trus contoh lainnya adalah misal mau bikin button login, itu bisa aja tag nya di html berupa button atau a, nah itu kalo pake css selector itu dia break, nah kalo pake get_by_role() masih aman dikarenakan parameter methodnya pakai name. btw xpath bisa juga kalo untuk mau complex text matching.

b. ketika elementnya ngga punya struktur label, text, atau role yg jelas, ketika mau cari element berdasar posisi atau struktur DOM, misal punya 10 div identik, nah itu mau pake nth misal, nah itu gabisa pake get_by method, trus juga kan css gabisa kayak nyari parent child kayak xpath, makanya gabisa pake get_by method, harus pake si xpath. contohnya adalah misal tadi beberapa tag html yg identik, nah itu harus misal by position kan, nah itu harus pake css selector. trus misal contoh lainnya adalah kita mau nargetin element a, atau tag a, yg dia merupakan child dari elemen2 diatasnya di hierarki html itu, nah itu gabisa pake get_by method, itu harus pakai xpath.

c. locator strictness adalah kondisi dimana playwright tidak mengizinkan locatornya untuk nargetin element yg punya lebih dari satu element identik didalam satu file html or css yg sama. playwright throw error id kondisi itu karena playwright tidak tau harus memproses element yg mana, karena kayak ambigu gitu. then cara handlenya adalah dengan pake .first, .last, atau nth, yg mana dia merujuk pada posisi elemen2 identik itu, jadi tetap merujuk ke satu elemen saja.
---

## Question 3 (Hard)

Kamu sedang scraping sebuah e-commerce website dengan HTML structure berikut:

```html
<div class="product-list">
  <div class="product">
    <h3 class="name">Laptop Pro X</h3>
    <span class="price">$999</span>
    <div class="tags">
      <span class="tag">electronics</span>
      <span class="tag">featured</span>
    </div>
    <button>Add to Cart</button>
  </div>
  <div class="product">
    <h3 class="name">Phone Ultra</h3>
    <span class="price">$599</span>
    <div class="tags">
      <span class="tag">electronics</span>
      <span class="tag">sale</span>
    </div>
    <button>Add to Cart</button>
  </div>
</div>
```

a. Tulis Playwright code untuk extract SEMUA products 
   (name, price, tags) ke list of dicts. 
   Gunakan locator chaining dan .all().
b. Tulis Playwright code untuk find product yang punya tag "sale" 
   menggunakan .filter(has=).
c. Tulis Playwright code untuk click "Add to Cart" pada product "Phone Ultra" 
   menggunakan chaining (find product by name, then find button inside it).
d. Kenapa `page.get_by_role("button", name="Add to Cart").click()` 
   akan ERROR di page ini? Bagaimana solusinya?

### Answer:
<!-- Tulis jawaban kamu di sini -->
a. jawaban:
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
   browser = p.chromium.launch()
   page = browser.new_page()
   page.goto(URL)

   list=[]
   product = page.locator(".product").all()
   for i in range(len(product)):
      name = product[i].locator(".name").text_content()
      price = product[i].locator(".price").text_content()
      tags = product[i].locator(".tag").all_text_contents()
      list.append({"name": name, "price": price, "tags": tags})
   browser.close()

b. jawaban:
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
   browser = p.chromium.launch()
   page = browser.new_page()
   tag_sale = page.locator(".product").filter(has=page.locator(".tags", has_text="sale"))
   browser.close()

c. jawaban:
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
   browser = p.chromium.launch()
   page = browser.new_page()
   product_phone = page.locator(".product").filter(has=page.locator(".name", has_text="Phone Ultra"))
   cart_phone = product_phone.locator("button")
   cart_phone.click()
   browser.close()

d. karena dia menargetkan elemen2 yg identik, bisa dilihat itu ada beberapa add to cart button, sehingga supaya tidak error, perlu untuk dilakukan spesifikasi posisinya, entah pakai .first, .last, atapun nth. atau bisa juga paaki cara filter by product name dulu, baru click button di dalamnya, seperti part C yg sudah ditulis codenya.
---