# 60Hz Right-Side Artwork Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Replace only the right-side hero artwork with the supplied painterly background and a transparent farewell-character cutout while preserving the existing page content and support behavior.

**Architecture:** Keep the dependency-free static GitHub Pages site. Add two repository-local PNG assets, expose them as separate decorative layers inside the existing hero-art element, and restrict the painterly background to the right 58% of the desktop hero. Replace the fade with the approved solid elliptical curve-of-wind seam and a thin yellow border, then reset that treatment at the mobile breakpoint. Validate the visual composition at desktop and mobile sizes before merging and publishing `main`.

**Tech Stack:** HTML5, CSS3, PNG assets, pytest, Python static HTTP server, GitHub Pages.

## Global Constraints

- Replace only the hero artwork composition and its background treatment; preserve the existing page structure.
- Keep the current left-side text, header, support card, footer, and support interactions unchanged.
- Keep the page dependency-free and compatible with GitHub Pages.
- Preserve responsive behavior from 320 px upward.
- Do not add a custom domain or CNAME file.
- Use relative asset paths that work at /60hz-site/.
- No new character or text is generated in the artwork assets.

---

### Task 1: Add artwork asset coverage and prepare the PNG files

**Files:**
- Modify: tests/test_site.py
- Create: assets/60hz-painterly-background.png
- Create: assets/60hz-character-cutout.png

**Interfaces:**
- Consumes: the user-provided files "/Users/fabiocposser/Downloads/ChatGPT Image 7 de ago. de 2026, 21_22_04.png" and "/Users/fabiocposser/Downloads/ChatGPT Image 7 de ago. de 2026, 21_20_42.png".
- Produces: two repository-local PNG paths that the HTML/CSS tasks reference exactly.

- [ ] **Step 1: Write the failing asset test**

Add this test to tests/test_site.py:

~~~python
def test_hero_art_assets_exist_and_are_referenced():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "artistic-background.css").read_text(encoding="utf-8")
    background = ROOT / "assets/60hz-painterly-background.png"
    character = ROOT / "assets/60hz-character-cutout.png"

    assert background.exists()
    assert character.exists()
    assert "60hz-painterly-background.png" in html + css
    assert "60hz-character-cutout.png" in html + css
~~~

- [ ] **Step 2: Run the focused test and verify the expected failure**

Run:

~~~bash
pytest tests/test_site.py::test_hero_art_assets_exist_and_are_referenced -q
~~~

Expected result: FAIL because the new PNG files and their references do not exist yet.

- [ ] **Step 3: Copy and normalize the painterly background**

Copy the supplied background image into the repository with the exact target name:

~~~bash
cp "/Users/fabiocposser/Downloads/ChatGPT Image 7 de ago. de 2026, 21_22_04.png" assets/60hz-painterly-background.png
~~~

Keep the image in PNG format and do not add a text overlay; its existing yellow sun and 60Hz wordmark are part of the approved composition.

- [ ] **Step 4: Create the transparent character cutout**

Use the image-editing tool on "/Users/fabiocposser/Downloads/ChatGPT Image 7 de ago. de 2026, 21_20_42.png" with the instruction to remove only the dark/gradient background, preserve the character exactly, preserve the raised hand, coat, scarf, hair, and colors, and return a transparent PNG. Save the resulting file as assets/60hz-character-cutout.png.

Trim only transparent outer padding after export if necessary so CSS sizing is based on the character bounds. Do not crop the raised hand, scarf ends, hair, or lower coat.

- [ ] **Step 5: Inspect asset metadata**

Run:

~~~bash
file assets/60hz-painterly-background.png assets/60hz-character-cutout.png
~~~

Expected result: both files are valid PNG images. The focused test remains red until Task 2 adds the HTML references.

- [ ] **Step 6: Commit the asset/test checkpoint**

~~~bash
git add tests/test_site.py assets/60hz-painterly-background.png assets/60hz-character-cutout.png
git commit -m "Add final 60Hz hero artwork assets"
~~~

### Task 2: Replace the hero artwork markup with explicit image layers

**Files:**
- Modify: index.html:18-25

**Interfaces:**
- Consumes: assets/60hz-painterly-background.png and assets/60hz-character-cutout.png from Task 1.
- Produces: a decorative hero-art DOM layer with hero-background behind hero-character.

- [ ] **Step 1: Replace the current decorative hero children**

Replace the existing sun-orbit, energy-line, and hero-logo children with:

~~~html
<div class="hero-art" aria-hidden="true">
  <img class="hero-background" src="assets/60hz-painterly-background.png" alt="">
  <img class="hero-character" src="assets/60hz-character-cutout.png" alt="">
</div>
~~~

Do not change the surrounding hero, container, hero-grid, hero-copy, or support markup.

- [ ] **Step 2: Run the existing content tests**

Run:

~~~bash
pytest tests/test_site.py -q
~~~

Expected result: PASS; the existing copy, email, viewport, palette, breakpoint, no-CNAME, and asset-reference checks remain valid.

- [ ] **Step 3: Commit the markup checkpoint**

~~~bash
git add index.html
git commit -m "Layer hero background and farewell character"
~~~

### Task 3: Style the desktop and responsive artwork composition

**Files:**
- Modify: artistic-background.css

**Interfaces:**
- Consumes: hero-background and hero-character markup from Task 2.
- Produces: a desktop right-side composition and a full-width mobile artwork block without changing page behavior.

- [ ] **Step 1: Replace the obsolete artwork overrides**

First update `test_hero_art_background_matches_reference_treatment` in `tests/test_site.py` to require the desktop curve and its mobile reset:

~~~python
hero_before = re.search(r"\.hero-art::before\s*\{([^}]*)\}", css)
mobile_css = css.split("@media (max-width: 980px)", maxsplit=1)[1]

assert 'content: "";' in hero_before.group(1)
assert "left: -46%;" in hero_before.group(1)
assert "width: 58%;" in hero_before.group(1)
assert "height: 124%;" in hero_before.group(1)
assert "background: #fff;" in hero_before.group(1)
assert "border-right: 3px solid rgba(255, 201, 40, 0.82);" in hero_before.group(1)
assert "border-radius: 50%;" in hero_before.group(1)
assert "content: none;" in mobile_css
~~~

Run the focused test and confirm it fails because the current desktop CSS still uses a gradient transition:

~~~bash
uv run --with pytest pytest tests/test_site.py::test_hero_art_background_matches_reference_treatment -q
~~~

Then replace the obsolete transition with readable, scoped rules equivalent to:

~~~css
.hero-art {
  top: 0;
  right: 0;
  width: 58%;
  height: 100%;
  overflow: hidden;
  background: #0b56ba;
}

.hero-background,
.hero-character {
  position: absolute;
  display: block;
  max-width: none;
}

.hero-background {
  z-index: 1;
  inset: 0 auto 0 0;
  width: 112%;
  height: 100%;
  object-fit: cover;
  object-position: center right;
}

.hero-character {
  z-index: 2;
  right: 1%;
  bottom: -8%;
  width: min(58%, 620px);
  height: auto;
  filter: drop-shadow(0 18px 24px rgba(3, 35, 83, 0.22));
}

.hero-art::before {
  content: "";
  position: absolute;
  z-index: 2;
  top: -12%;
  left: -46%;
  width: 58%;
  height: 124%;
  background: #fff;
  border: 0;
  border-right: 3px solid rgba(255, 201, 40, 0.82);
  border-radius: 50%;
  pointer-events: none;
}
~~~

Keep the existing hero sizing and support overlap rules unless the local preview proves the artwork hides the support card. Do not reintroduce a separate overlaid logo, orbit, or synthetic energy lines.

- [ ] **Step 2: Add the mobile artwork rules**

Within the existing breakpoints, set the art layer below the copy:

~~~css
@media (max-width: 980px) {
  .hero-art {
    top: auto;
    bottom: 0;
    width: 100%;
    height: 270px;
  }

  .hero-art::before { content: none; }

  .hero-background {
    object-position: 64% center;
  }

  .hero-character {
    right: 2%;
    bottom: -7%;
    width: min(58%, 360px);
  }
}

@media (max-width: 640px) {
  .hero-art {
    height: 220px;
  }

  .hero-character {
    right: 0;
    bottom: -5%;
    width: min(62%, 250px);
  }
}
~~~

Ensure the existing hero-copy bottom padding still leaves room for the mobile art block.

- [ ] **Step 3: Run static checks and inspect the diff**

Run:

~~~bash
pytest tests/test_site.py -q
git diff --check
~~~

Expected result: all tests pass and git diff --check prints no whitespace errors.

- [ ] **Step 4: Commit the styling checkpoint**

~~~bash
git add artistic-background.css
git commit -m "Match hero artwork to approved reference"
~~~

### Task 4: Verify the visual result locally at desktop and mobile sizes

**Files:**
- Inspect: index.html, artistic-background.css, assets/60hz-painterly-background.png, assets/60hz-character-cutout.png

**Interfaces:**
- Consumes: the complete implementation from Tasks 1–3.
- Produces: verified screenshots and a clean test result before publishing.

- [ ] **Step 1: Start a local static server**

From the repository root, run:

~~~bash
python3 -m http.server 4173
~~~

Use http://127.0.0.1:4173/ for the local page.

- [ ] **Step 2: Inspect the desktop composition**

Open the local page at a desktop viewport near 1440 × 900 and confirm:

- the painterly background fills the right side;
- the character is in front, large, and free of a rectangular dark backdrop;
- the face, raised hand, coat, and scarf are visible;
- the left copy and support card remain unchanged;
- the background sun/60Hz wordmark is not duplicated by another logo layer.

- [ ] **Step 3: Inspect the mobile composition**

Open the same local page at a narrow viewport near 390 × 844 and confirm:

- text remains readable above the artwork;
- the character remains visible below the copy;
- the face is not clipped and the artwork does not cover the support content;
- no horizontal scrollbar appears.

- [ ] **Step 4: Run the full verification set**

~~~bash
pytest tests/test_site.py -q
git status -sb
git diff HEAD~3..HEAD --stat
~~~

Expected result: all tests pass, only intended site files and the design/plan documentation are present, and the diff contains the new artwork assets plus the hero markup/CSS change.

### Task 5: Merge and publish the finished change to GitHub

**Files:**
- No additional files; publish the verified commits from the local repository.

**Interfaces:**
- Consumes: the verified local branch from Task 4.
- Produces: the verified feature branch merged into `main` and the updated `main` pushed to `origin`.

- [ ] **Step 1: Confirm branch and authentication state**

Run:

~~~bash
git status -sb
gh --version
gh auth status
git remote get-url origin
git branch --show-current
~~~

If the current branch is main, create agent/60hz-right-artwork before staging the final change. Keep unrelated working-tree changes out of the branch.

- [ ] **Step 2: Re-run verification before publishing**

~~~bash
pytest tests/test_site.py -q
git diff --check
~~~

- [ ] **Step 3: Confirm the remote base and fast-forward merge into main**

~~~bash
git fetch origin
git merge-base --is-ancestor origin/main main
git checkout main
git merge --ff-only agent/60hz-right-artwork
~~~

- [ ] **Step 4: Verify the merged main branch**

~~~bash
uv run --with pytest pytest tests/test_site.py -q
git diff --check origin/main..main
~~~

Expected result: all tests pass and the merged branch has no whitespace errors.

- [ ] **Step 5: Push main**

~~~bash
git push origin main
~~~

- [ ] **Step 6: Inspect the published GitHub Pages URL**

After GitHub Pages updates, open https://smarley2.github.io/60hz-site/ and confirm the new artwork is served from the pushed branch/default deployment. Report the branch, commit, PR, test result, and any Pages propagation delay.
