# Estado da entrega — 22/09/2026

O ZIP oficial enviado pelo usuário passou em `ZipFile.testzip()` e seus 13 arquivos foram extraídos em `data/`. O inventário está em `outputs/data_inspection.json`. O cache GEOSS2S de 491 meses foi baixado da fonte Columbia; temperaturas inválidas e marcadores de ausência são removidos na leitura.

A validação temporal foi executada em três períodos. O modelo oceânico de referência obteve RMSE 1,806078 (2015–2016), 1,792887 (2021–2022) e 1,762926 (2022). A mistura com 50% GEOSS2S obteve 1,780411, 1,789962 e 1,761786, respectivamente. O peso foi escolhido entre quatro opções previamente fixadas, exigindo melhora em cada período e no segundo ano dos blocos de dois anos. O relatório completo está em `outputs/nmme_gate.json`. Esses números são locais, não a nota Kaggle; o bloco 2022 está contido em 2021–2022.

O treino final usa alvos até dezembro de 2022. O candidato está em `outputs/submission_candidate_2023_2024.csv`, com 1.885.464 linhas, todos os IDs do arquivo de exemplo, previsões finitas e não negativas. SHA-256: `777633a4dee553192ba54c982d8691ba89d70ecbd105bb50561c2dff22c4ef7a`. A auditoria está em `outputs/candidate_audit.json`. O CSV ainda não foi enviado ao Kaggle; seu resultado em 2024 permanece desconhecido.

O projeto contém scripts de download, validação, treino, geração, auditoria e instruções no `README.md`. O ZIP de dados e caches ficam fora do pacote de código por tamanho.

## Retorno Kaggle e próximo experimento

O usuário informou nota Kaggle **1,69147** para `submission_candidate_2023_2024.csv`, contra **1,69874** do CSV anterior. Para chegar a 1,50000 seria necessária redução adicional de 0,19147 (aproximadamente 11,3% da nota atual). A captura de tela não identifica a nota privada de 2024.

Nos folds 2015–2016 e 2021–2022, 1% das células-mês com maior erro quadrático responde por 28,2% e 27,2% do erro total. Testes rápidos de escala global de 0,97 melhoraram o RMSE apenas de 1,78041 para 1,77962 e de 1,78996 para 1,78735; suavização espacial de 0,7 célula piorou ambos os folds. Esses ajustes são insuficientes para buscar 1,5. O próximo trabalho útil é investigar eventos extremos e fontes preditivas adicionais com validação temporal, sem ajustar o modelo diretamente à nota pública.
