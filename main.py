from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
import json

BASE_URL = "https://qipedc.moet.gov.vn"
VIDEOS_API = "https://qipedc.moet.gov.vn/videos"

def handle_recursive_scrapping(dict: dict):
    vids = WebDriverWait(driver=driver, timeout=3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1)"))
    )
    vids = driver.find_elements(By.CSS_SELECTOR, "section:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) a")
    for vid in vids:
        gross = vid.find_element(By.CSS_SELECTOR, "p").text
        raw_thumb_url = vid.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        base_thumbs_url = "https://qipedc.moet.gov.vn/thumbs/"
        videosID = raw_thumb_url[len(base_thumbs_url):len(raw_thumb_url) - 4]
        video_url = BASE_URL + "/videos/" + videosID + ".mp4"

        item = {
            "gross": gross,
            "url": video_url
        }
        print(item)
        dict.append(item)
    return

options = Options()
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://qipedc.moet.gov.vn/dictionary")
print(driver.title)
f = open("output.txt", "w+")
f.write(driver.page_source)
f.close()


try:
    json_file = open("data.json", "w+", encoding="utf8")
    output_dict = []

    handle_recursive_scrapping(output_dict)

    for i in range (2, 5):
        id = i
        if i != 2: id = i + 1
        button = driver.find_element(By.CSS_SELECTOR, f"button:nth-of-type({id})")
        button.click()
        handle_recursive_scrapping(output_dict)
    for i in range (5, 218):
        id = 6
        button = driver.find_element(By.CSS_SELECTOR, f"button:nth-of-type({id})")
        button.click()
        handle_recursive_scrapping(output_dict)
    
    for i in range(218, 220):
        id = 6
        if i!= 218: id = 7
        button = driver.find_element(By.CSS_SELECTOR, f"button:nth-of-type({id})")
        button.click()
        handle_recursive_scrapping(output_dict)

    str = json.dumps(output_dict, ensure_ascii=False)
    json_file.write(str)
    json_file.close()
except Exception as e:
    print("No videos found \n")
    print(e)

time.sleep(7)
driver.close()