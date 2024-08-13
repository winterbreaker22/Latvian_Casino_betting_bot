from playwright.async_api import async_playwright
import asyncio
import json
import time

async def site_name_to_url(name: str) -> str:
    url: str = ""
    if name == "x3000":
        url = "https://www.x3000.lv/betting?flowType=gamingOverview#sports-hub/tennis"
    elif name == "casino777":
        url = ""
    else:
        url = ""
    return url

async def extract_from_xx(page) -> dict:
    winner: dict = {
        "first": {
            "name": "",
            "odd": "",
            "wager": "",
            "site": "",
        },
        "second": {
            "name": "",
            "odd": "",
            "wager": "",
            "site": "",
        },
        "category": "",
    }

    first_odd = await page.query_selector('tr:first-of-type td:nth-of-type(4) h2:first-of-type')
    winner["first"]["odd"] = await first_odd.text_content()
    second_odd = await page.query_selector('tr:first-of-type td:nth-of-type(4) h2:last-of-type')
    winner["second"]["odd"] = await second_odd.text_content()
    first_wager = await page.query_selector('tr:first-of-type td:nth-of-type(5) h3:first-of-type')
    first_wager_value = await first_wager.text_content()
    second_wager = await page.query_selector('tr:first-of-type td:nth-of-type(5) h3:last-of-type')
    second_wager_value = await second_wager.text_content()
    winner["first"]["wager"] = first_wager_value.split(' ')[1]
    winner["second"]["wager"] = second_wager_value.split(' ')[1]
    category_element = await page.query_selector('tr:first-of-type td:first-of-type > span:nth-of-type(2)')
    winner["category"] = await category_element.text_content()
    first_site_element = await page.query_selector('tr:first-of-type td:last-of-type a:first-of-type')
    first_site_element_value = await first_site_element.text_content()
    second_site_element = await page.query_selector('tr:first-of-type td:last-of-type a:last-of-type')
    second_site_element_value = await second_site_element.text_content()
    winner["first"]["site"] = await site_name_to_url(first_site_element_value)
    winner["second"]["site"] = await site_name_to_url(second_site_element_value)
    name = await page.query_selector('tr:first-of-type td:first-of-type h2')
    both_name = await name.text_content()
    winner["first"]["name"] = both_name.split('vs.')[0].strip()
    winner["second"]["name"] = both_name.split('vs.')[1].strip()

    return winner

async def bet(page, winner: dict, who: str):
    await page.goto(winner[who]["site"])
    time.sleep(40)
    
    text_to_find = winner["category"]
    try:
        element = await page.wait_for_selector(f"text={text_to_find}", timeout=15000)
        if element:
            print(f"{element} selected.")
            await element.click()
            text_to_find = winner[who]["odd"]
            try:
                element = await page.wait_for_selector(f"text={text_to_find}", timeout=15000)
                if element:
                    print(f"{element} selected.")
                    await element.click()

                    # Bet Wager
                    element = await page.query_selector("input[class='mod-KambiBC-stake-input']")
                    await page.fill(element, winner[who]["wager"])
                    bet_btn = await page.query_selector("button[class='mod-KambiBC-betslip__place-bet-btn']")
                    await bet_btn.click()
                    bet_slip = await page.query_selector("button[class='mod-KambiBC-betslip-button--highlighted']")
                    await bet_slip.click()

                else:
                    print(f"{element} not found.")
            except TimeoutError as error:
                print(error)
        else:
            print(f"{element} not found.")
    except TimeoutError as error:
        print(error)
    
async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)  # Set headless=True if you don't want to see the browser UI
    context = await browser.new_context()
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)

    await context.add_cookies(cookies)
    page = await context.new_page()

    await page.goto("https://www.rr28.xyz/")    
    time.sleep(3)

    text_to_find = "History"
    try:
        element = await page.wait_for_selector(f"text={text_to_find}", timeout=5000)
        if element:
            print(f"History entered.")
            await element.click()
            time.sleep(3)
        else:
            print(f"History button not found.")
    except TimeoutError as error:
        print(error)
    
    winner: dict = await extract_from_xx(page)
    print (winner)

    # First Winner Bet
    await bet(page, winner, "first")
    # Second Winner Bet
    # await bet(page, winner, "second")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())

