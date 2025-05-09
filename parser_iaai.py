import requests
from bs4 import BeautifulSoup

def fetch_iaai_info_by_stock_number(stock_number: str) -> dict:
    fs_url = "http://localhost:8191/v1"
    search_url = f"https://www.iaai.com/Search?Keyword={stock_number}"

    payload = {
        "cmd": "request.get",
        "url": search_url,
        "maxTimeout": 60000
    }

    try:
        response = requests.post(fs_url, json=payload, timeout=60)
        result = response.json()

        if "solution" in result and "response" in result["solution"]:
            html = result["solution"]["response"]
            return parse_iaai_html(html)
        else:
            return {"error": "❌ Не вдалося отримати HTML-контент від FlareSolverr"}
    except Exception as e:
        print("❌ FlareSolverr error:", e)
        return {"error": "⚠️ Внутрішня помилка запиту до FlareSolverr"}

def parse_iaai_html(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')

    def get_value(label):
        item = soup.find("span", string=lambda s: s and label in s)
        if item:
            parent = item.find_parent("li", class_="data-list__item")
            value = parent.find("span", class_="data-list__value") if parent else None
            return value.text.strip() if value else "—"
        return "—"

    return {
        "VIN": get_value("VIN"),
        "Odometer": get_value("Odometer"),
        "Location": get_value("Selling Branch"),
        "Loss": get_value("Loss"),
        "Primary Damage": get_value("Primary Damage"),
        "Title": get_value("Title/Sale Doc"),
        "Airbags": get_value("Airbags"),
        "Engine": get_value("Engine"),
        "Drive Line Type": get_value("Drive Line Type"),
        "Transmission": get_value("Transmission"),
        "Fuel Type": get_value("Fuel Type"),
        "Cylinders": get_value("Cylinders"),
        "Keys": get_value("Key"),
        "Auction Date": get_value("Auction Date and Time"),
    }
