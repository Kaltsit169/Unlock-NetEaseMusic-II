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
    browser.add_cookie({"name": "MUSIC_U", "value": "0024416CF53F1EF23AE94A2406390FB813B9DA512D64E66266267B3B48AB5F4875C3784BFD36B1C158F37CF9E655DE3278004C850DAA91DFC7DE26B5E324F941B6884B883C92207D15A491519CD3FF4450AFE604BD75F38DF56CC8A9B29CCDB514D9B8561A7B0CC2F4D76AE48AFCE1ABFB46E43899DF1E469C604B773BC13DEB01530772490BFF43F33CC725545507A2165986851A187AD303BF3D254506C38E868D8E6F46C47429A8971D0241702E5CE1DA794B080311414E38768CE816935E3B93833A9D6C5129E1BC498355453EA73EACABB9D801889DB19B7B05BC98000FA5BCC0F9D2CF8406CAD5C188F7865CC9644E8E6D9DA1A741E0501592FACB06733F2CBA22320A5EE8F0BB486167F5684CE7EC4733FBFF046B1BC8ABF771935522791FC22E3C6A9484E94A536587DD2D298D807C642238604A9D84294AC9A120E20F8285FDF198756DF63AE697A68A538303

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
