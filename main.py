from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime, timedelta
from os import path, remove

# Ultima semana del curso con clases, o eventos a guardar
texto_final = 'Abr 29 – May 5, 2024' 

meses_abreviados = {
    'Ene': 'Jan',
    'Feb': 'Feb',
    'Mar': 'Mar',
    'Abr': 'Apr',
    'May': 'May',
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Ago': 'Aug',
    'Sep': 'Sep',
    'Oct': 'Oct',
    'Nov': 'Nov',
    'Dic': 'Dec',
}

def fill_credentials(wait):
    
    sleep(1)
    campo_usuario = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
    campo_usuario.clear()
    campo_usuario.send_keys(credentials()['user'])
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="idSIButton9"]'))).click()
    
    sleep(1)
    campo_passw = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
    campo_passw.clear()
    campo_passw.send_keys(credentials()['password'])
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="idSIButton9"]'))).click()
    
def append_table_to_txt(driver):
    output_file = 'horario.txt'
    month_date = driver.find_element(By.XPATH, '//*[@id="j_id_71:j_id_7e_container"]/div[1]/div[3]/h2').text
    
    try:
        clases = []
        days_n = []
        
        days = driver.find_elements(By.CSS_SELECTOR, "[class*='fc-day']")
        
        for day in days:
            # print(day_head.get_attribute('data-date'))
            days_n.append(day.get_attribute('data-date')) if day.get_attribute('data-date') not  in days_n else None
                
        for day in days_n:
            print(day)
        
        pass
        
        # # Lunes
        # clases.append(f"Lunes {fecha_completa.strftime('%d/%m/%Y')}")
        # clases.append(table[1].text + '\n')
        
        # # Martes
        # fecha_completa = fecha_completa + timedelta(days=1)
        # clases.append(f"Martes {fecha_completa.strftime('%d/%m/%Y')}")
        # clases.append(table[3].text + '\n')

        # # Miercoles
        # fecha_completa = fecha_completa + timedelta(days=1)
        # clases.append(f"Miercoles {fecha_completa.strftime('%d/%m/%Y')}")
        # clases.append(table[5].text + '\n')
        
        # # Jueves
        # fecha_completa = fecha_completa + timedelta(days=1)
        # clases.append(f"Jueves {fecha_completa.strftime('%d/%m/%Y')}")
        # clases.append(table[7].text + '\n')
        
        # # Viernes
        # fecha_completa = fecha_completa + timedelta(days=1)
        # clases.append(f"Viernes {fecha_completa.strftime('%d/%m/%Y')}")
        # clases.append(table[9].text + '\n')

        # # Añadir los datos al archivo de texto
        # with open(output_file, 'a', encoding='utf-8') as file:
        #     # file.write(f'{fecha_completa.strftime("%d/%m/%Y")}\n')
        #     for c in clases:
        #         file.write(f'{c}\n')

        # print(f"Datos de la semana del {lun_date} añadidos al archivo {output_file}")

    except Exception as e:
        print(f"Error: {e}")

def descargar():
    url = "https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.faces"
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', False)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    driver.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContenedorProviders"]/div[1]/span/div'))).click()
    
    fill_credentials(wait)
    
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/p/a'))).click()
    
    driver.get(url)
        
    # Change to the month view
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_71:j_id_7e_container"]/div[1]/div[2]/div/button[1]'))).click()

    if path.exists('horario.txt'):
        remove('horario.txt')
    
    print("Descargando...")
    texto_actual = ''
    while texto_actual != texto_final:
        texto_actual = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_71:j_id_7e_container"]/div[1]/div[3]/h2'))).text
        sleep(1)
        append_table_to_txt(driver)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_71:j_id_7e_container"]/div[1]/div[1]/div/button[2]'))).click()

def credentials():
    ret = {}
    if path.exists('credentials'):
        with open('credentials', 'r') as file:
            lines = file.readlines()
            ret['user'] = lines[0].split('=')[1].strip()
            ret['password'] = lines[1].split('=')[1].strip()
        return ret
    else:
        print("No se ha encontrado el archivo 'credentials'\nCreandolo...")
        with open('credentials', 'w') as file:
            file.write("user=\npassword=\n")

if __name__ == '__main__':
    try:
        descargar()
    except Exception as e:
        print(f"Error: {e}")
        