from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
import os
import pandas as pd

def get_cookies(url):
    options = Options()
    #options.add_argument("--headless")
    #options.add_argument('--disable-gpu')
    #options.add_argument('--log-level=3') #Can't get all cookies when running using headless mode
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(r"user-data-dir=C:\user-data") #Create and use a new profile in Chrome
    driver = webdriver.Chrome("./chromedriver.exe", options=options) #change the path to your chromedriver


    driver.get(url)
    input("Kindly select the option, then press any key to continue ...") #SELECT AGREE TO COOKIES OR DENY
    time.sleep(5)  #WAIT FOR ALL COOKIES TO BE LOADED
    driver.quit() #QUIT TO SAVE THE COOKIES IN THE FILE

    #READ FROM COOKIE FILE
    src = r'C:\user-data\Default\Cookies'
    con = sqlite3.connect(src)
    cur = con.cursor()
    cur.execute("SELECT * FROM cookies")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    # df = df[df.columns[0:3]] 
    # df.columns = ['timestampe','domain','cookie_name'] #Extracted data have no headers.
    con.close() #close all services that're using the cookie file so that it can be removed
    os.remove(src) #DELETE COOKIES FILE TO RESET
    return df


url = "https://www.google.com"
df_live = get_cookies(url)
df_live.to_csv("output.csv", index=0)