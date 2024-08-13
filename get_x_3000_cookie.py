from playwright.async_api import async_playwright
import asyncio
import browser_cookie3
import time
import json

async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)  # Set headless=True if you don't want to see the browser UI
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.x3000.lv/")    
    time.sleep(10)

    accept_cookies = await page.wait_for_selector(f"text=Accept all", timeout=8000)
    if accept_cookies:
        await accept_cookies.click()
    time.sleep(3)

    sports = await page.wait_for_selector(f"text=Sports", timeout=8000)
    if sports:
        print ("sports clicked")
        await sports.click()
    time.sleep(20)

    login = await page.wait_for_selector(f'text=Log in with credentials', timeout=8000)
    if login:
        await login.click()
    time.sleep(3)

    await page.fill('input[name="email"]', "retssrets@gmail.com")
    await page.fill('input[name="password"]', "Upwork123456!")

    login_btn = await page.wait_for_selector('text=Log In', timeout=8000)
    await login_btn.click()
    time.sleep(3)
    
    # cross = await page.wait_for_selector('svg')
    # await cross.click()
    time.sleep(10)
    await page.goto('https://www.x3000.lv/betting?flowType=gamingOverview#sports-hub/tennis')
    time.sleep(30)

    cookies = await context.cookies()

        # Save cookies to a JSON file
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)

    print("Cookies saved to cookies.json")


async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())


