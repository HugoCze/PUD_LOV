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
import datetime
date_time = datetime.datetime.now()


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

class Search_And_Like:
    
    def get_homePage(self, path, comment):
        homepage = "https://www.pudelek.pl/" + path
        try:
            driver.get(homepage)
            print("got home page")
            self.terms(path, comment)
        except ignored_exceptions:
            print(f"{date_time} - failed to get homePage - closing driver", file=open('SAL_Final.txt','a'))
            # self.main(path, comment)
            # driver.close()
            driver.refresh()
            self.get_homePage(path, comment)
    
    def terms(self, path, comment):
        print("Terms")
        try:
            TermsAndConditions = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/button[2]")))
            TermsAndConditions.click()
        except ignored_exceptions:
            print(f"{date_time} -Terms and conditions not found - searching comment", file=open('SAL_Final.txt','a'))
            self.search_comment(path, comment)

    def search_comment(self, path, comment):
        print("searching for comment")
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                # try:
                #     print(f"def search comment text: {comment_text}", file=open('SAL_Final.txt','a')) #; our type {comment}")
                # except UnicodeEncodeError:
                #     pass
                if comment_text.strip() == comment.strip():
                    print(f"got the cooomment: {comment_text}", file=open('SAL_Final.txt','a'))
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print("got the like butt")
                    # self.click_it(like_button_xp)
                    print(f"def click: used xpath: {like_button_xp}", file=open('SAL_Final.txt','a'))
                    button_location = driver.find_element(By.XPATH, like_button_xp)
                    driver.execute_script("arguments[0].click();", button_location)
                    print("def click: clicked", file=open('SAL_Final.txt','a'))
                    # print("click_it")
                    break
            except ignored_exceptions:
                pass
        else:
            self.search_next(path, comment)
            
    def search_next(self, path, comment):
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
                        self.search_comment(path, comment)
                except ignored_exceptions:
                    pass

    # def click(self,)

    def main(self, path, comment):
        self.get_homePage(path, comment)
        self.search_comment(path, comment)

SAL = Search_And_Like()
while True: 
    start_time = time.time()
    SAL.main("marcin-prokop-drwi-z-tomasza-kammela-i-jego-sylwestrowych-zapewnien-foto-6851161590766400a", "Lewaki to najwięksi hipokryci i hejterzy")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time of looking the comment is equal to: {total_time} ",  file=open('SAL_Final.txt','a'))