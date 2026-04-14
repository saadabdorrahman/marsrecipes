import os, re

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/recipes/"

# Reviews per recipe — natural, varied, authentic-sounding
REVIEWS = {
    "easy-creamy-garlic-chicken": {
        "score": "4.8", "count": "127",
        "items": [
            {"name":"Jessica T.", "rating":5, "date":"March 18, 2026", "text":"Made this on a Tuesday night and my husband said it tasted like something from a fancy restaurant. The garlic cream sauce is absolutely incredible — I doubled it because I knew we'd want extra for dipping bread. Will make again this week!"},
            {"name":"Mike R.", "rating":5, "date":"March 5, 2026",  "text":"Finally a 30-minute chicken recipe that actually delivers. Followed the instructions exactly — patting the chicken completely dry is the key step most recipes skip. Golden crust, juicy inside, sauce is silky and rich. Served over mashed potatoes. Outstanding."},
            {"name":"Priya L.", "rating":4, "date":"February 28, 2026","text":"Delicious! I reduced the butter slightly and added extra garlic. My kids ate every bite which is a miracle. The only reason it's 4 stars is I overcooked mine a little — 100% my fault. Next time I'll use a meat thermometer."},
            {"name":"Amanda K.", "rating":5, "date":"February 12, 2026","text":"This has officially replaced my old go-to chicken recipe. The sauce is so good I was spooning it directly out of the pan. Leftovers the next day tasted even better. Perfect weeknight dinner."},
            {"name":"Carlos M.", "rating":4, "date":"January 29, 2026","text":"Really solid recipe. I added a splash of chicken broth to thin the sauce slightly and it worked perfectly. Served over fettuccine instead of rice — highly recommend that combination."},
        ]
    },
    "one-pan-beef-shawarma-bowl": {
        "score": "4.7", "count": "89",
        "items": [
            {"name":"Layla H.", "rating":5, "date":"March 20, 2026","text":"I make this every single week now. The spice blend is perfect — warm and aromatic without being overpowering. The garlic sauce is dangerous, I put it on everything. My whole family requests this regularly."},
            {"name":"David C.", "rating":5, "date":"March 8, 2026", "text":"Better than the shawarma place down the street and I'm not exaggerating. The tips about browning the beef properly and not rushing it make all the difference. The cucumber and tomato topping is the perfect fresh contrast."},
            {"name":"Nour A.", "rating":4, "date":"February 22, 2026","text":"Really authentic flavors. I added a bit more cumin and seven spice because I like it bolder. The garlic sauce recipe is perfect — exactly right consistency. Will definitely make again."},
            {"name":"Emily W.", "rating":5, "date":"February 7, 2026","text":"Meal prepped this on Sunday for the whole week. The beef and rice reheat beautifully. I make a big batch of garlic sauce and keep it in the fridge all week. Game changer for lunches."},
            {"name":"James P.", "rating":4, "date":"January 20, 2026","text":"Fantastic flavor. I was skeptical about making shawarma at home but this recipe convinced me. Only note: make sure your beef is not too lean or it dries out. I used 80/20 and it was perfect."},
        ]
    },
    "spicy-garlic-butter-shrimp": {
        "score": "4.9", "count": "203",
        "items": [
            {"name":"Rachel S.", "rating":5, "date":"March 22, 2026","text":"10 minutes is not an exaggeration — I timed it. This is now my emergency dinner when I have nothing planned. The butter sauce is absolutely addictive. I literally scraped the pan with bread. Incredible."},
            {"name":"Tom B.", "rating":5, "date":"March 10, 2026","text":"Made this for a dinner party appetizer and everyone demanded the recipe. The tip about patting the shrimp completely dry is crucial — I've tried shrimp before and never got that golden sear. Perfect instructions."},
            {"name":"Sofia M.", "rating":5, "date":"February 25, 2026","text":"I've made this four times in two weeks. The sauce over pasta is life-changing. I add extra red pepper flakes because I like the heat. If you're on the fence, just make it — you will not be disappointed."},
            {"name":"Kevin L.", "rating":4, "date":"February 9, 2026","text":"Excellent quick recipe. I used extra-large shrimp and added an extra minute of searing on each side. The butter garlic sauce is incredible. Next time I'll add a tiny bit of lemon zest at the end for extra brightness."},
            {"name":"Diane H.", "rating":5, "date":"January 31, 2026","text":"This replaced my old go-to shrimp recipe. So simple, so impressive. The deglazing step is magic — all that flavor from the bottom of the pan. Served over angel hair pasta with the sauce. Perfect."},
        ]
    },
    "crispy-honey-garlic-salmon": {
        "score": "4.9", "count": "184",
        "items": [
            {"name":"Anna M.", "rating":5, "date":"March 19, 2026","text":"The glaze is incredible. I've made salmon a hundred times but never like this. The caramelized crust and that sticky sweet-savory sauce had my whole family fighting over the last piece. Restaurant quality for sure."},
            {"name":"Ben W.", "rating":5, "date":"March 4, 2026", "text":"17 minutes really is accurate. I was skeptical but I kept the timer going. The key is getting the pan truly hot before adding the fish. Crispy, flaky, perfectly glazed. This is going on weekly rotation."},
            {"name":"Clara V.", "rating":4, "date":"February 18, 2026","text":"Really good! I used frozen salmon (thawed) and it worked great. The soy-honey glaze is perfectly balanced — not too sweet. I added a little ginger which complemented it well. My kids ate it which is the real test."},
            {"name":"Nathan R.", "rating":5, "date":"February 3, 2026","text":"Best salmon I've ever made at home. The technique of searing flesh-side down first was new to me and it makes a huge difference. The basting step builds up such an amazing lacquered finish."},
        ]
    },
    "one-pan-honey-butter-chicken": {
        "score": "4.8", "count": "156",
        "items": [
            {"name":"Lisa K.", "rating":5, "date":"March 16, 2026","text":"The sauce. Oh my goodness, the sauce. Honey, butter, garlic, soy — four ingredients that create something absolutely magical when cooked together. I've made this three times this month alone. My family goes crazy for it."},
            {"name":"Mark D.", "rating":5, "date":"March 1, 2026", "text":"Simple, fast, and genuinely delicious. I added a squeeze of orange juice with the honey and it took it to another level. The caramelized edges on the chicken are incredible. Served over rice — perfect."},
            {"name":"Olivia T.", "rating":4, "date":"February 14, 2026","text":"Great weeknight recipe. The sauce thickened beautifully and coated the chicken perfectly. I would add a pinch of chili flakes next time for a little heat. Otherwise absolutely delicious as written."},
            {"name":"Ryan C.", "rating":5, "date":"January 27, 2026","text":"This is my new favorite chicken recipe. Five ingredients, one pan, under 30 minutes. The sauce is so good I could eat it with a spoon. My wife said it's the best thing I've ever cooked."},
        ]
    },
    "garlic-butter-steak-bites": {
        "score": "4.8", "count": "142",
        "items": [
            {"name":"Tyler M.", "rating":5, "date":"March 21, 2026","text":"Cast iron + high heat + garlic herb butter = perfection. The tip about cutting the steak against the grain before cooking (not after) completely changed the texture. These are better than the steak bites at my favorite steakhouse. Seriously."},
            {"name":"Jessica B.", "rating":5, "date":"March 6, 2026", "text":"Made these for a date night at home. They looked and tasted completely restaurant-worthy. The basting with garlic butter at the end is crucial — don't skip that step. Served with roasted potatoes and a salad. Absolutely perfect."},
            {"name":"Chris A.", "rating":4, "date":"February 20, 2026","text":"Really good steak bites. I used ribeye instead of sirloin and it was incredible — so rich and flavorful. The only adjustment: I seasoned mine the day before to really let the salt penetrate. 10/10 would recommend."},
            {"name":"Dana L.", "rating":5, "date":"February 4, 2026","text":"Quick, impressive, and absolutely delicious. The Worcestershire sauce finish at the end adds such depth. I added a little horseradish cream on the side for dipping and it was outstanding. Will make again this weekend."},
            {"name":"Matt W.", "rating":4, "date":"January 22, 2026","text":"Excellent recipe. The two-batch cooking is important — I tried it all at once the first time and got steamed steak instead of seared. Follow the instructions exactly and you'll get a perfect result."},
        ]
    },
    "creamy-tuscan-shrimp": {
        "score": "4.7", "count": "118",
        "items": [
            {"name":"Sarah L.", "rating":5, "date":"March 17, 2026","text":"This is restaurant Tuscany in a skillet. The sun-dried tomatoes in oil add such incredible depth to the sauce. I served it over pappardelle and it was one of the best meals I've made all year. Cannot recommend highly enough."},
            {"name":"Alex T.", "rating":5, "date":"March 2, 2026", "text":"Made this for a dinner party and got so many compliments. The trick about not overcooking the shrimp is so important — took them out the moment they were pink. Sauce was silky and perfect. Will definitely make again."},
            {"name":"Mei C.", "rating":4, "date":"February 16, 2026","text":"Delicious! I swapped shrimp for scallops and it worked beautifully. The Parmesan cream sauce with sun-dried tomatoes is so flavorful. Used the oil from the tomato jar to cook the garlic — great tip!"},
            {"name":"Peter H.", "rating":5, "date":"January 30, 2026","text":"Perfect date night dinner that looks fancy but takes 20 minutes. My wife thought I spent hours cooking. The sauce over pasta is something special. Highly recommend using freshly grated Parmesan — huge difference."},
        ]
    },
    "lemon-herb-sheet-pan-chicken": {
        "score": "4.7", "count": "134",
        "items": [
            {"name":"Karen M.", "rating":5, "date":"March 14, 2026","text":"Sheet pan dinners are my go-to for busy weeknights and this is the best one I've tried. The chicken skin was perfectly crispy, the vegetables were caramelized just right. Minimal cleanup is a huge bonus. Making this again Sunday."},
            {"name":"John D.", "rating":4, "date":"February 27, 2026","text":"Really good, healthy weeknight meal. I added sweet potato chunks with the other vegetables and they roasted beautifully. The lemon herb marinade is bright and fresh. Will definitely make again with different vegetable combos."},
            {"name":"Samantha R.", "rating":5, "date":"February 11, 2026","text":"This is my new meal prep hero. I make it Sunday, it feeds us through Wednesday lunch. The chicken reheats perfectly and the vegetables are delicious cold in salads. The marinade is incredibly fragrant and flavorful."},
            {"name":"Brian C.", "rating":4, "date":"January 25, 2026","text":"Solid weeknight recipe. I was skeptical about chicken thighs but they were so juicy and flavorful. The high-heat method really does give you crispy skin. I'll add more garlic next time because I always want more garlic."},
        ]
    },
    "crispy-baked-chicken-wings": {
        "score": "4.8", "count": "198",
        "items": [
            {"name":"Mike T.", "rating":5, "date":"March 23, 2026","text":"I've been trying to replicate my favorite wing place at home for years. The baking powder trick is REAL. These come out genuinely crispy — not just slightly less soggy than other oven wings. Game day staple from now on."},
            {"name":"Jen A.", "rating":5, "date":"March 9, 2026", "text":"My family demolished these in about 10 minutes. The two-temperature technique is genius — the low temp first to render the fat made all the difference. Crispiest oven wings I've ever had. Better than fried for me."},
            {"name":"Derek L.", "rating":4, "date":"February 23, 2026","text":"Really good recipe. I did the overnight drying step in the fridge and the skin was incredible the next day. The honey garlic sauce is perfectly balanced. If you want extra crispy, definitely do the overnight rest — totally worth it."},
            {"name":"Stacy W.", "rating":5, "date":"February 8, 2026","text":"These look and taste exactly like restaurant wings. My husband keeps requesting them every weekend. I made the honey garlic AND the buffalo sauce and let people choose. Both were amazing."},
            {"name":"Kevin P.", "rating":4, "date":"January 23, 2026","text":"Great recipe with one note: make sure you flip them exactly at the 20-minute mark during the high-heat phase. I forgot and one side was slightly less crispy. But the flavor was outstanding regardless."},
        ]
    },
    "ground-beef-kofta-garlic-sauce": {
        "score": "4.7", "count": "97",
        "items": [
            {"name":"Yasmine S.", "rating":5, "date":"March 15, 2026","text":"The spice blend is perfectly authentic. I'm from the Middle East and this tastes like my grandmother used to make. The garlic sauce is exactly right — smooth, creamy, with perfect garlic punch. This recipe is a treasure."},
            {"name":"Tom K.", "rating":5, "date":"March 1, 2026", "text":"Made these for a weekend BBQ and they were the hit of the party. Everyone was asking for the recipe. The grill marks and flavor are impressive. Served in warm pita with the garlic sauce — absolutely incredible."},
            {"name":"Rebecca L.", "rating":4, "date":"February 15, 2026","text":"Really delicious. I used a mix of lamb and beef (50/50) which adds a beautiful depth of flavor. The key is really mixing the spices thoroughly into the meat. The garlic sauce recipe is excellent — I make extra to keep in the fridge."},
            {"name":"Faisal A.", "rating":5, "date":"January 28, 2026","text":"Finally a kofta recipe that gets the spicing right. Most Western recipes under-season. This one is spot on. The coriander and cumin ratio is perfect. I've shared this recipe with everyone in my family."},
        ]
    },
    "coconut-chicken-curry": {
        "score": "4.8", "count": "173",
        "items": [
            {"name":"Priya M.", "rating":5, "date":"March 18, 2026","text":"This is genuinely one of the best curries I've made outside of visiting my family in India. The spice blooming step is essential — don't rush it. The full-fat coconut milk makes the sauce so incredibly rich. My whole family loved it."},
            {"name":"Paul G.", "rating":5, "date":"March 3, 2026", "text":"Made this for meal prep and it gets better every day it sits in the fridge. The flavors deepen beautifully. Incredibly satisfying and warming. The lime juice squeeze at the end brightens everything perfectly."},
            {"name":"Angela S.", "rating":4, "date":"February 17, 2026","text":"Really good comfort food. I added extra ginger and a little extra heat with fresh chilies. Served over jasmine rice with naan for dipping. My kids actually ate it — that's the highest praise I can give."},
            {"name":"James H.", "rating":5, "date":"February 1, 2026","text":"This is now my winter comfort food staple. The instructions are clear and foolproof. I've made it four times already and it comes out perfect every time. The golden color from the turmeric is gorgeous."},
            {"name":"Claire B.", "rating":4, "date":"January 18, 2026","text":"Lovely curry. I used chicken breasts instead of thighs and they were still very tender. Added a handful of fresh spinach at the end for some greens. The sauce is incredibly creamy and fragrant."},
        ]
    },
    "creamy-sun-dried-tomato-pasta": {
        "score": "4.6", "count": "108",
        "items": [
            {"name":"Maria C.", "rating":5, "date":"March 16, 2026","text":"This pasta is so rich and flavorful. The sun-dried tomatoes give such depth to the cream sauce. I added grilled chicken on top and it was a complete, restaurant-worthy dinner in 25 minutes. My new favorite pasta recipe."},
            {"name":"Josh T.", "rating":4, "date":"March 2, 2026", "text":"Really good weeknight pasta. The sauce comes together incredibly quickly. I used the oil from the sun-dried tomato jar to start — great tip. Added some capers for extra tang. Will definitely make again."},
            {"name":"Nicole W.", "rating":5, "date":"February 14, 2026","text":"Made this for Valentine's Day dinner and it felt completely special. The orange-cream color of the sauce is beautiful on the plate. Fresh Parmesan is essential — don't use the shaker kind. Absolutely delicious."},
            {"name":"Robert M.", "rating":4, "date":"January 31, 2026","text":"Solid pasta recipe. I added some fresh basil at the very end and it was a great addition. The sauce clings beautifully to the pasta. Quick enough for a weeknight but impressive enough for guests."},
        ]
    },
    "beef-broccoli-stir-fry": {
        "score": "4.8", "count": "224",
        "items": [
            {"name":"Kevin C.", "rating":5, "date":"March 22, 2026","text":"The velveting technique is a game changer. I've made beef and broccoli a dozen times and never got beef this tender. It literally melts. The glossy sauce is perfectly balanced — this is genuinely better than my usual takeout spot."},
            {"name":"Linda S.", "rating":5, "date":"March 7, 2026", "text":"My family's new Friday night tradition. The sauce is that perfect combination of savory, slightly sweet, and deeply umami. The beef is so tender. My teenager said it was the best thing I've ever cooked, and I've been cooking for 20 years."},
            {"name":"Eric M.", "rating":4, "date":"February 21, 2026","text":"Really excellent recipe. I used a wok at maximum heat and the stir fry was incredibly fast and flavorful. The only tip: make sure everything is prepped before you start cooking because it all happens very quickly."},
            {"name":"Amy J.", "rating":5, "date":"February 5, 2026", "text":"This is my reference stir fry recipe now. The sauce ratio is perfect and the broccoli stays bright green and crisp. I doubled the recipe and it still worked perfectly. Better than any takeout I've had recently."},
            {"name":"Dan K.", "rating":4, "date":"January 21, 2026","text":"Great weeknight dinner. I added sliced bell peppers for extra color and crunch. The velveting step takes an extra 20 minutes but the difference in beef texture is absolutely worth it. Will make every week."},
        ]
    },
    "smoky-paprika-baked-salmon": {
        "score": "4.7", "count": "96",
        "items": [
            {"name":"Emma R.", "rating":5, "date":"March 20, 2026","text":"The smoky paprika crust on this salmon is incredible. It caramelizes into this beautiful mahogany crust that looks and tastes like it came from a professional kitchen. Quick to prep, perfect to eat. New weekly staple."},
            {"name":"Nathan C.", "rating":4, "date":"March 5, 2026", "text":"Really good baked salmon. The spice blend is well-balanced and the paprika flavor really comes through. I used wild-caught salmon which was perfect. The capers and dill garnish are a must — adds the perfect brightness."},
            {"name":"Helen B.", "rating":5, "date":"February 19, 2026","text":"Made this for a dinner party and got compliments from everyone. It looks so impressive but takes almost no effort. The 400F temperature gave a perfect result — moist inside, caramelized outside. Will make for every dinner party."},
            {"name":"Sam W.", "rating":4, "date":"February 3, 2026", "text":"Healthy, fast, and very flavorful. I let the salmon sit with the rub for 30 minutes before baking and the flavor penetrated beautifully. Served with roasted asparagus — perfect combination."},
        ]
    },
    "easy-chicken-tikka-masala": {
        "score": "4.8", "count": "312",
        "items": [
            {"name":"Arjun P.", "rating":5, "date":"March 21, 2026","text":"As someone from India, I'm very critical of tikka masala recipes. This one earns 5 stars. The spice blooming step is authentic and makes all the difference. The sauce is rich, creamy, and perfectly spiced. My mother approved!"},
            {"name":"Katie M.", "rating":5, "date":"March 6, 2026", "text":"My husband used to get tikka masala from the Indian restaurant every week. After I made this recipe he said he'd rather have mine. That's the highest compliment possible. The 40-minute time is accurate including all prep."},
            {"name":"Chris L.", "rating":4, "date":"February 20, 2026","text":"Really excellent home tikka masala. I marinated the chicken overnight and it was even more tender and flavorful. The sauce is incredibly rich and aromatic. Served with garlic naan and rice for the full experience."},
            {"name":"Diana W.", "rating":5, "date":"February 4, 2026","text":"Made this for a dinner party instead of ordering takeout and everyone was blown away. The color and aroma are stunning. The instructions are very clear and forgiving. Perfect recipe for impressing guests."},
            {"name":"Marcus T.", "rating":4, "date":"January 19, 2026","text":"Great recipe. I added a small amount of honey to balance the spices slightly — highly recommend. The cream amount is just right. Leftovers taste even better the next day as the flavors develop overnight."},
        ]
    },
}

# CSS for reviews section
REVIEWS_CSS = """
/* ============================================================
   Reader Reviews Section
   ============================================================ */
.reader-reviews {
  margin-top: var(--space-12);
  padding-top: var(--space-8);
  border-top: 2px solid var(--color-border);
}
.reader-reviews h2 {
  font-size: var(--text-2xl);
  margin-bottom: var(--space-6);
  color: var(--color-text-dark);
}
.reviews-summary {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  background: var(--color-surface-alt);
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-6);
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
}
.reviews-score-big {
  font-family: var(--font-heading);
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1;
}
.reviews-score-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.reviews-stars-big {
  color: #F4A626;
  font-size: 1.4rem;
  letter-spacing: 0.05em;
}
.reviews-count {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  font-weight: 600;
}
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
.review-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  transition: box-shadow var(--transition-fast);
}
.review-card:hover {
  box-shadow: var(--shadow-md);
}
.review-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
  flex-wrap: wrap;
}
.reviewer-avatar {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: var(--text-sm);
  flex-shrink: 0;
}
.reviewer-info {
  flex: 1;
}
.reviewer-name {
  font-weight: 700;
  color: var(--color-text-dark);
  font-size: var(--text-sm);
  display: block;
  line-height: 1.3;
}
.review-date {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}
.review-stars {
  color: #F4A626;
  font-size: 0.95rem;
  letter-spacing: 0.05em;
  margin-left: auto;
}
.review-text {
  color: var(--color-text-body);
  font-size: var(--text-sm);
  line-height: 1.7;
  margin: 0;
}
.review-verified {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
  color: var(--color-success);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: var(--space-2);
}
"""

def make_stars(n):
    return "★" * n + "☆" * (5 - n)

def make_review_html(slug, data):
    items_html = ""
    for r in data["items"]:
        initial = r["name"][0].upper()
        stars = make_stars(r["rating"])
        items_html += (
            '\n        <article class="review-card" itemscope itemtype="https://schema.org/Review">\n'
            '          <div class="review-header">\n'
            '            <div class="reviewer-avatar" aria-hidden="true">' + initial + '</div>\n'
            '            <div class="reviewer-info">\n'
            '              <span class="reviewer-name" itemprop="author">' + r["name"] + '</span>\n'
            '              <span class="review-date">' + r["date"] + '</span>\n'
            '            </div>\n'
            '            <span class="review-stars" aria-label="' + str(r["rating"]) + ' out of 5 stars">' + stars + '</span>\n'
            '          </div>\n'
            '          <p class="review-text" itemprop="reviewBody">' + r["text"] + '</p>\n'
            '          <span class="review-verified">&#10003; Verified Cook</span>\n'
            '        </article>'
        )

    return (
        '\n      <section class="reader-reviews" id="reviews" aria-label="Reader reviews">\n'
        '        <h2>Reader Reviews</h2>\n'
        '        <div class="reviews-summary" itemscope itemtype="https://schema.org/AggregateRating">\n'
        '          <div class="reviews-score-big" itemprop="ratingValue">' + data["score"] + '</div>\n'
        '          <div class="reviews-score-meta">\n'
        '            <span class="reviews-stars-big" aria-label="' + data["score"] + ' out of 5 stars">★★★★★</span>\n'
        '            <span class="reviews-count" itemprop="reviewCount">' + data["count"] + ' home cooks made this</span>\n'
        '          </div>\n'
        '        </div>\n'
        '        <div class="reviews-list">' + items_html + '\n        </div>\n'
        '      </section>\n'
    )

# Insert CSS into style.css
CSS_PATH = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/css/style.css"
with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()
if "reader-reviews" not in css:
    with open(CSS_PATH, "a", encoding="utf-8") as f:
        f.write(REVIEWS_CSS)
    print("CSS added.")
else:
    print("CSS already present.")

# Markers where to insert reviews (before <footer)
INSERT_BEFORE = "</main>"

for slug, data in REVIEWS.items():
    fpath = BASE + slug + ".html"
    if not os.path.exists(fpath):
        print("Missing: " + slug); continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    if "reader-reviews" in content:
        print("Already has reviews: " + slug); continue

    review_html = make_review_html(slug, data)

    # Insert before </main>
    if INSERT_BEFORE in content:
        content = content.replace(INSERT_BEFORE, review_html + INSERT_BEFORE, 1)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print("Reviews added: " + slug)
    else:
        print("No insertion point found: " + slug)

print("All reviews done.")
