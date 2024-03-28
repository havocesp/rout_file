from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS
#33775511l
url = 'https://pvsz.store/login'
user_email = "rwork875@gmail.com"
user_password = "33775511l"
site_key = '6LdqzaEpAAAAAJlGjpcK26RTleOxreHtk1f29UJ_'

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def captcha_solver():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(site_key)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


def login(driver):
    driver.get(url)
    driver.maximize_window()

    result_captcha = captcha_solver()
    driver.implicitly_wait(7.5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.XPATH, '//*[@id="input-01"]')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="input-02"]')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'recaptcha-submit')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    while True:
        try:
            driver.implicitly_wait(4.5)
            find_error = driver.find_element(By.CSS_SELECTOR, 'div.wrap > div.content_block > div > div.silver-bk > p > b').text

            if "Ошибка" in find_error:

                result_captcha = captcha_solver()

                driver.implicitly_wait(7.5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)
                sleep(2.5)

                driver.implicitly_wait(50)
                input_email = driver.find_element(By.XPATH, '//*[@id="input-01"]')
                input_email.clear()
                input_email.send_keys(user_email)

                driver.implicitly_wait(10)
                input_password = driver.find_element(By.XPATH, '//*[@id="input-02"]')
                input_password.clear()
                input_password.send_keys(user_password)

                driver.implicitly_wait(10)
                login_button = driver.find_element(By.ID, 'recaptcha-submit')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", login_button)
            else:
                break
        except:
            break
    driver.get('https://pvsz.store/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(40)
            input_amoun = driver.find_element(By.ID, 'val1')
            input_amoun.clear()
            input_amoun.send_keys("550")

            driver.implicitly_wait(30)
            choose_freekassa = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/form[1]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_freekassa)
        except Exception as e:
            print(f"ERROR CHOOSE FREEKASSA \n{e}")

        driver.refresh()
        sleep(2)

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(40)
            input_email = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            print(f"SUBMIT ERROR \n{e}")

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
