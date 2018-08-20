from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import unittest
import time
import pytest
import shutil
import os
import tempfile
import email
import datetime
import json
import eml_parser
import re
import urlextract
import datetime

"""
now = datetime.datetime.now()
mail="test153@gmail.com"
way=r"\\172.21.13.66\mails\"" + mail + str(now.date) +"_" + str(now.month) +"_" +str(now.year)
password="Qq111111"

"""


#Исходные данные
phone="700-153-00-00"
mail="test153@gmail.com"
password="Qq111111"



#заходим на сайт 
driver = webdriver.Chrome()
driver.get("http://p2.modulbank.ru/#/signin")
#Вводим логин
input_phone = driver.find_element_by_name("tel")
input_phone.clear()
input_phone.send_keys(phone)
#открываем ссылку на восстановление пароля
recovery_link = driver.find_element_by_partial_link_text("Восстановить").get_attribute("href")
driver.get(recovery_link)
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'button')))
button_next = driver.find_element_by_class_name("button")
button_next.click()  #кликаем на кнопку восстановления пароля, после чего в папку падает письмо
time.sleep(10)


#Копируем письмо с сообщением для восстановления в локальную папку
now = datetime.datetime.now()
way=r"\\172.21.13.66\mails\"" + mail + now.day +"_" + now.month +"_" +now.year
source_file = r"\\172.21.13.66\mails\test153@gmail.com\17_8_2018\1e25b609-5bce-49c9-9c6c-31b2b9b3aa1d.eml" #todo переписать
dest_file = r'D:\1\2.eml'
shutil.copy2(source_file, dest_file)


#Открываем файл eml и получаем из него ссылку
dest_file = r'D:\1\2.eml'
with open(dest_file, 'rb') as fhdl:
    raw_email = fhdl.read()
#Получаем дамп файла
parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email, include_raw_body=True)
jsondata=json.dumps(parsed_eml, default=json_serial) #json строка с письмом

#Ищем по содержимому письма подстроку с recoverpassword
s=jsondata.find('recoverpassword')
k1=jsondata.rindex('http', 1, s) #начало ссылки на запрос восстановления пароля
k2=s+58  #конец ссылки на восстановление пароля, подсчитан, получаем ссылку.
link1=jsondata[k1:k2]
#открыть ссылку на восстановление пароля
driver = webdriver.Chrome()
driver.get(link1)  

driver.close()
