from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
from urllib.request import urlopen as ureq
import pandas as pd

binary = FirefoxBinary()
binary.add_command_line_options('--binary=C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)

yt_url="https://www.youtube.com/@PW-Foundation/videos"
driver.get(yt_url)
videos=driver.find_elements(By.XPATH, './/*[@id="dismissible"]')

video_list=[]


for video in videos[:5]:
    title=video.find_element(By.XPATH,'.//*[@id="video-title"]').text
    views=video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[1]').text
    video_title_link=video.find_element(By.XPATH,'.//*[@id="video-title-link"]')
    href_link = video_title_link.get_attribute('href')
    release_date=video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[2]').text
    thumbnail_url=video.find_element(By.XPATH,'.//*[@id="thumbnail"]')
    img_url=thumbnail_url.get_attribute('href')
    video_items={
        "title":title,
        "views":views,
        "when":release_date,
        "title_link":href_link,
        "img_link":img_url
    }
    video_list.append(video_items)

df=pd.DataFrame(video_list)
print(df)