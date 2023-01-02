import asyncio
import pprint
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

my_printer = pprint.PrettyPrinter(width=20)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-features=DefaultPassthroughCommandDecoder")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

chrome_options.headless = True
# Test
# chrome_options.headless = False

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(15)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)


class Search_And_Like():

    def get_homePage(self, path, comment):
        homepage = "https://www.pudelek.pl/" + path
        print("Entering homepage")
        try:
            driver.get(homepage)
        except ignored_exceptions:
            try:
                driver.get(homepage)
            except ignored_exceptions:
                print("starting again")
                self.get_homePage(path, comment)
        print("passed starting - running terms")
        self.terms_and_conditions(path, comment)
    
    def terms_and_conditions(self, path, comment):
        print("Terms accepted")
        try:
            TermsAndConditions = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/button[2]")))
            TermsAndConditions.click()
        except ignored_exceptions:
            print("Terms and conditions not found")
            self.search(path, comment)

    def search(self, path, comment):
        print("searching for comment")
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                # print(f"def search comment text: {comment_text}") #; our type {comment}")
                if comment_text.strip() == comment.strip():
                    print("got the cooomment")
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print("got the like butt")
                    # self.click_it(like_button_xp)
                    print(f"def click: used xpath: {like_button_xp}\n")
                    button_location = driver.find_element(By.XPATH, like_button_xp)
                    driver.execute_script("arguments[0].click();", button_location)
                    print("def click: clicked\n")
                    # print("click_it")
                    break
                    # SAL.get_homePage(path, comment)
            except ignored_exceptions:
                pass
        else:
            print("search for the next page button")
            for i in range(19, 36):
                for j in range(2,4):
                    try:
                        next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                        button_action = driver.find_element(By.XPATH, next_button_xp)
                        button_possible_text = button_action.get_attribute('innerHTML')
                        if button_possible_text == "Następna strona":
                            # print(f"next page button text: {button_possible_text} ; next page button xp {next_button_xp}")
                            print("got the next button")
                            # self.click_it(next_button_xp)
                            print(f"def click: used xpath: {next_button_xp}\n")
                            button_location = driver.find_element(By.XPATH, next_button_xp)
                            driver.execute_script("arguments[0].click();", button_location)
                            print("def click: clicked\n")
                            # print("click_it")
                            self.search(path, comment)
                    except ignored_exceptions:
                        pass

    # def click_it(self, xpath):
    #     print(f"def click: used xpath: {xpath}\n")
    #     button_location = driver.find_element(By.XPATH, xpath)
    #     driver.execute_script("arguments[0].click();", button_location)
    #     print("def click: clicked\n")
    
    # def main(self, path, comment):
    #     SAL.get_homePage(path, comment)
    #     SAL.search(path, comment)
    #     print("def main - finished working", file=open('SAL_LogFile.txt','a'))


SAL = Search_And_Like()

while True:
    start_time = time.time()
    SAL.get_homePage("katarzyna-cichopek-i-maciej-kurzajewski-juz-sa-po-wigilii-w-tym-roku-nieco-wczesniej-zdjecia-6847767886412608a", "Pani Cichochłopek bardzo ładny stół w tym roku! Gratuluję!")
    SAL.search("katarzyna-cichopek-i-maciej-kurzajewski-juz-sa-po-wigilii-w-tym-roku-nieco-wczesniej-zdjecia-6847767886412608a", "Pani Cichochłopek bardzo ładny stół w tym roku! Gratuluję!")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time of looking the comment is equal to: {total_time} ",  file=open('SAL_LogFile.txt','a'))
    
