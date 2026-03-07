# Tango in Tübingen

Community-Website für die Tübinger Tango-Szene: Milonga-Kalender, Lehrer:innen und Community-Angebote auf einen Blick.

**Live:** [tangotübingen.de](https://tangotübingen.de/)

## Philosophie

- **Schnell & einfach** — Kein Bloat, kein Framework. Statisches HTML, CSS und Vanilla JS. Beim Aufruf der Seite sind direkt die nächsten Veranstaltungen sichtbar.
- **Privacy first** — Keine Cookies, keine Werbung, keine personenbezogenen Daten. Nur miniamle Analytics über [GoatCounter](https://www.goatcounter.com/) (Open Source, DSGVO-konform).
- **Accessibility** — Semantisches HTML, Skip-Links, ARIA-Labels, Screenreader-optimiert.

## Aufbau

- `index.html` — Hauptseite mit Milonga-Kalender, Lehrer:innen und Community
- `data/milongas.json` — Veranstaltungsdaten im JSON-Format
- `data/teachers.json` — Lehrer:innen-Daten
- `js/` — Kalender-Logik und Lehrer:innen-Liste
- `css/style.css` — Styling mit selbst gehosteten Schriften 

## Du willst das auch für deine Stadt?

Diese Seite ist Open Source (GPL-3.0). Wenn du für deine Stadt oder Community eine ähnliche Seite aufbauen willst und Fragen hast, melde dich gerne: **tango@christianleroy.de**

## Lizenz

[GPL-3.0](LICENSE)
