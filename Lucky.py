import asyncio
from telethon import TelegramClient, events
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pickle
from datetime import datetime
from selenium.webdriver.chrome.options import Options
# create Chromeoptions instance

print("go", flush=True)
options = webdriver.ChromeOptions()

# adding argument to disable the AutomationControlled flag
options.add_argument("--disable-blink-features=AutomationControlled")

# exclude the collection of enable-automation switches
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# turn-off userAutomationExtension
options.add_experimental_option("useAutomationExtension", False)

options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# setting the driver path and requesting a page
driver = webdriver.Chrome(options=options)

driver.get("https://1woahn.com/?sub1=20250508-1337-1283-86d6-c3f070abf2d1&sub2=2210_1_win_net_in_reg")
print("platform opened", flush=True)
time.sleep(180)
driver.save_screenshot("page.png")
try:
    # Checking if the main page is available before loading login cookies
    login = WebDriverWait(driver, 3000).until(
        EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Login']"))
    )

except TimeoutException:
    print("Element not found")

else:
    # Loading login cookies
    with open("cookies.pkl", "rb") as f:
    	cookies = pickle.load(f)

    for cookie in cookies:
    	driver.add_cookie(cookie)

    driver.refresh()


    try:
        # Clicking lucky jet
        wait = WebDriverWait(driver, 3000)
        lucky_jet = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[6]//div[1]//img[1]"))
        )

    except TimeoutException:
        print("Element not found")

    else:
        lucky_jet.click()
        # switching to iframe
        try:
            wait = WebDriverWait(driver, 3000)
            iframe = wait.until(
                EC.presence_of_element_located((By.XPATH, "//iframe[@class='CasinoGameFrame_root_V6yFR CasinoGame_game_JenRc']"))
            )

        except TimeoutException:
            print("Element not found")

        else:
            driver.switch_to.frame(iframe)



def process_stake(results, stake):
    if results == "won":
        return 100
    elif results == "lose":
        return 2 * stake



def play_lucky_jet(time, stake, odds):
    """
	enter stake, odds, set auto withdrawal and place bet
	"""
    print(f"Bet will be placed at {time}")
    try:
        odds = float(odds)
    except ValueError:
        print("odds is not numeric")

    else:
        if stake < 1000:
            # Entering stake
            try:
                wait = WebDriverWait(driver, 3000)
                stake_button = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sc-dISpDn"))
                )
            except TimeoutException:
                print("Element not found")
            else:
                stake_button.send_keys(Keys.CONTROL, Keys.BACKSPACE)
                stake_button.send_keys(stake)

                # Enter odds
                try:
                    wait = WebDriverWait(driver, 300)
                    odds_button = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "sc-ggqIjW"))
                    )
                except TimeoutException:
                    print("Element not found")
                else:
                    odds_button.send_keys(Keys.CONTROL, Keys.BACKSPACE)
                    odds_button.send_keys(odds)

                    # checking autowithdrawal checkbox
                    try:
                        wait = WebDriverWait(driver, 300)
                        auto_withdrawal_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//body/div[@id='root']/div[@id='mobile']/div[@class='sc-bizigk dKNoSI']/div[@class='sc-hyBbbR hfulpO sc-gAjuZT gRhbmO']/div[1]/div[1]/div[2]/div[1]")) 
                        )
                    except TimeoutException:
                        print("Element not found")

                    else:
                        if auto_withdrawal_button.get_attribute("value") == "false":
                            auto_withdrawal_button.click()

                        # placing bet
                        try:
                            wait = WebDriverWait(driver, 300)
                            bet_button = wait.until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "sc-DWsrX")) 
                        )

                        except TimeoutException:
                            print("Element not found")

                        else:
                            while True:
                                if (datetime.now().hour, datetime.now().minute) >= time:
                                    bet_button.click()
                                    print("Bet placed")
                                    break


                            return "stake normal"
        else:
            return "stake exceeds"


stake = 100


# Replace with your credentials
api_id = "24965125"
api_hash = "6ba1da2dd8c4a17c41fc2774757f0d1d"
phone_number = "+265998604550"

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats="https://t.me/lucky_jet_test"))
async def new_message_listener(event):
    global stake
    signal = ""
    time_minutes = 0
    time_hours = 0
    odds = ""

    message = event.message.message
    m = message.replace(" ", "")
    if "Wewon" in m:
        signal = m

    elif "IfIhaven'tmentionedyourcountry" in m:
        standard_minutes = ""
        signal = m
        time_index = m.find("minuteofyourtime")	
        odds_index = m.find("Withdrawalat")
        minutes = (m[(time_index - 4):time_index-2])

        for i in minutes:
            if i.isdigit():
                standard_minutes += i

        if standard_minutes.startswith("0"):
            try:
                time_minutes = int(standard_minutes[1:]) 

            except ValueError:
                print("minutes are not numeric")
        
        else:
            try:
                time_minutes = int(standard_minutes)

            except ValueError:
                print("minutes are not numeric")

        try:
            if datetime.now().minute > (time_minutes):
                time_hours = (datetime.now().hour + 1)

            else:
                time_hours = datetime.now().hour

        except TypeError:
            print("int can't be compared with str")

        exit_odds = (m[(odds_index + 12):(odds_index + 15)])
        for i in exit_odds:
            if i.isdigit() or i == ".":
                odds += i

    if signal:
        if "IfIhaven'tmentionedyourcountry" in signal:
            result = play_lucky_jet(time=(time_hours, time_minutes), stake=stake, odds=odds)
            if result == "stake normal":
                stake = process_stake("lose", stake)

            elif result == "stake exceeds":
                stake = process_stake("won", stake)
                

        elif "Wewon" in signal:
            stake = process_stake("won", stake)


async def main():
    await client.start(phone=phone_number)
    print("Listening for new messages...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())


