# Umstieg in HACS: vom alten auf das neue Repository

Für alle, die die Integration bis Version 0.6 aus
`Thomas1607Haja/Rezepteverwaltung_Essenplan` installiert haben. Dauer etwa
10 Minuten. Die Domain bleibt `rezeptplaner`: Eintrag unter Geräte & Dienste,
Entitäts-IDs (`calendar.rezeptplaner_essensplan`, `sensor.rezeptplaner_heute`),
Automationen und Dashboard-Karten bleiben erhalten.

**Ab Home Assistant 2026.11** heißt HACS **Marketplace** (Einstellungen →
Marketplace) und hat beim ersten Start alle Einträge aus HACS übernommen. Die
Reihenfolge der Schritte bleibt gleich, nur die Menüs heißen anders:
„Entfernen“ ist ⋮ → **Uninstall**, das neue Repository kommt über **Add from
link** hinzu, und das alte Repository entfernst du aus der Liste der
benutzerdefinierten Repositories
([direkt öffnen](https://my.home-assistant.io/redirect/marketplace_repositories/)).

## 0. Backup

1. **Einstellungen → System → Backups → Backup erstellen** (vollständig, mit
   Home Assistant und Apps).
2. Warten, bis das Backup in der Liste steht.

## 1. Vorher notieren

- **Einstellungen → Geräte & Dienste → Rezeptplaner**: Der Eintrag ist da und
  „eingerichtet“.
- **HACS → Rezeptplaner**: zeigt „android-v0.…“ (das ist der Fehler).

## 2. Altes Repository aus HACS entfernen

1. **HACS** öffnen, **Rezeptplaner** anklicken → ⋮ oben rechts → **Entfernen**
   → bestätigen. Das löscht nur die Dateien unter
   `/config/custom_components/rezeptplaner`. Der Eintrag unter Geräte & Dienste
   bleibt.
2. **Jetzt nicht neu starten.**
3. **HACS → ⋮ → Benutzerdefinierte Repositories**: Den Eintrag
   `https://github.com/Thomas1607Haja/Rezepteverwaltung_Essenplan` (Typ
   Integration) mit dem Mülleimer entfernen, falls er noch da ist.

   Das **App-Repository** im App-Store (Einstellungen → Apps → App-Store →
   ⋮ → Repositories) bleibt unverändert. Darüber kommt weiter die
   Rezeptplaner-App.

## 3. Neues Repository hinzufügen und 0.7.0 installieren

1. Diesen Link öffnen und „Öffnen“ bestätigen:
   https://my.home-assistant.io/redirect/marketplace_repository/?owner=Thomas1607Haja&repository=rezeptplaner-ha&category=integration

   Alternativ: **HACS → ⋮ → Benutzerdefinierte Repositories**, Adresse
   `https://github.com/Thomas1607Haja/rezeptplaner-ha`, Typ **Integration**,
   **Hinzufügen**.
2. Im Repository auf **Herunterladen** klicken, Version **0.7.0** wählen und
   bestätigen.
3. HACS zeigt danach „Neustart erforderlich“.

## 4. Neustart

**Einstellungen → System → ⋮ oben rechts → Home Assistant neu starten**
(vollständiger Neustart, kein schnelles Neuladen).

## 5. Prüfen

- **HACS → Rezeptplaner** zeigt **0.7.0** (nicht mehr „android-v…“).
- **Einstellungen → Geräte & Dienste → Rezeptplaner**: eingerichtet, mit
  neuem Icon (ab Home Assistant 2026.3), keine Fehlermeldung.
- `calendar.rezeptplaner_essensplan` und `sensor.rezeptplaner_heute` haben
  Werte (Entwicklerwerkzeuge → Zustände).
- Dashboard mit Strg+F5 neu laden, dann wird die Karte „Essensplan“ angezeigt.
  In der Companion-App ggf. unter Einstellungen → Companion-App →
  Fehlerbehebung den Frontend-Cache zurücksetzen.
- Künftige Versionen meldet HACS als Update.

## Falls etwas schiefgeht

- **Integration „nicht geladen“ nach dem Neustart:** Wahrscheinlich wurde
  Schritt 2 nach Schritt 3 ausgeführt, dann fehlen die Dateien. In HACS
  „Rezeptplaner“ (rezeptplaner-ha) erneut herunterladen und neu starten.
- **Eintrag unter Geräte & Dienste ist weg:** Rezeptplaner-App einmal neu
  starten. Sie meldet sich wieder an, und „Rezeptplaner“ erscheint unter
  **Entdeckt**. Bestätigen. Die Entitäts-IDs entstehen dann wieder aus den Namen und sind in der Regel dieselben.
- **Alles zurück:** Einstellungen → System → Backups → das Backup aus
  Schritt 0 → Wiederherstellen.
