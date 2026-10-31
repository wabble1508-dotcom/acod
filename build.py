"""Erzeugt die statische Website von ACoD e.V. im Ordner site/.

Alle Inhalte (Projekte, News, Termine, Vorstand, Kontakt) stehen oben in diesem
Skript. Texte hier ändern, dann `python3 build.py` ausführen und den Ordner
site/ auf den Webspace hochladen.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).parent / "docs"

# ---------------------------------------------------------------- Vereinsdaten
VEREIN = {
    "name": "ACoD e.V.",
    "lang": "Afrikanische Community in Dortmund e.V.",
    "strasse": "Musterstraße 1",
    "ort": "44135 Dortmund",
    "mail": "info@acod-dortmund.de",
    "tel": "0231 000 000 00",
    "sprechstunde": "Dienstags 17–19 Uhr und nach Vereinbarung",
    "iban": "DE00 0000 0000 0000 0000 00",
    "bic": "XXXXDEXXXXX",
    "bank": "Bank (Platzhalter)",
    "register": "Amtsgericht Dortmund, VR 00000",
    "facebook": "https://www.facebook.com/ACoD2020/",
}

VORSTAND = [
    ("V1", "Name Vorsitz", "1. Vorsitzende/r"),
    ("V2", "Name Stellvertretung", "2. Vorsitzende/r"),
    ("K", "Name Kasse", "Kassenwart/in"),
    ("S", "Name Schriftführung", "Schriftführer/in"),
    ("J", "Name Jugend", "Jugendbeauftragte/r"),
    ("B", "Name Beratung", "Koordination Beratung"),
    ("Ku", "Name Kultur", "Koordination Kultur"),
    ("Ö", "Name Öffentlichkeit", "Presse & Social Media"),
]

PROJEKTE = [
    {
        "slug": "lernbruecke", "t": "Lernbrücke", "s": "laufend", "art": "art-a",
        "cat": "Bildung & Jugend", "time": "seit 09/2024", "ort": "Dortmund-Nordstadt",
        "d": "Wöchentliche Hausaufgabenhilfe und Lesepatenschaften für Kinder aus afrikanischen Familien in der Nordstadt.",
        "lage": "Viele Kinder aus zugewanderten Familien wachsen mehrsprachig auf. Zu Hause fehlt oft die Zeit oder das Wissen über das deutsche Schulsystem, um bei Hausaufgaben zu helfen.",
        "tun": ["Hausaufgabenhilfe jeden Mittwoch und Samstag für die Klassen 1 bis 7",
                "Lesepatenschaften: eine Stunde pro Woche, ein Kind, ein Buch",
                "Elternabende zum Schulsystem in mehreren Sprachen",
                "Ferienprogramm mit Ausflügen in Dortmunder Museen und Bibliotheken"],
        "ziele": ["30 Kinder regelmäßig begleiten", "15 ausgebildete Lesepatinnen und -paten", "Zwei Elternabende pro Halbjahr"],
        "partner": "Grundschulen der Nordstadt, Stadtbibliothek Dortmund (geplant)",
        "goal": 6000, "raised": 4150,
    },
    {
        "slug": "willkommenslotsen", "t": "Willkommenslotsen", "s": "laufend", "art": "art-b",
        "cat": "Beratung & Begleitung", "time": "seit 03/2023", "ort": "ganz Dortmund",
        "d": "Neu angekommene Familien werden von erfahrenen Community-Mitgliedern zu Ämtern, Ärzten und Schulen begleitet.",
        "lage": "Wer neu in Deutschland ist, steht vor Formularen, Terminen und Fristen in einer fremden Sprache. Fehler kosten Zeit, Geld und Nerven.",
        "tun": ["Begleitung zu Behörden, Jobcenter, Arztpraxen und Schulen",
                "Übersetzung u. a. in Englisch, Französisch, Twi, Yoruba, Lingala und Swahili",
                "Offene Sprechstunde jeden Dienstag",
                "Schulung neuer Lotsinnen und Lotsen zweimal im Jahr"],
        "ziele": ["100 Begleitungen pro Jahr", "20 aktive Lotsinnen und Lotsen", "Kooperation mit drei Beratungsstellen"],
        "partner": "Integrationsnetzwerk Dortmund (geplant)",
        "goal": 4000, "raised": 1720,
    },
    {
        "slug": "afrika-tag", "t": "Afrika-Tag Dortmund", "s": "laufend", "art": "art-c",
        "cat": "Kultur & Begegnung", "time": "jährlich im Mai", "ort": "Dortmunder Innenstadt",
        "d": "Ein Fest mit Musik, Essen, Mode und Gesprächen, das afrikanische Kulturen in der Stadtmitte sichtbar macht.",
        "lage": "Afrikanische Kulturen sind in Dortmund vielfältig vertreten, im Stadtbild aber kaum sichtbar. Begegnung baut Vorurteile ab.",
        "tun": ["Bühnenprogramm mit Musik, Tanz und Modenschau",
                "Essensstände von Community-Mitgliedern",
                "Podiumsgespräch zu Teilhabe und Rassismus",
                "Kinderprogramm mit Geschichten und Trommelworkshop"],
        "ziele": ["2.000 Besucherinnen und Besucher", "20 beteiligte Vereine und Gruppen", "Ein Fest, das jedes Jahr wiederkommt"],
        "partner": "Partnervereine der afrikanischen Community",
        "goal": 8000, "raised": 2600,
    },
    {
        "slug": "frauen-staerken", "t": "Frauen stärken", "s": "abgeschlossen", "art": "art-d",
        "cat": "Empowerment", "time": "2023 – 2024", "ort": "Vereinsraum",
        "d": "Workshopreihe zu Bewerbung, Selbstständigkeit und Gesundheit für Frauen afrikanischer Herkunft.",
        "lage": "Frauen mit Migrationsgeschichte haben es auf dem Arbeitsmarkt besonders schwer, auch mit guten Abschlüssen aus dem Herkunftsland.",
        "tun": ["12 Workshops zu Bewerbung, Anerkennung von Abschlüssen und Gründung",
                "Gesundheitsabende mit einer Ärztin",
                "Kinderbetreuung während aller Termine"],
        "ziele": ["85 Teilnehmerinnen erreicht", "Mehrere Teilnehmerinnen haben eine Ausbildung oder Arbeit begonnen", "Ein Netzwerk, das sich weiter trifft"],
        "partner": "Ehrenamtliche Referentinnen",
    },
    {
        "slug": "corona-hilfe", "t": "Corona-Hilfe 2020", "s": "abgeschlossen", "art": "art-e",
        "cat": "Soforthilfe", "time": "2020 – 2021", "ort": "ganz Dortmund",
        "d": "Übersetzte Informationen, Einkaufshilfe und Lebensmittelpakete während der Pandemie, das Gründungsprojekt des Vereins.",
        "lage": "Im Frühjahr 2020 erreichten viele Corona-Regeln die Community nur auf Deutsch. Ältere und Kranke konnten nicht mehr selbst einkaufen.",
        "tun": ["Übersetzung der Corona-Regeln in mehrere Sprachen",
                "Einkaufshilfe für Risikogruppen",
                "Lebensmittelpakete für Familien in Not"],
        "ziele": ["Aus der Nachbarschaftshilfe ist ACoD als eingetragener Verein entstanden"],
        "partner": "Nachbarinnen und Nachbarn",
    },
    {
        "slug": "fussball-verbindet", "t": "Fußball verbindet", "s": "abgeschlossen", "art": "art-f",
        "cat": "Sport & Jugend", "time": "Sommer 2022", "ort": "Sportpark Dortmund",
        "d": "Ein Turnier mit Jugendteams aus Dortmunder Vereinen und der Community.",
        "lage": "Sport bringt Jugendliche zusammen, die sich im Alltag selten begegnen.",
        "tun": ["Turnier mit 16 gemischten Jugendteams", "Fair-Play-Workshop vor dem Anpfiff", "Abschlussfest im Park"],
        "ziele": ["16 Teams und über 200 Gäste", "Neue Kontakte zu Dortmunder Sportvereinen"],
        "partner": "Dortmunder Jugendfußballvereine",
    },
]

NEWS = [
    ("14.10.2026", "Projekte", "Lernbrücke sucht neue Lesepaten", "Für das Wintersemester suchen wir Ehrenamtliche, die eine Stunde pro Woche mit Kindern lesen. Vorkenntnisse sind nicht nötig, wir bereiten Sie in einem kurzen Workshop vor."),
    ("28.09.2026", "Verein", "Rückblick: Mitgliederversammlung", "Der Vorstand wurde bestätigt und das Jahresprogramm 2027 beschlossen. Neu dabei: eine Arbeitsgruppe für Jugendliche."),
    ("02.09.2026", "Kooperation", "Zusammenarbeit mit Dortmunder Grundschulen", "Drei Schulen in der Nordstadt arbeiten künftig mit unseren Willkommenslotsen zusammen."),
    ("15.06.2026", "Kultur", "Afrika-Tag mit über 1.500 Gästen", "Musik, Essen und viele Gespräche: Danke an alle Helferinnen und Helfer, die den Tag möglich gemacht haben."),
    ("03.04.2026", "Spenden", "Danke für 2.000 € beim Frühjahrsaufruf", "Mit Ihrer Hilfe finanzieren wir Lernmaterial und das Ferienprogramm der Lernbrücke."),
]

TERMINE = [
    ("08", "Nov", "2026", "Offener Kochabend", "18:00 Uhr · Vereinsraum, Dortmund-Nordstadt", "Wir kochen gemeinsam Gerichte aus Ghana und Kamerun. Eintritt frei, Spenden willkommen."),
    ("22", "Nov", "2026", "Infoabend Schule & Ausbildung", "17:30 Uhr · auf Deutsch, Englisch und Französisch", "Wie funktioniert das Schulsystem? Welche Wege führen in eine Ausbildung?"),
    ("13", "Dez", "2026", "Jahresabschlussfest", "16:00 Uhr · für Mitglieder, Familien und Freunde", "Rückblick, Musik und Essen zum Jahresende."),
    ("17", "Jan", "2027", "Schulung für Willkommenslotsen", "10:00–15:00 Uhr · Vereinsraum", "Für alle, die neu als Lotsin oder Lotse einsteigen möchten. Anmeldung per E-Mail."),
]

# ---------------------------------------------------------------- Navigation
NAV = [
    ("index.html", "Start", []),
    ("ueber-uns.html", "Über uns", [("ueber-uns.html", "Verein & Geschichte"), ("vorstand.html", "Vorstand & Team"), ("transparenz.html", "Finanzen & Transparenz")]),
    ("integrationsrat.html", "Integrationsrat", []),
    ("projekte.html", "Projekte", [("projekte.html#laufend", "Laufende Projekte"), ("projekte.html#abgeschlossen", "Abgeschlossene Projekte"), ("projekte.html", "Alle Projekte")]),
    ("aktuelles.html", "Aktuelles", [("aktuelles.html", "Neuigkeiten"), ("termine.html", "Termine"), ("galerie.html", "Bilder & Videos")]),
    ("mitmachen.html", "Mitmachen", [("mitmachen.html#mitglied", "Mitglied werden"), ("mitmachen.html#ehrenamt", "Ehrenamt"), ("mitmachen.html#kooperation", "Kooperationen")]),
    ("kontakt.html", "Kontakt", []),
]
SECTION_OF = {"vorstand.html": "ueber-uns.html", "transparenz.html": "ueber-uns.html", "termine.html": "aktuelles.html", "galerie.html": "aktuelles.html"}
SECTION_OF.update({f"projekt-{p['slug']}.html": "projekte.html" for p in PROJEKTE})

WORDMARK = '<span class="wordmark" aria-hidden="true">AC<span class="o-check">o<svg viewBox="0 0 40 40"><path d="M6 21 L16 31 L36 6"/></svg></span>D</span>'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:wght@400;600;700&display=swap">'

e = escape


def nav_html(current):
    active = SECTION_OF.get(current, current)
    items = []
    for href, label, sub in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if sub:
            subs = "".join(f'<li><a href="{h}">{e(l)}</a></li>' for h, l in sub)
            items.append(f'<li class="has-sub"><a href="{href}"{cur}>{e(label)}</a><ul class="sub">{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{e(label)}</a></li>')
    return "".join(items)


def header(current):
    return f'''<div class="topbar"><div class="wrap">
  <a href="termine.html">Termine</a><a href="mitmachen.html#mitglied">Mitglied werden</a><a href="kontakt.html">Kontakt</a>
  <a href="{VEREIN['facebook']}" target="_blank" rel="noopener">Facebook</a>
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
<div class="pattern" aria-hidden="true"></div>
<div class="notice"><div class="wrap">Entwurf: Texte, Zahlen, Namen und Bankdaten sind Platzhalter und müssen vom Verein ersetzt werden.</div></div>'''


def footer():
    return f'''<div class="pattern" aria-hidden="true"></div>
<footer>
  <div class="wrap grid">
    <div class="stack" style="gap:.6rem">
      <h3>{VEREIN['name']}</h3>
      <p>{VEREIN['lang']}<br>{VEREIN['strasse']}, {VEREIN['ort']}<br>{VEREIN['mail']}</p>
      <p>Spendenkonto: {VEREIN['iban']}</p>
    </div>
    <div><h3>Verein</h3><ul><li><a href="ueber-uns.html">Über uns</a></li><li><a href="vorstand.html">Vorstand &amp; Team</a></li><li><a href="transparenz.html">Finanzen &amp; Transparenz</a></li><li><a href="aktuelles.html">Aktuelles</a></li><li><a href="termine.html">Termine</a></li></ul></div>
    <div><h3>Projekte</h3><ul><li><a href="projekte.html#laufend">Laufende Projekte</a></li><li><a href="projekte.html#abgeschlossen">Abgeschlossene Projekte</a></li>{"".join(f'<li><a href="projekt-{p["slug"]}.html">{e(p["t"])}</a></li>' for p in PROJEKTE if p["s"] == "laufend")}</ul></div>
    <div><h3>Unterstützen</h3><ul><li><a href="spenden.html">Spenden</a></li><li><a href="mitmachen.html#mitglied">Mitglied werden</a></li><li><a href="mitmachen.html#ehrenamt">Ehrenamt</a></li><li><a href="kontakt.html">Kontakt</a></li><li><a href="{VEREIN['facebook']}" target="_blank" rel="noopener">Facebook</a></li></ul></div>
  </div>
  <div class="legal"><div class="wrap"><span>© 2026 {VEREIN['lang']}</span><span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span></div></div>
</footer>
<script src="assets/main.js"></script>'''


def page(filename, title, body, description):
    full_title = "ACoD Dortmund" if filename == "index.html" else f"{title} · ACoD Dortmund"
    head = f'''<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<link rel="stylesheet" href="assets/style.css">'''
    content = f"{header(filename)}\n<main id=\"inhalt\">\n{body}\n</main>\n{footer()}\n"
    full = f'<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body>\n{content}</body>\n</html>\n'
    (OUT / filename).write_text(full, encoding="utf-8")
    if filename == "index.html":
        # Variante ohne Dokumentgerüst für die Artifact-Vorschau
        (OUT.parent / "preview-index.html").write_text(f"{head}\n{content}", encoding="utf-8")


def page_head(eyebrow, title, lead, crumbs):
    c = " / ".join(f'<a href="{h}">{e(l)}</a>' if h else e(l) for h, l in crumbs)
    return f'''<div class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Pfad">{c}</nav>
  <p class="eyebrow">{e(eyebrow)}</p>
  <h1>{e(title)}</h1>
  <p class="lead">{e(lead)}</p>
</div></div>'''


# ---------------------------------------------------------------- Bausteine
def project_card(p):
    done = p["s"] == "abgeschlossen"
    prog = ""
    if p.get("goal"):
        pct = round(p["raised"] / p["goal"] * 100)
        prog = f'<div class="progress"><div class="progress-bar" role="progressbar" aria-label="Spendenstand" aria-valuemin="0" aria-valuemax="{p["goal"]}" aria-valuenow="{p["raised"]}"><i style="width:{pct}%"></i></div><span>{eur(p["raised"])} von {eur(p["goal"])} gesammelt</span></div>'
    return f'''<a class="project" href="projekt-{p["slug"]}.html" data-status="{p["s"]}">
  <div class="project-art {p["art"]}"><span class="status{" done" if done else ""}">{"Abgeschlossen" if done else "Laufend"}</span></div>
  <div class="project-body"><div class="project-meta"><span>{e(p["cat"])}</span><span>{e(p["time"])}</span></div><h3>{e(p["t"])}</h3><p>{e(p["d"])}</p>{prog}<span class="more">Zum Projekt →</span></div>
</a>'''


def eur(n):
    return f"{n:,}".replace(",", ".") + " €"


def news_html(items):
    return "".join(f'<article><time>{d} · {e(c)}</time><h3>{e(t)}</h3><p>{e(x)}</p></article>' for d, c, t, x in items)


def events_html(items, long=False):
    out = []
    for day, mon, year, t, meta, desc in items:
        extra = f"<p>{e(desc)}</p>" if long else ""
        out.append(f'<div class="event"><div class="event-date"><b>{day}</b><span>{mon}</span></div><div><h3>{e(t)}</h3><p>{e(meta)}</p>{extra}</div></div>')
    return "".join(out)


def cta(title, text, href="spenden.html", label="Jetzt spenden"):
    return f'<div class="wrap section"><div class="cta"><div><h2>{e(title)}</h2><p>{e(text)}</p></div><a class="btn btn-donate" href="{href}">{e(label)}</a></div></div>'


USES = '''<ul class="uses">
  <li><b>25 €</b><span>finanzieren eine Woche Hausaufgabenhilfe für ein Kind</span></li>
  <li><b>50 €</b><span>decken Material für einen Sprach- und Bewerbungsworkshop</span></li>
  <li><b>120 €</b><span>ermöglichen einen Begegnungsabend für 40 Gäste</span></li>
</ul>'''


# ---------------------------------------------------------------- Seiten
def build():
    OUT.mkdir(exist_ok=True)
    laufend = [p for p in PROJEKTE if p["s"] == "laufend"]
    abgeschlossen = [p for p in PROJEKTE if p["s"] == "abgeschlossen"]

    # Start
    page("index.html", "Start", f'''
<div class="hero"><div class="wrap">
  <div>
    <p class="eyebrow">Afrikanische Community in Dortmund · seit 2020</p>
    <h1>Zusammen ankommen. Zusammen gestalten.</h1>
    <p class="lead">Wir verbinden Menschen afrikanischer Herkunft in Dortmund, begleiten Familien beim Ankommen und bauen Brücken zwischen Kulturen, Generationen und Kontinenten.</p>
    <div class="hero-actions"><a class="btn btn-donate" href="spenden.html">Jetzt spenden</a><a class="btn btn-ghost" href="projekte.html">Unsere Projekte</a></div>
  </div>
  <figure class="hero-photo">
    <img src="assets/img/gruppenfoto-2020.jpg" alt="Mitglieder von ACoD stehen gemeinsam auf einer Treppe in Dortmund" width="785" height="278">
  </figure>
</div></div>
<div class="wrap">
  <div class="section">
    <div class="facts" aria-label="Der Verein in Zahlen">
      <div><b>2020</b><span>gegründet in Dortmund</span></div>
      <div><b>120+</b><span>Mitglieder &amp; Engagierte</span></div>
      <div><b>14</b><span>Herkunftsländer im Verein</span></div>
      <div><b>{len(PROJEKTE)}</b><span>Projekte seit Gründung</span></div>
    </div>
  </div>
  <div class="section council">
    <div class="stack">
      <p class="eyebrow">Politische Teilhabe</p>
      <h2>Unsere Stimme im Integrationsrat der Stadt Dortmund</h2>
      <p class="lead">ACoD ist als Wahlliste der Afrikanischen Community angetreten, zuerst als <b>Liste 4</b> bei der Integrationsratswahl am 13. September 2020. Wir bringen die Anliegen afrikanischer Familien dorthin, wo in Dortmund über Integration entschieden wird.</p>
      <p class="langs" lang="mul">Geh wählen! · Vote! · Allez voter! · <span lang="ar" dir="rtl">تعالوا و انتخبوا</span></p>
      <div><a class="btn btn-green" href="integrationsrat.html">Mehr zum Integrationsrat</a></div>
    </div>
    <a class="council-badge" href="integrationsrat.html" aria-label="Liste 4 bei der Integrationsratswahl 2020"><span>Liste</span><b>4</b><small>Integrationsratswahl 2020</small></a>
  </div>
  <div class="section">
    <p class="eyebrow">Was wir tun</p>
    <div class="pillars">
      <div class="pillar"><h3>Beraten &amp; begleiten</h3><p>Hilfe bei Behördengängen, Schule, Ausbildung und Wohnungssuche, in Deutsch, Englisch, Französisch und weiteren Sprachen.</p></div>
      <div class="pillar"><h3>Bildung &amp; Jugend</h3><p>Hausaufgabenhilfe, Mentoring und Workshops, damit junge Menschen ihre Wege in Dortmund selbstbewusst gehen.</p></div>
      <div class="pillar"><h3>Kultur &amp; Begegnung</h3><p>Feste, Kochabende und Diskussionen, die afrikanische Kulturen in der Stadt sichtbar machen und Nachbarschaft stiften.</p></div>
    </div>
  </div>
  <div class="section">
    <div class="section-head"><div class="stack" style="gap:.3rem"><p class="eyebrow">Laufende Projekte</p><h2>Woran wir gerade arbeiten</h2></div><a class="btn btn-ghost" href="projekte.html">Alle Projekte</a></div>
    <div class="projects">{"".join(project_card(p) for p in laufend)}</div>
  </div>
</div>
<div class="donate-band"><div class="wrap donate-grid">
  <div class="stack"><p class="eyebrow">Hilfe zur Selbsthilfe</p><h2>Jede Spende stärkt die Community vor Ort.</h2><p class="lead">ACoD arbeitet ehrenamtlich. Ihre Spende fließt direkt in Nachhilfe, Beratung und Begegnung in Dortmund.</p><div><a class="btn btn-donate" href="spenden.html">Spenden</a></div></div>
  {USES}
</div></div>
<div class="wrap"><div class="section two-col">
  <div class="stack"><div class="section-head"><p class="eyebrow">Aktuelles</p><a href="aktuelles.html">Alle Neuigkeiten →</a></div><div class="news">{news_html(NEWS[:3])}</div></div>
  <div class="stack"><div class="section-head"><p class="eyebrow">Nächste Termine</p><a href="termine.html">Alle Termine →</a></div><div class="events">{events_html(TERMINE[:3])}</div></div>
</div></div>
{cta("Mitmachen statt zuschauen", "Ob als Mitglied, Lesepatin oder Helfer beim Afrika-Tag: Bei uns ist Platz für alle, die Dortmund gemeinsam gestalten wollen.", "mitmachen.html", "So machen Sie mit")}''',
         "ACoD – Afrikanische Community in Dortmund e.V.: Beratung, Bildung und Begegnung für Menschen afrikanischer Herkunft in Dortmund.")

    # Über uns
    page("ueber-uns.html", "Über uns", page_head("Über uns", "Eine Community, viele Herkunftsländer, eine Stadt.",
         "Die Afrikanische Community in Dortmund ist ein gemeinnütziger Verein von und für Menschen afrikanischer Herkunft und alle, die mit ihnen zusammenleben.",
         [("index.html", "Start"), (None, "Über uns")]) + f'''
<div class="wrap">
  <div class="section two-col">
    <div class="prose">
      <h2>Wer wir sind</h2>
      <p>ACoD ist 2020 als Wahlliste der Afrikanischen Community zur Integrationsratswahl in Dortmund angetreten. Aus dieser gemeinsamen Kandidatur ist ein Verein entstanden: von Menschen, die in Dortmund leben und ihre Erfahrungen weitergeben wollen. Wir sind überparteilich und konfessionell unabhängig.</p>
      <p>Unser Ziel ist eine Stadtgesellschaft, in der Menschen afrikanischer Herkunft gleichberechtigt teilhaben, mitreden und mitgestalten. Dafür arbeiten wir mit Schulen, Beratungsstellen, der Stadt Dortmund und anderen Vereinen zusammen.</p>
      <h2>Unsere Werte</h2>
      <div class="values"><span>Teilhabe</span><span>Respekt</span><span>Solidarität</span><span>Bildung</span><span>Transparenz</span></div>
    </div>
    <div class="stack">
      <h2>Unsere Geschichte</h2>
      <ol class="timeline">
        <li><b>2020</b><p>ACoD tritt als Liste 4 zur Integrationsratswahl am 13. September an, unter dem Motto „Wir sind eine Gemeinschaft!“.</p></li>
        <li><b>2021</b><p>Eintragung ins Vereinsregister und Anerkennung der Gemeinnützigkeit.</p></li>
        <li><b>2022</b><p>Erstes Fußballturnier „Fußball verbindet“ mit 16 Teams.</p></li>
        <li><b>2023</b><p>Start der Willkommenslotsen und der Workshopreihe „Frauen stärken“.</p></li>
        <li><b>2024</b><p>Die Lernbrücke beginnt mit Hausaufgabenhilfe in der Nordstadt.</p></li>
        <li><b>2026</b><p>Über 120 Mitglieder und Engagierte aus 14 Herkunftsländern.</p></li>
      </ol>
    </div>
  </div>
  <div class="section">
    <h2>Mehr über den Verein</h2>
    <div class="cards3">
      <a class="card" href="vorstand.html" style="text-decoration:none;color:inherit"><h3>Vorstand &amp; Team</h3><p>Die Menschen, die den Verein ehrenamtlich führen.</p><span class="more">Ansehen →</span></a>
      <a class="card" href="transparenz.html" style="text-decoration:none;color:inherit"><h3>Finanzen &amp; Transparenz</h3><p>Woher unser Geld kommt und wofür wir es ausgeben.</p><span class="more">Ansehen →</span></a>
      <a class="card" href="mitmachen.html" style="text-decoration:none;color:inherit"><h3>Mitmachen</h3><p>Mitglied werden, ehrenamtlich helfen oder kooperieren.</p><span class="more">Ansehen →</span></a>
    </div>
  </div>
</div>''', "Über ACoD e.V.: Geschichte, Werte und Ziele der Afrikanischen Community Dortmund.")

    # Vorstand
    team = "".join(f'<div class="person"><div class="avatar" aria-hidden="true">{e(k)}</div><b>{e(n)}</b><span>{e(r)}</span></div>' for k, n, r in VORSTAND)
    page("vorstand.html", "Vorstand & Team", page_head("Über uns", "Vorstand & Team",
         "Der Vorstand wird alle zwei Jahre von der Mitgliederversammlung gewählt und arbeitet ehrenamtlich.",
         [("index.html", "Start"), ("ueber-uns.html", "Über uns"), (None, "Vorstand & Team")]) + f'''
<div class="wrap">
  <div class="section"><h2>Vorstand</h2><div class="team">{team}</div></div>
  <div class="section"><div class="prose"><h2>Ansprechpartner</h2><p>Sie erreichen den Vorstand über <b>{VEREIN['mail']}</b> oder in unserer Sprechstunde: {VEREIN['sprechstunde']}.</p></div></div>
</div>''', "Vorstand und Team von ACoD e.V. in Dortmund.")

    # Transparenz
    page("transparenz.html", "Finanzen & Transparenz", page_head("Über uns", "Finanzen & Transparenz",
         "Wir legen offen, woher unser Geld kommt und wofür wir es einsetzen.",
         [("index.html", "Start"), ("ueber-uns.html", "Über uns"), (None, "Finanzen & Transparenz")]) + f'''
<div class="wrap">
  <div class="section cards3">
    <div class="card"><h3>Gemeinnützig</h3><p>Eingetragen beim {VEREIN['register']}. Vom Finanzamt Dortmund als gemeinnützig anerkannt, Spenden sind steuerlich absetzbar.</p></div>
    <div class="card"><h3>Ehrenamtlich</h3><p>Der Vorstand arbeitet unentgeltlich. Verwaltungskosten halten wir so niedrig wie möglich.</p></div>
    <div class="card"><h3>Geprüft</h3><p>Zwei gewählte Kassenprüferinnen oder Kassenprüfer prüfen jedes Jahr die Finanzen und berichten der Mitgliederversammlung.</p></div>
  </div>
  <div class="section two-col">
    <div class="prose">
      <h2>Einnahmen 2025</h2>
      <p>Beispielwerte, bitte durch den echten Jahresabschluss ersetzen.</p>
      <dl class="kv box"><dt>Spenden</dt><dd>9.800 €</dd><dt>Mitgliedsbeiträge</dt><dd>5.400 €</dd><dt>Projektförderung</dt><dd>6.200 €</dd><dt>Sonstiges</dt><dd>900 €</dd><dt><b>Gesamt</b></dt><dd>22.300 €</dd></dl>
    </div>
    <div class="prose">
      <h2>Ausgaben 2025</h2>
      <p>Beispielwerte, bitte durch den echten Jahresabschluss ersetzen.</p>
      <dl class="kv box"><dt>Projekte</dt><dd>17.600 €</dd><dt>Raummiete</dt><dd>2.400 €</dd><dt>Verwaltung</dt><dd>1.100 €</dd><dt>Öffentlichkeitsarbeit</dt><dd>700 €</dd><dt><b>Gesamt</b></dt><dd>21.800 €</dd></dl>
    </div>
  </div>
  <div class="section prose"><h2>Satzung &amp; Berichte</h2><p>Satzung, Freistellungsbescheid und Jahresberichte senden wir auf Anfrage gern zu. Schreiben Sie an {VEREIN['mail']}.</p></div>
</div>''', "Finanzen, Gemeinnützigkeit und Transparenz bei ACoD e.V.")

    # Projekte
    page("projekte.html", "Projekte", page_head("Projekte", "Unsere Projekte",
         "Von Hausaufgabenhilfe bis Kulturfest: Hier sehen Sie, was gerade läuft und was wir bereits abgeschlossen haben.",
         [("index.html", "Start"), (None, "Projekte")]) + f'''
<div class="wrap"><div class="section">
  <div class="filters" role="group" aria-label="Projekte filtern">
    <button type="button" data-filter="alle" aria-pressed="true">Alle ({len(PROJEKTE)})</button>
    <button type="button" data-filter="laufend" aria-pressed="false">Laufende Projekte ({len(laufend)})</button>
    <button type="button" data-filter="abgeschlossen" aria-pressed="false">Abgeschlossene Projekte ({len(abgeschlossen)})</button>
  </div>
  <div class="projects">{"".join(project_card(p) for p in PROJEKTE)}</div>
</div></div>
{cta("Projekte brauchen Unterstützung", "Mit einer Spende helfen Sie, dass unsere laufenden Projekte weitergehen können.")}''',
         "Laufende und abgeschlossene Projekte von ACoD e.V. in Dortmund.")

    # Projekt-Detailseiten
    for p in PROJEKTE:
        done = p["s"] == "abgeschlossen"
        tun = "".join(f"<li>{e(x)}</li>" for x in p["tun"])
        ziele = "".join(f"<li>{e(x)}</li>" for x in p["ziele"])
        if p.get("goal"):
            pct = round(p["raised"] / p["goal"] * 100)
            support = f'''<div class="box"><h3>Spendenstand</h3><div class="progress"><div class="progress-bar" role="progressbar" aria-label="Spendenstand" aria-valuemin="0" aria-valuemax="{p["goal"]}" aria-valuenow="{p["raised"]}"><i style="width:{pct}%"></i></div><span>{eur(p["raised"])} von {eur(p["goal"])} · {pct} %</span></div><a class="btn btn-donate" href="spenden.html">Für dieses Projekt spenden</a></div>'''
        else:
            support = '<div class="box"><h3>Weitermachen</h3><p class="empty">Dieses Projekt ist abgeschlossen. Ihre Spende hilft unseren laufenden Projekten.</p><a class="btn btn-green" href="projekte.html#laufend">Laufende Projekte</a></div>'
        others = [o for o in PROJEKTE if o["slug"] != p["slug"] and o["s"] == p["s"]][:3] or [o for o in PROJEKTE if o["slug"] != p["slug"]][:3]
        page(f"projekt-{p['slug']}.html", p["t"], page_head(("Abgeschlossenes" if done else "Laufendes") + " Projekt · " + p["cat"], p["t"], p["d"],
             [("index.html", "Start"), ("projekte.html", "Projekte"), ("projekte.html#" + p["s"], "Abgeschlossene Projekte" if done else "Laufende Projekte"), (None, p["t"])]) + f'''
<div class="wrap">
  <div class="detail">
    <div class="prose">
      <div class="detail-art {p["art"]}" role="img" aria-label="Musterbild zum Projekt {e(p["t"])}"><span class="status{" done" if done else ""}">{"Abgeschlossen" if done else "Laufend"}</span></div>
      <h2>Ausgangslage</h2><p>{e(p["lage"])}</p>
      <h2>Was wir tun</h2><ul>{tun}</ul>
      <h2>{"Ergebnisse" if done else "Unsere Ziele"}</h2><ul class="goals">{ziele}</ul>
      <h2>Partner</h2><p>{e(p["partner"])}</p>
    </div>
    <aside class="aside">
      <div class="box"><h3>Auf einen Blick</h3><dl class="kv"><dt>Status</dt><dd>{"Abgeschlossen" if done else "Laufend"}</dd><dt>Bereich</dt><dd>{e(p["cat"])}</dd><dt>Zeitraum</dt><dd>{e(p["time"])}</dd><dt>Ort</dt><dd>{e(p["ort"])}</dd></dl></div>
      {support}
      <div class="box"><h3>Mitmachen</h3><p class="empty">Sie möchten in diesem Projekt helfen?</p><a href="kontakt.html">Schreiben Sie uns →</a></div>
    </aside>
  </div>
  <div class="section"><h2>Weitere Projekte</h2><div class="projects">{"".join(project_card(o) for o in others)}</div></div>
</div>''', f"{p['t']}: {p['d']}")

    # Aktuelles
    page("aktuelles.html", "Aktuelles", page_head("Aktuelles", "Neues aus dem Verein",
         "Berichte aus unseren Projekten, Rückblicke und Neuigkeiten aus dem Vereinsleben.",
         [("index.html", "Start"), (None, "Aktuelles")]) + f'''
<div class="wrap"><div class="section two-col">
  <div class="news">{news_html(NEWS)}</div>
  <div class="stack"><h3>Nächste Termine</h3><div class="events">{events_html(TERMINE[:3])}</div><a href="termine.html">Alle Termine →</a>
    <div class="box"><h3>Immer informiert</h3><p class="empty">Folgen Sie uns auf Facebook für aktuelle Fotos und Ankündigungen.</p><a class="btn btn-green" href="{VEREIN['facebook']}" target="_blank" rel="noopener">ACoD auf Facebook</a></div>
  </div>
</div></div>''', "Neuigkeiten von ACoD e.V. aus Dortmund.")

    # Termine
    page("termine.html", "Termine", page_head("Aktuelles", "Termine & Veranstaltungen",
         "Alle Veranstaltungen sind offen für Mitglieder, Familien und alle Interessierten, sofern nicht anders angegeben.",
         [("index.html", "Start"), ("aktuelles.html", "Aktuelles"), (None, "Termine")]) + f'''
<div class="wrap"><div class="section" style="max-width:780px">
  <div class="events">{events_html(TERMINE, long=True)}</div>
  <p class="empty">Sie möchten eine Veranstaltung mit uns planen? <a href="kontakt.html">Sprechen Sie uns an.</a></p>
</div></div>''', "Termine und Veranstaltungen von ACoD e.V. in Dortmund.")

    # Mitmachen
    page("mitmachen.html", "Mitmachen", page_head("Mitmachen", "Werden Sie Teil der Community.",
         "Mitglied werden, Zeit schenken oder gemeinsam Projekte entwickeln: Es gibt viele Wege, ACoD zu unterstützen.",
         [("index.html", "Start"), (None, "Mitmachen")]) + f'''
<div class="wrap">
  <div class="section cards3">
    <a class="card" href="#mitglied" style="text-decoration:none;color:inherit"><h3>Mitglied werden</h3><p>Ab 5 € im Monat unterstützen Sie den Verein dauerhaft und stimmen in der Mitgliederversammlung mit.</p><span class="more">Zum Antrag ↓</span></a>
    <a class="card" href="#ehrenamt" style="text-decoration:none;color:inherit"><h3>Ehrenamtlich helfen</h3><p>Nachhilfe geben, übersetzen, Feste mitorganisieren. Jede Stunde zählt, ganz gleich welche Herkunft Sie haben.</p><span class="more">Aufgaben ansehen ↓</span></a>
    <a class="card" href="#kooperation" style="text-decoration:none;color:inherit"><h3>Kooperieren</h3><p>Schulen, Unternehmen und Vereine: Lassen Sie uns gemeinsame Projekte in Dortmund entwickeln.</p><span class="more">Mehr erfahren ↓</span></a>
  </div>
  <div class="section two-col" id="mitglied">
    <div class="prose">
      <p class="eyebrow">Mitgliedschaft</p><h2>Mitglied werden</h2>
      <p>Mitglieder tragen den Verein. Sie erhalten Einladungen zu allen Veranstaltungen, stimmen in der Mitgliederversammlung ab und können sich in den Vorstand wählen lassen.</p>
      <dl class="kv box"><dt>Erwachsene</dt><dd>5 € / Monat</dd><dt>Schüler, Studierende, ermäßigt</dt><dd>2 € / Monat</dd><dt>Familien</dt><dd>8 € / Monat</dd><dt>Fördermitglied</dt><dd>frei wählbar</dd></dl>
    </div>
    <form class="form" data-demo novalidate>
      <h3>Mitgliedsantrag</h3>
      <div class="row2"><div class="field"><label for="m-vor">Vorname *</label><input id="m-vor" required></div><div class="field"><label for="m-nach">Nachname *</label><input id="m-nach" required></div></div>
      <div class="field"><label for="m-mail">E-Mail *</label><input id="m-mail" type="email" required></div>
      <div class="field"><label for="m-adr">Adresse</label><input id="m-adr"></div>
      <div class="field"><label for="m-art">Art der Mitgliedschaft</label><select id="m-art"><option>Erwachsene (5 €)</option><option>Ermäßigt (2 €)</option><option>Familie (8 €)</option><option>Fördermitglied</option></select></div>
      <label class="check"><input type="checkbox" id="m-ok" required> Ich habe die Datenschutzerklärung gelesen und bin einverstanden. *</label>
      <button class="btn btn-donate" type="submit">Antrag absenden</button>
      <p class="form-msg" hidden></p>
    </form>
  </div>
  <div class="section" id="ehrenamt">
    <p class="eyebrow">Ehrenamt</p><h2>Wo wir Hilfe brauchen</h2>
    <div class="cards3">
      <div class="card"><h3>Lesepatin / Lesepate</h3><p>Eine Stunde pro Woche mit einem Kind lesen. Projekt: Lernbrücke.</p></div>
      <div class="card"><h3>Willkommenslotse</h3><p>Familien zu Ämtern und Ärzten begleiten. Mehrsprachigkeit ist ein Plus.</p></div>
      <div class="card"><h3>Event-Team</h3><p>Afrika-Tag, Kochabende und Feste mit planen und umsetzen.</p></div>
    </div>
  </div>
  <div class="section prose" id="kooperation">
    <p class="eyebrow">Kooperationen</p><h2>Gemeinsam mehr erreichen</h2>
    <p>Wir arbeiten mit Schulen, Beratungsstellen, Unternehmen und anderen Vereinen zusammen. Ob Projektpartnerschaft, Raumspende oder Sponsoring beim Afrika-Tag: Sprechen Sie uns an.</p>
    <div><a class="btn btn-green" href="kontakt.html">Kontakt aufnehmen</a></div>
  </div>
</div>''', "Mitglied werden, Ehrenamt und Kooperationen bei ACoD e.V.")

    # Spenden
    page("spenden.html", "Spenden", page_head("Spenden", "Ihre Spende wirkt in Dortmund.",
         "Mit einer einmaligen oder monatlichen Spende sichern Sie Beratung, Bildung und Begegnung für Familien afrikanischer Herkunft.",
         [("index.html", "Start"), (None, "Spenden")]) + f'''
<div class="donate-band"><div class="wrap donate-grid">
  <div class="stack" style="gap:1.2rem">
    <h2>Was Ihre Spende bewirkt</h2>
    {USES}
    <h3>Per Überweisung</h3>
    <dl class="bank">
      <dt>Empfänger</dt><dd>{VEREIN['lang']}</dd>
      <dt>IBAN</dt><dd><span id="iban">{VEREIN['iban']}</span><button class="copy" type="button" data-copy="iban">Kopieren</button></dd>
      <dt>BIC · Bank</dt><dd>{VEREIN['bic']} · {VEREIN['bank']}</dd>
      <dt>Verwendungszweck</dt><dd>Spende + Ihre Adresse für die Zuwendungsbestätigung</dd>
    </dl>
  </div>
  <form class="form" id="donateForm" novalidate>
    <h3>Online spenden</h3>
    <div class="seg" role="radiogroup" aria-label="Spendenrhythmus">
      <input type="radio" name="rhythm" id="r-once" value="einmalig" checked><label for="r-once">Einmalig</label>
      <input type="radio" name="rhythm" id="r-month" value="monatlich"><label for="r-month">Monatlich</label>
    </div>
    <div class="amounts" role="radiogroup" aria-label="Betrag">
      <input type="radio" name="amount" id="a25" value="25"><label for="a25">25 €</label>
      <input type="radio" name="amount" id="a50" value="50" checked><label for="a50">50 €</label>
      <input type="radio" name="amount" id="a120" value="120"><label for="a120">120 €</label>
      <input type="radio" name="amount" id="a250" value="250"><label for="a250">250 €</label>
    </div>
    <div class="field"><label for="custom">Anderer Betrag (€)</label><input id="custom" type="number" min="1" step="1" inputmode="numeric" placeholder="z. B. 30"></div>
    <div class="field"><label for="purpose">Wofür?</label>
      <select id="purpose"><option>Wo es am nötigsten ist</option>{"".join(f"<option>{e(p['t'])}</option>" for p in laufend)}</select>
    </div>
    <p class="impact" id="impact"></p>
    <button class="btn btn-donate" type="submit">Spende abschließen</button>
    <p class="form-msg" id="donateMsg" hidden></p>
  </form>
</div></div>
<div class="wrap"><div class="section">
  <h2>Häufige Fragen</h2>
  <div class="faq">
    <details><summary>Bekomme ich eine Spendenquittung?</summary><p>Ja. Für Spenden bis 300 € genügt dem Finanzamt Ihr Kontoauszug. Für höhere Beträge schicken wir Ihnen Anfang des Folgejahres automatisch eine Zuwendungsbestätigung, wenn Sie Ihre Adresse angeben.</p></details>
    <details><summary>Kann ich für ein bestimmtes Projekt spenden?</summary><p>Ja. Geben Sie im Verwendungszweck den Projektnamen an oder wählen Sie das Projekt im Formular. Zweckgebundene Spenden setzen wir nur für dieses Projekt ein.</p></details>
    <details><summary>Wie viel meiner Spende kommt an?</summary><p>Der Vorstand arbeitet ehrenamtlich. Über 80 % unserer Ausgaben fließen direkt in Projekte. Details finden Sie unter <a href="transparenz.html">Finanzen &amp; Transparenz</a>.</p></details>
    <details><summary>Kann ich auch Sachspenden geben?</summary><p>Gern, vor allem Schulmaterial, Kinderbücher und Laptops. Bitte sprechen Sie uns vorher an, damit wir planen können.</p></details>
  </div>
</div></div>''', "Spenden für ACoD e.V.: Beratung, Bildung und Begegnung in Dortmund unterstützen.")

    # Kontakt
    page("kontakt.html", "Kontakt", page_head("Kontakt", "Schreiben Sie uns.",
         "Wir antworten in der Regel innerhalb weniger Tage, auf Deutsch, Englisch oder Französisch.",
         [("index.html", "Start"), (None, "Kontakt")]) + f'''
<div class="wrap"><div class="section two-col">
  <dl class="contact-list">
    <div><dt>Adresse</dt><dd>{VEREIN['lang']}<br>{VEREIN['strasse']}, {VEREIN['ort']}</dd></div>
    <div><dt>E-Mail</dt><dd><span id="mail">{VEREIN['mail']}</span><button class="copy" type="button" data-copy="mail">Kopieren</button></dd></div>
    <div><dt>Telefon</dt><dd>{VEREIN['tel']}</dd></div>
    <div><dt>Sprechstunde</dt><dd>{VEREIN['sprechstunde']}</dd></div>
    <div><dt>Social Media</dt><dd><a href="{VEREIN['facebook']}" target="_blank" rel="noopener">facebook.com/ACoD2020</a></dd></div>
  </dl>
  <form class="form" data-demo novalidate>
    <div class="row2"><div class="field"><label for="c-name">Name *</label><input id="c-name" required></div><div class="field"><label for="c-mail">E-Mail *</label><input id="c-mail" type="email" required></div></div>
    <div class="field"><label for="c-topic">Anliegen</label><select id="c-topic"><option>Allgemeine Frage</option><option>Beratung</option><option>Mitgliedschaft</option><option>Ehrenamt</option><option>Kooperation</option><option>Presse</option></select></div>
    <div class="field"><label for="c-msg">Nachricht *</label><textarea id="c-msg" rows="6" required></textarea></div>
    <label class="check"><input type="checkbox" id="c-ok" required> Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen und bin einverstanden. *</label>
    <button class="btn btn-donate" type="submit">Nachricht senden</button>
    <p class="form-msg" hidden></p>
  </form>
</div></div>''', "Kontakt zu ACoD e.V. in Dortmund.")

    # Integrationsrat
    page("integrationsrat.html", "Integrationsrat", page_head("Politische Teilhabe", "ACoD im Integrationsrat der Stadt Dortmund",
         "Die Wahlliste der Afrikanischen Community in Dortmund: Wir sind eine Gemeinschaft!",
         [("index.html", "Start"), (None, "Integrationsrat")]) + f'''
<div class="wrap">
  <div class="section">
    <figure class="flyer"><img src="assets/img/flyer-integrationsratswahl-2020.jpg" alt="Wahlplakat: ACoD im Integrationsrat der Stadt Dortmund, die Wahlliste der Afrikanischen Community in Dortmund, Liste 4, Integrationsratswahl am 13. September 2020" width="960" height="448"><figcaption>Unser Wahlaufruf zur Integrationsratswahl am 13. September 2020</figcaption></figure>
  </div>
  <div class="section two-col">
    <div class="prose">
      <h2>Was ist der Integrationsrat?</h2>
      <p>Der Integrationsrat vertritt die Interessen der Dortmunderinnen und Dortmunder mit Einwanderungsgeschichte gegenüber Rat und Verwaltung der Stadt. Er wird alle fünf Jahre zusammen mit der Kommunalwahl gewählt und kann sich mit allen Angelegenheiten der Stadt befassen.</p>
      <p>Wählen dürfen unter anderem Menschen ohne deutsche Staatsangehörigkeit, Eingebürgerte und Menschen, die die deutsche Staatsangehörigkeit durch Geburt als Kind ausländischer Eltern erworben haben.</p>
      <h2>Wofür wir uns einsetzen</h2>
      <ul class="goals">
        <li>Mehr Beratung in afrikanischen Sprachen, Englisch und Französisch bei Ämtern</li>
        <li>Faire Chancen in Schule, Ausbildung und auf dem Arbeitsmarkt</li>
        <li>Anerkennung ausländischer Abschlüsse beschleunigen</li>
        <li>Klare Haltung gegen Rassismus und Diskriminierung</li>
        <li>Räume und Förderung für Vereine der afrikanischen Community</li>
      </ul>
    </div>
    <aside class="stack">
      <div class="council-badge big"><span>Liste</span><b>4</b><small>Integrationsratswahl 13.09.2020</small></div>
      <div class="box"><h3>Geh wählen!</h3><p class="langs">Geh wählen! · Vote! · Allez voter! · <span lang="ar" dir="rtl">تعالوا و انتخبوا</span></p><p class="empty">Unser Aufruf richtet sich an alle Wahlberechtigten, in allen Sprachen der Community.</p></div>
      <div class="box"><h3>Unsere Vertreter*innen</h3><p class="empty"><mark>Bitte ergänzen: Namen der gewählten Mitglieder und Wahlergebnisse 2020 und 2025.</mark></p></div>
    </aside>
  </div>
</div>
{cta("Ihre Anliegen gehören in den Integrationsrat", "Was muss sich in Dortmund ändern? Schreiben Sie uns, wir tragen es weiter.", "kontakt.html", "Anliegen schicken")}''', "ACoD als Wahlliste der Afrikanischen Community im Integrationsrat der Stadt Dortmund.")

    # Galerie
    tiles = "".join(f'<div class="tile placeholder"><span>Foto von Facebook einfügen</span></div>' for _ in range(5))
    page("galerie.html", "Bilder & Videos", page_head("Aktuelles", "Bilder & Videos",
         "Eindrücke aus Wahlkampf, Festen und Projekten. Mehr Fotos und Videos finden Sie auf unserer Facebook-Seite.",
         [("index.html", "Start"), ("aktuelles.html", "Aktuelles"), (None, "Bilder & Videos")]) + f'''
<div class="wrap">
  <div class="section">
    <h2>Fotos</h2>
    <div class="gallery">
      <figure class="tile wide"><img src="assets/img/gruppenfoto-2020.jpg" alt="Gruppenfoto von ACoD 2020" width="785" height="278"><figcaption>Unser Team zur Integrationsratswahl 2020</figcaption></figure>
      {tiles}
    </div>
  </div>
  <div class="section">
    <h2>Videos</h2>
    <div class="cards3">
      <div class="card"><div class="tile placeholder video"><span>Video von Facebook einbetten</span></div><h3>Wahlaufruf 2020</h3><p>Geh wählen! · Vote! · Allez voter!</p></div>
      <div class="card"><div class="tile placeholder video"><span>Video von Facebook einbetten</span></div><h3>Afrika-Tag</h3><p>Musik, Tanz und Begegnung in der Innenstadt.</p></div>
      <div class="card"><div class="tile placeholder video"><span>Video von Facebook einbetten</span></div><h3>Aus dem Vereinsleben</h3><p>Weitere Videos auf Facebook.</p></div>
    </div>
    <div><a class="btn btn-green" href="{VEREIN['facebook']}" target="_blank" rel="noopener">Alle Bilder und Videos auf Facebook</a></div>
  </div>
</div>''', "Bilder und Videos von ACoD aus Dortmund.")

    # Impressum
    page("impressum.html", "Impressum", page_head("Rechtliches", "Impressum", "Angaben gemäß § 5 DDG.",
         [("index.html", "Start"), (None, "Impressum")]) + f'''
<div class="wrap"><div class="section legal-text">
  <p><mark>Vorlage: Bitte alle markierten Angaben vom Verein prüfen und ergänzen lassen.</mark></p>
  <h2>Anbieter</h2>
  <p>{VEREIN['lang']}<br>{VEREIN['strasse']}<br>{VEREIN['ort']}</p>
  <h2>Vertreten durch den Vorstand</h2>
  <p><mark>Name 1. Vorsitzende/r</mark>, <mark>Name 2. Vorsitzende/r</mark></p>
  <h2>Kontakt</h2>
  <p>E-Mail: {VEREIN['mail']}<br>Telefon: {VEREIN['tel']}</p>
  <h2>Registereintrag</h2>
  <p>Eingetragen im Vereinsregister. Registergericht: <mark>{VEREIN['register']}</mark></p>
  <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
  <p><mark>Name, Anschrift wie oben</mark></p>
  <h2>Haftung für Links</h2>
  <p>Unsere Website enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter verantwortlich.</p>
</div></div>''', "Impressum von ACoD e.V.")

    # Datenschutz
    page("datenschutz.html", "Datenschutz", page_head("Rechtliches", "Datenschutzerklärung", "Wie wir mit Ihren Daten umgehen.",
         [("index.html", "Start"), (None, "Datenschutz")]) + f'''
<div class="wrap"><div class="section legal-text">
  <p><mark>Vorlage: Diese Erklärung ist ein Gerüst. Bitte vor Veröffentlichung an Hoster, Zahlungsanbieter und Formulare anpassen, z. B. mit einem Datenschutz-Generator oder fachlicher Beratung.</mark></p>
  <h2>1. Verantwortlicher</h2>
  <p>{VEREIN['lang']}, {VEREIN['strasse']}, {VEREIN['ort']}, E-Mail: {VEREIN['mail']}</p>
  <h2>2. Hosting und Server-Logfiles</h2>
  <p>Diese Website wird bei <mark>Name des Hosters</mark> betrieben. Beim Aufruf werden technisch notwendige Daten (IP-Adresse, Datum, Uhrzeit, aufgerufene Seite) in Logfiles gespeichert. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.</p>
  <h2>3. Schriftarten</h2>
  <p>Diese Website lädt Schriftarten von Google Fonts. Dabei wird Ihre IP-Adresse an Google übertragen. <mark>Empfehlung: Schriften lokal einbinden, dann kann dieser Abschnitt entfallen.</mark></p>
  <h2>4. Kontakt- und Mitgliedsformular</h2>
  <p>Wenn Sie uns über ein Formular schreiben, verarbeiten wir Ihre Angaben zur Bearbeitung Ihrer Anfrage bzw. Ihrer Mitgliedschaft (Art. 6 Abs. 1 lit. b DSGVO). Die Daten werden gelöscht, sobald sie nicht mehr benötigt werden und keine gesetzlichen Aufbewahrungsfristen bestehen.</p>
  <h2>5. Spenden</h2>
  <p>Für Online-Spenden nutzen wir <mark>Name des Zahlungsanbieters</mark>. Für Zuwendungsbestätigungen speichern wir Name, Adresse und Betrag gemäß den steuerrechtlichen Aufbewahrungspflichten.</p>
  <h2>6. Links zu sozialen Netzwerken</h2>
  <p>Wir verlinken auf unsere Facebook-Seite. Erst wenn Sie den Link anklicken, werden Daten an Meta übertragen.</p>
  <h2>7. Ihre Rechte</h2>
  <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht auf Beschwerde bei einer Aufsichtsbehörde, z. B. der LDI NRW.</p>
</div></div>''', "Datenschutzerklärung von ACoD e.V.")


if __name__ == "__main__":
    build()
    print("\n".join(sorted(p.name for p in OUT.glob("*.html"))))
