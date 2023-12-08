import json
import keyboard
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import warnings
import os
import sys
import time


def validate_same_site(cookie):
    if "sameSite" not in cookie or cookie["sameSite"] not in ["None", "Lax", "Strict"]:
        cookie["sameSite"] = "None"


def print_and_exit(message, status=1):
    print(message)
    sys.exit(status)


def import_cookies(driver, cookies):
    for cookie in cookies:
        validate_same_site(cookie)
        driver.add_cookie(cookie)


def download_cookies(url):
    response = requests.get(url)
    if response.status_code == 200:
        cookies = json.loads(response.text)
        if not isinstance(cookies, list):
            print_and_exit("Invalid cookie format. Expected a list of cookies.")
        for cookie in cookies:
            validate_same_site(cookie)
        return cookies
    else:
        print_and_exit(f"Failed to download cookies. Status code: {response.status_code}")


def main():
    # Suppress warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="selenium")

    try:
        # Try using Chrome
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        driver.maximize_window()
    except WebDriverException:
        # If Chrome is not available, use Edge as an alternative
        driver = webdriver.Chrome()
        driver.maximize_window()

    # Download cookies from the URL
    cookies = download_cookies('https://cookies.hamo.dev/freepik')
    driver.get('https://www.freepik.com/')
    import_cookies(driver, cookies)
    driver.refresh()

    # Open a new tab with the URL 'hamo.dev'
    driver.execute_script("window.open('https://chrome.google.com/webstore/detail/idm-integration-module/ngpampappnmepgilojfohadhhmbhlaek', '_blank');")
    # Open a new tab with the URL 'hamo.dev'
    driver.execute_script("window.open('https://hamo.dev', '_blank');")

    # Enter the loop after setting up the browser
    while True:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('q'):
            print_and_exit("Quitting", status=0)


if __name__ == "__main__":
    main()
