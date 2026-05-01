import csv
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

INPUT_FILE = Path("data/lead_input.csv")
OUTPUT_FILE = Path("data/leads_output.csv")

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CHAT_WORDS = ["chatbot", "livechat", "live chat", "intercom", "zendesk", "tawk.to", "tidio", "crisp"]


def make_demo_file():
    INPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if INPUT_FILE.exists():
        return
    with INPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "website", "niche"])
        writer.writeheader()
        writer.writerow({"name": "Demo Shop", "website": "https://example.com", "niche": "Mode"})


def get_html(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        response = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code >= 400:
            return ""
        return response.text
    except Exception:
        return ""


def find_contact_pages(base_url, html):
    pages = []
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        text = link.get_text(" ", strip=True).lower()
        check = (href + " " + text).lower()
        if "kontakt" in check or "contact" in check or "impressum" in check:
            pages.append(urljoin(base_url, href))
    return list(dict.fromkeys(pages))[:3]


def analyze_shop(name, website, niche):
    html = get_html(website)
    emails = set(EMAIL_PATTERN.findall(html))
    chatbot_found = any(word in html.lower() for word in CHAT_WORDS)

    for page in find_contact_pages(website, html):
        page_html = get_html(page)
        emails.update(EMAIL_PATTERN.findall(page_html))
        if any(word in page_html.lower() for word in CHAT_WORDS):
            chatbot_found = True

    score = 50
    if emails:
        score += 25
    if not chatbot_found:
        score += 20
    if niche:
        score += 5

    note = "Guter Kandidat, kein klarer Chatbot gefunden." if not chatbot_found else "Hat eventuell schon Chat oder Support-Tool."

    email_text = create_message(name, website, niche, chatbot_found)

    return {
        "name": name,
        "website": website,
        "niche": niche,
        "emails": ", ".join(sorted(emails)),
        "chatbot_found": chatbot_found,
        "score": min(score, 100),
        "note": note,
        "message": email_text,
    }


def create_message(name, website, niche, chatbot_found):
    shop = name or website
    if chatbot_found:
        problem = "Ich habe gesehen, dass Sie eventuell schon eine Chat-Loesung nutzen. Vielleicht kann man diese noch besser fuer Verkauf und Kundenservice einsetzen."
    else:
        problem = "Ich habe keinen klaren KI-Chatbot auf Ihrer Website gesehen. Dadurch bleiben viele Kundenfragen eventuell unbeantwortet."

    return f"""Betreff: Kurze Idee fuer {shop}

Hallo {shop}-Team,

ich habe mir Ihre Website angeschaut und hatte eine kurze Idee.

{problem}

Ich baue einfache KI-Kundenservice-Bots fuer Online-Shops. Der Bot kann haeufige Fragen beantworten und Kunden schneller helfen.

Haetten Sie Interesse an einer kostenlosen Mini-Analyse Ihrer Website?

Viele Gruesse
Kadir
""".strip()


def main():
    make_demo_file()

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    results = []
    for row in rows:
        print("Pruefe:", row.get("website", ""))
        results.append(analyze_shop(row.get("name", ""), row.get("website", ""), row.get("niche", "")))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "website", "niche", "emails", "chatbot_found", "score", "note", "message"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("Fertig. Ergebnis ist in data/leads_output.csv")


if __name__ == "__main__":
    main()
