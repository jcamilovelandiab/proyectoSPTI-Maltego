# -*- coding: utf-8 -*-
import urllib
from MaltegoTransformPY27 import *
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
from selenium.webdriver.common.keys import Keys

m = MaltegoTransform()
m.parseArguments(sys.argv)
country = sys.argv[1]
#country = "Colombia"

m.addUIMessage("COMENZANDO")

chrome_options = Options()
driver = None

'''
BUSQUEDA DEL PAIS
'''
try:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), chrome_options=chrome_options)
    rutaPais = "https://otx.alienvault.com/browse/pulses?q=country:%20" + country
    driver.get(rutaPais)
except Exception as e:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
    rutaPais = "https://otx.alienvault.com/browse/pulses?q=country:%20" + country
    driver.get(rutaPais)

try:
    '''
    CANTIDAD DE PULSOS
    '''
    time.sleep(5)
    numeroDePulsos = int(driver.find_element_by_xpath("/html/body/app-root/app-header/nav/ul/li[1]/a/span").text)


    '''
    CARGA DE LA PAGINA COMPLETA
    '''

    numeroDePulsos = min(numeroDePulsos,4)
    html = driver.find_element_by_tag_name('html')
    for i in range((numeroDePulsos//10) + 1):
        html.send_keys(Keys.END)
        time.sleep(3)

    '''
    OBTENCION DE LOS PULSOS
    '''
    pulsos = driver.find_elements_by_xpath("/html/body/app-root//div[1]/div[1]/app-browse/div[1]/div/div[2]/div/div/*/div/*")
    urlsPulsos = []
    count=0
    #print("URL PULSOS")

    for pulso in pulsos:
        urlsPulsos.append("https://otx.alienvault.com/" + pulso.get_attribute("id").replace("-", "/"))
        count+=1
        #print urlsPulsos[-1]
        if count >= numeroDePulsos: break

    #print("PULSOS:")
    for pulso in urlsPulsos:
        infoPulso = {}
        driver.get(pulso)
        time.sleep(5)
        namePulse = driver.find_element_by_xpath("/html/body/app-root/div[1]/div[1]/app-pulse-detail/div[1]/div/div/div/header/div[1]/h1").text

        ent = m.addEntity('osint.Pulse', namePulse.encode('utf8'))

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
            cnt=0
            for fila in indicadores1 + indicadores2:
                infoPulso["URL"].append(fila.text)
                #print("URL",fila.text)
                #ent.addAdditionalFields("URL", "URL", True, (fila.text).encode('utf8'))
                url = fila.text[:-1]
                ent2 = m.addEntity('osint.URL', url.encode('utf8'))
                if cnt>2: break
                cnt+=1

            """BUSCAR EMAIL"""
            barraBusqueda.clear()
            barraBusqueda.send_keys("email")
            infoPulso["email"] = []
            time.sleep(5)
            try:
                indicadores1 = driver.find_elements_by_xpath(
                    "//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
                indicadores2 = driver.find_elements_by_xpath(
                    "//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
            except Exception as e:
                indicadores1, indicadores2 = [], []
            cnt=0
            for fila in indicadores1 + indicadores2:
                infoPulso["email"].append(fila.text)
                email = fila.text
                ent3 = m.addEntity('maltego.EmailAddress', email)
                if cnt>2: break
                cnt+=1

            """BUSCAR DOMAIN"""
            barraBusqueda.clear()
            barraBusqueda.send_keys("domain")
            infoPulso["domain"] = []
            time.sleep(5)
            try:
                indicadores1 = driver.find_elements_by_xpath(
                    "//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
                indicadores2 = driver.find_elements_by_xpath(
                    "//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
            except Exception as e:
                indicadores1, indicadores2 = [], []
            cnt=0
            for fila in indicadores1 + indicadores2:
                infoPulso["domain"].append(fila.text)
                domain = fila.text
                ent4 = m.addEntity('maltego.Domain', domain)
                if cnt>2: break
                cnt+=1

            """BUSCAR IPV4"""
            barraBusqueda.clear()
            barraBusqueda.send_keys("IPV4")
            infoPulso["IPV4"] = []
            time.sleep(5)
            try:
                indicadores1 = driver.find_elements_by_xpath(
                    "//tbody/*[@class='show-row no-footer even']/td[2]/a/span/span")
                indicadores2 = driver.find_elements_by_xpath(
                    "//tbody/*[@class='show-row no-footer odd']/td[2]/a/span/span")
            except Exception as e:
                indicadores1, indicadores2 = [], []
            cnt=0
            for fila in indicadores1 + indicadores2:
                infoPulso["IPV4"].append(fila.text)
                ipv4 = fila.text
                ent5 = m.addEntity('maltego.IPv4Address', ipv4.encode)
                if cnt>2: break
                cnt+=1

        except Exception as e:
            #print("no se pudo extraer la informacion")
            continue
except Exception as error:
    m.addUIMessage("no se pudo extraer la informacion")
    m.addUIMessage(error.__str__())
m.returnOutput()
driver.quit()
