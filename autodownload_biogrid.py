"""
Usage: 
"""
#!/usr/bin/python3

from sys import argv
, gene_list, species = argv
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

genes = []
genes = [i.lower() for i in genes]

for gene in genes:
    cs_url = 'https://thebiogrid.org/search.php?search='+ gene +'&organism=all'
    r = requests.get(cs_url)
    text = str(r.content)
    url_list = re.findall(r'https://thebiogrid.org/\d+/summary/[\w-]+/', text)
    
    if len(url_list) > 0:
        url_list = [i for i in url_list if i[-13:-1] == 'homo-sapiens']
        geneID = [j[j.find('/',21)+1 : j.find('/',23)] for j in url_list]

        if len(geneID) > 0:
            url = 'https://thebiogrid.org/downloadgenerator.php?geneID=' + geneID[0]
            driver.get(url)  
            try:
                elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "buildGeneButton"))) 
            finally:
                elem.click()
            try:
                elem = WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "customDownloadButton")))    
            finally:
                elem.click()
        else:
            print (gene+' no homo-sapiens')
    else:
        print(gene+' did not find any')