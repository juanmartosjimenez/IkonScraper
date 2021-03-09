from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from random import randint


def get_user_data():
    user_email = input("Enter email:\n")
    user_date = input("Enter date in the form day/month/year for example 27/02/2021:\n")
    user_datetime = datetime.strptime(user_date, '%d/%m/%Y')
    format_date = user_datetime.strftime('%a %b %d %Y')
    today = datetime.now()
    if user_datetime < today:
        raise Exception("Input date is too small")
    user_password = input("Enter password:\n")
    mountain = input("Enter mountain:\n")
    return user_email, user_password, format_date, mountain


def click_button(driver, text):
    xpath = "//button[@class][@data-test='button']/span[text()='{}']".format(text)
    driver.find_element_by_xpath(xpath).click()


def run_scrape():
    user_email, user_password, format_date, mountain = get_user_data()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    driver = webdriver.Chrome(executable_path='/home/juanmartos/Downloads/chromedriver', options= chrome_options)
    driver.get('https://account.ikonpass.com/en/login')

    email = driver.find_element_by_id('email')
    email.clear()
    email.send_keys(user_email)
    password = driver.find_element_by_id('sign-in-password')
    password.clear()
    password.send_keys(user_password)
    password.send_keys(Keys.ENTER)

    time.sleep(2)
    reserve = driver.find_element_by_xpath('//a[@href="/myaccount/add-reservations/"]')
    reserve.click()
    while True:
        time.sleep(2)
        search_bar = driver.find_element_by_xpath('//input[@aria-controls="react-autowhatever-resort-picker"]')
        search_bar.send_keys(mountain)
        loon = driver.find_element_by_id('react-autowhatever-resort-picker-section-0-item-0')
        loon.click()
        time.sleep(1)
        click_button(driver, "Continue")
        time.sleep(5)
        target_day = driver.find_element_by_xpath('//*[@aria-label="' + format_date + '"]')
        time.sleep(2)
        target_html = target_day.get_attribute('outerHTML')
        if "unavailable" in target_html:
            print("no booking, trying again")
            driver.refresh()
            time.sleep(randint(300, 500))
        else:
            print("there is a booking")
            target_day.click()
            time.sleep(1)
            click_button(driver, "Save")
            time.sleep(2)
            click_button(driver, "Continue to Confirm")
            time.sleep(1)
            driver.find_element_by_css_selector("label.amp-checkbox-input").click()
            click_button(driver, "Confirm Reservations")
            break


if __name__ == '__main__':
    run_scrape()
