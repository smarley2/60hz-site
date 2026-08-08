# Legacy URL Redirects Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Send visitors from retired WooCommerce and WordPress URLs to the 60Hz closure landing page and expose only the canonical landing page to search engines.

**Architecture:** Keep the site static on GitHub Pages. Use GitHub Pages' root `404.html` as a client-side fallback for every missing legacy path, and add a minimal canonical `sitemap.xml` plus `robots.txt`. Keep `www.60hz.com.br` as the canonical custom domain and do not hard-code the 125 product paths.

**Tech Stack:** Static HTML, XML, plain text, Python assertion tests, GitHub Pages.

## Global Constraints

- Redirect destination: `https://www.60hz.com.br/`.
- The fallback must include JavaScript, a zero-second meta refresh, and a visible link for no-JavaScript clients.
- The fallback must be `noindex`.
- The sitemap contains only `https://www.60hz.com.br/`.
- The existing `CNAME` value remains `www.60hz.com.br`.
- No dependencies or build system may be added.

---

### Task 1: Add regression tests for legacy routes and SEO files

**Files:**
- Modify: `tests/test_site.py`

**Interfaces:**
- Tests read the repository's static files directly; no runtime redirect helper or dependency is introduced.

- [ ] **Step 1: Replace the obsolete custom-domain assertion**

Change the test that expects no `CNAME` file to read `CNAME`, strip whitespace, and assert it equals `www.60hz.com.br`.

- [ ] **Step 2: Write the failing redirect and SEO tests**

Add assertions equivalent to:

```python
def test_legacy_urls_redirect_to_landing_page():
    html = (ROOT / "404.html").read_text(encoding="utf-8")
    assert '<meta name="robots" content="noindex">' in html
    assert '<meta http-equiv="refresh" content="0; url=https://www.60hz.com.br/">' in html
    assert 'window.location.replace("https://www.60hz.com.br/")' in html
    assert 'href="https://www.60hz.com.br/"' in html


def test_sitemap_and_robots_expose_only_the_landing_page():
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "https://www.60hz.com.br/" in sitemap
    assert "/produto/" not in sitemap
    assert "Sitemap: https://www.60hz.com.br/sitemap.xml" in robots


def test_landing_page_declares_canonical_url():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert '<link rel="canonical" href="https://www.60hz.com.br/">' in html
```

- [ ] **Step 3: Run the focused tests and verify the expected red state**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import importlib.util

path = Path("tests/test_site.py").resolve()
spec = importlib.util.spec_from_file_location("test_site", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for name in (
    "test_legacy_urls_redirect_to_landing_page",
    "test_sitemap_and_robots_expose_only_the_landing_page",
    "test_landing_page_declares_canonical_url",
):
    try:
        getattr(module, name)()
    except Exception as error:
        print(f"{name}: expected failure: {error}")
    else:
        raise SystemExit(f"{name}: unexpectedly passed")
PY
```

Expected: each focused test fails because the new static files and canonical tag do not exist yet.

### Task 2: Implement the static fallback and canonical SEO files

**Files:**
- Create: `404.html`
- Create: `sitemap.xml`
- Create: `robots.txt`
- Modify: `index.html`

**Interfaces:**
- `404.html` serves as the GitHub Pages fallback and sends all unknown paths to the canonical landing URL.
- `sitemap.xml` contains one `<url>` entry for the landing page.
- `robots.txt` references the sitemap.
- `index.html` declares the same canonical URL.

- [ ] **Step 1: Add `404.html`**

Create a valid HTML document with `lang="pt-BR"`, `noindex`, a zero-second refresh to `https://www.60hz.com.br/`, the inline `window.location.replace("https://www.60hz.com.br/")` fallback, and a visible link to the same URL.

- [ ] **Step 2: Add the canonical sitemap and robots policy**

Create a sitemap using the standard `http://www.sitemaps.org/schemas/sitemap/0.9` namespace with one `<loc>https://www.60hz.com.br/</loc>` entry. Create `robots.txt` with `User-agent: *`, `Allow: /`, and `Sitemap: https://www.60hz.com.br/sitemap.xml`.

- [ ] **Step 3: Add the canonical link to `index.html`**

Place `<link rel="canonical" href="https://www.60hz.com.br/">` in the document head alongside the existing description and favicon metadata.

- [ ] **Step 4: Run the focused tests and verify green**

Run the focused test harness from Task 1. Expected: all three new tests pass.

### Task 3: Run the full checks and inspect the static output

**Files:**
- Test: `tests/test_site.py`
- Inspect: `404.html`, `sitemap.xml`, `robots.txt`, `index.html`

- [ ] **Step 1: Run every test function in the existing test module**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import importlib.util

path = Path("tests/test_site.py").resolve()
spec = importlib.util.spec_from_file_location("test_site", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

tests = sorted(name for name in dir(module) if name.startswith("test_"))
for name in tests:
    getattr(module, name)()
    print(f"PASS {name}")
print(f"{len(tests)} tests passed")
PY
```

Expected: every test prints `PASS` and the process exits with status 0.

- [ ] **Step 2: Check XML and whitespace**

Run:

```bash
python3 -c 'import xml.etree.ElementTree as ET; ET.parse("sitemap.xml")'
git diff --check
```

Expected: both commands exit with status 0.

- [ ] **Step 3: Commit the implementation**

Run:

```bash
git add 404.html index.html robots.txt sitemap.xml tests/test_site.py
git commit -m "Redirect legacy URLs to closure landing page"
```

### Task 4: Publish and verify the deployed behavior

**Files:**
- Publish the committed branch through a Pull Request into `main`.

- [ ] **Step 1: Confirm the diff and branch state**

Run `git status -sb` and `git diff origin/main...HEAD --stat`; only the redirect, SEO, test, and plan/spec files may be included.

- [ ] **Step 2: Push the branch and open a draft Pull Request**

Push `agent/legacy-url-redirects` and open a draft PR targeting `main`, because the repository's active ruleset requires Pull Requests.

- [ ] **Step 3: After merge, verify public routes**

Check:

```bash
curl -I https://www.60hz.com.br/
curl -sS https://www.60hz.com.br/sitemap.xml
curl -sS https://www.60hz.com.br/robots.txt
curl -sS https://www.60hz.com.br/produto/kit-bomba-solar-4spn2-11p-4-pol-ate-136m-ou-24m-dia-samking/
```

Expected: the landing page is available, sitemap and robots are the new static files, and the legacy product route loads `404.html` and redirects the browser to the landing page.
