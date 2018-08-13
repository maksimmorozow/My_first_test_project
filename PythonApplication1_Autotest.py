from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import unittest
import time
import pytest

#Запускаем драйвер и открываем страницу авторизации в ЛК
driver = webdriver.Chrome()
driver.get("http://p2.modulbank.ru/#/signin")

#Вводим логин-пароль
input_phone = driver.find_element_by_name("tel")
input_phone.clear()
input_phone.send_keys("700-153-00-00")

input_pass = driver.find_element_by_name("password")
input_pass.clear()
input_pass.send_keys("Qq111111")

time.sleep(10)
# buttonnext=driver.find_element_by_css_selector('#Далее')
button_next = driver.find_element_by_class_name("button")
button_next.click()

#Ожидаем появления окна ввода СМС и осуществляем вход
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.NAME,'smsCode')))

input_sms = driver.find_element_by_name("smsCode")
input_sms.clear()
input_sms.send_keys("11111")

#Здесь что-то делаем в ЛК (пытаюсь закрыть popup окно с рекламой
s1= "drop header_service_menu drop-element drop-element-attached-top drop-element-attached-center drop-target-attached-bottom drop-target-attached-center drop-out-of-bounds drop-out-of-bounds-left"
s2="popup_close icon-close"
driver.switch_to_window()
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'s2')))
driver.find_element_by_css_selector(s2)

#убедиться в наличии иконки выхода и выйти из ЛК
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'icon-logout')))
icon_logout = driver.find_element_by_class_name("icon-logout")
icon_logout.click()
assert "No results found." not in driver.page_source
driver.close()