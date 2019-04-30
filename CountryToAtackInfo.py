# -*- coding: utf-8 -*-
import urllib
from MaltegoTransform import *
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from PIL import ImageTk, Image
import time
import tkinter as tk
import sys
from selenium.webdriver.common.keys import Keys

m = MaltegoTransform()
#repoName = sys.argv[1]
repoName = "hola"

chrome_options = Options()
driver = None

'''
BUSQUEDA DEL PAIS
'''

try:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), chrome_options=chrome_options)
    rutaPais = "https://otx.alienvault.com/browse/pulses?q=country:%20" + "Colombia"
    driver.get(rutaPais)
except Exception as e:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
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
    infoPulso = {}
    driver.get(pulso)
    time.sleep(5)
    print(driver.find_element_by_xpath("/html/body/app-root/div[1]/div[1]/app-pulse-detail/div[1]/div/div/div/header/div[1]/h1").text)
    time.sleep(5)
    driver.find_element_by_name("DataTables_Table_0_length").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/app-root/div[1]/div[1]/app-pulse-detail/div[1]/div/div/div/div/app-pulse-indicators/div/div/div[2]/div/div[1]/div[1]/div/label/select/option[2]").click()
    time.sleep(3)
    barraBusqueda = driver.find_element_by_xpath("/html/body/app-root/div[1]/div[1]/app-pulse-detail/div[1]/div/div/div/div/app-pulse-indicators/div/div/div[2]/div/div[1]/div[2]/div/label/input")
    barraBusqueda.send_keys("URL")
    barraBusqueda.send_keys(Keys.END)
    indicadores1 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer odd']")
    indicadores2 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer even']")
    for fila in indicadores1:
        info = fila.find_element_by_xpath("//a").get_property("href")
        print(info)
    #for fila in indicadores2:
#driver.quit()
