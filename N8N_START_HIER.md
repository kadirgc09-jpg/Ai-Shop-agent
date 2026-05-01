# N8N START HIER

Du willst einen n8n-Agenten. Genau dafuer ist diese Datei.

## Was ich dir gebaut habe

Ich habe dir eine n8n-Workflow-Datei vorbereitet:

```text
workflows/n8n-shop-agent.json
```

Diese Datei kannst du in n8n importieren.

## Was der n8n-Agent macht

Du gibst einen Online-Shop ein.

Der Workflow prueft dann:

1. Website laden
2. E-Mail-Adressen finden
3. Hinweise auf Chatbot finden
4. Score erstellen
5. Verkaufsnachricht vorbereiten

## So importierst du es in n8n

1. Oeffne n8n
2. Klicke links auf Workflows
3. Klicke oben rechts auf die drei Punkte
4. Klicke Import from File
5. Lade diese Datei hoch:

```text
workflows/n8n-shop-agent.json
```

## Wichtig

Dieser erste n8n-Agent braucht noch keinen API-Key.

Er ist extra einfach gebaut, damit du erstmal verstehst, wie n8n funktioniert.

## Danach

Spaeter bauen wir Version 2 mit OpenAI API, Google Sheets und Gmail-Entwuerfen.
