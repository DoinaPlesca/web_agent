import requests
from bs4 import BeautifulSoup


def get_stock_price(url: str) -> dict:

    try:
        session = requests.Session()

        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        })

        r = session.get(url, timeout=10,allow_redirects=True)
        if"consent.google.com" in r.url:

         consent_payload = {
            "continue": url,
            "gl": "US",
            "hl": "en",
            "m": "0",
            "pc": "fgc",
            "cm": "2",
            "set_eom": "false",
            "bl": "boq_consentrevamp",
            "yes": "yes"
        }

        session.post(
            "https://consent.google.com/save",
            data=consent_payload,timeout=10)

        r =session.get(url, timeout=10)


        html = r.text

        soup = BeautifulSoup(html, "html.parser")

        price_tag = soup.select_one("div.YMlKec.fxKbKc")

        if not price_tag:
            return {
                "success": False,
                "error": "Could not find price on page",
                "final_url": r.url
            }

        price = price_tag.text.strip().replace(",", "").replace("$", "")

        return {
            "success": True,
            "price": price,
            "source_url": r.url
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


