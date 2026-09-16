# Desafio Kaggle — Previsão Climática de Precipitação sobre a América do Sul (WORCAP 2026)

> Documento técnico de entendimento do desafio, produzido a partir da leitura direta da página oficial da competição no Kaggle em **16/09/2026**.
> URL analisada: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul` (abas Overview, Data, Code, Models, Discussion, Leaderboard, Rules, Team).
>
> **Convenção usada neste documento:**
> - Texto normal = fato oficial encontrado na página do Kaggle.
> - Blocos marcados **[Sugestão da análise]** = ideia técnica nossa, não presente na documentação oficial.
> - Blocos marcados **[Inferência]** = dedução lógica/aritmética a partir de fatos oficiais (ex.: contagem de meses), não uma afirmação literal da página.
> - Onde a informação não estava disponível publicamente, está marcado como:
>   > **Não encontrado na documentação pública.**

---

## Contradições e imprecisões encontradas entre o briefing inicial e a página oficial

Antes de tudo, é importante registrar divergências entre o contexto inicial fornecido e o que a página realmente mostra em 16/09/2026, para que a equipe não trabalhe com premissas erradas:

1. **Limite de submissões por dia**: o briefing inicial menciona "máximo de 3 submissões por dia". A aba **Rules** da competição declara explicitamente **"Você pode enviar no máximo cinco (5) envios por dia"**. Considerar **5/dia** como valor oficial vigente.
2. **Tamanho máximo de equipe**: a aba **Rules** (regras específicas da competição) diz **"O tamanho máximo da equipe é de quatro (4) integrantes"**. Já a aba **Team**, ao exibir o formulário da própria equipe do usuário, mostra o texto genérico de interface **"Your team can have a maximum of 10 members"**. Esse "10" parece ser um texto padrão da plataforma Kaggle (não específico da competição) — a regra específica da competição (4 integrantes) deve prevalecer como número oficial, já que é a regra explicitamente escrita para este desafio.
3. **Exemplo de `id` na seção Evaluation**: a seção *Evaluation* do Overview usa como exemplo `2025_01_-30.00_-53.00` (ano 2025). Isso contradiz a seção *Data*, que declara que o período de avaliação real é **2023–2024**, e o próprio `sample_submission.csv`, cujas linhas reais começam com `2023_01_...`. Portanto, o "2025" da seção Evaluation é um exemplo ilustrativo genérico/desatualizado do texto, **não** representa o intervalo de anos real da submissão. O intervalo real de anos a usar é **2023 e 2024**, confirmado pelo arquivo de exemplo de submissão.
4. **"RMSE sobre precipitação absoluta"**: essa frase exata não aparece na página oficial. A seção *Evaluation* oficial diz apenas "RMSE (...) entre a precipitação prevista e o dado de referência, em mm/dia". A leitura de "absoluta" (valor previsto diretamente, não anomalia/desvio em relação à climatologia) é consistente com o texto oficial, mas é uma interpretação, não uma citação literal.

---

# 1. Visão geral do desafio

**Nome oficial:** Previsão Climática de Precipitação sobre a América do Sul
**Título nas regras:** WORCAP 2026 — Previsão Mensal de Precipitação na América do Sul
**Organizador:** Programa de Pós-Graduação do Instituto Nacional de Pesquisas Espaciais (INPE) — Workshop de Computação Aplicada (WORCAP 2026)
**Host Kaggle (usuário responsável):** Gerônimo Gallarreta Zubiaurre Lemos
**Tipo:** *Community Prediction Competition*, competição **privada** (visível apenas a convidados/participantes registrados)
**Premiação:** Não há prêmio em dinheiro nem pontos/medalhas Kaggle ("Does not award Points or Medals"). Prêmio declarado: "Kudos"; do 1º ao 3º lugar: certificado de premiação e reconhecimento no ranking oficial.

## O problema, em linguagem simples

Você recebe, para um determinado mês `M`, um "retrato" do estado da atmosfera sobre a América do Sul: temperatura, pressão, umidade, vento e nuvens em vários pontos de uma grade regular, além da própria precipitação observada nesse mês. A tarefa é prever, para cada ponto dessa mesma grade, **qual será a precipitação média do mês seguinte (`M+1`)**, em milímetros por dia (mm/dia).

Para quem vem de Machine Learning "tradicional" (tabular, imagens, etc.) mas não de meteorologia, uma forma de pensar o problema:

- Cada mês é uma **"imagem" multicanal**: uma grade 2D de latitude × longitude, com vários canais (um por variável atmosférica) — parecido com uma imagem RGB, mas com 10 canais climáticos em vez de 3 canais de cor.
- A tarefa é um problema de **regressão espaço-temporal**: prever a "imagem" de precipitação do mês seguinte a partir da "imagem" multicanal do mês atual.
- Não há features tabulares avulsas por linha — a unidade fundamental é o **par (mês, ponto de grade)**, e cada previsão é um número real (mm/dia) não-negativo.

**Entrada:** o estado atmosférico observado do mês `M` (10 variáveis, cada uma em grade 301×261).
**Saída:** a precipitação média prevista do mês `M+1`, em mm/dia, para cada um dos 78.561 pontos da grade.
**Horizonte de previsão:** 1 mês à frente (M → M+1). Não há evidência oficial de horizontes maiores (2, 3+ meses) fazendo parte do desafio.
**Região geográfica:** América do Sul (grade retangular cobrindo de 60°S a 15°N e de 90°O a 25°O — engloba a América do Sul e parte do entorno; ver Seção 6).
**Resolução espacial:** grade regular de 0,25° (≈ 25–28 km, dependendo da latitude) — resolução herdada diretamente do ERA5.
**Unidade da previsão:** milímetros por dia (mm/dia) — a mesma unidade dos dados de precipitação de treino (`tp`).
**Objetivo da competição:** minimizar o RMSE (raiz do erro quadrático médio) entre a precipitação prevista e a precipitação de referência (ERA5), agregado sobre todos os pontos de grade e todos os meses do período de avaliação (24 meses: jan/2023–dez/2024).

---

# 2. Formulação matemática do problema

A página não apresenta uma formulação matemática formal com notação — o que segue é a formalização da nossa análise, construída diretamente a partir da descrição oficial em texto ("Dado o estado atmosférico observado do mês M, estimar a precipitação média do mês M+1, em mm/dia, em cada ponto de grade") e do código de exemplo (`xarray`) fornecido na aba Data.

Seja:

- `G` = conjunto de pontos de grade, com `|G| = 301 × 261 = 78.561` pontos (lat × lon), cada ponto identificado por `(lat_i, lon_j)`.
- `t` = índice do mês (mensal, de jan/1940 a dez/2022 no treino).
- `V = {tp, t2, cloud_cover, surface_pressure, shum_850, rel_hum_850, temperature_850, geopotential_850, u_850, v_850}` = conjunto das 10 variáveis atmosféricas distribuídas (1 de precipitação + 9 atmosféricas), cada uma como campo 2D sobre `G`.

**Entrada (features) no mês `t`:**

```
X_t ∈ R^(301 × 261 × 10)
```

um tensor espacial com 10 canais (as 10 variáveis listadas acima), cada canal com forma `(301, 261)` — o estado atmosférico completo observado no mês `t`.

**Alvo (target) para o mês `t+1`:**

```
y_{t+1} ∈ R^(301 × 261)
```

um único campo escalar: a precipitação média (mm/dia) em cada ponto de grade no mês seguinte.

**Formulação da tarefa:** aprender uma função

```
f: X_t ↦ ŷ_{t+1},   ŷ_{t+1} ∈ R^(301 × 261)
```

que minimize o erro entre `ŷ_{t+1}` e `y_{t+1}` (medido via RMSE, Seção 8), agregando sobre todos os pontos de grade `(i, j) ∈ G` e todos os meses `t` do conjunto de avaliação.

**Dimensão espacial:** 2D (lat × lon), fixa em `301 × 261 = 78.561` pontos por mês (grade constante ao longo do tempo).
**Dimensão temporal:** mensal; a variável independente é o índice do mês (não há sub-mensal nos dados distribuídos).
**Canais/variáveis meteorológicas de entrada:** 10 no total — 1 relacionada à própria precipitação (`tp`, mês `M`) + 9 variáveis atmosféricas auxiliares (todas em 850 hPa, exceto `t2`, `cloud_cover` e `surface_pressure`, que são de superfície/coluna).

Um detalhe importante confirmado pela descrição do arquivo `treino_tp_alvo.nc`: o "deslocamento" de `y` já vem **pré-aplicado** pelos organizadores (cada posição do eixo `time` de `treino_tp_alvo.nc` já contém a precipitação do mês seguinte). A equipe não precisa (e não deve) recalcular esse deslocamento manualmente a partir de `treino_tp.nc` — ele já está pronto no arquivo `treino_tp_alvo.nc`.

---

# 3. Dados

**Origem:** reanálise **ERA5** do ECMWF (European Centre for Medium-Range Weather Forecasts) — "a base de referência do ECMWF", segundo a própria página. Atribuição oficial obrigatória: *"Contains modified Copernicus Climate Change Service information 2026. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains."*

**Período temporal (treino):** janeiro de 1940 a dezembro de 2022 — **[Inferência]** isso equivale a `83 anos × 12 meses = 996 meses` de dados mensais de treino (cálculo nosso a partir do intervalo declarado; não é um número citado literalmente pela página).

**Período de avaliação:** 24 meses, janeiro de 2023 a dezembro de 2024.

**Resolução espacial:** grade regular de 0,25°.

**Região:** 301 latitudes × 261 longitudes = **78.561 pontos de grade por mês**, cobrindo de **60°S a 15°N** e de **90°O a 25°O**.

**Frequência temporal:** mensal (não há dados diários/horários distribuídos — a página não menciona nenhuma resolução sub-mensal disponível).

**Variáveis (10 no total):** a precipitação (`tp`) mais nove variáveis atmosféricas: temperatura a 2 m, cobertura de nuvens, pressão à superfície, umidade específica, umidade relativa, temperatura, geopotencial e as componentes zonal e meridional do vento — estas seis últimas no nível de **850 hPa**.

**Formato dos arquivos:** NetCDF (`.nc`) para as séries de grade, CSV para a submissão. 13 arquivos no total, 2,06 GB.

**Como carregar (exemplo oficial fornecido na página, em Python/xarray):**

```python
import xarray as xr

tp = xr.open_dataset("treino_tp.nc").tp        # (time, lat, lon), mm/dia
alvo = xr.open_dataset("treino_tp_alvo.nc").tp_alvo  # precipitação de M+1
vento = xr.open_dataset("treino_u_850.nc").u_850
teste = xr.open_dataset("teste_features.nc")

X = tp.values[:-1]   # entrada: mês M
y = alvo.values[:-1] # saída: mês M+1
```

Nota oficial da página: **"A latitude está em ordem crescente."**

## Tabela de variáveis

| Variável | Nome do arquivo (.nc) | Nome da variável interna | Descrição (oficial) | Unidade | Dimensão | Uso |
|---|---|---|---|---|---|---|
| Precipitação | `treino_tp.nc` | `tp` | Precipitação mensal observada | mm/dia (confirmado) | `(time, lat, lon)` — grade 301×261, ~996 meses [Inferência] | Feature (mês M) e base para o target |
| Precipitação alvo | `treino_tp_alvo.nc` | `tp_alvo` | Precipitação do mês seguinte a cada posição do eixo `time` (deslocamento já aplicado); último mês da série é `NaN` | mm/dia (mesma natureza de `tp`; não reafirmado explicitamente para este arquivo) | mesma grade; último passo temporal = NaN | **Target** |
| Temperatura a 2 m | `treino_t2.nc` | `t2` | Temperatura do ar a 2 metros de altura | **Não encontrado na documentação pública** | mesma grade | Feature |
| Cobertura de nuvens | `treino_cloud_cover.nc` | `cloud_cover` | Cobertura de nuvens | **Não encontrado na documentação pública** | mesma grade | Feature |
| Pressão à superfície | `treino_surface_pressure.nc` | `surface_pressure` | Pressão à superfície | **Não encontrado na documentação pública** | mesma grade | Feature |
| Umidade específica (850 hPa) | `treino_shum_850.nc` | `shum_850` | Umidade específica em 850 hPa | **Não encontrado na documentação pública** | mesma grade | Feature |
| Umidade relativa (850 hPa) | `treino_rel_hum_850.nc` | `rel_hum_850` | Umidade relativa em 850 hPa | **Não encontrado na documentação pública** | mesma grade | Feature |
| Temperatura (850 hPa) | `treino_temperature_850.nc` | `temperature_850` | Temperatura em 850 hPa | **Não encontrado na documentação pública** | mesma grade | Feature |
| Geopotencial (850 hPa) | `treino_geopotential_850.nc` | `geopotential_850` | Geopotencial em 850 hPa | **Não encontrado na documentação pública** | mesma grade | Feature |
| Vento zonal (850 hPa) | `treino_u_850.nc` | `u_850` | Componente zonal do vento em 850 hPa | **Não encontrado na documentação pública** | mesma grade | Feature |
| Vento meridional (850 hPa) | `treino_v_850.nc` | `v_850` | Componente meridional do vento em 850 hPa | **Não encontrado na documentação pública** | mesma grade | Feature |
| Features de teste | `teste_features.nc` | (as 10 acima) + `tp_alvo`, `tp_ultima_obs`, `lag_meses` | Estado atmosférico do mês anterior ao mês-alvo, mais campos auxiliares | mm/dia para `tp_ultima_obs`; demais como acima | mesma grade; `time` = mês alvo | Feature (teste) |
| Submissão | `sample_submission.csv` | `id`, `tp_mm_day` | Identificador `ano_mês_lat_lon` e previsão | mm/dia | 1.885.464 linhas | Output/Submissão |

**[Sugestão da análise]** As unidades ERA5 "de fábrica" costumam ser: temperatura em K, pressão em Pa/hPa, geopotencial em m²/s² (ou geopotential height em m), umidade específica em kg/kg, umidade relativa em %, vento em m/s, cobertura de nuvens como fração 0–1. **Isso não está confirmado pela página da competição** — os organizadores podem ter reescalado/convertido essas variáveis antes de distribuí-las. A equipe deve **verificar empiricamente a faixa de valores de cada arquivo** (min/max/média) antes de assumir qualquer unidade, em vez de assumir os padrões ERA5 "de livro".

Não foi possível inspecionar diretamente o conteúdo binário dos arquivos `.nc` pela interface do Kaggle — a pré-visualização retornou **"Unable to show preview — Previews for binary data are not supported"**. Toda a informação de variáveis/dimensões acima vem do texto da aba *Data*, não de inspeção direta dos bytes dos arquivos. A única prévia tabular disponível foi a do `sample_submission.csv` (ver Seção 4).

---

# 4. Estrutura dos arquivos

```text
dataset/ (13 arquivos, 2.06 GB, tipos: nc, csv)
├── treino_tp.nc                  # precipitação mensal observada (1940–2022) — feature
├── treino_tp_alvo.nc             # precipitação do mês seguinte, já deslocada — TARGET de treino
├── treino_t2.nc                  # temperatura a 2 m — feature
├── treino_cloud_cover.nc         # cobertura de nuvens — feature
├── treino_surface_pressure.nc    # pressão à superfície — feature
├── treino_shum_850.nc            # umidade específica @850hPa — feature
├── treino_rel_hum_850.nc         # umidade relativa @850hPa — feature
├── treino_temperature_850.nc     # temperatura @850hPa — feature
├── treino_geopotential_850.nc    # geopotencial @850hPa — feature
├── treino_u_850.nc               # vento zonal @850hPa — feature
├── treino_v_850.nc               # vento meridional @850hPa — feature
├── teste_features.nc             # features do período avaliado (2023-2024) + auxiliares
└── sample_submission.csv         # (48.15 MB) template de submissão, 1.885.464 linhas
```

Descrição de cada arquivo (conforme texto oficial da aba *Data*):

- **`treino_tp.nc`** — precipitação mensal observada, em mm/dia, de 1940 a 2022. Variável `tp`, eixo `time` no mês da própria observação.
- **`treino_tp_alvo.nc`** — a precipitação do mês *seguinte* a cada posição do eixo `time` (i.e., já é `tp` deslocado em -1 mês). É o alvo de treino "pronto para uso". O último mês da série é `NaN`, porque apontaria para um mês fora do período de treino (não existe "jan/2023" dentro do arquivo de treino).
- **Nove arquivos `treino_<variável>.nc`** — cada um traz uma das variáveis atmosféricas auxiliares, no mesmo período (1940–2022) e na mesma grade que `treino_tp.nc`, com o eixo `time` no mês da observação (não deslocado).
- **`teste_features.nc`** — cobre o período avaliado (24 meses, 2023–2024). O eixo `time` é o **mês alvo** (o mês que deve ser previsto) e casa com o prefixo do `id` de submissão. Os campos de cada posição temporal são os valores atmosféricos do **mês anterior** ao alvo, registrados também na coordenada `time_origem`. Contém ainda:
  - `tp_alvo`: inteiramente `NaN` — é exatamente o que deve ser previsto pela equipe;
  - `tp_ultima_obs`: a precipitação de dezembro de 2022, a última observação de `tp` disponível antes do período avaliado;
  - `lag_meses`: a defasagem (em meses) entre `tp_ultima_obs` (dez/2022) e cada mês-alvo, variando de 1 a 24.
- **`sample_submission.csv`** — lista completa de `id` na ordem esperada pela plataforma, com `tp_mm_day` zerado (placeholder). 1.885.464 linhas, 2 colunas (`id`, `tp_mm_day`), 48,15 MB.

Relação entre os arquivos: os nove arquivos `treino_*.nc` + `treino_tp.nc` formam o conjunto de features de treino (mês `M`); `treino_tp_alvo.nc` é o target de treino (mês `M+1`), alinhado pelo mesmo índice `time`; `teste_features.nc` desempenha, no período de avaliação, o mesmo papel das features de treino, mas sem o alvo observado (`tp_alvo` é `NaN` nele); `sample_submission.csv` define o formato/ordem exata das previsões esperadas para os `tp_alvo` de `teste_features.nc`.

---

# 5. Entendimento temporal

```text
Mês M (treino: jan/1940 ... dez/2022)
   → observações atmosféricas (tp, t2, cloud_cover, surface_pressure,
      shum_850, rel_hum_850, temperature_850, geopotential_850, u_850, v_850)
        ↓
      Modelo
        ↓
Mês M+1 → precipitação prevista (tp_alvo), mm/dia, em cada ponto de grade
```

**Como o treinamento temporal funciona:** cada exemplo de treino é um par `(estado atmosférico do mês M, precipitação do mês M+1)`. O arquivo `treino_tp_alvo.nc` já entrega esse alvo pré-deslocado — não é necessário (nem correto) reconstruir o deslocamento manualmente somando um mês à mão, exceto para entender/validar os dados.

**Meses disponíveis:** jan/1940 a dez/2022 para as features de treino (996 meses [Inferência]). O último mês desse intervalo (dez/2022) tem `tp_alvo = NaN`, pois "jan/2023" está fora do arquivo de treino.

**Meses com target:** todos os meses de treino exceto o último (que é `NaN`), ou seja, efetivamente **jan/1940 a nov/2022** têm um alvo válido dentro de `treino_tp_alvo.nc` — **[Inferência]**: isso é dedução lógica a partir da explicação "o último mês da série é NaN", não uma contagem exposta explicitamente pela página.

**Onde começa e termina o treinamento:** começa em jan/1940, termina em dez/2022 (última observação de features); o último alvo válido correspondente seria dez/2022 → jan/1940 até nov/2022 com alvo utilizável, dependendo de como a equipe decide tratar a borda.

**Como 2023 é utilizado:** define o **leaderboard público** durante a competição (feedback ao vivo, mas não é a métrica que decide a colocação final).

**Como 2024 é utilizado:** define a **classificação final** da competição — só é revelado ao encerramento, no **leaderboard privado**.

**Confirmação adicional pelo leaderboard:** a própria aba *Leaderboard* exibe o aviso "This leaderboard is calculated with approximately 50% of the test data. The final results will be based on the other 50%, so the final standings may be different." — consistente com a divisão declarada de 12 meses (2023, público) e 12 meses (2024, privado) dentro dos 24 meses totais de avaliação (50%/50%).

**Risco de leakage temporal (nossa análise):**

- A **precipitação observada dos 24 meses avaliados (2023–2024) não está em nenhum arquivo distribuído** — segundo a própria página. Isso reduz bastante o risco de leakage direto via dados fornecidos.
- **[Sugestão da análise]** Ainda assim, há um risco indireto real: se a equipe usar **dados externos** (reanálises públicas, outros produtos ERA5, etc.) que cubram 2023–2024, é tecnicamente possível "vazar" a precipitação real do período de teste para dentro do pipeline, mesmo sem baixar diretamente do Kaggle. A regra de dados externos (Seção 13) exige que qualquer fonte usada seja declarada — a equipe deve ter cuidado redobrado de **não usar, direta ou indiretamente, a precipitação real de 2023–2024** de nenhuma fonte externa, sob risco de comprometer a validade da submissão.
- **[Sugestão da análise]** Outro ponto de atenção: como `teste_features.nc` entrega o "mês anterior ao alvo" como feature (e não o próprio mês-alvo), a equipe deve garantir que qualquer feature derivada (médias móveis, lags, anomalias) para o conjunto de teste use exclusivamente informação disponível **até o mês anterior ao alvo**, replicando exatamente a mesma defasagem usada no treino.

---

# 6. Grid espacial

**Região coberta:** América do Sul e entorno — latitude de **60°S a 15°N**, longitude de **90°O a 25°O** (conforme texto oficial da aba Data).

**Resolução:** 0,25° em ambas as dimensões.

**Quantidade de pontos:**
- Latitudes: **301** (confirmado oficialmente).
- Longitudes: **261** (confirmado oficialmente).
- Pontos de grade por mês: **78.561** (301 × 261 = 78.561 — confirmado oficialmente pelo próprio texto da página, e consistente aritmeticamente).

**[Inferência]** Verificação aritmética do intervalo: `(15 − (−60)) / 0,25 + 1 = 301` latitudes; `(−25 − (−90)) / 0,25 + 1 = 261` longitudes — os números batem exatamente com o texto oficial, o que dá confiança de que os limites geográficos declarados (60°S–15°N, 90°O–25°O) estão corretos e consistentes com a contagem de pontos.

**Formato espacial dos dados:** cada variável, em cada mês, é uma matriz 2D `(lat, lon)` de shape `(301, 261)`, com latitude em ordem crescente (conforme nota oficial).

**Como uma previsão deve ser produzida:** para cada um dos 24 meses avaliados, o modelo deve gerar um valor de `tp_mm_day` para **cada um** dos 78.561 pontos de grade — logo, `24 × 78.561 = 1.885.464` previsões no total, exatamente o número de linhas declarado para a submissão completa.

```text
        Longitude → (90°O ........................ 25°O), passo 0,25°, 261 colunas
Lat ↓
(15°N)  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
        ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
        ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
        ...                                        301 linhas
        ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
(60°S)  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
```

---

# 7. Target

O target oficial é: **"a precipitação média do mês seguinte, em mm/dia"** por ponto de grade.

- **Unidade:** mm/dia (confirmado oficialmente para `tp` e, por extensão de natureza, para `tp_alvo`).
- **Significado:** precipitação média diária esperada ao longo do mês seguinte (não é o total acumulado do mês; é expressa como taxa média por dia — "mm/dia" e não "mm/mês").
- **Acumulada ou média?** É uma **média** (mm/dia), não um total acumulado mensal — assim indicado explicitamente pela unidade "mm/dia" usada em todo o texto oficial (evaluation, arquivo, submissão).
- **Absoluta:** sim, no sentido de que o modelo deve prever o valor real de precipitação (e não uma anomalia relativa à climatologia) — é o que a estrutura de `tp_alvo`/`tp_mm_day` sugere; a página não usa explicitamente a palavra "absoluta", mas não há nenhuma menção a previsão de anomalias/desvios.
- **Dimensão:** um escalar por ponto de grade e por mês-alvo — grade `(301, 261)` por mês, 24 meses no total no período de avaliação.
- **Transformação necessária:** **Não encontrado na documentação pública.** A página não exige nenhuma transformação (log, normalização, clipping) antes da submissão — o exemplo de submissão usa valores decimais diretos em mm/dia (ex.: `3.812`).
- **Existência de zeros:** **Não encontrado na documentação pública** de forma explícita para o target — mas é fisicamente esperado que existam muitos meses/pontos com precipitação próxima de zero (regiões áridas, por exemplo, no Chile/Argentina dentro da grade). **[Sugestão da análise]** A equipe deve inspecionar empiricamente a distribuição de `tp` em `treino_tp.nc` (não apenas assumir), já que a documentação não descreve a distribuição.
- **Possíveis características da distribuição:** **Não encontrada descrição oficial.** **[Sugestão da análise]** Séries de precipitação mensal tipicamente têm distribuição assimétrica à direita (cauda longa, muitos valores baixos e poucos eventos extremos de chuva) — isso é uma expectativa técnica geral, não uma afirmação da documentação, e deve ser verificada nos dados reais antes de qualquer decisão de modelagem (ex.: uso de transformação log1p).

---

# 8. Métrica

**Métrica oficial: RMSE (Root Mean Squared Error / raiz do erro quadrático médio).**

Texto oficial (aba Overview → Evaluation): *"As previsões são avaliadas por RMSE (raiz do erro quadrático médio) entre a precipitação prevista e o dado de referência, em mm/dia, sobre todas os pontos de grade e todos os meses do período de teste."*

A página **não publica uma fórmula matemática explícita** (não há LaTeX/expressão formal na aba Evaluation). A formalização abaixo é nossa, construída a partir do texto oficial citado:

```
RMSE = sqrt( (1 / N) * Σ_{m=1..24} Σ_{(i,j)∈G} ( ŷ_{m,i,j} − y_{m,i,j} )² )
```

onde:
- `m` percorre os 24 meses do período de teste (jan/2023–dez/2024);
- `(i,j)` percorre os `|G| = 78.561` pontos de grade;
- `ŷ_{m,i,j}` é a precipitação prevista (mm/dia) para o mês `m` no ponto `(i,j)`;
- `y_{m,i,j}` é a precipitação de referência ERA5 (mm/dia) para o mesmo mês/ponto;
- `N = 24 × 78.561 = 1.885.464`, que **[Inferência]** bate exatamente com o número de linhas do arquivo de submissão — coerente com a leitura de que o RMSE é calculado de forma "achatada" (*pooled*), sobre todos os pares (mês, ponto) de uma vez, e não como média de RMSEs mensais/espaciais separados.

**O que está sendo comparado:** precipitação prevista (`tp_mm_day` submetido) vs. precipitação de referência ERA5 (não distribuída, mantida pelos organizadores).
**Sobre quais pontos:** todos os pontos de grade do domínio (os 78.561 pontos).
**Sobre quais meses:** todos os meses do período de teste (24 meses; dividido em público=2023 e privado=2024, conforme Seção 5).
**Como o erro é agregado:** por soma quadrática sobre todos os pontos e meses, seguida de raiz quadrada — a página não detalha explicitamente se é uma média "flat" (todos os 1.885.464 pares com peso igual) ou alguma ponderação por área de célula (grades regulares em lat/lon têm células menores perto dos polos) — **[Sugestão da análise]** isso não é mencionado, então deve-se assumir peso igual por ponto de grade, mas a equipe deve estar ciente de que essa é uma limitação/ambiguidade não esclarecida oficialmente.
**Significado de "RMSE sobre chuva absoluta":** entendemos que significa que o erro é calculado diretamente sobre o valor previsto de precipitação (mm/dia), e não sobre uma anomalia (desvio em relação à climatologia) — ver observação na seção de contradições no topo do documento, já que essa frase exata não está na página.

**Por que isso importa para a estratégia:** como o erro é quadrático e agregado sobre TODOS os pontos e meses (incluindo regiões/estações de baixa precipitação, onde um pequeno erro absoluto já é proporcionalmente grande, e regiões/eventos de chuva extrema, onde erros absolutos tendem a ser maiores em valor absoluto e dominam a soma dos quadrados), **[Sugestão da análise]** modelos que acertam bem a magnitude em eventos de chuva forte tendem a ter impacto desproporcional no RMSE final, mesmo que sejam uma minoria dos pontos/meses.

---

# 9. Baselines

**Busca realizada:** abas *Code* (Notebooks) e *Models* da competição, e aba *Discussion*.

**Resultado:**
- Aba **Code**: nenhum notebook público listado no momento da análise (16/09/2026) — apenas a interface padrão de criação de notebook, sem nenhum notebook publicado na competição.
- Aba **Models**: "No models found" — nenhum modelo do Kaggle Model Hub associado à competição.
- Aba **Discussion**: "No discussions found" — nenhum tópico de fórum criado até o momento.

> **Não encontrado na documentação pública: não há baseline oficial, notebook de exemplo, benchmark ou discussão técnica publicada pelos organizadores ou pela comunidade até o momento desta análise.**

A única referência a um "patamar a bater" é textual, na aba Overview: *"A régua a bater é a climatologia: um bom modelo precisa superar a média histórica de forma consistente, não apenas reproduzi-la."* Isso sugere fortemente que a **climatologia** (média histórica por ponto/mês) é o baseline conceitual esperado pelos organizadores, ainda que nenhum número de RMSE de referência seja publicado.

## Baselines sugeridos pela nossa análise (não oficiais)

**[Sugestão da análise]** Como não há baseline oficial publicado, sugerimos que a equipe implemente e documente internamente, para ter pontos de comparação:

- **Climatologia por ponto/mês:** para cada ponto de grade e mês do calendário (jan, fev, ..., dez), usar a média histórica de `tp` daquele mês específico ao longo dos anos de treino. É o baseline mais natural dado o comentário oficial sobre climatologia.
- **Persistência:** usar `tp` do mês `M` como previsão para `M+1` (ou, no conjunto de teste, `tp_ultima_obs` ajustado pela defasagem `lag_meses`) — simples, mas ignora sazonalidade.
- **Média móvel:** média de `tp` dos últimos N meses como previsão do próximo mês.
- **Regressão linear simples** (por ponto ou global, com poucas features).
- **Random Forest / Gradient Boosting (XGBoost, LightGBM):** tratando cada ponto de grade (ou agregações regionais) como amostras tabulares.
- **Redes neurais densas (MLP):** por ponto ou com achatamento da grade.
- **CNNs espaciais:** tratando cada mês como uma "imagem" multicanal.
- **ConvLSTM / modelos espaço-temporais.**
- **Modelos baseados em Transformer** (ex.: Transformers espaço-temporais, Earthformer-like).

Nenhuma dessas abordagens é indicada como superior sem validação (ver Seção 10 e 12) — são apenas sugestões de pontos de partida.

---

# 10. Estratégias de Machine Learning possíveis

Esta seção mapeia o espaço de soluções. **Nenhuma abordagem é recomendada como vencedora** — cabe à equipe decidir com base em validação (Seção 12).

### 10.1 Baseline extremamente simples

- **Entrada:** nenhuma feature aprendida — apenas estatística histórica (climatologia) ou o próprio `tp` do mês anterior (persistência).
- **Saída:** valor de `tp_mm_day` por ponto de grade.
- **Como representar a grade:** array 2D simples, sem necessidade de arquitetura de ML.
- **Vantagens:** rapidíssimo de implementar, serve como sanity check e referência mínima ("é preciso superar a climatologia", conforme a própria página adverte).
- **Limitações:** não captura nenhuma relação causal/física entre as variáveis atmosféricas e a chuva; ignora anos anômalos (El Niño/La Niña, por exemplo).
- **Custo computacional:** trivial.
- **Risco de overfitting:** praticamente nulo (não há parâmetros aprendidos, ou muito poucos).
- **Compatibilidade com a métrica:** direta — serve como piso de RMSE a ser superado.

### 10.2 Machine Learning tabular

- **Entrada:** cada `(ponto de grade, mês)` vira uma linha de tabela, com colunas = as 10 variáveis (+ possivelmente lat/lon/mês como features adicionais, feature engineering da Seção 11).
- **Saída:** `tp_mm_day` previsto por linha.
- **Como representar a grade:** "achatada" (flatten) — perde-se a noção de vizinhança espacial explícita, a menos que se adicionem features espaciais manualmente (lat, lon, altitude, distância à costa, etc. — ver Seção 11).
- **Vantagens:** rápido de treinar, ferramentas maduras (XGBoost/LightGBM/CatBoost), fácil de interpretar (importância de features), lida bem com poucos dados por ponto se compartilhar um único modelo global.
- **Limitações:** não captura relações espaciais entre pontos vizinhos de forma nativa; pode precisar de features espaciais manuais para compensar.
- **Custo computacional:** moderado — dataset pode ficar grande (78.561 pontos × ~996 meses ≈ 78 milhões de linhas se um modelo global for treinado linha a linha, o que pode exigir amostragem ou treino por região/mês).
- **Risco de overfitting:** moderado, controlável com regularização/validação cruzada adequada (ver Seção 12).
- **Compatibilidade com a métrica:** boa — otimizar RMSE (ou MSE) é suportado nativamente pela maioria dessas bibliotecas.

### 10.3 CNN espacial

- **Entrada:** tensor `(301, 261, 10)` por mês (a grade completa, todos os canais).
- **Saída:** tensor `(301, 261, 1)` — o campo de precipitação previsto.
- **Como representar a grade:** diretamente como "imagem" multicanal — abordagem natural dado o formato dos dados.
- **Vantagens:** captura correlação espacial local (padrões meteorológicos são inerentemente espaciais); arquiteturas conhecidas (U-Net, etc.) se aplicam bem a esse tipo de regressão "imagem para imagem".
- **Limitações:** cada mês é uma única amostra de treino — com ~996 meses de treino, o dataset é pequeno para o padrão de deep learning de imagens (poucas "imagens" de treino); requer cuidado com overfitting e talvez data augmentation ou modelos mais simples/regularizados.
- **Custo computacional:** moderado a alto, dependendo da arquitetura, mas ainda tratável em GPU única dado o tamanho pequeno do dataset (~996 amostras).
- **Risco de overfitting:** alto, dado o número reduzido de amostras temporais (996 meses) frente ao tamanho da grade (78.561 pontos por amostra) — validação temporal robusta é essencial.
- **Compatibilidade com a métrica:** direta — MSE/RMSE por pixel é a loss natural para treinar esse tipo de rede.

### 10.4 Modelos temporais

- **Entrada:** sequência de estados atmosféricos ao longo de múltiplos meses anteriores (não apenas o mês `M`, mas `M-1, M-2, ..., M-k`), por ponto de grade ou agregação regional.
- **Saída:** `tp_mm_day` do mês `M+1`.
- **Como representar a grade:** cada ponto (ou região) tratado como uma série temporal univariada/multivariada independente (RNN/LSTM/GRU por ponto, ou por cluster de pontos).
- **Vantagens:** pode capturar padrões de persistência/sazonalidade/tendência de médio prazo (ex.: relação com ENSO em escala de meses).
- **Limitações:** ignora (ou trata de forma limitada) a estrutura espacial entre pontos vizinhos; tratar cada ponto isoladamente multiplica o número de séries em 78.561.
- **Custo computacional:** pode ser alto se treinado ponto a ponto; mais tratável se agregado por região.
- **Risco de overfitting:** moderado a alto, dependendo de quantos parâmetros por série.
- **Compatibilidade com a métrica:** boa, desde que a loss de treino seja MSE/RMSE.

### 10.5 Modelos espaço-temporais

- **Entrada:** sequência de tensores `(301, 261, 10)` ao longo de vários meses (histórico) — um "vídeo" climático multicanal.
- **Saída:** tensor `(301, 261, 1)` do mês seguinte.
- **Como representar a grade:** ConvLSTM, ConvGRU, ou arquiteturas 3D-CNN (espaço + tempo simultaneamente).
- **Vantagens:** captura simultaneamente dependência espacial (vizinhança) e temporal (evolução ao longo dos meses) — conceitualmente o modelo mais fiel à física do problema.
- **Limitações:** maior complexidade de implementação e ajuste; dataset de apenas ~996 meses limita a quantidade de sequências temporais completas disponíveis para treino, especialmente com janelas longas.
- **Custo computacional:** alto (memória e tempo de treino).
- **Risco de overfitting:** alto, dado o número reduzido de sequências temporais frente ao número de parâmetros típico dessas arquiteturas.
- **Compatibilidade com a métrica:** direta, mas exige atenção à forma de validação (Seção 12) para não superestimar desempenho.

### 10.6 Transformers / modelos avançados

- **Entrada:** grade espaço-temporal, possivelmente tokenizada em patches espaciais (ao estilo Vision Transformer) com atenção também ao longo do tempo.
- **Saída:** campo de precipitação previsto do mês seguinte.
- **Como representar a grade:** patches espaciais como tokens, com codificação posicional lat/lon e temporal.
- **Vantagens:** capacidade de capturar dependências de longo alcance (ex.: teleconexões climáticas entre regiões distantes da América do Sul) sem as limitações de campo receptivo local das CNNs.
- **Limitações:** tipicamente exigem muito mais dados de treino do que os ~996 meses disponíveis; alto risco de overfitting e maior dificuldade de regularização/ajuste de hiperparâmetros em cenário de dados escassos.
- **Custo computacional:** o mais alto entre as abordagens listadas.
- **Risco de overfitting:** o mais alto, dado o volume de dados relativamente pequeno (996 meses) frente à complexidade típica de Transformers.
- **Compatibilidade com a métrica:** direta (MSE/RMSE como loss), mas o ganho sobre abordagens mais simples não está garantido neste regime de poucos dados — deve ser testado, não assumido.

---

# 11. Feature engineering

## Informação oficialmente disponível

- O arquivo `teste_features.nc` já fornece, prontas: `tp_ultima_obs` (última precipitação observada antes do período de teste, dez/2022) e `lag_meses` (defasagem de 1 a 24 meses até cada alvo). Isso são, na prática, features de "persistência com defasagem" já entregues pelos organizadores.
- Fora isso, a página **não descreve nenhuma feature derivada oficial** (não há menção a lags, médias móveis, anomalias, sazonalidade, etc. como parte do dataset). Tudo o que segue abaixo é sugestão nossa.

## Ideias sugeridas pela análise **[Sugestão da análise]**

- **Lags:** valores de `tp` e das demais variáveis em `M-1, M-2, M-3, ...` além do mês `M` usado oficialmente como entrada.
- **Médias móveis:** média das últimas 3/6/12 observações de cada variável, para suavizar ruído e capturar tendência.
- **Climatologia por ponto/mês:** média histórica de cada variável (especialmente `tp`) para aquele ponto de grade e mês do calendário — útil tanto como feature quanto como baseline (Seção 9).
- **Anomalias:** valor observado menos a climatologia do ponto/mês — pode ajudar o modelo a focar em desvios em vez de reaprender o ciclo sazonal básico.
- **Sazonalidade / mês do ano:** codificação cíclica do mês (`sin`/`cos`) como feature categórica/numérica.
- **Estatísticas espaciais:** médias/desvios-padrão em janelas espaciais (ex.: média dos 8 vizinhos de cada ponto), para suavizar ruído local e capturar contexto regional.
- **Gradientes espaciais:** diferenças entre pontos vizinhos (proxy de frentes, gradientes de pressão/temperatura).
- **Médias regionais:** agregações por sub-região da América do Sul (ex.: Amazônia, Nordeste, Sul, Andes) como features adicionais ou contexto de macro-escala.
- **Variabilidade temporal:** desvio-padrão das últimas N observações por ponto, como proxy de "instabilidade" atmosférica recente.
- **Interações entre variáveis:** por exemplo, umidade × temperatura, ou vento zonal × vento meridional (magnitude e direção do vento resultante).
- **Índices climáticos externos** (ver também Seção 13): incorporação de índices como ENSO/ONI como features de contexto de larga escala, se permitido e devidamente declarado.

Nenhuma dessas ideias deve ser assumida como eficaz sem validação empírica adequada (Seção 12).

---

# 12. Validação

**Por que um split aleatório é problemático aqui:** os dados são uma série temporal mensal com forte autocorrelação (meses vizinhos são parecidos, há sazonalidade e possíveis tendências de longo prazo). Um split aleatório (embaralhando meses entre treino e validação) permitiria que o modelo "veja" informações de meses muito próximos aos que está tentando prever (por exemplo, treinar com fev/2010 e validar com jan/2010 e mar/2010), inflando artificialmente a métrica de validação e mascarando o desempenho real em previsão *out-of-sample* futura — exatamente o cenário real da competição, em que se prevê 2023–2024 usando apenas dados até 2022.

## Alternativas sugeridas **[Sugestão da análise]**

**1. Split temporal simples (holdout no final da série):**

```text
1940 ───────────────────── 2015 | 2016 ───── 2020 | 2021 ─ 2022
              treinamento              validação        teste-like (opcional)
```

Reservar os últimos anos de treino (ex.: 2016–2022) como validação, treinando apenas com dados anteriores — simula diretamente a situação real de prever o futuro a partir do passado.

**2. Validação em janela deslizante / expanding window (rolling / forward validation):**

Treinar com `[1940, Y]`, validar em `[Y+1, Y+1]` (ou um pequeno bloco), depois avançar `Y` e repetir — dá múltiplas estimativas de RMSE "fora da amostra" ao longo de diferentes períodos, reduzindo a dependência de um único corte arbitrário.

**3. Validação por blocos anuais recentes**, dado que a avaliação oficial usa 2023 (público) e 2024 (privado): reservar, por exemplo, 2021–2022 como "proxy" do comportamento do leaderboard público/privado, já que são os anos mais recentes disponíveis no treino e mais parecidos (em termos de tendência climática) com 2023–2024.

**Como simular o problema real:**
- Sempre treinar apenas com dados anteriores ao ponto de corte escolhido, nunca usar meses futuros (em relação ao corte) para gerar features ou treinar o modelo.
- Replicar exatamente a defasagem usada no teste oficial (features do mês `M` → previsão de `M+1`, sem atalhos).

**Como evitar leakage:**
- Não normalizar/padronizar estatísticas (médias, desvios-padrão, climatologia) usando o período de validação/teste — calcular essas estatísticas apenas com dados de treino.
- Cuidado especial com features de "climatologia por ponto/mês" (Seção 11): se calculadas usando todo o histórico (incluindo anos de validação), vazam informação futura para dentro da validação.

**Como escolher períodos de validação:** priorizar os anos mais recentes do treino disponível (mais parecidos climatologicamente com 2023–2024) e, se possível, usar mais de um período de validação (rolling) para reduzir variância na estimativa.

**Como medir RMSE localmente:** implementar exatamente a fórmula da Seção 8 (RMSE "achatado" sobre todos os pontos de grade × todos os meses do conjunto de validação escolhido), para que o número seja comparável (em espírito, não em valor absoluto) ao que o leaderboard do Kaggle reportará.

**Como comparar experimentos:** manter um mesmo protocolo de validação fixo (mesmo corte temporal, mesma métrica, mesmas regras de pré-processamento) entre todos os experimentos da equipe, documentando resultados (ex.: uma planilha/log de experimentos) para que comparações sejam justas.

---

# 13. Dados externos

## O que as regras oficiais dizem

Texto oficial da aba *Rules* (Seção "DADOS EXTERNOS E FERRAMENTAS"):

> "Você pode usar dados que não sejam os Dados da Competição ('Dados Externos') para desenvolver e testar suas Submissões. No entanto, você deverá garantir que os Dados Externos sejam de domínio público e igualmente acessíveis a todos os Participantes da Competição para os fins da competição, sem custo para os demais Participantes, ou que atendam aos critérios de Razoabilidade descritos na Seção 2.6.b abaixo."

**Não encontrado na documentação pública:** o detalhamento completo do critério de "Razoabilidade" citado (Seção 2.6.b) não estava visível/expandido no texto capturado da página — a regra apenas referencia essa seção, sem reproduzi-la integralmente no trecho acessado.

Resumo das condições oficiais para uso de dados externos:
1. Devem ser de **domínio público**;
2. Devem ser **igualmente acessíveis a todos os participantes**, sem custo;
3. **OU** atender ao critério de "Razoabilidade" da Seção 2.6.b (não detalhado no texto acessado);
4. (Implícito pelo enunciado do desafio, fora das Rules) — "dados externos públicos são permitidos, desde que declarados" — a declaração do uso é esperada, embora o mecanismo exato de declaração (fórum, notebook, formulário) não esteja explicitado na aba Rules.

## Fontes públicas potencialmente relevantes **[Sugestão da análise — não misturar com regra oficial]**

Estas são sugestões técnicas, não indicações oficiais da competição:

| Fonte potencial | O que fornece | Período | Resolução | Utilidade possível | Risco de leakage | Como declarar (sugestão) |
|---|---|---|---|---|---|---|
| ERA5 completo (Copernicus CDS) | Mais variáveis/níveis do que os 10 distribuídos | 1940–presente | 0,25° (nativa) | Enriquecer features de entrada com variáveis adicionais do próprio ERA5 | Baixo, se limitado ao período de treino (≤2022); **alto se usado para obter dados de 2023–2024**, pois pode reintroduzir a variável-alvo que os organizadores removeram propositalmente | Declarar no fórum/discussão da competição, especificando variáveis e período usados |
| Índices ENSO/ONI (NOAA) | Índice de El Niño/La Niña | histórico longo, mensal | pontual (índice único, não espacial) | Feature de contexto climático de larga escala, relevante para precipitação na América do Sul | Baixo, se o índice usado for definido/calculado apenas com base em dados até o mês `M` (mesma regra de defasagem do problema) | Declarar a fonte exata (ex.: NOAA CPC) e o período utilizado |
| Dados de SST (temperatura da superfície do mar) | Temperatura oceânica, relacionada a padrões de teleconexão | histórico longo | variável conforme produto | Feature adicional de contexto oceânico | Baixo a moderado, dependendo do produto e período | Declarar produto/fonte e garantir acesso público igualitário |
| Outras reanálises (ex.: NCEP/NCAR, MERRA-2) | Produtos atmosféricos alternativos | históricos longos | variável | Validação cruzada de features, ensemble de fontes | Moderado — misturar reanálises diferentes pode introduzir inconsistências não triviais | Declarar fonte, versão e forma de uso |
| Climatologias públicas (ex.: normais climatológicas) | Médias históricas de referência | períodos-padrão (ex.: 1991–2020) | variável | Comparação com baseline de climatologia (Seção 9) | Baixo | Declarar fonte e período de referência |

Para qualquer fonte externa, a recomendação **[Sugestão da análise]** é: (1) confirmar que é gratuita e publicamente acessível a todos os participantes; (2) documentar exatamente quais variáveis, período e resolução foram usados; (3) nunca incorporar, direta ou indiretamente, a precipitação real do período de teste (2023–2024); (4) declarar o uso conforme as regras da competição assim que houver um canal oficial de declaração (ex.: tópico no fórum).

---

# 14. Submission

**Formato esperado:** arquivo **CSV**.

**Colunas:** `id` e `tp_mm_day`.

**Formato do `id`:** `ano_mês_lat_lon`, com duas casas decimais em latitude e longitude (ex.: `2023_01_-30.00_-53.00`). O `id` já vem pronto, na ordem correta, dentro de `sample_submission.csv` — a página instrui explicitamente: **"não o reconstrua"**.

**Ordem:** a ordem exata das linhas é a do `sample_submission.csv` fornecido.

**Identificação dos pontos:** cada linha corresponde a um par único (mês-alvo, ponto de grade).

**Número de previsões:** **1.885.464** linhas no total (24 meses × 78.561 pontos de grade), confirmado tanto pelo texto da aba Data quanto pela contagem de valores únicos observada na prévia do `sample_submission.csv` (1.885.464 valores únicos de `id`).

**Formato numérico:** `tp_mm_day` é um valor decimal (mm/dia); o sample usa 0 (zero) como placeholder, e o exemplo da seção Evaluation usa valores como `3.812`, `4.507`, `5.226` (3 casas decimais no exemplo, mas não há confirmação de que 3 casas sejam obrigatórias).

**Sample submission:** `sample_submission.csv`, 48,15 MB, 2 colunas, 1.885.464 linhas, disponível para download na aba Data.

Exemplo oficial de estrutura (retirado da seção *Evaluation* — nota: usa `2025` como ano ilustrativo, o que diverge do intervalo real 2023–2024 usado no `sample_submission.csv` real; ver contradições no topo do documento):

```csv
id,tp_mm_day
2025_01_-30.00_-53.00,3.812
2025_01_-30.00_-52.75,4.507
2025_01_-30.00_-52.50,5.226
```

Exemplo real observado na prévia do `sample_submission.csv` (primeiras linhas, com `tp_mm_day` = 0 como placeholder):

```csv
id,tp_mm_day
2023_01_-60.00_-90.00,0.0
2023_01_-60.00_-89.75,0.0
2023_01_-60.00_-89.50,0.0
2023_01_-60.00_-89.25,0.0
```

---

# 15. Limitações e regras da competição

- **Tamanho máximo da equipe:** 4 integrantes (regra específica da competição — ver observação de contradição com o texto genérico "10" exibido na aba Team, no topo do documento).
- **Limite de submissões:** 5 por dia (regra específica da competição).
- **Dados externos:** permitidos, desde que de domínio público, igualmente acessíveis e gratuitos a todos os participantes, ou conforme critério de "Razoabilidade" (Seção 2.6.b, não detalhado no texto acessado). Uso deve ser declarado.
- **Regras de código:**
  - Compartilhamento **privado** de código/dados fora da própria equipe é proibido (inclusive entre equipes diferentes, exceto em caso de fusão).
  - Compartilhamento **público** de código é permitido, mas deve ser feito nos fóruns/notebooks associados à competição, sob licença aprovada pela Open Source Initiative, sem restrição de uso comercial.
  - Se usar código open source de terceiros no modelo, ele também deve ter licença aprovada pela OSI, sem restringir uso comercial.
- **Uso e acesso aos dados:** apenas para fins não comerciais — participação na competição e nos fóruns Kaggle, e pesquisa acadêmica/educacional.
- **Licença da submissão vencedora:** deve ser licenciada (submissão + código-fonte) sob licença OSI-aprovada, sem restrição de uso comercial.
- **Restrição computacional:** **Não encontrado na documentação pública** (nenhuma menção a limites de tempo de execução, hardware exigido/permitido, ou tamanho máximo de notebook/modelo).
- **Requisito de publicação (vencedores):** o vencedor deve entregar ao patrocinador o código-fonte do modelo final (treino + inferência) e documentação do ambiente computacional necessário, como condição para receber o prêmio.
- **Penalidades:** desqualificação em caso de múltiplas contas, compartilhamento privado indevido de código, uso de informação obtida por rotulagem manual/humana dos dados de validação/teste, ou qualquer tentativa de fraudar/comprometer a operação da competição (conforme Regras Fundamentais do Kaggle).
- **Elegibilidade:** conforme Regras Fundamentais do Kaggle — maior de 18 anos (ou maioridade local), conta registrada no Kaggle, não residente em determinadas jurisdições sob sanções (Crimeia, "DNR"/"LNR", Cuba, Irã, Coreia do Norte) nem sujeito a controles de exportação dos EUA.
- **Critério de desempate:** em caso de empate, vence a submissão que foi enviada **primeiro** à competição (Regras Fundamentais do Kaggle).
- **Fusão de equipes:** permitida, feita pelo líder da equipe; a equipe combinada deve ter, até o prazo de fusão, um número total de submissões igual ou inferior ao máximo permitido (submissões/dia × dias de competição).
- **Prêmio:** sem valor monetário — certificado de premiação e reconhecimento no ranking oficial para o 1º ao 3º lugar; não concede pontos nem medalhas Kaggle.

---

# 16. Cronograma

| Evento | Data | Importância |
|---|---|---|
| Início da competição (Start) | **~14/09/2026** (aproximado — a página mostrava "2 days ago" em 16/09/2026; data exata não exposta pela interface) | Abertura de submissões |
| Encerramento (Close) | **~23/09/2026** (aproximado — a página mostrava "7 days to go" em 16/09/2026; data exata não exposta pela interface) | Prazo final de submissão; ponto em que o leaderboard privado (2024) é revelado |
| Prazo de fusão de equipes | **Não encontrado na documentação pública** (regras referenciam a página de "Cronograma da competição" no Overview, mas nenhuma data específica de fusão distinta do encerramento foi encontrada) | — |
| Revelação do resultado final (leaderboard privado) | Coincide com o encerramento (Close), conforme regras gerais de determinação de vencedores | Define a classificação final |

⚠️ As datas de início e encerramento acima são **aproximações calculadas** a partir dos contadores relativos ("2 days ago" / "7 days to go") exibidos na página em 16/09/2026 — a interface do Kaggle não expôs timestamps exatos (nem em texto visível, nem em atributos de data acessíveis via inspeção da página) no momento da análise. A equipe deve **conferir a data exata diretamente na aba Overview da competição**, na barra "Start/Close".

Estatísticas de participação no momento da análise (16/09/2026): **80 Entrants, 25 Participants, 19 Teams, 76 Submissions.**

---

# 17. Riscos técnicos

- **Leakage temporal:** uso indevido de dados externos que possam conter, direta ou indiretamente, a precipitação real de 2023–2024 (ver Seção 5 e 13).
- **Overfitting:** dataset de treino relativamente pequeno em número de "amostras temporais" (~996 meses) frente à alta dimensionalidade espacial (78.561 pontos por amostra) — especialmente crítico para arquiteturas de deep learning mais complexas (Seções 10.3–10.6).
- **Alta dimensionalidade:** 78.561 pontos de grade × 10 variáveis por mês — pipelines de dados e treino precisam ser eficientes em memória (arquivos NetCDF grandes: 2,06 GB no total).
- **Correlação espacial:** pontos de grade vizinhos são fortemente correlacionados — validação e modelagem que ignorem essa estrutura podem ser enganosas ou subótimas.
- **Distribuição assimétrica da chuva:** **[Sugestão da análise]** precipitação mensal tende a ter distribuição assimétrica (muitos valores baixos, cauda de eventos extremos) — não confirmado oficialmente para este dataset específico, mas é uma expectativa técnica razoável a ser verificada empiricamademente.
- **Eventos extremos / dificuldade de prever extremos:** RMSE penaliza fortemente grandes erros (erro quadrático) — meses/regiões de chuva extrema podem dominar a métrica final, mesmo sendo uma minoria dos casos.
- **Diferença entre leaderboard público e privado:** o público usa 2023, o privado usa 2024 — desempenho no público não garante desempenho equivalente no privado, especialmente se houver overfitting ao padrão climático específico de 2023 (ex.: eventos El Niño/La Niña daquele ano específico).
- **Custo computacional e memória:** arquivos NetCDF de até ~187 MB cada (ex.: `treino_tp.nc`), totalizando 2,06 GB — manipular todas as 10 variáveis simultaneamente ao longo de ~996 meses pode exigir cuidado com uso de memória, especialmente em abordagens de deep learning espaço-temporal.
- **Resolução espacial:** 0,25° é relativamente fina (78.561 pontos) — pode ser computacionalmente custoso para arquiteturas convolucionais/transformer sem alguma forma de downsampling, patching ou treino regional.
- **Desalinhamento entre datasets externos:** caso a equipe use dados externos (Seção 13), grades, resoluções e convenções de unidade diferentes das do dataset oficial podem introduzir erros de alinhamento espacial/temporal se não tratados com cuidado (reamostragem, interpolação).
- **Ambiguidade na agregação do RMEE (peso por célula):** conforme observado na Seção 8, não está confirmado se o RMSE pondera por área de célula (relevante em grades lat/lon regulares) — a equipe deve assumir peso uniforme por padrão, mas ficar atenta a esse ponto.

---

# 18. Plano de desenvolvimento sugerido **[Sugestão da análise]**

```text
1. Entender os dados
        ↓  (baixar/inspecionar os 13 arquivos, confirmar shapes, unidades, NaNs, faixas de valores)
2. Criar baseline
        ↓  (climatologia por ponto/mês — o "piso" citado oficialmente pela página)
3. Criar validação temporal
        ↓  (split ou rolling window respeitando a ordem cronológica, sem leakage)
4. Treinar primeiro modelo
        ↓  (ex.: modelo tabular simples — Seção 10.2 — para ter um ciclo completo rodando)
5. Analisar erros
        ↓  (RMSE por região, por mês do ano, por magnitude de chuva — identificar pontos fracos)
6. Feature engineering
        ↓  (lags, anomalias, climatologia, features espaciais — Seção 11)
7. Modelo espacial
        ↓  (CNN — Seção 10.3 — para capturar estrutura de vizinhança)
8. Modelo espaço-temporal
        ↓  (ConvLSTM/3D-CNN ou Transformer — Seções 10.5/10.6 — se o tempo e os recursos permitirem)
9. Ensemble
        ↓  (combinar previsões de modelos diferentes para reduzir variância)
10. Submissão
        (gerar CSV no formato exato do sample_submission.csv, validar contagem de linhas e ids antes de enviar)
```

Objetivo de cada etapa:
1. **Entender os dados** — pré-requisito para qualquer decisão de modelagem; evita suposições erradas sobre unidades/distribuições (esta análise já deixou marcado o que não pôde ser confirmado).
2. **Criar baseline** — estabelece o "piso" mínimo de qualidade (climatologia), citado como referência pelos próprios organizadores.
3. **Criar validação temporal** — garante que toda comparação futura entre modelos seja justa e realista frente ao cenário real da competição (prever o futuro com dados do passado).
4. **Treinar primeiro modelo** — valida o pipeline de ponta a ponta (dados → features → modelo → submissão) antes de investir em complexidade.
5. **Analisar erros** — direciona onde investir esforço (regiões, meses, magnitudes de erro mais problemáticas).
6. **Feature engineering** — melhora a capacidade preditiva com informação adicional derivada dos dados brutos.
7. **Modelo espacial** — explora a estrutura de grade explicitamente, algo que modelos tabulares simples ignoram.
8. **Modelo espaço-temporal** — combina estrutura espacial e temporal, potencialmente o modelo mais alinhado à física do problema, se os recursos permitirem.
9. **Ensemble** — reduz variância combinando pontos fortes de diferentes abordagens.
10. **Submissão** — validação final de formato antes do envio (evitar erros bobos de formatação, que zerariam a pontuação).

---

# 19. Organização recomendada do projeto **[Sugestão da análise]**

```text
project/
├── data/
│   ├── raw/                # arquivos .nc e .csv originais, como baixados do Kaggle
│   └── processed/          # dados intermediários (ex.: arrays numpy/zarr já alinhados)
├── notebooks/               # exploração, EDA, protótipos rápidos
├── src/
│   ├── preprocessing/       # leitura dos .nc, alinhamento de grade, tratamento de NaN
│   ├── features/            # lags, climatologia, anomalias, features espaciais (Seção 11)
│   ├── models/               # implementações de baseline, tabular, CNN, ConvLSTM, etc.
│   ├── validation/           # split temporal, rolling window, cálculo de RMSE local (Seção 12)
│   └── inference/            # geração da submissão a partir de um modelo treinado
├── configs/                  # arquivos de configuração de experimentos (hiperparâmetros, paths)
├── experiments/               # logs/resultados de cada experimento (RMSE local, configuração usada)
├── submissions/                # arquivos CSV gerados, prontos para envio ao Kaggle
├── models/                     # pesos/artefatos de modelos treinados
├── README.md
└── requirements.txt
```

Essa estrutura separa claramente dados brutos de processados, isola features de modelos, e mantém um histórico de experimentos e submissões — importante para uma equipe de até 4 pessoas trabalhando em paralelo em diferentes abordagens (Seção 10).

---

# 20. Glossário

- **ERA5:** conjunto de dados de reanálise atmosférica global de quinta geração do ECMWF, usado como fonte de todas as variáveis desta competição.
- **Reanalysis (reanálise):** produto climático que combina observações históricas com modelos numéricos para reconstruir o estado da atmosfera no passado de forma espacialmente e temporalmente consistente.
- **Precipitation (precipitação):** quantidade de água (chuva) que cai sobre uma área, aqui expressa como taxa média diária (mm/dia) para o mês.
- **Climatology (climatologia):** média histórica de uma variável climática para um determinado local e período do ano (ex.: média de chuva em janeiro ao longo de várias décadas) — citada oficialmente como o "patamar a bater" da competição.
- **Anomaly (anomalia):** desvio de uma observação em relação à sua climatologia (valor observado menos a média histórica esperada).
- **Grid (grade):** malha regular de pontos espaciais (aqui, 301 × 261 pontos) sobre os quais os dados são organizados e as previsões devem ser feitas.
- **Latitude:** coordenada de posição norte-sul (aqui, de 60°S a 15°N).
- **Longitude:** coordenada de posição leste-oeste (aqui, de 90°O a 25°O).
- **RMSE (Root Mean Squared Error):** métrica de erro que penaliza quadraticamente desvios entre valor previsto e valor real, depois extrai a raiz quadrada da média — métrica oficial única desta competição.
- **Temporal leakage (vazamento temporal):** uso indevido, direto ou indireto, de informação do futuro (em relação ao ponto de previsão) durante o treino ou validação, inflando artificialmente o desempenho aparente do modelo.
- **Spatial correlation (correlação espacial):** tendência de pontos geograficamente próximos apresentarem valores semelhantes/correlacionados — relevante tanto para modelagem quanto para validação.
- **Ensemble:** combinação das previsões de múltiplos modelos, geralmente para reduzir variância e melhorar robustez frente a um único modelo.
- **Baseline:** modelo ou abordagem simples, usado como referência mínima de desempenho a ser superada por abordagens mais sofisticadas.
- **Leaderboard público:** ranking visível durante a competição, calculado sobre uma parte do conjunto de teste (aqui, o ano de 2023 — confirmado oficialmente; a página do leaderboard indica ~50% dos dados de teste).
- **Leaderboard privado:** ranking que define a classificação final, calculado sobre a outra parte do conjunto de teste (aqui, o ano de 2024), revelado apenas ao final da competição.

---

# 21. Checklist final da equipe

## Dados

- [ ] Entender todas as variáveis (as 10 do ERA5 distribuídas, mesmo sem unidades oficialmente confirmadas para 9 delas)
- [ ] Confirmar dimensões (301 lat × 261 lon; ~996 meses de treino)
- [ ] Confirmar unidades (mm/dia confirmado para `tp`/`tp_alvo`; demais variáveis devem ser verificadas empiricamente, já que não há confirmação oficial)
- [ ] Confirmar target (`tp_alvo` em `treino_tp_alvo.nc`, já deslocado; último mês = NaN)
- [ ] Confirmar datas (treino: jan/1940–dez/2022; avaliação: jan/2023–dez/2024, público=2023/privado=2024)

## Validação

- [ ] Criar split temporal (nunca aleatório — ver Seção 12)
- [ ] Implementar RMSE (fórmula da Seção 8, agregada sobre todos os pontos × meses)
- [ ] Verificar leakage (especialmente ao usar dados externos — Seção 13)

## Modelos

- [ ] Baseline (climatologia por ponto/mês — citada oficialmente como o "patamar a bater")
- [ ] Modelo ML tabular
- [ ] Modelo espacial (CNN)
- [ ] Modelo temporal/espaço-temporal
- [ ] Comparação de experimentos (protocolo de validação fixo e documentado)

## Submission

- [ ] Formato correto (CSV, colunas `id` e `tp_mm_day`)
- [ ] Todas as células da grade (78.561 pontos por mês)
- [ ] Todas as datas necessárias (24 meses, 2023–2024)
- [ ] Valores válidos (1.885.464 linhas no total; sem usar o `id` reconstruído manualmente — usar o do `sample_submission.csv`)
- [ ] Submissão de teste (respeitando o limite de 5 envios/dia, confirmado nas Rules)

---

# TL;DR

1. **O que precisamos prever:** a precipitação média do mês seguinte (M+1), em mm/dia, para cada ponto de uma grade regular de 0,25° sobre a América do Sul.
2. **Quais dados temos:** 10 variáveis mensais do ERA5 (precipitação + 9 variáveis atmosféricas, a maioria em 850 hPa), de jan/1940 a dez/2022, em grade de 301×261 pontos (78.561 pontos/mês).
3. **Qual é o target:** `tp_alvo` (precipitação do mês seguinte, mm/dia), já pré-deslocado no arquivo `treino_tp_alvo.nc`.
4. **Qual é a métrica:** RMSE, calculado sobre todos os pontos de grade e todos os meses do período de teste (fórmula formalizada por nós na Seção 8, já que a página não publica a fórmula explícita).
5. **Como funciona a divisão temporal:** treino = 1940–2022; avaliação = 24 meses (jan/2023–dez/2024); 2023 alimenta o leaderboard público, 2024 define o resultado final (leaderboard privado).
6. **Quais são as restrições:** equipes de até 4 pessoas (regra específica — atenção à divergência com o texto "10" da interface); até 5 submissões por dia (não 3, como no briefing inicial); dados externos permitidos se públicos, gratuitos e declarados; código da submissão vencedora deve ser entregue com licença open source.
7. **Não há baseline oficial nem notebooks/discussões publicados** até o momento da análise (16/09/2026) — a única referência é conceitual: "a climatologia é o patamar a bater".
8. **A precipitação real de 2023–2024 não está em nenhum arquivo distribuído** — reduz o risco de leakage direto, mas exige cuidado redobrado com dados externos.
9. **`teste_features.nc` já entrega**, prontos, `tp_ultima_obs` (última observação, dez/2022) e `lag_meses` (defasagem de 1 a 24) — úteis como features de persistência.
10. **O `id` de submissão já vem pronto** no `sample_submission.csv` (formato `ano_mês_lat_lon`); a página instrui explicitamente a não reconstruí-lo.
11. **Total de previsões esperadas:** 1.885.464 linhas (24 meses × 78.561 pontos de grade).
12. **Principais desafios técnicos:** poucas "amostras temporais" (~996 meses) frente à alta dimensionalidade espacial; correlação espacial forte; possível distribuição assimétrica da chuva; RMSE penaliza fortemente eventos extremos; risco de diferença de desempenho entre 2023 (público) e 2024 (privado).
13. **Nenhuma unidade das 9 variáveis atmosféricas auxiliares está confirmada oficialmente** (apenas `tp`/`tp_mm_day` em mm/dia é confirmado) — a equipe deve inspecionar os arquivos empiricamente antes de assumir unidades padrão do ERA5.
14. **Primeiros passos recomendados:** (1) baixar e inspecionar os 13 arquivos, confirmando shapes/NaNs/faixas de valores; (2) implementar o baseline de climatologia por ponto/mês; (3) montar uma validação temporal (nunca split aleatório); (4) treinar um primeiro modelo simples de ponta a ponta antes de evoluir para abordagens espaciais/espaço-temporais mais complexas.
15. **Datas de início/fim da competição são aproximadas** (não há timestamp exato exposto pela interface do Kaggle no momento da análise) — a equipe deve conferir a data exata diretamente na aba Overview.
16. **Prêmio é simbólico** (certificado + reconhecimento no ranking, sem valor monetário nem pontos/medalhas Kaggle) — o foco é o mérito técnico da solução.

---

## Fontes

- Aba Overview: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/overview`
- Aba Data: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/data`
- Aba Code: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/code`
- Aba Models: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/models`
- Aba Discussion: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/discussion`
- Aba Leaderboard: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/leaderboard`
- Aba Rules: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/rules`
- Aba Team: `https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul/team`

Todas as informações marcadas como oficiais foram coletadas por navegação direta nessas páginas em **16/09/2026**. Este documento não inclui nenhuma informação de fontes externas ao Kaggle.
