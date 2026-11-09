"""Prüft, dass alle Sprachdateien der Integration und der Karte dieselben
Schlüssel und Platzhalter haben (Englisch ist die Rückfallsprache).

Ausführen: python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTEGRATION = ROOT / "custom_components" / "rezeptplaner"

LANGUAGES = ("en", "de", "fr", "es", "it")
PLURAL_FORMS = {"zero", "one", "two", "few", "many", "other"}
PLACEHOLDER = re.compile(r"\{[a-z_][a-z0-9_]*\}|%(?:\d+\$)?[sd]")


def flatten(value, prefix: str = "", out: dict[str, str] | None = None) -> dict[str, str]:
    """Verschachteltes JSON als flache Schlüssel ("a.b.c"); ein Objekt nur
    aus Pluralformen wird zu "schlüssel#one", "schlüssel#other" usw."""
    out = {} if out is None else out
    if isinstance(value, dict):
        if value and set(value) <= PLURAL_FORMS:
            for form, text in value.items():
                out[f"{prefix}#{form}"] = text if isinstance(text, str) else ""
            return out
        for key, child in value.items():
            flatten(child, f"{prefix}.{key}" if prefix else key, out)
    elif isinstance(value, str):
        out[prefix] = value
    else:
        out[prefix] = ""
    return out


def base_keys(entries: dict[str, str]) -> set[str]:
    return {key.split("#", 1)[0] for key in entries}


def placeholders_of(entries: dict[str, str], base: str) -> list[str]:
    found: set[str] = set()
    for key, text in entries.items():
        if key == base or key.startswith(base + "#"):
            found.update(PLACEHOLDER.findall(text))
    return sorted(found)


def first_text(entries: dict[str, str], base: str) -> str:
    return entries.get(base, entries.get(base + "#other", ""))


def compare(name: str, files: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    en = files.get("en")
    if en is None:
        return [f"{name}: englische Datei fehlt (Rückfallsprache)"]
    en_keys = base_keys(en)
    for lang in LANGUAGES:
        entries = files.get(lang)
        if entries is None:
            errors.append(f"{name}: Sprache {lang} fehlt")
            continue
        keys = base_keys(entries)
        errors += [f"{name} [{lang}]: Schlüssel {k!r} fehlt" for k in sorted(en_keys - keys)]
        for key in sorted(keys):
            if key not in en_keys:
                errors.append(f"{name} [{lang}]: Schlüssel {key!r} gibt es im Englischen nicht")
                continue
            if key not in entries and key + "#other" not in entries:
                errors.append(f'{name} [{lang}]: {key!r} hat Pluralformen, aber keine Form "other"')
            if not first_text(entries, key).strip():
                errors.append(f"{name} [{lang}]: {key!r} ist leer")
            want, got = placeholders_of(en, key), placeholders_of(entries, key)
            if want != got:
                errors.append(f"{name} [{lang}]: {key!r} hat Platzhalter {got}, Englisch {want}")
    return errors


def read_json_dir(directory: Path) -> dict[str, dict[str, str]]:
    files = {}
    for lang in LANGUAGES:
        path = directory / f"{lang}.json"
        if path.exists():
            files[lang] = flatten(json.loads(path.read_text(encoding="utf-8")))
    return files


class TranslationTests(unittest.TestCase):
    def assert_no_errors(self, errors: list[str]) -> None:
        self.assertFalse(errors, "\n" + "\n".join(errors))

    def test_integration_translations(self) -> None:
        self.assert_no_errors(compare("translations", read_json_dir(INTEGRATION / "translations")))

    def test_integration_texts(self) -> None:
        """Texte der Kalendertermine und des Sensors."""
        self.assert_no_errors(compare("texts", read_json_dir(INTEGRATION / "texts")))

    def test_card_translations(self) -> None:
        """Die Karte ist eine einzelne JS-Datei ohne Build; ihre Texte stehen
        als reines JSON zwischen "// i18n:begin" und "// i18n:end"."""
        source = (INTEGRATION / "frontend" / "rezeptplaner-card.js").read_text(encoding="utf-8")
        _, found, rest = source.partition("// i18n:begin")
        self.assertTrue(found, "// i18n:begin fehlt")
        block, found, _ = rest.partition("// i18n:end")
        self.assertTrue(found, "// i18n:end fehlt")
        texts = json.loads(block[block.index("{") : block.rindex("}") + 1])
        files = {lang: flatten(value) for lang, value in texts.items()}
        self.assert_no_errors(compare("rezeptplaner-card.js", files))

    def test_manifest(self) -> None:
        manifest = json.loads((INTEGRATION / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["domain"], "rezeptplaner")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
