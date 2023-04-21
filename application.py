from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
from urllib.request import urlopen as ureq
import pandas as pd
from pymongo.mongo_client import MongoClient
import cython


logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
application = Flask(__name__)
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--no-sandbox')
driver = webdriver.Firefox(options=firefox_options)


@application.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@application.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            yt_string = request.form['content'].replace(" ","")
            yt_url = "https://www.youtube.com/@"+yt_string+"/videos"
            driver.get(yt_url)
            videos=driver.find_elements(By.XPATH, './/*[@id="dismissible"]')
            # filename =  yt_string + ".csv"
            # fw = open(filename, "w")
            # headers = "Title, Views, Release_date, title_url, thumbnail_url \n"
            # fw.write(headers)
            video_list=[]
            for video in videos[:6]:
                try:
                    #title.encode(encoding='utf-8')
                   title=video.find_element(By.XPATH,'.//*[@id="video-title"]').text

                except:
                    logging.info("title")

                try:
                    #views.encode(encoding='utf-8')
                    views=video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[1]').text


                except:
                    views = 'No Views'
                    logging.info("views")

                try:
                    #video_title_link.encode(encoding='utf-8')
                    video_title_link=video.find_element(By.XPATH,'.//*[@id="video-title-link"]')
                    href_link = video_title_link.get_attribute('href')
                    
                except:
                    href_link = 'No links'
                    logging.info("href_link")
                try:
                    release_date=video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[2]').text
                except :
                    release_date="no date"
                    logging.info("release_date")
                try:
                    thumbnail_url=video.find_element(By.XPATH,'.//*[@id="thumbnail"]')
                    img_url=thumbnail_url.get_attribute('href')
                except:
                    thumbnail_url="no link"
                    logging.info("thumbnail_url")

                video_items={"title":title,"views":views,"when":release_date,"title_link":href_link,"img_link":img_url}
                video_list.append(video_items)
                # df=pd.DataFrame(video_list)
                # print(df)
                # df.to_csv("yotube_data.csv")
           
            logging.info("log my final result {}".format(video_list))
            return render_template('result2.html', reviews=video_list[0:len(video_list)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__=="__main__":
    application.run(debug=True)
