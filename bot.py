import asyncio
from playwright.async_api import async_playwright
import json
import requests
from defines import ( 
    ARBITRAGE_API_LINK, WAGER, X3000_LINK, TONYBET_LINK, SPELET_LINK, COMPETITION_TRANS, 
    COMPETITION_PARSE, TTBET_LINK, UNIBET_LINK
)

bet_time = False
winner_info = None
old_winner_info = None

async def extract_info() -> dict:
    winner: dict = {
        "first": {
            "name": "", "odd": "", "wager": "", "site": "",
        },
        "second": {
            "name": "", "odd": "", "wager": "", "site": "",
        },
        "sport": "",
        "competition": "",
    }
    response = requests.get(ARBITRAGE_API_LINK)
    res = response.json()
    if res:
        data = res[0]
        odd1 = float(data['odds'][0]['odd_value'])
        odd2 = float(data['odds'][1]['odd_value'])
        total_implied_probability = float(data['total_implied_probability'])
        wager1 = WAGER / total_implied_probability / odd1
        wager2 = WAGER / total_implied_probability / odd2
        sport = data['sport']
        competition = data['competition']
        site1 = data['site_names'][0]
        site2 = data['site_names'][1]
        home_name = data['home_team']
        away_name = data['away_team']

        winner["first"]["odd"] = odd1
        winner["second"]["odd"] = odd2
        winner["first"]["wager"] = wager1
        winner["second"]["wager"] = wager2
        winner["sport"] = sport
        winner["competition"] = competition
        winner["first"]["site"] = site1
        winner["second"]["site"] = site2
        winner["first"]["name"] = home_name
        winner["second"]["name"] = away_name

    return winner

async def run_main_thread():
    global bet_time
    global winner_info
    global old_winner_info
    
    await asyncio.sleep(30) # Delay for loading casinos

    while True:
        winner_info = await extract_info()
        if winner_info is not None and winner_info["sport"] != "" and winner_info != old_winner_info:
            if not bet_time:
                print (winner_info)
                bet_time = True # Trigger action

        await asyncio.sleep(1)

async def login_x3000(page):
    await page.goto(X3000_LINK)
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

    deposit_close = page.locator('[id="flow-content-container"]').locator('svg')
    if await deposit_close.is_visible():
        await deposit_close.click()

async def pool_x3000(page):
    global bet_time
    global winner_info
    global old_winner_info

    await page.goto(X3000_LINK)
    await asyncio.sleep(10)

    # Change to English
    language_select = page.locator('[id="headlessui-listbox-button-:R3al36:"]')
    await language_select.scroll_into_view_if_needed()
    await language_select.click()
    English_select = page.locator('[id*="headlessui-listbox-options"]').locator('text=English')
    await English_select.click()
    await asyncio.sleep(10)

    frame_sel = '[src^="/static/betting-clients/kambi/kambi-client.html?language=lv&outcomeID=true#sports-hub/"]'
    frame = page.frame_locator(frame_sel)

    # Show all sports list
    select_sport = frame.locator(f'text=All Sports')
    await select_sport.click()

    while True:
        if bet_time:
            # Select sport
            sport_category = winner_info['sport']
            if sport_category == 'Tennis':
                sport = frame.locator('.KambiBC-navigation-menu__section--sports').locator('.KambiBC-navigation-menu__section-links').locator('li:nth-of-type(3) div')
                await sport.click()

            bet = True
            if winner_info["first"]["site"] == "x3000":
                who = "first"
            elif winner_info["second"]["site"] == "x3000":
                who = "second"
            else:
                bet = False 
            if bet:           
                print ("x3000 entered")
                try:
                    if winner_info['sport'] == 'Tennis':
                        steps = COMPETITION_PARSE["X3000"]["Tennis"][winner_info["competition"]]
                        for step in steps:
                            competition_step = frame.locator(f'text={step}')
                            await competition_step.click()
                        try:
                            odd_element = frame.locator("ul.KambiBC-sandwich-filter__list").locator(f"text={winner_info[who]["odd"]}")
                            if await odd_element.is_visible():
                                await odd_element.click()
                                print(f"{odd_element} selected.")
                                await asyncio.sleep(1)

                                # Bet Wager
                                wager_element = frame.locator("div.mod-KambiBC-betslip").locator("input.mod-KambiBC-stake-input")
                                # await wager_element.fill(winner_info[who]["wager"])
                                await wager_element.fill("0.1")
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
    
    browser = await playwright.chromium.launch(
        headless=False,
    )
    context = await browser.new_context(
        locale="en-US",
        viewport={"width": 1920, "height": 1080},
    )
    with open('x3000_cookies.json', 'r') as f:
        cookies = json.load(f)
    await context.add_cookies(cookies)
    page = await context.new_page()

    await login_x3000(page)
    await pool_x3000(page)
      
async def login_tonybet(page):
    await page.goto(TONYBET_LINK)
    await asyncio.sleep(10)

    login = page.locator(f'text=Log in')
    login_lv = page.locator(f'text=Ielogoties')
    if await login.is_visible():
        await login.click()
    else:
        await login_lv.click()
    await login.click()
    password_provider = page.locator("button[data-test='passwordProviderButton']")
    await password_provider.click()
    await page.fill('input[type="email"]', "retssrets@gmail.com")
    await page.fill('input[type="password"]', "Upwork1234!")
    login_btn = page.locator(f'button[type="submit"]')
    await login_btn.click()
    await asyncio.sleep(10)

async def pool_tonybet(page):
    global bet_time
    global winner_info
    global old_winner_info

    await page.goto(TONYBET_LINK)
    await asyncio.sleep(10)

    while True:
        if bet_time:
            # Select sport
            sport_category = winner_info['sport']
            if sport_category == 'Tennis':
                sport = page.locator(f'text=Teniss')
                await sport.click()

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
    
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(
        locale="en-US",
        viewport={"width": 1920, "height": 1080},
    )
    page = await context.new_page()

    await login_tonybet(page)
    await pool_tonybet(page)

async def login_spelet(page):
    await page.goto(SPELET_LINK)
    await asyncio.sleep(10)

    login = page.locator('header').locator(f'text=Come in')
    login_lv = page.locator('header').locator(f'text=Ienākt')
    if await login.is_visible():
        await login.click()
    else:
        await login_lv.click()
    await asyncio.sleep(2)
    await page.fill('input[name="username"]', "37129227571")
    await page.fill('input[type="password"]', "Upwork1234!")

    login_btn = page.locator(f'button[type="submit"]')
    await login_btn.click()
    await asyncio.sleep(10)

async def pool_spelet(page):
    global bet_time
    global winner_info
    global old_winner_info

    await page.goto(SPELET_LINK)
    await asyncio.sleep(10)

    # Change to English
    language_select = page.locator('header button.css-selt3s')
    await language_select.click()
    English_select = page.locator('header ul li:first-of-type span').click()
    await English_select.click()
    await asyncio.sleep(3)

    while True:
        if bet_time:
            # Select sport
            sport_category = winner_info['sport']
            if sport_category == 'Tennis':
                sport = page.locator('.nav-sport-menu-app').locator('text=Tennis')
                await sport.click()

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
                        # await wager_element.fill(winner_info[who]["wager"])
                        await wager_element.fill("0.1")
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
    
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(
        locale="en-US",
        viewport={"width": 1920, "height": 1080},
    )
    page = await context.new_page()

    await login_spelet(page)
    await pool_spelet(page)

async def login_22bet(page):
    await page.goto(TTBET_LINK)
    await asyncio.sleep(10)

    login = page.locator('#curLoginForm').locator('text=Log in')
    await login.click()
    await asyncio.sleep(2)
    email = page.locator('.loginDropTop_div form').locator('input[type="text"]')
    await page.fill(email, "37129227571")
    password = page.locator('.loginDropTop_div form').locator('input[type="password"]')
    await page.fill(password, "Upwork1234!")

    login_btn = page.locator('.loginDropTop_div form').locator('text=Log in')
    await login_btn.click()
    await asyncio.sleep(10)

async def pool_22bet(page):
    global bet_time
    global winner_info
    global old_winner_info

    await page.goto(TTBET_LINK)
    await asyncio.sleep(10)

    sport_select = page.locator('#sports_left').locator('text=Tennis')
    await sport_select.click()

    while True:
        if bet_time:
            bet = True
            if winner_info["first"]["site"] == "22bet":
                who = "first"
            elif winner_info["second"]["site"] == "22bet":
                who = "second"
            else:
                bet = False 
            if bet:  
                print ("22bet entered")
                try:
                    odd_element = page.locator(f"text={winner_info[who]["odd"]}")
                    if await odd_element.is_visible():
                        await odd_element.click()
                        print(f"{odd_element} selected.")
                        await asyncio.sleep(1)

                        # Bet Wager
                        wager_element = page.locator("#remote-view .coupon-main-tab__content .coupon-amount").locator("input[type='text']")
                        # await wager_element.fill(winner_info[who]["wager"])
                        await wager_element.fill('0.1')
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

async def run_22bet(playwright):
    global bet_time
    global winner_info
    global old_winner_info
    
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(
        locale="en-US",
        viewport={"width": 1920, "height": 1080},
    )
    page = await context.new_page()

    await login_22bet(page)
    await pool_22bet(page)

# Main function to run browsers simultaneously
async def main():
    async with async_playwright() as playwright:
        task_main = asyncio.create_task(run_main_thread())
        # task_x3000 = asyncio.create_task(run_x3000(playwright))
        # task_tonybet = asyncio.create_task(run_tonybet(playwright))
        task_spelet = asyncio.create_task(run_spelet(playwright))

        # await asyncio.gather(task_main, task_x3000, task_tonybet, task_spelet)
        await asyncio.gather(task_main, task_tonybet)
        task_x3000 = asyncio.create_task(run_x3000(playwright))
        # task_tonybet = asyncio.create_task(run_tonybet(playwright))
        # task_spelet = asyncio.create_task(run_spelet(playwright))

        # await asyncio.gather(task_main, task_x3000, task_tonybet, task_spelet)
        await asyncio.gather(task_main, task_x3000)

if __name__ == "__main__":
    asyncio.run(main())
