# Pipeline ETL Operacional

Pipeline completo de engenharia de dados para coleta, tratamento, modelagem e visualização de dados operacionais de call center — desenvolvido como prova técnica de recrutamento.

O projeto cobre todas as etapas de um pipeline de dados moderno: desde a extração automatizada das fontes até a disponibilização dos indicadores em um dashboard no Power BI.

---

## Visão Geral da Arquitetura

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│      01_python        ──▶       02_sql            ──▶     03_powerbi    │
│                     │     │                      │     │                 │
│  Extração via API   │     │  Staging → Dimensões │     │   Dashboard     │
│  Automação Selenium │     │  Fato → View         │     │   Operacional   │
│  Tratamento Pandas  │     │  Procedure de Carga  │     │                 │
└─────────────────────┘     └──────────────────────┘     └─────────────────┘
```

---

## Estrutura do Repositório

```
pipeline-etl-operacional/
│
├── 01_python/                        # Extração e tratamento dos dados
│   ├── extracao_api.py               # Extração via API Airtable com paginação
│   ├── extracao_kaggle.py            # Automação web com Selenium
│   ├── processamento_arquivos.py     # Limpeza e normalização com Pandas
│   ├── requirements.txt              # Dependências do projeto
│   └── README.md
│
├── 02_sql/                           # Modelagem e carga no SQL Server
│   ├── CRIACAO_Tabelas_de_Staging.sql
│   ├── CRIACAO_Dimensoes_Analiticas.sql
│   ├── CRIACAO_Tabelas_Fato.sql
│   ├── CRIACAO_PROCEDURE.sql
│   ├── CRIACAO_VIEW.sql
│   ├── BULK_INSERT.sql
│   └── README.md
│
├── 03_powerbi/                       # Dashboard de visualização
│   └── README.md
│
└── README.md                         # Este arquivo
```

---

## Etapa 1 — Python: Extração e Tratamento

Os scripts Python automatizam a coleta dos dados a partir de duas fontes distintas e realizam todo o tratamento necessário antes da carga no SQL Server.

### `extracao_api.py` — Extração via API Airtable
- Consumo da API REST do Airtable com autenticação via token (`Bearer`)
- Tratamento de paginação dinâmica com controle de `offset`
- Extração das bases de **Forecast** e **De-Para Skill**
- Sleep entre requisições para evitar throttling da API
- Token gerenciado via variável de ambiente (`AIRTABLE_TOKEN`)
- Geração dos CSVs `forecast.csv` e `depara_skill.csv` em `saida_csv/`

### `extracao_kaggle.py` — Automação Web com Selenium
- Automação do fluxo completo de login no Kaggle
- Configuração do navegador para evitar detecção de automação
- Download automatizado do dataset como `.zip`
- Monitoramento do download com timeout controlado (60s)
- Credenciais gerenciadas via variáveis de ambiente (`KAGGLE_EMAIL`, `KAGGLE_PASSWORD`)

### `processamento_arquivos.py` — Tratamento com Pandas
- Extração automática do `.zip` baixado pelo Selenium
- Processamento modular por tipo de arquivo: **HSPLIT**, **HAGENT**, **FORECAST** e **DEPARA_SKILL**
- Mapeamento e renomeação de colunas para padrão analítico
- Normalização de strings, remoção de caracteres especiais e quebras de linha
- Conversão de tipos numéricos com tratamento de vírgulas decimais
- Conversão de TMO de minutos para segundos
- Agregação intraday por Data, Intervalo, ACD e Split
- Limpeza automática de arquivos temporários após processamento
- Geração dos CSVs tratados prontos para carga no SQL Server

📁 Detalhes técnicos: [`01_python/README.md`](01_python/README.md)

---

## Etapa 2 — SQL Server: Modelagem e Carga

A camada SQL implementa uma arquitetura dimensional para suportar análises operacionais.

### Modelagem dos Dados

| Camada | Tabelas | Descrição |
|--------|---------|-----------|
| **Staging** | `stg_hsplit`, `stg_hagent`, `stg_forecast`, `stg_depara_skill` | Recepção dos CSVs brutos via BULK INSERT |
| **Dimensões** | `dim_tempo`, `dim_intervalo`, `dim_skill` | Contexto analítico: tempo, intervalo e skill |
| **Fato** | `fato_forecast`, `fato_real` | Métricas de planejado vs. realizado |
| **View** | `vw_operacional_consolidado` | Superfície unificada de consumo para o Power BI |

### Procedure de Carga (`sp_tratar_carga_operacional`)

Centraliza toda a lógica de transformação em uma única execução:
- Limpeza controlada das tabelas fato antes de cada carga (evita duplicidade)
- Conversão e sanitização de campos com `TRY_CONVERT` + remoção de caracteres inválidos
- Prevenção de duplicidades nas dimensões com `NOT EXISTS`
- Tratamento de skills não mapeadas via registro padrão (`id_skill = -1`)
- Consolidação dos dados HSPLIT + HAGENT em uma única tabela fato (LEFT JOIN por Data, Intervalo, ACD e Split)

### Tratamento de Inconsistências

Durante o desenvolvimento foram identificadas e documentadas limitações na base original, especialmente em campos de Volume Real, NS Real e dados de pausas. Essas situações foram tratadas por regras de negócio explícitas, garantindo rastreabilidade e transparência no pipeline.

📁 Detalhes técnicos: [`02_sql/README.md`](02_sql/README.md)

---

## Etapa 3 — Power BI: Dashboard Operacional

> Em documentação.

O dashboard consome diretamente a view `vw_operacional_consolidado`, consolidando os indicadores de forecast e realizado em uma única superfície analítica.

📁 Detalhes técnicos: [`03_powerbi/README.md`](03_powerbi/README.md)

---

## Pré-requisitos

### Python
```
python >= 3.10
pandas
requests
selenium
```

### SQL Server
```
SQL Server 2019+
Permissão BULK INSERT no servidor
```

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com:
```env
AIRTABLE_TOKEN=seu_token
KAGGLE_EMAIL=seu_email
KAGGLE_PASSWORD=sua_senha
```

---

## Como Executar

**1. Instalar dependências Python**
```bash
pip install -r 01_python/requirements.txt
```

**2. Executar extração e tratamento**
```bash
python 01_python/extracao_api.py
python 01_python/extracao_kaggle.py
python 01_python/processamento_arquivos.py
```

**3. Criar estrutura no SQL Server**
```sql
-- Execute na ordem:
CRIACAO_Tabelas_de_Staging.sql
CRIACAO_Dimensoes_Analiticas.sql
CRIACAO_Tabelas_Fato.sql
CRIACAO_PROCEDURE.sql
CRIACAO_VIEW.sql
```

**4. Carregar os dados**
```sql
-- Ajuste os caminhos dos arquivos CSV e execute:
BULK_INSERT.sql

-- Em seguida, execute a procedure de carga:
EXEC sp_tratar_carga_operacional
```

**5. Conectar o Power BI**
```
Fonte: SQL Server
Query: SELECT * FROM vw_operacional_consolidado
```

---

## Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)

---

## Autor

**Gudierre Biral**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/seu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/GudierreBiral)
