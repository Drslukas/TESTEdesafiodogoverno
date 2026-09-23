# Resultados de experimentos locais

Todos os números abaixo usam RMSE global em mm/dia, com treino anterior ao
bloco validado e `tp` congelada durante a validação. Nenhum CSV foi submetido
ao Kaggle.

| Modelo | El Niño 2015--16 | El Niño 1997--98 | Decisão |
|---|---:|---:|---|
| Climatologia por ponto/mês | 1.9713 | 2.2728 | referência |
| Residual com `tp` fresca | 1.9490 | — | rejeitado: não imita o teste |
| Blend residual + climatologia | 1.9255 | — | rejeitado: lag-aware é melhor |
| Residual lag-aware | 1.8851 | 2.0459 | manter |
| Lag-aware + circulação | **1.8840** | **2.0383** | manter provisoriamente |
| Lag-aware + circulação + médias causais de 3 meses | 1.8878 | — | rejeitado: piorou |
| LightGBM causal simples (grade reduzida, stride 8) | **1.8607** | **1.9670** | melhor configuração testada |
| LightGBM causal simples (2021--22, stride 8) | **1.8051** | — | validação independente |
| Ridge causal (2015--16, stride 8) | 1.9223 | — | rejeitado: pior que LightGBM |
| LightGBM causal simples (2015--16, stride 4) | 1.8840 | — | referência em resolução maior |
| LightGBM causal, 127 folhas (2015--16, stride 8) | **1.8560** | — | melhor hiperparâmetro testado |
| LightGBM causal, 31 folhas (2015--16, stride 8) | 1.8669 | — | rejeitado: pior que 127 folhas |
| LightGBM causal, 127 folhas (1997--98, stride 8) | **1.9613** | — | validação independente |
| LightGBM causal, 127 folhas (2021--22, stride 8) | 1.8059 | — | praticamente empatado |
| LightGBM causal, 255 folhas (2015--16, stride 8) | **1.8545** | — | melhor configuração atual |
| LightGBM causal, 511 folhas (2015--16, stride 8) | 1.8570 | — | rejeitado: pior que 255 |
| LightGBM, 192 folhas, lr=0,025, 700 rodadas | **1.8521** | — | candidato |
| LightGBM, 224 folhas, lr=0,025, 700 rodadas | **1.8510** | — | melhor candidato atual |
| LightGBM, 256 folhas, lr=0,025, 700 rodadas | 1.8549 | — | rejeitado |
| LightGBM, 224 folhas, lr=0,02, 800 rodadas | 1.8528 | — | rejeitado |

## Aprendizados

- Simular a idade da precipitação é o maior ganho confirmado até agora.
- O blend global com climatologia não ajuda nos dois modelos lag-aware.
- Fluxos de umidade e velocidade do vento em 850 hPa têm ganho pequeno, mas
  consistente nos dois El Niños; precisam de mais blocos antes do modelo final.
- Médias temporais simples de três meses adicionaram ruído e foram removidas.
- A busca temporal com `tp` congelada confirmou que o LightGBM simples, usando
  somente campos atmosféricos em `time_origem` e lags causais de precipitação,
  é mais robusto que Ridge e que as expansões com estatísticas climáticas ou
  histórico âncora.
- O RMSE agrupado dos três blocos reduzidos (1997--98, 2015--16 e 2021--22)
  foi 1.8606. Esse valor é uma referência local, não uma garantia do placar
  privado do Kaggle.

## Próximos testes válidos

1. calibração regional/mensal com scikit-learn, treinada em blocos históricos
   e aplicada em outro bloco, sem leakage;
2. índices oceânicos Pacífico--Atlântico, apenas se as regras permitirem;
3. U-Net residual em TensorFlow/Keras quando houver Python 3.13 e GPU.
