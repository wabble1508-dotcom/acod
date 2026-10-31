// ACoD e.V. – gemeinsames Skript für alle Seiten
const eur = n => n.toLocaleString("de-DE") + " €";

// Mobiles Menü
const nav = document.getElementById("nav"), toggle = document.getElementById("menuToggle");
toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", open);
});

// Projektfilter (projekte.html): #laufend, #abgeschlossen oder alle
const filterButtons = document.querySelectorAll("[data-filter]");
if (filterButtons.length) {
  const cards = document.querySelectorAll("[data-status]");
  const setFilter = f => {
    filterButtons.forEach(b => b.setAttribute("aria-pressed", b.dataset.filter === f));
    cards.forEach(c => c.hidden = f !== "alle" && c.dataset.status !== f);
  };
  filterButtons.forEach(b => b.addEventListener("click", () => setFilter(b.dataset.filter)));
  const fromHash = () => setFilter(["laufend", "abgeschlossen"].includes(location.hash.slice(1)) ? location.hash.slice(1) : "alle");
  window.addEventListener("hashchange", fromHash);
  fromHash();
}

// Spendenformular
const donate = document.getElementById("donateForm");
if (donate) {
  const custom = document.getElementById("custom");
  const impactText = { 25: "eine Woche Hausaufgabenhilfe für ein Kind", 50: "Material für einen Bewerbungsworkshop", 120: "einen Begegnungsabend für 40 Gäste", 250: "einen Monat Lotsenarbeit für zwei Familien" };
  const amount = () => Number(custom.value) || Number(donate.querySelector("[name=amount]:checked")?.value || 0);
  const update = () => {
    const a = amount(), r = donate.querySelector("[name=rhythm]:checked").value;
    const key = [250, 120, 50, 25].find(k => a >= k);
    document.getElementById("impact").innerHTML = a ? `<b>${eur(a)} ${r}</b>${key ? ` · ermöglicht z. B. ${impactText[key]}` : ""}` : "Bitte einen Betrag wählen.";
  };
  donate.addEventListener("change", e => { if (e.target.name === "amount") custom.value = ""; update(); });
  custom.addEventListener("input", () => { if (custom.value) donate.querySelectorAll("[name=amount]").forEach(i => i.checked = false); update(); });
  update();
  donate.addEventListener("submit", e => {
    e.preventDefault();
    const m = document.getElementById("donateMsg"); m.hidden = false;
    m.textContent = amount()
      ? `Vorschau: Hier wird der Zahlungsanbieter (z. B. PayPal, Stripe oder betterplace) eingebunden. Gewählt: ${eur(amount())}.`
      : "Bitte einen Betrag wählen.";
  });
}

// Kontakt- und Mitgliedsformular (noch ohne Versand)
document.querySelectorAll("form[data-demo]").forEach(f => f.addEventListener("submit", e => {
  e.preventDefault();
  const m = f.querySelector(".form-msg"); m.hidden = false;
  m.textContent = f.checkValidity()
    ? "Vorschau: Das Formular ist noch nicht mit einem Postfach verbunden. Bitte schreiben Sie vorerst per E-Mail."
    : "Bitte füllen Sie alle Pflichtfelder (*) aus.";
}));

// Kopieren-Knöpfe
document.querySelectorAll("[data-copy]").forEach(b => b.addEventListener("click", () => {
  const el = document.getElementById(b.dataset.copy);
  const select = () => getSelection().selectAllChildren(el);
  if (!navigator.clipboard) return select();
  navigator.clipboard.writeText(el.textContent).then(() => b.textContent = "Kopiert", select);
}));
