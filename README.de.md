# Rezeptplaner für Home Assistant

[English](README.md) · **Deutsch**

Integration und Dashboard-Karte für den [Rezeptplaner](https://github.com/Thomas1607Haja/Rezepteverwaltung_Essenplan) – eine schlanke Rezeptverwaltung mit Essensplan, die als App (Add-on) in Home Assistant läuft.

- **Dashboard-Karte** „Essensplan“ mit den nächsten Tagen
- **Kalender** „Essensplan“ mit allen geplanten Gerichten
- **Sensor** „Heute“ (z. B. für eine Ansage „Heute gibt es …“)

Voraussetzung ist die **Rezeptplaner-App** in Home Assistant. Zuerst installieren:

[![Home Assistant öffnen und die Rezeptplaner-App anzeigen (fügt bei Bedarf das Repository hinzu).](https://my.home-assistant.io/badges/supervisor_app.svg)](https://my.home-assistant.io/redirect/supervisor_app/?app=45a92d34_rezeptplaner&repository_url=https%3A%2F%2Fgithub.com%2FThomas1607Haja%2FRezepteverwaltung_Essenplan)

Erscheint die App nicht, das Repository unter Einstellungen → Apps → App-Store → ⋮ → Repositories hinzufügen: `https://github.com/Thomas1607Haja/Rezepteverwaltung_Essenplan`.

## Installation über HACS

[![Home Assistant öffnen und dieses Repository im Marketplace anzeigen.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=Thomas1607Haja&repository=rezeptplaner-ha&category=integration)

1. Auf den Button oben klicken – oder unter **Einstellungen → Marketplace → Add from link** `Thomas1607Haja/rezeptplaner-ha` eintragen. Vor Home Assistant 2026.11 öffnet der Button HACS; dort **HACS → ⋮ → Benutzerdefinierte Repositories** mit Typ **Integration**.
2. **Rezeptplaner** herunterladen und Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste** erscheint „Rezeptplaner“ als **Entdeckt** – auf **Hinzufügen** klicken und bestätigen. Adresse und Schlüssel liefert die App selbst. Oder die Einrichtung hier starten:

   [![Home Assistant öffnen und die Einrichtung der Rezeptplaner-Integration starten.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=rezeptplaner)
4. Die Seite einmal neu laden (F5), dann im Dashboard eine Karte **Essensplan** hinzufügen (in der Kartenauswahl oder als `type: custom:rezeptplaner-card`).

Die Integration trägt die Karte selbst als Dashboard-Ressource ein (Einstellungen → Dashboards → ⋮ → Ressourcen) und hält den Eintrag bei Updates aktuell. Werden die Ressourcen in YAML gepflegt (`lovelace: resource_mode: yaml`), dort einen Eintrag mit `url: /rezeptplaner_static/rezeptplaner-card.js` und `type: module` ergänzen; bis dahin lädt die Integration die Karte ersatzweise über die Startseite.

„Öffnen“ auf der Karte führt zur Weboberfläche der App – auch wenn die App nicht in der Seitenleiste steht.

### Einstellungen der Karte

| Feld | Bedeutung | Standard |
|---|---|---|
| `title` | Überschrift | „Essensplan“ in der Sprache des Nutzers |
| `days` | Anzahl Tage ab heute (1–31) | aktueller Einkaufszeitraum |
| `height` | Höhe in Pixel; passt nicht alles hinein, scrollt der Inhalt innerhalb der Karte | so hoch wie der Inhalt |

### Entitäten

Die Entitäts-IDs richten sich nach der Sprache bei der Einrichtung, z. B. `calendar.rezeptplaner_essensplan` und `sensor.rezeptplaner_heute` auf Deutsch, `calendar.rezeptplaner_meal_plan` und `sensor.rezeptplaner_today` auf Englisch. Bestehende Entitäten behalten ihre IDs.

## Umstieg vom bisherigen Repository

Bis Version 0.6 lag die Integration im Repository `Thomas1607Haja/Rezepteverwaltung_Essenplan`. HACS zeigte dort die Version der Android-App an und meldete keine Updates. Die Domain ist weiterhin `rezeptplaner` – Einrichtung, Entitäten und Karten bleiben erhalten:

1. Backup erstellen (Einstellungen → System → Backups).
2. **HACS:** „Rezeptplaner“ öffnen → ⋮ → **Entfernen**, danach unter ⋮ → Benutzerdefinierte Repositories `…/Rezepteverwaltung_Essenplan` entfernen (nur den Eintrag für die Integration – das App-Repository im App-Store bleibt). Entfernen löscht nur die Dateien; der Eintrag unter Geräte & Dienste bleibt.
3. Dieses Repository hinzufügen (Knopf oben), **Rezeptplaner 0.7.0** herunterladen.
4. Home Assistant neu starten.

Schritt 2 und 3 nicht vertauschen: Wer den alten Eintrag erst nach dem Herunterladen entfernt, löscht damit die frisch installierten Dateien wieder. Ausführliche Anleitung mit Prüfpunkten: [docs/UMSTIEG.md](docs/UMSTIEG.md).

## Sprachen

Deutsch, Englisch, Französisch, Spanisch und Italienisch. Die Integration nutzt die Systemsprache von Home Assistant, die Karte die Sprache des angemeldeten Nutzers; Rückfall ist Englisch. Die Texte stehen in `custom_components/rezeptplaner/translations/`, `texts/` und im Block zwischen `// i18n:begin` und `// i18n:end` in `frontend/rezeptplaner-card.js`. Verbesserungen sind willkommen – `python -m unittest discover -s tests` prüft, dass alle Sprachen dieselben Schlüssel und Platzhalter haben.

## Zugriff über einen Cloudflare-Tunnel

Cloudflare speichert ohne eigene Regel auch Fehlerantworten zwischen und weist Browser an, sie 4 Stunden zu behalten. Fragt ein Browser oder die Companion-App die Karte während eines Neustarts von Home Assistant ab, bleibt sie danach stundenlang verschwunden („Konfigurationsfehler“). Abhilfe im Cloudflare-Dashboard der Domain:

1. **Caching → Cache Rules → Create rule:** Name „Home Assistant nicht cachen“, Bedingung *Hostname equals* `<HA-Hostname>`, Aktion **Bypass cache**, speichern.
2. **Caching → Configuration → Browser Cache TTL:** **Respect Existing Headers**.
3. Einmalig **Caching → Configuration → Purge Everything**; in der Companion-App unter Einstellungen → Companion-App → Fehlerbehebung den Frontend-Cache zurücksetzen.

## Sicherheit

Für die Integration erzeugt die App einen eigenen Schlüssel und teilt ihn Home Assistant über die Discovery mit. Mit diesem Schlüssel lassen sich im internen Netz nur Essensplan, Rezepte und Bilder lesen.

## Releases

Die Version steht in `custom_components/rezeptplaner/manifest.json` (`version`). Ein Tag `v1.2.3` erzeugt das GitHub-Release – nur wenn Übersetzungstest, hassfest und HACS-Prüfung grün sind. Änderungen: [CHANGELOG.md](CHANGELOG.md).

## Hilfe und Fehlermeldungen

Fragen und Fehler zur Integration oder Karte: [Issues dieses Repositorys](https://github.com/Thomas1607Haja/rezeptplaner-ha/issues). Zur App selbst: [Rezepteverwaltung_Essenplan](https://github.com/Thomas1607Haja/Rezepteverwaltung_Essenplan/issues).

## Lizenz

[MIT](LICENSE)
