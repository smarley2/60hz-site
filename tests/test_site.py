from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_site_files_exist():
    assert (ROOT / "index.html").exists()
    assert (ROOT / "styles.css").exists()


def test_required_content_and_support_link():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Foi uma jornada incrível." in html
    assert "Após 13 anos" in html
    assert "Foi o tempo que perdeste com a tua rosa que fez a tua rosa tão importante." in html
    assert "atendimento@60hz.com.br" in html
    assert 'data-copy-email="atendimento@60hz.com.br"' in html
    assert '<meta name="viewport"' in html


def test_support_card_is_single_column_and_email_copies_only():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    support_card = re.search(r"\.support-card\s*\{([^}]*)\}", css)

    assert support_card
    assert "grid-template-columns: 112px minmax(0, 1fr);" in support_card.group(1)
    assert "max-width: 980px;" in support_card.group(1)
    assert 'class="support-email" type="button"' in html
    assert '<div class="support-action">' not in html
    assert "mail.google.com" not in html
    assert "navigator.clipboard.writeText(email)" in html
    assert "status.textContent = 'Copiando…';" in html


def test_brand_palette_present():
    css = (ROOT / "styles.css").read_text(encoding="utf-8").lower()
    assert "#ffc000" in css or "#ffc20a" in css or "#ffc100" in css
    assert "#0b84f3" in css or "#0080ff" in css or "#007fff" in css or "#0090ff" in css


def test_responsive_breakpoint_present():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert re.search(r"@media\s*\(max-width:\s*\d+px\)", css)


def test_custom_domain_points_to_live_site():
    assert (ROOT / "CNAME").read_text(encoding="utf-8").strip() == "www.60hz.com.br"


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


def test_hero_art_assets_exist_and_are_referenced():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "artistic-background.css").read_text(encoding="utf-8")
    background = ROOT / "assets/60hz-painterly-background.png"
    character = ROOT / "assets/60hz-character-cutout.png"

    assert background.exists()
    assert character.exists()
    assert "60hz-painterly-background.png" in html + css
    assert "60hz-character-cutout.png" in html + css


def test_hero_art_background_matches_reference_treatment():
    css = (ROOT / "artistic-background.css").read_text(encoding="utf-8")
    hero_art = re.search(r"\.hero-art\s*\{([^}]*)\}", css)
    hero_background = re.search(r"\.hero-background\s*\{([^}]*)\}", css)
    hero_before = re.search(r"\.hero-art::before\s*\{([^}]*)\}", css)
    mobile_css = css.split("@media (max-width: 980px)", maxsplit=1)[1]

    assert hero_art
    assert hero_background
    assert hero_before
    assert "width: 58%;" in hero_art.group(1)
    assert "width: 112%;" in hero_background.group(1)
    assert "object-position: center right;" in hero_background.group(1)
    assert 'content: "";' in hero_before.group(1)
    assert "left: -46%;" in hero_before.group(1)
    assert "width: 58%;" in hero_before.group(1)
    assert "height: 124%;" in hero_before.group(1)
    assert "background: #fff;" in hero_before.group(1)
    assert "border-right: 3px solid rgba(255, 201, 40, 0.82);" in hero_before.group(1)
    assert "border-radius: 50%;" in hero_before.group(1)
    assert "content: none;" in mobile_css
