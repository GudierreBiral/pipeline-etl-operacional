Estrutura

Volume Recebido
Descrição: Total de chamadas recebidas no período.
Origem: HSPLIT
Cálculo: Soma de ChamadasRecebidas

TMA (Tempo Médio de Atendimento)
Descrição: Tempo médio falado por chamada atendida.
Origem: HSPLIT
Cálculo:
TempoFaladoTotal / ChamadasAtendidas

NS (Nível de Serviço)
Descrição: Percentual de chamadas atendidas dentro do SLA.
Origem: HSPLIT
Cálculo: AtendidasNS / (Recebidas - AbandonadasNS)

Percentual de Ocupação
Descrição: Percentual do tempo produtivo dos agentes.
Origem: HAGENT
Cálculo:
(TempoLogado - TempoPausa - TempoDisponível) / (TempoLogado - TempoPausa)