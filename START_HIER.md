# START HIER

Ich habe dir hier einen ersten Shop-Agenten gebaut.

Du musst den Code am Anfang nicht verstehen.

## Was du machst

Du schreibst Shop-Websites in diese Datei:

```text
data/lead_input.csv
```

Beispiel:

```csv
name,website,niche
Demo Shop,https://example.com,Mode
```

## Was der Agent macht

Er prueft die Website und erstellt eine vorbereitete Nachricht fuer den Shop.

## Ergebnis

Das Ergebnis landet in:

```text
data/leads_output.csv
```

## Start auf dem PC

```bash
python main.py
```
