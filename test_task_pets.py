import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture()
def driver():
    driver = webdriver.Chrome('c:/to/chromedriver.exe')
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver
    driver.quit()



def test_my_pets_explicit(driver):
    # Явное ожидание.
    time.sleep(5)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    # Ввод логина
    time.sleep(1)
    driver.find_element(By.ID, 'email').send_keys('patst44@yandex.ru')
    # Ввод пароля
    time.sleep(1)
    driver.find_element(By.ID, 'pass').send_keys('kill1234')
    # Нажатие кнопки ввода
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверка что находимся на главной странице пользователя
    time.sleep(5)
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'
    driver.save_screenshot('result_explicit.png')


def test_my_pets_implicit(driver):
    # Неявное ожидание.
    time.sleep(2)
    driver.find_element(By.ID, 'email').send_keys('patst44@yandex.ru')
    time.sleep(2)
    driver.find_element(By.ID, 'pass').send_keys('kill1234')
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'
    driver.save_screenshot('result_implicit.png')