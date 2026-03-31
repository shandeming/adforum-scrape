import asyncio
from playwright.async_api import async_playwright

url = "https://www.adforum.com/directories/agency/advertising?location=city:Chicago&discipline_strkey=DSP010"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        is_webdriver = await page.evaluate("navigator.webdriver")
        print(f"navigator.webdriver detected: {is_webdriver}")
        await page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        await page.goto(url)
        print(await page.title())
        await page.locator("#btnLoadmore").click()
        await browser.close()


asyncio.run(main())  # start a web browser
