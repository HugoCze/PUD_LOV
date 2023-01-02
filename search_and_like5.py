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

# chrome_options.headless = True
# Test
chrome_options.headless = False

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(15)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)

class Search_And_Like:
    
    # TODO get rid of that
    date_time = date_time
    next_button_list = []
    comment_XPATH, comment_TEXT, like_button = "", "", ""

    
    def get_homePage(self, path, comment):
        homepage = "https://www.pudelek.pl/" + path
        try:
            driver.get(homepage)
            print("got home page", file=open('SAL_LogFile2.txt','a'))
            self.terms(path, comment)
        except ignored_exceptions:
            print(f"{self.date_time} - failed to get homePage - closing driver", file=open('SAL_LogFile2.txt','a'))
            # self.main(path, comment)
            driver.close()
    
    def terms(self, path, comment):
        print("Terms", file=open('SAL_LogFile2.txt','a'))
        try:
            TermsAndConditions = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/button[2]")))
            TermsAndConditions.click()
        except ignored_exceptions:
            print(f"{self.date_time} -Terms and conditions not found - searching comment", file=open('SAL_LogFile2.txt','a'))
            self.search_comment(path, comment)

    def search_comment(self, path, comment):
        print("searching for comment", file=open('SAL_LogFile2.txt','a'))
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                # print(f"def search comment text: {comment_text}") #; our type {comment}")
                if comment_text.strip() == comment.strip():
                    self.map_tool(possible_comment_xp, "comment_xpath")
                    self.map_tool(comment_text, "comment_text")
                    print("got the cooomment", file=open('SAL_LogFile2.txt','a'))
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print("got the like butt", file=open('SAL_LogFile2.txt','a'))
                    # self.click_it(like_button_xp)
                    self.map_tool(like_button_xp, "like")
                    break
            except ignored_exceptions:
                pass
        else:
            self.search_next(path, comment)
            
    def search_next(self, path, comment):
        print("search for the next page button", file=open('SAL_LogFile2.txt','a'))
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                        # print(f"next page button text: {button_possible_text} ; next page button xp {next_button_xp}")
                        print("got the next button", file=open('SAL_LogFile2.txt','a'))
                        self.map_tool(next_button_xp, "next")
                        self.search_comment(path, comment)
        
                except ignored_exceptions:
                    pass
    
    def mapped(self, path, comment):
        if self.next_button_list:
            print(f"Button list is not empty: ", file=open('SAL_LogFile2.txt','a'))
            for i in range(19, 36):
                for j in range(2,4):
                    try:
                        next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                        button_action = driver.find_element(By.XPATH, next_button_xp)
                        button_possible_text = button_action.get_attribute('innerHTML')
                        if button_possible_text == "Następna strona":
                            print(f" next button xp: {next_button_xp}", file=open('SAL_LogFile2.txt','a'))
                    except ignored_exceptions:
                        pass
            
            print(f"Len for self.next_button_list {len(self.next_button_list)}", file=open('SAL_LogFile2.txt','a'))
            
            for button in self.next_button_list:
                if button != self.next_button_list[-1]:
                    print(f"def mapped next button: {button}", file=open('SAL_LogFile2.txt','a'))
                    self.click(button)
                    print(f"Clicked button: {button} ", file=open('SAL_LogFile2.txt','a'))
                    time.sleep(1)
        comment_XPATH = self.comment_XPATH
        comment_XPATH_finder = driver.find_element(By.XPATH, comment_XPATH)
        comment_TEXT = comment_XPATH_finder.get_attribute('innerHTML')
        print(f"Checking comment: {comment_TEXT}, {comment_XPATH} ", file=open('SAL_LogFile2.txt','a'))
        if self.comment_TEXT == comment_TEXT:
            self.click(self.like_button)
            print(f"Clicked the like button: {self.like_button} ", file=open('SAL_LogFile2.txt','a'))
        elif self.comment_TEXT != comment_TEXT:
            self.next_button_list = []
            self.comment_XPATH, self.comment_TEXT, self.like_button = "", "", ""
            print(f"Clicked the like button: {comment_TEXT}  and {self.comment_TEXT} are not the same", file=open('SAL_LogFile2.txt','a'))
        # TODO check if I dont need to call the search

    def click(self, xpath):
        print(f"def click: used xpath: {xpath}\n", file=open('SAL_LogFile2.txt','a'))
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        print("def click: clicked\n", file=open('SAL_LogFile2.txt','a'))

    def map_tool(self, xpath, type):

        if type == "next":

            print(f"def map_tool: used xpath: {xpath}\n", file=open('SAL_LogFile2.txt','a'))
            self.click(xpath)
            self.next_button_list.append(xpath)
            print("next appended to list", file=open('SAL_LogFile2.txt','a'))
        
        elif type == "like":

            print(f"def click: used xpath: {xpath}\n", file=open('SAL_LogFile2.txt','a'))
            self.click(xpath)
            print("def click: clicked\n", file=open('SAL_LogFile2.txt','a'))
            self.like_button = xpath
            print(f"like new xpath: {xpath}", file=open('SAL_LogFile2.txt','a'))

        #TODO change the xpath to something less direct
        elif type == "comment_text":
            self.comment_TEXT = xpath
            print(f"new comment text: {xpath}", file=open('SAL_LogFile2.txt','a'))

        elif type == "comment_xpath":
            self.comment_XPATH = xpath
            print(f"new comment xpath: {xpath}", file=open('SAL_LogFile2.txt','a'))

    def main(self, path, comment):
        start_time = time.time()
        self.get_homePage(path, comment)
        if self.comment_XPATH == "" or self.comment_TEXT == ""or  self.like_button == "":
            self.search_comment(path, comment)
        elif self.comment_XPATH != "" and self.comment_TEXT != "" and  self.like_button != "":
            print(f"List of next buttons: {self.next_button_list}", file=open('SAL_LogFile2.txt','a'))
            self.mapped(path, comment)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"{self.date_time} - Time of looking the comment is equal to: {total_time} ", file=open('SAL_LogFile2.txt','a'))
        print(f"next_button_list: {self.next_button_list}", file=open('SAL_LogFile2.txt','a'))
        print(f"Comment XPATH, CommentTEXT, Like button XP{self.comment_XPATH, self.comment_TEXT, self.like_button}", file=open('SAL_LogFile2.txt','a'))
        print("Next buttons list: ", self.next_button_list)

SAL = Search_And_Like()
while True: 
    SAL.main("katarzyna-cichopek-i-maciej-kurzajewski-juz-sa-po-wigilii-w-tym-roku-nieco-wczesniej-zdjecia-6847767886412608a", "Co cwansi nie piszą komentarzy tylko jeżdżą na castingi i odbierają telefony a ci drudzy co wola pisać o kimś kogo nie lubią ani oni ani wielu")
