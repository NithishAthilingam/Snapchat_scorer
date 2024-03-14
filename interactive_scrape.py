#%%
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#%%
# Load
person = 'Nithish Athilingam'
with open('credentials.json', 'r') as file:
    credentials = json.load(file)
with open('selectors.json', 'r') as file:
    selectors = json.load(file)

#%%
# Initialize WebDriver
driver = webdriver.Chrome()
# Navigate to the initial page
driver.get("https://www.snapchat.com/")

#%%
# Perform login
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['loginButton']))).click()
WebDriverWait(driver, 10).until(EC.new_window_is_opened)
driver.switch_to.window(driver.window_handles[1])

#%%
max_retries = 3
attempts = 0
while attempts < max_retries:
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "accountIdentifier"))).send_keys(credentials['username'])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['nextButton']))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(credentials['password'])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['nextButton']))).click()
        break
    except Exception as e:
        print(f"Attempt {attempts + 1} failed, refreshing page and retrying...")
        driver.refresh()
        time.sleep(random.uniform(1, 3))
        attempts += 1

if attempts == max_retries:
    print("Failed to complete the process after several retries.")

#%%
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['closeButton']))).click()

#%%
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['cameraButton']))).click()

#%%
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['gotItButton']))).click()

# Permissions might need manual handling or browser profile configuration
#%%
while True:
    try:
        driver.find_element(By.CSS_SELECTOR, selectors['captureButton']).click()
    except Exception as e:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['cameraButton']))).click()
        driver.find_element(By.CSS_SELECTOR, selectors['captureButton']).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['sendToButton']))).click()
    person_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '{}')]".format(person))))
    person_element.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['submitButtonLoop']))).click()
    time.sleep(random.uniform(1, 3))

# %%