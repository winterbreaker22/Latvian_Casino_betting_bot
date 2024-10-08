import asyncio
from playwright.async_api import async_playwright
import json

bet_time = False
winner_info = None
old_winner_info = None

tennis_category: dict = {
    "Grand Slam": "Grand Slam",
    "ATP": "ATP",
    "WTA": "WTA",
    "Challenger": "Challenger",
    "Challenger Doubles": "Challenger dubultspēles",
    "ATP Doubles": "ATP Doubles",
    "ITF Men": "ITF Vīriešu Vienspēles",
    "ITF Men Doubles": "ITF Vīriešu Dubultspēles",
    "ITF Men Qual.": "ITF Viriešu Kvalifikācijas Turnīrs",
    "ITF Women": "ITF Sieviešu Vienspēles",
    "WTA Doubles": "WTA dubultspēles",
}

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
    winner["first"]["site"] = await first_site_element.text_content()
    second_site_element = await page.query_selector('tr:first-of-type td:last-of-type a:last-of-type')
    winner["second"]["site"] = await second_site_element.text_content()
    name = await page.query_selector('tr:first-of-type td:first-of-type h2')
    both_name = await name.text_content()
    winner["first"]["name"] = both_name.split('vs.')[0].strip()
    winner["second"]["name"] = both_name.split('vs.')[1].strip()

    return winner

# Async function to run the xx browser
async def run_rr(playwright):
    global bet_time
    global winner_info
    global old_winner_info
    
    # Launch first browser instance
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # Navigate to the first URL
    await page.goto("https://www.rr28.xyz/")
    await asyncio.sleep(50)
    text_to_find = "History"
    try:
        element = await page.wait_for_selector(f"text={text_to_find}", timeout=5000)
        if element:
            print(f"History entered.")
            await element.click()
            await asyncio.sleep(3)
        else:
            print(f"History button not found.")
    except TimeoutError as error:
        print(error)

    while True:
        winner_info = await extract_from_xx(page)
        if winner_info is not None and winner_info != old_winner_info:
            if not bet_time:
                bet_time = True # Trigger action

        await asyncio.sleep(3)  # Polling delay

    # Keep the browser open for further actions or close it
    # await browser.close()

# Async function to run the second browser and react to the shared variable
async def run_x3000(playwright):
    global bet_time
    global winner_info
    global old_winner_info
    global tennis_category
    
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(locale="en-US")
    with open('x3000_cookies.json', 'r') as f:
        cookies = json.load(f)
    await context.add_cookies(cookies)
    page = await context.new_page()

    await page.goto("https://www.x3000.lv/betting?flowType=gamingOverview#sports-hub/tennis")
    await asyncio.sleep(10)

    # Login
    play_btn = page.locator('body header').locator(f'text=Play')
    await play_btn.click()
    await asyncio.sleep(5)

    login = await page.wait_for_selector(f'text=Log in with credentials', timeout=8000)
    if login:
        await login.click()
    await page.fill('input[name="email"]', "retssrets@gmail.com")
    await page.fill('input[name="password"]', "Upwork123456!")

    login_btn = page.locator('form').locator(f'text=Log In')
    await login_btn.click()
    await asyncio.sleep(10)

    unnecessary = page.locator('#flow-content-container path')
    if await unnecessary.is_visible():
        await unnecessary.click()

    await page.goto("https://www.x3000.lv/betting?flowType=gamingOverview#sports-hub/tennis")
    await asyncio.sleep(10)

    # Wait for the shared variable to be updated
    while True:
        if bet_time:
            bet = True
            if winner_info["first"]["site"] == "x3000":
                who = "first"
            elif winner_info["second"]["site"] == "x3000":
                who = "second"
            else:
                bet = False 
            if bet:           
                print ("x3000 entered")
                frame_sel = '[src^="/static/betting-clients/kambi/kambi-client.html?language=lv&outcomeID=true#sports-hub/tennis"]'
                frame = page.frame_locator(frame_sel)
                try:
                    # category_element = frame.locator("div.KambiBC-scroller").locator("ul.KambiBC-filter-menu").locator(f"ul.KambiBC-filter-menu:nth-of-type({tennis_category[winner_info["category"]]}) > div")
                    category_element = frame.locator("div.KambiBC-scroller").locator(f"text={tennis_category[winner_info["category"]]}")
                    if category_element:
                        await category_element.click()
                        print(f"{category_element} selected.")
                        await asyncio.sleep(1)
                        try:
                            odd_element = frame.locator("ul.KambiBC-sandwich-filter__list").locator(f"text={winner_info[who]["odd"]}")
                            if await odd_element.is_visible():
                                await odd_element.click()
                                print(f"{odd_element} selected.")
                                await asyncio.sleep(1)

                                # Bet Wager
                                wager_element = frame.locator("div.mod-KambiBC-betslip").locator("input.mod-KambiBC-stake-input")
                                await wager_element.fill(winner_info[who]["wager"])
                                bet_btn = frame.locator("button.mod-KambiBC-betslip__place-bet-btn")
                                await bet_btn.click()
                                bet_slip = frame.locator("button.mod-KambiBC-betslip-button--highlighted")
                                await bet_slip.click()

                            else:
                                print(f"{odd_element} not found.")
                                bet_time = False
                                old_winner_info = winner_info
                        except TimeoutError as error:
                            print(error)
                    else:
                        print(f"{category_element} not found.")
                except TimeoutError as error:
                    print(error)

                old_winner_info = winner_info
                bet_time = False
        await asyncio.sleep(1)

    # Keep the browser open for further actions or close it
    # await browser.close()
  
# Main function to run both browsers simultaneously
async def main():
    async with async_playwright() as playwright:
        task_main = asyncio.create_task(run_rr(playwright))
        task_x3000 = asyncio.create_task(run_x3000(playwright))

        await asyncio.gather(task_main, task_x3000)

if __name__ == "__main__":
    asyncio.run(main())
