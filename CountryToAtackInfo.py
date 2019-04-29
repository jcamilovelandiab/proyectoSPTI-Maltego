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
#repoName = sys.argv[1]
repoName = "hola"

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)
    # uses PIL library to open image in memory
    image = Image.open(path)
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image

chrome_options = Options()
driver = None
try:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), chrome_options=chrome_options)
    driver.get("https://otx.alienvault.com")
except Exception as e:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
    driver.get("https://otx.alienvault.com")

'''
LOGIN, CUENTA FALSA EN OTX
'''
formaLogin = driver.find_element_by_xpath("//ul[@class='auth-nav']/li[2]/button")
formaLogin.click()
usuario = "osintmaltego"
contraseña = "osint123"
username = driver.find_element_by_id("id_login")
password = driver.find_element_by_id("id_password")
username.send_keys(usuario)
password.send_keys(contraseña)
botonLogin = driver.find_element_by_id("loginBtn")
botonLogin.click()

'''
BUSQUEDA DEL PAIS
'''

lupaBusqueda = driver.find_element_by_id("headerSearchInput")
lupaBusqueda.send_keys("country: Colombia")
botonBusqueda = driver.find_element_by_id("otxSearchSubmitButton")
botonBusqueda.click()

#driver.quit()
