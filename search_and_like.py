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

# chrome_options.headless = True
#Test
chrome_options.headless = False

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(30)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)

class Search_And_Like():

    next_buttons = []
    comment_fullText_content = ""
    comment_xp = ""
    like_button_xp = ""

    def get_homePage(self, path):
        homepage = "https://www.pudelek.pl/" + path
        print("Entering homepage")
        try:
            driver.get(homepage)
        except ignored_exceptions:
            print("starting again")
            self.get_homePage(path)
        self.terms_and_conditions()
    
    def terms_and_conditions(self):
        print("Terms accepted")
        try:
            TermsAndConditions = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/button[2]")))
            TermsAndConditions.click()
        except ignored_exceptions:
            print("Terms and conditions not found")

    def search_for_comment(self, comment):
        comments_per_page_text = []
        comments_per_page_xpath = []
        print("searching for comment")
        for i in range(0, 31):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                comments_per_page_text.append(comment_text.strip())
                comments_per_page_xpath.append(possible_comment_xp)
            except ignored_exceptions:
                pass
        # print(f"comments on page: {comments_per_page}")
        return comments_per_page_text, comments_per_page_xpath


    def search_for_next_button(self):
        print("search for the next page button")
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    print("checked")
                    if button_possible_text == "Następna strona":
                        print(f"next page button text: {button_possible_text}, next page button xp {button_xp}")
                        self.next_buttons.append(button_xp)
                        return button_xp
                except ignored_exceptions:
                    pass


    def check_search(self, comment):
        print("def check")
        comment = comment.strip()
        
        comments_per_page_text, comments_per_page_xpath = self.search_for_comment(comment)

        if comment in comments_per_page_text:
            print("def check: Found the comment")
            comments_index = comments_per_page_text.index(comment)
            comments_xpath = comments_per_page_xpath[comments_index]
            self.comment_fullText_content = comment
            self.comment_xp = comments_xpath
            print("Appending like button xpath")
            like_button = comments_xpath[:-6]
            like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
            self.like_button_xp = like_button_xp

        else:
            print("def check: Didnt found the comment -> next page")
            next_button_xp = self.search_for_next_button()
            next_button_action = driver.find_element(By.XPATH, next_button_xp)
            driver.execute_script("arguments[0].click();", next_button_action)
            self.check_search(comment)
    
    # def check_vars(self):
    #     print("checking vars")
    #     if self.like_button_xp == "" or self.comment_xp == "" or self.comment_fullText_content == "" or self.next_buttons == []:
    #         return True
    #     else:
    #         return False

    def mapped(self, path, comment):
        # self.get_homePage(path)
        print("mapp")
        if self.like_button_xp == "" or self.comment_xp == "" or self.comment_fullText_content == "": # or self.next_buttons == []:
            print("def mapped - vars are empty checking search")
            self.get_homePage(path)
            time.sleep(1)
            self.check_search(comment)
        # elif self.like_button_xp != "" and self.comment_xp != "" and self.comment_fullText_content != "": # and self.next_buttons != []:
        else:
            print("vars are not empty\n")
            self.get_homePage(path)
            time.sleep(1)

            for button in self.next_buttons:
                self.click(button)
                print("clicked next form def mapped\n")
                time.sleep(1)
            mapped_comment_verify = driver.find_element(By.XPATH, self.comment_xp)
            mapped_comment_verify_text = mapped_comment_verify.get_attribute('innerHTML')
            print(f"def mapped - comment verfication text: {mapped_comment_verify_text.strip()}, - comment in memory {self.comment_fullText_content.strip()}")
            if mapped_comment_verify_text.strip() == self.comment_fullText_content.strip():
                print("clicked like from def mapped\n")
                self.click(self.like_button_xp)
                print("refreshed from def mapp\n")
            else:
                print("Comment content from history do not match def mapped verification \n")
                # driver.refresh()
                # self.get_homePage(path)
                self.next_buttons = []
                self.comment_fullText_content = ""
                self.comment_xp = ""
                self.like_button_xp = ""
                self.check_search(comment)


    def click(self, xpath):
        print(f"def click: used xpath: {xpath}\n")
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        print("def click: clicked\n")

    def main(self, path, comment):
        while True:
            start_time = time.time()
            self.mapped(path, comment)
            end_time = time.time()
            total_time = end_time - start_time
            print("Time of looking the comment is equal to: ", total_time)


sal = Search_And_Like()

sal.main("katarzyna-cichopek-i-maciej-kurzajewski-juz-sa-po-wigilii-w-tym-roku-nieco-wczesniej-zdjecia-6847767886412608a", "Dlaczego nie ogłaszają kiedy jest pogrzeb tego pana ?")