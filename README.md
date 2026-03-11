Prova Python – Automação e Tratamento de Dados

Objetivo
Este conjunto de scripts Python foi desenvolvido para automatizar o processo de coleta, extração, organização e tratamento de arquivos operacionais utilizados no relatório Intraday.
O objetivo principal é garantir que os dados sejam obtidos de forma padronizada, íntegra e organizada, facilitando a carga posterior no banco de dados SQL Server e o consumo no Power BI.

Escopo da Solução
Os scripts contemplam as seguintes etapas do processo:

Acesso automatizado a ambiente web autenticado

Download de arquivos operacionais

Extração de arquivos compactados

Leitura e tratamento de dados tabulares

Organização e movimentação de arquivos em diretórios

Preparação dos dados para processos de ETL subsequentes

Estrutura dos Scripts
Os scripts foram desenvolvidos de forma modular, com responsabilidades bem definidas, permitindo fácil manutenção e reaproveitamento.
Cada script executa uma etapa específica do processo, respeitando a ordem lógica de execução da automação e do tratamento dos dados.

Bibliotecas Utilizadas

Bibliotecas externas
As seguintes bibliotecas não fazem parte da biblioteca padrão do Python e estão listadas no arquivo requirements.txt:

pandas
Utilizada para leitura, manipulação, limpeza e transformação de dados tabulares.

requests
Utilizada para realização de requisições HTTP e download de arquivos.

selenium
Utilizada para automação de navegação web, especialmente em ambientes que exigem autenticação e interação com elementos dinâmicos.

Bibliotecas padrão do Python
As bibliotecas abaixo fazem parte da biblioteca padrão do Python e não requerem instalação adicional:

os

time

glob

shutil

zipfile

Essas bibliotecas são utilizadas para manipulação de arquivos, diretórios, controle de tempo e extração de arquivos compactados.

Dependências
Todas as dependências externas necessárias para execução dos scripts estão listadas no arquivo requirements.txt.

Para instalação das dependências, executar o seguinte comando:

pip install -r requirements.txt

Conteúdo do arquivo requirements.txt:

pandas
requests
selenium

Observações Técnicas
Os scripts foram desenvolvidos utilizando bibliotecas amplamente utilizadas no mercado.
O uso do Selenium se justifica pela necessidade de interação com páginas web autenticadas e dinâmicas.
O código foi estruturado visando clareza, organização e facilidade de manutenção.
O tratamento de arquivos e dados foi pensado para evitar retrabalho e garantir consistência no processo de carga.

Resultado Esperado
Ao final da execução dos scripts, os arquivos estarão organizados e prontos para serem utilizados nos processos de carga em banco de dados e na construção dos dashboards no Power BI, conforme especificado na prova.