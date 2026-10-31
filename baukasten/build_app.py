"""Baut den Website-Baukasten aus src/ zusammen.

Ausgabe:
  dist/baukasten.html            – Fassung für Claude (ohne Dokumentgerüst)
  ../docs/baukasten/index.html   – eigenständige Fassung für GitHub Pages
Das ACoD-Projekt wird als Beispielprojekt eingebettet.
"""
import base64, json, random, string
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
SRC = HERE / "src"


def rid():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


def data_url(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def s(type_, **kw):
    return {"id": rid(), "type": type_, **kw}


def page(title, slug, sections, **kw):
    return {"id": rid(), "title": title, "slug": slug, "kind": "page", "inNav": True, "description": "", "sections": sections, **kw}


def seed():
    img = ROOT / "docs" / "assets" / "img"
    assets = {
        "logo": {"name": "ACoD Logo", "file": "acod-logo.png", "data": data_url(HERE / "acod-logo.png", "image/png")},
        "team": {"name": "Gruppenfoto 2020", "file": "gruppenfoto-2020.jpg", "data": data_url(img / "gruppenfoto-2020.jpg", "image/jpeg")},
        "flyer": {"name": "Flyer Integrationsratswahl 2020", "file": "flyer-integrationsratswahl-2020.jpg", "data": data_url(img / "flyer-integrationsratswahl-2020.jpg", "image/jpeg")},
    }
    projekte = [
        {"title": "Lernbrücke", "text": "Wöchentliche Hausaufgabenhilfe und Lesepatenschaften für Kinder aus afrikanischen Familien in der Nordstadt.", "status": "laufend", "meta": "Bildung & Jugend · seit [Jahr]", "image": "", "link": ""},
        {"title": "Willkommenslotsen", "text": "Neu angekommene Familien werden zu Ämtern, Ärzten und Schulen begleitet.", "status": "laufend", "meta": "Beratung · seit [Jahr]", "image": "", "link": ""},
        {"title": "Afrika-Tag Dortmund", "text": "Ein Fest mit Musik, Essen, Mode und Gesprächen in der Innenstadt.", "status": "laufend", "meta": "Kultur · jährlich", "image": "", "link": ""},
        {"title": "Integrationsratswahl 2020", "text": "Kandidatur als Liste 4 unter dem Motto „Wir sind eine Gemeinschaft!“.", "status": "abgeschlossen", "meta": "Politische Teilhabe · 2020", "image": "asset:flyer", "link": "integrationsrat"},
    ]
    termine = [
        {"date": "[TT.MM.JJJJ]", "title": "Offener Kochabend", "text": "18:00 Uhr · [Ort]"},
        {"date": "[TT.MM.JJJJ]", "title": "Infoabend Schule & Ausbildung", "text": "17:30 Uhr · auf Deutsch, Englisch und Französisch"},
    ]
    pages = [
        page("Start", "index", [
            s("hero", eyebrow="Afrikanische Community in Dortmund", title="Wir sind eine Gemeinschaft!", text="Wir verbinden Menschen afrikanischer Herkunft in Dortmund, begleiten Familien beim Ankommen und bringen ihre Stimme in die Stadtpolitik.", image="asset:team", cta1="Jetzt spenden", link1="spenden", cta2="Unsere Projekte", link2="projekte"),
            s("imageText", title="Unsere Stimme im Integrationsrat", text="ACoD ist als Wahlliste der Afrikanischen Community angetreten, zuerst als Liste 4 bei der Integrationsratswahl am 13. September 2020.\n\nGeh wählen! · Vote! · Allez voter!", image="asset:flyer", reverse=False, cta="Mehr zum Integrationsrat", link="integrationsrat"),
            s("features", title="Was wir tun", intro="", items=[
                {"title": "Beraten & begleiten", "text": "Hilfe bei Behörden, Schule, Ausbildung und Wohnungssuche, in mehreren Sprachen."},
                {"title": "Bildung & Jugend", "text": "Hausaufgabenhilfe, Mentoring und Workshops für junge Menschen."},
                {"title": "Kultur & Begegnung", "text": "Feste, Kochabende und Diskussionen, die Nachbarschaft stiften."}]),
            s("projects", title="Laufende Projekte", intro="", filter=False, items=[p for p in projekte if p["status"] == "laufend"]),
            s("cta", title="Mitmachen statt zuschauen", text="Als Mitglied, Lesepatin oder Helfer beim Afrika-Tag: Bei uns ist Platz für alle.", cta="So machst du mit", link="mitmachen"),
        ], description="ACoD – Afrikanische Community in Dortmund: Beratung, Bildung, Begegnung und politische Teilhabe."),
        page("Über uns", "ueber-uns", [
            s("text", title="Wer wir sind", text="ACoD ist 2020 als Wahlliste der Afrikanischen Community zur Integrationsratswahl in Dortmund angetreten. Daraus ist ein Verein entstanden: von Menschen, die in Dortmund leben und ihre Erfahrungen weitergeben wollen.\n\nWir sind überparteilich und konfessionell unabhängig."),
            s("team", title="Vorstand", items=[{"name": "[Name]", "role": "1. Vorsitz", "image": ""}, {"name": "[Name]", "role": "2. Vorsitz", "image": ""}, {"name": "[Name]", "role": "Kasse", "image": ""}, {"name": "[Name]", "role": "Schriftführung", "image": ""}]),
        ]),
        page("Integrationsrat", "integrationsrat", [
            s("imageText", title="ACoD im Integrationsrat der Stadt Dortmund", text="Die Wahlliste der Afrikanischen Community in Dortmund. Bei der Integrationsratswahl am 13. September 2020 sind wir als Liste 4 angetreten.", image="asset:flyer", reverse=False, cta="", link=""),
            s("features", title="Wofür wir uns einsetzen", intro="", items=[
                {"title": "Beratung in vielen Sprachen", "text": "Mehr Angebote auf Englisch, Französisch und in afrikanischen Sprachen bei Ämtern."},
                {"title": "Faire Chancen", "text": "In Schule, Ausbildung und auf dem Arbeitsmarkt, mit schnellerer Anerkennung von Abschlüssen."},
                {"title": "Gegen Rassismus", "text": "Klare Haltung gegen Diskriminierung in Dortmund."}]),
            s("cta", title="Ihre Anliegen gehören in den Integrationsrat", text="Was muss sich in Dortmund ändern? Schreiben Sie uns.", cta="Anliegen schicken", link="kontakt"),
        ]),
        page("Projekte", "projekte", [s("projects", title="Unsere Projekte", intro="Was gerade läuft und was wir schon abgeschlossen haben.", filter=True, items=projekte)]),
        page("Termine", "termine", [s("events", title="Termine", items=termine)]),
        page("Bilder", "galerie", [s("gallery", title="Bilder & Videos", items=[{"image": "asset:team", "caption": "Unser Team 2020"}, {"image": "asset:flyer", "caption": "Wahlaufruf 2020"}]),
                                   s("cta", title="Mehr auf Facebook", text="Fotos und Videos aus dem Vereinsleben.", cta="Zu Facebook", link="https://www.facebook.com/ACoD2020/")]),
        page("Mitmachen", "mitmachen", [
            s("features", title="So kannst du mitmachen", intro="", items=[{"title": "Mitglied werden", "text": "Ab [Betrag] im Monat."}, {"title": "Ehrenamt", "text": "Nachhilfe, Übersetzen, Feste organisieren."}, {"title": "Kooperieren", "text": "Gemeinsame Projekte mit Schulen, Firmen und Vereinen."}]),
            s("signup", title="Mitglied werden", text="Schick uns deine Daten, wir senden dir den Antrag.", cta="Antrag anfordern", formAction="", anchor="mitglied"),
        ]),
        page("Spenden", "spenden", [
            s("donate", title="Ihre Spende wirkt in Dortmund", text="ACoD arbeitet ehrenamtlich. Ihre Spende fließt direkt in Nachhilfe, Beratung und Begegnung.", amounts="25, 50, 120, 250", payLink="", holder="ACoD – Afrikanische Community in Dortmund", iban="[IBAN]", purpose="Spende + Ihre Adresse"),
            s("faq", title="Fragen zur Spende", items=[{"q": "Bekomme ich eine Spendenquittung?", "a": "Bis 300 € genügt der Kontoauszug, darüber senden wir eine Zuwendungsbestätigung."}, {"q": "Kann ich für ein Projekt spenden?", "a": "Ja, geben Sie den Projektnamen im Verwendungszweck an."}]),
        ], inNav=False),
        page("Kontakt", "kontakt", [s("contact", title="Schreiben Sie uns", text="Wir antworten auf Deutsch, Englisch oder Französisch.", formAction="")]),
        page("Impressum", "impressum", [s("legal", title="Impressum", text="[Impressum vom Verein ergänzen]")], inNav=False),
        page("Datenschutz", "datenschutz", [s("legal", title="Datenschutzerklärung", text="[Datenschutzerklärung ergänzen]")], inNav=False),
        page("Lesepaten gesucht", "lesepaten", [
            s("hero", eyebrow="Ehrenamt in der Nordstadt", title="Eine Stunde pro Woche. Ein Kind. Ein Buch.", text="Werde Lesepatin oder Lesepate bei der Lernbrücke. Keine Vorkenntnisse nötig.", image="", cta1="Jetzt melden", link1="#melden", cta2="", link2=""),
            s("features", title="Darum lohnt es sich", intro="", items=[{"title": "Wirkung, die man sieht", "text": "Kinder lesen sicherer und gehen lieber zur Schule."}, {"title": "Flexibel", "text": "Du wählst Tag und Uhrzeit."}, {"title": "Gut vorbereitet", "text": "Ein kurzer Workshop vor dem Start."}]),
            s("signup", title="Jetzt melden", text="Wir rufen dich an und erzählen dir alles Weitere.", cta="Ich mache mit", formAction="", anchor="melden"),
        ], kind="landing", inNav=False),
    ]
    return {
        "id": "beispiel-acod", "version": 1, "name": "Beispiel: ACoD Dortmund", "updated": 0,
        "site": {"name": "ACoD", "tagline": "Afrikanische Community in Dortmund", "email": "[E-Mail]", "phone": "", "address": "[Adresse], Dortmund",
                 "ctaLabel": "Spenden", "ctaLink": "spenden", "facebook": "https://www.facebook.com/ACoD2020/", "instagram": "", "domain": "",
                 "notice": "Entwurf: Inhalte in [eckigen Klammern] sind Platzhalter."},
        "brand": {"logo": "asset:logo", "colors": {"primary": "#1B5E47", "accent": "#B8195C", "dark": "#0E2B25"}, "font": "slab", "hero": "dark", "radius": "10", "bg": "tint", "showName": False},
        "assets": assets, "pages": pages,
    }


def main():
    css = (SRC / "app.css").read_text()
    body = (SRC / "body.html").read_text()
    js = (SRC / "app.js").read_text()
    seed_json = json.dumps(seed(), ensure_ascii=False).replace("</", "<\\/")
    head = """<title>Website-Baukasten</title>
<meta name="description" content="Websites mit Logo-Farben, KI-Texten und Landingpages in Serie bauen.">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>"""
    content = f"{head}\n<style>\n{css}</style>\n{body}\n<script>const SEED = {seed_json};</script>\n<script>\n{js}</script>\n"
    (HERE / "dist").mkdir(exist_ok=True)
    (HERE / "dist" / "baukasten.html").write_text(content)
    out = ROOT / "docs" / "baukasten"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(f'<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n<style>\n{css}</style>\n</head>\n<body>\n{body}\n<script>const SEED = {seed_json};</script>\n<script>\n{js}</script>\n</body>\n</html>\n')
    print("ok", len(content) // 1024, "KB")


if __name__ == "__main__":
    main()
