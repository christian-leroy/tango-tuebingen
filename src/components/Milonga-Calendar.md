# Milonga-Calendar – Migration zu Astro

Notizen zum Umbau von client-seitigem Rendering (`public/js/milonga-cal.js`)
auf Build-Zeit-Rendering im Astro-Frontmatter.

## Grundidee

Frontmatter (zwischen den `---`) läuft beim **Build** auf dem Server.
JSON wird per Import geladen, nicht per `fetch`:

```astro
---
import milongas from '../data/milongas.json';
---
```

Statt das DOM zur Laufzeit zu bauen, rendert das Frontmatter **alle** Milongas
ins Markup (`.map()`). Die überzähligen kriegen eine CSS-Klasse zum Einklappen.
`show-more`/`show-less` erzeugen dann nichts mehr, sie togglen nur Sichtbarkeit.

## Wohin kommt welche Funktion?

### Ins Frontmatter (Build-Zeit)

| Funktion | Wird zu |
|---|---|
| `processMilongas` | Datum parsen, sortieren, filtern – Kernstück |
| `createMilongaHTML` | Astro-Markup mit `.map()`; `if(description)` → `{milonga.description && <aside>…</aside>}` |
| `createMonthDividerHTML` | Monatswechsel-Logik in der `.map`-Schleife (Vergleich mit Vormonat statt `currentMonth`-State) |
| `generateAllMilongaSchemas` | `<script type="application/ld+json" set:html={JSON.stringify(schema)} />` direkt im Markup |
| Konstanten `dayNames`, `monthNames` … | Lookup-Tabellen fürs Rendern |

### Bleibt Client-JS (Laufzeit-Interaktion)

| Funktion | Anmerkung |
|---|---|
| Button-Handler `moreBtn`/`lessBtn` | Togglen Klassen statt Daten zu bauen |
| `collapseMilongas` | „Klassen wieder setzen" statt `.remove()` |
| `announceUpdate` | Screenreader-Ansage, feuert beim Togglen |

### Fällt weg

| Funktion | Grund |
|---|---|
| `getMilongas` | Ersetzt durch `import`. Kaputtes JSON bricht jetzt den **Build** ab statt zur Laufzeit – Fehler vor dem Deploy sichtbar |
| `displayNextMilongas` | Als Generator tot; Schleife → `.map`, „nächste k" → CSS-Toggle |
| `initMilongaCal` | Kein Init-Orchestrator mehr nötig |

## Zwei Gotchas

1. **`defaultAmount` per `screen.width`** (`milonga-cal.js:7`)
   Build-Zeit kennt die Bildschirmbreite nicht. Welche `<li>` initial eingeklappt
   sind, muss client-seitig entschieden werden – per CSS-Media-Query
   (`@media (max-width:600px)`), kein JS nötig.

2. **`processMilongas` filtert `date >= today`**
   Das `today` ist beim Build **eingefroren**. Auf GitHub Pages verschwinden
   vergangene Milongas erst beim nächsten Build, nicht automatisch um Mitternacht.
   Optionen:
   - GH Action per `schedule:` (Cron) regelmäßig neu bauen, **oder**
   - genau diesen Datums-Filter client-seitig lassen.

   Das ist die eigentliche Design-Entscheidung beim Wechsel Runtime → Build-Time.
