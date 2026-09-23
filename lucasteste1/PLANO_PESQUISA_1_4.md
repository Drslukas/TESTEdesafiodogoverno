# Plano técnico para buscar RMSE de 1,4

O placar é RMSE em mm/dia. O modelo atual deve ser comparado apenas por
backtests temporais que imitem o teste: prever o mês seguinte sem usar o alvo
e manter `tp` congelada quando essa for a condição de inferência.

## Filtro para artigos e novas features

Uma ideia só entra em experimento se atender todos os critérios abaixo:

1. explicar precipitação mensal na América do Sul, e não apenas outro alvo;
2. estar disponível antes do mês que será previsto;
3. ser compatível com as regras da competição;
4. poder ser reproduzida com os dados disponíveis;
5. reduzir o RMSE em mais de um bloco temporal, contra o baseline atual.

Caso falhe em qualquer critério, ela é registrada como referência e não é
adicionada ao modelo.

## Prioridade 1 — validação que decide submissões

Usar blocos cronológicos completos, treinando somente antes de cada bloco:

- 1997--1998: El Niño muito forte;
- 2015--2016: El Niño muito forte;
- um ou mais blocos neutros/La Niña para evitar um modelo especializado em um
  único regime.

Para cada bloco, avaliar climatologia, modelo lag-aware e ensemble. Uma
submissão só é candidata quando a melhoria aparece em todos os blocos e no
RMSE agregado. A pontuação 1,9255 do blend atual vem de um único bloco e não
é evidência suficiente para uma submissão.

## Prioridade 2 — modelo que reproduz o mecanismo de teste

Treinar um residual da climatologia por ponto e mês, mas criar exemplos de
treino artificiais com `tp` congelada por 1 a 24 meses. Cada exemplo deve usar
o valor de `tp` do mês âncora e a variável `lag_meses`, enquanto os demais
campos disponíveis naquele mês continuam como preditores. Assim o modelo não
aprende uma relação com chuva recente que não existirá no conjunto de teste.

Começar com LightGBM/XGBoost lag-aware e calibrar o peso do residual contra a
climatologia. O peso pode variar por mês e por região, aprendido em blocos
temporais anteriores com regressão ridge e limitado para evitar sobreajuste.

## Prioridade 3 — informação oceânica, somente se as regras permitirem

Adicionar índices conhecidos antes da data de emissão da previsão:

- Niño 3.4 e Niño 1+2, com defasagens de 0--6 meses;
- gradiente do Atlântico Tropical Norte--Sul (TAG);
- gradiente do Atlântico Sul (SAG);
- anomalias de temperatura da superfície do mar (SST) em baixa resolução ou
  componentes principais/EOFs delas.

ENSO, TAG e SAG são mecanismos documentados para chuva na América do Sul. Os
índices devem ser montados apenas com observações disponíveis até o mês de
inicialização. Dados externos não devem ser baixados ou usados até confirmar
as regras da competição.

## Prioridade 4 — modelo espacial

Treinar uma U-Net residual ou ConvLSTM-U-Net na grade completa. A entrada deve
ter os campos atmosféricos em 3--6 meses consecutivos, latitude/longitude,
climatologia e máscara de `lag_meses`; a saída é a anomalia de precipitação.
Uma rede espacial consegue aprender padrões conectados entre Amazônia, Andes,
SACZ, Sul do Brasil e bacia do Prata que árvores por pixel não capturam.

Usar perda MSE diretamente em mm/dia e validar na mesma grade completa do
Kaggle. Para não gastar GPU cedo, a U-Net só entra na disputa depois de o
modelo lag-aware estabelecer um ganho estável.

## Prioridade 5 — ensemble final

Combinar previsões por uma regressão de pesos ajustada somente em validações
anteriores:

1. climatologia mensal por pixel;
2. LightGBM residual lag-aware;
3. U-Net residual;
4. previsões sazonais dinâmicas, se forem permitidas e disponíveis no momento
   histórico correto.

O trabalho publicado para a América do Sul indica que a calibração e a
combinação ponderada de modelos melhoram a habilidade em relação à média
simples, principalmente em regiões afetadas por ENSO.

## Evidências consultadas

- DUNE usa uma U-Net++ com inicialização em meses anteriores e validações
  temporais para previsão climática mensal: <https://journals.ametsoc.org/view/journals/aies/4/4/AIES-D-24-0073.1.xml>.
- Estudo de redes neurais para precipitação na América do Sul mostrou que
  arquiteturas espaciais reproduzem padrões sazonais e podem superar o modelo
  operacional em partes do domínio: <https://www.mdpi.com/2072-4292/13/13/2468>.
- Estudo de previsão mensal no leste da Amazônia identifica ENSO, TAG e SAG
  como preditores de grande escala relevantes: <https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2025.1576377/full>.
- TelNet combina índices climáticos de SST/ERA5 e normaliza anomalias por
  ponto e estação: <https://www.nature.com/articles/s43247-025-02207-2>.
- Calibração e combinação de ensembles sobre a América do Sul melhoraram a
  habilidade em relação a combinações simples: <https://www.cptec.inpe.br/pesquisadores/caio.coelho/Osman-et-al-2021.pdf>.

## Ideia rejeitada após o filtro

O artigo sobre ressaca no Sul/Sudeste durante 2015--2016 estuda ondas,
avisos marítimos e padrões sinóticos diários. Ele não oferece um preditor
mensal adicional para todo o domínio; vento, pressão e geopotencial já estão
representados pelos campos da competição. Não será usado no modelo atual:
<https://www.scielo.br/j/rbmet/a/SScxjgVvRSkPNY75xbskQwj/?lang=pt>.
