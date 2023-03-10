import asyncio
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

comment_fullText_content = []
comment_index = []
next_buttons = []
like_button = []

class PudLove: 

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

    async def search_for_comment(self, comment_content):
        print("searching for comment")
        next_button_location = await self.search_for_nextPage_button()
        for i in range(0, 31):
            
            try:
                comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment = driver.find_element(By.XPATH, comment_xp)
                possible_text = comment.get_attribute('innerHTML')
                if comment_content in possible_text:
                    print(f"Found the article containing phrase. comment xp = {comment_xp}")
                    comment_index.append(comment_xp)
                    comment_fullText_content.append(possible_text)
                    return comment_xp
            except ignored_exceptions:
                print(f"index: {i} doesn't contain the desired comment")
        if len(comment_index) == 0:
        # else:
            next_button_action = driver.find_element(By.XPATH, next_button_location)
            driver.execute_script("arguments[0].click();", next_button_action)
            await self.search_for_comment(comment_content)
            
    async def search_for_nextPage_button(self):
        print("search next page button")
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    print("checked")
                    if button_possible_text == "Nast??pna strona":
                        print(f"button xp = {button_xp}")
                        next_buttons.append(button_xp)
                        return(button_xp)
                except ignored_exceptions:
                    pass

    async def like(self, comment):
        print("like comment")
        comment_xp = await self.search_for_comment(comment)
        if comment_xp != None:
            print("comment xp from like def")
            like_button = comment_xp[:-6]
            # print(f" like button: {like_button}")
            like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
            like_button_xp_search = driver.find_element(By.XPATH, like_button_xp)

                    driver.execute_script("arguments[0].click();", new_like_button_search)

    
    def main(self, article, comment):
        start_time = time.time()
        start = self.get_homePage(article)
        asyncio.run(self.like(comment))
        print(f"comment_fullText_content: {comment_fullText_content}")
        print(f"comment_index: {comment_index}")
        print(f"next_buttons: {next_buttons}")
        print(f"like_button: {like_button}")
        end_time = time.time()
        total_time = end_time - start_time
        print("Time of looking the comment is equal to: ", total_time) 
        

    


pl = PudLove()

pl.main("katarzyna-cichopek-i-maciej-kurzajewski-juz-sa-po-wigilii-w-tym-roku-nieco-wczesniej-zdjecia-6847767886412608a", "Bezgu??cie goni bezgu??cie. Zobacz kobieto jak Pani Wachowicz nakrywa do sto??u.")