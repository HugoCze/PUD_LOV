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
driver.set_page_load_timeout(5)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)

counter = 0

class Search_And_Like:
    
    def get_homePage(self, path, comment):
        homepage = "https://www.pudelek.pl/" + path
        try:
            driver.get(homepage)
            print("got home page")
            self.terms(path, comment)
        except ignored_exceptions:
            print(f"Search_And_Like - failed to get homePage - refresh and terms", file=open('SAL_Final.txt','a'))
            self.terms(path, comment)
            
    def terms(self, path, comment):
        print("Terms and conditions starting...", file=open('SAL_Final.txt','a'))
        try:
            self.click("/html/body/div[3]/div/div[2]/div[3]/div/button[2]", "clicked accept terms button")
            self.search_comment(path, comment)
        except ignored_exceptions:
            print(f"terms - Terms and conditions not found - searching comment", file=open('SAL_Final.txt','a'))
            self.search_comment(path, comment)

    def search_comment(self, path, comment):
        print("search_comment - searching for comment", file=open('SAL_Final.txt','a'))
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                if comment_text.strip() == comment.strip():
                    print(f"Did find the comment: {comment_text}", file=open('SAL_Final.txt','a'))
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print("got the like butt xpath", file=open('SAL_Final.txt','a'))
                    self.click(like_button_xp, "search_comment - called click like button from comment searching")
                    break
            except ignored_exceptions:
                pass
        else:
            self.search_next(path, comment)
            
    def search_next(self, path, comment):
        print("search_next - searching the next button", file=open('SAL_Final.txt','a'))
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                        print("search_next - got the next button", file=open('SAL_Final.txt','a'))
                        self.click(next_button_xp, "search_next - clicked the next button")
                        self.search_comment(path, comment)
                        return
                except ignored_exceptions:
                    pass

    def click(self, xpath, call_indication):
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        print(f"click - clicking given xpath: {xpath} - {call_indication}", file=open('SAL_Final.txt','a'))

    def main(self, path, comment):
        print("main - here we are at main. Calling get_homePage", file=open('SAL_Final.txt','a'))
        self.get_homePage(path, comment)

SAL = Search_And_Like()
while True:
    counter += 1 
    start_time = time.time()
    SAL.main("harry-udzielil-kolejnego-wywiadu-promuje-autobiografie-w-ktorej-uderzy-w-ksiecia-williama-ich-relacje-wisza-na-wlosku-6851223058971456a", 'Puszczający się na prawo i lewo William stale zdradza wystrzerzoną Kate, która najwyraźniej popadła z tego powodu w anoreksję. A Karol sprzedaje gazetom wszystkich po kolei, żeby wykreować w mediach wizerunek Camilli jako świętej krowy. Nic dziwnego, że Harry i Meghan postanowili zwiać z tej rąbniętej rodzinki.')
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time of looking the comment is equal to: {total_time} ",  file=open('SAL_Final.txt','a'))
    print(f"Counter: {counter} ",  file=open('SAL_Final.txt','a'))