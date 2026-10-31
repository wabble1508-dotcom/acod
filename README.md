# ACoD – Website & Website-Baukasten

Website der **Afrikanischen Community in Dortmund (ACoD)** und ein Baukasten, mit dem sich solche Websites für beliebige Projekte erstellen lassen.

| Ordner | Inhalt |
| --- | --- |
| `docs/` | Fertige ACoD-Website (statisches HTML). Wird von GitHub Pages veröffentlicht. |
| `docs/baukasten/` | Website-Baukasten als eigenständige Web-App |
| `build.py` | Erzeugt die ACoD-Website in `docs/`. Inhalte stehen oben im Skript. |
| `baukasten/src/` | Quelltext des Baukastens (`app.js`, `app.css`, `body.html`) |
| `baukasten/build_app.py` | Baut den Baukasten nach `docs/baukasten/` und `baukasten/dist/` |

## Online stellen mit GitHub Pages

1. Repository auf GitHub öffnen → **Settings** → **Pages**
2. Unter *Build and deployment*: Source **Deploy from a branch**, Branch **main**, Ordner **/docs** → **Save**
3. Nach etwa einer Minute ist die Seite erreichbar unter
   `https://<benutzername>.github.io/<repository>/` und der Baukasten unter `…/baukasten/`

## Website-Baukasten

- **Logo hochladen** → Farben werden automatisch aus dem Logo gelesen und auf die ganze Website angewendet (Hauptfarbe, Akzent, Dunkel). Logofarben lassen sich per Klick einer Rolle zuweisen, ein Kontrast-Check warnt bei schlecht lesbaren Kombinationen.
- **Stil**: 7 Schriftpaarungen, Einstieg dunkel/farbig/hell, Ecken, Hintergrund.
- **Seiten & Abschnitte**: 17 Abschnittstypen (Hero, Leistungen, Projekte laufend/abgeschlossen, Termine, Team, Preise, FAQ, Galerie, Spenden, Kontakt, Anmeldung …), frei sortierbar, Bilder hochladen.
- **KI (in Claude)**: komplette Website, einzelne Seite oder Landingpage aus einer Beschreibung erzeugen; jeden Abschnitt mit einer Anweisung umschreiben; Logo analysieren lassen (Farben, Schrift, Wirkung); Meta-Beschreibungen schreiben.
- **Automatisierung**: Landingpages in Serie aus einer Tabelle (`{{stadt}}`, `{{angebot}}` …), optional pro Seite von Claude individualisiert; alle Formulare auf einmal mit einem Formular-Dienst verbinden; Meta-Beschreibungen ergänzen; `sitemap.xml` und `robots.txt` beim Export.
- **Export**: ZIP mit allen Seiten, CSS, JS, Bildern und einer Projektdatei, die sich wieder laden lässt.
- **Speichern**: in Claude im eigenen Konto, sonst im Browser; zusätzlich als Projektdatei.

Außerhalb von Claude (z. B. auf GitHub Pages) funktioniert alles außer den KI-Funktionen.

## Noch offen für die ACoD-Website

- Platzhalter (Projekte, Termine, Vorstand, Adresse, Bankdaten) durch echte Inhalte ersetzen
- Impressum und Datenschutz vervollständigen
- Zahlungsanbieter für Online-Spenden und Formular-Dienst verbinden
