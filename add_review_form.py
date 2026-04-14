"""
add_review_form.py
Add interactive review form (stars + comment) after .reviews-list on all recipe pages.
Skip pages that already have the form.
"""
import os, re

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/recipes/"

REVIEW_FORM = """
        <!-- Review Form -->
        <div class="review-form-wrap" id="reviewFormWrap">
          <h3 class="review-form-title">Write a Review</h3>
          <form class="review-form" id="reviewForm" novalidate>
            <div class="rf-stars-row">
              <span class="rf-stars-label">Your Rating</span>
              <div class="rf-stars" id="rfStars" role="group" aria-label="Select star rating">
                <button type="button" class="rf-star" data-v="1" aria-label="1 star">&#9733;</button>
                <button type="button" class="rf-star" data-v="2" aria-label="2 stars">&#9733;</button>
                <button type="button" class="rf-star" data-v="3" aria-label="3 stars">&#9733;</button>
                <button type="button" class="rf-star" data-v="4" aria-label="4 stars">&#9733;</button>
                <button type="button" class="rf-star" data-v="5" aria-label="5 stars">&#9733;</button>
              </div>
              <input type="hidden" id="rfRating" name="rating" value="0">
            </div>
            <div class="rf-field">
              <input type="text" id="rfName" placeholder="Your name" required maxlength="60" autocomplete="name">
            </div>
            <div class="rf-field">
              <textarea id="rfComment" placeholder="Share your experience with this recipe..." required rows="4" maxlength="800"></textarea>
            </div>
            <p class="rf-note">Reviews are moderated before publishing.</p>
            <button type="submit" class="btn btn--primary rf-submit">Post Review</button>
          </form>
          <div class="rf-success" id="rfSuccess" hidden>
            &#10003; Thank you! Your review has been received and will appear after moderation.
          </div>
        </div>"""

updated = 0
for fname in sorted(os.listdir(BASE)):
    if not fname.endswith(".html") or fname == "index.html":
        continue
    path = BASE + fname
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "review-form-wrap" in content:
        print("Skip (already has form):", fname)
        continue

    # Insert before closing </section> of reader-reviews
    if '</div>\n      </section>' in content and 'reader-reviews' in content:
        # Find the reviews section close
        new_content = content.replace(
            '        </div>\n      </section>',
            '        </div>' + REVIEW_FORM + '\n      </section>',
            1
        )
    elif 'reviews-list' in content:
        # Fallback: insert before </section> right after reviews-list close
        new_content = re.sub(
            r'(</div>\s*</section>)',
            REVIEW_FORM + r'\n      </section>',
            content,
            count=1
        )
    else:
        print("No reviews section:", fname)
        continue

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        updated += 1
        print("Updated:", fname)
    else:
        print("No change:", fname)

print(f"\nDone. {updated} files updated.")
