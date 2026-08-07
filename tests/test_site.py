from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_site_files_exist():
    assert (ROOT / "index.html").exists()
    assert (ROOT / "styles.css").exists()


def test_required_content_and_mailto():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Foi uma jornada incrível." in html
    assert "Após 13 anos" in html
    assert "atendimento@60hz.com.br" in html
    assert 'href="mailto:atendimento@60hz.com.br' in html
    assert '<meta name="viewport"' in html


def test_brand_palette_present():
    css = (ROOT / "styles.css").read_text(encoding="utf-8").lower()
    assert "#ffc000" in css or "#ffc20a" in css
    assert "#0b84f3" in css or "#0080ff" in css or "#007fff" in css


def test_responsive_breakpoint_present():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert re.search(r"@media\s*\(max-width:\s*\d+px\)", css)


def test_no_custom_domain_yet():
    assert not (ROOT / "CNAME").exists()
