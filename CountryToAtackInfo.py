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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        barraBusqueda = driver.find_element_by_xpath("// *[ @ id = 'DataTables_Table_0_filter'] / label / input")

        """BUSCAR URLS"""
        barraBusqueda.send_keys("URL")
        infoPulso["URL"] = []
        time.sleep(5)
        barraBusqueda.send_keys(Keys.END)
        try:
            indicadores1 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
            indicadores2 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
        except Exception as e:
            indicadores1, indicadores2 = [],[]
        for fila in indicadores1 + indicadores2:
            infoPulso["URL"].append(fila.text)
            print("URL",fila.text)

        """BUSCAR IPV4"""
        barraBusqueda.clear()
        barraBusqueda.send_keys("IPV4")
        infoPulso["IPV4"] = []
        time.sleep(5)
        try:
            indicadores1 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
            indicadores2 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
        except Exception as e:
            indicadores1, indicadores2 = [], []
        for fila in indicadores1 + indicadores2:
            infoPulso["IPV4"].append(fila.text)
            print("IPV4", fila.text)

        """BUSCAR HOSTAME"""
        barraBusqueda.clear()
        barraBusqueda.send_keys("hostname")
        infoPulso["hostname"] = []
        time.sleep(5)
        try:
            indicadores1 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
            indicadores2 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
        except Exception as e:
            indicadores1, indicadores2 = [], []
        for fila in indicadores1 + indicadores2:
            infoPulso["hostname"].append(fila.text)
            print("hostname", fila.text)

        """BUSCAR DOMAIN"""
        barraBusqueda.clear()
        barraBusqueda.send_keys("domain")
        infoPulso["domain"] = []
        time.sleep(5)
        try:
            indicadores1 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
            indicadores2 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
        except Exception as e:
            indicadores1, indicadores2 = [], []
        for fila in indicadores1 + indicadores2:
            infoPulso["domain"].append(fila.text)
            print("domain", fila.text)

        """BUSCAR EMAIL"""
        barraBusqueda.clear()
        barraBusqueda.send_keys("email")
        infoPulso["email"] = []
        time.sleep(5)
        try:
            indicadores1 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
            indicadores2 = driver.find_elements_by_xpath("//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
        except Exception as e:
            indicadores1, indicadores2 = [], []
        for fila in indicadores1 + indicadores2:
            infoPulso["email"].append(fila.text)
            print("email", fila.text)
    except Exception as e:
        print("no se pudo extraer")
#driver.quit()
