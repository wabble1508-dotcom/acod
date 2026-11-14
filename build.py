"""Erzeugt die Website von ACoD – Afrikanische Community in Dortmund – im Ordner docs/.

Alle Inhalte stehen oben in diesem Skript. Texte ändern, `python3 build.py`
ausführen und den Ordner docs/ veröffentlichen (GitHub Pages: Branch main, Ordner /docs).

Felder in VEREIN, die leer sind, werden auf der Website nicht angezeigt.
Sobald Adresse, E-Mail oder Bankverbindung feststehen, hier eintragen und neu bauen.
"""
from pathlib import Path
from html import escape as e

OUT = Path(__file__).parent / "docs"

# ---------------------------------------------------------------- Vereinsdaten
VEREIN = {
    "name": "ACoD",
    "lang": "Afrikanische Community in Dortmund",
    "adresse": "",          # z. B. "Musterweg 1, 44135 Dortmund"
    "mail": "",             # z. B. "info@acod-dortmund.de"
    "tel": "",
    "vertreten": "",        # Impressum: vertretungsberechtigte Person(en)
    "register": "",         # Impressum: z. B. "Amtsgericht Dortmund, VR 12345"
    "iban": "",             # Spenden: wird nur gezeigt, wenn eingetragen
    "kontoinhaber": "",
    "facebook": "https://www.facebook.com/ACoD2020/",
    "messenger": "https://m.me/ACoD2020",
}
FB_VIDEOS = "https://www.facebook.com/ACoD2020/videos"
FB_PHOTOS = "https://www.facebook.com/ACoD2020/photos"

# ---------------------------------------------------------------- Projekte
PROJEKTE = [
    {
        "slug": "lernbruecke", "t": "Lernbrücke", "s": "laufend", "art": "art-a", "cat": "Bildung & Jugend",
        "d": "Hausaufgabenhilfe und Lesepatenschaften für Kinder aus afrikanischen Familien in Dortmund.",
        "lage": "Viele Kinder aus zugewanderten Familien wachsen mehrsprachig auf. Zu Hause fehlt oft die Zeit oder das Wissen über das deutsche Schulsystem, um bei den Hausaufgaben zu helfen.",
        "tun": ["Hilfe bei Hausaufgaben und beim Lernen für die Schule", "Lesepatenschaften: Ehrenamtliche lesen regelmäßig mit Kindern", "Informationen für Eltern zum Schulsystem, in mehreren Sprachen"],
        "ziele": ["Kinder lernen sicherer und gehen lieber zur Schule", "Eltern kennen ihre Möglichkeiten im Schulsystem", "Ehrenamtliche aus der Community werden zu Vorbildern"],
        "mitmachen": "Wir suchen Lesepatinnen und Lesepaten sowie Menschen, die bei den Hausaufgaben helfen.",
    },
    {
        "slug": "willkommenslotsen", "t": "Willkommenslotsen", "s": "laufend", "art": "art-b", "cat": "Beratung & Begleitung",
        "d": "Erfahrene Community-Mitglieder begleiten neu angekommene Familien zu Ämtern, Ärzten und Schulen.",
        "lage": "Wer neu in Deutschland ist, steht vor Formularen, Terminen und Fristen in einer fremden Sprache. Fehler kosten Zeit, Geld und Nerven.",
        "tun": ["Begleitung zu Behörden, Jobcenter, Arztpraxen und Schulen", "Übersetzen und Erklären in Englisch, Französisch und afrikanischen Sprachen", "Weitervermittlung an passende Beratungsstellen in Dortmund"],
        "ziele": ["Niemand muss allein zum Amt", "Familien finden sich schneller in Dortmund zurecht", "Wissen aus der Community wird weitergegeben"],
        "mitmachen": "Sie sprechen mehrere Sprachen und kennen sich in Dortmund aus? Werden Sie Lotsin oder Lotse.",
    },
    {
        "slug": "kultur-begegnung", "t": "Kultur & Begegnung", "s": "laufend", "art": "art-c", "cat": "Kultur",
        "d": "Feste, Kochabende und Gespräche, die afrikanische Kulturen in Dortmund sichtbar machen.",
        "lage": "Afrikanische Kulturen sind in Dortmund vielfältig vertreten, im Stadtbild aber kaum sichtbar. Begegnung baut Vorurteile ab und schafft Nachbarschaft.",
        "tun": ["Feste mit Musik, Tanz und Essen aus vielen Ländern Afrikas", "Kochabende und offene Treffen für alle", "Gespräche über Teilhabe, Rassismus und Zusammenleben"],
        "ziele": ["Afrikanische Kulturen werden in Dortmund sichtbar", "Menschen unterschiedlicher Herkunft lernen sich kennen", "Die Community stärkt ihren Zusammenhalt"],
        "mitmachen": "Helfen Sie bei der Planung, kochen Sie mit oder bringen Sie Ihre Musik mit.",
    },
    {
        "slug": "integrationsratswahl-2020", "t": "Integrationsratswahl 2020", "s": "abgeschlossen", "art": "art-d", "cat": "Politische Teilhabe",
        "img": "assets/img/flyer-integrationsratswahl-2020.jpg",
        "d": "Als Liste 4 ist ACoD zur Integrationsratswahl der Stadt Dortmund am 13. September 2020 angetreten.",
        "lage": "Im Integrationsrat werden die Interessen der Dortmunderinnen und Dortmunder mit Einwanderungsgeschichte vertreten. Die afrikanische Community wollte dort mit einer eigenen Stimme sprechen.",
        "tun": ["Gründung von ACoD als Wahlliste der Afrikanischen Community in Dortmund", "Kandidatur als Liste 4 unter dem Motto „Wir sind eine Gemeinschaft!“", "Mehrsprachiger Wahlaufruf: Geh wählen! · Vote! · Allez voter! und auf Arabisch"],
        "ziele": ["Die afrikanische Community ist in der Dortmunder Stadtpolitik sichtbar geworden", "Aus der Wahlliste ist eine dauerhafte Gemeinschaft entstanden"],
        "mitmachen": "",
    },
]

NEWS = [
    ("Oktober 2026", "Verein", "Unsere neue Website ist online", "Hier finden Sie ab sofort unsere Themenschwerpunkte, Projekte, unser politisches Engagement und alle Wege, wie Sie mitmachen und spenden können."),
    ("17. Dezember 2025", "Politik", "Der neue ACI nimmt seine Arbeit auf", "Der Ausschuss für Chancengerechtigkeit und Integration der Stadt Dortmund hat sich konstituiert. Für ACoD ist Biraan S. N. J. Bah stimmberechtigtes Mitglied."),
    ("14. September 2025", "Politik", "Wahl zum Ausschuss für Chancengerechtigkeit und Integration", "Dortmund hat den ACI gewählt, die politische Vertretung der Menschen mit Einwanderungsgeschichte. ACoD ist mit Biraan S. N. J. Bah vertreten."),
    ("13. September 2020", "Integrationsrat", "ACoD tritt als Liste 4 an", "Bei der Integrationsratswahl der Stadt Dortmund kandidiert ACoD als Wahlliste der Afrikanischen Community: „Wir sind eine Gemeinschaft!“"),
]

# ---------------------------------------------------------------- Themenschwerpunkte
# Politisches Engagement steht immer zuerst und hat eine eigene Seite.
THEMEN = [
    {"id": "politik", "t": "Politisches Engagement", "href": "politisches-engagement.html",
     "kurz": "Unsere Stimme in der Dortmunder Stadtpolitik: 2020 als Liste 4 im Integrationsrat, seit 2025 stimmberechtigt im Ausschuss für Chancengerechtigkeit und Integration.",
     "text": "ACoD ist als Wahlliste der Afrikanischen Community entstanden. Wir bringen die Anliegen afrikanischer Familien dorthin, wo in Dortmund über Integration und Teilhabe entschieden wird.",
     "punkte": ["Vertretung im Ausschuss für Chancengerechtigkeit und Integration (ACI)", "Anliegen der Community in Rat und Verwaltung einbringen", "Wahlaufrufe und Informationen in vielen Sprachen", "Haltung gegen Rassismus und Diskriminierung"]},
    {"id": "beraten", "t": "Beraten & begleiten", "projekt": "willkommenslotsen",
     "kurz": "Hilfe bei Behördengängen, Schule, Ausbildung und Wohnungssuche, in Deutsch, Englisch, Französisch und weiteren Sprachen.",
     "text": "Wer neu in Dortmund ist, steht vor Formularen, Terminen und Fristen in einer fremden Sprache. Erfahrene Mitglieder der Community helfen und begleiten.",
     "punkte": ["Begleitung zu Behörden, Jobcenter, Arztpraxen und Schulen", "Übersetzen und Erklären in vielen Sprachen", "Weitervermittlung an passende Beratungsstellen"]},
    {"id": "bildung", "t": "Bildung & Jugend", "projekt": "lernbruecke",
     "kurz": "Hausaufgabenhilfe und Lesepatenschaften, damit junge Menschen ihre Wege in Dortmund selbstbewusst gehen.",
     "text": "Kinder und Jugendliche aus afrikanischen Familien sollen in Schule und Ausbildung die gleichen Chancen haben wie alle anderen.",
     "punkte": ["Hausaufgabenhilfe und Lesepatenschaften", "Vorbilder aus der Community", "Informationen für Eltern zum Schulsystem"]},
    {"id": "kultur", "t": "Kultur & Begegnung", "projekt": "kultur-begegnung",
     "kurz": "Feste, Kochabende und Gespräche, die afrikanische Kulturen in der Stadt sichtbar machen und Nachbarschaft stiften.",
     "text": "Afrikanische Kulturen sind in Dortmund vielfältig vertreten. Begegnung baut Vorurteile ab und schafft Nachbarschaft.",
     "punkte": ["Feste mit Musik, Tanz und Essen", "Offene Treffen und Kochabende", "Gespräche über Zusammenleben und Teilhabe"]},
    {"id": "sport", "t": "Sport",
     "kurz": "Sport verbindet: gemeinsame Bewegung, Teamgeist und Begegnung, besonders für Kinder und Jugendliche.",
     "text": "Auf dem Platz zählt das Team, nicht die Herkunft. Sport bringt Menschen zusammen, die sich im Alltag selten begegnen.",
     "punkte": ["Gemeinsame Sportangebote und Turniere", "Kontakte zu Dortmunder Sportvereinen", "Fairness und Teamgeist als Werte"]},
    {"id": "integration", "t": "Nachhaltige Integration & Bildung",
     "kurz": "Integration, die bleibt: Sprache, Anerkennung von Abschlüssen, Ausbildung, Arbeit und demokratische Teilhabe.",
     "text": "Ankommen ist der Anfang. Damit Integration nachhaltig gelingt, braucht es Bildung, Arbeit und die Möglichkeit, mitzureden.",
     "punkte": ["Sprache und Weiterbildung fördern", "Anerkennung ausländischer Abschlüsse unterstützen", "Wege in Ausbildung und Arbeit öffnen", "Demokratiebildung und Mitbestimmung"]},
]

# ---------------------------------------------------------------- Koordination
# Keine Geschäftsführung: ACoD wird ehrenamtlich koordiniert.
# Foto: Datei nach docs/assets/img/team/ legen und Dateinamen eintragen.
KOORDINATION = [
    {"rolle": "Sprecher/in", "name": "", "foto": "", "text": "Vertritt ACoD nach außen und führt die Koordination."},
    {"rolle": "Stellvertretende/r Sprecher/in", "name": "", "foto": "", "text": "Unterstützt und vertritt die Sprecherin oder den Sprecher."},
    {"rolle": "Politischer Vertreter", "name": "Biraan S. N. J. Bah", "foto": "biraan-bah.jpg", "text": "Politischer Vertreter der Afrikanischen Community in Dortmund (ACoD) im Ausschuss für Chancengerechtigkeit und Integration (ACI) der Stadt Dortmund."},
    {"rolle": "Kulturbeauftragte/r", "name": "", "foto": "", "text": "Plant Feste, Begegnungen und kulturelle Angebote."},
    {"rolle": "IT & Support", "name": "", "foto": "", "text": "Kümmert sich um Website, Social Media und digitale Werkzeuge."},
]

# ---------------------------------------------------------------- Mitgliedsorganisationen
# ACoD ist ein Netzwerk. Einträge: ("Name", "https://website-oder-facebook", "kurze Beschreibung")
MITGLIEDER = [
]

# ---------------------------------------------------------------- Partner
PARTNER = [
    {"name": "FreiwilligenAgentur Dortmund", "url": "https://www.freiwilligenagenturdortmund.de/", "logo": "assets/img/partner-freiwilligenagentur-dortmund.png",
     "text": "Vermittelt seit 2002 zwischen Menschen, die sich engagieren möchten, und Organisationen, die Freiwillige suchen."},
    {"name": "Ausschuss für Chancengerechtigkeit und Integration (ACI)", "kurz": "ACI", "url": "https://www.dortmund.de/rathaus-und-verwaltung/lokalpolitik/rat-ausschuesse-beiraete-und-bezirksvertretungen/ausschuesse/ausschuss-fuer-chancengerechtigkeit-und-integration/", "logo": "assets/img/partner-stadt-dortmund.svg",  # eigenes ACI-Logo ist nicht öffentlich, daher Logo der Stadt
     "text": "Vertritt die Interessen der Menschen mit Einwanderungsgeschichte in Dortmund und berät Rat und Verwaltung der Stadt."},
    {"name": "Kommunales Integrationszentrum Dortmund (MIA-DO-KI)", "kurz": "MIA-DO-KI", "url": "https://www.dortmund.de/rathaus/verwaltung/amt-fuer-angelegenheiten-des-oberbuergermeisters-und-des-rates/kommunales-integrationszentrum-dortmund-mia-do-ki/", "logo": "assets/img/partner-mia-do-ki.png",
     "text": "Plant und fördert Integration in Dortmund gemeinsam mit Politik, Verwaltung, Vereinen und Migrantenorganisationen."},
]

# ---------------------------------------------------------------- Navigation
NAV = [
    ("index.html", "Start", []),
    ("ueber-uns.html", "Über ACoD", [("ueber-uns.html", "Wer wir sind"), ("mitglieder.html", "Mitgliedsorganisationen"), ("koordination.html", "Koordination"), ("partner.html", "Partner")]),
    ("was-wir-tun.html", "Was wir tun", [(t.get("href") or f"was-wir-tun.html#{t['id']}", t["t"]) for t in THEMEN]),
    ("projekte.html", "Projekte", [("projekte.html#laufend", "Laufende Projekte"), ("projekte.html#abgeschlossen", "Abgeschlossene Projekte")]),
    ("aktuelles.html", "Aktuelles", [("aktuelles.html", "Neuigkeiten & Termine"), ("galerie.html", "Bilder & Videos")]),
    ("mitmachen.html", "Mitmachen", []),
    ("kontakt.html", "Kontakt", []),
]
SECTION_OF = {"galerie.html": "aktuelles.html", "mitglieder.html": "ueber-uns.html", "koordination.html": "ueber-uns.html", "partner.html": "ueber-uns.html", "politisches-engagement.html": "was-wir-tun.html"}
SECTION_OF.update({f"projekt-{p['slug']}.html": "projekte.html" for p in PROJEKTE})

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:wght@400;600;700&display=swap">'
WORDMARK = '<span class="wordmark" aria-hidden="true">AC<span class="o-check">o<svg viewBox="0 0 40 40"><path d="M6 21 L16 31 L36 6"/></svg></span>D</span>'
EXT = 'target="_blank" rel="noopener"'


def nav_html(current):
    active = SECTION_OF.get(current, current)
    out = []
    for href, label, sub in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if sub:
            subs = "".join(f'<li><a href="{h}">{e(l)}</a></li>' for h, l in sub)
            out.append(f'<li class="has-sub"><a href="{href}"{cur}>{e(label)}</a><ul class="sub">{subs}</ul></li>')
        else:
            out.append(f'<li><a href="{href}"{cur}>{e(label)}</a></li>')
    return "".join(out)


def header(current):
    return f'''<div class="topbar"><div class="wrap">
  <a href="aktuelles.html">Aktuelles</a><a href="mitmachen.html">Mitmachen</a><a href="kontakt.html">Kontakt</a>
  <a href="{VEREIN['facebook']}" {EXT}>Facebook</a>
</div></div>
<header class="site"><div class="wrap">
  <a class="logo" href="index.html" aria-label="ACoD Startseite">
    {WORDMARK}
    <span class="logo-text">Afrikanische Community<br>in Dortmund</span>
  </a>
  <nav class="main" id="nav" aria-label="Hauptmenü"><ul>{nav_html(current)}</ul></nav>
  <button class="menu-toggle" id="menuToggle" type="button" aria-expanded="false" aria-controls="nav">Menü</button>
  <a class="btn btn-donate" href="spenden.html">Spenden</a>
</div></header>
<div class="pattern" aria-hidden="true"></div>'''


def contact_lines():
    v = VEREIN
    parts = [v["lang"]]
    if v["adresse"]:
        parts.append(e(v["adresse"]))
    else:
        parts.append("Dortmund")
    if v["mail"]:
        parts.append(f'<a href="mailto:{e(v["mail"])}">{e(v["mail"])}</a>')
    return "<br>".join(parts)


def footer():
    return f'''<div class="pattern" aria-hidden="true"></div>
<footer>
  <div class="wrap grid">
    <div class="stack" style="gap:.6rem">
      <h3>ACoD</h3>
      <p>{contact_lines()}</p>
      <p>„Wir sind eine Gemeinschaft!“</p>
    </div>
    <div><h3>Über ACoD</h3><ul><li><a href="ueber-uns.html">Wer wir sind</a></li><li><a href="mitglieder.html">Mitgliedsorganisationen</a></li><li><a href="koordination.html">Koordination</a></li><li><a href="partner.html">Partner</a></li><li><a href="politisches-engagement.html">Politisches Engagement</a></li></ul></div>
    <div><h3>Projekte</h3><ul><li><a href="projekte.html#laufend">Laufende Projekte</a></li><li><a href="projekte.html#abgeschlossen">Abgeschlossene Projekte</a></li>{"".join(f'<li><a href="projekt-{p["slug"]}.html">{e(p["t"])}</a></li>' for p in PROJEKTE if p["s"] == "laufend")}</ul></div>
    <div><h3>Unterstützen</h3><ul><li><a href="spenden.html">Spenden</a></li><li><a href="mitmachen.html">Mitmachen</a></li><li><a href="kontakt.html">Kontakt</a></li><li><a href="{VEREIN['facebook']}" {EXT}>Facebook</a></li></ul></div>
  </div>
  <div class="legal"><div class="wrap"><span>© 2026 ACoD – {VEREIN['lang']}</span><span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span></div></div>
</footer>
<script src="assets/main.js"></script>'''


def page(filename, title, body, description):
    full_title = "ACoD – Afrikanische Community in Dortmund" if filename == "index.html" else f"{title} · ACoD Dortmund"
    head = f'''<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="assets/img/gruppenfoto-2020.jpg">
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<link rel="stylesheet" href="assets/style.css">'''
    content = f"{header(filename)}\n<main id=\"inhalt\">\n{body}\n</main>\n{footer()}\n"
    (OUT / filename).write_text(f'<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body>\n{content}</body>\n</html>\n', encoding="utf-8")
    if filename == "index.html":
        (OUT.parent / "preview-index.html").write_text(f"{head}\n{content}", encoding="utf-8")


def page_head(eyebrow, title, lead, crumbs):
    c = " / ".join(f'<a href="{h}">{e(l)}</a>' if h else e(l) for h, l in crumbs)
    return f'''<div class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Pfad">{c}</nav>
  <p class="eyebrow">{e(eyebrow)}</p>
  <h1>{e(title)}</h1>
  <p class="lead">{e(lead)}</p>
</div></div>'''


def project_card(p):
    done = p["s"] == "abgeschlossen"
    art = f'<div class="project-art"><img src="{p["img"]}" alt="" style="width:100%;height:100%;object-fit:cover;display:block"><span class="status done">Abgeschlossen</span></div>' if p.get("img") else \
        f'<div class="project-art {p["art"]}"><span class="status{" done" if done else ""}">{"Abgeschlossen" if done else "Laufend"}</span></div>'
    return f'''<a class="project" href="projekt-{p["slug"]}.html" data-status="{p["s"]}">
  {art}
  <div class="project-body"><div class="project-meta"><span>{e(p["cat"])}</span></div><h3>{e(p["t"])}</h3><p>{e(p["d"])}</p><span class="more">Zum Projekt →</span></div>
</a>'''


def news_html(items):
    return "".join(f'<article><time>{e(d)} · {e(c)}</time><h3>{e(t)}</h3><p>{e(x)}</p></article>' for d, c, t, x in items)


def cta(title, text, href, label, ext=False):
    return f'<div class="wrap section"><div class="cta"><div><h2>{e(title)}</h2><p>{e(text)}</p></div><a class="btn btn-donate" href="{href}" {EXT if ext else ""}>{e(label)}</a></div></div>'


def write_box(text="Schreiben Sie uns eine Nachricht über Facebook. Wir antworten auf Deutsch, Englisch oder Französisch."):
    mail = f'<p class="empty">Oder per E-Mail: <a href="mailto:{e(VEREIN["mail"])}">{e(VEREIN["mail"])}</a></p>' if VEREIN["mail"] else ""
    return f'''<div class="box"><h3>Nachricht schreiben</h3><p class="empty">{e(text)}</p>
  <a class="btn btn-donate" href="{VEREIN['messenger']}" {EXT}>Nachricht über Facebook</a>
  <a class="btn btn-ghost" href="{VEREIN['facebook']}" {EXT} style="color:var(--green)">Zur Facebook-Seite</a>{mail}</div>'''


LANGS = 'Geh wählen! · Vote! · Allez voter! · <span lang="ar" dir="rtl">تعالوا و انتخبوا</span>'


def theme_href(t):
    return t.get("href") or f"was-wir-tun.html#{t['id']}"


def themes_grid():
    """Politisches Engagement als breite Karte mit Liste-4-Abzeichen, danach die übrigen Schwerpunkte."""
    pol, rest = THEMEN[0], THEMEN[1:]
    feature = f'''<a class="theme feature" href="{theme_href(pol)}">
    <div class="stack" style="gap:.6rem">
      <p class="eyebrow">Politische Teilhabe</p>
      <h3>{e(pol["t"])}</h3>
      <p>ACoD ist als Wahlliste der Afrikanischen Community angetreten, als <b>Liste 4</b> bei der Integrationsratswahl am 13. September 2020. Seit 2025 sind wir mit Biraan S. N. J. Bah stimmberechtigt im Ausschuss für Chancengerechtigkeit und Integration (ACI) vertreten. Wir bringen die Anliegen afrikanischer Familien dorthin, wo in Dortmund über Integration entschieden wird.</p>
      <p class="langs" lang="mul">{LANGS}</p>
      <span class="more">Mehr zum politischen Engagement →</span>
    </div>
    <span class="council-badge" aria-hidden="true"><span>Liste</span><b>4</b><small>Integrationsratswahl 2020</small></span>
  </a>'''
    cards = "".join(f'<a class="theme" href="{theme_href(t)}"><h3>{e(t["t"])}</h3><p>{e(t["kurz"])}</p><span class="more">Mehr erfahren →</span></a>' for t in rest)
    join = '<a class="theme join" href="mitmachen.html"><h3>Mitmachen</h3><p>In jedem Schwerpunkt freuen wir uns über Menschen, die mit anpacken.</p><span class="more">So machen Sie mit →</span></a>'
    return f'<div class="themes">{feature}{cards}{join}</div>'


SILHOUETTE = '<svg viewBox="0 0 64 64" width="46%" fill="currentColor" aria-hidden="true"><circle cx="32" cy="22" r="12"/><path d="M8 60c0-14 11-22 24-22s24 8 24 22z"/></svg>'


def initials(name):
    w = [x for x in name.split() if x[0].isalpha()]
    return (w[0][0] + w[-1][0]).upper() if len(w) > 1 else name[:2].upper()


def person_card(p):
    pic = f'<img class="avatar" src="assets/img/team/{e(p["foto"])}" alt="{e(p["name"])}" style="object-fit:cover">' if p.get("foto") else \
        f'<div class="avatar" aria-hidden="true">{e(initials(p["name"])) if p["name"] else SILHOUETTE}</div>'
    name = f'<b>{e(p["name"])}</b>' if p["name"] else '<b class="tbd">Wird in Kürze vorgestellt</b>'
    return f'<div class="person">{pic}<span class="role">{e(p["rolle"])}</span>{name}<p class="empty">{e(p["text"])}</p></div>'


def partner_card(p):
    mark = f'<img src="{p["logo"]}" alt="{e(p["name"])}">' if p.get("logo") else f'<span class="pmark">{e(p.get("kurz") or p["name"])}</span>'
    return f'''<a class="partner" href="{p["url"]}" {EXT}><div class="plogo">{mark}</div><h3>{e(p["name"])}</h3><p>{e(p["text"])}</p><span class="more">Website ansehen ↗</span></a>'''


# ---------------------------------------------------------------- Seiten
def build():
    OUT.mkdir(exist_ok=True)
    for old in ["vorstand.html", "transparenz.html", "termine.html", "projekt-afrika-tag.html", "projekt-frauen-staerken.html", "projekt-corona-hilfe.html", "projekt-fussball-verbindet.html", "integrationsrat.html"]:
        (OUT / old).unlink(missing_ok=True)
    laufend = [p for p in PROJEKTE if p["s"] == "laufend"]
    abgeschlossen = [p for p in PROJEKTE if p["s"] == "abgeschlossen"]

    # Start
    page("index.html", "Start", f'''
<div class="hero"><div class="wrap">
  <div>
    <p class="eyebrow">Afrikanische Community in Dortmund · seit 2020</p>
    <h1>Wir sind eine Gemeinschaft!</h1>
    <p class="lead">Wir verbinden Menschen afrikanischer Herkunft in Dortmund, begleiten Familien beim Ankommen und bringen die Stimme der Community in die Stadtpolitik.</p>
    <div class="hero-actions"><a class="btn btn-donate" href="spenden.html">Jetzt unterstützen</a><a class="btn btn-ghost" href="projekte.html">Unsere Projekte</a></div>
  </div>
  <figure class="hero-photo">
    <img src="assets/img/gruppenfoto-2020.jpg" alt="Mitglieder von ACoD stehen gemeinsam auf einer Treppe in Dortmund" width="785" height="278">
  </figure>
</div></div>
<div class="wrap">
  <div class="section">
    <div class="section-head"><div class="stack" style="gap:.3rem"><p class="eyebrow">Was wir tun</p><h2>Unsere Themenschwerpunkte</h2></div><a class="btn btn-ghost" href="was-wir-tun.html">Alle Schwerpunkte</a></div>
    {themes_grid()}
  </div>
  <div class="section network">
    <div class="stack">
      <p class="eyebrow">Ein Netzwerk</p>
      <h2>ACoD verbindet Organisationen der afrikanischen Community</h2>
      <p class="lead">Unter dem Dach von ACoD arbeiten mehrere Vereine und Initiativen zusammen. Gemeinsam sind wir eine Stimme für die afrikanische Community in Dortmund.</p>
      <div class="hero-actions" style="margin-top:.2rem"><a class="btn btn-green" href="mitglieder.html">Mitgliedsorganisationen</a><a class="btn btn-ghost" href="koordination.html" style="color:var(--green)">Koordination</a></div>
    </div>
  </div>
  <div class="section">
    <div class="section-head"><div class="stack" style="gap:.3rem"><p class="eyebrow">Laufende Projekte</p><h2>Woran wir arbeiten</h2></div><a class="btn btn-ghost" href="projekte.html">Alle Projekte</a></div>
    <div class="projects">{"".join(project_card(p) for p in laufend)}</div>
  </div>
</div>
<div class="donate-band"><div class="wrap donate-grid">
  <div class="stack"><p class="eyebrow">Unterstützen</p><h2>Jede Hilfe stärkt die Community vor Ort.</h2><p class="lead">ACoD lebt vom Engagement seiner Mitglieder. Mit einer Spende oder Ihrer Zeit helfen Sie direkt in Dortmund.</p><div class="hero-actions" style="margin-top:.4rem"><a class="btn btn-donate" href="spenden.html">Spenden</a><a class="btn btn-ghost" href="mitmachen.html" style="color:var(--green)">Mitmachen</a></div></div>
  <ul class="uses">
    <li><b>Lernen</b><span>Material und Begleitung für die Hausaufgabenhilfe</span></li>
    <li><b>Ankommen</b><span>Begleitung neu angekommener Familien</span></li>
    <li><b>Begegnen</b><span>Feste und Treffen für die ganze Stadt</span></li>
  </ul>
</div></div>
<div class="wrap"><div class="section two-col">
  <div class="stack"><div class="section-head"><p class="eyebrow">Aktuelles</p><a href="aktuelles.html">Alle Neuigkeiten →</a></div><div class="news">{news_html(NEWS)}</div></div>
  <div class="stack"><p class="eyebrow">Bilder</p><figure class="flyer"><img src="assets/img/flyer-integrationsratswahl-2020.jpg" alt="Wahlplakat von ACoD zur Integrationsratswahl 2020, Liste 4" width="960" height="448" loading="lazy"><figcaption>Unser Wahlaufruf 2020. Mehr Fotos und Videos auf <a href="{FB_PHOTOS}" {EXT}>Facebook</a>.</figcaption></figure></div>
</div></div>
<div class="wrap"><div class="section">
  <div class="section-head"><div class="stack" style="gap:.3rem"><p class="eyebrow">Partner</p><h2>Gemeinsam für Dortmund</h2></div><a class="btn btn-ghost" href="partner.html">Alle Partner</a></div>
  <div class="partners">{"".join(partner_card(p) for p in PARTNER)}</div>
</div></div>
{cta("Mitmachen statt zuschauen", "Ob als Mitglied, Lesepatin oder Helfer bei Festen: Bei uns ist Platz für alle, die Dortmund gemeinsam gestalten wollen.", "mitmachen.html", "So machen Sie mit")}''',
         "ACoD – Afrikanische Community in Dortmund: Netzwerk für politisches Engagement, Beratung, Bildung, Kultur, Sport und nachhaltige Integration.")

    # Über ACoD
    page("ueber-uns.html", "Über ACoD", page_head("Über ACoD", "Eine Community, viele Organisationen, eine Stimme.",
         "ACoD ist das Netzwerk der afrikanischen Community in Dortmund: Mitgliedsorganisationen, Engagierte und alle, die mit ihnen zusammenleben.",
         [("index.html", "Start"), (None, "Über ACoD")]) + f'''
<div class="wrap">
  <div class="section two-col">
    <div class="prose">
      <h2>Wer wir sind</h2>
      <p>ACoD ist 2020 als Wahlliste der Afrikanischen Community zur Integrationsratswahl in Dortmund angetreten. Aus dieser gemeinsamen Kandidatur ist ein Netzwerk entstanden: Mehrere Vereine und Initiativen der afrikanischen Community haben sich unter dem Dach von ACoD zusammengeschlossen.</p>
      <p>Unser Ziel ist eine Stadtgesellschaft, in der Menschen afrikanischer Herkunft gleichberechtigt teilhaben, mitreden und mitgestalten. Dafür bringen wir uns in die Stadtpolitik ein, unterstützen Familien im Alltag und schaffen Orte der Begegnung.</p>
      <h2>So sind wir organisiert</h2>
      <p>ACoD hat keine Geschäftsführung. Die Arbeit wird ehrenamtlich von einem Koordinationsteam getragen: Sprecher, stellvertretender Sprecher, politischer Vertreter, Kulturbeauftragter sowie IT &amp; Support.</p>
      <h2>Unsere Werte</h2>
      <div class="values"><span>Gemeinschaft</span><span>Teilhabe</span><span>Respekt</span><span>Solidarität</span><span>Bildung</span></div>
    </div>
    <div class="stack">
      <figure class="flyer"><img src="assets/img/gruppenfoto-2020.jpg" alt="Gruppenfoto der ACoD-Mitglieder 2020" width="785" height="278"><figcaption>Das Team von ACoD zur Integrationsratswahl 2020</figcaption></figure>
      <h2>Unser Weg</h2>
      <ol class="timeline">
        <li><b>13. September 2020</b><p><strong>ACoD tritt als Liste 4 an.</strong> Bei der Integrationsratswahl der Stadt Dortmund kandidiert ACoD als Wahlliste der Afrikanischen Community: „Wir sind eine Gemeinschaft!“</p></li>
        <li><b>14. September 2025</b><p><strong>Neue Wahlperiode im ACI.</strong> Bei der Wahl zum Ausschuss für Chancengerechtigkeit und Integration der Stadt Dortmund wird ACoD-Mitglied Biraan S. N. J. Bah stimmberechtigtes Mitglied.</p></li>
        <li><b>17. Dezember 2025</b><p><strong>Der ACI nimmt seine Arbeit auf.</strong> ACoD bringt die Anliegen der afrikanischen Community direkt in den Ausschuss ein.</p></li>
        <li><b>Heute</b><p>Als Netzwerk mehrerer Organisationen engagieren wir uns in Politik, Beratung, Bildung, Kultur, Sport und für nachhaltige Integration.</p></li>
      </ol>
    </div>
  </div>
  <div class="section">
    <h2>Mehr über ACoD</h2>
    <div class="cards3">
      <a class="card" href="mitglieder.html" style="text-decoration:none;color:inherit"><h3>Mitgliedsorganisationen</h3><p>Die Vereine und Initiativen, die ACoD tragen.</p><span class="more">Ansehen →</span></a>
      <a class="card" href="koordination.html" style="text-decoration:none;color:inherit"><h3>Koordination</h3><p>Die Menschen, die ACoD ehrenamtlich koordinieren und vertreten.</p><span class="more">Ansehen →</span></a>
      <a class="card" href="partner.html" style="text-decoration:none;color:inherit"><h3>Partner</h3><p>Mit wem wir in Dortmund zusammenarbeiten.</p><span class="more">Ansehen →</span></a>
    </div>
  </div>
</div>''', "Über ACoD – Afrikanische Community in Dortmund: ein Netzwerk von Organisationen, unsere Werte und unser Weg seit 2020.")

    # Mitgliedsorganisationen
    if MITGLIEDER:
        liste = '<div class="members">' + "".join(
            f'<a class="member" href="{e(u)}" {EXT}><h3>{e(n)}</h3><p>{e(d)}</p><span class="more">Website ansehen ↗</span></a>' if u else
            f'<div class="member"><h3>{e(n)}</h3><p>{e(d)}</p></div>' for n, u, d in MITGLIEDER) + "</div>"
        zahl = f'<p class="lead">{len(MITGLIEDER)} Organisationen arbeiten unter dem Dach von ACoD zusammen.</p>'
    else:
        liste = '<div class="box"><h3>Unsere Mitglieder stellen sich vor</h3><p class="empty">Die Übersicht unserer Mitgliedsorganisationen mit Links zu ihren Seiten wird gerade zusammengestellt.</p></div>'
        zahl = ""
    page("mitglieder.html", "Mitgliedsorganisationen", page_head("Über ACoD", "Mitgliedsorganisationen",
         "ACoD ist ein Netzwerk: Vereine und Initiativen der afrikanischen Community in Dortmund arbeiten unter einem Dach zusammen.",
         [("index.html", "Start"), ("ueber-uns.html", "Über ACoD"), (None, "Mitgliedsorganisationen")]) + f'''
<div class="wrap">
  <div class="section">{zahl}{liste}</div>
  <div class="section two-col">
    <div class="prose">
      <h2>Mit Ihrer Organisation Mitglied werden</h2>
      <p>Sie engagieren sich mit einem Verein, einer Gemeinde oder einer Initiative für die afrikanische Community in Dortmund? Werden Sie Teil des Netzwerks. Gemeinsam haben wir eine stärkere Stimme in der Stadtpolitik, teilen Wissen und planen Projekte zusammen.</p>
      <ul class="goals"><li>Vertretung im Ausschuss für Chancengerechtigkeit und Integration</li><li>Austausch und gemeinsame Projekte</li><li>Sichtbarkeit auf dieser Website</li></ul>
    </div>
    {write_box("Schreiben Sie uns, welche Organisation Sie vertreten. Wir melden uns bei Ihnen.")}
  </div>
</div>''', "Mitgliedsorganisationen im Netzwerk ACoD – Afrikanische Community in Dortmund.")

    # Koordination
    page("koordination.html", "Koordination", page_head("Über ACoD", "Koordination",
         "ACoD hat keine Geschäftsführung. Ein ehrenamtliches Team koordiniert das Netzwerk und vertritt es in Politik und Öffentlichkeit.",
         [("index.html", "Start"), ("ueber-uns.html", "Über ACoD"), (None, "Koordination")]) + f'''
<div class="wrap">
  <div class="section"><div class="team roles">{"".join(person_card(p) for p in KOORDINATION)}</div></div>
  <div class="section two-col">
    <div class="prose">
      <h2>Vertretung in der Politik</h2>
      <p>Biraan S. N. J. Bah vertritt ACoD als stimmberechtigtes Mitglied im Ausschuss für Chancengerechtigkeit und Integration (ACI) der Stadt Dortmund. Dort bringt er die Anliegen der afrikanischen Community in Rat und Verwaltung ein.</p>
      <p><a href="politisches-engagement.html">Mehr zu unserem politischen Engagement →</a></p>
    </div>
    {write_box("Sie möchten jemanden aus der Koordination erreichen? Schreiben Sie uns.")}
  </div>
</div>''', "Koordination von ACoD: Sprecher, stellvertretender Sprecher, politischer Vertreter, Kulturbeauftragter sowie IT & Support.")

    # Partner
    page("partner.html", "Partner", page_head("Über ACoD", "Unsere Partner",
         "Mit diesen Partnern arbeiten wir in Dortmund zusammen.",
         [("index.html", "Start"), ("ueber-uns.html", "Über ACoD"), (None, "Partner")]) + f'''
<div class="wrap">
  <div class="section"><div class="partners">{"".join(partner_card(p) for p in PARTNER)}</div></div>
</div>
{cta("Partner werden", "Schulen, Unternehmen, Vereine und Initiativen: Lassen Sie uns gemeinsam etwas für Dortmund bewegen.", VEREIN["messenger"], "Kontakt aufnehmen", ext=True)}''', "Partner von ACoD: FreiwilligenAgentur Dortmund, Ausschuss für Chancengerechtigkeit und Integration, MIA-DO-KI.")

    # Was wir tun
    def topic(t, i):
        proj = next((p for p in PROJEKTE if p["slug"] == t.get("projekt")), None)
        links = []
        if t.get("href"):
            links.append(f'<a class="btn btn-green" href="{t["href"]}">Mehr zum politischen Engagement</a>')
        if proj:
            links.append(f'<a class="btn btn-ghost" href="projekt-{proj["slug"]}.html" style="color:var(--green)">Projekt: {e(proj["t"])}</a>')
        badge = '<div class="council-badge" aria-hidden="true"><span>Liste</span><b>4</b><small>Integrationsratswahl 2020</small></div>' if t["id"] == "politik" else ""
        return f'''<section class="topic" id="{t["id"]}">
  <div class="stack"><h2>{e(t["t"])}</h2><p class="lead">{e(t["kurz"])}</p>{badge}</div>
  <div class="prose"><p>{e(t["text"])}</p><ul class="goals">{"".join(f"<li>{e(x)}</li>" for x in t["punkte"])}</ul>{f'<div class="hero-actions" style="margin-top:.4rem">{"".join(links)}</div>' if links else ""}</div>
</section>'''
    page("was-wir-tun.html", "Was wir tun", page_head("Was wir tun", "Unsere Themenschwerpunkte",
         "Politisches Engagement, Beratung, Bildung, Kultur, Sport und nachhaltige Integration: Dafür setzt sich ACoD in Dortmund ein.",
         [("index.html", "Start"), (None, "Was wir tun")]) + f'''
<div class="wrap">
  <div class="section">{themes_grid()}</div>
  {"".join(topic(t, i) for i, t in enumerate(THEMEN))}
</div>
{cta("Machen Sie mit", "In jedem Schwerpunkt freuen wir uns über Unterstützung.", "mitmachen.html", "So machen Sie mit")}''', "Was ACoD tut: politisches Engagement, Beraten & begleiten, Bildung & Jugend, Kultur & Begegnung, Sport und nachhaltige Integration.")

    # Politisches Engagement
    bah = next(p for p in KOORDINATION if p["name"] == "Biraan S. N. J. Bah")
    page("politisches-engagement.html", "Politisches Engagement", page_head("Was wir tun", "Politisches Engagement",
         "Unsere Stimme in der Dortmunder Stadtpolitik: 2020 als Liste 4 im Integrationsrat, seit 2025 stimmberechtigt im Ausschuss für Chancengerechtigkeit und Integration.",
         [("index.html", "Start"), ("was-wir-tun.html", "Was wir tun"), (None, "Politisches Engagement")]) + f'''
<div class="wrap">
  <div class="section two-col">
    <div class="prose">
      <p class="eyebrow">Seit 2025</p>
      <h2>ACoD im Ausschuss für Chancengerechtigkeit und Integration</h2>
      <p>Am 14. September 2025 hat Dortmund den Ausschuss für Chancengerechtigkeit und Integration (ACI) gewählt. Er vertritt die Interessen der Menschen mit Einwanderungsgeschichte, berät Rat und Verwaltung der Stadt und entscheidet über die Förderung von Integrationsprojekten. Am 17. Dezember 2025 hat er seine Arbeit aufgenommen.</p>
      <p>ACoD ist dort mit Biraan S. N. J. Bah als stimmberechtigtem Mitglied vertreten.</p>
      <h2>Wofür wir uns einsetzen</h2>
      <ul class="goals">
        <li>Mehr Beratung in afrikanischen Sprachen, Englisch und Französisch bei Ämtern</li>
        <li>Faire Chancen in Schule, Ausbildung und auf dem Arbeitsmarkt</li>
        <li>Schnellere Anerkennung ausländischer Abschlüsse</li>
        <li>Eine klare Haltung gegen Rassismus und Diskriminierung</li>
        <li>Räume und Förderung für Vereine der afrikanischen Community</li>
      </ul>
    </div>
    <aside class="stack">
      <div class="box vertretung"><p class="eyebrow">Unsere Vertretung</p>{person_card(bah)}</div>
      <div class="box"><h3>Der ACI bei der Stadt Dortmund</h3><p class="empty">Sitzungen, Mitglieder und Förderrichtlinien des Ausschusses.</p><a class="btn btn-green" href="{PARTNER[1]["url"]}" {EXT}>Zur Seite der Stadt</a></div>
    </aside>
  </div>
  <div class="section two-col">
    <figure class="flyer"><img src="assets/img/flyer-integrationsratswahl-2020.jpg" alt="Wahlplakat: ACoD im Integrationsrat der Stadt Dortmund, die Wahlliste der Afrikanischen Community in Dortmund, Liste 4, Integrationsratswahl am 13. September 2020" width="960" height="448"><figcaption>Unser Wahlaufruf zur Integrationsratswahl am 13. September 2020</figcaption></figure>
    <div class="prose">
      <p class="eyebrow">2020</p>
      <h2>Liste 4 bei der Integrationsratswahl</h2>
      <p>Am 13. September 2020 ist ACoD als Wahlliste der Afrikanischen Community zur Integrationsratswahl der Stadt Dortmund angetreten, unter dem Motto „Wir sind eine Gemeinschaft!“. Damit hat die afrikanische Community zum ersten Mal mit einer eigenen Liste kandidiert.</p>
      <p class="langs" lang="mul">{LANGS}</p>
    </div>
  </div>
  <div class="section">
    <h2>Partner in der Stadtpolitik</h2>
    <div class="partners">{partner_card(PARTNER[1])}{partner_card(PARTNER[2])}</div>
  </div>
</div>
{cta("Ihre Anliegen gehören in die Stadtpolitik", "Was muss sich in Dortmund ändern? Schreiben Sie uns, wir tragen es in den Ausschuss.", VEREIN["messenger"], "Anliegen schicken", ext=True)}''', "Politisches Engagement von ACoD: Liste 4 bei der Integrationsratswahl 2020, seit 2025 stimmberechtigt im Ausschuss für Chancengerechtigkeit und Integration Dortmund.")

    # Projekte
    page("projekte.html", "Projekte", page_head("Projekte", "Unsere Projekte",
         "Was gerade läuft und was wir bereits abgeschlossen haben.",
         [("index.html", "Start"), (None, "Projekte")]) + f'''
<div class="wrap"><div class="section">
  <div class="filters" role="group" aria-label="Projekte filtern">
    <button type="button" data-filter="alle" aria-pressed="true">Alle ({len(PROJEKTE)})</button>
    <button type="button" data-filter="laufend" aria-pressed="false">Laufende Projekte ({len(laufend)})</button>
    <button type="button" data-filter="abgeschlossen" aria-pressed="false">Abgeschlossene Projekte ({len(abgeschlossen)})</button>
  </div>
  <div class="projects">{"".join(project_card(p) for p in PROJEKTE)}</div>
</div></div>
{cta("Projekte brauchen Unterstützung", "Mit einer Spende oder Ihrer Zeit helfen Sie, dass unsere Projekte weitergehen.", "spenden.html", "Jetzt unterstützen")}''',
         "Laufende und abgeschlossene Projekte von ACoD in Dortmund.")

    for p in PROJEKTE:
        done = p["s"] == "abgeschlossen"
        tun = "".join(f"<li>{e(x)}</li>" for x in p["tun"])
        ziele = "".join(f"<li>{e(x)}</li>" for x in p["ziele"])
        art = f'<img src="{p["img"]}" alt="Wahlplakat zur Integrationsratswahl 2020" style="width:100%;border-radius:16px">' if p.get("img") else \
            f'<div class="detail-art {p["art"]}" role="img" aria-label="Musterbild zum Projekt {e(p["t"])}"><span class="status">Laufend</span></div>'
        support = (f'<div class="box"><h3>Mitmachen</h3><p class="empty">{e(p["mitmachen"])}</p><a class="btn btn-donate" href="{VEREIN["messenger"]}" {EXT}>Nachricht schreiben</a></div>'
                   f'<div class="box"><h3>Unterstützen</h3><p class="empty">Ihre Spende hilft diesem Projekt direkt.</p><a class="btn btn-green" href="spenden.html">Spenden</a></div>') if not done else \
            '<div class="box"><h3>Weitermachen</h3><p class="empty">Dieses Projekt ist abgeschlossen. Ihre Unterstützung hilft unseren laufenden Projekten.</p><a class="btn btn-green" href="projekte.html#laufend">Laufende Projekte</a></div>'
        others = [o for o in PROJEKTE if o["slug"] != p["slug"]][:3]
        page(f"projekt-{p['slug']}.html", p["t"], page_head(("Abgeschlossenes" if done else "Laufendes") + " Projekt · " + p["cat"], p["t"], p["d"],
             [("index.html", "Start"), ("projekte.html", "Projekte"), ("projekte.html#" + p["s"], "Abgeschlossene Projekte" if done else "Laufende Projekte"), (None, p["t"])]) + f'''
<div class="wrap">
  <div class="detail">
    <div class="prose">
      {art}
      <h2>Ausgangslage</h2><p>{e(p["lage"])}</p>
      <h2>{"Was wir gemacht haben" if done else "Was wir tun"}</h2><ul>{tun}</ul>
      <h2>{"Was daraus geworden ist" if done else "Was wir erreichen wollen"}</h2><ul class="goals">{ziele}</ul>
    </div>
    <aside class="aside">
      <div class="box"><h3>Auf einen Blick</h3><dl class="kv"><dt>Status</dt><dd>{"Abgeschlossen" if done else "Laufend"}</dd><dt>Bereich</dt><dd>{e(p["cat"])}</dd><dt>Ort</dt><dd>Dortmund</dd></dl></div>
      {support}
    </aside>
  </div>
  <div class="section"><h2>Weitere Projekte</h2><div class="projects">{"".join(project_card(o) for o in others)}</div></div>
</div>''', f"{p['t']}: {p['d']}")

    # Aktuelles
    page("aktuelles.html", "Aktuelles", page_head("Aktuelles", "Neuigkeiten & Termine",
         "Neues aus der Community. Termine und Veranstaltungen kündigen wir auf Facebook an.",
         [("index.html", "Start"), (None, "Aktuelles")]) + f'''
<div class="wrap"><div class="section two-col">
  <div class="news">{news_html(NEWS)}</div>
  <div class="stack">
    <div class="box"><h3>Termine</h3><p class="empty">Feste, Treffen und Infoabende kündigen wir auf unserer Facebook-Seite an. Folgen Sie uns, dann verpassen Sie nichts.</p><a class="btn btn-donate" href="{VEREIN['facebook']}" {EXT}>Termine auf Facebook</a></div>
    <div class="box"><h3>Bilder &amp; Videos</h3><p class="empty">Eindrücke aus Wahlkampf, Festen und Projekten.</p><a class="btn btn-green" href="galerie.html">Zur Galerie</a></div>
  </div>
</div></div>''', "Neuigkeiten und Termine von ACoD – Afrikanische Community in Dortmund.")

    # Galerie
    page("galerie.html", "Bilder & Videos", page_head("Aktuelles", "Bilder & Videos",
         "Eindrücke aus der Community. Die meisten Fotos und Videos teilen wir auf Facebook.",
         [("index.html", "Start"), ("aktuelles.html", "Aktuelles"), (None, "Bilder & Videos")]) + f'''
<div class="wrap">
  <div class="section">
    <div class="gallery">
      <figure class="tile wide"><img src="assets/img/gruppenfoto-2020.jpg" alt="Gruppenfoto von ACoD 2020" width="785" height="278"><figcaption>Unser Team zur Integrationsratswahl 2020</figcaption></figure>
      <figure class="tile"><img src="assets/img/flyer-integrationsratswahl-2020.jpg" alt="Wahlplakat Liste 4" width="960" height="448" style="object-fit:contain;background:var(--surface)"><figcaption>Wahlaufruf 2020</figcaption></figure>
    </div>
  </div>
  <div class="section cards3">
    <div class="card"><h3>Fotos</h3><p>Alle Fotoalben auf unserer Facebook-Seite.</p><a class="btn btn-green" href="{FB_PHOTOS}" {EXT}>Fotos ansehen</a></div>
    <div class="card"><h3>Videos</h3><p>Wahlaufrufe, Feste und Beiträge aus dem Vereinsleben.</p><a class="btn btn-green" href="{FB_VIDEOS}" {EXT}>Videos ansehen</a></div>
    <div class="card"><h3>Folgen</h3><p>Neue Bilder und Termine direkt in Ihrem Feed.</p><a class="btn btn-donate" href="{VEREIN['facebook']}" {EXT}>ACoD auf Facebook</a></div>
  </div>
</div>''', "Bilder und Videos von ACoD – Afrikanische Community in Dortmund.")

    # Mitmachen
    page("mitmachen.html", "Mitmachen", page_head("Mitmachen", "Werden Sie Teil der Gemeinschaft.",
         "Mitglied werden, Zeit schenken oder gemeinsam Projekte entwickeln: Es gibt viele Wege, ACoD zu unterstützen.",
         [("index.html", "Start"), (None, "Mitmachen")]) + f'''
<div class="wrap">
  <div class="section cards3">
    <div class="card"><h3>Mitglied werden</h3><p>Mitglieder tragen die Gemeinschaft, reden mit und gestalten unsere Arbeit. Schreiben Sie uns, wir erklären Ihnen alles Weitere.</p></div>
    <div class="card"><h3>Ehrenamtlich helfen</h3><p>Hausaufgabenhilfe, Übersetzen, Begleiten oder Feste organisieren: Jede Stunde zählt, ganz gleich welche Herkunft Sie haben.</p></div>
    <div class="card"><h3>Kooperieren</h3><p>Schulen, Unternehmen, Vereine und Initiativen: Lassen Sie uns gemeinsame Projekte in Dortmund entwickeln.</p></div>
  </div>
  <div class="section two-col">
    <div class="prose">
      <h2>Wo wir Hilfe brauchen</h2>
      <ul class="goals">
        <li>Lesepatinnen und Lesepaten für die Lernbrücke</li>
        <li>Willkommenslotsen mit Sprachkenntnissen</li>
        <li>Helferinnen und Helfer für Feste und Treffen</li>
        <li>Menschen mit Erfahrung in Öffentlichkeitsarbeit, Fotografie oder Video</li>
      </ul>
    </div>
    {write_box("Sagen Sie uns kurz, wie Sie mitmachen möchten. Wir melden uns bei Ihnen.")}
  </div>
</div>''', "Mitglied werden, ehrenamtlich helfen und kooperieren bei ACoD in Dortmund.")

    # Spenden
    bank = f'''<dl class="bank"><dt>Kontoinhaber</dt><dd>{e(VEREIN["kontoinhaber"] or "ACoD – " + VEREIN["lang"])}</dd><dt>IBAN</dt><dd><span id="iban">{e(VEREIN["iban"])}</span><button class="copy" type="button" data-copy="iban">Kopieren</button></dd><dt>Verwendungszweck</dt><dd>Spende + ggf. Projektname</dd></dl>''' if VEREIN["iban"] else \
        f'''<div class="box"><h3>Bankverbindung anfragen</h3><p class="empty">Schreiben Sie uns kurz über Facebook. Wir senden Ihnen die Bankverbindung und beantworten gern Ihre Fragen.</p><a class="btn btn-donate" href="{VEREIN['messenger']}" {EXT}>Nachricht schreiben</a></div>'''
    page("spenden.html", "Spenden", page_head("Spenden", "Ihre Spende wirkt in Dortmund.",
         "Mit Ihrer Spende unterstützen Sie Bildung, Begleitung und Begegnung für Familien afrikanischer Herkunft.",
         [("index.html", "Start"), (None, "Spenden")]) + f'''
<div class="donate-band"><div class="wrap donate-grid">
  <div class="stack" style="gap:1.2rem">
    <h2>Wofür Ihre Spende eingesetzt wird</h2>
    <ul class="uses">
      <li><b>Lernen</b><span>Material und Begleitung für Kinder in der Lernbrücke</span></li>
      <li><b>Ankommen</b><span>Begleitung neu angekommener Familien durch Willkommenslotsen</span></li>
      <li><b>Begegnen</b><span>Feste, Kochabende und Treffen für die ganze Stadt</span></li>
    </ul>
  </div>
  <div class="stack">
    <h2>So spenden Sie</h2>
    {bank}
  </div>
</div></div>
<div class="wrap"><div class="section">
  <h2>Häufige Fragen</h2>
  <div class="faq">
    <details><summary>Kann ich für ein bestimmtes Projekt spenden?</summary><p>Ja. Nennen Sie uns das Projekt, zum Beispiel die Lernbrücke. Wir setzen Ihre Spende dann dafür ein.</p></details>
    <details><summary>Bekomme ich eine Spendenbestätigung?</summary><p>Bitte sprechen Sie uns an. Wir sagen Ihnen, welche Bestätigung wir für Ihre Spende ausstellen können.</p></details>
    <details><summary>Kann ich auch Sachspenden geben?</summary><p>Gern, vor allem Schulmaterial, Kinderbücher und Laptops. Bitte melden Sie sich vorher, damit wir planen können.</p></details>
    <details><summary>Wie kann ich ohne Geld helfen?</summary><p>Mit Ihrer Zeit. Auf der Seite <a href="mitmachen.html">Mitmachen</a> finden Sie, wo wir Unterstützung brauchen.</p></details>
  </div>
</div></div>''', "Spenden für ACoD – Afrikanische Community in Dortmund: Bildung, Begleitung und Begegnung unterstützen.")

    # Kontakt
    extra = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [
        ("Adresse", e(VEREIN["adresse"])), ("E-Mail", f'<a href="mailto:{e(VEREIN["mail"])}">{e(VEREIN["mail"])}</a>' if VEREIN["mail"] else ""), ("Telefon", e(VEREIN["tel"]))] if v)
    page("kontakt.html", "Kontakt", page_head("Kontakt", "Schreiben Sie uns.",
         "Am schnellsten erreichen Sie uns über Facebook. Wir antworten auf Deutsch, Englisch oder Französisch.",
         [("index.html", "Start"), (None, "Kontakt")]) + f'''
<div class="wrap"><div class="section two-col">
  <dl class="contact-list">
    <div><dt>Name</dt><dd>ACoD – {VEREIN['lang']}</dd></div>
    <div><dt>Ort</dt><dd>Dortmund</dd></div>
    {extra}
    <div><dt>Facebook</dt><dd><a href="{VEREIN['facebook']}" {EXT}>facebook.com/ACoD2020</a></dd></div>
  </dl>
  {write_box()}
</div></div>''', "Kontakt zu ACoD – Afrikanische Community in Dortmund.")

    # Impressum
    def val(k, fallback="wird ergänzt"):
        return e(VEREIN[k]) if VEREIN[k] else f"<em>{fallback}</em>"
    page("impressum.html", "Impressum", page_head("Rechtliches", "Impressum", "Angaben gemäß § 5 DDG",
         [("index.html", "Start"), (None, "Impressum")]) + f'''
<div class="wrap"><div class="section legal-text">
  <h2>Anbieter</h2>
  <p>ACoD – {VEREIN['lang']}<br>{val("adresse")}</p>
  <h2>Vertreten durch</h2>
  <p>{val("vertreten")}</p>
  <h2>Kontakt</h2>
  <p>E-Mail: {val("mail")}<br>Facebook: <a href="{VEREIN['facebook']}" {EXT}>facebook.com/ACoD2020</a></p>
  {f"<h2>Registereintrag</h2><p>{e(VEREIN['register'])}</p>" if VEREIN["register"] else ""}
  <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
  <p>{val("vertreten")}</p>
  <h2>Haftung für Links</h2>
  <p>Unsere Website enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter verantwortlich.</p>
</div></div>''', "Impressum von ACoD – Afrikanische Community in Dortmund.")

    # Datenschutz
    page("datenschutz.html", "Datenschutz", page_head("Rechtliches", "Datenschutzerklärung", "Wie wir mit Ihren Daten umgehen.",
         [("index.html", "Start"), (None, "Datenschutz")]) + f'''
<div class="wrap"><div class="section legal-text">
  <h2>1. Verantwortlich</h2>
  <p>ACoD – {VEREIN['lang']}, {val("adresse", "Dortmund")}. Kontakt: {val("mail", "über Facebook")}</p>
  <h2>2. Hosting</h2>
  <p>Diese Website wird über GitHub Pages (GitHub Inc., USA) bereitgestellt. Beim Aufruf verarbeitet der Anbieter technisch notwendige Daten wie IP-Adresse, Datum, Uhrzeit und aufgerufene Seite, um die Website auszuliefern und zu schützen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.</p>
  <h2>3. Schriftarten</h2>
  <p>Diese Website lädt Schriftarten von Google Fonts (Google Ireland Ltd.). Dabei wird Ihre IP-Adresse an Google übertragen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO, unser Interesse an einer einheitlichen Darstellung.</p>
  <h2>4. Keine Formulare, keine Cookies</h2>
  <p>Diese Website setzt keine Cookies, nutzt keine Analyse-Werkzeuge und enthält keine Formulare.</p>
  <h2>5. Links zu Facebook</h2>
  <p>Wir verlinken auf unsere Facebook-Seite und den Facebook Messenger. Erst wenn Sie einen dieser Links anklicken, werden Daten an Meta Platforms Ireland Ltd. übertragen. Dort gilt die Datenschutzerklärung von Meta.</p>
  <h2>6. Ihre Rechte</h2>
  <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht auf Beschwerde bei einer Aufsichtsbehörde, zum Beispiel der Landesbeauftragten für Datenschutz und Informationsfreiheit NRW.</p>
</div></div>''', "Datenschutzerklärung von ACoD – Afrikanische Community in Dortmund.")


if __name__ == "__main__":
    build()
    print("\n".join(sorted(p.name for p in OUT.glob("*.html"))))
