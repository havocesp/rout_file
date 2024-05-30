from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://ru.bitcoincam.org/login'
user_email = "rworkkkkk1"
user_password = "00001111Rw"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.add_extension(ext)

# proxy_address = "45.130.254.133"
# proxy_login = 'K0nENe'
# proxy_password = 'uw7RQ3'
# proxy_port = 8000

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if not("2Cap" in driver.title):
            break


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    actions = ActionChains(driver)
    driver.maximize_window()
    api_connect(driver)
    driver.get(url)

    try:
        wait_visibility(driver, 50, '//*[@id="login_login_or_email"]')
        input_data(driver, 10, '//*[@id="login_login_or_email"]', user_email)
        input_data(driver, 10, '//*[@id="login_password"]', user_password)
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX ')

    try:
        wait_visibility(driver, 30, '//button[@type="submit"]')
        click(driver, 10, '//button[@type="submit"]')
    except Exception as e:
        print(f'ERROR CLICK LOG BUTTON \n{e}')

    try:
        wait_visibility(driver, 30, '//a[@class="dropdown-link"]')
        click(driver, 10, '//a[@class="dropdown-link"]')
        click(driver, 20, '//*[@id="body"]/div[2]/div/header/div/div/nav[2]/div[3]/div/div/ul/li[1]/button')
    except Exception as e:
        print(f'ERROR APPEND TOKENS \n{e}')

    try:
        wait_visibility(driver, 30, '//li[@class="cryptocoin"]')
        click(driver, 10, '//li[@class="cryptocoin"]')
        click(driver, 10, '//*[@id="body"]/div[2]/div[1]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/ul/li[1]')
        click(driver, 10, '//*[@id="continue_button_id"]')
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')

    wait_visibility(driver, 30, '//iframe[@class="tokens-wizard-billing-iframe"]')
    find_frame = driver.find_element(By.XPATH, '//iframe[@class="tokens-wizard-billing-iframe"]')
    driver.switch_to.frame(find_frame)

    try:
        wait_visibility(driver, 60, '//img[@alt="USDT"]')
        js_click(driver, 10, '//img[@alt="USDT"]')
        click(driver, 10, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
        click(driver, 30, '//img[@alt="Tron"]')
        click(driver, 10, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
    except Exception as e:
        print(f'error choose trc20 \n{e}')

    try:
        wait_visibility(driver, 50, '//input[@name="email"]')
        input_data(driver, 10, '//input[@name="email"]', "kiracase34@gmail.com")
        sleep(1.5)
        click(driver, 10 , '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button')
    except Exception as e:
        print(f'ERROR INPUT EMAIL \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div')
            amount = amount_elem.text

            return {
                "address": address.replace("\n", '').replace("Copy", '').replace(" ", ''),
                "amount": amount.replace("USDT", '').replace("\n", '').replace("Copy", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
