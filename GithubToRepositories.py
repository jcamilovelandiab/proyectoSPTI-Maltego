# -*- coding: utf-8 -*-
import urllib
from MaltegoTransform import *
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from PIL import ImageTk, Image
import time
import tkinter as tk
import sys
from selenium.webdriver.common.keys import Keys

m = MaltegoTransform()
repoName = sys.argv[1]

def get_captcha(driver, element, path):

chrome_options = Options()
driver = None
try:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), chrome_options=chrome_options)
    driver.get("https://www.google.com")
except Exception as e:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
    driver.get("https://www.google.com")

barraBusqueda = driver.find_element_by_name("q")
barraBusqueda.send_keys("github")
barraBusqueda.send_keys(Keys.ENTER)

buscarGITHUB = driver.find_element_by_id("nqsbq")
buscarGITHUB.send_keys(repoName)
buscarGITHUB.send_keys(Keys.ENTER)

link = driver.find_element_by_partial_link_text(repoName)
link.click()

linkRepos = driver.find_element_by_xpath("//span[@class='Counter']")
m.addUIMessage(linkRepos.text)

m.returnOutput()
driver.quit()
