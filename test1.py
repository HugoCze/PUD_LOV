from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, TimeoutException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time 

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--disable-features=DefaultPassthroughCommandDecoder")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

PATH = r"C:\Users\Hugo\PartyBot\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=chrome_options)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException, TimeoutException, ElementClickInterceptedException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)

print("start")
start_time = time.time()
driver.get("https://www.pudelek.pl/robert-lewandowski-jednak-komentuje-30-milionow-premii-od-morawieckiego-to-sie-wszystko-dzieje-poza-pilkarzami-ktorzy-razem-z-kibicami-sa-ofiarami-6842487736318496a")
TermsAndConditions = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/button[2]")))
TermsAndConditions.click()
print("Terms accepted")

h1 = driver.find_element(By.TAG_NAME, 'h1')
h1_text = h1.get_attribute('innerHTML')
print(h1_text)


end_time = time.time()
total_time = end_time - start_time
print("Time of looking the comment is equal to: ", total_time)

# Test notes: 

# on pc
# Time of looking the comment is equal to:  1.8768177032470703