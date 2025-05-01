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
    browser.add_cookie({"name": "MUSIC_U", "value": "005BF5F22D0AFF644C9D371C84B234B2ADBBFFF2982B662DA5F088F35EAD968D0148F6469FFAE2948F2F40B12777C34D12ECF37607C2637FFDD9330021CE842CE55FFA7E8B12D033388583524A7604FF1476EB736BF5FFDA355FA2F03F96298F4FD70CA265E9670368906EBE89AAF5AB563CFAD78BC508AC02520B4933FB900B2121D765E16BE4E56D22680110ACC8BA61EBC87F1D309C2DFD455D16CFAFBB0B22F30A2DF3F7B4CE3120CA4904C6631F8EEDD39A502EE9583FECC83E3A313151C55627974280BBF1B1F7F75D43CCB8CE1415F77A5AD28FCDD5F8C25EB900151A512B321B8B9D25D57327B70C4517E7DABD96D94F520CB670997FB5E0C0186D82E89E0072499F64DD9DCCCD280BE00FDB85E8CD08317CC6FABBE97C130B2D1B20A4F17967B84DDD5DC3B1C5D2E6227EDCD2D82B187BCE80684C4651C5F092778207BCD3F311ABF18C4BD3FE04F5CFC711275652D99B21213F8724C3B8B1503F2D3C
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
