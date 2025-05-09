import asyncio
from playwright.async_api import async_playwright
import json

async def save_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # открывает реальный браузер
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.copart.com")

        print("🔐 Авторизуйтесь в браузере вручную, затем нажмите Enter в терминале.")
        input()

        cookies = await context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)

        print("✅ Cookies сохранены в cookies.json")
        await browser.close()

asyncio.run(save_cookies())