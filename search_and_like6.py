import asyncio
import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, InvalidSessionIdException, ElementNotInteractableException, StaleElementReferenceException, TimeoutException,ElementClickInterceptedException
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

ignored_exceptions=(NoSuchElementException, InvalidSelectorException, StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)

class Search_And_Like:

    next_button_list = []
    comment_XPATH, comment_TEXT, like_button = "", "", ""
    
    def get_homePage(self, path, comment):
        homepage = "https://www.pudelek.pl/" + path
        try:
            print("get_homePage - getting home page", file=open('mapped_log.txt','a'))
            driver.get(homepage)
            print("get_homePage - got home page", file=open('mapped_log.txt','a'))
            print("get_homePage - terms loading", file=open('mapped_log.txt','a'))
            self.terms(path, comment)
            print("get_homePage - terms loaded", file=open('mapped_log.txt','a'))
        except ignored_exceptions:
            print("get_homePage - terms loaded", file=open('mapped_log.txt','a'))
            print(f"get_homePage - failed to get homePage - closing driver", file=open('mapped_log.txt','a'))
            # self.main(path, comment)
            driver.close()
            print(f"get_homePage - driver closed ", file=open('mapped_log.txt','a'))
    
    def terms(self, path, comment):
        print(f"terms - terms opening ", file=open('mapped_log.txt','a'))
        try:
            print(f"terms - trying  terms clicking ", file=open('mapped_log.txt','a'))
            TermsAndConditions = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/button[2]")))
            TermsAndConditions.click()
            print(f"terms - clicked ", file=open('mapped_log.txt','a'))
        except ignored_exceptions:
            print(f"terms - exception ", file=open('mapped_log.txt','a'))
            print(f"{date_time} -Terms and conditions not found - searching comment", file=open('SAL_LogFile.txt','a'))
            self.search_comment(path, comment)
            print(f"terms - search comment initialized ", file=open('mapped_log.txt','a'))

    def search_comment(self, path, comment):
        print(f"search_comment - search comment starting ", file=open('mapped_log.txt','a'))
        
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                # print(f"search_comment - Looping through comments: {possible_comment_xp} with text: {comment_text}", file=open('mapped_log.txt','a'))
                if comment_text.strip() == comment.strip():
                    print(f"search_comment - got the matching comment", file=open('mapped_log.txt','a'))
                    self.comment_XPATH = possible_comment_xp
                    self.comment_TEXT = comment_text
                    print(f"search_comment - appended to commentXPATH: {possible_comment_xp} with commentTEXT: {comment_text}", file=open('mapped_log.txt','a'))
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print(f"search_comment - like button distinguished", file=open('mapped_log.txt','a'))
                    self.click(like_button_xp)
                    print(f"search_comment - like button clicked with self.click - breaking", file=open('mapped_log.txt','a'))
                    self.like_button = like_button_xp
                    break
            except ignored_exceptions:
                print(f"search_comment - got the search comment exception - passing as descripted", file=open('mapped_log.txt','a'))
                pass
        else:
            print(f"search_comment - for loop got through all the comments with no match for us - searching next", file=open('mapped_log.txt','a'))
            self.search_next(path, comment)
            
    def search_next(self, path, comment):
        print(f"search_next - welcome to search next - looping through possible next buttons", file=open('mapped_log.txt','a'))
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                        print(f"search_next - found the button {button_possible_text} with XPATH {next_button_xp} = ", file=open('mapped_log.txt','a'))
                        self.next_button_list.append(next_button_xp)
                        print(f"search_next - self next button list after appending: {self.next_button_list} ", file=open('mapped_log.txt','a'))
                        print(f"search_next - clicking with self.click ", file=open('mapped_log.txt','a'))
                        self.click(next_button_xp)
                        print(f"search_next - clicked with self.click - going with search comment", file=open('mapped_log.txt','a'))
                        self.search_comment(path, comment)
                except ignored_exceptions:
                    print(f"search_next - got an exception on search next while in loop", file=open('mapped_log.txt','a'))
                    pass

    def click(self, xpath):
        print(f"click - clicking given xpath", file=open('mapped_log.txt','a'))
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)

    def mapped(self, path, comment):
        print(f"mapped - welcome to mapped", file=open('mapped_log.txt','a'))
        page = 1
        print(f"mapped - current page should be: {page}", file=open('mapped_log.txt','a'))
        try:
            print(f"mapped - trying driver refresh", file=open('mapped_log.txt','a'))
            driver.refresh()
        except ignored_exceptions:
            print(f"mapped - got a exception on  driver refresh - going with self mapped", file=open('mapped_log.txt','a'))
            self.mapped(path, comment)
        print(f"mapped - refreshed without any errors - checking if refreshed", file=open('mapped_log.txt','a'))

        self.check_if_refreshed('//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[1]/div/div/button','//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[2]/div/div/button', '//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[3]/div/div/button')

        print(f"mapped - looping through index and button on next list", file=open('mapped_log.txt','a'))
        for index, button in enumerate(self.next_button_list):
            if index != -1:
                print(f"mapped - not including last button. The button in loop is: {button} of index: {index}", file=open('mapped_log.txt','a'))
                page += 1
                try:
                    self.click(button)
                    print(f"mapped - clicked the next button", file=open('mapped_log.txt','a'))
                    print(f"mapped - checking if we are still on the first page", file=open('mapped_log.txt','a'))
                    try:
                        print("#####################LOOK BELOW #############################", file=open('mapped_log.txt','a'))
                        next_button_decteced_text = self.get_element_content_text(button)
                        print(f"mapped - checked the next_button_decteced_text : {next_button_decteced_text} and the clicked button xpath: {button}", file=open('mapped_log.txt','a'))
                    except ignored_exceptions:
                        print(f"mapped - wasn't able to check the next button due to ignored exceptions", file=open('mapped_log.txt','a'))
                    try:
                        self.check_if_refreshed('//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[1]/div/div/button','//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[2]/div/div/button', '//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[3]/div/div/button')
                        print(f"mapped -checked if we are still on the first page", file=open('mapped_log.txt','a'))
                    except ignored_exceptions:
                        print(f"mapped - checking if we are still on the first page went wrong - probably due to the different page xpath - TODO add some exception to page checker", file=open('mapped_log.txt','a'))
                except ignored_exceptions:
                    print(f"mapped - exception on clicking and we move back to the self mapped def ", file=open('mapped_log.txt','a'))
                    self.mapped(path, comment)
                print(f"def mapped - Page: {page}", file=open('mapped_log.txt','a'))
        try:
            print(f"mapped - trying to get the comment that was saved in self comment XPATH var", file=open('mapped_log.txt','a'))
            comment_location = driver.find_element(By.XPATH, self.comment_XPATH)
            comment_text = comment_location.get_attribute('innerHTML')

        # TODO script crashed on trying to equal the current saved comment with this under saved xpath and failed.
        # I would write a def that will replace whole loop searching for the next button and use it under search next 
        # It will also help us to determine which page are we on currently. 
        #  After some consideration some small loop checking the current site page 
        # working alongside or instead the "first page" check would be great!

        except ignored_exceptions:
            print(f"mapped - got an exception with locating the saved comment", file=open('mapped_log.txt','a'))
            # place for def that will check for the next button
            # at the same time we will check for the vallues at the bottom of the page
            # First need to compare nextbutton xp with the xpaths from check if refreshed 
            driver.refresh()
            self.search_comment(path, comment)
            print(f"mapped - refreshed and went for search comment", file=open('mapped_log.txt','a'))
        if self.comment_TEXT.strip() == comment_text.strip():
            try:
                print(f"mapped - comment TEXT equals with saved comment text", file=open('mapped_log.txt','a'))
                self.click(self.like_button)
                driver.refresh()
            except ignored_exceptions:
                print(f"mapped - exception while clicking the equal comment XPATH", file=open('mapped_log.txt','a'))
        else:
            print(f"mapped - comment TEXT doesn't equals with saved comment text - cleaning vars and checking if still first page", file=open('mapped_log.txt','a'))
            print(f"self.comment_TEXT.strip() {self.comment_TEXT.strip()} and the passed comment: {comment_text.strip()} was. ", file=open('mapped_log.txt','a'))
            try:
                for index, button in enumerate(self.next_button_list):
                    if index != -1:
                        self.click(button)

                print(f"mapped - comment does't equal comment - trying to next the page", file=open('mapped_log.txt','a'))
                self.click(self.like_button)
            except ignored_exceptions:
                # self.check_if_refreshed('//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[1]/div/div/button','//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[2]/div/div/button', '//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[30]/div/div[1]/div[3]/div/div/button')
                self.next_button_list = []
                self.comment_XPATH, self.comment_TEXT, self.like_button = "", "", ""
    
        
    def check_if_refreshed(self, xp1, xp2, xp3):
        xp1 = self.get_element_content_text(xp1)
        xp2 = self.get_element_content_text(xp2)
        xp3 = self.get_element_content_text(xp3)
        print(f"check_if_refreshed - checking the pages values", file=open('mapped_log.txt','a'))
        if (xp1 == "1" or 1) and (xp2 == "2" or 2) and (xp3 == "3" or 3):
            print(f"check_if_refreshed - we are on the first page", file=open('mapped_log.txt','a'))
        else:
            print(f"check_if_refreshed - we are not on the first page. The xps are {xp1}, {xp2}, {xp3}", file=open('mapped_log.txt','a'))

    def get_element_content_text(self, xpath):
        print(f"get_element_content_text - searching for elements xpath", file=open('mapped_log.txt','a'))
        try:
            xp_loc = driver.find_element(By.XPATH, xpath)
            xp_con = xp_loc.get_attribute('innerHTML')
            print(f"get_element_content_text - returning text", file=open('mapped_log.txt','a'))
            return xp_con
        except ignored_exceptions:
            print(f"get_element_content_text - due to the igorned exception the get ele def wasnt able to declare the text assigned to xpath", file=open('mapped_log.txt','a'))

    def main(self, path, comment):
        print(f"main - checking the content of comment xpath, text and like button xpath", file=open('mapped_log.txt','a'))
        print(f"main - self.comment_XPATH {self.comment_XPATH}, self.comment_TEXT {self.comment_TEXT} and self.like_button {self.like_button}", file=open('mapped_log.txt','a'))
        if self.comment_XPATH != "" and self.comment_TEXT != "" and self.like_button != "":
            self.mapped(path, comment)
        else:
            print(f"main - it appears that vars are empty so we go with getHomePage and search_comment def", file=open('mapped_log.txt','a'))
            self.get_homePage(path, comment)
            self.search_comment(path, comment)
            # driver.close()

SAL = Search_And_Like()
while True: 
    start_time = time.time()
    SAL.main("katarzyna-cichopek-i-maciej-kurzajewski-juz-sa-po-wigilii-w-tym-roku-nieco-wczesniej-zdjecia-6847767886412608a", "Nie no fajna babka")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"{date_time} - Time of looking the comment is equal to: {total_time} ",  file=open('mapped_log.txt','a'))
