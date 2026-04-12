#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
SOURCE_PAGES = ROOT / "source-download" / "pages"
SOURCE_ASSETS = ROOT / "source-download" / "assets"
OUTPUT_ASSETS = ROOT / "assets" / "images"

SITE_NAME = "Nikko Indonesia"
TAGLINE = "Chemicals and Laboratory Equipment"
PHONE = "+62-778-466373, +62-778-466374"
EMAIL = "yana@nikko-indonesia.co.id"
ADDRESS = "Kara Industrial Park Blok A No.50 A, Batam - Indonesia, 29463"

NAV_ITEMS = [
    ("Home", "/"),
    ("Laboratory Equipment", "/laboratory-equipment/"),
    ("Chemicals and Life Science", "/chemicals-and-life-science/"),
    ("Scientific", "/scientific/"),
    ("About Us", "/about-us/"),
    ("Contact", "/contact-us/"),
]

PRODUCTS = [
    (
        "Frontier Duo Fume Hoods",
        "/laboratory-equipment/frontier-duo-fume-hoods/",
        "Duo-Fume-Hoods.jpg",
        "Fume hood with ergonomic design and reliable containment for laboratory safety.",
    ),
    (
        "Frontier Mono Fume Hoods",
        "/laboratory-equipment/frontier-mono-fume-hoods/",
        "Mono-Fume-Hoods.jpg",
        "Primary containment solution for personnel protection from hazardous chemicals.",
    ),
    (
        "SubliMate Freeze Dryer",
        "/laboratory-equipment/sublimate-freeze-dryer/",
        "Freeze-Dryer.jpg",
        "Freeze drying solution for dependable laboratory sample preparation workflows.",
    ),
    (
        "Airstream Horizontal Laminar Flow",
        "/laboratory-equipment/airstream-horizontal-laminar-flow-clean-benches/",
        "Horizontal-Laminar-Flow.jpg",
        "Clean bench system designed for sample and process protection.",
    ),
    (
        "Airstream Vertical Laminar Flow",
        "/laboratory-equipment/airstream-vertical-laminar-flow-clean-benches/",
        "Vertical-Laminar-Flow.jpg",
        "Energy-efficient airflow protection for sensitive work areas.",
    ),
    (
        "Class II Biological Safety Cabinet",
        "/laboratory-equipment/airstream-class-ii-biological-safety-cabinet-d-series/",
        "bsc-AC2-D.jpg",
        "Biological safety cabinet for personnel, product, and environmental protection.",
    ),
    (
        "Combination Refrigerator and Freezer",
        "/laboratory-equipment/esco-hp-series-laboratory-combination-refrigerator-and-freezer/",
        "Refrigerator-and-Freezer.jpg",
        "Cold storage solution for laboratories that need reliable dual-mode performance.",
    ),
    (
        "Forced Convection Incubators",
        "/laboratory-equipment/isotherm-forced-convection-laboratory-incubators/",
        "Laboratory-Incubators.jpg",
        "Stable incubator platform for research and controlled temperature workflows.",
    ),
    (
        "Forced Convection Ovens",
        "/laboratory-equipment/isotherm-forced-convection-laboratory-ovens/",
        "Oven.jpg",
        "Laboratory oven line built for consistent heating and dependable throughput.",
    ),
    (
        "Laboratory Refrigerators",
        "/laboratory-equipment/esco-hp-series-laboratory-refrigerators/",
        "Laboratory-Refrigerators.jpg",
        "Dedicated laboratory refrigeration for secure cold storage applications.",
    ),
    (
        "PCR Cabinets",
        "/laboratory-equipment/airstream-polymerase-chain-reaction-cabinets/",
        "PCR-A.jpg",
        "PCR cabinet range supporting contamination-controlled molecular workflows.",
    ),
]

PRODUCT_SUMMARY = {href: summary for _, href, _, summary in PRODUCTS}

PAGE_FILES = {
    "/about-us/": "about-us.html",
    "/contact-us/": "contact-us.html",
    "/chemicals-and-life-science/": "chemicals-and-life-science.html",
    "/scientific/": "scientific.html",
    "/laboratory-equipment/": "laboratory-equipment.html",
    "/laboratory-equipment/frontier-duo-fume-hoods/": "laboratory-equipment__frontier-duo-fume-hoods.html",
    "/laboratory-equipment/frontier-mono-fume-hoods/": "laboratory-equipment__frontier-mono-fume-hoods.html",
    "/laboratory-equipment/sublimate-freeze-dryer/": "laboratory-equipment__sublimate-freeze-dryer.html",
    "/laboratory-equipment/airstream-horizontal-laminar-flow-clean-benches/": "laboratory-equipment__airstream-horizontal-laminar-flow-clean-benches.html",
    "/laboratory-equipment/airstream-vertical-laminar-flow-clean-benches/": "laboratory-equipment__airstream-vertical-laminar-flow-clean-benches.html",
    "/laboratory-equipment/airstream-class-ii-biological-safety-cabinet-d-series/": "laboratory-equipment__airstream-class-ii-biological-safety-cabinet-d-series.html",
    "/laboratory-equipment/esco-hp-series-laboratory-combination-refrigerator-and-freezer/": "laboratory-equipment__esco-hp-series-laboratory-combination-refrigerator-and-freezer.html",
    "/laboratory-equipment/isotherm-forced-convection-laboratory-incubators/": "laboratory-equipment__isotherm-forced-convection-laboratory-incubators.html",
    "/laboratory-equipment/isotherm-forced-convection-laboratory-ovens/": "laboratory-equipment__isotherm-forced-convection-laboratory-ovens.html",
    "/laboratory-equipment/esco-hp-series-laboratory-refrigerators/": "laboratory-equipment__esco-hp-series-laboratory-refrigerators.html",
    "/laboratory-equipment/airstream-polymerase-chain-reaction-cabinets/": "laboratory-equipment__airstream-polymerase-chain-reaction-cabinets.html",
}

HERO_TEXT = {
    "/": "",
    "/about-us/": "A trusted partner for laboratory equipment, chemicals, and scientific supplies in Batam and surrounding areas.",
    "/contact-us/": "Connect with our team for product information, quotations, and business inquiries.",
    "/chemicals-and-life-science/": "Supporting laboratories and industry with essential chemicals and life science supply categories.",
    "/scientific/": "A practical range of laboratory glassware, plasticware, porcelain, and supporting tools.",
    "/laboratory-equipment/": "Explore the main laboratory equipment lines currently featured by PT. Nikko Indonesia.",
}

CONTENT_OVERRIDES = {
    "/about-us/": """
    <h2>About PT. Nikko Indonesia</h2>
    <p><strong>PT. Nikko Indonesia</strong> was established on 28 March 2001 in Batam. The company began by supplying barcode labels in collaboration with a Singapore-based partner and later expanded into laboratory equipment, chemicals, and scientific supplies to serve broader industrial and laboratory requirements.</p>
    <p>Today, we support customers in Batam as well as companies in surrounding areas by providing dependable products, responsive service, and practical product support. Our goal is to help customers access the equipment and materials they need with confidence.</p>
    <p>We are committed to offering quality laboratory products and scientific supplies that align with customer needs. By combining recognized brands, reliable sourcing, and efficient communication, PT. Nikko Indonesia continues to build long-term business relationships based on trust and service.</p>
    """,
    "/contact-us/": """
    <h2>Get in Touch</h2>
    <p>For product information, pricing inquiries, and further assistance, please contact PT. Nikko Indonesia through the details below.</p>
    <p><strong>Address</strong><br>Kara Industrial Park Blok A No.50 A<br>Batam - Indonesia, 29463</p>
    <p><strong>Phone</strong><br><a href="tel:+62778466373">+62-778-466373</a>, <a href="tel:+62778466374">+62-778-466374</a></p>
    <p><strong>Email</strong><br><a href="mailto:yana@nikko-indonesia.co.id">yana@nikko-indonesia.co.id</a></p>
    <p>We welcome inquiries related to laboratory equipment, chemicals, and scientific products.</p>
    """,
    "/chemicals-and-life-science/": """
    <h2>Chemicals and Life Science</h2>
    <p>PT. Nikko Indonesia supports laboratories and industrial customers with a focused range of chemicals and life science related product categories. Our supply scope includes:</p>
    <ul>
      <li>Biosciences and biotechnology</li>
      <li>Staining kits</li>
      <li>Chromatography</li>
      <li>Water and food analysis, including lab water support</li>
      <li>Microbiology and biomonitoring</li>
      <li>Laboratory equipment</li>
      <li>Pharmaceutical chemical solutions</li>
      <li>Laboratory essentials</li>
    </ul>
    <p>Please contact us if you would like more information on availability and suitable products for your application.</p>
    """,
    "/scientific/": """
    <h2>Scientific Products</h2>
    <p>We offer a practical range of scientific and laboratory support products for daily use, routine analysis, and general laboratory operations.</p>
    <h3>Plasticware</h3>
    <ul>
      <li>Beaker plastic</li>
      <li>Measuring jug</li>
      <li>Wash bottle</li>
      <li>Sample bottle, narrow and wide neck</li>
      <li>Funnel</li>
      <li>Measuring cylinder and disposable pipette</li>
      <li>Universal pipette tips and filter tips</li>
      <li>PCR tube, micro tubes, microtube rack, and PCR tube rack</li>
    </ul>
    <h3>Porcelain</h3>
    <ul>
      <li>Mortar</li>
      <li>Pestle</li>
      <li>Evaporating basin</li>
      <li>Crucible</li>
    </ul>
    <h3>Glassware</h3>
    <ul>
      <li>Beaker glass</li>
      <li>Erlenmeyer flask with or without stopper</li>
      <li>Erlenmeyer flask with screw cap</li>
      <li>Boiling flask, round and flat bottom</li>
      <li>Boiling flask, two-neck and three-neck</li>
      <li>Kjeldahl flask</li>
      <li>Separating funnel and standard funnel</li>
      <li>Condenser</li>
      <li>Measuring cylinder</li>
      <li>Volumetric flask</li>
      <li>Measuring pipette and volumetric pipette</li>
      <li>Burette and automatic burette</li>
      <li>Washing bottle</li>
      <li>BOD bottle, laboratory bottle, and reagent bottle</li>
      <li>Filtering flask, filtering bottle, and filter holder</li>
      <li>Threaded bottle with cap</li>
      <li>Microscope slide and cover glass</li>
      <li>Rod stirrer glass, test tube, centrifuge tube, and Pasteur pipette</li>
      <li>Soxhlet extractor</li>
    </ul>
    <h3>Tools</h3>
    <ul>
      <li>Thermometer, hydrometer, thermohygrometer, and refractometer</li>
      <li>Bunsen burner, lamp alcohol, and magnetic stirrer bar</li>
      <li>Tweezer, spatula, and support clamps</li>
      <li>Rod, stand, tripod, and lab jack</li>
      <li>Weighing bottle, crucible and lid</li>
      <li>Pipette filter, pipette controller, micropipette, dispenser, and digital burette</li>
      <li>Pipette rack, stand, and rotary holder</li>
      <li>Test tube rack and stainless steel accessories</li>
    </ul>
    """,
    "/laboratory-equipment/": """
    <h2>Laboratory Equipment</h2>
    <p>PT. Nikko Indonesia offers a focused range of laboratory equipment for safety, sample handling, temperature control, and contamination-controlled applications.</p>
    <p>The main product lines currently featured on our website include:</p>
    <ul>
      <li>Frontier® Mono™ Fume Hoods</li>
      <li>Frontier™ Duo Fume Hoods</li>
      <li>SubliMate® Freeze Dryer</li>
      <li>Airstream® Horizontal Laminar Flow Clean Benches</li>
      <li>Airstream® Vertical Laminar Flow Clean Benches</li>
      <li>Airstream® Class II Biological Safety Cabinet (D-Series)</li>
      <li>Esco HP Series Laboratory Combination Refrigerator and Freezer</li>
      <li>Isotherm® Forced Convection Laboratory Incubators</li>
      <li>Isotherm® Forced Convection Laboratory Ovens</li>
      <li>Esco HP Series Laboratory Refrigerators</li>
      <li>Airstream® Polymerase Chain Reaction Cabinets</li>
    </ul>
    <p>Browse the detail pages below for product overviews and key features.</p>
    """,
}


def ensure_assets() -> None:
    OUTPUT_ASSETS.mkdir(parents=True, exist_ok=True)
    for item in SOURCE_ASSETS.iterdir():
        if item.is_file():
            shutil.copy2(item, OUTPUT_ASSETS / item.name)


def read_page(path: str) -> tuple[str, str]:
    source = (SOURCE_PAGES / PAGE_FILES[path]).read_text(encoding="utf-8")

    title_match = re.search(r'<h1 class="header-post-title-class">(.*?)</h1>', source, re.S)
    content_match = re.search(
        r'<div class="entry-content clearfix">(.*?)</div>\s*<footer class="entry-meta-bar',
        source,
        re.S,
    )

    title = html.unescape(strip_tags(title_match.group(1))).strip() if title_match else SITE_NAME
    content = content_match.group(1).strip() if content_match else ""
    if path in CONTENT_OVERRIDES:
        return title, CONTENT_OVERRIDES[path].strip()
    return title, clean_content(content)


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value)


def clean_content(content: str) -> str:
    content = content.replace("\r", "")
    content = content.replace("http://nikko-indonesia.ganitheyong.masuk.web.id/wp-content/uploads/", "/assets/images/")
    content = content.replace("https://nikko-indonesia.co.id/wp-content/uploads/", "/assets/images/")
    content = re.sub(r"/assets/images/\d{4}/\d{2}/", "/assets/images/", content)
    content = content.replace("&nbsp;", " ")
    content = content.replace("&#8211;", "-")
    content = content.replace("&#038;", "&")
    content = content.replace(" ", " ")
    content = re.sub(r'\sclass="[^"]*"', "", content)
    content = re.sub(r'\sstyle="[^"]*"', "", content)
    content = re.sub(r'\swidth="[^"]*"', "", content)
    content = re.sub(r'\sheight="[^"]*"', "", content)
    content = re.sub(r'\sdecoding="[^"]*"', "", content)
    content = re.sub(r'\sfetchpriority="[^"]*"', "", content)
    content = re.sub(r'\ssizes="[^"]*"', "", content)
    content = re.sub(r'\ssrcset="[^"]*"', "", content)
    content = re.sub(r'<a[^>]+href="[^"]+\.(?:jpg|jpeg|png|gif|webp)"[^>]*>(.*?)</a>', r"\1", content, flags=re.S | re.I)
    content = re.sub(r"</?(?:div|section|footer)[^>]*>", "", content)
    content = re.sub(r"<p>\s*</p>", "", content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r'href="https://nikko-indonesia\.co\.id', 'href="', content)
    content = re.sub(r'href="http://nikko-indonesia\.ganitheyong\.masuk\.web\.id', 'href="', content)
    return content.strip()


def nav_html(current_path: str) -> str:
    items = []
    for label, href in NAV_ITEMS:
        active = ' class="is-active"' if href == current_path else ""
        items.append(f'<a href="{relative_url(current_path, href)}"{active}>{label}</a>')
    return "".join(items)


def relative_url(current_path: str, target_path: str) -> str:
    if current_path == target_path:
        return "./"

    current_parts = [part for part in current_path.strip("/").split("/") if part]
    target_parts = [part for part in target_path.strip("/").split("/") if part]

    if current_path == "/":
        current_dir = []
    else:
        current_dir = current_parts

    common = 0
    for left, right in zip(current_dir, target_parts):
        if left != right:
            break
        common += 1

    up = [".."] * (len(current_dir) - common)
    down = target_parts[common:]
    parts = up + down

    if not parts:
        return "./"

    return "/".join(parts) + "/"


def asset_url(current_path: str, asset_path: str) -> str:
    return relative_url(current_path, "/") + asset_path.lstrip("/")


def layout(title: str, current_path: str, hero_title: str, hero_text: str, body: str) -> str:
    hero_paragraph = f'      <p>{html.escape(hero_text)}</p>\n' if hero_text else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} | {SITE_NAME}</title>
  <meta name="description" content="Nikko Indonesia supplies laboratory equipment, chemicals, and scientific products for industrial and research needs.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{asset_url(current_path, 'assets/css/site.css')}">
</head>
<body>
  <header class="site-header">
    <div class="topbar">
      <div class="shell">
        <span>{TAGLINE}</span>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
    </div>
    <div class="shell nav-wrap">
      <a class="brand" href="{relative_url(current_path, '/')}">
        <img src="{asset_url(current_path, 'assets/images/Logo-Nikko.png')}" alt="Nikko Indonesia logo">
        <div>
          <strong>{SITE_NAME}</strong>
          <span>{TAGLINE}</span>
        </div>
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" class="site-nav">
        {nav_html(current_path)}
      </nav>
    </div>
  </header>

  <section class="page-hero">
    <img src="{asset_url(current_path, 'assets/images/cropped-Nikkoheader.jpg')}" alt="" aria-hidden="true">
    <div class="shell hero-inner">
      <p class="eyebrow">PT. Nikko Indonesia</p>
      <h1>{html.escape(hero_title)}</h1>
{hero_paragraph}    </div>
  </section>

  <main class="shell page-body">
    {body}
  </main>

  <footer class="site-footer">
    <div class="shell footer-grid">
      <div>
        <h3>{SITE_NAME}</h3>
        <p>{TAGLINE}</p>
        <p>{ADDRESS}</p>
      </div>
      <div>
        <h3>Contact</h3>
        <p><a href="tel:+62778466373">{PHONE}</a></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h3>Quick Links</h3>
        <p><a href="{relative_url(current_path, '/laboratory-equipment/')}">Laboratory Equipment</a></p>
        <p><a href="{relative_url(current_path, '/chemicals-and-life-science/')}">Chemicals and Life Science</a></p>
        <p><a href="{relative_url(current_path, '/scientific/')}">Scientific</a></p>
      </div>
    </div>
    <div class="shell footer-bottom">
      <p>Copyright &copy; 2026 {SITE_NAME}. Rebuilt as a static website for fast hosting and easy maintenance.</p>
    </div>
  </footer>

  <script src="{asset_url(current_path, 'assets/js/site.js')}"></script>
</body>
</html>
"""


def product_cards(current_path: str, limit: int | None = None) -> str:
    cards = []
    for name, href, image, summary in PRODUCTS[:limit]:
        cards.append(
            f"""
            <article class="product-card">
              <img src="{asset_url(current_path, f'assets/images/{image}')}" alt="{html.escape(name)}">
              <div>
                <h3>{html.escape(name)}</h3>
                <p>{html.escape(summary)}</p>
                <a href="{relative_url(current_path, href)}">View details</a>
              </div>
            </article>
            """
        )
    return "".join(cards)


def home_body() -> str:
    cards = product_cards("/", limit=6)
    return f"""
    <section class="grid-intro">
      <article class="panel lead-panel">
        <p class="eyebrow">Laboratory Supplier in Indonesia</p>
        <h2>Reliable supply for laboratory equipment, chemicals, and scientific products.</h2>
        <p>PT. Nikko Indonesia consistently applies a documented quality management system and continues improving service quality so our products can be proven objectively.</p>
        <div class="inline-actions">
          <a class="button" href="{relative_url('/', '/contact-us/')}">Contact us</a>
          <a class="button button-secondary" href="{relative_url('/', '/laboratory-equipment/')}">Explore products</a>
        </div>
      </article>
      <aside class="panel stats-panel">
        <div>
          <strong>Since 2001</strong>
          <span>Serving customers in Batam and surrounding areas.</span>
        </div>
        <div>
          <strong>Focused Expertise</strong>
          <span>Laboratory equipment, chemicals, and scientific supplies.</span>
        </div>
        <div>
          <strong>Customer Support</strong>
          <span>Responsive communication for product information and inquiries.</span>
        </div>
      </aside>
    </section>

    <section class="section-heading">
      <div>
        <p class="eyebrow">Featured Products</p>
        <h2>Main equipment highlights from the current website</h2>
      </div>
      <a href="{relative_url('/', '/laboratory-equipment/')}">See all equipment</a>
    </section>
    <section class="product-grid">
      {cards}
    </section>

    <section class="grid-intro split-section">
      <article class="panel">
        <p class="eyebrow">Vision</p>
        <h2>Long-term professional supplier for laboratory needs.</h2>
        <p>Our vision is to become a long-term professional supplier of laboratory equipment, chemicals, and scientific products in Indonesia, especially in Batam and surrounding areas.</p>
      </article>
      <article class="panel">
        <p class="eyebrow">Mission</p>
        <h2>Excellent service for every customer.</h2>
        <p>We are confident to provide excellent services to all customers through dependable products and practical support.</p>
      </article>
    </section>

    <section class="category-strip">
      <a class="category-card" href="{relative_url('/', '/laboratory-equipment/')}">
        <span>Laboratory Equipment</span>
        <strong>11 major product pages</strong>
      </a>
      <a class="category-card" href="{relative_url('/', '/chemicals-and-life-science/')}">
        <span>Chemicals and Life Science</span>
        <strong>Core supply categories</strong>
      </a>
      <a class="category-card" href="{relative_url('/', '/scientific/')}">
        <span>Scientific</span>
        <strong>Glassware, tools, plastic, porcelain</strong>
      </a>
    </section>
    """


def article_body(title: str, content: str, current_path: str) -> str:
    content = content.replace('src="/assets/', f'src="{asset_url(current_path, "assets/")}')
    content = content.replace('href="/assets/', f'href="{asset_url(current_path, "assets/")}')
    sidebar = f"""
    <aside class="side-panel">
      <div class="panel sticky-panel">
        <p class="eyebrow">Need Information?</p>
        <h3>Contact Nikko Indonesia</h3>
        <p>For product availability, technical inquiries, or quotation requests, contact our team directly.</p>
        <ul class="contact-list">
          <li>{ADDRESS}</li>
          <li><a href="tel:+62778466373">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
        <a class="button" href="{relative_url(current_path, '/contact-us/')}">Go to contact page</a>
      </div>
    </aside>
    """

    extra = ""
    if current_path == "/laboratory-equipment/":
        cards = product_cards(current_path)
        extra = f"""
        <section class="section-heading compact">
          <div>
            <p class="eyebrow">Equipment Range</p>
            <h2>Detail pages rebuilt from the original website</h2>
          </div>
        </section>
        <section class="product-grid">
          {cards}
        </section>
        """

    return f"""
    <div class="content-layout">
      <article class="panel article-panel">
        <div class="prose">
          {content}
        </div>
        {extra}
      </article>
      {sidebar}
    </div>
    """


def write_page(path: str, html_text: str) -> None:
    out_dir = ROOT if path == "/" else ROOT / path.strip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html_text, encoding="utf-8")


def build_pages(paths: Iterable[str]) -> None:
    for current_path in paths:
        title, content = read_page(current_path)
        hero_text = HERO_TEXT.get(current_path, PRODUCT_SUMMARY.get(current_path, "Trusted laboratory products and support from PT. Nikko Indonesia."))
        body = article_body(title, content, current_path)
        page_html = layout(
            title=title,
            current_path=current_path,
            hero_title=title,
            hero_text=hero_text,
            body=body,
        )
        write_page(current_path, page_html)


def build_home() -> None:
    page_html = layout(
        title=SITE_NAME,
        current_path="/",
        hero_title=TAGLINE,
        hero_text=HERO_TEXT["/"],
        body=home_body(),
    )
    write_page("/", page_html)


def main() -> None:
    ensure_assets()
    build_home()
    build_pages(path for path in PAGE_FILES if path != "/")
    print("site build complete")


if __name__ == "__main__":
    main()
