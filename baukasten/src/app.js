"use strict";
/* ============================================================
   Website-Baukasten
   Projekte → Seiten → Abschnitte. Marke (Logo, Farben, Schrift)
   färbt jede erzeugte Seite. Vorschau per iframe, Export als ZIP.
   ============================================================ */

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const uid = () => Math.random().toString(36).slice(2, 10);
const clone = o => JSON.parse(JSON.stringify(o));
const slugify = s => String(s || "").toLowerCase()
  .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
  .normalize("NFKD").replace(/[̀-ͯ]/g, "")
  .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60) || "seite";
const para = t => esc(t).split(/\n{2,}/).map(p => `<p>${p.replace(/\n/g, "<br>")}</p>`).join("");
const lines = t => String(t || "").split("\n").map(s => s.trim()).filter(Boolean);
const use = name => (window.claude && window.claude.use ? window.claude.use(name).catch(() => null) : Promise.resolve(null));

/* ---------------------------------------------------------- Farben */
const hex2rgb = h => { h = h.replace("#", ""); if (h.length === 3) h = [...h].map(c => c + c).join(""); const n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; };
const rgb2hex = ([r, g, b]) => "#" + [r, g, b].map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("").toUpperCase();
const mix = (a, b, t) => { const A = hex2rgb(a), B = hex2rgb(b); return rgb2hex(A.map((v, i) => v + (B[i] - v) * t)); };
const lum = h => { const c = hex2rgb(h).map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }); return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]; };
const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
const onColor = h => contrast(h, "#FFFFFF") >= contrast(h, "#111111") ? "#FFFFFF" : "#111111";
function rgb2hsl([r, g, b]) {
  r /= 255; g /= 255; b /= 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
  if (mx === mn) return [0, 0, l];
  const d = mx - mn, s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn);
  const h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [h * 60, s, l];
}
function hsl2hex(h, s, l) {
  const k = n => (n + h / 30) % 12, a = s * Math.min(l, 1 - l);
  const f = n => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  return rgb2hex([f(0) * 255, f(8) * 255, f(4) * 255]);
}
const hueDist = (a, b) => { const d = Math.abs(a - b) % 360; return d > 180 ? 360 - d : d; };

/** Liest die prägenden Farben eines Logos: Rückgabe sortiert nach Gewicht. */
function logoColors(img) {
  const c = document.createElement("canvas"), max = 96;
  const k = Math.min(1, max / Math.max(img.naturalWidth || img.width, img.naturalHeight || img.height));
  c.width = Math.max(1, Math.round((img.naturalWidth || img.width) * k));
  c.height = Math.max(1, Math.round((img.naturalHeight || img.height) * k));
  const x = c.getContext("2d", { willReadFrequently: true });
  x.drawImage(img, 0, 0, c.width, c.height);
  const d = x.getImageData(0, 0, c.width, c.height).data, buckets = new Map();
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 140) continue;
    const key = (d[i] >> 4) << 8 | (d[i + 1] >> 4) << 4 | (d[i + 2] >> 4);
    const b = buckets.get(key) || { r: 0, g: 0, b: 0, n: 0 };
    b.r += d[i]; b.g += d[i + 1]; b.b += d[i + 2]; b.n++;
    buckets.set(key, b);
  }
  let list = [...buckets.values()].map(b => {
    const rgb = [b.r / b.n, b.g / b.n, b.b / b.n], [h, s, l] = rgb2hsl(rgb);
    return { hex: rgb2hex(rgb), n: b.n, h, s, l };
  }).sort((a, b) => b.n - a.n);
  // ähnliche Farben zusammenfassen
  const merged = [];
  for (const c1 of list) {
    const m = merged.find(c2 => { const A = hex2rgb(c1.hex), B = hex2rgb(c2.hex); return Math.hypot(A[0] - B[0], A[1] - B[1], A[2] - B[2]) < 38; });
    if (m) m.n += c1.n; else merged.push({ ...c1 });
  }
  const total = merged.reduce((a, c) => a + c.n, 0) || 1;
  return merged.filter(c => c.n / total > .004).slice(0, 10);
}

/** Leitet aus Logofarben eine Markenpalette ab. */
function paletteFromLogo(cols) {
  const nonWhite = cols.filter(c => c.l < .93);
  const chroma = nonWhite.filter(c => c.s > .22 && c.l > .12 && c.l < .85);
  const darks = nonWhite.filter(c => c.l <= .25);
  const byWeight = (a, b) => b.n * (.4 + b.s) - a.n * (.4 + a.s);
  const sorted = [...chroma].sort(byWeight);
  let primary = sorted[0], accent = sorted.find(c => primary && hueDist(c.h, primary.h) > 35);
  let dark = darks.sort((a, b) => b.n - a.n)[0];
  if (!primary && dark) primary = dark;
  if (!primary) primary = nonWhite[0] || { hex: "#1F5BD8", h: 220, s: .7, l: .48 };
  if (!accent) {
    // keine zweite Farbe im Logo: Akzent aus der Hauptfarbe ableiten
    accent = primary.s < .15 ? { hex: "#D9822B" } : { hex: hsl2hex((primary.h + 28) % 360, Math.min(.85, primary.s + .1), Math.min(.55, Math.max(.4, primary.l))) };
  }
  // ein sehr dunkles Logo-Grün/Blau eignet sich als Hauptfarbe besser als ein grelles Akzentrot
  if (dark && dark.s > .15 && dark.n > primary.n * 1.4) { accent = primary; primary = dark; }
  const darkHex = dark ? dark.hex : hsl2hex(primary.h || 0, Math.min(.5, primary.s || .2), .14);
  let p = primary.hex;
  if (lum(p) > .45) p = mix(p, "#000000", .35); // Hauptfarbe muss auf Weiß lesbar sein
  let d = lum(darkHex) > .06 ? mix(darkHex, "#000000", .55) : darkHex;
  // Hauptfarbe und Dunkelfarbe sollen sich unterscheiden
  if (contrast(p, d) < 1.25) d = mix(p, "#000000", .45);
  return { primary: p, accent: accent.hex, dark: d };
}

/* ---------------------------------------------------------- Schriften */
const FONTS = {
  modern: { label: "Modern – Bricolage + Source Sans", h: '"Bricolage Grotesque"', b: '"Source Sans 3"', w: 800, q: "family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Source+Sans+3:wght@400;600;700" },
  slab: { label: "Kräftig – Alfa Slab + Source Sans", h: '"Alfa Slab One"', b: '"Source Sans 3"', w: 400, q: "family=Alfa+Slab+One&family=Source+Sans+3:wght@400;600;700" },
  freundlich: { label: "Freundlich – Nunito", h: '"Nunito"', b: '"Nunito"', w: 800, q: "family=Nunito:wght@400;600;800" },
  elegant: { label: "Elegant – Cormorant + Lato", h: '"Cormorant Garamond"', b: '"Lato"', w: 700, q: "family=Cormorant+Garamond:wght@600;700&family=Lato:wght@400;700" },
  sachlich: { label: "Sachlich – Archivo", h: '"Archivo"', b: '"Archivo"', w: 800, q: "family=Archivo:wght@400;600;800" },
  editorial: { label: "Editorial – Playfair + Work Sans", h: '"Playfair Display"', b: '"Work Sans"', w: 800, q: "family=Playfair+Display:wght@700;800&family=Work+Sans:wght@400;600" },
  rund: { label: "Weich – Quicksand + Mulish", h: '"Quicksand"', b: '"Mulish"', w: 700, q: "family=Quicksand:wght@600;700&family=Mulish:wght@400;600;700" },
};

/* ---------------------------------------------------------- Abschnitte */
// Feldtypen: text, area, img, bool, select, list
const SECTIONS = {
  hero: { label: "Einstieg (Hero)", fields: [["eyebrow", "Kleine Überschrift"], ["title", "Titel"], ["text", "Text", "area"], ["image", "Bild", "img"], ["cta1", "Button 1"], ["link1", "Button 1 Ziel", "link"], ["cta2", "Button 2"], ["link2", "Button 2 Ziel", "link"]] },
  features: { label: "Leistungen / Vorteile", fields: [["title", "Titel"], ["intro", "Einleitung", "area"], ["items", "Punkte", "list", [["title", "Titel"], ["text", "Text", "area"]]]] },
  text: { label: "Textblock", fields: [["title", "Titel"], ["text", "Text", "area"]] },
  imageText: { label: "Bild + Text", fields: [["title", "Titel"], ["text", "Text", "area"], ["image", "Bild", "img"], ["reverse", "Bild links", "bool"], ["cta", "Button"], ["link", "Button Ziel", "link"]] },
  stats: { label: "Kennzahlen", fields: [["items", "Zahlen", "list", [["value", "Wert"], ["label", "Beschriftung"]]]] },
  projects: { label: "Projekte (laufend / abgeschlossen)", fields: [["title", "Titel"], ["intro", "Einleitung", "area"], ["filter", "Filter anzeigen", "bool"], ["items", "Projekte", "list", [["title", "Titel"], ["text", "Text", "area"], ["status", "Status", "select", ["laufend", "abgeschlossen"]], ["meta", "Zeitraum / Bereich"], ["image", "Bild", "img"], ["link", "Ziel (optional)", "link"]]]] },
  events: { label: "Termine", fields: [["title", "Titel"], ["items", "Termine", "list", [["date", "Datum (TT.MM.JJJJ)"], ["title", "Titel"], ["text", "Ort / Info"]]]] },
  team: { label: "Team", fields: [["title", "Titel"], ["items", "Personen", "list", [["name", "Name"], ["role", "Rolle"], ["image", "Foto", "img"]]]] },
  testimonials: { label: "Stimmen / Bewertungen", fields: [["title", "Titel"], ["items", "Zitate", "list", [["quote", "Zitat", "area"], ["name", "Name"]]]] },
  pricing: { label: "Preise / Pakete", fields: [["title", "Titel"], ["items", "Pakete", "list", [["name", "Name"], ["price", "Preis"], ["features", "Leistungen (eine pro Zeile)", "area"], ["cta", "Button"], ["link", "Button Ziel", "link"]]]] },
  faq: { label: "Häufige Fragen", fields: [["title", "Titel"], ["items", "Fragen", "list", [["q", "Frage"], ["a", "Antwort", "area"]]]] },
  gallery: { label: "Galerie", fields: [["title", "Titel"], ["items", "Bilder", "list", [["image", "Bild", "img"], ["caption", "Bildunterschrift"]]]] },
  cta: { label: "Aufruf (Call to Action)", fields: [["title", "Titel"], ["text", "Text", "area"], ["cta", "Button"], ["link", "Button Ziel", "link"]] },
  donate: { label: "Spenden", fields: [["title", "Titel"], ["text", "Text", "area"], ["amounts", "Beträge (mit Komma)"], ["payLink", "Link zum Zahlungsanbieter", "link"], ["holder", "Empfänger"], ["iban", "IBAN"], ["purpose", "Verwendungszweck"]] },
  contact: { label: "Kontakt + Formular", fields: [["title", "Titel"], ["text", "Text", "area"], ["formAction", "Formular-Ziel (URL, optional)"]] },
  signup: { label: "Anmeldung / Newsletter", fields: [["title", "Titel"], ["text", "Text", "area"], ["cta", "Button"], ["formAction", "Formular-Ziel (URL, optional)"]] },
  legal: { label: "Rechtstext", fields: [["title", "Titel"], ["text", "Text", "area"]] },
};
const AI_FIELDS = Object.entries(SECTIONS).map(([k, v]) => `${k}: ` + v.fields.filter(f => f[2] !== "img").map(f => f[2] === "list" ? `${f[0]}:[{${f[3].filter(g => g[2] !== "img").map(g => g[0]).join(",")}}]` : f[0]).join(", ")).join("\n");

function defaultSection(type) {
  const D = {
    hero: { eyebrow: "", title: "Überschrift, die sagt, was ihr tut", text: "Ein bis zwei Sätze für wen ihr da seid und was man hier findet.", cta1: "Kontakt aufnehmen", link1: "kontakt", cta2: "", link2: "" },
    features: { title: "Was wir bieten", intro: "", items: [{ title: "Erster Punkt", text: "Kurz erklären." }, { title: "Zweiter Punkt", text: "Kurz erklären." }, { title: "Dritter Punkt", text: "Kurz erklären." }] },
    text: { title: "Überschrift", text: "Hier steht euer Text." },
    imageText: { title: "Überschrift", text: "Text neben dem Bild.", image: "", reverse: false, cta: "", link: "" },
    stats: { items: [{ value: "10+", label: "Jahre Erfahrung" }, { value: "250", label: "zufriedene Kunden" }, { value: "3", label: "Standorte" }] },
    projects: { title: "Projekte", intro: "", filter: true, items: [{ title: "Projekt A", text: "Kurzbeschreibung.", status: "laufend", meta: "seit 2025" }, { title: "Projekt B", text: "Kurzbeschreibung.", status: "abgeschlossen", meta: "2024" }] },
    events: { title: "Termine", items: [{ date: "15.01.2027", title: "Veranstaltung", text: "18:00 Uhr · Ort" }] },
    team: { title: "Team", items: [{ name: "Name", role: "Rolle" }, { name: "Name", role: "Rolle" }] },
    testimonials: { title: "Das sagen andere", items: [{ quote: "Ein kurzes, echtes Zitat.", name: "Name" }] },
    pricing: { title: "Preise", items: [{ name: "Basis", price: "[Preis]", features: "Leistung 1\nLeistung 2", cta: "Anfragen", link: "kontakt" }, { name: "Plus", price: "[Preis]", features: "Leistung 1\nLeistung 2\nLeistung 3", cta: "Anfragen", link: "kontakt" }] },
    faq: { title: "Häufige Fragen", items: [{ q: "Frage?", a: "Antwort." }] },
    gallery: { title: "Galerie", items: [] },
    cta: { title: "Bereit für den nächsten Schritt?", text: "Ein Satz, der zum Handeln einlädt.", cta: "Jetzt starten", link: "kontakt" },
    donate: { title: "Jetzt spenden", text: "Ihre Spende hilft direkt vor Ort.", amounts: "25, 50, 100", payLink: "", holder: "", iban: "", purpose: "Spende" },
    contact: { title: "Kontakt", text: "Schreiben Sie uns, wir melden uns.", formAction: "" },
    signup: { title: "Jetzt anmelden", text: "Tragen Sie sich ein, wir melden uns mit allen Infos.", cta: "Anmelden", formAction: "" },
    legal: { title: "Rechtliches", text: "" },
  };
  return { id: uid(), type, ...clone(D[type] || {}) };
}

/* ---------------------------------------------------------- Projekt-Vorlagen */
const LEGAL_IMPRESSUM = "Angaben gemäß § 5 DDG\n\n[Name / Organisation]\n[Straße Nr.]\n[PLZ Ort]\n\nVertreten durch: [Name]\nKontakt: [E-Mail], [Telefon]\n\nRegistereintrag: [Registergericht, Nummer]\n\nVerantwortlich für den Inhalt nach § 18 Abs. 2 MStV: [Name, Anschrift]";
const LEGAL_DATENSCHUTZ = "1. Verantwortlicher\n[Name, Anschrift, E-Mail]\n\n2. Hosting\nDiese Website wird bei [Hoster] betrieben. Beim Aufruf werden technisch notwendige Daten (IP-Adresse, Datum, Uhrzeit, aufgerufene Seite) verarbeitet. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO.\n\n3. Schriftarten\nDiese Website lädt Schriftarten von Google Fonts. Dabei wird Ihre IP-Adresse an Google übertragen. Empfehlung: Schriften lokal einbinden.\n\n4. Formulare\nAngaben aus Formularen verarbeiten wir zur Bearbeitung Ihrer Anfrage (Art. 6 Abs. 1 lit. b DSGVO) und löschen sie, wenn sie nicht mehr benötigt werden.\n\n5. Ihre Rechte\nAuskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit, Widerspruch und Beschwerde bei einer Aufsichtsbehörde.\n\n[Bitte vor Veröffentlichung prüfen lassen.]";

function sec(type, data) { return { ...defaultSection(type), ...data }; }
function pg(title, slug, sections, extra = {}) { return { id: uid(), title, slug, kind: "page", inNav: true, description: "", sections, ...extra }; }

const PAGE_TPL = {
  blank: t => pg(t || "Neue Seite", slugify(t || "neue-seite"), [sec("text", { title: t || "Neue Seite", text: "" })]),
  landing: t => pg(t || "Landingpage", slugify(t || "aktion"), [
    sec("hero", { eyebrow: "Aktion", title: t || "Ein klares Versprechen", text: "Für wen ist das Angebot, und was haben sie davon?", cta1: "Jetzt anmelden", link1: "#anmelden", cta2: "", link2: "" }),
    sec("features", { title: "Darum lohnt es sich", items: [{ title: "Vorteil 1", text: "Kurz und konkret." }, { title: "Vorteil 2", text: "Kurz und konkret." }, { title: "Vorteil 3", text: "Kurz und konkret." }] }),
    sec("testimonials", {}), sec("faq", {}),
    sec("signup", { title: "Jetzt anmelden", anchor: "anmelden" }),
  ], { kind: "landing", inNav: false }),
  about: t => pg(t || "Über uns", "ueber-uns", [sec("text", { title: t || "Über uns", text: "Wer wir sind und warum es uns gibt." }), sec("team", {})]),
  services: t => pg(t || "Leistungen", "leistungen", [sec("features", { title: t || "Leistungen" }), sec("pricing", {}), sec("cta", {})]),
  projects: t => pg(t || "Projekte", "projekte", [sec("projects", { title: t || "Unsere Projekte" })]),
  events: t => pg(t || "Termine", "termine", [sec("events", {})]),
  donate: t => pg(t || "Spenden", "spenden", [sec("donate", {}), sec("faq", { title: "Fragen zur Spende", items: [{ q: "Bekomme ich eine Spendenquittung?", a: "Ja. Bis 300 € genügt der Kontoauszug, darüber senden wir eine Zuwendungsbestätigung." }] })]),
  contact: t => pg(t || "Kontakt", "kontakt", [sec("contact", {})]),
  faq: t => pg(t || "Häufige Fragen", "faq", [sec("faq", {})]),
  impressum: () => pg("Impressum", "impressum", [sec("legal", { title: "Impressum", text: LEGAL_IMPRESSUM })], { inNav: false }),
  datenschutz: () => pg("Datenschutz", "datenschutz", [sec("legal", { title: "Datenschutzerklärung", text: LEGAL_DATENSCHUTZ })], { inNav: false }),
};

function templateProject(type, name, desc) {
  name = name || "Meine Website";
  const d = desc || "";
  const home = (eyebrow, title, text, cta1, link1, extra) => pg("Start", "index", [sec("hero", { eyebrow, title, text: d || text, cta1, link1, cta2: "Mehr erfahren", link2: extra[0] }), ...extra[1]]);
  let pages;
  switch (type) {
    case "verein": pages = [
      home(name, "Gemeinsam mehr bewegen", "Wir sind ein Verein, der Menschen verbindet und vor Ort anpackt.", "Jetzt spenden", "spenden", ["projekte", [sec("stats", { items: [{ value: "[Jahr]", label: "gegründet" }, { value: "[Zahl]", label: "Mitglieder" }, { value: "[Zahl]", label: "Projekte" }] }), sec("features", { title: "Was wir tun", items: [{ title: "Beraten", text: "Wir helfen im Alltag." }, { title: "Bilden", text: "Workshops und Nachhilfe." }, { title: "Begegnen", text: "Feste und Treffpunkte." }] }), sec("projects", { title: "Laufende Projekte", filter: false, items: [{ title: "[Projekt]", text: "Kurzbeschreibung.", status: "laufend", meta: "seit [Jahr]" }] }), sec("cta", { title: "Mitmachen statt zuschauen", text: "Werde Mitglied oder hilf ehrenamtlich.", cta: "So machst du mit", link: "mitmachen" })]]),
      PAGE_TPL.about(), PAGE_TPL.projects(),
      pg("Mitmachen", "mitmachen", [sec("features", { title: "So kannst du mitmachen", items: [{ title: "Mitglied werden", text: "Ab [Betrag] im Monat." }, { title: "Ehrenamt", text: "Zeit schenken, wo du magst." }, { title: "Kooperieren", text: "Gemeinsame Projekte mit Schulen und Firmen." }] }), sec("signup", { title: "Mitglied werden", text: "Schick uns deine Daten, wir senden dir den Antrag.", cta: "Antrag anfordern" })]),
      PAGE_TPL.events(), PAGE_TPL.donate(), PAGE_TPL.contact(), PAGE_TPL.impressum(), PAGE_TPL.datenschutz()]; break;
    case "praxis": pages = [
      home(name, "Gesund werden mit Zeit und Fachwissen", "Wir behandeln individuell und nehmen uns Zeit für Sie.", "Termin anfragen", "kontakt", ["leistungen", [sec("features", { title: "Schwerpunkte", items: [{ title: "[Leistung]", text: "Kurz erklärt." }, { title: "[Leistung]", text: "Kurz erklärt." }, { title: "[Leistung]", text: "Kurz erklärt." }] }), sec("testimonials", {}), sec("cta", { title: "Termin vereinbaren", text: "Rufen Sie an oder schreiben Sie uns.", cta: "Kontakt", link: "kontakt" })]]),
      PAGE_TPL.services(), pg("Team", "team", [sec("team", { title: "Unser Team" })]), PAGE_TPL.faq(), PAGE_TPL.contact(), PAGE_TPL.impressum(), PAGE_TPL.datenschutz()]; break;
    case "handwerk": pages = [
      home(name, "Saubere Arbeit, fester Preis, pünktlich", "Wir planen, bauen und reparieren in der Region.", "Angebot anfordern", "kontakt", ["leistungen", [sec("features", { title: "Leistungen", items: [{ title: "[Leistung]", text: "" }, { title: "[Leistung]", text: "" }, { title: "[Leistung]", text: "" }] }), sec("gallery", { title: "Referenzen" }), sec("testimonials", {}), sec("cta", { title: "Projekt besprechen", text: "Kostenlose Erstberatung vor Ort.", cta: "Angebot anfordern", link: "kontakt" })]]),
      PAGE_TPL.services(), pg("Referenzen", "referenzen", [sec("gallery", { title: "Referenzen" })]), PAGE_TPL.contact(), PAGE_TPL.impressum(), PAGE_TPL.datenschutz()]; break;
    case "gastro": pages = [
      home(name, "Gutes Essen, das nach Zuhause schmeckt", "Frisch gekocht, mit Zutaten aus der Region.", "Tisch reservieren", "reservieren", ["speisekarte", [sec("imageText", { title: "Unsere Küche", text: "Erzählt, was eure Küche besonders macht." }), sec("events", { title: "Öffnungszeiten & Events", items: [{ date: "", title: "Mo–Fr", text: "11–22 Uhr" }] }), sec("testimonials", {})]]),
      pg("Speisekarte", "speisekarte", [sec("pricing", { title: "Speisekarte", items: [{ name: "Vorspeisen", price: "", features: "[Gericht] – [Preis]\n[Gericht] – [Preis]", cta: "", link: "" }, { name: "Hauptgerichte", price: "", features: "[Gericht] – [Preis]\n[Gericht] – [Preis]", cta: "", link: "" }] })]),
      pg("Reservieren", "reservieren", [sec("signup", { title: "Tisch reservieren", text: "Datum, Uhrzeit und Personenzahl angeben.", cta: "Anfrage senden" })]), PAGE_TPL.contact(), PAGE_TPL.impressum(), PAGE_TPL.datenschutz()]; break;
    case "agentur": pages = [
      home(name, "Wir machen eure Marke sichtbar", "Strategie, Design und Umsetzung aus einer Hand.", "Projekt anfragen", "kontakt", ["leistungen", [sec("features", { title: "Leistungen", items: [{ title: "Strategie", text: "" }, { title: "Design", text: "" }, { title: "Umsetzung", text: "" }] }), sec("stats", {}), sec("testimonials", {}), sec("cta", {})]]),
      PAGE_TPL.services(), pg("Referenzen", "referenzen", [sec("projects", { title: "Referenzen", filter: false })]), PAGE_TPL.about(), PAGE_TPL.contact(), PAGE_TPL.impressum(), PAGE_TPL.datenschutz()]; break;
    case "event": pages = [
      pg("Start", "index", [sec("hero", { eyebrow: "[Datum] · [Ort]", title: name, text: d || "Ein Satz, warum man dabei sein muss.", cta1: "Jetzt anmelden", link1: "#anmelden", cta2: "Programm", link2: "#programm" }), sec("features", { title: "Das erwartet dich" }), sec("events", { title: "Programm", anchor: "programm" }), sec("faq", {}), sec("signup", { title: "Jetzt anmelden", anchor: "anmelden" })]),
      PAGE_TPL.impressum(), PAGE_TPL.datenschutz()]; break;
    default: pages = [pg("Start", "index", [sec("hero", { eyebrow: "", title: name, text: d || "Kurz sagen, worum es geht.", cta1: "", link1: "", cta2: "", link2: "" })]), PAGE_TPL.impressum(), PAGE_TPL.datenschutz()];
  }
  return {
    id: uid(), version: 1, name, updated: Date.now(),
    site: { name, tagline: "", email: "", phone: "", address: "", ctaLabel: type === "verein" ? "Spenden" : "", ctaLink: type === "verein" ? "spenden" : "", facebook: "", instagram: "", domain: "", notice: "" },
    brand: { logo: "", colors: { primary: "#1F5BD8", accent: "#E8833A", dark: "#14213D" }, font: "modern", hero: "dark", radius: "10", bg: "tint", showName: true },
    assets: {}, pages,
  };
}

/* ---------------------------------------------------------- Seiten erzeugen */
function themeVars(b) {
  const { primary, accent, dark } = b.colors;
  const text = lum(dark) < .03 ? dark : mix(dark, "#000000", .5);
  const bg = b.bg === "white" ? "#FFFFFF" : mix(primary, "#FFFFFF", .955);
  const soft = mix(primary, "#FFFFFF", .9);
  const heroBg = b.hero === "light" ? soft : b.hero === "primary" ? primary : dark;
  const heroFg = b.hero === "light" ? text : onColor(heroBg);
  const eyebrowOnHero = contrast(accent, heroBg) >= 3 ? accent : heroFg;
  const r = Number(b.radius || 10);
  const f = FONTS[b.font] || FONTS.modern;
  return {
    "--primary": primary, "--accent": accent, "--dark": dark, "--text": text, "--bg": bg, "--surface": "#FFFFFF", "--soft": soft,
    "--muted": mix(text, "#FFFFFF", .36), "--line": mix(text, "#FFFFFF", .86),
    "--on-primary": onColor(primary), "--on-accent": onColor(accent), "--on-dark": onColor(dark),
    "--hero-bg": heroBg, "--hero-fg": heroFg, "--hero-eyebrow": eyebrowOnHero,
    "--eyebrow": contrast(accent, bg) >= 3 ? accent : primary,
    "--r": r + "px", "--r2": Math.round(r * 1.4) + "px",
    "--fh": `${f.h}, Georgia, serif`, "--fb": `${f.b}, "Segoe UI", system-ui, sans-serif`, "--fhw": f.w,
  };
}

const SITE_CSS = `*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;background:var(--bg);color:var(--text);font:400 17px/1.6 var(--fb)}
img{max-width:100%;display:block}[hidden]{display:none!important}
h1,h2,h3{font-family:var(--fh);font-weight:var(--fhw);line-height:1.12;margin:0;text-wrap:balance}
h1{font-size:clamp(2.1rem,5vw,3.6rem);letter-spacing:-.01em}h2{font-size:clamp(1.6rem,3.2vw,2.4rem)}h3{font-size:1.2rem}
p{margin:0}a{color:var(--primary)}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.w{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.sec{padding-block:4rem}.sec+.sec:not(.band){padding-top:1rem}.band{background:var(--soft)}
.head{display:grid;gap:.6rem;margin-bottom:2rem;max-width:62ch}.lead{font-size:1.12rem;color:var(--muted)}
.eyebrow{font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--eyebrow)}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:.75em 1.35em;border-radius:var(--r);font:700 1rem var(--fb);text-decoration:none;border:2px solid transparent;cursor:pointer;transition:transform .15s}
.btn:hover{transform:translateY(-1px)}.btn-a{background:var(--accent);color:var(--on-accent)}.btn-p{background:var(--primary);color:var(--on-primary)}.btn-o{border-color:currentColor;color:inherit;background:transparent}
.notice{background:var(--accent);color:var(--on-accent);font-size:.9rem}.notice .w{padding-block:.45rem}
header.hd{position:sticky;top:0;z-index:20;background:var(--surface);border-bottom:1px solid var(--line)}
.hd .w{display:flex;align-items:center;gap:1rem;padding-block:.65rem;position:relative}
.brand{display:flex;align-items:center;gap:.7rem;margin-right:auto;text-decoration:none;color:var(--text);font:var(--fhw) 1.3rem/1.1 var(--fh);min-width:0}
.brand img{height:46px;width:auto;max-width:200px;object-fit:contain}.brand small{display:block;font:400 .8rem var(--fb);color:var(--muted)}
nav.mn ul{list-style:none;margin:0;padding:0;display:flex;gap:.15rem;flex-wrap:wrap}
nav.mn a{display:block;padding:.45rem .6rem;font-size:.97rem;border-radius:var(--r);text-decoration:none;color:var(--text);font-weight:600}
nav.mn a:hover,nav.mn a[aria-current]{background:var(--soft);color:var(--primary)}
.burger{display:none;background:none;border:1px solid var(--line);border-radius:var(--r);padding:.45rem .7rem;font:600 .95rem var(--fb);color:var(--text);cursor:pointer}
@media(max-width:1060px){.burger{display:inline-block}nav.mn{display:none;position:absolute;top:100%;left:0;right:0;background:var(--surface);border-bottom:1px solid var(--line)}nav.mn.open{display:block}nav.mn ul{flex-direction:column;padding:.5rem max(16px,env(safe-area-inset-right,0px)) 1rem max(16px,env(safe-area-inset-left,0px))}.hd .btn{padding:.55em 1em}}
@media(max-width:460px){.brand small{display:none}}
.hero{background:var(--hero-bg);color:var(--hero-fg)}.hero .w{display:grid;grid-template-columns:1.1fr 1fr;gap:2.5rem;align-items:center;padding-block:4.5rem}
.hero.noimg .w{grid-template-columns:minmax(0,760px)}.hero .eyebrow{color:var(--hero-eyebrow)}.hero .lead{color:inherit;opacity:.86;margin-top:1rem}
.hero img{border-radius:var(--r2);width:100%;height:auto}.acts{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.7rem}
@media(max-width:820px){.hero .w{grid-template-columns:1fr;padding-block:3rem}}
.feats{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:2rem}
.feat{border-top:4px solid var(--accent);padding-top:1rem;display:grid;gap:.4rem;align-content:start}.feat:nth-child(3n+2){border-color:var(--primary)}.feat:nth-child(3n+3){border-color:var(--dark)}.feat p{color:var(--muted)}
.prose{max-width:70ch;display:grid;gap:1rem}.prose p{color:var(--muted)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem;align-items:center}.split.rev>:first-child{order:2}.split img{border-radius:var(--r2);width:100%;height:auto}
@media(max-width:820px){.split{grid-template-columns:1fr}.split.rev>:first-child{order:0}}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:var(--r2);overflow:hidden}
.stats div{background:var(--surface);padding:1.3rem 1.2rem}.stats b{display:block;font:var(--fhw) 2rem var(--fh);color:var(--primary);font-variant-numeric:tabular-nums}.stats span{color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:1.3rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r2);overflow:hidden;display:grid;grid-template-rows:auto 1fr;text-decoration:none;color:var(--text)}
.card .pic{aspect-ratio:16/9;width:100%;object-fit:cover;background:repeating-linear-gradient(135deg,var(--soft) 0 14px,var(--surface) 14px 28px)}
.card .bd{padding:1.1rem 1.2rem 1.3rem;display:grid;gap:.45rem;align-content:start}.card .bd p{color:var(--muted)}.meta{font-size:.85rem;color:var(--muted)}
.st{justify-self:start;font-size:.75rem;font-weight:700;padding:.15rem .6rem;border-radius:99px;background:var(--soft);color:var(--primary)}.st.done{color:var(--muted)}
.filters{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1.4rem}
.filters button{font:600 .95rem var(--fb);padding:.5rem 1rem;border-radius:99px;border:1px solid var(--line);background:var(--surface);color:var(--text);cursor:pointer}
.filters button[aria-pressed=true]{background:var(--text);color:var(--surface);border-color:var(--text)}
.evs{display:grid;gap:.8rem;max-width:780px}.ev{display:grid;grid-template-columns:76px 1fr;gap:1rem;align-items:start;background:var(--surface);border:1px solid var(--line);border-radius:var(--r2);padding:.9rem}
.ev .dt{text-align:center;background:var(--soft);border-radius:var(--r);padding:.4rem 0;line-height:1.1}.ev .dt b{display:block;font:var(--fhw) 1.5rem var(--fh);color:var(--primary)}.ev .dt span{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}.ev p{color:var(--muted);font-size:.95rem}
.team{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:1.3rem}.person{display:grid;gap:.25rem}.person span{color:var(--muted);font-size:.92rem}
.av{aspect-ratio:1;width:100%;border-radius:var(--r2);object-fit:cover;display:grid;place-items:center;font:var(--fhw) 2rem var(--fh);background:var(--primary);color:var(--on-primary)}
.person:nth-child(3n+2) .av{background:var(--accent);color:var(--on-accent)}.person:nth-child(3n+3) .av{background:var(--dark);color:var(--on-dark)}
.quotes{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.3rem}.quotes figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r2);padding:1.4rem;display:grid;gap:.8rem}
.quotes blockquote{margin:0;font-size:1.08rem}.quotes blockquote::before{content:"\\201E";font:var(--fhw) 2.6rem/0 var(--fh);color:var(--accent);display:block;margin:1rem 0 .4rem}.quotes figcaption{color:var(--muted);font-weight:600}
.prices{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.3rem}.price{background:var(--surface);border:1px solid var(--line);border-radius:var(--r2);padding:1.5rem;display:grid;gap:.8rem;align-content:start}
.price .pr{font:var(--fhw) 2rem var(--fh);color:var(--primary)}.price ul{margin:0;padding-left:1.1rem;color:var(--muted);display:grid;gap:.3rem}
.faq{display:grid;gap:.6rem;max-width:780px}.faq details{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:.9rem 1.1rem}.faq summary{cursor:pointer;font-weight:700}.faq details p{margin-top:.6rem;color:var(--muted)}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem}.gal figure{margin:0;display:grid;gap:.4rem}.gal img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r)}.gal figcaption{font-size:.9rem;color:var(--muted)}
.ctab{background:var(--dark);color:var(--on-dark);border-radius:var(--r2);padding:2.2rem;display:flex;justify-content:space-between;gap:1.5rem;align-items:center;flex-wrap:wrap}.ctab p{opacity:.85;max-width:56ch;margin-top:.4rem}
.two{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem;align-items:start}@media(max-width:820px){.two{grid-template-columns:1fr}}.two>*{min-width:0}
.form{display:grid;gap:1rem;background:var(--surface);border:1px solid var(--line);border-radius:var(--r2);padding:1.5rem}
.field{display:grid;gap:.3rem}.field label{font-weight:600;font-size:.92rem}.field input,.field textarea,.field select{font:inherit;padding:.65rem .8rem;border:1px solid var(--line);border-radius:var(--r);background:var(--bg);color:var(--text);width:100%}
.msg{font-weight:600;color:var(--primary)}
.amts{display:flex;gap:.5rem;flex-wrap:wrap}.amts button{flex:1;min-width:70px;padding:.7rem;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);font:700 1rem var(--fb);color:var(--text);cursor:pointer;font-variant-numeric:tabular-nums}.amts button[aria-pressed=true]{background:var(--text);color:var(--surface);border-color:var(--text)}
.bank{display:grid;gap:.15rem;margin:0;border:1px dashed var(--line);border-radius:var(--r);padding:1rem;font-variant-numeric:tabular-nums}.bank dt{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}.bank dd{margin:0 0 .5rem;font-weight:700;word-break:break-word}
.info{display:grid;gap:.8rem;margin:0}.info dt{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}.info dd{margin:0;font-weight:600}
footer.ft{background:var(--dark);color:var(--on-dark);padding-block:3rem 1.4rem}.ft .cols{display:grid;grid-template-columns:2fr 1fr 1fr;gap:2rem}@media(max-width:720px){.ft .cols{grid-template-columns:1fr}}
.ft h3{font-size:1rem;margin-bottom:.6rem}.ft a{color:inherit;opacity:.85}.ft ul{list-style:none;padding:0;margin:0;display:grid;gap:.35rem}.ft p{opacity:.85}.ft .logo{height:42px;width:auto;max-width:180px;margin-bottom:.7rem;object-fit:contain;background:#fff;padding:4px 8px;border-radius:var(--r)}
.ft .legal{border-top:1px solid color-mix(in srgb,currentColor 18%,transparent);margin-top:2rem;padding-top:1rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;font-size:.85rem;opacity:.8}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}`;

const SITE_JS = `document.querySelector(".burger")?.addEventListener("click",e=>{const n=document.querySelector("nav.mn"),o=n.classList.toggle("open");e.currentTarget.setAttribute("aria-expanded",o)});
document.querySelectorAll("[data-pfilter]").forEach(g=>g.addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));const f=b.dataset.f;g.parentElement.querySelectorAll("[data-status]").forEach(c=>c.hidden=f!=="alle"&&c.dataset.status!==f)}));
document.querySelectorAll(".amts").forEach(g=>g.addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));const i=g.parentElement.querySelector("[data-amount]");if(i)i.textContent=b.dataset.v+" €"}));
document.querySelectorAll("form[data-local]").forEach(f=>f.addEventListener("submit",e=>{e.preventDefault();const m=f.querySelector(".msg");m.hidden=false;m.textContent=f.checkValidity()?f.dataset.local:"Bitte alle Pflichtfelder ausfüllen."}));`;

/** ctx: { P, mode: "preview"|"export", img(id) } */
function linkHref(v, ctx) {
  v = String(v || "").trim();
  if (!v) return "#";
  if (/^(https?:|mailto:|tel:|#)/.test(v)) return v;
  const clean = v.replace(/\.html$/, "").replace(/^\//, "");
  const [slug, hash] = clean.split("#");
  const p = ctx.P.pages.find(x => x.slug === slug);
  if (p) return (p.slug === "index" ? "index" : p.slug) + ".html" + (hash ? "#" + hash : "");
  return v;
}
const ext = (v) => /^https?:/.test(v) ? ' target="_blank" rel="noopener"' : "";
const btn = (label, link, cls, ctx) => label ? `<a class="btn ${cls}" href="${esc(linkHref(link, ctx))}"${ext(link)}>${esc(label)}</a>` : "";
const head = (title, intro) => title || intro ? `<div class="head">${title ? `<h2>${esc(title)}</h2>` : ""}${intro ? `<p class="lead">${esc(intro)}</p>` : ""}</div>` : "";
function formEl(s, ctx, fields, submit) {
  const action = ctx.mode === "export" && s.formAction ? ` action="${esc(s.formAction)}" method="POST"` : "";
  const email = ctx.P.site.email;
  const local = ctx.mode === "preview" ? "Vorschau: Das Formular wird erst auf der fertigen Website gesendet."
    : `Das Formular ist noch nicht verbunden.${email ? " Bitte schreiben Sie an " + email + "." : ""}`;
  return `<form class="form"${action}${action ? "" : ` data-local="${esc(local)}"`}>${fields}<button class="btn btn-a" type="submit">${esc(submit)}</button><p class="msg" hidden></p></form>`;
}

const R = {
  hero(s, ctx) {
    const im = ctx.img(s.image);
    return `<section class="hero${im ? "" : " noimg"}"${s.anchor ? ` id="${esc(s.anchor)}"` : ""}><div class="w"><div>${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ""}<h1>${esc(s.title)}</h1>${s.text ? `<p class="lead">${esc(s.text)}</p>` : ""}${s.cta1 || s.cta2 ? `<div class="acts">${btn(s.cta1, s.link1, "btn-a", ctx)}${btn(s.cta2, s.link2, "btn-o", ctx)}</div>` : ""}</div>${im ? `<img src="${esc(im)}" alt="${esc(s.title)}">` : ""}</div></section>`;
  },
  features: s => `<div class="w">${head(s.title, s.intro)}<div class="feats">${(s.items || []).map(i => `<div class="feat"><h3>${esc(i.title)}</h3>${i.text ? `<p>${esc(i.text)}</p>` : ""}</div>`).join("")}</div></div>`,
  text: s => `<div class="w"><div class="prose">${s.title ? `<h2>${esc(s.title)}</h2>` : ""}${para(s.text)}</div></div>`,
  imageText(s, ctx) {
    const im = ctx.img(s.image);
    return `<div class="w"><div class="split${s.reverse ? " rev" : ""}"><div class="prose">${s.title ? `<h2>${esc(s.title)}</h2>` : ""}${para(s.text)}${s.cta ? `<div>${btn(s.cta, s.link, "btn-p", ctx)}</div>` : ""}</div>${im ? `<img src="${esc(im)}" alt="${esc(s.title)}">` : `<div></div>`}</div></div>`;
  },
  stats: s => `<div class="w"><div class="stats">${(s.items || []).map(i => `<div><b>${esc(i.value)}</b><span>${esc(i.label)}</span></div>`).join("")}</div></div>`,
  projects(s, ctx) {
    const items = s.items || [];
    const nL = items.filter(i => i.status !== "abgeschlossen").length, nA = items.length - nL;
    const filter = s.filter && nL && nA ? `<div class="filters" role="group" aria-label="Projekte filtern" data-pfilter><button type="button" data-f="alle" aria-pressed="true">Alle (${items.length})</button><button type="button" data-f="laufend" aria-pressed="false">Laufende Projekte (${nL})</button><button type="button" data-f="abgeschlossen" aria-pressed="false">Abgeschlossene Projekte (${nA})</button></div>` : "";
    return `<div class="w">${head(s.title, s.intro)}${filter}<div class="cards">${items.map(i => {
      const done = i.status === "abgeschlossen", im = ctx.img(i.image), tag = i.link ? "a" : "div";
      return `<${tag} class="card" data-status="${done ? "abgeschlossen" : "laufend"}"${i.link ? ` href="${esc(linkHref(i.link, ctx))}"` : ""}>${im ? `<img class="pic" src="${esc(im)}" alt="">` : `<div class="pic"></div>`}<div class="bd"><span class="st${done ? " done" : ""}">${done ? "Abgeschlossen" : "Laufend"}</span><h3>${esc(i.title)}</h3>${i.meta ? `<span class="meta">${esc(i.meta)}</span>` : ""}${i.text ? `<p>${esc(i.text)}</p>` : ""}</div></${tag}>`;
    }).join("")}</div></div>`;
  },
  events: s => `<div class="w">${head(s.title)}<div class="evs">${(s.items || []).map(i => {
    const m = String(i.date || "").match(/^(\d{1,2})\.(\d{1,2})\./), mon = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
    const dt = m ? `<b>${m[1].padStart(2, "0")}</b><span>${mon[+m[2] - 1] || ""}</span>` : `<b>•</b><span>${esc(i.date)}</span>`;
    return `<div class="ev"><div class="dt">${dt}</div><div><h3>${esc(i.title)}</h3>${i.text ? `<p>${esc(i.text)}</p>` : ""}</div></div>`;
  }).join("")}</div></div>`,
  team: (s, ctx) => `<div class="w">${head(s.title)}<div class="team">${(s.items || []).map(i => {
    const im = ctx.img(i.image), ini = String(i.name || "?").split(/\s+/).map(x => x[0]).join("").slice(0, 2);
    return `<div class="person">${im ? `<img class="av" src="${esc(im)}" alt="${esc(i.name)}">` : `<div class="av" aria-hidden="true">${esc(ini)}</div>`}<b>${esc(i.name)}</b><span>${esc(i.role)}</span></div>`;
  }).join("")}</div></div>`,
  testimonials: s => `<div class="w">${head(s.title)}<div class="quotes">${(s.items || []).map(i => `<figure><blockquote>${esc(i.quote)}</blockquote><figcaption>${esc(i.name)}</figcaption></figure>`).join("")}</div></div>`,
  pricing: (s, ctx) => `<div class="w">${head(s.title)}<div class="prices">${(s.items || []).map(i => `<div class="price"><h3>${esc(i.name)}</h3>${i.price ? `<div class="pr">${esc(i.price)}</div>` : ""}<ul>${lines(i.features).map(f => `<li>${esc(f)}</li>`).join("")}</ul>${btn(i.cta, i.link, "btn-a", ctx)}</div>`).join("")}</div></div>`,
  faq: s => `<div class="w">${head(s.title)}<div class="faq">${(s.items || []).map(i => `<details><summary>${esc(i.q)}</summary><p>${esc(i.a)}</p></details>`).join("")}</div></div>`,
  gallery: (s, ctx) => `<div class="w">${head(s.title)}<div class="gal">${(s.items || []).filter(i => ctx.img(i.image)).map(i => `<figure><img src="${esc(ctx.img(i.image))}" alt="${esc(i.caption)}" loading="lazy">${i.caption ? `<figcaption>${esc(i.caption)}</figcaption>` : ""}</figure>`).join("") || `<p class="meta">Noch keine Bilder.</p>`}</div></div>`,
  cta: (s, ctx) => `<div class="w"><div class="ctab"><div><h2>${esc(s.title)}</h2>${s.text ? `<p>${esc(s.text)}</p>` : ""}</div>${btn(s.cta, s.link, "btn-a", ctx)}</div></div>`,
  donate(s, ctx) {
    const amts = String(s.amounts || "").split(",").map(x => x.trim()).filter(Boolean);
    const bank = s.iban ? `<dl class="bank">${s.holder ? `<dt>Empfänger</dt><dd>${esc(s.holder)}</dd>` : ""}<dt>IBAN</dt><dd>${esc(s.iban)}</dd>${s.purpose ? `<dt>Verwendungszweck</dt><dd>${esc(s.purpose)}</dd>` : ""}</dl>` : "";
    return `<div class="w"><div class="two"><div class="prose"><h2>${esc(s.title)}</h2>${para(s.text)}${bank}</div><div class="form">${amts.length ? `<div class="amts" role="group" aria-label="Betrag">${amts.map((a, i) => `<button type="button" data-v="${esc(a)}" aria-pressed="${i === 1 || amts.length === 1 ? "true" : "false"}">${esc(a)} €</button>`).join("")}</div><p>Gewählt: <b data-amount>${esc(amts[Math.min(1, amts.length - 1)])} €</b></p>` : ""}${s.payLink ? `<a class="btn btn-a" href="${esc(linkHref(s.payLink, ctx))}" target="_blank" rel="noopener">Jetzt online spenden</a>` : `<p class="meta">Online-Spenden: Link zum Zahlungsanbieter (z. B. PayPal, betterplace) im Baukasten eintragen.</p>`}</div></div></div>`;
  },
  contact(s, ctx) {
    const S = ctx.P.site;
    const info = [S.address && ["Adresse", S.address], S.email && ["E-Mail", S.email], S.phone && ["Telefon", S.phone]].filter(Boolean);
    return `<div class="w"><div class="two"><div class="prose"><h2>${esc(s.title)}</h2>${para(s.text)}${info.length ? `<dl class="info">${info.map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join("")}</dl>` : ""}</div>${formEl(s, ctx, `<div class="field"><label for="f-name-${s.id}">Name *</label><input id="f-name-${s.id}" name="name" required></div><div class="field"><label for="f-mail-${s.id}">E-Mail *</label><input id="f-mail-${s.id}" name="email" type="email" required></div><div class="field"><label for="f-msg-${s.id}">Nachricht *</label><textarea id="f-msg-${s.id}" name="nachricht" rows="5" required></textarea></div>`, "Nachricht senden")}</div></div>`;
  },
  signup: (s, ctx) => `<div class="w"><div class="two"><div class="prose"><h2>${esc(s.title)}</h2>${para(s.text)}</div>${formEl(s, ctx, `<div class="field"><label for="s-name-${s.id}">Name *</label><input id="s-name-${s.id}" name="name" required></div><div class="field"><label for="s-mail-${s.id}">E-Mail *</label><input id="s-mail-${s.id}" name="email" type="email" required></div>`, s.cta || "Absenden")}</div></div>`,
  legal: s => `<div class="w"><div class="prose"><h1>${esc(s.title)}</h1>${para(s.text)}</div></div>`,
};
const BANDED = new Set(["stats", "testimonials", "donate"]);

function renderSections(page, ctx) {
  return page.sections.map((s, i) => {
    const r = R[s.type];
    if (!r) return "";
    const inner = r(s, ctx);
    if (s.type === "hero") return inner;
    const band = BANDED.has(s.type) || s.band;
    return `<section class="sec${band ? " band" : ""}"${s.anchor ? ` id="${esc(s.anchor)}"` : ""}>${inner}</section>`;
  }).join("\n");
}

function renderPage(P, page, mode) {
  const ctx = { P, mode, img: v => resolveImg(P, v, mode) };
  const S = P.site, B = P.brand, f = FONTS[B.font] || FONTS.modern;
  const vars = Object.entries(themeVars(B)).map(([k, v]) => `${k}:${v}`).join(";");
  const nav = P.pages.filter(p => p.inNav);
  const logo = ctx.img(B.logo);
  const file = p => (p.slug === "index" ? "index" : p.slug) + ".html";
  const navHtml = nav.map(p => `<li><a href="${file(p)}"${p.id === page.id ? ' aria-current="page"' : ""}>${esc(p.title)}</a></li>`).join("");
  const legal = P.pages.filter(p => !p.inNav && p.kind !== "landing");
  const social = [S.facebook && ["Facebook", S.facebook], S.instagram && ["Instagram", S.instagram]].filter(Boolean);
  const title = page.slug === "index" ? (S.name + (S.tagline ? " – " + S.tagline : "")) : `${page.title} · ${S.name}`;
  const desc = page.description || S.tagline || "";
  const fonts = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?${f.q}&display=swap">`;
  const css = mode === "export" ? `<link rel="stylesheet" href="assets/style.css">` : `<style>:root{${vars}}${SITE_CSS}</style>`;
  const js = mode === "export" ? `<script src="assets/site.js"><\/script>` : `<script>${SITE_JS}${PREVIEW_JS}<\/script>`;
  const brand = `<a class="brand" href="index.html">${logo ? `<img src="${esc(logo)}" alt="${esc(S.name)}">` : ""}${!logo || B.showName ? `<span>${esc(S.name)}${S.tagline ? `<small>${esc(S.tagline)}</small>` : ""}</span>` : ""}</a>`;
  return `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
${desc ? `<meta name="description" content="${esc(desc)}">` : ""}
<meta property="og:title" content="${esc(title)}">
${fonts}
${css}
</head>
<body>
${S.notice ? `<div class="notice"><div class="w">${esc(S.notice)}</div></div>` : ""}
<header class="hd"><div class="w">${brand}<nav class="mn" id="mn" aria-label="Hauptmenü"><ul>${navHtml}</ul></nav><button class="burger" type="button" aria-expanded="false" aria-controls="mn">Menü</button>${S.ctaLabel ? btn(S.ctaLabel, S.ctaLink, "btn-a", ctx) : ""}</div></header>
<main>
${renderSections(page, ctx)}
</main>
<footer class="ft"><div class="w"><div class="cols"><div>${logo ? `<img class="logo" src="${esc(logo)}" alt="">` : ""}<h3>${esc(S.name)}</h3><p>${[S.address, S.email, S.phone].filter(Boolean).map(esc).join("<br>")}</p></div><div><h3>Seiten</h3><ul>${nav.map(p => `<li><a href="${file(p)}">${esc(p.title)}</a></li>`).join("")}</ul></div><div>${social.length ? `<h3>Folgen</h3><ul>${social.map(([n, u]) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${n}</a></li>`).join("")}</ul>` : ""}</div></div><div class="legal"><span>© ${new Date().getFullYear()} ${esc(S.name)}</span><span>${legal.map(p => `<a href="${file(p)}">${esc(p.title)}</a>`).join(" · ")}</span></div></div></footer>
${js}
</body>
</html>`;
}

function resolveImg(P, v, mode) {
  if (!v) return "";
  if (v.startsWith("asset:")) {
    const a = P.assets[v.slice(6)];
    if (!a) return "";
    return mode === "export" ? `assets/img/${a.file}` : a.data;
  }
  return v;
}

const PREVIEW_JS = `
document.addEventListener("click",e=>{const a=e.target.closest("a[href]");if(!a)return;const h=a.getAttribute("href");if(/^(https?:|mailto:|tel:)/.test(h)){e.preventDefault();parent.postMessage({bk:"ext",href:h},"*");return}e.preventDefault();if(h.startsWith("#")){document.getElementById(h.slice(1))?.scrollIntoView();return}parent.postMessage({bk:"nav",href:h},"*")});
let t;addEventListener("scroll",()=>{clearTimeout(t);t=setTimeout(()=>parent.postMessage({bk:"scroll",y:scrollY},"*"),80)},{passive:true});
scrollTo(0,window.__y||0);`;

/* ---------------------------------------------------------- Zustand */
let P = null;          // aktuelles Projekt
let curPageId = null;
let device = "desktop";
let previewScroll = {};
const caps = { sample: null, downloads: null, db: null, user: null, uid: null, images: false };

function page() { return P.pages.find(p => p.id === curPageId) || P.pages[0]; }

/* ---------------------------------------------------------- Speicher */
const LS = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); return true; } catch { return false; } },
  del(k) { try { localStorage.removeItem(k); } catch { /* egal */ } },
};
const store = {
  mode: "local",
  savedAssets: new Set(),
  projRef(id) { return caps.db.doc(`data/users/${caps.uid}/projects`).collection("items").doc(id); },
  assetCol() { return caps.db.doc(`data/users/${caps.uid}/assets`).collection("items"); },
  async list() {
    if (this.mode === "db") {
      const snap = await caps.db.doc(`data/users/${caps.uid}/projects`).collection("items").orderBy("updated", "desc").limit(200).get();
      return snap.docs.map(d => ({ id: d.id, name: d.data().name, updated: d.data().updated }));
    }
    try { return JSON.parse(LS.get("bk:list") || "[]"); } catch { return []; }
  },
  async load(id) {
    if (this.mode === "db") {
      const d = await this.projRef(id).get();
      if (!d.exists) return null;
      const p = JSON.parse(d.data().json);
      const as = await this.assetCol().where("pid", "==", id).get();
      as.docs.forEach(a => { const x = a.data(); if (p.assets[x.aid]) { p.assets[x.aid].data = x.data; this.savedAssets.add(id + "_" + x.aid); } });
      return p;
    }
    try { return JSON.parse(LS.get("bk:p:" + id)); } catch { return null; }
  },
  async save(p) {
    p.updated = Date.now();
    if (this.mode === "db") {
      for (const [aid, a] of Object.entries(p.assets)) {
        const key = p.id + "_" + aid;
        if (this.savedAssets.has(key)) continue;
        await this.assetCol().doc(key).set({ pid: p.id, aid, data: a.data });
        this.savedAssets.add(key);
      }
      const light = { ...p, assets: Object.fromEntries(Object.entries(p.assets).map(([k, a]) => [k, { ...a, data: "" }])) };
      await this.projRef(p.id).set({ name: p.name, updated: p.updated, json: JSON.stringify(light) });
      return "db";
    }
    const list = (await this.list()).filter(x => x.id !== p.id);
    list.unshift({ id: p.id, name: p.name, updated: p.updated });
    const ok = LS.set("bk:p:" + p.id, JSON.stringify(p)) && LS.set("bk:list", JSON.stringify(list));
    if (!ok) throw new Error("quota");
    return "local";
  },
  async remove(id) {
    if (this.mode === "db") {
      const as = await this.assetCol().where("pid", "==", id).get();
      for (const a of as.docs) await this.assetCol().doc(a.id).delete();
      await this.projRef(id).delete();
      return;
    }
    LS.del("bk:p:" + id);
    LS.set("bk:list", JSON.stringify((await this.list()).filter(x => x.id !== id)));
  },
};

let saveTimer = null, dirty = false;
function changed(opts = {}) {
  dirty = true;
  setSave("Ungespeichert", "");
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, 1200);
  if (opts.preview !== false) schedulePreview();
}
async function saveNow() {
  if (!dirty) return;
  dirty = false;
  setSave("Speichert …", "");
  try {
    const where = await store.save(P);
    setSave(where === "db" ? "Gespeichert" : "Gespeichert (dieser Browser)", "ok");
    renderProjList();
  } catch (e) {
    setSave(e.message === "quota" ? "Speicher voll – Projektdatei sichern" : "Nicht gespeichert", "err");
  }
}
function setSave(t, cls) { const el = $("#saveState"); el.textContent = t; el.className = "save-state " + cls; }

/* ---------------------------------------------------------- Vorschau */
let pvTimer = null;
function schedulePreview() { clearTimeout(pvTimer); pvTimer = setTimeout(renderPreview, 250); }
function renderPreview() {
  const pg0 = page();
  if (!pg0) return;
  const html = renderPage(P, pg0, "preview").replace("<script>", `<script>window.__y=${previewScroll[pg0.id] || 0};`);
  $("#pv").srcdoc = html;
}
window.addEventListener("message", e => {
  if (e.source !== $("#pv").contentWindow || !e.data || !e.data.bk) return;
  if (e.data.bk === "scroll") previewScroll[curPageId] = e.data.y;
  if (e.data.bk === "nav") {
    const slug = e.data.href.replace(/\.html.*$/, "");
    const target = P.pages.find(p => p.slug === slug);
    if (target) { selectPage(target.id); previewScroll[target.id] = 0; }
  }
  if (e.data.bk === "ext") toast("Externer Link: " + e.data.href);
});

/* ---------------------------------------------------------- Oberfläche: allgemein */
function toast(msg) {
  const t = $("#toast"); t.textContent = msg; t.hidden = false;
  clearTimeout(toast.t); toast.t = setTimeout(() => t.hidden = true, 3200);
}
$$(".tabs button").forEach(b => b.addEventListener("click", () => {
  $$(".tabs button").forEach(x => x.setAttribute("aria-selected", x === b));
  $$(".panel").forEach(p => p.hidden = p.dataset.panel !== b.dataset.tab);
  try { localStorage.setItem("bk:tab", b.dataset.tab); } catch { /* egal */ }
}));
$$(".devices button").forEach(b => b.addEventListener("click", () => {
  device = b.dataset.dev;
  $$(".devices button").forEach(x => x.setAttribute("aria-pressed", x === b));
  $("#frameWrap").dataset.dev = device;
}));
$$(".mode-switch button").forEach(b => b.addEventListener("click", () => {
  $$(".mode-switch button").forEach(x => x.setAttribute("aria-pressed", x === b));
  $(".main").dataset.view = b.dataset.mode;
}));
$("#pageSelect").addEventListener("change", e => selectPage(e.target.value));
$("#projName").addEventListener("input", e => { P.name = e.target.value; changed({ preview: false }); });

function renderAll() {
  $("#projName").value = P.name;
  renderSiteFields(); renderBrand(); renderPages(); renderEditor(); renderAutoSelects(); renderProjList();
  renderPreview();
}

/* ---------------------------------------------------------- Projekt-Tab */
async function renderProjList() {
  let list = [];
  try { list = await store.list(); } catch { /* offline */ }
  if (!list.find(x => x.id === P.id)) list.unshift({ id: P.id, name: P.name + " (nicht gespeichert)", updated: P.updated });
  const fmt = t => t ? new Date(t).toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit" }) : "";
  $("#projList").innerHTML = list.map(x => `<li class="${x.id === P.id ? "cur" : ""}" data-id="${esc(x.id)}">
    <button type="button" class="nm" data-act="open">${esc(x.name || "Ohne Namen")}</button><small>${fmt(x.updated)}</small>
    <button type="button" class="iconbtn" data-act="dup" title="Duplizieren">Kopie</button>
    <button type="button" class="iconbtn del" data-act="del" title="Löschen">Löschen</button></li>`).join("");
  $("#storeHint").textContent = store.mode === "db"
    ? "Projekte werden in deinem Claude-Konto gespeichert und sind nur für dich sichtbar."
    : "Projekte werden in diesem Browser gespeichert. Sichere wichtige Projekte zusätzlich als Projektdatei.";
}
$("#projList").addEventListener("click", async e => {
  const b = e.target.closest("button"); if (!b) return;
  const li = b.closest("li"), id = li.dataset.id, act = b.dataset.act;
  if (act === "open" && id !== P.id) { await saveNow(); const p = await store.load(id); if (p) openProject(p); }
  if (act === "dup") { await saveNow(); const src = id === P.id ? P : await store.load(id); if (!src) return; const c = clone(src); c.id = uid(); c.name = src.name + " (Kopie)"; openProject(c); changed(); toast("Kopie angelegt"); }
  if (act === "del") {
    li.innerHTML = `<span class="ask">„${esc(li.querySelector(".nm").textContent)}“ löschen?</span><button type="button" class="btn small danger" data-act="del-yes">Löschen</button><button type="button" class="btn small ghost" data-act="del-no">Behalten</button>`;
  }
  if (act === "del-no") renderProjList();
  if (act === "del-yes") {
    await store.remove(id);
    if (id === P.id) { const rest = await store.list(); const next = rest[0] ? await store.load(rest[0].id) : templateProject("verein", "Neues Projekt"); openProject(next); }
    renderProjList(); toast("Projekt gelöscht");
  }
});
$("#createProj").addEventListener("click", async () => {
  await saveNow();
  const p = templateProject($("#newType").value, $("#newName").value.trim(), $("#newDesc").value.trim());
  p.brand = defaultBrand();
  openProject(p); changed(); toast("Projekt angelegt");
  $("#aiPrompt").value = $("#newDesc").value;
});
function defaultBrand() { return { logo: "", colors: { primary: "#1F5BD8", accent: "#E8833A", dark: "#14213D" }, font: "modern", hero: "dark", radius: "10", bg: "tint", showName: true }; }

function renderSiteFields() { $$("[data-site]").forEach(i => i.value = P.site[i.dataset.site] || ""); }
$$("[data-site]").forEach(i => i.addEventListener("input", () => { P.site[i.dataset.site] = i.value; changed(); }));

$("#exportJson").addEventListener("click", () => saveFile(slugify(P.name) + ".baukasten.json", new Blob([JSON.stringify(P)], { type: "application/json" })));
$("#importJson").addEventListener("change", async e => {
  const f = e.target.files[0]; e.target.value = "";
  if (!f) return;
  try {
    const p = JSON.parse(await f.text());
    if (!p.pages || !p.site || !p.brand) throw new Error();
    await saveNow(); p.id = uid(); p.assets = p.assets || {}; openProject(p); changed(); toast("Projekt geladen");
  } catch { toast("Die Datei ist keine Baukasten-Projektdatei."); }
});

/* ---------------------------------------------------------- Logo & Stil */
$("#fontSel").innerHTML = Object.entries(FONTS).map(([k, f]) => `<option value="${k}">${esc(f.label)}</option>`).join("");
function renderBrand() {
  const B = P.brand, logo = resolveImg(P, B.logo, "preview");
  $("#logoPreview").hidden = !logo; $("#logoEmpty").hidden = !!logo;
  if (logo) $("#logoPreview").src = logo;
  $("#cPrimary").value = B.colors.primary; $("#cAccent").value = B.colors.accent; $("#cDark").value = B.colors.dark;
  $$("[data-brand]").forEach(i => { if (i.type === "checkbox") i.checked = !!B[i.dataset.brand]; else i.value = B[i.dataset.brand]; });
  $("#logoAI").hidden = !(caps.sample && caps.images && logo);
  renderSwatches(); renderContrast();
}
function renderContrast() {
  const c = P.brand.colors, t = themeVars(P.brand), notes = [];
  if (contrast(c.primary, t["--bg"]) < 4.5) notes.push("Die Hauptfarbe ist auf dem Hintergrund schwer lesbar – wähle sie dunkler.");
  if (contrast(c.accent, t["--on-accent"]) < 3) notes.push("Buttons in der Akzentfarbe haben wenig Kontrast.");
  const el = $("#contrastNote");
  el.textContent = notes.join(" ") || "Kontrast ist in Ordnung.";
  el.className = "contrast" + (notes.length ? " warn" : "");
}
let logoSwatches = [];
function renderSwatches() {
  $("#logoSwatches").innerHTML = logoSwatches.length ? `<span class="hint" style="width:100%">Farben im Logo – zum Übernehmen auf ein Farbfeld ziehen oder unten antippen:</span>` + logoSwatches.map(c => `<span class="sw" draggable="true" data-hex="${c}" style="background:${c}" title="${c}"></span>`).join("") : "";
  $$(".color").forEach(row => {
    let pick = row.querySelector(".pick");
    if (!pick) { pick = document.createElement("div"); pick.className = "pick"; row.append(pick); }
    const role = row.querySelector("input").dataset.color;
    pick.innerHTML = logoSwatches.map(c => `<button type="button" style="background:${c}" data-role="${role}" data-hex="${c}" aria-label="${c} als ${role}"></button>`).join("");
  });
}
$(".colors").addEventListener("click", e => { const b = e.target.closest("[data-role]"); if (!b) return; P.brand.colors[b.dataset.role] = b.dataset.hex; renderBrand(); changed(); });
$("#logoSwatches").addEventListener("dragstart", e => e.dataTransfer.setData("text/plain", e.target.dataset.hex || ""));
$$(".color input").forEach(i => {
  i.addEventListener("input", () => { P.brand.colors[i.dataset.color] = i.value.toUpperCase(); renderContrast(); changed(); });
  i.addEventListener("dragover", e => e.preventDefault());
  i.addEventListener("drop", e => { e.preventDefault(); const h = e.dataTransfer.getData("text/plain"); if (/^#[0-9A-F]{6}$/i.test(h)) { P.brand.colors[i.dataset.color] = h; renderBrand(); changed(); } });
});
$$("[data-brand]").forEach(i => i.addEventListener("change", () => { P.brand[i.dataset.brand] = i.type === "checkbox" ? i.checked : i.value; renderContrast(); changed(); }));

const logoDrop = $("#logoDrop");
logoDrop.addEventListener("click", () => $("#logoFile").click());
logoDrop.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); $("#logoFile").click(); } });
logoDrop.addEventListener("dragover", e => { e.preventDefault(); logoDrop.classList.add("over"); });
logoDrop.addEventListener("dragleave", () => logoDrop.classList.remove("over"));
logoDrop.addEventListener("drop", e => { e.preventDefault(); logoDrop.classList.remove("over"); const f = e.dataTransfer.files[0]; if (f) setLogo(f); });
$("#logoFile").addEventListener("change", e => { const f = e.target.files[0]; e.target.value = ""; if (f) setLogo(f); });
$("#logoRemove").addEventListener("click", () => { P.brand.logo = ""; logoSwatches = []; renderBrand(); changed(); });
$("#logoColors").addEventListener("click", async () => {
  const src = resolveImg(P, P.brand.logo, "preview");
  if (!src) { toast("Lade zuerst ein Logo hoch."); return; }
  applyLogoPalette(await loadImg(src)); toast("Farben aus dem Logo übernommen");
});

async function setLogo(file) {
  if (!file.type.startsWith("image/")) { toast("Bitte eine Bilddatei wählen."); return; }
  const data = await fileToData(file, 800, file.type === "image/svg+xml" ? "keep" : "image/png");
  const id = addAsset(file.name || "logo.png", data);
  P.brand.logo = "asset:" + id;
  applyLogoPalette(await loadImg(data));
  toast("Logo übernommen, Farben angepasst");
}
function applyLogoPalette(img) {
  const cols = logoColors(img);
  logoSwatches = cols.filter(c => c.l < .96).map(c => c.hex).slice(0, 8);
  P.brand.colors = paletteFromLogo(cols);
  renderBrand(); changed();
}
function loadImg(src) { return new Promise((ok, bad) => { const i = new Image(); i.onload = () => ok(i); i.onerror = bad; i.src = src; }); }

$("#logoAI").addEventListener("click", async () => {
  const btn0 = $("#logoAI"); btn0.disabled = true; $("#logoHint").textContent = "Claude sieht sich das Logo an …";
  try {
    const src = resolveImg(P, P.brand.logo, "preview");
    const blob = dataToBlob(src);
    const r = await caps.sample.json(`Analysiere dieses Logo für eine Website. Antworte nur mit JSON:
{"primary":"#RRGGBB (Hauptfarbe, auf Weiß gut lesbar)","accent":"#RRGGBB (Akzent für Buttons)","dark":"#RRGGBB (sehr dunkle Farbe für Kopf- und Fußbereich)","font":"einer von ${Object.keys(FONTS).join("|")}","hero":"dark|primary|light","radius":"2|10|22","mood":"ein Satz auf Deutsch, welche Wirkung das Logo hat und wie die Website wirken sollte"}
Nimm die Farben aus dem Logo. Wähle die Schrift passend zum Charakter der Logo-Schrift.`, { images: [blob], modelTier: "default" });
    const hex = v => /^#[0-9a-f]{6}$/i.test(v || "") ? v.toUpperCase() : null;
    const c = P.brand.colors;
    P.brand.colors = { primary: hex(r.primary) || c.primary, accent: hex(r.accent) || c.accent, dark: hex(r.dark) || c.dark };
    if (FONTS[r.font]) P.brand.font = r.font;
    if (["dark", "primary", "light"].includes(r.hero)) P.brand.hero = r.hero;
    if (["2", "10", "22"].includes(String(r.radius))) P.brand.radius = String(r.radius);
    $("#logoHint").textContent = r.mood ? "Claude: " + r.mood : "Stil aus dem Logo übernommen.";
    renderBrand(); changed();
  } catch (e) { $("#logoHint").textContent = aiError(e); }
  btn0.disabled = false;
});

/* ---------------------------------------------------------- Bilder */
function addAsset(name, data) {
  const id = uid(), m = data.match(/^data:image\/([a-z+]+)/), e0 = m ? (m[1] === "jpeg" ? "jpg" : m[1] === "svg+xml" ? "svg" : m[1]) : "png";
  P.assets[id] = { name, file: `${slugify(name.replace(/\.[a-z0-9]+$/i, ""))}-${id}.${e0}`, data };
  return id;
}
function fileToData(file, maxW, type) {
  return new Promise((ok, bad) => {
    const rd = new FileReader();
    rd.onerror = bad;
    rd.onload = async () => {
      if (type === "keep") return ok(rd.result);
      try {
        const img = await loadImg(rd.result);
        const k = Math.min(1, maxW / img.naturalWidth), c = document.createElement("canvas");
        c.width = Math.round(img.naturalWidth * k); c.height = Math.round(img.naturalHeight * k);
        c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
        ok(c.toDataURL(type || "image/jpeg", .84));
      } catch (e) { bad(e); }
    };
    rd.readAsDataURL(file);
  });
}
function dataToBlob(data) {
  const [h, b64] = data.split(","), mime = h.match(/data:([^;]+)/)[1];
  const bin = atob(b64), u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
  return new Blob([u], { type: mime });
}
let imgTarget = null;
$("#imgFile").addEventListener("change", async e => {
  const f = e.target.files[0]; e.target.value = "";
  if (!f || !imgTarget) return;
  const data = await fileToData(f, 1600, f.type === "image/png" ? "image/png" : "image/jpeg");
  const id = addAsset(f.name, data);
  setPath(imgTarget.sec, imgTarget.key, "asset:" + id);
  imgTarget = null; renderEditor(); changed();
});

/* ---------------------------------------------------------- Seiten-Tab */
function renderPages() {
  const P0 = P.pages;
  $("#pageList").innerHTML = P0.map((p, i) => `<li class="${p.id === curPageId ? "cur" : ""}" data-id="${p.id}">
    <button type="button" class="nm" data-act="sel">${esc(p.title)}</button>
    <span class="tagk${p.kind === "landing" ? " lp" : ""}">${p.kind === "landing" ? "Landing" : p.inNav ? "Menü" : "Seite"}</span>
    <button type="button" class="iconbtn" data-act="up" ${i === 0 ? "disabled" : ""} aria-label="Nach oben">↑</button>
    <button type="button" class="iconbtn" data-act="down" ${i === P0.length - 1 ? "disabled" : ""} aria-label="Nach unten">↓</button>
    <button type="button" class="iconbtn" data-act="dup" aria-label="Duplizieren">Kopie</button>
    <button type="button" class="iconbtn del" data-act="del" aria-label="Löschen">✕</button></li>`).join("");
  $("#pageSelect").innerHTML = P0.map(p => `<option value="${p.id}"${p.id === curPageId ? " selected" : ""}>${esc(p.title)}${p.kind === "landing" ? " (Landing)" : ""}</option>`).join("");
  $("#pageSlugs").innerHTML = P0.map(p => `<option value="${esc(p.slug)}">${esc(p.title)}</option>`).join("");
  const p = page();
  $("#pageSettings").innerHTML = `<h2>Seite „${esc(p.title)}“</h2>
    <div class="row2"><div class="field"><label for="pTitle">Titel</label><input id="pTitle" data-page="title" value="${esc(p.title)}"></div>
    <div class="field"><label for="pSlug">Dateiname</label><input id="pSlug" data-page="slug" class="mono" value="${esc(p.slug)}" ${p.slug === "index" ? "disabled" : ""}></div></div>
    <div class="row2"><div class="field"><label for="pKind">Art</label><select id="pKind" data-page="kind"><option value="page"${p.kind !== "landing" ? " selected" : ""}>Normale Seite</option><option value="landing"${p.kind === "landing" ? " selected" : ""}>Landingpage</option></select></div>
    <label class="check" style="align-self:end;padding-bottom:.4rem"><input type="checkbox" id="pNav" data-page="inNav"${p.inNav ? " checked" : ""}> Im Menü</label></div>
    <div class="field"><label for="pDesc">Beschreibung für Google</label><textarea id="pDesc" data-page="description" rows="2">${esc(p.description)}</textarea></div>`;
}
$("#pageList").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  const id = b.closest("li").dataset.id, i = P.pages.findIndex(p => p.id === id), act = b.dataset.act;
  if (act === "sel") return selectPage(id);
  if (act === "up" && i > 0) { [P.pages[i - 1], P.pages[i]] = [P.pages[i], P.pages[i - 1]]; }
  if (act === "down" && i < P.pages.length - 1) { [P.pages[i + 1], P.pages[i]] = [P.pages[i], P.pages[i + 1]]; }
  if (act === "dup") { const c = clone(P.pages[i]); c.id = uid(); c.title += " (Kopie)"; c.slug = uniqueSlug(c.slug === "index" ? "start" : c.slug); c.sections.forEach(s => s.id = uid()); P.pages.splice(i + 1, 0, c); curPageId = c.id; }
  if (act === "del") {
    if (P.pages.length === 1) { toast("Eine Seite muss bleiben."); return; }
    const li = b.closest("li");
    li.innerHTML = `<span class="ask">„${esc(P.pages[i].title)}“ löschen?</span><button type="button" class="btn small danger" data-act="del-yes">Löschen</button><button type="button" class="btn small ghost" data-act="del-no">Behalten</button>`;
    li.dataset.id = id; return;
  }
  if (act === "del-no") { renderPages(); return; }
  if (act === "del-yes") { P.pages.splice(i, 1); if (curPageId === id) curPageId = P.pages[0].id; ensureIndex(); }
  renderPages(); renderEditor(); renderAutoSelects(); changed();
});
$("#pageSettings").addEventListener("input", e => {
  const k = e.target.dataset.page; if (!k) return;
  const p = page();
  if (k === "inNav") p.inNav = e.target.checked;
  else if (k === "slug") { p.slug = slugify(e.target.value); }
  else p[k] = e.target.value;
  if (k === "title" || k === "kind" || k === "inNav") { $("#pageList").querySelector(`li[data-id="${p.id}"] .nm`).textContent = p.title; renderPagesLight(); }
  changed();
});
$("#pageSettings").addEventListener("change", e => { if (e.target.dataset.page === "slug") { const p = page(); p.slug = uniqueSlug(slugify(e.target.value), p.id); e.target.value = p.slug; renderPagesLight(); changed(); } if (e.target.dataset.page === "kind") renderPages(); });
function renderPagesLight() { $("#pageSelect").innerHTML = P.pages.map(p => `<option value="${p.id}"${p.id === curPageId ? " selected" : ""}>${esc(p.title)}</option>`).join(""); $("#pageSlugs").innerHTML = P.pages.map(p => `<option value="${esc(p.slug)}">${esc(p.title)}</option>`).join(""); }
function uniqueSlug(s, selfId) { let x = s, n = 2; while (P.pages.some(p => p.slug === x && p.id !== selfId) || (x === "index" && P.pages.some(p => p.slug === "index" && p.id !== selfId))) x = `${s}-${n++}`; return x; }
function ensureIndex() { if (!P.pages.some(p => p.slug === "index")) P.pages[0].slug = "index"; }
$("#addPage").addEventListener("click", () => {
  const t = $("#addPageName").value.trim(), tpl = $("#addPageTpl").value;
  const p = PAGE_TPL[tpl](t);
  p.slug = uniqueSlug(t ? slugify(t) : p.slug);
  P.pages.push(p); curPageId = p.id; $("#addPageName").value = "";
  renderPages(); renderEditor(); renderAutoSelects(); changed(); toast(`Seite „${p.title}“ hinzugefügt`);
});
function selectPage(id) { curPageId = id; renderPages(); renderEditor(); renderPreview(); }

/* ---------------------------------------------------------- Abschnitts-Editor */
$("#addSecType").innerHTML = Object.entries(SECTIONS).map(([k, v]) => `<option value="${k}">${esc(v.label)}</option>`).join("");
$("#addSec").addEventListener("click", () => {
  const s = defaultSection($("#addSecType").value);
  page().sections.push(s); openSecs.add(s.id); renderEditor(); changed();
});
const openSecs = new Set();
function getPath(o, path) { return path.split(".").reduce((a, k) => a == null ? a : a[k], o); }
function setPath(o, path, v) { const ks = path.split("."), last = ks.pop(); const t = ks.reduce((a, k) => a[k], o); t[last] = v; }
function fieldHtml(sIdx, key, f, val) {
  const [, label, t = "text", extra] = f, id = `f-${sIdx}-${key.replace(/\./g, "-")}`;
  const attrs = `id="${id}" data-sec="${sIdx}" data-k="${key}"`;
  if (t === "area") return `<div class="field"><label for="${id}">${esc(label)}</label><textarea ${attrs} rows="3">${esc(val)}</textarea></div>`;
  if (t === "bool") return `<label class="check"><input type="checkbox" ${attrs}${val ? " checked" : ""}> ${esc(label)}</label>`;
  if (t === "select") return `<div class="field"><label for="${id}">${esc(label)}</label><select ${attrs}>${extra.map(o => `<option${o === val ? " selected" : ""}>${o}</option>`).join("")}</select></div>`;
  if (t === "link") return `<div class="field"><label for="${id}">${esc(label)}</label><input ${attrs} list="pageSlugs" value="${esc(val)}" placeholder="Seite, #anker oder https://"></div>`;
  if (t === "img") {
    const src = resolveImg(P, val, "preview");
    const opts = Object.entries(P.assets).map(([aid, a]) => `<option value="asset:${aid}"${val === "asset:" + aid ? " selected" : ""}>${esc(a.name)}</option>`).join("");
    return `<div class="field"><span class="lbl">${esc(label)}</span><div class="imgpick">${src ? `<img class="th" src="${esc(src)}" alt="">` : `<span class="th"></span>`}
      <select ${attrs} aria-label="${esc(label)} auswählen"><option value="">Kein Bild</option>${opts}</select>
      <button type="button" class="btn small" data-act="upload" data-sec="${sIdx}" data-k="${key}">Hochladen</button></div></div>`;
  }
  if (t === "list") {
    const items = val || [];
    return `<div class="field"><span class="lbl">${esc(label)}</span><div class="list-items">${items.map((it, j) => `<div class="item"><div class="item-head"><span>${j + 1}</span><span>
      <button type="button" class="iconbtn" data-act="item-up" data-sec="${sIdx}" data-k="${key}" data-j="${j}" aria-label="Nach oben" ${j === 0 ? "disabled" : ""}>↑</button>
      <button type="button" class="iconbtn del" data-act="item-del" data-sec="${sIdx}" data-k="${key}" data-j="${j}" aria-label="Entfernen">✕</button></span></div>
      ${extra.map(g => fieldHtml(sIdx, `${key}.${j}.${g[0]}`, g, it[g[0]] ?? "")).join("")}</div>`).join("")}</div>
      <button type="button" class="btn small" data-act="item-add" data-sec="${sIdx}" data-k="${key}">+ Eintrag</button></div>`;
  }
  return `<div class="field"><label for="${id}">${esc(label)}</label><input ${attrs} value="${esc(val)}"></div>`;
}
function renderEditor() {
  const p = page(), box = $("#sections");
  box.innerHTML = p.sections.map((s, i) => {
    const def = SECTIONS[s.type] || { label: s.type, fields: [] };
    const sub = s.title || s.eyebrow || "";
    return `<details class="sec" data-id="${s.id}"${openSecs.has(s.id) ? " open" : ""}><summary><span class="t">${esc(def.label)}<small>${esc(sub)}</small></span>
      <button type="button" class="iconbtn" data-act="up" data-sec="${i}" aria-label="Nach oben" ${i === 0 ? "disabled" : ""}>↑</button>
      <button type="button" class="iconbtn" data-act="down" data-sec="${i}" aria-label="Nach unten" ${i === p.sections.length - 1 ? "disabled" : ""}>↓</button>
      <button type="button" class="iconbtn" data-act="dup" data-sec="${i}" aria-label="Duplizieren">Kopie</button>
      <button type="button" class="iconbtn del" data-act="del" data-sec="${i}" aria-label="Löschen">✕</button></summary>
      <div class="sec-body">${def.fields.map(f => fieldHtml(i, f[0], f, s[f[0]] ?? (f[2] === "list" ? [] : ""))).join("")}
      <div class="field"><label for="anc-${i}">Anker (für Links wie #anmelden)</label><input id="anc-${i}" data-sec="${i}" data-k="anchor" class="mono" value="${esc(s.anchor || "")}"></div>
      ${caps.sample ? `<div class="ai-sec"><label class="sr" for="ai-${s.id}">Anweisung an Claude</label><input id="ai-${s.id}" placeholder="z. B. kürzer, herzlicher, auf Englisch" data-ai="${i}"><button type="button" class="btn small" data-act="ai" data-sec="${i}">Mit Claude umschreiben</button></div>` : ""}
      </div></details>`;
  }).join("") || `<p class="hint">Diese Seite hat noch keine Abschnitte.</p>`;
}
const secBox = $("#sections");
secBox.addEventListener("toggle", e => { const d = e.target; if (d.matches?.("details.sec")) d.open ? openSecs.add(d.dataset.id) : openSecs.delete(d.dataset.id); }, true);
secBox.addEventListener("input", e => {
  const el = e.target; if (el.dataset.sec == null || !el.dataset.k) return;
  const s = page().sections[+el.dataset.sec];
  setPath(s, el.dataset.k, el.type === "checkbox" ? el.checked : el.value);
  if (el.tagName === "SELECT" && el.closest(".imgpick")) renderEditor();
  changed();
});
secBox.addEventListener("click", async e => {
  const b = e.target.closest("button[data-act]"); if (!b) return;
  e.preventDefault();
  const secs = page().sections, i = +b.dataset.sec, s = secs[i], act = b.dataset.act;
  if (act === "up" && i > 0) [secs[i - 1], secs[i]] = [secs[i], secs[i - 1]];
  else if (act === "down" && i < secs.length - 1) [secs[i + 1], secs[i]] = [secs[i], secs[i + 1]];
  else if (act === "dup") { const c = clone(s); c.id = uid(); secs.splice(i + 1, 0, c); }
  else if (act === "del") { secs.splice(i, 1); }
  else if (act === "upload") { imgTarget = { sec: s, key: b.dataset.k }; $("#imgFile").click(); return; }
  else if (act === "item-add") {
    const list = getPath(s, b.dataset.k) || []; const def = SECTIONS[s.type].fields.find(f => f[0] === b.dataset.k)[3];
    list.push(Object.fromEntries(def.map(g => [g[0], g[2] === "select" ? g[3][0] : ""]))); setPath(s, b.dataset.k, list);
  }
  else if (act === "item-del") getPath(s, b.dataset.k).splice(+b.dataset.j, 1);
  else if (act === "item-up") { const l = getPath(s, b.dataset.k), j = +b.dataset.j; [l[j - 1], l[j]] = [l[j], l[j - 1]]; }
  else if (act === "ai") return rewriteSection(i, b);
  renderEditor(); changed();
});

/* ---------------------------------------------------------- KI */
function aiError(e) {
  const c = e && e.code;
  if (c === "not_granted") return "Claude wurde für diese Seite nicht freigegeben.";
  if (c === "rate_limited") return "Gerade zu viele Anfragen. Bitte kurz warten und erneut versuchen.";
  if (c === "cancelled") return "Abgebrochen.";
  if (c === "images_unavailable") return "Bilder können hier nicht an Claude gesendet werden.";
  if (e instanceof SyntaxError || c === "invalid_json") return "Claude hat kein gültiges Ergebnis geliefert. Bitte noch einmal versuchen.";
  return "Das hat nicht geklappt" + (e && e.message ? ": " + e.message : ".");
}
const SCHEMA_TEXT = `Abschnittstypen und ihre Felder (Listen in eckigen Klammern):\n${AI_FIELDS}\nFür projects.items.status nur "laufend" oder "abgeschlossen". filter ist true/false. Links (link, link1, link2, ctaLink) sind ein slug einer anderen Seite, ein #anker oder eine https-URL.`;
const RULES = `Regeln:
- Schreibe auf Deutsch, konkret und lebendig, kurze Sätze, keine Floskeln.
- Erfinde keine Fakten: keine Adressen, Telefonnummern, Preise, Namen, Zahlen oder Daten. Wo so etwas fehlt, schreibe einen Platzhalter in eckigen Klammern, z. B. [Adresse].
- Keine Bildfelder ausfüllen.
- Antworte nur mit JSON, ohne Erklärung.`;
function siteBrief() {
  const S = P.site;
  return `Name: ${S.name}\nUntertitel: ${S.tagline || "-"}\nE-Mail: ${S.email || "-"}\nTelefon: ${S.phone || "-"}\nAdresse: ${S.address || "-"}`;
}
function normSection(s) {
  if (!s || !SECTIONS[s.type]) return null;
  const out = { id: uid(), type: s.type };
  for (const f of SECTIONS[s.type].fields) {
    const v = s[f[0]], t = f[2];
    if (t === "list") out[f[0]] = Array.isArray(v) ? v.slice(0, 24).map(it => Object.fromEntries(f[3].map(g => [g[0], g[2] === "select" ? (g[3].includes(it?.[g[0]]) ? it[g[0]] : g[3][0]) : g[2] === "img" ? "" : String(it?.[g[0]] ?? "")]))) : [];
    else if (t === "bool") out[f[0]] = !!v;
    else if (t === "img") out[f[0]] = "";
    else out[f[0]] = String(v ?? "");
  }
  if (s.anchor) out.anchor = slugify(s.anchor);
  return out;
}
function normPage(p, fallbackKind) {
  const sections = (p.sections || []).map(normSection).filter(Boolean);
  return { id: uid(), title: String(p.title || "Seite"), slug: slugify(p.slug || p.title), kind: p.kind === "landing" || fallbackKind === "landing" ? "landing" : "page", inNav: fallbackKind === "landing" ? false : p.inNav !== false, description: String(p.description || "").slice(0, 300), sections: sections.length ? sections : [defaultSection("text")] };
}

let aiCtl = null;
$("#aiStop").addEventListener("click", () => aiCtl?.abort());
$("#aiRun").addEventListener("click", () => {
  if (!$("#aiPrompt").value.trim()) { setAi("Bitte beschreibe zuerst die Website.", "err"); return; }
  if ($("#aiMode").value === "site") { $("#aiConfirm").hidden = false; return; }
  runAI();
});
$("#aiConfirmNo").addEventListener("click", () => $("#aiConfirm").hidden = true);
$("#aiConfirmYes").addEventListener("click", () => { $("#aiConfirm").hidden = true; runAI(); });
function setAi(t, cls = "") { const el = $("#aiStatus"); el.textContent = t; el.className = "ai-status " + cls; }

async function runAI() {
  const mode = $("#aiMode").value, desc = $("#aiPrompt").value.trim();
  const existing = P.pages.map(p => `${p.slug} (${p.title})`).join(", ");
  const prompt = mode === "site"
    ? `Erstelle eine vollständige Website mit mehreren Seiten.\n\nAngaben zur Website:\n${siteBrief()}\n\nBeschreibung vom Auftraggeber:\n${desc}\n\n${SCHEMA_TEXT}\n\n${RULES}\n- Die erste Seite hat slug "index" und beginnt mit einem hero.\n- Jede Seite 2 bis 6 Abschnitte, sinnvolle Reihenfolge, die Startseite endet mit cta.\n- Füge immer die Seiten "impressum" und "datenschutz" mit inNav false und je einem legal-Abschnitt hinzu (Platzhalter in eckigen Klammern).\n- Höchstens 7 Seiten im Menü.\n\nJSON-Format:\n{"tagline":"kurzer Untertitel","ctaLabel":"Text für den Button oben rechts oder leer","ctaLink":"slug","pages":[{"title":"","slug":"","kind":"page","inNav":true,"description":"Meta-Beschreibung, max. 155 Zeichen","sections":[{"type":"hero", ...Felder}]}]}`
    : `Erstelle eine neue ${mode === "landing" ? "Landingpage (eine Seite mit einem klaren Ziel, z. B. Anmeldung, Spende oder Anfrage; mit hero, Nutzen, Vertrauen, FAQ und einem Formular- oder CTA-Abschnitt)" : "Unterseite"} für diese Website.\n\nAngaben zur Website:\n${siteBrief()}\nVorhandene Seiten: ${existing}\n\nWunsch:\n${desc}\n\n${SCHEMA_TEXT}\n\n${RULES}\n\nJSON-Format:\n{"title":"","slug":"","description":"max. 155 Zeichen","sections":[{"type":"…", ...Felder}]}`;
  aiCtl = new AbortController();
  $("#aiRun").disabled = true; $("#aiStop").hidden = false;
  setAi("Claude denkt nach … (das kann eine Minute dauern)");
  try {
    let shown = 0;
    const r = await caps.sample.json(prompt, {
      signal: aiCtl.signal, modelTier: mode === "site" ? "complex" : "default",
      onText: ({ text }) => { if (text.length - shown > 300) { shown = text.length; setAi(`Claude schreibt … ${Math.round(text.length / 100) / 10}k Zeichen`); } },
    });
    if (mode === "site") {
      const pages = (r.pages || []).map(p => normPage(p)).filter(p => p.sections.length);
      if (!pages.length) throw new SyntaxError();
      const seen = new Set();
      pages.forEach((p, i) => { if (i === 0) p.slug = "index"; let s = p.slug, n = 2; while (seen.has(s)) s = `${p.slug}-${n++}`; p.slug = s; seen.add(s); if (["impressum", "datenschutz"].includes(p.slug)) p.inNav = false; });
      P.pages = pages; curPageId = pages[0].id;
      if (r.tagline && !P.site.tagline) P.site.tagline = String(r.tagline);
      if (typeof r.ctaLabel === "string") { P.site.ctaLabel = r.ctaLabel; P.site.ctaLink = String(r.ctaLink || ""); }
      setAi(`Fertig: ${pages.length} Seiten erstellt. Prüfe die Platzhalter in [eckigen Klammern].`, "ok");
    } else {
      const p = normPage(r, mode === "landing" ? "landing" : undefined);
      p.slug = uniqueSlug(p.slug);
      P.pages.push(p); curPageId = p.id;
      setAi(`Fertig: „${p.title}“ hinzugefügt.`, "ok");
    }
    renderAll(); changed();
  } catch (e) { setAi(aiError(e), "err"); }
  $("#aiRun").disabled = false; $("#aiStop").hidden = true; aiCtl = null;
}

async function rewriteSection(i, b) {
  const s = page().sections[i], input = $(`[data-ai="${i}"]`), wish = input.value.trim() || "Verbessere die Texte: klarer, lebendiger, kürzer.";
  b.disabled = true; b.textContent = "Claude schreibt …";
  try {
    const keep = Object.fromEntries(Object.entries(s).filter(([k]) => k !== "id"));
    const r = await caps.sample.json(`Überarbeite diesen Website-Abschnitt (Typ ${s.type}) für „${P.site.name}“.\nWunsch: ${wish}\n\nAktueller Abschnitt als JSON:\n${JSON.stringify(keep)}\n\n${RULES}\n- Gib den Abschnitt im selben JSON-Format zurück, mit denselben Feldern und dem Feld "type".`, { modelTier: "default" });
    const n = normSection({ ...r, type: s.type });
    if (!n) throw new SyntaxError();
    // Bilder und Anker behalten
    SECTIONS[s.type].fields.forEach(f => { if (f[2] === "img") n[f[0]] = s[f[0]]; if (f[2] === "list") (n[f[0]] || []).forEach((it, j) => f[3].forEach(g => { if (g[2] === "img") it[g[0]] = s[f[0]]?.[j]?.[g[0]] || ""; })); });
    n.id = s.id; if (s.anchor) n.anchor = s.anchor;
    page().sections[i] = n; openSecs.add(n.id);
    renderEditor(); changed(); toast("Abschnitt überarbeitet");
  } catch (e) { toast(aiError(e)); b.disabled = false; b.textContent = "Mit Claude umschreiben"; }
}

/* ---------------------------------------------------------- Automatisierung */
function renderAutoSelects() {
  const sel = $("#serTpl"), cur = sel.value;
  sel.innerHTML = P.pages.map(p => `<option value="${p.id}">${esc(p.title)}${p.kind === "landing" ? " (Landing)" : ""}</option>`).join("");
  if (P.pages.some(p => p.id === cur)) sel.value = cur; else { const lp = P.pages.find(p => p.kind === "landing"); if (lp) sel.value = lp.id; }
  $("#serAI").disabled = !caps.sample; $("#seoAI").hidden = !caps.sample;
  if (!caps.sample) $("#serAI").checked = false;
}
function parseRows(txt) {
  const ls = txt.split("\n").map(l => l.trim()).filter(Boolean);
  if (ls.length < 2) return null;
  const sep = ls[0].includes(";") ? ";" : ls[0].includes("\t") ? "\t" : ",";
  const cols = ls[0].split(sep).map(c => c.trim().toLowerCase());
  return { cols, rows: ls.slice(1).map(l => { const v = l.split(sep).map(x => x.trim()); return Object.fromEntries(cols.map((c, i) => [c, v[i] || ""])); }) };
}
const fill = (str, row) => String(str).replace(/\{\{\s*([\wäöüß-]+)\s*\}\}/gi, (m, k) => row[k.toLowerCase()] ?? m);
function fillDeep(o, row) { if (typeof o === "string") return fill(o, row); if (Array.isArray(o)) return o.map(x => fillDeep(x, row)); if (o && typeof o === "object") return Object.fromEntries(Object.entries(o).map(([k, v]) => [k, k === "id" || k === "image" ? v : fillDeep(v, row)])); return o; }
let serCtl = null;
$("#serStop").addEventListener("click", () => { serCtl?.abort(); });
$("#serRun").addEventListener("click", async () => {
  const data = parseRows($("#serData").value), tpl = P.pages.find(p => p.id === $("#serTpl").value), st = $("#serStatus");
  if (!data) { st.textContent = "Bitte mindestens eine Kopfzeile und eine Datenzeile eingeben."; st.className = "ai-status err"; return; }
  const withAI = $("#serAI").checked && caps.sample;
  serCtl = new AbortController();
  $("#serRun").disabled = true; $("#serStop").hidden = !withAI;
  let made = 0;
  for (const row of data.rows) {
    if (serCtl.signal.aborted) break;
    const p = clone(tpl);
    p.id = uid(); p.kind = "landing"; p.inNav = $("#serNav").checked;
    p.title = fill($("#serTitle").value, row); p.slug = uniqueSlug(slugify(fill($("#serSlug").value, row)));
    p.sections = fillDeep(p.sections, row).map(s => ({ ...s, id: uid() }));
    if (p.description) p.description = fill(p.description, row);
    if (withAI) {
      st.textContent = `Claude passt „${p.title}“ an … (${made + 1}/${data.rows.length})`; st.className = "ai-status";
      try {
        const r = await caps.sample.json(`Passe diese Landingpage für die Variante ${JSON.stringify(row)} an. Website: „${P.site.name}“. Schreibe die Texte so um, dass sie für genau diese Variante überzeugend und einzigartig sind (nicht nur Wörter austauschen).\n\nSeite als JSON:\n${JSON.stringify({ title: p.title, description: p.description, sections: p.sections.map(({ id, ...s }) => s) })}\n\n${SCHEMA_TEXT}\n\n${RULES}\n- Gib dieselbe Struktur zurück: {"title","description","sections":[...]} mit denselben Abschnittstypen in derselben Reihenfolge.`, { signal: serCtl.signal, modelTier: "default" });
        const np = normPage({ ...r, slug: p.slug }, "landing");
        np.sections.forEach((s, j) => { const old = p.sections[j]; if (old && old.type === s.type) { SECTIONS[s.type].fields.forEach(f => { if (f[2] === "img") s[f[0]] = old[f[0]]; }); if (old.anchor) s.anchor = old.anchor; } });
        p.title = np.title || p.title; p.description = np.description; p.sections = np.sections;
      } catch (e) { if (e && e.code === "cancelled") break; st.textContent = aiError(e) + " Seite wurde ohne KI-Anpassung angelegt."; }
    }
    P.pages.push(p); made++;
  }
  renderPages(); renderAutoSelects(); changed();
  st.textContent = `${made} Landingpage${made === 1 ? "" : "s"} erzeugt. Du findest sie im Tab „Seiten“.`; st.className = "ai-status ok";
  $("#serRun").disabled = false; $("#serStop").hidden = true; serCtl = null;
});
$("#applyForms").addEventListener("click", () => {
  const url = $("#formEndpoint").value.trim();
  if (url && !/^https:\/\//.test(url)) { toast("Die Adresse muss mit https:// beginnen."); return; }
  let n = 0;
  P.pages.forEach(p => p.sections.forEach(s => { if (s.type === "contact" || s.type === "signup") { s.formAction = url; n++; } }));
  renderEditor(); changed(); toast(`${n} Formular${n === 1 ? "" : "e"} ${url ? "verbunden" : "getrennt"}`);
});
function textOf(p) { return p.sections.map(s => [s.title, s.text, s.intro, ...(s.items || []).map(i => i.text || i.a || "")].filter(Boolean).join(" ")).join(" ").replace(/\s+/g, " ").trim(); }
$("#seoLocal").addEventListener("click", () => {
  let n = 0;
  P.pages.forEach(p => { if (!p.description) { const t = textOf(p); if (t) { p.description = t.length > 155 ? t.slice(0, 152).replace(/\s\S*$/, "") + " …" : t; n++; } } });
  renderPages(); changed(); $("#seoStatus").textContent = n ? `${n} Beschreibungen ergänzt.` : "Alle Seiten haben schon eine Beschreibung.";
});
$("#seoAI").addEventListener("click", async () => {
  const st = $("#seoStatus"); st.textContent = "Claude schreibt die Beschreibungen …"; st.className = "ai-status";
  try {
    const r = await caps.sample.json(`Schreibe für jede Seite der Website „${P.site.name}“ eine Meta-Beschreibung für Google (Deutsch, 120–155 Zeichen, konkret, mit Nutzen, keine erfundenen Fakten).\nSeiten:\n${P.pages.map(p => `${p.slug}: ${p.title} – ${textOf(p).slice(0, 600)}`).join("\n")}\n\nAntworte nur mit JSON: {"slug":"Beschreibung", ...}`, { modelTier: "quick" });
    let n = 0; P.pages.forEach(p => { if (typeof r[p.slug] === "string") { p.description = r[p.slug].slice(0, 170); n++; } });
    renderPages(); changed(); st.textContent = `${n} Beschreibungen geschrieben.`; st.className = "ai-status ok";
  } catch (e) { st.textContent = aiError(e); st.className = "ai-status err"; }
});

/* ---------------------------------------------------------- Export */
async function saveFile(name, blob) {
  if (caps.downloads) {
    try { await caps.downloads.save({ filename: name, data: blob }); toast("Gespeichert: " + name); }
    catch (e) { if (e.code !== "declined") toast("Speichern ging nicht: " + (e.message || e.code)); }
    return;
  }
  if (window.claude) { toast("Dateien speichern ist in dieser Ansicht nicht möglich."); return; }
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}
$("#exportZip").addEventListener("click", async () => {
  if (!window.JSZip) { toast("Der ZIP-Baustein konnte nicht geladen werden."); return; }
  const z = new JSZip(), vars = Object.entries(themeVars(P.brand)).map(([k, v]) => `${k}:${v}`).join(";");
  P.pages.forEach(p => z.file((p.slug === "index" ? "index" : p.slug) + ".html", renderPage(P, p, "export")));
  z.file("assets/style.css", `:root{${vars}}\n${SITE_CSS}`);
  z.file("assets/site.js", SITE_JS);
  Object.values(P.assets).forEach(a => { if (a.data) z.file("assets/img/" + a.file, dataToBlob(a.data)); });
  const dom = (P.site.domain || "").replace(/\/$/, "");
  if (dom) {
    z.file("sitemap.xml", `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${P.pages.map(p => `  <url><loc>${esc(dom)}/${p.slug === "index" ? "" : p.slug + ".html"}</loc></url>`).join("\n")}\n</urlset>\n`);
    z.file("robots.txt", `User-agent: *\nAllow: /\nSitemap: ${dom}/sitemap.xml\n`);
  } else z.file("robots.txt", "User-agent: *\nAllow: /\n");
  z.file("LIESMICH.txt", `${P.site.name} – erstellt mit dem Website-Baukasten\n\nVeröffentlichen:\n1. Alle Dateien dieses Ordners auf den Webspace laden (oder in ein GitHub-Repository und GitHub Pages aktivieren).\n2. index.html ist die Startseite.\n\nVor dem Start prüfen:\n- Platzhalter in [eckigen Klammern] ersetzen\n- Impressum und Datenschutz vervollständigen\n- Formulare verbinden (Baukasten → Automatisierung → Formulare verbinden)\n\nDas Projekt lässt sich mit baukasten-projekt.json wieder in den Baukasten laden.\n`);
  z.file("baukasten-projekt.json", JSON.stringify(P));
  const blob = await z.generateAsync({ type: "blob" });
  saveFile(slugify(P.site.name || P.name) + "-website.zip", blob);
});

/* ---------------------------------------------------------- Start */
function openProject(p) {
  P = p;
  P.assets = P.assets || {};
  P.site = { name: "", tagline: "", email: "", phone: "", address: "", ctaLabel: "", ctaLink: "", facebook: "", instagram: "", domain: "", notice: "", ...P.site };
  P.brand = { ...defaultBrand(), ...P.brand, colors: { ...defaultBrand().colors, ...(P.brand || {}).colors } };
  ensureIndex();
  curPageId = P.pages[0].id; previewScroll = {}; logoSwatches = []; dirty = false;
  try { localStorage.setItem("bk:last", P.id); } catch { /* egal */ }
  renderAll();
  setSave(store.mode === "db" ? "Gespeichert" : "Bereit", "");
  const src = resolveImg(P, P.brand.logo, "preview");
  if (src) loadImg(src).then(img => { logoSwatches = logoColors(img).filter(c => c.l < .96).map(c => c.hex).slice(0, 8); renderSwatches(); }).catch(() => {});
}
function seedProject() { const s = clone(SEED || templateProject("verein", "Mein Verein")); s.id = uid(); return s; }

async function boot() {
  // 1) sofort etwas zeigen: zuletzt geöffnetes Projekt aus dem Browser oder das Beispiel
  const last = LS.get("bk:last");
  let p = last ? await store.load(last) : null;
  openProject(p || seedProject());
  try { const tab = localStorage.getItem("bk:tab"); if (tab) $(`.tabs [data-tab="${tab}"]`)?.click(); } catch { /* egal */ }
  // 2) Fähigkeiten nachladen
  const [sample, downloads, db, user] = await Promise.all([use("sample"), use("downloads"), use("db"), use("user")]);
  caps.sample = sample; caps.downloads = downloads;
  if (sample) { try { caps.images = !!(await sample.limits())?.images; } catch { caps.images = false; } }
  $("#aiOff").hidden = !!sample; $("#aiRun").disabled = !sample;
  if (db && user) {
    try {
      caps.uid = await user.id();
      if (caps.uid) {
        caps.db = db; store.mode = "db";
        const list = await store.list();
        const lastDb = list.find(x => x.id === last) || list[0];
        if (lastDb && (!p || p.id !== lastDb.id) && !dirty) { const dp = await store.load(lastDb.id); if (dp) openProject(dp); }
        else if (p && !dirty) { dirty = true; saveNow(); }
      }
    } catch { store.mode = "local"; caps.db = null; }
  }
  renderBrand(); renderEditor(); renderAutoSelects(); renderProjList();
}
boot();
