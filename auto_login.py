# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00701ED78EB919EE5B611C4210FD544241B8DF01065B4BF38FE5D140D12B4FF76C4DAA4867E5EE06A2CC607C00AD24D006166C7567F0F985C2FD29561D03116B3885B251799982C317798A4D9B406895704F15879B56C695D95293264BBCC241EE30573CCE6C37475B0443FA9EAC84140FAB81350E2A65DB15349B54C97CC933EF56BC34C01E80E993AA977F01B44184A6334A9E7E2B120EE50D0590793A444B2EBFD190C5C203B1A5C96DD565ECF518A25FAA3BDA5F68E134C7E2ED5D95E8EC9374D14E0CFCE13D6624E13FD0BF574054FB35D1CDAD75648C756B8580255D6FBFEEAFF440D9CE0CA6BC5B2498B6E3FE25FD044FC257A785606D2B5CF1D2AE06F49B39B84F3309A0C84CC8AF8CFB95258930C48BC148F575182721B29600774F98CEE8E6E1BF842F7DF667950CC34DFA919C382ABC8287BA666143AEA14B1BDB756C65620A7FA6728568E921D77DA386AE1B90CC9326798BE66C38393D802420928E3303380E87BD705B82A0F6BB57D061AFBFFF60EC82F542F8349B0F8B48CE29852CE9861266D366C31665E39BE35762

"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
