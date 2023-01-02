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

class MappAndLike:

    next_button_list = []
    page_search = 1
    page_mapped = 1
    likeButton_xp, commentXPATH, commentTEXT = "", "", ""

    def choose_option(self, path, comment):
        if self.likeButton_xp == "":
            print(f"choose_option - like button is empty going with search", file=open('mapped_log.txt','a'))
            self.search_comment(path, comment)
        elif self.likeButton_xp != "":
            print(f"choose_option - like button is not empty going with mapped", file=open('mapped_log.txt','a'))
            self.mapped(path, comment)

    def get_homePage(self, path, comment):
        homepage = "https://www.pudelek.pl/" + path
        try:
            driver.get(homepage)
        except ignored_exceptions:
            print("def getHomePage - Exception on getting the home page", file=open('mapped_log.txt','a'))
        try:
            self.click("/html/body/div[3]/div/div[2]/div[3]/div/button[2]", "def terms - clicking the accept terms button from terms def")
            print("def getHomePage - No Exception on clicking terms - starting choose_option ", file=open('mapped_log.txt','a'))
            self.choose_option(path, comment)
        except ignored_exceptions:
            print("def getHomePage - Exception on clicking terms - starting choose_option", file=open('mapped_log.txt','a'))
            self.choose_option(path, comment)

    def search_comment(self, path, comment):
        print("def search_comment - searching for comment", file=open('mapped_log.txt','a'))
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                if comment_text.strip() == comment.strip():
                    
                    print("def search_comment - got the comment", file=open('mapped_log.txt','a'))
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    self.click(like_button_xp, "called from def search_comment on like button")
                    self.commentTEXT = comment_text
                    self.commentXPATH = possible_comment_xp
                    self.likeButton_xp = like_button_xp
                    return
            except ignored_exceptions:
                pass
        else:
            print("def search_comment - calling for search_next def", file=open('mapped_log.txt','a'))
            self.search_next(path, comment)
            
    def search_next(self, path, comment):
        print("search_next - search for the next page button", file=open('mapped_log.txt','a'))
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                        self.click(next_button_xp, "called from def search next on next button")
                        self.page_search += 1
                        self.search_comment(path, comment)
                except ignored_exceptions:
                    pass

    def search_next_at_mapped_loop(self, path, comment):
        print("search_next_at_mapped_loop - search for the next page button", file=open('mapped_log.txt','a'))
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                       self.page_mapped += 1
                       self.click(next_button_xp, "search_next_at_mapped_loop - clicked on next mapped search button ")
                       time.sleep(1)
                       self.mapped(path, comment)
                except ignored_exceptions:
                    pass

    def mapped(self, path, comment):
        print(f"def mapped - starting mapped def", file=open('mapped_log.txt','a'))
        print(f"Page search: {self.page_search}", file=open('mapped_log.txt','a'))
        print(f"Page mapped: {self.page_mapped}", file=open('mapped_log.txt','a'))

        checked_xpath_comment_text = self.read_text(self.commentXPATH, "def mapped - reading text of comment based on saved xpath ")

        print(f"def mapped - checking if comments texts are equal", file=open('mapped_log.txt','a'))
        if checked_xpath_comment_text == self.commentTEXT.strip():
            self.click(self.likeButton_xp, "def mapped clicked like button after checking comments text equality")
            return
        elif checked_xpath_comment_text != self.commentTEXT.strip() and self.page_mapped <= self.page_search:
            self.search_next_at_mapped_loop(path, comment)
            print(f"def mapped - elif conditional page mapped is: {self.page_mapped} and page search count is: {self.page_search}", file=open('mapped_log.txt','a'))
        elif checked_xpath_comment_text != self.commentTEXT.strip() and self.page_mapped > self.page_search:
            print(f"def mapped - comments are not equal - cleaning vars: checked_xpath_comment_text {checked_xpath_comment_text}, saved comment text: {self.commentTEXT.strip()}", file=open('mapped_log.txt','a'))
            self.page_search = 1
            self.page_mapped = 1
            self.likeButton_xp, self.commentXPATH, self.commentTEXT = "", "", ""
            return

    def read_text(self, xpath, call_indication):
        find_xpath = driver.find_element(By.XPATH, xpath)
        xpath_text = find_xpath.get_attribute('innerHTML')
        print(f"def read_text - readed text is: {xpath_text}, call_indication: {call_indication}", file=open('mapped_log.txt','a'))
        return xpath_text.strip()

    def click(self, xpath, call_comment):
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        print(f"click - clicking given xpath: {xpath} - {call_comment}", file=open('mapped_log.txt','a'))

    def main(self, path, comment):
        print(f"main - starting main - ", file=open('mapped_log.txt','a'))
        self.get_homePage(path, comment)
        

SAL = MappAndLike()
while True: 
    start_time = time.time()
    SAL.main("marcin-prokop-drwi-z-tomasza-kammela-i-jego-sylwestrowych-zapewnien-foto-6851161590766400a", "Lewaki to najwięksi hipokryci i hejterzy")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time of looking the comment is equal to: {total_time} ",  file=open('mapped_log.txt','a'))