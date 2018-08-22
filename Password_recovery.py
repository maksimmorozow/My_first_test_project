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
import arrow




#Исходные данные
phone="700-153-00-00"
mail="test153@gmail.com"
password_new="Qq111112"



#заходим на сайт 
driver = webdriver.Chrome()
driver.get("http://p2.modulbank.ru/#/signin")
#Вводим логин
input_phone = driver.find_element_by_name("tel")
input_phone.clear()
input_phone.send_keys(phone)
#открываем ссылку на восстановление пароля
recovery_link = driver.find_element_by_partial_link_text("ЗАБЫЛИ").get_attribute("href")
driver.get(recovery_link)
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'button')))
button_next = driver.find_element_by_class_name("button")
button_next.click()  #кликаем на кнопку восстановления пароля, после чего в папку падает письмо
time.sleep(10)


#Копируем письмо с сообщением для восстановления в локальную папку
now = datetime.datetime.now()
path=r"\\172.21.13.66\mails" +"\\" + mail + "\\"+ arrow.now().format('D_M_YYYY') +"\\"
files = os.listdir(path)
files = [os.path.join(path, file) for file in files]
files = [file for file in files if os.path.isfile(file)]
source_file = max(files, key=os.path.getctime)
#source_file =r"\\172.21.13.66\mails\test153@gmail.com\17_8_2018\7b3ad3df-3770-4c01-a25f-3c4eeeb47084.eml"
dest_file = r'D:\1\temp.eml'
shutil.copy2(source_file, dest_file)



#Открываем файл eml и получаем из него ссылку
with open(dest_file, 'rb') as fhdl:
    raw_email = fhdl.read()
#Получаем дамп файла
parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email, include_raw_body=True)
def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
jsondata = json.dumps(parsed_eml, default=json_serial) #json строка с письмом

#Ищем по содержимому письма подстроку с recoverpassword
s=jsondata.find('recoverpassword')
k1=jsondata.rindex('http', 1, s) #начало ссылки на запрос восстановления пароля
k2=s+58  #конец ссылки на восстановление пароля, подсчитан, получаем ссылку.
link1=jsondata[k1:k2]


#открыть ссылку на восстановление пароля
#link1="http://p2.modulbank.ru/#/goto/account/recoverpassword?token=6140a742-f2ff-4695-ac47-91e4a88f5221"
driver = webdriver.Chrome()
driver.get(link1)  
#time.sleep(5)
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.NAME,'password')))
input_pass1 = driver.find_element_by_name('password')
input_pass1.clear()
input_pass1.send_keys(password_new)
input_pass2 = driver.find_element_by_name('repeatPassword')
input_pass2.clear()
input_pass2.send_keys(password_new)

WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'button')))
button_submit = driver.find_element_by_class_name("button")
button_submit.click()
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.NAME,'smsCode')))
input_sms = driver.find_element_by_name("smsCode")
input_sms.clear()
input_sms.send_keys("11111")

time.sleep(5)
#driver.close()

