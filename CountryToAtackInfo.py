# -*- coding: utf-8 -*-
import urllib
from MaltegoTransform import *
import time
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
try:
    formaLogin = driver.find_element_by_xpath("/html/body/app-root/div[1]/div[1]/app-home/section[1]/div/div/div[2]/div/ul/li[2]/button")
    formaLogin.click()
except Exception as e:
    formaLogin = driver.find_element_by_xpath("/html/body/app-root/div[1]/div[1]/app-home/section[1]/div/div/div[2]/div/ul/li[2]/button")
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
rutaPais = "https://otx.alienvault.com/browse/pulses?q=country:%20" + "Colombia"
driver.get(rutaPais)

'''
CANTIDAD DE PULSOS
'''
time.sleep(5)
numeroDePulsos = int(driver.find_element_by_xpath("/html/body/app-root/app-header/nav/ul/li[1]/a/span").text)


'''
CARGA DE LA PAGINA COMPLETA
'''

html = driver.find_element_by_tag_name('html')
for i in range((numeroDePulsos//10) + 1):
    html.send_keys(Keys.END)
    time.sleep(3)

'''
OBTENCION DE LOS PULSOS
'''
pulsos = driver.find_elements_by_xpath("/html/body/app-root//div[1]/div[1]/app-browse/div[1]/div/div[2]/div/div/*/div/*")
urlsPulsos = []
for pulso in pulsos:
    urlsPulsos.append("https://otx.alienvault.com/" + pulso.get_attribute("id").replace("-", "/"))
for pulso in urlsPulsos:
    driver.get(pulso)
    time.sleep(5)
    print(driver.find_element_by_xpath("/html/body/app-root/div[1]/div[1]/app-pulse-detail/div[1]/div/div/div/header/div[1]/h1").text)
#driver.quit()
