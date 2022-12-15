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

comment_index = []
content_of_comment = "Lorem"   
# content_of_comment = "Ech, teraz plynu do plukania sztucznej szczeki nie zareklam"   
counter = 0

class Pudlove: 
    
    def start(self):
        print("Starting")
        try:
            start_time = time.time()
            driver.get("https://www.pudelek.pl/robert-lewandowski-jednak-komentuje-30-milionow-premii-od-morawieckiego-to-sie-wszystko-dzieje-poza-pilkarzami-ktorzy-razem-z-kibicami-sa-ofiarami-6842487736318496a")
        except ignored_exceptions:
            print("starting again")
            driver.get("https://www.pudelek.pl/robert-lewandowski-jednak-komentuje-30-milionow-premii-od-morawieckiego-to-sie-wszystko-dzieje-poza-pilkarzami-ktorzy-razem-z-kibicami-sa-ofiarami-6842487736318496a")
        self.terms_and_conditions()
        return start_time
    
    def terms_and_conditions(self):
        print("Terms accepted")
        try:
            TermsAndConditions = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/button[2]")))
            TermsAndConditions.click()
        except ignored_exceptions:
            print("Terms and conditions not found")

        # Solution for the nextpage issue
    def switch_to_next_page(self):
        print("switch to next page")
        # time.sleep(2)
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    button = driver.find_element(By.XPATH, f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div')
                    button_possible_text = button.get_attribute('innerHTML')
                    print("checked")
                    if "Następna" in button_possible_text:
                        driver.execute_script("arguments[0].click();", button)
                        print(f"clicked index_i: {i} and index_j: {j}", button_possible_text)
                except ignored_exceptions:
                    pass

    def look_for_desired_comment_on_single_page(self):
        print("look_for_desired_comment_on_single_page")
        for i in range(0, 31):
            try:
                comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                            #  //*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[15]/div/div[2]
                comment = driver.find_element(By.XPATH, comment_xp)
                possible_text = comment.get_attribute('innerHTML')
                if content_of_comment in possible_text:
                    print(f"Found the article containing phrase. Index equals == {i}")
                    comment_index.append(comment_xp)
            except ignored_exceptions:
                print(f"index: {i} doesn't contain the desired comment")
        if len(comment_index) == 0:
            self.switch_to_next_page()

    def check_comment_index_list(self):
        while len(comment_index) == 0:
            self.look_for_desired_comment_on_single_page()
        return comment_index

    def likeing(self):
        start_time = self.start()
        print("liking")
        our_comment_xpath = self.check_comment_index_list()[0]
        comment = driver.find_element(By.XPATH, our_comment_xpath)
        possible_text = comment.get_attribute('innerHTML')
        print(f" Found comment text {possible_text}")
        if content_of_comment in possible_text:
            like_button = our_comment_xpath[:-6]
            print(f" like button: {like_button}")
            new_like_button = like_button + "div[1]/div[2]/div/button[1]"
            # new_like_button_search = wait.until(EC.element_to_be_clickable((By.XPATH, new_like_button)))
            try:
                new_like_button_search = driver.find_element(By.XPATH, new_like_button)
                if content_of_comment in possible_text:
                    driver.execute_script("arguments[0].click();", new_like_button_search)
                    print("like clicked")
                    comment_index.pop()
                    end_time = time.time()
                    total_time = end_time - start_time
                    print("Time of looking the comment is equal to: ", total_time) 
                    
            except ignored_exceptions:
                print("I wasn't able to like for some reason")
                
                
       

pl = Pudlove()
while True:
    pl.likeing()
    counter += 1
    print(f"counter: {counter}")
    time.sleep(2)
