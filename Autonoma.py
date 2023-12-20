from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException
import time
import re
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)



PageNum = 1

def UserName():
    url = navegador.current_url
    parsed_url = urlparse(url)

# Obtém a parte do caminho da URL
    caminho = parsed_url.path

# Divide o caminho usando "/" como delimitador
    partes_do_caminho = caminho.split("/")

# Se houver pelo menos duas partes, a segunda parte será "Nullity"
    if len(partes_do_caminho) >= 2:
        nome_de_usuario = partes_do_caminho[1]
   
    return  nome_de_usuario
def ProjName(url):
    projName = url.split("/")[4]  # Split by "/" and access the 5th element
    return projName
def RepoName():
    
    time.sleep(0.5)
    url_atual = navegador.current_url
    projName = ProjName(url_atual)
  
    url =  url_atual + "/tree/" + branch + "/" + projName
    return(url)
def CsProjName(url_atual):
   
   
   time.sleep(0.5)
   
   url_atual = navegador.current_url

   projName = ProjName(url_atual)

   csproj =  '.csproj'


   url_atual = url_atual.replace("tree", "blob")
   url_atual = url_atual + "/" + projName  +csproj

   return url_atual
def IsCsProjThere():
    try:
        csproj_element =WebDriverWait(navegador, 2).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "csproj")]')))
        csproj_href = csproj_element.get_attribute('href')
        navegador.get(csproj_href)
        textarea_element = WebDriverWait(navegador, 0.5).until(
        EC.presence_of_element_located((By.ID, 'read-only-cursor-text-area'))
        ) 
        # Obtém o texto dentro do elemento <textarea>
        csproj_text = textarea_element.text 
        # Usa regex para encontrar o valor entre as tags TargetFramework
        padrao = re.compile(r'<TargetFramework>(.*?)</TargetFramework>', re.DOTALL)
        resultado = re.search(padrao, csproj_text) 
        # Se houver uma correspondência, imprima o valor
        if resultado:
         valor_target_framework = resultado.group(1)
         url_atual = navegador.current_url
         projeto = ProjName(url_atual)
         print(i," - ",projeto," - ",valor_target_framework)
         print("--------------------------------------------")
        return csproj_href
    except TimeoutException:
        return "No"
def CheckLogin():  
    try:
        input_element = navegador.find_element(By.LINK_TEXT, "Sign in")  # Example using link text

        if input_element:
            input_element.click()
            time.sleep(1)
            Login()
            return 1
    except NoSuchElementException:
        return 0

def Login():
        input_element = navegador.find_element(By.ID, "login_field")
        input_element.clear()
        print("Insira seu email da Organização:")
        email = input()
        input_element.send_keys(str(email))
        password_element = navegador.find_element(By.ID, "password")
        password_element.clear()
        print("Agora, insira sua senha:")
        senha = input()
        password_element.send_keys(str(senha))
        submit_button = navegador.find_element(By.CLASS_NAME, "js-sign-in-button")  # Use a reliable identifier
        submit_button.click()

print("Insira o nome da sua organização.")
Usuario = input()
branch  = "master"
("=======================================================")
print("Como padrão iremos checar a branch: ", branch)

navegador.get(str("https://github.com/orgs/"+ Usuario +"/repositories?q=&type=all&language=c%23&sort="))
check = CheckLogin()
print("=======================================================")
print("Conta logada com sucesso, procurando repositórios...")
print("=======================================================")
for i in range(1, 32, 1):
    navegador.get(str("https://github.com/orgs/"+ Usuario +"/repositories?q=&type=all&language=c%23&sort="))

    Repository = WebDriverWait(navegador, 1).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="org-repositories"]/div/div/div[2]/ul/li['+str(i)+']/div/div[1]/div[1]/h3/a'))
    )

    Repository.click()
    IsThereCsProj = IsCsProjThere()
    if IsThereCsProj == "No":
        folder = WebDriverWait(navegador, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='folder-row-1']/td[2]/div/div/h3/div/a"))
        )
        folder.click()
        time.sleep(2)
        IsThereCsProj = IsCsProjThere()
        if IsThereCsProj == "No":
            folder = WebDriverWait(navegador, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='folder-row-1']/td[2]/div/div/h3/div/a"))
            )
            folder.click()
            time.sleep(2)
            IsThereCsProj = IsCsProjThere()
            if IsThereCsProj == "No":
                time.sleep(1)
                url_atual = navegador.current_url
                projeto = ProjName(url_atual)
                print(i," - ",projeto," - ","Não encontrado")
                print("--------------------------------------------")

    else:
        IsCsProjThere()


print("Created by Nuullity & NRLacerda")

navegador.quit()