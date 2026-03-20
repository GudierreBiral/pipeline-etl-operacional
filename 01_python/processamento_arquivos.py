import pandas as pd
import zipfile
import os
import glob
import shutil

# ==============================
# DEFINIÇÃO DE DIRETÓRIOS
# ==============================
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_RAIZ = os.path.dirname(DIRETORIO_SCRIPT)
PASTA_ENTRADA = os.path.join(PASTA_RAIZ, "saida_csv")
PASTA_EXTRACAO = os.path.join(PASTA_ENTRADA, "extraido_temp")
ARQUIVO_ZIP = os.path.join(PASTA_ENTRADA, "archive.zip")

# ==============================
# FUNÇÃO DE LIMPEZA PADRÃO
# ==============================
def limpar_strings(df):
    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace("\n", " ", regex=False)
            .str.replace("\r", "", regex=False)
        )
    return df

# ==============================
# CONSOLIDAÇÃO DOS ARQUIVOS
# ==============================
def consolidar(lista_arquivos, tipo):
    if not lista_arquivos:
        print(f"Nenhum arquivo encontrado para {tipo}")
        return

    print(f"Processando {tipo}...")

    dfs = []
    for arq in lista_arquivos:
        if arq.endswith(".xlsx"):
            dfs.append(pd.read_excel(arq))
        else:
            dfs.append(pd.read_csv(arq, sep=";", encoding="utf-8"))

    df = pd.concat(dfs, ignore_index=True)

    # ==============================
    # HSPLIT – VOLUMETRIA
    # ==============================
    
    if tipo == "HSPLIT":
        # Mapeamento desejado (modelo conceitual)
        mapa = {
            "row_date": "Data",
            "intrvl": "Intervalo",
            "acd": "ACD",
            "split": "Split",
            "inflowcalls": "Chamadas_Recebidas",
            "acdcalls": "Chamadas_Atendidas",
            "acdtime": "Tempo_Falado",
            "anstime": "Tempo_Espera"
        }
        
        # Seleciona apenas colunas existentes
        colunas_existentes = {k: v for k, v in mapa.items() if k in df.columns}
        df = df[list(colunas_existentes.keys())].rename(columns=colunas_existentes)

        # Agregação intraday
        df = (
            df.groupby(["Data", "Intervalo", "ACD", "Split"], as_index=False)
            .sum()
        )


    # ==============================
    # HAGENT – TEMPOS DE AGENTE
    # ==============================
    elif tipo == "HAGENT":
        # Mapeamento base obrigatório
        mapa = {
            "row_date": "Data",
            "intrvl": "Intervalo",
            "acd": "ACD",
            "split": "Split",
            "i_stafftime": "Tempo_Logado",
            "i_availtime": "Tempo_Disponivel",
            "ti_auxtime": "Tempo_Pausa"
        }

        # Seleciona apenas colunas existentes
        colunas_existentes = {k: v for k, v in mapa.items() if k in df.columns}
        df = df[list(colunas_existentes.keys())].rename(columns=colunas_existentes)

        # Consolidação intraday (remove granularidade por agente)
        df = (
            df.groupby(["Data", "Intervalo", "ACD", "Split"], as_index=False)
            .sum()
        )

    # ==============================
    # FORECAST
    # ==============================
    elif tipo == "FORECAST":
        import re

        print("Processando FORECAST...")

        # ----------------------------------
        # Normalização forte de colunas
        # ----------------------------------
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("%", "")
            .str.replace("(", "")
            .str.replace(")", "")
            .str.replace(".", "")
        )

        # ----------------------------------
        # Função auxiliar para localizar colunas
        # ATENÇÃO: padrões devem refletir colunas já normalizadas
        # ----------------------------------
        def encontrar_coluna(padroes):
            for col in df.columns:
                for p in padroes:
                    if re.search(p, col):
                        return col
            return None

        # ----------------------------------
        # Mapeamento correto conforme arquivo real
        # ----------------------------------
        col_data = encontrar_coluna(["data", "date", "dia"])
        col_intervalo = encontrar_coluna(["intervalo"])
        col_volume = encontrar_coluna(["volume_oferecidas"])
        col_tma = encontrar_coluna(["tmo_previsto"])
        col_ns = encontrar_coluna(["ns_previsto"])
        col_hc = encontrar_coluna(["hc_previsto"])

        # ----------------------------------
        # Validação mínima obrigatória
        # ----------------------------------
        if not col_data or not col_intervalo:
            raise ValueError("FORECAST sem Data ou Intervalo")

        if not col_volume or not col_tma or not col_ns:
            raise ValueError("FORECAST sem colunas métricas obrigatórias")

        # ----------------------------------
        # Renomeação explícita
        # ----------------------------------
        renomear = {
            col_data: "Data",
            col_intervalo: "Intervalo",
            col_volume: "Volume_Forecast",
            col_tma: "TMA_Forecast",
            col_ns: "NS_Forecast"
        }

        if col_hc:
            renomear[col_hc] = "HC_Forecast"

        df = df.rename(columns=renomear)

        # ----------------------------------
        # Skill não existe no forecast
        # ----------------------------------
        df["Skill"] = "GLOBAL"

        # ----------------------------------
        # Conversões numéricas
        # ----------------------------------
        df["Volume_Forecast"] = pd.to_numeric(df["Volume_Forecast"], errors="coerce")

        df["TMA_Forecast"] = (
            df["TMA_Forecast"]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df["TMA_Forecast"] = pd.to_numeric(df["TMA_Forecast"], errors="coerce")

        # TMO previsto vem em minutos → converter para segundos
        df["TMA_Forecast"] = df["TMA_Forecast"] * 60

        df["NS_Forecast"] = (
            df["NS_Forecast"]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df["NS_Forecast"] = pd.to_numeric(df["NS_Forecast"], errors="coerce")

        if "HC_Forecast" in df.columns:
            df["HC_Forecast"] = pd.to_numeric(df["HC_Forecast"], errors="coerce")

        # ----------------------------------
        # Agregação correta por granularidade
        # ----------------------------------
        aggs = {
            "Volume_Forecast": "sum",
            "TMA_Forecast": "mean",
            "NS_Forecast": "mean"
        }

        if "HC_Forecast" in df.columns:
            aggs["HC_Forecast"] = "mean"

        df = (
            df
            .groupby(["Data", "Intervalo", "Skill"], as_index=False)
            .agg(aggs)
        )

        print("FORECAST processado com sucesso.")

    # ==============================
    # DEPARA SKILL
    # ==============================
    elif tipo == "DEPARA_SKILL":
        df = df.rename(columns={
            "SKILL": "Skill_Tecnica",
            "SKILL_FORECAST": "Skill_Forecast",
            "OPERACAO": "Operacao",
            "SEGMENTO": "Segmento"
        })

        df["id_skill"] = range(1, len(df) + 1)

    # ==============================
    # LIMPEZA FINAL
    # ==============================
    df = limpar_strings(df)

    # Preenche nulos apenas em métricas
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        df[col] = df[col].fillna(0)

    # ==============================
    # EXPORTAÇÃO
    # ==============================
    caminho_csv = os.path.join(PASTA_ENTRADA, f"{tipo.lower()}.csv")
    df.to_csv(
        caminho_csv,
        index=False,
        sep=";",
        encoding="utf-8",
        decimal=".",
        quoting=1
    )

    print(f"{tipo.lower()}.csv gerado com sucesso.")

# ==============================
# ORQUESTRAÇÃO
# ==============================
def processar_dados():
    print("Iniciando processamento...")

    if os.path.exists(ARQUIVO_ZIP):
        with zipfile.ZipFile(ARQUIVO_ZIP, "r") as zip_ref:
            zip_ref.extractall(PASTA_EXTRACAO)
        print("ZIP extraído.")

    arquivos_hsplit = glob.glob(os.path.join(PASTA_EXTRACAO, "HSPLIT*.xlsx"))
    arquivos_hagent = glob.glob(os.path.join(PASTA_EXTRACAO, "HAGENT*.xlsx"))
    arquivos_forecast = glob.glob(os.path.join(PASTA_ENTRADA, "forecast.csv"))
    arquivos_depara = glob.glob(os.path.join(PASTA_ENTRADA, "depara_skill.csv"))

    consolidar(arquivos_hsplit, "HSPLIT")
    consolidar(arquivos_hagent, "HAGENT")
    consolidar(arquivos_forecast, "FORECAST")
    consolidar(arquivos_depara, "DEPARA_SKILL")

    # Limpeza final
    if os.path.exists(PASTA_EXTRACAO):
        shutil.rmtree(PASTA_EXTRACAO)

    if os.path.exists(ARQUIVO_ZIP):
        os.remove(ARQUIVO_ZIP)

    print("Processamento finalizado com sucesso.")

# ==============================
# EXECUÇÃO
# ==============================
if __name__ == "__main__":
    processar_dados()
