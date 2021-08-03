from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import json


class Booking:
    def __init__(self, uuid, query):
        self.uuid = uuid
        self.query = query

    def close_last_tab(self):
        if len(self.driver.window_handles) == 2:
            chwd = self.driver.window_handles
            for w in chwd:
                if w != self.p:
                    self.driver.switch_to.window(w)


    def get_text(self, div, xpath):
        a = div.find_element_by_xpath(xpath)
        return a.text

    def get_search_list(self):
        text = self.query
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

        url = "https://www.booking.com/"
        # options = webdriver.ChromeOptions()
        # options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)
        data = []

        try:
            search_box_xpath = "//input[@id='ss']"

            w = WebDriverWait(self.driver, 8)
            w.until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))

            search_box = self.driver.find_element_by_xpath(search_box_xpath)
            search_box.click()
            search_box.send_keys(text)

            # wait 3 secs
            time.sleep(3)

            # get results
            results_xpath = "//button[@data-sb-id='main']"
            results = self.driver.find_element_by_xpath(results_xpath)
            results.click()

            time.sleep(3)

            # get card 'sr_item'

            title_xpath = "//*[@id='hotellist_inner']/div[1]/div[2]/div[1]/div[2]/div/div[1]/a/div/div[2]/div[1]"

            w = WebDriverWait(self.driver, 8)
            w.until(EC.presence_of_element_located((By.XPATH, title_xpath)))

            title = self.driver.find_elements_by_xpath(title_xpath)
            print("Title", title[0].text)

            rating_xpath = "//*[@id='hotellist_inner']/div[1]/div[2]/div[1]/div[2]/div/div[1]/a/div/div[1]"
            rating = self.driver.find_elements_by_xpath(rating_xpath)
            print("rating", rating[0].text)

            self.p = self.driver.current_window_handle
            rating_link_xpath = "//*[@id='hotellist_inner']/div[1]/div[2]/div[1]/div[2]/div/div[1]/a/div/div[2]/div[2]"
            rating_link = self.driver.find_element_by_xpath(rating_link_xpath)
            rating_link.click()

            self.close_last_tab()

            # //button[@rel='reviews']
            review_all_xpath = "//button[@rel='reviews']"
            w = WebDriverWait(self.driver, 8)
            w.until(EC.presence_of_element_located((By.XPATH, review_all_xpath)))
            review_all = self.driver.find_element_by_xpath(review_all_xpath)
            review_all.click()

            page_xpath = "//*[@id='review_list_page_container']/div[6]/div/div[1]/div/div[3]"
            w = WebDriverWait(self.driver, 8)
            w.until(EC.presence_of_element_located((By.XPATH, page_xpath)))
            page = self.driver.find_element_by_xpath(page_xpath)
            page.click()





        except Exception as e:
            print(self.uuid, e)
        else:
            print(self.uuid, "No errors")
        finally:
            #self.driver.close()
            print(self.uuid, json.dumps(data))
            with open("data/" + self.uuid + ".json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def start_search(self):
        self.get_search_list()


b = Booking(12345, "Marino Beach Colombo")
b.start_search()
