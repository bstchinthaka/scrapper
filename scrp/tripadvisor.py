from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import json


class Tripadvisor:
    def __init__(self, uuid, query):
        self.uuid = uuid
        self.query = query
        self.source = "tripadvisor"

    def get_text(self, div, xpath):
        a = div.find_element_by_xpath(xpath)
        return a.text

    def get_search_list(self):
        text = self.query
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

        url = "https://www.tripadvisor.com/Hotels"
        # options = webdriver.ChromeOptions()
        # options.headless = True
        # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        data = []

        try:
            search_box_xpath = "//input[@placeholder='Hotel name or destination']"

            w = WebDriverWait(driver, 8)
            w.until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))

            search_box = driver.find_element_by_xpath(search_box_xpath)
            search_box.click()
            search_box.send_keys(text)

            # wait 3 secs
            time.sleep(3)

            # get results
            results_xpath = "//div[@id='typeahead_results']/a"
            results = driver.find_element_by_xpath(results_xpath)
            results.click()

            # get rank
            rank_xpath = "//div[@id='ABOUT_TAB']/div[2]/div[1]/div[1]/span"
            w = WebDriverWait(driver, 8)
            w.until(EC.presence_of_element_located((By.XPATH, rank_xpath)))
            rank = driver.find_element_by_xpath(rank_xpath)
            # print(rank.text)

            # print(driver.current_url)

            current_url = driver.current_url

            for i in range(20):
                # get all review card divs  HR_CC_CARD
                review_card_xpath = "//div[@data-test-target='HR_CC_CARD']"
                review_cards = driver.find_elements_by_xpath(review_card_xpath)
                # print(review_cards)
                for review_card in review_cards:
                    divs = review_card.find_elements_by_xpath("div")
                    # print(len(divs))
                    if len(divs) == 2:  # no images
                        name = self.get_text(divs[0], "div/div[2]")
                        title = self.get_text(divs[1], "div/a/span/span")
                        review = self.get_text(divs[1], "div[3]/div[1]/div[1]/q/span")
                    elif len(divs) == 3:  # has images
                        name = self.get_text(divs[0], "div/div[2]")
                        title = self.get_text(divs[2], "div/a/span/span")
                        review = self.get_text(divs[2], "div[3]/div[1]/div[1]/q/span")
                    else:
                        print("ignore review card")
                    item = {
                        "name": name.split('wrote a review')[0].strip(),
                        "review_date": name.split('wrote a review')[1].strip(),
                        "title": title,
                        "review": review,

                    }
                    data.append(item)
                driver.get(current_url.replace('Reviews-', 'Reviews-or' + str(5 * i) + '-'))

        except Exception as e:
            print(self.uuid, e)
        else:
            print(self.uuid, "No errors")
        finally:
            driver.close()
            output = {"source": self.source, "reviews": data, "rating": rank.text}
            print(self.uuid, json.dumps(data))
            with open("data/" + self.uuid + "_" + self.source + ".json", 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)

    def start_search(self):
        self.get_search_list()


