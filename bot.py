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

async def extract_info(page) -> dict:
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

    first_odd = await page.query_selector('#odds1_value')
    if first_odd:
        winner["first"]["odd"] = await first_odd.text_content()
    second_odd = await page.query_selector('#odds2_value')
    if second_odd:
        winner["second"]["odd"] = await second_odd.text_content()
    first_wager = await page.query_selector('#wagger1')
    if first_wager:
        first_wager_value = await first_wager.text_content()
        winner["first"]["wager"] = first_wager_value.split(' ')[1]
    second_wager = await page.query_selector('#wagger2')
    if second_wager:
        second_wager_value = await second_wager.text_content()
        winner["second"]["wager"] = second_wager_value.split(' ')[1]
    category_element = await page.query_selector('#competition')
    if category_element:
        category_text = await category_element.text_content()
        winner["category"] = category_text.split(' | ')[1]
    first_site_element = await page.query_selector('#site1')
    if first_site_element:
        winner["first"]["site"] = await first_site_element.text_content()
    second_site_element = await page.query_selector('#site2')
    if second_site_element:
        winner["second"]["site"] = await second_site_element.text_content()
    first_name = await page.query_selector('#home-teams')
    second_name = await page.query_selector('#away-team')
    if first_name:
        winner["first"]["name"] = first_name.text_content()
    if second_name:
        winner["second"]["name"] = second_name.text_content()

    return winner

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
    await asyncio.sleep(40)
    # text_to_find = "History"
    # try:
    #     element = await page.wait_for_selector(f"text={text_to_find}", timeout=5000)
    #     if element:
    #         print(f"History entered.")
    #         await element.click()
    #         await asyncio.sleep(3)
    #     else:
    #         print(f"History button not found.")
    # except TimeoutError as error:
    #     print(error)

    while True:
        winner_info = await extract_info(page)
        if winner_info is not None and winner_info != old_winner_info:
            if not bet_time:
                bet_time = True # Trigger action

        await asyncio.sleep(3)  # Polling delay

    # Keep the browser open for further actions or close it
    # await browser.close()

async def login_x3000(page):
    
    await page.goto("https://www.x3000.lv/betting?flowType=gamingOverview#sports-hub/tennis")
    await asyncio.sleep(10)

    # Login
    play_btn = page.locator('body header').locator(f'text=Play')
    play_btn_lv = page.locator('body header').locator(f'text=Spēlēt')
    if await play_btn.is_visible():
        await play_btn.click()
    else:
        await play_btn_lv.click()

    await asyncio.sleep(5)

    login = await page.wait_for_selector(f'text=Pieslēgties ar lietotāja datiem', timeout=8000) # Log in with credentials
    if login:
        await login.click()
    await page.fill('input[name="email"]', "retssrets@gmail.com")
    await page.fill('input[name="password"]', "Upwork123456!")

    login_btn = page.locator('form').locator(f'text=Pieslēgties') # Log In
    await login_btn.click()
    await asyncio.sleep(10)

    unnecessary = page.locator('#flow-content-container path:first-of-type')
    if await unnecessary.is_visible():
        await unnecessary.click()

async def pool_x3000(page):
    global bet_time
    global winner_info
    global old_winner_info
    
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

    await login_x3000(page)
    await pool_x3000(page)
      
async def login_tonybet(page):
    await page.goto("https://tonybet.lv/en/")
    await asyncio.sleep(10)

    login = page.locator(f'text=IELOGOTIES')
    await login.click()
    await page.fill('input[type="email"]', "retssrets@gmail.com")
    await page.fill('input[type="password"]', "Upwork1234!")
    login_btn = page.locator(f'button[type="submit"]')
    await login_btn.click()
    await asyncio.sleep(10)

async def pool_tonybet(page):
    global bet_time
    global winner_info
    global old_winner_info

    await page.goto("https://tonybet.lv/live/tennis")
    await asyncio.sleep(10)

    while True:
        if bet_time:
            bet = True
            if winner_info["first"]["site"] == "tonybet":
                who = "first"
            elif winner_info["second"]["site"] == "tonybet":
                who = "second"
            else:
                bet = False 
            if bet:  
                print ("tonybet entered")
                try:
                    odd_element = page.locator(f"text={winner_info[who]["odd"]}")
                    if await odd_element.is_visible():
                        await odd_element.click()
                        print(f"{odd_element} selected.")
                        await asyncio.sleep(1)

                        # Bet Wager
                        # wager_element = frame.locator("div.mod-KambiBC-betslip").locator("input.mod-KambiBC-stake-input")
                        # await wager_element.fill(winner_info[who]["wager"])
                        # bet_btn = frame.locator("button.mod-KambiBC-betslip__place-bet-btn")
                        # await bet_btn.click()
                        # bet_slip = frame.locator("button.mod-KambiBC-betslip-button--highlighted")
                        # await bet_slip.click()

                    else:
                        print(f"{odd_element} not found.")
                        bet_time = False
                        old_winner_info = winner_info
                except TimeoutError as error:
                    print (error)

                bet_time = False
        await asyncio.sleep(1)   

async def run_tonybet(playwright):
    global bet_time
    global winner_info
    global old_winner_info
    global tennis_category
    
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(locale="en-US")
    page = await context.new_page()

    await login_tonybet(page)
    await pool_tonybet(page)

async def login_spelet(page):
    await page.goto("https://spelet.lv/")
    await asyncio.sleep(10)

    login = page.locator(f'text=Come in')
    await login.click()
    await page.fill('input[name="username"]', "37129227571")
    await page.fill('input[type="password"]', "Upwork1234!")

    login_btn = page.locator(f'button[type="submit"]')
    await login_btn.click()
    await asyncio.sleep(10)

async def pool_spelet(page):
    global bet_time
    global winner_info
    global old_winner_info

    await page.goto("https://spelet.lv/line/tennis")
    await asyncio.sleep(10)

    while True:
        if bet_time:
            bet = True
            if winner_info["first"]["site"] == "spelet":
                who = "first"
            elif winner_info["second"]["site"] == "spelet":
                who = "second"
            else:
                bet = False 
            if bet:  
                print ("Spelet entered")
                try:
                    odd_element = page.locator(f"text={winner_info[who]["odd"]}")
                    if await odd_element.is_visible():
                        await odd_element.click()
                        print(f"{odd_element} selected.")
                        await asyncio.sleep(1)

                        # Bet Wager
                        wager_element = page.locator("#remote-view .coupon-main-tab__content .coupon-amount").locator("input[type='text']")
                        await wager_element.fill(winner_info[who]["wager"])
                        bet_btn = page.locator("#remote-view .coupon-main-tab__content .coupon-buttons").locator('button[type="button"]')
                        await bet_btn.click()
                        
                    else:
                        print(f"{odd_element} not found.")
                        bet_time = False
                        old_winner_info = winner_info
                except TimeoutError as error:
                    print (error)

                bet_time = False
        await asyncio.sleep(1)   

async def run_spelet(playwright):
    global bet_time
    global winner_info
    global old_winner_info
    global tennis_category
    
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(locale="en-US")
    page = await context.new_page()

    await login_spelet(page)
    await pool_spelet(page)

# Main function to run browsers simultaneously
async def main():
    async with async_playwright() as playwright:
        task_main = asyncio.create_task(run_rr(playwright))
        task_x3000 = asyncio.create_task(run_x3000(playwright))
        # task_tonybet = asyncio.create_task(run_tonybet(playwright))
        # task_spelet = asyncio.create_task(run_spelet(playwright))

        # await asyncio.gather(task_main, task_x3000, task_tonybet, task_spelet)
        await asyncio.gather(task_main, task_x3000)

if __name__ == "__main__":
    asyncio.run(main())
