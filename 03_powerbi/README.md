# Dashboard Intraday Operacional — Power BI

## 1. Visão Geral

Dashboard desenvolvido para análise de volumetria, tempos e indicadores de desempenho de operações telefônicas, com foco na comparação **Forecast x Real** em granularidade diária e intradiária.

O relatório foi construído no Power BI consumindo uma view consolidada no SQL Server, priorizando simplicidade de modelagem, performance e consistência nos cálculos.

---

## 2. Fonte de Dados e Modelagem

Os dados são provenientes da view `vw_operacional_consolidado`, que reúne:
- Volumetria (Forecast e Real)
- Tempos operacionais (Logado, Pausa, Falado, Espera)
- Indicadores de desempenho (TMA, NS, Ocupação)

A decisão por utilizar uma única view teve como objetivo:
- Reduzir relacionamentos no Power BI
- Evitar ambiguidades de cardinalidade
- Garantir consistência nos cálculos
- Facilitar manutenção e leitura do modelo

> Não foi criada tabela calendário adicional, pois a granularidade temporal já é atendida pela estrutura da view (data e intervalo).

---

## 3. Estrutura do Relatório

### Página 1 — Visão Geral (Diária)
- Cards de indicadores principais (Volume Previsto, TMA Previsto, HC Previsto, Tempo Falado, Tempo Logado)
- Gráfico comparativo de Volume Forecast x Atendido por dia
- Gráfico de TMA Forecast x TMA Real por dia
- Gráfico de NS Forecast por dia
- Navegação por ícones e filtros interativos de data

**Objetivo:** fornecer uma visão executiva e rápida do desempenho operacional.

### Página 2 — Análise Intraday (Por Intervalo)
- Indicadores de Tempo agregado (Logado, Pausa, Falado, Espera)
- Cards de % Pausas e % Ocupação
- Gráfico de TMA Forecast x TMA Real por intervalo
- Gráfico de Volume Forecast x Volume Real por intervalo
- Gráfico de Tempo Logado x Tempo Pausa
- Tabela resumo com Volume Forecast, Volume Atendido e TMA Real

**Objetivo:** permitir análise granular intradiária, identificando desvios de performance ao longo do dia.

---

## 4. Métricas e Cálculos (DAX)

| Métrica | Descrição | Base |
|---|---|---|
| Volume Recebido | Total de chamadas recebidas | HSPLIT |
| Volume Atendido | Total de chamadas atendidas | HSPLIT |
| TMA | Tempo Falado Total / Chamadas Atendidas | HSPLIT |
| NS | Atendidas NS / (Recebidas - Abandonadas NS) | HSPLIT |
| Tempo Logado | Soma do tempo logado dos agentes | HAGENT |
| Tempo Falado | Soma do tempo em atendimento | HSPLIT |
| % Pausas | Tempo Pausa / Tempo Logado | HAGENT |
| % Ocupação | (Tempo Logado - Pausa - Disponível) / (Tempo Logado - Pausa) | HAGENT |

As medidas foram criadas em DAX seguindo boas práticas, utilizando agregações corretas e evitando cálculo linha a linha quando possível.

---

## 5. Tema Personalizado

O dashboard utiliza um tema customizado em JSON (`tema_personalizado.json`), aplicado diretamente no Power BI via **Exibição → Temas → Procurar temas**.

O arquivo define paleta de cores, fundo das páginas, bordas e cantos arredondados dos visuais — demonstrando como é possível padronizar a identidade visual de relatórios Power BI sem depender de configurações manuais visual a visual.

---

## 6. Limitações Conhecidas

Volume Real e NS Real apresentam indisponibilidade ou inconsistência na base operacional original. Para evitar exposição de dados inválidos, esses indicadores não foram exibidos em cards principais, sendo substituídos por métricas consistentes. As limitações foram tratadas por validações lógicas e decisões de design documentadas.

---

## 7. Decisões de Design

- Tema customizado via JSON para padronização visual
- Layout em duas páginas: visão executiva e análise intradiária
- Uso de ícones para navegação entre páginas
- Priorização de leitura clara, com contraste adequado e foco em usabilidade
