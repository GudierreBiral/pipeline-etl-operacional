import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================
# CONFIGURAÇÕES
# ==============================
EMAIL_KAGGLE = os.getenv("KAGGLE_EMAIL")
SENHA_KAGGLE = os.getenv("KAGGLE_PASSWORD")

URL_DATASET = "https://www.kaggle.com/datasets/thomassimeo/volumetria-tempos-fictcios"
PASTA_DOWNLOAD = os.path.join(os.getcwd(), "saida_csv")

# ==============================
# CONFIGURAÇÃO DO NAVEGADOR
# ==============================
def configurar_navegador():
    options = Options()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    prefs = {
        "download.default_directory": PASTA_DOWNLOAD,
        "directory_upgrade": True,
        "prompt_for_download": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }

    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver

# ==============================
# EXECUÇÃO PRINCIPAL
# ==============================
def executar_automacao():
    if not EMAIL_KAGGLE or not SENHA_KAGGLE:
        raise RuntimeError("Credenciais Kaggle não definidas nas variáveis de ambiente.")

    os.makedirs(PASTA_DOWNLOAD, exist_ok=True)

    driver = configurar_navegador()
    wait = WebDriverWait(driver, 30)

    try:
        print("Acessando login do Kaggle...")
        driver.get("https://www.kaggle.com/account/login")
        driver.maximize_window()

        btn_email = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Email')]"))
        )
        btn_email.click()

        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL_KAGGLE)
        driver.find_element(By.NAME, "password").send_keys(SENHA_KAGGLE)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        print("Login realizado. Aguarde possíveis validações...")
        time.sleep(8)

        print("Acessando dataset...")
        driver.get(URL_DATASET)

        btn_download = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Download')]"))
        )
        driver.execute_script("arguments[0].click();", btn_download)

        btn_zip = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Download dataset as zip')]"))
        )
        driver.execute_script("arguments[0].click();", btn_zip)

        print("Download iniciado. Aguardando conclusão...")

        # Aguarda o arquivo aparecer
        timeout = time.time() + 60
        while time.time() < timeout:
            arquivos = [f for f in os.listdir(PASTA_DOWNLOAD) if f.endswith(".zip")]
            if arquivos:
                print(f"Arquivo {arquivos[0]} detectado.")
                break
            time.sleep(2)
        else:
            raise TimeoutError("Download não foi concluído no tempo esperado.")

    except Exception as e:
        print(f"Erro durante automação Kaggle: {e}")

    finally:
        print("Automação Kaggle finalizada.")

# ==============================
# START
# ==============================
if __name__ == "__main__":
    executar_automacao()
