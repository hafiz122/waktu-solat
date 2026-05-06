#!/usr/bin/env python3
"""
Generate all HTML files for Waktu Solat Malaysia website.
Generates home pages and zone pages for all 5 languages.
"""
import json
import os

with open("data/zones.json", "r", encoding="utf-8") as f:
    ZONES = json.load(f)

LANGS = {
    "ms": {"name": "Bahasa Melayu", "dir": ".", "path_prefix": "", "home_url": "index.html"},
    "en": {"name": "English", "dir": "en", "path_prefix": "en/", "home_url": "en/index.html"},
    "zh": {"name": "中文", "dir": "zh", "path_prefix": "zh/", "home_url": "zh/index.html"},
    "ta": {"name": "தமிழ்", "dir": "ta", "path_prefix": "ta/", "home_url": "ta/index.html"},
    "ar": {"name": "العربية", "dir": "ar", "path_prefix": "ar/", "home_url": "ar/index.html"},
}

GA_CODE = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D98NW4WJ9D"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-D98NW4WJ9D');
</script>"""

# Unsplash mosque images
HERO_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/5/56/Putra_Mosque_being_reflected_in_the_lake_%28cropped%29.jpg"
GALLERY_IMAGES = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/5/56/Putra_Mosque_being_reflected_in_the_lake_%28cropped%29.jpg", "caption_ms": "Masjid Putra, Putrajaya", "caption_en": "Putra Mosque, Putrajaya", "caption_zh": "布特拉清真寺, 布城", "caption_ta": "புத்ரா மசூதி, புத்ராஜாயா", "caption_ar": "مسجد بترا، بوتراجايا"},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/4/4b/SA_Blue_Mosque.jpg", "caption_ms": "Masjid Sultan Salahuddin Abdul Aziz Shah", "caption_en": "Sultan Salahuddin Abdul Aziz Mosque", "caption_zh": "苏丹 Salahuddin Abdul Aziz 清真寺", "caption_ta": "சுல்தான் சலாஹுதீன் அப்துல் அஜீஸ் மசூதி", "caption_ar": "مسجد السلطان صلاح الدين عبد العزيز"},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/8/85/Cristal_Mosque_in_Kuala_Terengganu.jpg", "caption_ms": "Masjid Kristal, Kuala Terengganu", "caption_en": "Crystal Mosque, Kuala Terengganu", "caption_zh": "水晶清真寺, 瓜拉登嘉楼", "caption_ta": "கிரிஸ்டல் மசூதி, கோலா தெரெங்கானு", "caption_ar": "مسجد الكريستال، كوالا ترغانو"},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Masjid_Negara_Malaysia_20250822.jpg/3840px-Masjid_Negara_Malaysia_20250822.jpg", "caption_ms": "Masjid Negara, Kuala Lumpur", "caption_en": "National Mosque, Kuala Lumpur", "caption_zh": "国家清真寺, 吉隆坡", "caption_ta": "தேசிய மசூதி, கோலாலம்பூர்", "caption_ar": "المسجد الوطني، كوالالمبور"},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Ubudiah_Mosque%2C_circa_2023.jpg", "caption_ms": "Masjid Ubudiah, Perak", "caption_en": "Ubudiah Mosque, Perak", "caption_zh": "乌布迪亚清真寺, 霹雳", "caption_ta": "உபுதியா மசூதி, பேராக்", "caption_ar": "مسجد أبودياه، بيراك"},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/2/24/Albukhary.png", "caption_ms": "Masjid Al-Bukhary, Kedah", "caption_en": "Al-Bukhary Mosque, Kedah", "caption_zh": "阿尔-布哈里清真寺, 吉打", "caption_ta": "அல்-புகாரி மசூதி, கெடா", "caption_ar": "مسجد البخاري، كيداه"},
]

def get_translations(lang):
    t = {
        "ms": {
            "title": "Waktu Solat Malaysia",
            "zone_title": "Waktu Solat {zone_code} - {zone_name}",
            "subtitle": "Jadual Waktu Solat Bagi Semua Zon di Malaysia",
            "select_zone": "Pilih Zon",
            "search_place": "Cari tempat (contoh: Alor Setar, Ipoh)",
            "today_prayer": "Waktu Solat Hari Ini",
            "next_30_days": "Waktu Solat 30 Hari Akan Datang",
            "home": "Laman Utama",
            "current_zone": "Zon Semasa",
            "detected_location": "Lokasi Dikesan",
            "next_prayer": "Solat Seterusnya",
            "disclaimer": "Masa solat adalah anggaran. Sila rujuk JAKIM untuk ketepatan rasmi.",
            "seo_desc": "Waktu solat Malaysia mengikut zon JAKIM. Jadual solat harian dan 30 hari akan datang dengan pengesanan lokasi automatik.",
            "gallery_title": "Galeri Masjid Malaysia",
            "days": "Hari",
            "date": "Tarikh",
            "imsak": "Imsak",
            "subuh": "Subuh",
            "syuruk": "Syuruk",
            "zohor": "Zohor",
            "asar": "Asar",
            "maghrib": "Maghrib",
            "isyak": "Isyak",
        },
        "en": {
            "title": "Malaysia Prayer Times",
            "zone_title": "Prayer Times {zone_code} - {zone_name}",
            "subtitle": "Prayer Times for All Zones in Malaysia",
            "select_zone": "Select Zone",
            "search_place": "Search place (e.g. Alor Setar, Ipoh)",
            "today_prayer": "Today's Prayer Times",
            "next_30_days": "Next 30 Days Prayer Times",
            "home": "Home",
            "current_zone": "Current Zone",
            "detected_location": "Detected Location",
            "next_prayer": "Next Prayer",
            "disclaimer": "Prayer times are approximate. Please refer to JAKIM for official accuracy.",
            "seo_desc": "Malaysia prayer times by JAKIM zone. Daily and 30-day prayer schedules with automatic location detection.",
            "gallery_title": "Malaysian Mosque Gallery",
            "days": "Day",
            "date": "Date",
            "imsak": "Imsak",
            "subuh": "Fajr",
            "syuruk": "Sunrise",
            "zohor": "Dhuhr",
            "asar": "Asr",
            "maghrib": "Maghrib",
            "isyak": "Isha",
        },
        "zh": {
            "title": "马来西亚祈祷时间",
            "zone_title": "祈祷时间 {zone_code} - {zone_name}",
            "subtitle": "马来西亚所有地区的祈祷时间",
            "select_zone": "选择地区",
            "search_place": "搜索地点 (例如: 亚罗士打, 怡保)",
            "today_prayer": "今日祈祷时间",
            "next_30_days": "未来30天祈祷时间",
            "home": "首页",
            "current_zone": "当前地区",
            "detected_location": "检测到的位置",
            "next_prayer": "下一次祈祷",
            "disclaimer": "祈祷时间为近似值。请参考JAKIM获取官方准确时间。",
            "seo_desc": "马来西亚JAKIM分区祈祷时间。每日及未来30天祈祷时间表，支持自动位置检测。",
            "gallery_title": "马来西亚清真寺画廊",
            "days": "日",
            "date": "日期",
            "imsak": "晨礼前",
            "subuh": "晨礼",
            "syuruk": "日出",
            "zohor": "晌礼",
            "asar": "晡礼",
            "maghrib": "昏礼",
            "isyak": "宵礼",
        },
        "ta": {
            "title": "மலேசியா நமஸ்கார நேரம்",
            "zone_title": "நமஸ்கார நேரம் {zone_code} - {zone_name}",
            "subtitle": "மலேசியாவின் அனைத்து மண்டலங்களுக்கான நமஸ்கார நேரம்",
            "select_zone": "மண்டலத்தைத் தேர்ந்தெடு",
            "search_place": "இடத்தைத் தேடு (எ.கா: அலோர் ஸ்டார், இப்போ)",
            "today_prayer": "இன்றைய நமஸ்கார நேரம்",
            "next_30_days": "அடுத்த 30 நாட்களின் நமஸ்கார நேரம்",
            "home": "முகப்பு",
            "current_zone": "தற்போதைய மண்டலம்",
            "detected_location": "கண்டறியப்பட்ட இடம்",
            "next_prayer": "அடுத்த நமஸ்காரம்",
            "disclaimer": "நமஸ்கார நேரங்கள் அணுகியதாகும். அதிகாரப்பூர்வ துல்லியத்திற்கு JAKIM-ஐப் பார்க்கவும்.",
            "seo_desc": "JAKIM மண்டலத்தின்படி மலேசியா நமஸ்கார நேரம். தானியங்கி இருப்பிடக் கண்டறிதலுடன் தினசரி மற்றும் 30 நாள் அட்டவணை.",
            "gallery_title": "மலேசிய பள்ளிவாசல் காட்சியகம்",
            "days": "நாள்",
            "date": "தேதி",
            "imsak": "இம்சாக்",
            "subuh": "சுபு",
            "syuruk": "சூர்யோதயம்",
            "zohor": "ஜோஹர்",
            "asar": "அஸ்ர்",
            "maghrib": "மக்ரிப்",
            "isyak": "இஷா",
        },
        "ar": {
            "title": "أوقات الصلاة في ماليزيا",
            "zone_title": "أوقات الصلاة {zone_code} - {zone_name}",
            "subtitle": "أوقات الصلاة لجميع المناطق في ماليزيا",
            "select_zone": "اختر المنطقة",
            "search_place": "ابحث عن مكان (مثال: ألور سيتار، إيبوه)",
            "today_prayer": "أوقات الصلاة اليوم",
            "next_30_days": "أوقات الصلاة للـ 30 يومًا القادمة",
            "home": "الرئيسية",
            "current_zone": "المنطقة الحالية",
            "detected_location": "الموقع المكتشف",
            "next_prayer": "الصلاة القادمة",
            "disclaimer": "أوقات الصلاة تقريبية. يرجى الرجوع إلى JAKIM للدقة الرسمية.",
            "seo_desc": "أوقات الصلاة في ماليزيا حسب منطقة JAKIM. جداول الصلاة اليومية ولمدة 30 يومًا مع الكشف التلقائي عن الموقع.",
            "gallery_title": "معرض المساجد الماليزية",
            "days": "يوم",
            "date": "التاريخ",
            "imsak": "الإمساك",
            "subuh": "الفجر",
            "syuruk": "الشروق",
            "zohor": "الظهر",
            "asar": "العصر",
            "maghrib": "المغرب",
            "isyak": "العشاء",
        },
    }
    return t[lang]


def generate_html(lang, zone_code=None, is_home=True):
    info = LANGS[lang]
    t = get_translations(lang)
    
    if zone_code:
        zone_name = ZONES[zone_code]
        page_title = t["zone_title"].format(zone_code=zone_code, zone_name=zone_name)
        canonical = f"https://waktusolat.my/{info['path_prefix']}{zone_code}.html"
        og_type = "article"
    else:
        page_title = t["title"]
        canonical = f"https://waktusolat.my/{info['path_prefix']}index.html"
        og_type = "website"
    
    html_lang = {"ms": "ms", "en": "en", "zh": "zh-CN", "ta": "ta", "ar": "ar"}[lang]
    rtl_attr = ' dir="rtl" data-t="body"' if lang == "ar" else ''
    
    # Breadcrumb for Schema.org
    breadcrumb_items = [
        {"name": t["home"], "url": f"https://waktusolat.my/{info['path_prefix']}index.html"},
    ]
    if zone_code:
        breadcrumb_items.append({"name": f"{zone_code} - {zone_name}", "url": canonical})
    
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": item["name"], "item": item["url"]}
            for i, item in enumerate(breadcrumb_items)
        ]
    }, ensure_ascii=False)
    
    # WebPage schema
    webpage_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page_title,
        "description": t["seo_desc"],
        "url": canonical,
        "inLanguage": html_lang,
        "isPartOf": {
            "@type": "WebSite",
            "name": "Waktu Solat Malaysia",
            "url": "https://waktusolat.my/"
        }
    }, ensure_ascii=False)
    
    # Prayer times schema for zone pages
    prayer_schema = ""
    if zone_code:
        prayer_schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "SpecialAnnouncement",
            "name": page_title,
            "text": f"Daily prayer times for {zone_code} - {zone_name}",
            "datePosted": "2026-05-01T00:00:00+08:00",
            "announcementLocation": {
                "@type": "Place",
                "name": zone_name,
                "address": {"@type": "PostalAddress", "addressCountry": "MY"}
            }
        }, ensure_ascii=False)
    
    # Language links for header
    lang_links = ""
    for lcode, linfo in LANGS.items():
        target = "index.html" if is_home else f"{zone_code}.html"
        active = ' active' if lcode == lang else ''
        prefix = "" if lcode == "ms" else f"{lcode}/"
        lang_links += f'<a href="/{prefix}{target}" hreflang="{html_lang}" class="{active}">{linfo["name"]}</a>'
    
    # Home button link (relative to current file location)
    if is_home:
        home_link = "index.html"
    else:
        # For zone pages, link to same-language home relative to current folder
        home_link = "index.html"
    
    # Gallery
    gallery_html = ""
    for img in GALLERY_IMAGES:
        cap = img.get(f"caption_{lang}", img["caption_en"])
        gallery_html += f'''
        <div class="gallery-item">
          <img src="{img["url"]}" alt="{cap}" loading="lazy" width="600" height="400">
          <div class="caption">{cap}</div>
        </div>'''
    
    # Path adjustments for subfolders
    css_path = "css/style.css" if info["dir"] == "." else "../css/style.css"
    js_path = "js/main.js" if info["dir"] == "." else "../js/main.js"
    data_prefix = "data/" if info["dir"] == "." else "../data/"
    
    html = f'''<!DOCTYPE html>
<html lang="{html_lang}"{rtl_attr}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['seo_desc']}">
<meta name="keywords" content="waktu solat, prayer times Malaysia, JAKIM, {zone_code or ''}, {zone_name if zone_code else ''} jadual solat, Malaysia prayer schedule">
<meta name="author" content="Waktu Solat Malaysia">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#1a5c3a">

<!-- Open Graph -->
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{t['seo_desc']}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{HERO_IMAGE}">
<meta property="og:locale" content="{html_lang}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page_title}">
<meta name="twitter:description" content="{t['seo_desc']}">
<meta name="twitter:image" content="{HERO_IMAGE}">

<!-- Canonical -->
<link rel="canonical" href="{canonical}">

<!-- Alternate languages -->
<link rel="alternate" hreflang="ms" href="https://waktusolat.my/{(zone_code + '.html') if zone_code else 'index.html'}">
<link rel="alternate" hreflang="en" href="https://waktusolat.my/en/{(zone_code + '.html') if zone_code else 'index.html'}">
<link rel="alternate" hreflang="zh" href="https://waktusolat.my/zh/{(zone_code + '.html') if zone_code else 'index.html'}">
<link rel="alternate" hreflang="ta" href="https://waktusolat.my/ta/{(zone_code + '.html') if zone_code else 'index.html'}">
<link rel="alternate" hreflang="ar" href="https://waktusolat.my/ar/{(zone_code + '.html') if zone_code else 'index.html'}">
<link rel="alternate" hreflang="x-default" href="https://waktusolat.my/{(zone_code + '.html') if zone_code else 'index.html'}">

<title>{page_title}</title>

{GA_CODE}

<script type="application/ld+json">
{webpage_schema}
</script>
<script type="application/ld+json">
{breadcrumb_schema}
</script>
{(f'<script type="application/ld+json">\\n{prayer_schema}\\n</script>' if prayer_schema else '')}

<link rel="preconnect" href="https://upload.wikimedia.org">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="stylesheet" href="{css_path}">
<style>
  /* Critical CSS for above-the-fold content */
  .hero{{min-height:420px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:#fff;position:relative;overflow:hidden;background:linear-gradient(135deg,#0d3320 0%,#1a5c3a 100%)}}
  .hero-bg{{position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:.35;z-index:1}}
  .hero-overlay{{position:absolute;top:0;left:0;width:100%;height:100%;background:linear-gradient(to bottom,rgba(13,51,32,.7) 0%,rgba(26,92,58,.85) 100%);z-index:2}}
  .hero-content{{position:relative;z-index:3;padding:2rem 1rem;max-width:800px}}
  .hero h1{{font-size:clamp(1.8rem,5vw,3rem);font-weight:700;margin-bottom:.5rem;text-shadow:0 2px 10px rgba(0,0,0,.3)}}
  .lang-nav{{position:absolute;top:1rem;right:1rem;z-index:4;display:flex;gap:.5rem;flex-wrap:wrap;justify-content:flex-end}}
  .lang-nav a{{color:#fff;text-decoration:none;font-size:.85rem;padding:.3rem .8rem;border-radius:20px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);transition:all .3s}}
  .home-btn{{position:absolute;top:1rem;left:1rem;z-index:4;color:#fff;text-decoration:none;font-size:.9rem;padding:.4rem 1rem;border-radius:20px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);display:inline-flex;align-items:center;gap:.4rem}}
</style>
</head>
<body{' dir="rtl"' if lang == 'ar' else ''}>

<header class="hero">
  <img class="hero-bg" src="{HERO_IMAGE}" alt="{t['title']}" fetchpriority="high" width="1920" height="1080">
  <div class="hero-overlay"></div>
  
  <nav class="lang-nav" aria-label="Language selector">
    {lang_links}
  </nav>
  
  <a href="{home_link}" class="home-btn" aria-label="{t['home']}">
    <span>🏠</span> <span>{t['home']}</span>
  </a>
  
  <div class="hero-content">
    <h1 id="pageTitle">{t['title']}</h1>
    <p class="subtitle" id="pageSubtitle">{t['subtitle']}</p>
    <div class="date-display" id="currentDate"></div>
  </div>
</header>

<main class="container">

  <section class="selector-section" aria-label="Zone selector">
    <h2>{t['select_zone']}</h2>
    <div class="search-row">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="{t['search_place']}" autocomplete="off" aria-label="Search location">
        <div class="search-results" id="searchResults"></div>
      </div>
      <div class="zone-select">
        <select id="zoneSelect" aria-label="Select zone">
          <option value="">{t['select_zone']}</option>
        </select>
      </div>
    </div>
    <div class="zone-info" id="detectedLocation" style="display:none;color:#1a5c3a;font-weight:600;margin-top:1rem;"></div>
    <div class="zone-info" style="margin-top:1rem;">
      <div class="zone-code" id="zoneCodeDisplay">{zone_code or '-'}</div>
      <div class="zone-name" id="zoneNameDisplay">{zone_name if zone_code else t['current_zone']}</div>
    </div>
  </section>

  <div class="countdown-box" id="countdownBox">
    <div class="label">{t['next_prayer']}</div>
    <div class="time-remaining">--:--:--</div>
    <div class="next-name">-</div>
  </div>

  <section class="prayer-section" aria-label="Today's prayer times">
    <h2 class="section-title">{t['today_prayer']}</h2>
    <div class="prayer-cards" id="todayPrayers">
      <div class="loading">Loading...</div>
    </div>
  </section>

  <div class="islamic-divider">✻ ✻ ✻</div>

  <section class="prayer-section" aria-label="Next 30 days prayer times">
    <h2 class="section-title">{t['next_30_days']}</h2>
    <div class="days-table-wrapper" id="days30Table">
      <div class="loading">Loading...</div>
    </div>
  </section>

  <div class="islamic-divider">✻ ✻ ✻</div>

  <section class="gallery-section" aria-label="Mosque gallery">
    <h2 class="section-title">{t['gallery_title']}</h2>
    <div class="gallery">
      {gallery_html}
    </div>
  </section>

</main>

<footer class="site-footer">
  <p>&copy; {2026} Waktu Solat Malaysia</p>
  <p class="disclaimer">{t['disclaimer']}</p>
</footer>

<script>
  // Set current date in hero
  (function(){{
    const now = new Date();
    const opts = {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }};
    const locale = '{html_lang}';
    document.getElementById('currentDate').textContent = now.toLocaleDateString(locale, opts);
  }})();
</script>
<script src="{js_path}" defer></script>
</body>
</html>'''
    
    return html


def main():
    # Generate home pages
    for lang in LANGS:
        info = LANGS[lang]
        html = generate_html(lang, zone_code=None, is_home=True)
        filepath = os.path.join(info["dir"], "index.html")
        os.makedirs(info["dir"], exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated {filepath}")
    
    # Generate zone pages
    for zone_code in ZONES:
        for lang in LANGS:
            info = LANGS[lang]
            html = generate_html(lang, zone_code=zone_code, is_home=False)
            filepath = os.path.join(info["dir"], f"{zone_code}.html")
            os.makedirs(info["dir"], exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Generated {filepath}")

if __name__ == "__main__":
    main()
