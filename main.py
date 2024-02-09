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
    
def append_table_to_txt(wait):
    output_file = 'horario.txt'
    lun_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_71:j_id_7e_container"]/div[1]/div[3]/h2'))).text
    lun_date = lun_date.split('–')[0].strip()
    mes_abreviado = meses_abreviados.get(lun_date[:3])
    fecha_completa = datetime.strptime(f"{mes_abreviado} {lun_date[4:]} 2024", "%b %d %Y")
    try:
        Clases = []
        clases = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class*='fc-title']")))
        
        for clase in clases:
            if clase.text != '':
                clase.click()
                sleep(0.2)
                text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class*='ui-dialog']"))).text.split('\n')
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_71:addButton"]'))).click()
                sleep(0.2)
                Clases.append(Clase(text))
                print(Clases[-1])
                

        # Añadir los datos al archivo de texto
        Clases.sort(key=lambda x: x.fecha)
        with open(output_file, 'a', encoding='utf-8') as file:
            for clase in Clases:
                file.write(str(clase))

        print(f"Datos de la semana del {lun_date} añadidos al archivo {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        pass

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
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_71:j_id_7e_container"]/div[1]/div[2]/div/button[1]'))).click()

    if path.exists('horario.txt'):
        remove('horario.txt')
    
    print("Descargando...")
    texto_actual = ''
    while texto_actual != texto_final:
        texto_actual = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id_71:j_id_7e_container"]/div[1]/div[3]/h2'))).text
        sleep(1)
        append_table_to_txt(wait)
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

class Clase:
    def __init__(self, fecha, hora_ini, hora_fin, aula, asignatura, clase_tipo):
        self.fecha = fecha
        self.hora_ini = hora_ini
        self.hora_fin = hora_fin
        self.aula = aula
        self.asignatura = asignatura
        self.clase_tipo = clase_tipo
        
    def __init__(self, text):
        self.fecha_str = text[2].split(' ')[1]
        self.fecha = datetime.strptime(self.fecha_str, "%d/%m/%Y")
        self.hora_ini = text[2].split(' ')[2]
        self.hora_fin = text[3].split(' ')[2]
        self.aula = text[1].split(' - ')[1]
        self.asignatura = text[0].split(' - ')[0]
        self.clase_tipo = text[0].split(' - ')[1]
        pass
    
    def __str__(self):
        return f'{self.fecha.strftime("%A")} - {self.fecha.strftime("%d/%m/%Y")}\n({self.hora_ini} - {self.hora_fin})\t{self.asignatura}\n{self.aula}\t{self.clase_tipo}\n\n'

if __name__ == '__main__':
    try:
        descargar()
    except Exception as e:
        print(f"Error: {e}")
        