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
    assert "atendimento@60hz.com.br" in html
    assert "to=atendimento@60hz.com.br" in html
    assert '<meta name="viewport"' in html


def test_brand_palette_present():
    css = (ROOT / "styles.css").read_text(encoding="utf-8").lower()
    assert "#ffc000" in css or "#ffc20a" in css or "#ffc100" in css
    assert "#0b84f3" in css or "#0080ff" in css or "#007fff" in css or "#0090ff" in css


def test_responsive_breakpoint_present():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert re.search(r"@media\s*\(max-width:\s*\d+px\)", css)


def test_no_custom_domain_yet():
    assert not (ROOT / "CNAME").exists()


def test_hero_art_assets_exist_and_are_referenced():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "artistic-background.css").read_text(encoding="utf-8")
    background = ROOT / "assets/60hz-painterly-background.png"
    character = ROOT / "assets/60hz-character-cutout.png"

    assert background.exists()
    assert character.exists()
    assert "60hz-painterly-background.png" in html + css
    assert "60hz-character-cutout.png" in html + css
