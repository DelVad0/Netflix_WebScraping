from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time 
import random
import requests


#Creando variables y preparando el web driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-notifications")
path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path, options=options)
MY_EMAIL = 'Introduce here your email'
MY_PASSWORD = 'Introduce here your password'
MY_PROFILE_NAME = 'Introduce here your Netflix profile name'
top10 = []
top10_imgs = []
horror_film_names = []
horror_film_year = []
horror_film_duration = []


#Funcion que abre Netflix con el drive Chrome, aceptar Cookies, desclikar "recuerdame" e iniciar sesión.
def start_netflix():
    driver.maximize_window()
    time.sleep(1)
    driver.get('http://netflix.com/es/')
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-accept btn-red'.replace(' ', '.')))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/a'))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/a[2]'))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#id_userLoginId'))).send_keys(MY_EMAIL)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#id_password'))).send_keys(MY_PASSWORD)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[3]/div/label'))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn login-button btn-submit btn-small'.replace(' ', '.')))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[2]/div/a/div/div'))).click()

#Pasar pagina y asi acceder a todos los datos para luego guardarlos en el TOP10    
def pass_page():
    button = driver.find_element(By.XPATH, "//*[@id='row-4']/div/div/div/span")
    actions = ActionChains(driver)
    actions.move_to_element(button).perform()
    time.sleep(5) 
    button.click()

#Mutea la serie que sale en la pagina principal para que no sea molesto el sonido
def mute_page():
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/span/div/div/div/div/div/div[1]/div[2]/div[2]/span[1]/div'))).click()
    except:
        pass

#Obtiene una lista con el nombre de las series TOP10 del dia en Netflix España
def get_top10_data():
    time.sleep(random.uniform(4.0, 6.0))
    shows = driver.find_element(By.ID, 'row-4')
    names = shows.text
    names = names.split('\n')
    for name in names:
        if "/" in name or ":" in name:
            name = name.replace("/", "_")
            name = name.replace(":", "")
        if name not in top10:
            top10.append(name)


#Guarda las imagenes de las series del top 10 en local con su correspondiente nombre 
def save_imgs():
    name_position = 0
    shows = driver.find_element(By.ID, 'row-4')
    urls = shows.find_elements(By.CLASS_NAME, 'boxart-image-in-padded-container')
    for url in urls[1:]:
        img = url.get_attribute('src')
        if img not in top10_imgs:
            top10_imgs.append(img)
            try:
                with open(f"images/{top10[name_position]}.jpg", "wb") as f:
                    f.write(requests.get(img).content)
            except Exception as e:
                print(f"No se pudo guardar la imagen {img}: {e}")
            name_position +=1


#Función que se deplaza a sección peliculas, selecciona las de terror y aplica el filtro por año de lanzamiento
def go_to_horror_films():
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div/ul/li[4]'))).click()
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]'))).click()
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[2]/ul[3]/li[6]'))).click()
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div/div/button'))).click()
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div'))).click()
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/ul/li[2]/a'))).click()
    time.sleep(random.uniform(4.0, 6.0))
      
     
#Obtiene los datos de todas las peliculas de terror de la web(nombre, año, duración) para despues guardarlas en un csv
#recorre todas las peliculas y acceciendo a sus datos, imprime por pantalla cuando la pelicula se ha añadido correctamente
def get_horror_films_data():
    driver.execute_script("window.scrollBy(0, 175)")
    terror_films = driver.find_elements(By.CLASS_NAME, 'title-card')
    for film in terror_films:
        try:
            film_name = film.text
            horror_film_names.append(film_name) 
            film.click()
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'global-supplemental-audio-toggle'))).click()
            film_year = driver.find_element(By.CLASS_NAME, "year").text
            film_duration = driver.find_element(By.CLASS_NAME, "duration").text          
            horror_film_year.append(film_year)
            horror_film_duration.append(film_duration)
            WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CLASS_NAME, 'previewModal-close'))).click()
            time.sleep(random.uniform(4.0, 5.0))
            print(f"{film_name} añadida")
            num+=1
        except Exception as e:
            print(f"Error {e} con la pelicula {film_name}")


#Ejecución de las funciones
start_netflix()
mute_page()
get_top10_data()
pass_page()
get_top10_data()
print(top10)
save_imgs()
go_to_horror_films()
get_horror_films_data()
driver.execute_script("window.scrollBy(0, 175)")
get_horror_films_data()
df = pd.DataFrame({'Names': horror_film_names, 'Year': horror_film_year, 'Duration': horror_film_duration})
print(df)
df.to_csv('horror_film_data.csv', index=False)
driver.quit()


