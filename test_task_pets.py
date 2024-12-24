import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome('c:/to/chromedriver.exe')
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture()
def go_to_my_pets(driver):
    #time.sleep(2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('patst44@yandex.ru')
    #time.sleep(2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('kill1234')
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    # Нажимаем на ссылку "Мои питомцы"
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()


@pytest.mark.usefixtures("go_to_my_pets")
def test_show_my_pets(driver):
    '''Проверяем что мы оказались на странице "Мои питомцы"'''

    # Проверяем что мы на странице "Мои питомцы"
    assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', f"Это не страница 'Мои питомцы'"


@pytest.mark.usefixtures("go_to_my_pets")
def test_get_all_pets(driver):
    # Ожидаем, пока таблица с питомцами станет доступной
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "all_my_pets"))
    )

    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')
    all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')
    time.sleep(2)
    # Получаем общее количество питомцев
    count_text = driver.find_element(By.CLASS_NAME, 'task3').text
    total_pets = int(count_text.split("\n")[1].split(" ")[-1])
    time.sleep(2)
    # Проверка, что список своих питомцев не пуст
    assert len(all_my_pets) > 0, "Список питомцев пуст!"

    pets_info = []
    pets_names = set()
    pets_with_images = 0

    for i in range(len(all_my_pets)):
        # Получаем информацию о питомце
        pet_info = all_my_pets[i].text.split("\n")
        #time.sleep(2)
        # Проверяем, что существует хотя бы имя питомца
        assert len(pet_info) > 0, f"Нет информации о питомце #{i + 1}"

        pet_name = pet_info[0]
        #time.sleep(2)
        # Проверяем, что имя уникально
        assert pet_name not in pets_names, f"Имя '{pet_name}' повторяется!"
        pets_names.add(pet_name)
        #time.sleep(2)
        # Увеличиваем счетчик для питомцев с изображениями, если они есть
        if len(all_pets_images) > i and all_pets_images[i].get_attribute('src'):
            pets_with_images += 1
       #time.sleep(2)
        # Проверка, что в информации достаточно данных о питомце
        if len(pet_info) < 2:
            raise AssertionError(f"Недостаточно информации о питомце #{i + 1}: {pet_info}")
    #time.sleep(2)
    # Проверка на уникальность питомцев
    unique_pets = len(set(tuple(info) for info in pets_info))
    assert unique_pets == len(
        pets_info), f"Найдены повторяющиеся питомцы! Найдено: {unique_pets}, Ожидалось: {len(pets_info)}"
    #time.sleep(2)
    # Проверка, что хотя бы у половины питомцев есть фото
    assert pets_with_images >= len(all_my_pets) / 2, "Менее половины питомцев имеют фото!"
    #time.sleep(2)
    # Проверка, что количество найденных питомцев соответствует total_pets
    assert len(
