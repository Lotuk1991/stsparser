import asyncio
from playwright.async_api import async_playwright

async def get_lot_info(lot_id: str) -> str:
    url = f"https://www.copart.com/lot/{lot_id}"

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(url)
            await page.wait_for_timeout(5000)

            data = await page.evaluate("() => window.__INITIAL_STATE__")
            await browser.close()

            lot = data.get("lotDetails", {}).get("data", {})
            if not lot:
                return "❌ Лот не знайдено або сторінка не містить інформації."

            return (
                f"<b>{lot.get('ln', 'Без назви')}</b>
"
                f"Марка: {lot.get('make', '—')}
"
                f"Модель: {lot.get('model', '—')}
"
                f"Рік: {lot.get('year', '—')}
"
                f"Тип: {lot.get('lotType', '—')}
"
                f"Пробіг: {lot.get('odometer', {}).get('value', '—')} mi
"
                f"Ключі: {lot.get('keys', '—')}
"
                f"Трансмісія: {lot.get('transmission', '—')}
"
                f"Тип палива: {lot.get('fuel', '—')}
"
                f"Пошкодження: {lot.get('damageDescription', '—')}"
            )

    except Exception as e:
        return f"❌ Помилка: {str(e)}"

if __name__ == "__main__":
    print(asyncio.run(get_lot_info("49338245")))
