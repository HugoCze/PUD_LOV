from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, ElementNotInteractableException, StaleElementReferenceException, TimeoutException,ElementClickInterceptedException
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

# chrome_options.headless = True
#Test
chrome_options.headless = False

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(30)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)


driver.get("https://www.pudelek.pl/katarzyna-cichopek-i-maciej-kurzajewski-juz-sa-po-wigilii-w-tym-roku-nieco-wczesniej-zdjecia-6847767886412608a")
comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[2]/div[3]/div/div'
comment = driver.find_element(By.XPATH, comment_xp)
possible_text = comment.get_attribute('innerHTML')
print(possible_text)
# //*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[17]/div
# //*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[17]/div/div[2]
# //*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[7]/div/div[2]