# Mars Recipes – دليل التثبيت على WordPress / Hostinger

## الخطوة 1 — نسخ ملفات الصور إلى القالب

قبل ضغط القالب، انسخ هذه الملفات من المجلد الجذر يدوياً:

```
من: C:\Users\Hp\OneDrive\Desktop\MyProject\marsrecipes claude code\
إلى: marsrecipes-theme\assets\images\
```

الملفات المطلوبة:
- favicon.ico
- favicon-16x16.png
- favicon-32x32.png
- favicon-192x192.png
- favicon-512x512.png
- apple-touch-icon.png

---

## الخطوة 2 — ضغط القالب كملف ZIP

1. افتح مجلد `marsrecipes claude code` في File Explorer
2. انقر بزر الماوس الأيمن على مجلد `marsrecipes-theme`
3. اختر **"Send to" ← "Compressed (zipped) folder"**
4. سيُنشأ ملف `marsrecipes-theme.zip` — هذا هو ملف القالب الجاهز للرفع

---

## الخطوة 3 — تثبيت WordPress على Hostinger

1. سجّل الدخول إلى **hPanel** على Hostinger
2. اذهب إلى **Websites ← Manage**
3. في قسم "Website", اضغط على **"Auto Installer"** أو **"WordPress"**
4. أدخل اسم الموقع والبريد الإلكتروني وكلمة المرور للأدمن
5. اضغط **Install** وانتظر اكتمال التثبيت

---

## الخطوة 4 — رفع القالب

1. اذهب إلى لوحة تحكم WordPress: `yourdomain.com/wp-admin`
2. من القائمة الجانبية: **Appearance ← Themes**
3. اضغط **Add New ← Upload Theme**
4. اختر ملف `marsrecipes-theme.zip`
5. اضغط **Install Now** ثم **Activate**

---

## الخطوة 5 — إعداد الروابط الدائمة (Permalinks)

هذه الخطوة مهمة جداً لكي تعمل روابط الوصفات بشكل صحيح:

1. اذهب إلى **Settings ← Permalinks**
2. اختر **"Post name"**: `/%postname%/`
3. اضغط **Save Changes**

---

## الخطوة 6 — إنشاء تصنيفات الوصفات

1. اذهب إلى **Recipes ← Categories** (ستجد "Recipes" في القائمة الجانبية)
2. أنشئ هذه التصنيفات بالـ Slug المحدد:

| الاسم         | Slug         |
|---------------|--------------|
| Chicken       | chicken      |
| Beef          | beef         |
| Seafood       | seafood      |
| Pasta         | pasta        |
| Quick Meals   | quick        |
| Vegetarian    | vegetarian   |

---

## الخطوة 7 — إضافة أول وصفة

1. اذهب إلى **Recipes ← Add New**
2. أدخل **عنوان الوصفة** في الحقل الرئيسي
3. في صندوق **Recipe Details** (أسفل الصفحة) أدخل:
   - Prep Time, Cook Time, Total Time (بالدقائق فقط مثل: `10`)
   - Servings, Calories, Difficulty (Easy/Medium/Hard)
   - Cuisine (مثل: Middle Eastern, American, Italian)
   - Ingredients: كل مكوّن في سطر منفصل
   - Instructions: كل خطوة في سطر منفصل
4. في صندوق **Nutrition** أدخل القيم الغذائية (اختياري)
5. في صندوق **Badge** اختر: Trending / Quick / Viral / New / Popular
6. في **Recipe Categories** (يمين الصفحة) اختر التصنيف المناسب
7. في **Featured Image** (يمين الصفحة) أضف صورة الوصفة
8. اضغط **Publish**

---

## الخطوة 8 — تثبيت Rank Math SEO

1. اذهب إلى **Plugins ← Add New**
2. ابحث عن `Rank Math SEO`
3. اضغط **Install** ثم **Activate**
4. اتبع معالج الإعداد (Setup Wizard)
5. في **Post Types** تأكد من تفعيل **Recipes**
6. الـ Schema (Recipe Schema) يُولَّد تلقائياً من بيانات الوصفة — لا تحتاج إعداداً إضافياً

---

## الخطوة 9 — إعداد الصفحة الرئيسية

1. اذهب إلى **Pages ← Add New**
2. أنشئ صفحة باسم "Home" وانشرها
3. اذهب إلى **Settings ← Reading**
4. اختر **"A static page"**
5. في **"Homepage"** اختر صفحة Home التي أنشأتها
6. اضغط **Save Changes**

القالب سيعرض تلقائياً `front-page.php` للصفحة الرئيسية، وهي تجلب الوصفات ديناميكياً من قاعدة البيانات.

---

## الخطوة 10 — رفع صور الوصفات

صور الوصفات الموجودة في مجلد `images/` هي ملفات PNG يمكن رفعها عبر:
- **Media ← Add New** في لوحة التحكم، ثم تعيينها كـ Featured Image لكل وصفة
- أو رفعها مباشرة عند إنشاء كل وصفة

---

## ملاحظات مهمة

### بحث الـ Overlay
شريط البحث الفوري يحتوي على قائمة الوصفات المُعرَّفة في الكود (15 وصفة). عند إضافة وصفات جديدة على WordPress، يمكنك إضافتها لاحقاً في ملف `assets/js/main.min.js` في مصفوفة `RECIPES`، أو الاعتماد على بحث WordPress الأصلي (الذي يعمل أيضاً عبر شريط البحث في `search.php`).

### الإصدار المقترح من الإضافات
- **Rank Math SEO** — مجاني، يدعم Recipe Schema
- **ShortPixel** أو **Imagify** — لضغط الصور
- **WP Super Cache** أو **W3 Total Cache** — للسرعة
- **UpdraftPlus** — للنسخ الاحتياطي

---

## هيكل ملفات القالب

```
marsrecipes-theme/
├── style.css              ← معلومات القالب (WordPress)
├── functions.php          ← إعدادات القالب، CPT، Meta Boxes، Scripts
├── header.php             ← الهيدر، التنقل، شريط البحث
├── footer.php             ← الفوتر، Newsletter، Cookie Consent
├── front-page.php         ← الصفحة الرئيسية
├── archive-recipe.php     ← أرشيف الوصفات (/recipes/)
├── single-recipe.php      ← صفحة الوصفة الفردية
├── page.php               ← صفحات WordPress العادية
├── search.php             ← نتائج البحث
├── 404.php                ← صفحة 404
├── index.php              ← القالب الاحتياطي
└── assets/
    ├── css/
    │   └── style.min.css  ← التصميم الكامل للموقع
    ├── js/
    │   └── main.min.js    ← كامل JavaScript
    └── images/
        ├── favicon.ico
        ├── favicon-16x16.png
        ├── favicon-32x32.png
        ├── favicon-192x192.png
        ├── favicon-512x512.png
        └── apple-touch-icon.png
```
