import requests
import pandas as pd
import os
import time

# ==============================
# CONFIGURAÇÕES
# ==============================
TOKEN = os.getenv("AIRTABLE_TOKEN")

URLS = {
    "forecast.csv": "https://api.airtable.com/v0/appMDw883DjY0pMej/Result%201",
    "depara_skill.csv": "https://api.airtable.com/v0/appnlzAmDtFtGBjyt/Result%201"
}

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

PASTA_SAIDA = "saida_csv"

# ==============================
# FUNÇÃO DE EXTRAÇÃO COM PAGINAÇÃO
# ==============================
def extrair_airtable(url, nome_arquivo):
    print(f"Iniciando extração: {nome_arquivo}")

    registros = []
    offset = None

    while True:
        params = {"offset": offset} if offset else {}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()

        data = response.json()
        registros.extend([r["fields"] for r in data.get("records", [])])

        offset = data.get("offset")
        if not offset:
            break

        time.sleep(0.3)  # evita throttling

    df = pd.DataFrame(registros)

    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)
    df.to_csv(caminho, index=False, sep=";", encoding="utf-8-sig")

    print(f"Arquivo {nome_arquivo} gerado com {len(df)} registros.")

# ==============================
# EXECUÇÃO
# ==============================
if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Variável de ambiente AIRTABLE_TOKEN não definida.")

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    for arquivo, url in URLS.items():
        extrair_airtable(url, arquivo)

    print("Extração via API finalizada.")
