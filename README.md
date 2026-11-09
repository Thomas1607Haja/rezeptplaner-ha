# Rezeptplaner for Home Assistant

**English** · [Deutsch](README.de.md)

Home Assistant integration and dashboard card for [Rezeptplaner](https://github.com/Thomas1607Haja/Rezepteverwaltung_Essenplan) – a lean recipe manager and meal planner that runs as an app (add-on) in Home Assistant.

- **Dashboard card** “Meal plan” with the upcoming days
- **Calendar** “Meal plan” with every planned dish
- **Sensor** “Today” (e.g. for an announcement “Today we're having …”)

The integration needs the **Rezeptplaner app** in Home Assistant. Install it first: Settings → Apps → App store → ⋮ → Repositories, add `https://github.com/Thomas1607Haja/Rezepteverwaltung_Essenplan` and install “Rezeptplaner”.

## Installation via HACS

[![Open your Home Assistant instance and open this repository in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Thomas1607Haja&repository=rezeptplaner-ha&category=integration)

1. Click the button above – or in **HACS → ⋮ → Custom repositories** add `https://github.com/Thomas1607Haja/rezeptplaner-ha` with type **Integration**.
2. Download **Rezeptplaner** and restart Home Assistant.
3. Under **Settings → Devices & services**, “Rezeptplaner” appears as **Discovered** – click **Add** and confirm. The app provides address and key itself.
4. Reload the page once (F5), then add a **Meal plan** card to a dashboard (from the card picker or as `type: custom:rezeptplaner-card`).

The integration registers the card as a dashboard resource itself (Settings → Dashboards → ⋮ → Resources) and keeps the entry up to date. If your resources are maintained in YAML (`lovelace: resource_mode: yaml`), add an entry with `url: /rezeptplaner_static/rezeptplaner-card.js` and `type: module`; until then the integration loads the card via the start page as a fallback.

“Open” on the card leads to the app's web interface – even if the app is not in the sidebar.

### Card options

| Field | Meaning | Default |
|---|---|---|
| `title` | Heading | “Meal plan” in the user's language |
| `days` | Number of days from today (1–31) | current shopping period |
| `height` | Height in pixels; if not everything fits, the card scrolls | as tall as the content |

### Entities

The entity IDs follow the language at setup, e.g. `calendar.rezeptplaner_meal_plan` and `sensor.rezeptplaner_today` in English, `calendar.rezeptplaner_essensplan` and `sensor.rezeptplaner_heute` in German. Existing entities keep their IDs.

## Moving from the old repository

Up to version 0.6 the integration was part of the repository `Thomas1607Haja/Rezepteverwaltung_Essenplan`. HACS showed the Android app's version there and offered no updates. The domain is still `rezeptplaner`, so your setup, entities and cards are kept:

1. Create a backup (Settings → System → Backups).
2. **HACS:** open “Rezeptplaner” → ⋮ → **Remove**, then under ⋮ → Custom repositories remove `…/Rezepteverwaltung_Essenplan` (only the integration entry – the app repository in the app store stays). Removing only deletes the files; the integration entry under Devices & services stays.
3. Add this repository (button above), download **Rezeptplaner 0.7.0**.
4. Restart Home Assistant.

Do not swap steps 2 and 3: removing the old entry after downloading would delete the freshly installed files again.

## Languages

English, German, French, Spanish and Italian. The integration uses the Home Assistant system language, the card the language of the logged-in user; English is the fallback. Translations live in `custom_components/rezeptplaner/translations/`, `texts/` and in the block between `// i18n:begin` and `// i18n:end` in `frontend/rezeptplaner-card.js`. Corrections are very welcome – `python -m unittest discover -s tests` checks that all languages have the same keys and placeholders.

## Access through a Cloudflare tunnel

Without a rule of its own, Cloudflare also caches error responses and tells browsers to keep them for 4 hours. If a browser or the companion app requests the card while Home Assistant is restarting, it stays missing for hours afterwards (“configuration error”). Fix it in the Cloudflare dashboard of your domain:

1. **Caching → Cache Rules → Create rule:** name “Do not cache Home Assistant”, condition *Hostname equals* `<HA host name>`, action **Bypass cache**, save.
2. **Caching → Configuration → Browser Cache TTL:** **Respect Existing Headers**.
3. Once: **Caching → Configuration → Purge Everything**; in the companion app reset the frontend cache under Settings → Companion app → Troubleshooting.

## Security

The app creates its own key for the integration and passes it to Home Assistant via discovery. This key can only read the meal plan, recipes and images inside the local network.

## Releases

Versions follow `version` in `custom_components/rezeptplaner/manifest.json`. A tag `v1.2.3` creates the GitHub release – only if the translation tests, hassfest and the HACS check pass. Changes: [CHANGELOG.md](CHANGELOG.md).

## Help and bug reports

Questions and bugs about the integration or card: [issues of this repository](https://github.com/Thomas1607Haja/rezeptplaner-ha/issues). About the app itself: [Rezepteverwaltung_Essenplan](https://github.com/Thomas1607Haja/Rezepteverwaltung_Essenplan/issues).

## License

[MIT](LICENSE)
