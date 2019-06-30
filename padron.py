from selenium import webdriver
from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product
from elasticsearch import Elasticsearch
es = Elasticsearch()

browser = webdriver.Firefox()

url = 'https://e2019.uy/buscar'

for combinacion in product(ascii_uppercase,repeat=3):
    serie = ''.join(combinacion)

    for numero in range (0, 99999):
        doc = {}
        browser.get(url)
        input_serie = browser.find_element_by_name("serieCredencial")
        input_numero = browser.find_element_by_name("numeroCredencial")
        boton = browser.find_elements_by_class_name("primary")[0]

        input_serie.send_keys(serie)
        input_numero.send_keys("%d" % numero)
        boton.click()

        try:
            info = browser.find_elements_by_class_name("information-container")[0]
            lines = info.text.splitlines()

            doc["nombre"] = lines[0]
            doc["primerNombre"] = lines[0].split()[0]
            doc["serie"] = serie
            doc["numero"] = numero
            doc["circuito"] = int(lines[4])
            doc["local"] = lines[6]
            doc["direccion"] = lines[8]

            res = es.index(index="padron", id="%s%d" % (serie,numero), body=doc)
            print(res)

        except:
            pass

browser.quit()
