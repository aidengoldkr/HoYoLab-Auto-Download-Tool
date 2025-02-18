import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

def sanitize_filename(name):
    return re.sub(r'[\/:*?"<>|]', '', name)

def download_imgs(SAVE_DIR,download_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(download_url)

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "mhy-article-page__content")))
    article_content = driver.find_element(By.CLASS_NAME, "mhy-article-page__content")

    try:
        upper_2 = article_content.find_element(By.CLASS_NAME, "mhy-img-article")
        try:
            upper_4 = article_content.find_element(By.CLASS_NAME, "mhy-img-article__list swiper-container swiper-container-initialized swiper-container-horizontal")
            swiper_wrapper = upper_2.find_element(By.CLASS_NAME, "swiper-wrapper")
            images = swiper_wrapper.find_elements(By.TAG_NAME, "img")
        except:
            only_2 = article_content.find_element(By.CLASS_NAME, "mhy-img-article__list swiper-container swiper-container-initialized swiper-container-horizontal")
            swiper_wrapper = upper_2.find_element(By.CLASS_NAME, "swiper-wrapper")
            images = swiper_wrapper.find_elements(By.TAG_NAME, "img")
    except:
        images = article_content.find_elements(By.TAG_NAME, "img")
        print("Swiper-container not found, using direct image extraction")

    title_r = driver.find_element(By.XPATH, '//div[@class = "mhy-article-page__title"]')
    title = (sanitize_filename(title_r.get_attribute("innerText")).strip())

    IMAGE_FOLDER = title
    SAVE_DIR = os.path.join(SAVE_DIR, IMAGE_FOLDER)
    os.makedirs(SAVE_DIR, exist_ok=True)
    print("Created folder:", SAVE_DIR)
    time.sleep(3)

    for i, img in enumerate(images):
        data_src = img.get_attribute("data-src") or img.get_attribute("src")
        if data_src:
            try:
                response = requests.get(data_src)
                if response.status_code == 200:
                    file_path = os.path.join(SAVE_DIR, f"image_{i+1}.jpg")
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded: {file_path}")
                else:
                    driver.quit()
                    return(f"Failed to download image {i}: {data_src}")
            except Exception as e:
                driver.quit()
                return(f"Error downloading image {i}: {e}")

    driver.quit()
    return("Download ss")