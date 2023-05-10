from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
import auth

EMAIL = auth.EMAIL
PASS = auth.PASS

Search_URL = auth.SEARCH_URL

# Driver Set Up
chrome_driver_path = r"C:\Users\Aleks\PycharmProjects\pythonProject\chromedriver_win32\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=chrome_options)


def log_in():
    time.sleep(2)
    sign_in = driver.find_element(By.XPATH, "/html/body/div[3]/a[1]")
    sign_in.click()
    time.sleep(1)
    email_field = driver.find_element(By.NAME, "session_key")
    email_field.send_keys(EMAIL)
    pass_field = driver.find_element(By.NAME, "session_password")
    pass_field.send_keys(PASS)
    confirm_sign_in = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
    confirm_sign_in.click()


def save_and_follow_job():
    time.sleep(1)
    save_job = driver.find_element(By.CSS_SELECTOR,
                                   ".jobs-save-button.artdeco-button.artdeco-button--3.artdeco-button--secondary")
    save_job.click()

    # scroll down
    overflow_bar = driver.find_element(By.CLASS_NAME, "overflow-x-hidden")
    scroll_origin = ScrollOrigin.from_element(overflow_bar)
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, 12000).perform()

    try:
        follow_job = driver.find_element(By.CSS_SELECTOR, ".follow.artdeco-button.artdeco-button--secondary.ml5")
        follow_job.click()
    except NoSuchElementException: # If no follow button, skip
        pass


driver.get(Search_URL)
log_in()


def scroll_jobs():
    job_bar = driver.find_element(By.CLASS_NAME, "scaffold-layout__list")
    scroll_origin = ScrollOrigin.from_element(job_bar)
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, 120).perform()


all_jobs_on_page = driver.find_elements(By.CLASS_NAME,
                                        "job-card-list__title")

job_list = [job for job in all_jobs_on_page]

saved_jobs = 0
for job in job_list:
    job.click()
    time.sleep(2)
    try:
        save_and_follow_job()
        saved_jobs += 1
    except ElementClickInterceptedException:  # Avoid popups
        pass
    time.sleep(1)
    scroll_jobs()

print(f"I saved {saved_jobs} jobs!")
driver.quit()
