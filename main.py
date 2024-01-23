from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime, timedelta

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
   
def append_table_to_txt(driver):
    output_file = 'horario.txt'
    lun_date = driver.find_element(By.XPATH, '//*[@id="j_id_6z:j_id_7c_container"]/div[1]/div[3]').text
    lun_date = lun_date.split('–')[0].strip()
    mes_abreviado = meses_abreviados.get(lun_date[:3])
    fecha_completa = datetime.strptime(f"{mes_abreviado} {lun_date[4:]} 2024", "%b %d %Y")
    try:

        table = driver.find_elements(By.CLASS_NAME, 'fc-event-container')
        clases = []
        
        # Lunes
        clases.append(f"Lunes {fecha_completa.strftime('%d/%m/%Y')}")
        clases.append(table[1].text + '\n')
        
        # Martes
        fecha_completa = fecha_completa + timedelta(days=1)
        clases.append(f"Martes {fecha_completa.strftime('%d/%m/%Y')}")
        clases.append(table[3].text + '\n')

        # Miercoles
        fecha_completa = fecha_completa + timedelta(days=1)
        clases.append(f"Miercoles {fecha_completa.strftime('%d/%m/%Y')}")
        clases.append(table[5].text + '\n')
        
        # Jueves
        fecha_completa = fecha_completa + timedelta(days=1)
        clases.append(f"Jueves {fecha_completa.strftime('%d/%m/%Y')}")
        clases.append(table[7].text + '\n')
        
        # Viernes
        fecha_completa = fecha_completa + timedelta(days=1)
        clases.append(f"Viernes {fecha_completa.strftime('%d/%m/%Y')}")
        clases.append(table[9].text + '\n')

        # Añadir los datos al archivo de texto
        with open(output_file, 'a') as file:
            # file.write(f'{fecha_completa.strftime("%d/%m/%Y")}\n')
            for c in clases:
                file.write(f'{c}\n')


        print(f"Datos de la semana del {lun_date} añadidos al archivo {output_file}")

    except Exception as e:
        print(f"Error: {e}")

def descargar():
    url = "https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.faces"
    print("Descargando...")
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', False)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 100)
    
    driver.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContenedorProviders"]/div[1]/span/div'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/p/a'))).click()
    
    driver.get(url)
    
    # Ultima semana del curso con clases, o eventos a guardar
    texto_final = 'Abr 29 – May 5, 2024' 

    texto_actual = ''
    while texto_actual != texto_final:
        texto_actual = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_6z:j_id_7c_container"]/div[1]/div[3]'))).text
        sleep(1)
        append_table_to_txt(driver)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_6z:j_id_7c_container"]/div[1]/div[1]/div/button[2]'))).click()
        

if __name__ == '__main__':
    descargar()