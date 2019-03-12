# -*- coding: utf-8 -*-
import urllib
from MaltegoTransform import *
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import ImageTk, Image
import time
import tkinter as tk
import sys
from selenium.webdriver.common.keys import Keys

# user = "H4sIAAAAAAAAAJWUT0hUQRzHZ3fdNF3FFIOIrc1EyPKpUBBoKIbWI81IXUMPNrtv2n3b7JtxZt7uE0nqUEF16FC3oKCOduoUeJHOBkl1qEvUITrUIYLADvV7b/+6aX8Gdubx3u83v8/v+/v9dukzCnIp0I4UzmDNVibVTmKZHMU8WP1m5dnO8y8CKKCj+jiOJ8lszFRpLC8Oo1rKsDGM44oJHW1XSUFkklHD4T9h9Q8gd4WyNbA3ws+vUAjHCVd4jCuTWbZAzTMjXkSKrYQ2FkuRuOq9/fzc/UZ5gPoRcgRqrPyOSsvhsFXZc2gRBdz7i0/B4pOv9BXS64yztCZtS7sAHNLbKVFSI1SbwIlRopLMGHI4pCGBLx/FF/JAdrkgjmtaaYebvrUNfphTOeDmol3J4uHVG+Nfp9f6XAuXpwpY2plIaKkYk1LLEmq4DlNwVl4eC6+8XG8PRfzIN4JqDOBNYEUU2u0J53QR2lXp0gsUPRW3eyWFEMNMZLEwTOu3bN8+bfmxemt5ucBYJ929AUj3FlTbJHc9zWmtePJ6pj+cCRU8sxrq2L+ALUXixCBwyEGCLS1X+wki0qbF5IgpFbGIuIRQZSOMKwGAvY/Xoh8/hRdO+POV9inUmhM3Vz6Sgbu1KKY2OZ4EPzLkvuDcyU6hyS7TMoijOUmVppGBI92Heg53RzIl20L4Y63/Ttrq5DUp7c3Zvv/KtaGUZZSZhtedLW6XATbnvNit1YsCdZQnCzXgzHITntR1i9uq7YxgnAg1f4rMy8JENHktWBZkyLLT5R+97lOonrI4pp504zAAhcH3XAYZo5DCakRcfnVv/Qs03jQKesrlvNGie4SV99I0PBn2+YD34Fa8Y7b6E7B7wR6Vj5ERqCoDymwYc85zUUAlsEvNmkbPZlPPyxUMAFHnVkRRk2TPMvZXpm0US6UbGwXSocoJIpreP3j0/cr1oyCQXhBow//VaTsdI+La0t1w3Z13N4uzDxGiUO1f+XLW2XMFAAA="

m = MaltegoTransform()
m.parseArguments(sys.argv)
cedulaTg = sys.argv[1]
#cedulaTg = "1015470901"


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
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1920x1080")
driver = None
try:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), chrome_options=chrome_options)
    driver.get("https://www.libretamilitar.mil.co/modules/consult/militarysituation")
except Exception as e:
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
    driver.get("https://www.libretamilitar.mil.co/modules/consult/militarysituation")

try:

    bandera = True
    while (bandera):
        try:
            #div= driver.find_element_by_xpath('//div[@id="aspnetForm"]/div[8]/div[6]/div[1]')
            driver.find_element_by_xpath('//select[ @ id = "ctl00_MainContent_drpDocumentType"]/option[text()="Cédula de Ciudadanía"]').click()
            #lista.click()
            bandera = False
        except Exception as e:
            print(e)
    bandera = True
    while (bandera):
        try:
            cedula = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_txtNumberDocument"]')
            cedula.send_keys(cedulaTg)
            bandera = False
        except Exception:
            continue
    bandera = True
    while (bandera):
        try:
            continuarBtn = driver.find_element_by_name("ctl00$MainContent$btnConsult")
            continuarBtn.click()
            bandera = False
        except Exception:
            continue

    nombre="No encontrado"
    libreta = "No encontrado"
    lugar = "No encontrado"
    direccion = "No encontrado"

    bandera = True
    while (bandera):
        try:
            nombre=driver.find_element_by_id("ctl00_MainContent_lblDefinedName").text
            libreta = driver.find_element_by_id("ctl00_MainContent_lblDefinedState").text
            lugar= driver.find_element_by_id("ctl00_MainContent_lblDefinedPlaceText").text
            direccion = driver.find_element_by_id("ctl00_MainContent_lblDefinedAdressText").text
            bandera = False
        except Exception:
            continue
        if(not bandera):
            try:
                error = driver.find_element_by_id("ctl00_MainContent_lblError")
                bandera = False
            except Exception as e:
                print(e)
            time.sleep(3)

    ent = m.addEntity('maltego.Person', nombre.encode('utf8'))
    ent2 = m.addEntity('eci.libreta', libreta.encode('utf8'))
    ent2.addAdditionalFields("lugar", "Lugar", True, lugar.encode('utf8'))
    ent2.addAdditionalFields("direccion", "Direccion", True, direccion.encode('utf8'))

except Exception:
    m.addUIMessage("Cedula no encontrada en la base de datos")

m.returnOutput()
driver.quit()
