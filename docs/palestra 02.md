0:022 segundosBeleza? Então, pessoal, uma boa tarde a todos. Sejam bem-vindos novamente para pra segunda parte do nosso esquenta aqui do do Rakaton 2016 eh 2026 do Work.
0:1515 segundosEh, agora à tarde a gente vai ter a palestra do Carlos Calaj, do Carlos Augusto Calaje. Ele é doutorando na
0:2323 segundosUniversidade Federal de Pelotas e é especialista em aprendizado de máquina. e ele eh preparou um material aqui, né?
0:3030 segundosEntão, como eu tinha comentado mais cedo, né, [roncando] pela manhã com a Dra. Marília, a gente eh teve uma um
0:3838 segundospanorama sobre o problema. Agora a gente vai falar um pouquinho sobre uma das possíveis eh soluções que é o que a
0:4646 segundosgente tá tentando propor aqui no na competição, né, que é o uso de aprendizado de marketing para fazer eh para fazer a previsão a previsão climática de precipitação.
0:5757 segundosEntão, eh desejar eu, eh em nome aqui de todos os participantes da comissão organizadora do WCAP, eu agradeço ao
1:061 minuto e 6 segundosCarlos pela boa vontade e disponibilidade. Muito obrigado, Carlos.
1:111 minuto e 11 segundosE eu acho que é isso. A palavra tá contigo. Eh, quando tu quiser compartilhar tua tela aí, dar início, por favor.
1:191 minuto e 19 segundosOlá. Bom, boa tarde, gente. Obrigado pelo pela eh
1:261 minuto e 26 segundospela participação aí. Eh, deixa eu compartilhar minha tela aqui rapidinho, ver se vai funcionar certinho.
1:351 minuto e 35 segundosVocês conseguem ver? Sim. Perfeito, Carlos. Tá certinho.
1:421 minuto e 42 segundosO problema é que me tirou a minha outra tela aqui. [risadas] Ah, deixa eu ver aqui como é que eu
1:521 minuto e 52 segundosAh, troquei. É, não consigo apresentar sem me tirar outra tela. Ã, bom, vamos assim.
2:032 minutos e 3 segundosQualquer coisa eu Bom, pessoal, então tá. Eh, boa tarde.
2:092 minutos e 9 segundosVocês estão me ouvindo bem? Eu troquei de microfone aqui. Estão tá conseguindoar bem aqui o Tá perfeito.
2:162 minutos e 16 segundosPerim muito bem. Ã, bom, pessoal, então, eh, boa tarde. Eh, meu meu nome é
2:232 minutos e 23 segundosCarlos, né? Deixa eu colocar um timer aqui, senão eh, eu sou um pouco prolixo, gente. Então, eh eu tenho que tá me
2:312 minutos e 31 segundoscuidando aqui com o tempo. Então, botar um timerinho aqui. Perfeito. Eh, eu me chamo Carlos Carlos Calaj. Eh, como o
2:392 minutos e 39 segundosGerônio falou, eu sou aqui da Universidade eh Federal de Pelotas, né?
2:442 minutos e 44 segundosVou deixar aqui o slide para vocês eh eventualmente que quiserem me seguir em alguma das redes aí. Esse é o meu e-mail institucional também.
2:532 minutos e 53 segundosH, e bom, eh, só para rapidamente, né, eu fiz a
2:592 minutos e 59 segundosgraduação, eh, mestrado e tô agora, eh, fazendo doutorado na FFPEL. Ã, desde o
3:073 minutos e 7 segundosinício eu, ã, ali na graduação já mexia com IA. Eh, e há muito tempo eu venho
3:153 minutos e 15 segundosparticipando de diversos projetos que envolvem, né, ã, inteligência artificial, ã, em diferentes níveis.
3:223 minutos e 22 segundosEntão, trabalhei desde coisas bem básicas, como eh coisas com ciência de dados, eh
3:293 minutos e 29 segundospredição, predições mais eh como é que eu vou dizer, mais tranquilas, né? Ã,
3:363 minutos e 36 segundosaté coisas mais avançadas, como atualmente que eu trabalho com LLM, não posso exatamente falar o projeto, mas ã atualmente eu trabalho com eh LLMs, né?
3:493 minutos e 49 segundosTreinamento de LLMs em si.
3:513 minutos e 51 segundosH, também já trabalhei com visão computacional, trabalhei com muita coisa. Eh, então acho que eu tenho uma uma bagagem legal aí de de projetos, né?
4:024 minutos e 2 segundosÃ, eu vou eh eu não tô vendo o chat aqui, então se vocês tiverem dúvidas podem eh mandem aí o Jerônimo ou alguém
4:114 minutos e 11 segundoseh me interrompe eh e me avisa qualquer coisa, ã que aí a gente para e e
4:174 minutos e 17 segundosconversa, né? Eu também queria um pouco a participação de vocês. Eh, talvez vamos ver eh, como é que vai ser o
4:264 minutos e 26 segundostempo, né? Mas tem algumas partes aqui que eu trouxe para que fosse um pouco mais divertido, além de só uma um workshop
4:354 minutos e 35 segundoseh mais palestra mesmo, né? [roncando] Mas bom, gente, eh uma última coisa só eh
4:434 minutos e 43 segundosque eu gostaria de pontuar, né? Vou voltar aqui pro nosso primeiro slide. Eu faço parte de um eh grupo de pesquisa chamado Hub de Inteligência Artificial.
4:534 minutos e 53 segundosEntão vocês também podem ver eh ali nas minhas redes, né? E a nossa é um projeto de pesquisa, extensão e ensino. Então a
5:015 minutos e 1 segundogente atua nas três frentes. A gente trabalha com empresas que eh buscam eh não só aplicação, mas conhecimento, né?
5:115 minutos e 11 segundosÃ trabalhamos com projetos de estado da arte. Então, eh, a gente costuma
5:185 minutos e 18 segundosdesenvolver um pouco mais a os os alunos dentro da faculdade, né, com os projetos, com empresas eh reais, com empresas que vem, né, nos contratar. E a
5:275 minutos e 27 segundosnossa contribuição pra sociedade é em desenvolver esse esse mercado e essas
5:335 minutos e 33 segundosempresas regionais também. Só um breve resumo sobre o meu a minha a minha
5:405 minutos e 40 segundosatuação, né, ali do do hub. Bom, vamos começar então a nossa palestra. Eh,
5:515 minutos e 51 segundoseu vou conversar, eu eu eu vou trazer algumas questões filosóficas, eu eu vou fazer uma conversa aqui com vocês e eu
5:575 minutos e 57 segundosquero que vocês eh eventualmente h eh interajam comigo, né?
6:046 minutos e 4 segundos[roncando]
6:046 minutos e 4 segundosH, mas bom, eu não sei como é qual é o grau de cada um de vocês em relação a IA, o quanto
6:136 minutos e 13 segundosvocês estão eh t conhecimento e o quanto vocês estão muito muito distante dos dos conhecimentos, né? Então, tive essa essa
6:226 minutos e 22 segundostarefa um pouco complicada aqui que o Gerônimo me passou de tentar fazer esse apanhado geral de introdução a IA e tentar falar um pouquinho dos algoritmos
6:316 minutos e 31 segundoslá na frente, tá? Então, eh, eu vou dar uma pincelada sobre as áreas, né? Ã, eu
6:386 minutos e 38 segundosnão quero me ater muito à matemática aqui dos dos modelos, o funcionamento tão aprofundado, mas eu quero dar essa
6:456 minutos e 45 segundosnoção mais intuitiva para que vocês entendam o que tá acontecendo meio por baixo dos panos.
6:536 minutos e 53 segundosBom, eh, até um tempo atrás, eh,
7:007 minutosvão, a gente pode pensar ali na revolução industrial, ã, nós tivemos um, um grande avanço, eh,
7:087 minutos e 8 segundosno sentido de automatizar certas tarefas que eram muito manuais, muito repetitivas, né? Então,
7:177 minutos e 17 segundoseh, em algum ponto a gente parou de, sei lá, alguém parou de ter que ficar
7:237 minutos e 23 segundospisando num pedal de tear, né, de de tecido e colocamos um motorzinho ali
7:307 minutos e 30 segundospara fazer aquele trabalho, né? Paramos de eh ter que necessariamente usar eh
7:387 minutos e 38 segundosforça mecânica para abrir um portão, por exemplo, e colocamos o motor ali, né?
7:447 minutos e 44 segundosEntão, se vocês pensarem, diversos diversas tarefas foram sendo eh automatizadas ao longo desse tempo, né?
7:547 minutos e 54 segundosEntretanto, se vocês pararem para pensar, grande parte dessas tarefas foram tarefas
8:008 minutospuramente eh mecânicas, né? foram tarefas bastante ã
8:098 minutos e 9 segundosque não necessariamente exigiam um um grau de eh raciocínio, um grau de um grau
8:188 minutos e 18 segundosdecisionário, né? Ã, então, por exemplo, abre um portão, né? O portão sempre abre do mesmo jeito, né?
8:278 minutos e 27 segundosNão, não tem muita diferença. Não abre pros lados ou só abre para um, para um lado e fecha para outro, né?
8:388 minutos e 38 segundosCoisas então que a gente consegue automatizar que não necessariamente necessitam de uma ação humana ali, de um
8:458 minutos e 45 segundosraciocínio humano, né? Ã, isso, entretanto, demorou um pouco de tempo pra gente
8:538 minutos e 53 segundosconseguir automatizar tarefas mais complexas.
8:578 minutos e 57 segundosEh, para quem não sabe muito da história da de inteligência artificial, né? Ã, a
9:059 minutos e 5 segundosnossa área vem vem se desenvolvendo há um bom tempo, né? Então, tem eh dados desde a época de da década de 50, né?
9:139 minutos e 13 segundospesquisadores eh tentando desenvolver essa área.
9:189 minutos e 18 segundosE bom, o ponto era sempre tentar desenvolver ã
9:269 minutos e 26 segundosprogramas que realizassem tarefas que necessariamente precisariam de uma de
9:339 minutos e 33 segundosuma de uma atividade de um ser humano, né? Então, vamos pensar um pouquinho antes da gente entrar eh nos nos
9:409 minutos e 40 segundosconceitos, né? Vamos pensar um pouquinho sobre algumas alguns pontos.
9:479 minutos e 47 segundosEh, pensem, por exemplo, eh, na tarefa de reconhecer um rosto.
9:579 minutos e 57 segundosÃ, pensem se vocês precisassem eh desenvolver um algoritmo que do zero,
10:0510 minutos e 5 segundosquem não conhece que sem sem pensar em IA ainda, né? Mas digamos que vocês quisessem eh desenvolver um um algoritmo
10:1410 minutos e 14 segundosque reconhecesse rostos, né? Então conseguisse reconhecer e separar pessoas através das imagens dos rostos.
10:2510 minutos e 25 segundosComo é que vocês fariam essa tarefa?
10:2710 minutos e 27 segundosVocês conseguem pensar e eh eh formas, né, abordagens?
10:3110 minutos e 31 segundosO o KNN poderia fazer pela questão de pixel. Normalmente as características de face eles têm fitos diferentes, tipo a
10:3910 minutos e 39 segundosmancha de roxo vai identificando todos os critérios assim. Isso.
10:4310 minutos e 43 segundosOutra forma poderia ser é essa é uma forma poder deixar aberto, mas pro pessoal poder compartilhar também, tá?
10:5010 minutos e 50 segundosSim. Eh, eu eu queria não tentar pensar em em aplicações que a gente já tem disponíveis. Pense se vocês fossem de
10:5910 minutos e 59 segundosfato, digamos que vocês peguem a foto da pessoa, né? digamos que você pegue uma foto minha aqui. O que que que
11:0611 minutos e 6 segundoscaracterísticas que vocês usariam para conseguir separar um rosto do outro, né?
11:1311 minutos e 13 segundosEntão assim, eh vamos pensar aqui, talvez vocês devem ter pensado em algumas características, né? Ã, o colega
11:2011 minutos e 20 segundosali citou uma mancha no rosto e e sei lá, alguma característica de cabelo, né?
11:2711 minutos e 27 segundosDaqui a pouco a distância dos olhos, o tamanho dos lábios, o tamanho do nariz. distância, nariz, lábios e olhos.
11:3511 minutos e 35 segundosÃ, e e OK, talvez a gente conseguisse eh pensar, montar um algoritmo que
11:4311 minutos e 43 segundoscapturasse cada uma dessas características, né? Ã, mas notem que primeiro que é uma tarefa bastante
11:5111 minutos e 51 segundosdifícil, né? Mesmo que a gente pense em todas as características possíveis eh metrificadas. Hã,
12:0012 minutose mesmo assim, ã, notem que nós somos tão bons em reconhecer rosto que a
12:0812 minutos e 8 segundosgente, mesmo com máscara, mesmo com a pessoa com chapéu, com um óculos diferente, ah, às vezes a pessoa envelheceu e mesmo assim a gente
12:1612 minutos e 16 segundosconsegue identificar que é aquela pessoa que a gente conheceu lá atrás.
12:2312 minutos e 23 segundosEh, parem um pouquinho para pensar o quão incrível é essa capacidade que a gente tem de fazer isso, né? Ã,
12:3012 minutos e 30 segundose bom, isso é uma tarefa bastante difícil pro para um para um para eh pra gente montar um algoritmo
12:4012 minutos e 40 segundosque faça exatamente isso, né? Ã, e bom, vamos eh entrar nos conceitos, vamos avançar um pouquinho mais, né?
12:5112 minutos e 51 segundosH, pensando um pouco como como a gente poderia fazer, né? Conforme a gente vai avançando, talvez isso vai ficando mais
13:0013 minutosclaro eh com esses algoritmos de de aprendizados de máquina, né? Mas bom, o
13:0813 minutos e 8 segundoso grande ponto aqui é que em algum momento a gente parou e pensou que tá, eu não consigo, mesmo que a gente faça
13:1713 minutos e 17 segundosas milhões de variações de de variáveis que a gente pode pensar de um rosto, a gente nunca vai chegar na característica
13:2513 minutos e 25 segundosque a gente usa para conseguir separar esses rostos.
13:2913 minutos e 29 segundosEh, notem que mesmo a gente sendo excelentes separadores de rosto, a gente não sabe como a gente faz isso. A gente
13:3813 minutos e 38 segundosfaz, a gente sabe separar, mas se a gente precisar botar na ponta do lápis, quais as características quando tu olha
13:4513 minutos e 45 segundospara uma pessoa, tu pensa, tá, é, é essas características que definem essa pessoa, né?
13:5113 minutos e 51 segundosEh, então em algum momento a gente parou para pensar que talvez essa não fosse a melhor abordagem, né? Ahã.
14:0214 minutos e 2 segundosTalvez seja mais fácil a gente passar um monte de fotos de uma pessoa e deixar pro computador, tá?
14:1114 minutos e 11 segundosAprende aí o que que quais as características que tornam essa pessoa essa pessoa.
14:1814 minutos e 18 segundosColoca mais um monte de fotos de outras pessoas diferentes daquelas pessoas e daí a gente delega essa tarefa de ahã
14:2714 minutos e 27 segundosdescobrir essas características pro computador. Então, basicamente é isso que a área de aprendizado de máquina,
14:3414 minutos e 34 segundosque é uma área que se tornou gigantesca, né? Hoje em dia, por exemplo, se grande parte do momento que a gente vê eh
14:4114 minutos e 41 segundosalguém falando sobre IA, na verdade estão querendo falar da área de aprendizado de máquina, né? Grande parte das vezes é isso. Ahã tem toda uma outra
14:5114 minutos e 51 segundosparte da IA que a gente não vai chegar a falar aqui, né? Que são eh a IA mais clássica, tem outras coisas que não são
14:5914 minutos e 59 segundossó necessariamente aprendizado de máquina, né?
15:0215 minutos e 2 segundosMas bom, vamos fazer um exercício aqui, ã, que eu trouxe, eh, só pra gente, eh, exercitar essa, essa questão.
15:1315 minutos e 13 segundosEsses aqui são alguns Pokémons que eu trouxe.
15:1615 minutos e 16 segundosÃ, e aí, bom, vocês conseguem e Carlos, desculpa, vou te interromper só um momentinho. Eu acho que tu não passou
15:2415 minutos e 24 segundoso teu slide. A gente ainda tá vendo de aprendizado. Hum.
15:2915 minutos e 29 segundosPassou. É só um delayzinho que deve ter dado. É um delay.
15:3215 minutos e 32 segundosAh, tá. Ah, agora foi. Desculpa. Toca a ficha aí. [roncando] Bom, gente, ã, eu trouxe aqui alguns Pokémons.
15:4015 minutos e 40 segundosÃ, e aqui tem, eu trouxe uma classe, duas classes apenas, né? Os Pokémons de luta e os Pokémons de água. Ã, olhando
15:5015 minutos e 50 segundosesses slides e mais para frente eu vou fazer essa pergunta para vocês eh me responderem. Por enquanto, só e eh
15:5815 minutos e 58 segundosobservem e pensem como é que a gente poderia separar um Pokémon de água de um Pokémon de luta. Olhem para esses para
16:0716 minutos e 7 segundosesses exemplos aí e pensem aí com vocês quais as características que talvez separem um do um do outro, né? Ah, eu
16:1516 minutos e 15 segundosvou mostrar mais uma classe aqui. São mais alguns exemplos, né? Ã, então temos mais dois Pokémons de luta e mais dois Pokémons de água.
16:2516 minutos e 25 segundosAhã. Vamos seguir aqui. Temos mais alguns exemplos.
16:3216 minutos e 32 segundosÃ, notem que provavelmente vocês devem ter ã características que vocês devem ter pensado que talvez separaria um
16:4116 minutos e 41 segundosPokémon de luta de um de água é que eles eram azuis, né? E aqui a gente começa a ver que já não é bem assim. Ahã.
16:5116 minutos e 51 segundosE bom, se a gente precisasse classificar esses daqui, por exemplo, que que vocês que que vocês me diriam?
16:5916 minutos e 59 segundosEh, aquele colega que tava interagindo comigo, o que que vocês O primeiro ele é psico e lutador, o
17:0817 minutos e 8 segundossegundo é lutador, o terceiro é de água e o terceiro e o quarto é de água.
17:1217 minutos e 12 segundosDe água. Tu já conhecia eles ou você não conheço.
17:1817 minutos e 18 segundosAh, então não. [risadas] Aí perdeu um pouco a graça, mas é exatamente isso, né? Os dois são
17:2617 minutos e 26 segundosprimeiros são de luta e os dois segundos são os dois últimos são de água, né? Ahã.
17:3317 minutos e 33 segundosÉ porque é porque no Pokémon a a característica é a é a forma física, é a
17:4017 minutos e 40 segundosforma do desenho do Pokémon e não a Perfeito. Exatamente. Ahã. Bom, gente, eu trouxe esse exemplo bastante lúdico
17:4817 minutos e 48 segundosaqui, só para mostrar para vocês que mais ou menos o processo que a gente de fato utiliza eh no aprendizado de
17:5717 minutos e 57 segundosmáquina. Claro que aqui eu tô usando um um exemplo super lúdico, né? Ã, mas a ideia é exatamente essa. A gente mostra
18:0518 minutos e 5 segundosalguns exemplos, né? Ã, com labels, que a gente chama, né? E aí eu já vou começar a introduzir as as a
18:1218 minutos e 12 segundosnomenclatura aqui. Ã, então a gente introduz esse essas imagens com os labels e a gente permite
18:1918 minutos e 19 segundosque a a gente delega para pro pra máquina, digamos, pro nosso algoritmo, pro nosso modelo, né? aprender as características que separam um do outro.
18:2918 minutos e 29 segundosComo vocês podem ver, eh, esse tipo de situação às vezes é se torna complicado, né? Se torna eh a gente acaba achando
18:3718 minutos e 37 segundosque uma característica de fato separa bem esses exemplos, mas na verdade quando a gente vai olhar eh vai expandir, né? A gente eh olha uma
18:4618 minutos e 46 segundospequena parcela de exemplos, depois quando a gente expande a gente vê que não é bem assim, que tem variações que não aquelas que a gente estava vendo,
18:5418 minutos e 54 segundosné? Ahã. Então eu trouxe esse exemplo também para mostrar para vocês que eh eh
19:0019 minutosuma das partes importantes além do nosso modelo, além do do da do modelo que a gente escolher ser um modelo
19:1019 minutos e 10 segundossuficientemente capaz de fazer essa separação, a gente também tem que ter uma uma variedade de dados que seja
19:1819 minutos e 18 segundosrepresentativo. Então eh no caso ali no início, vocês viram uma parcela de dados que eram muito parecidas, né? Ah, [roncando] e depois quando eh, e a gente
19:2719 minutos e 27 segundospode pensar que, eh, numa situação aonde aqui seja o, o, a vida real, né, o modelo aprendeu com aqueles dados e
19:3419 minutos e 34 segundosdepois chegou na vida real aqui e não era bem assim, né?
19:3819 minutos e 38 segundosEntão, bom, vamos seguir aqui o processo.
19:4219 minutos e 42 segundosEh, vamos eh deixa eu pegar o meu passador de de slide que eu tenho o
19:4919 minutos e 49 segundoscostume de ficar andando pelo para poder não gosto de ficar muito parado para
19:5719 minutos e 57 segundosfalar sobre isso. Vamos ver se tá passando. Beleza. Ah, bom, eh, vamos falar então de aprendizado
20:0520 minutos e 5 segundossupervisionado, tá? Eh, eu separei esses hã esses cada uma das das categorias desses
20:1420 minutos e 14 segundosdesses eh de abordagens, né, de forma linear. Então, a ideia é que eu vou
20:2220 minutos e 22 segundosconstruir com vocês uma linha e a gente vai construindo esse conhecimento ao longo dessa linha. Então, a gente vai construindo esse conhecimento aos
20:2920 minutos e 29 segundospoucos. Eh, quem já conhece, né, já sabe que tem supervisionado, não supervisionado por reforço, redes
20:3720 minutos e 37 segundosneurais, tudo isso vai ir aparecendo conforme a gente for andando, tá? Mas bom, ã, o aprendizado supervisionado é
20:4520 minutos e 45 segundosexatamente isso que eu acabei de mostrar para vocês. A gente mostra uma certa quantidade de dados pro modelo, né, pro
20:5320 minutos e 53 segundoscomputador, e ele vai aprender ã como correlacionar essas essas entradas com
21:0021 minutosos labels, né, com aqueles rótulos que a gente deu para ele. [roncando] Ah, e aí, bom, vamos entrar na primeira eh tarefa
21:0921 minutos e 9 segundosespecífica ali, que seria uma classificação.
21:1321 minutos e 13 segundosAh, classificação nada mais é isso que a gente fez. A gente, eh, vê um exemplo e a gente diz se é se é um ou outro ou
21:2221 minutos e 22 segundosmais classes, né? A gente basicamente ah vai associar uma uma classe, uma categoria para cada um dos exemplos, né?
21:3121 minutos e 31 segundosEu trouxe aqui um exemplo eh de por acaso previsão de chuva, tá? Eh, mas
21:3921 minutos e 39 segundosnão é relacionado com [risadas] com o que vocês estão provavelmente vão trabalhar. [roncando] Eh, aqui é um
21:4721 minutos e 47 segundosexemplo bem bobo, bem simples, tá? Ah, não reflete exatamente a realidade, mas só pra gente eh brincar um pouquinho, né?
21:5721 minutos e 57 segundosVamos pensar que a gente tem dados eh históricos de previsão de chuva.
22:0322 minutos e 3 segundosAh, e aí eu peguei dois dados específicos aqui, que é de umidade e de pressão, tá? Então, ã, eu tenho aqui
22:1222 minutos e 12 segundoscada um dos dias, né, ah, com a sua umidade, a sua pressão, a a pressão
22:1922 minutos e 19 segundosassociada à aquele aquele dia, ã, e se vai chover ou se não vai chover.
22:2622 minutos e 26 segundosVamos ã pensar o seguinte, tá?
22:3022 minutos e 30 segundosVamos pensar eh matematicamente um pouco. Vamos, eu eu queria correlacionar um pouco com a
22:3722 minutos e 37 segundosmatemática que às vezes eh a gente quem quem às vezes a gente programa, né?
22:4422 minutos e 44 segundostinha muito isso na graduação. Eu tinha um pouco de dificuldade de conseguir correlacionar as coisas que eu tava fazendo, os termos, os conceitos de
22:5222 minutos e 52 segundosprogramação com a matemática, apesar das duas estarem intimamente ligadas, né? Mas bom, vamos pensar o seguinte.
23:0023 minutosO que eu quero é uma função, tá? Que dado umaidade e dado uma pressão, ela vai me retornar um label.
23:1223 minutos e 12 segundosAh, então vamos usar um exemplo aqui, né?
23:1723 minutos e 17 segundosAh, então eu dei aqui uma entrada de umidade de 93 e uma pressão de 999.7.
23:2523 minutos e 25 segundosEssa essa função que a gente não sabe o que é. Vamos pensar essa função como a função que modela aqueles aqueles dados
23:3323 minutos e 33 segundosali que a gente não sabe. Pensem que cada problema eh cada situação que a gente encontra, a
23:4023 minutos e 40 segundosgente pode ter uma função que gera que gera aqueles dados. A gente talvez nunca vai saber qual é essa função. Ou talvez
23:4823 minutos e 48 segundosnão tenha uma função que descreva exatamente os fenô os fenômenos que acontecem.
23:5523 minutos e 55 segundosH, mas de alguma forma a gente tem uma função que mais ou menos dita aqueles dados que a gente tá vendo, tá? Então
24:0224 minutos e 2 segundosvamos pensar essa função como sendo essa f eh umidade pressão, né? Ã, mais um exemplo aqui, só para vocês verem.
24:1124 minutos e 11 segundosEntão, dei mais um exemplo e me disse sem chuva. E mais um exemplo sem chuva.
24:1824 minutos e 18 segundosBom, notem que a nossa tarefa com machine learning é gerar uma função, tá, que se
24:2824 minutos e 28 segundosaproxime da função que gera aqueles dados, que é essa função que a gente não sabe o que é. Pode ser uma função de
24:3624 minutos e 36 segundosprimeiro grau com um monte de variáveis, pode ser uma função de quinto, sexto grau de inúmeras dimensões. A gente não
24:4324 minutos e 43 segundossabe o que que é aquilo. A gente sabe que a gente tem aqueles dados que a gente observou e a gente, a partir
24:5024 minutos e 50 segundosdaqueles dados, a gente quer gerar uma função que eh gere aquele aquele label a partir daqueles dados.
24:5924 minutos e 59 segundosAqui eu vou chamar de eh h, uma função hipótese, tá? Então aí é a função hipótese que a gente vai tentar
25:0725 minutos e 7 segundosaproximar aquela função original que gera os dados. Então vamos olhar um exemplo aqui, tá?
25:1425 minutos e 14 segundosEu vou pilotar esses dados eh de chuva e de não chuva, tá?
25:2125 minutos e 21 segundosVocês conseguem perceber alguma coisa? Eh olhando esses só pelas cores aqui?
25:2825 minutos e 28 segundosH, provavelmente vocês devem ter visto que de alguma forma a gente consegue mais ou
25:3625 minutos e 36 segundosmenos separar o que é chuva e o que não é chuva, ã, traçando mais ou menos uma linha ali, um separador, né?
25:4525 minutos e 45 segundosAhã.
25:4625 minutos e 46 segundosMas vamos estressar um pouquinho esse ponto aqui. Vamos, digamos que eu eh tem esses dados aqui que a gente já sabe
25:5425 minutos e 54 segundosqual é o label deles. Então, chuva e não chuva, sem chuva, né? Ahã. Como é que vocês classificariam esse ponto novo que
26:0326 minutos e 3 segundosapareceu aqui? Que por acaso eu botei uma cor muito parecida com azul, mas esse ponto, deixa eu ver se o meu mouse
26:0926 minutos e 9 segundosaparece aqui, não aparece. Ahã. Esse ponto aqui eu vou ficar [suspirando] eh, deixar ele piscando aqui, né? Esse ponto
26:1926 minutos e 19 segundosaqui novo que apareceu, a gente não sabe o que que é esse ponto. A gente não sabe se aquilo ali vai ser uma previsão de chuva ou se é uma previsão de sem chuva.
26:2826 minutos e 28 segundosQual seria o palpite que vocês dariam para esse novo ponto aqui?
26:3426 minutos e 34 segundosProvavelmente vocês falariam que é um ponto de chuva, né?
26:4126 minutos e 41 segundosE aí vocês, por que, por que que vocês eh considerariam ele como chuva? Porque vocês viram que todos aqueles pontos que estão próximos ali ã são de chuva.
26:5126 minutos e 51 segundosEntão, provavelmente a melhor aposta que eu posso fazer seria que aquele ponto também seja um ponto de chuva, dado aquelas aquelas configurações, né? Ahã.
27:0227 minutos e 2 segundosÉ só uma coisa, me perdoem se eu tiver eh não deixando vocês falarem. Eu queria a interação de vocês, mas eh como a
27:0927 minutos e 9 segundosgente já tá com tempo mais avançado, eu vou ter que ir um pouquinho mais rápido.
27:1527 minutos e 15 segundosÃ, mas bom, então esse processo de ã pegar o os pontos mais próximos daquele
27:2327 minutos e 23 segundosnovo ponto que eu coloquei ali e atribuir a classe que é aquela classe que é próxima daqueles pontos, a gente chama eh de vizinho mais próximo, né?
27:3627 minutos e 36 segundosEntão, é um tipo de algoritmo que a gente vai pegar o vizinho mais próximo e vai atribuir a aquela classe à aquele
27:4327 minutos e 43 segundosvizinho. Então, é um é um exemplo muito simples.
27:4827 minutos e 48 segundosSe o nosso caso é que nem esse caso aqui, que ele caiu numa região próxima ali,
27:5527 minutos e 55 segundoseh, com dados muito parecidos, é fácil, né? Parece trivial, parece simples a gente fazer essa atribuição, né? Eu
28:0328 minutos e 3 segundostrouxe mais um exemplo aqui lá da classe de sem chuva e provavelmente vocês também vão eh fazer a mesma a mesma
28:1328 minutos e 13 segundosregra, né, que vocês fizeram eh inconscientemente e dizer que aquilo ali é sem chuva, né, possivelmente.
28:2128 minutos e 21 segundosMas agora vamos estressar um pouquinho isso, né? E se eu desse esse ponto aqui, que eu vou deixar ele piscando,
28:2828 minutos e 28 segundosesse ponto novo aqui, vocês classificariam ele como chuva ou como sem chuva?
28:3528 minutos e 35 segundosNotem que já começa a ficar um pouquinho mais complicado, né? Porque a gente tem um ponto ali que tá eh um pouco eh como
28:4328 minutos e 43 segundosé que eu vou dizer? Um pouco fora do padrão, né?
28:4828 minutos e 48 segundosE notem que isso vai ser uma constante no nosso trabalho. Aqui a gente tá, eu tô mostrando um exemplo aqui que é um
28:5528 minutos e 55 segundosexemplo muito bonitinho, mas na vida real a gente nunca vai ter um exemplos tão limpos quanto esses aqui, né? Sempre
29:0329 minutos e 3 segundosvai ter algum ruído. Eh, ah, quem já passou por algum processo de trabalhar com gente eh anotando dados, né? então
29:1129 minutos e 11 segundosdizendo se aquilo ali é chuva, aquilo ali não é chuva, vai saber que nesse processo a gente tem problema, por exemplo, de anotação
29:2129 minutos e 21 segundosincorreta. Então tem diversos problemas e bom, a o mundo real é o mundo real, né, gente? A gente não tem as coisas não
29:2929 minutos e 29 segundosnecessariamente seguem uma regra, né? A gente que quis inventar de de tentar achar uma regra para ã pra bagunça do mundo, né?
29:4129 minutos e 41 segundosMas bom, vamos voltar esse exemplo aqui.
29:4329 minutos e 43 segundosEntão, esse exemplo aqui específico eh se torna complicado. Alguns provavelmente podem ter dito: "Tá, esse
29:5129 minutos e 51 segundoscara aí é chuva". Outros podem ter dito que não. Ele tá muito próximo daquele cara ali que tá dizendo que não é chuva,
29:5829 minutos e 58 segundosentão talvez não seja chuva. Ã, pela regra do vizinho mais próximo, a gente vai considerar ele como sem chuva, tá?
30:0730 minutos e 7 segundosHã, notem que aqui eu não tô, eu não quero que vocês de fato saibam isso daqui, né? Só mostrando como seria essa
30:1430 minutos e 14 segundosaplicação pelo algoritmo, que é esse primeiro que eu apresentei para vocês, né?
30:2130 minutos e 21 segundosÃ, mas perfeito. Ah, e aí vocês podem olhar para mim e falar: "Tá, Carlos, mas
30:2730 minutos e 27 segundoseh apesar daquele ponto ali específico C sem chuva, tem vários outros pontos na volta que não são chuva.
30:3630 minutos e 36 segundosH, e daí a gente entra no próximo algoritmo, né, que é os vizinhos mais próximos. Então, ao invés de eu considerar aquele vizinho único, eu vou
30:4530 minutos e 45 segundosconsiderar K vizinhos e sendo K um número que eu vou escolher, tá? Então, digamos que aqui, ao invés de eu
30:5330 minutos e 53 segundosconsiderar um vizinho, eu considere três, por exemplo, ou até dois, né? Mas três eh fica melhor porque daí tem o
31:0131 minutos e 1 segundodesempate, né? Então seria ã o vizinho da da esquerda ali mais para baixo, o de
31:0831 minutos e 8 segundoscima e o da direita, né? E aí a gente olharia que a grande a maioria deles é chuva, então a gente atribui chuva para
31:1631 minutos e 16 segundosesse cara. Então esse é o algoritmo de vizinhos mais próximos, né?
31:2231 minutos e 22 segundosAhã. Perfeito. Esses são alguns algoritmos clássicos que a gente eh tem dentro da área de machine learning que são mais básicos, né?
31:3331 minutos e 33 segundosÃ, mas aí eu volto aquela questão que a gente conversou no início, né? E aqui eu ajustei um pouquinho melhor essa nossa configuração.
31:4231 minutos e 42 segundosSe vocês prestarem atenção, a gente consegue traçar uma linha que separa bem esses dois lados, né?
31:4931 minutos e 49 segundosEntão, e se a gente traça essa linha para separar esses dois, essas duas classes, né?
31:5731 minutos e 57 segundosLegal, parece funcionar. Então, tudo que tiver acima dessa linha vai ser sem chuva e tudo que tiver abaixo dessa
32:0432 minutos e 4 segundoslinha vai ser sem chuva. E notem que aqui a gente já começa a introduzir um pouco de matemática, né? Então, a gente
32:1132 minutos e 11 segundosbasicamente fez uma reta, né? Então, a gente vai usar a a equação da reta pra gente eh começar a trabalhar com isso,
32:1832 minutos e 18 segundosné? Então, notem que muitos eh entendem machine learning como
32:2832 minutos e 28 segundosuma coisa inacreditável, uma coisa que vai dominar o mundo, que vai eh dominar a humanidade, né?
32:3632 minutos e 36 segundosMas no fundo, se a gente for pensar por baixo dos panos, quase tudo é matemática, tudo é álgebra linear, tudo é estatística, né, de alguma forma.
32:4432 minutos e 44 segundosEntão, ã, mas bom, vamos seguir aqui o processo, né?
32:5032 minutos e 50 segundosDigamos agora que eu tenha esses essa situação que a gente tava lidando ali, né? Ã, tendo essa linha já fica bem mais
32:5932 minutos e 59 segundosfácil para mim ã classificar novos pontos, né? Eu não preciso estar calculando cada um dos vizinhos, é só eu ver se ele tá para
33:0833 minutos e 8 segundoscima ou para baixo da linha. Notem que sempre vai ter uma margem de erro.
33:1233 minutos e 12 segundosSempre vai ter erro. Não tem eh a não ser que seja uma coisa muito controlada e vai ser muito difícil isso acontecer,
33:2133 minutos e 21 segundosmas sempre vai ter um erro atrelado ao nosso modelo. Então esse modelo que eu fiz aqui, ele tem um erro, né? Ele
33:2833 minutos e 28 segundoserrou, por exemplo, quatro pontos ali, né? quatro pontos que ele não que que digamos ele tá fora, né, digamos do do
33:3733 minutos e 37 segundosque seria esse essa essa separação completa dos dois dos dois lados, né?
33:4433 minutos e 44 segundosMas bom, vamos botar isso rapidamente eh numa função matemática pra gente ver como é que isso funciona. Então, vamos
33:5133 minutos e 51 segundospensar que a umidade é o nosso eh x1, a nossa pressão é o x2. Então, são
33:5933 minutos e 59 segundosargumentos, né? E aí a gente pode ter Xnos.
34:0534 minutos e 5 segundosÃ, aqui por enquanto só temos dois. A gente vai colocar na nossa eh hipótese, na nossa função de hipótese, né, para
34:1334 minutos e 13 segundostentar aproximar aquilo ali que a gente tá vendo. Então, uma forma que a gente poderia fazer é, como eu disse, pegar a
34:2134 minutos e 21 segundosequação da reta e simplesmente eh atrelar esse eh colocar, somar tudo, né?
34:2834 minutos e 28 segundosAhã. E aí a gente teria eh x1 atrelado a um peso mais x2 atrelado
34:3734 minutos e 37 segundosao peso. Então a pressão atrelada a um peso mais um da um peso extra ali que a gente se a gente precisar, por exemplo,
34:4634 minutos e 46 segundosandar com essa reta, né? Ã ali entre o o no gráfico, né? Ahã.
34:5434 minutos e 54 segundosEsse W0 aqui a gente vai chamar de baias, mas a gente já vai falar deles melhor mais para frente, né? Então eu
35:0135 minutos e 1 segundocoloquei basicamente uma função aqui de primeiro grau que soma tudo e tem pesos atrelados a cada uma dessas variáveis,
35:1035 minutos e 10 segundosné? Então talvez vocês possam pensar que a umidade pode ser mais importante que a pressão ou vice-versa, né? Então, a
35:1935 minutos e 19 segundosgente tem que ter algum peso, algum número para indicar que aquilo ali é mais importante que o que o outro nessa
35:2535 minutos e 25 segundosequação, né? E aí eu vou fazer uma regra bem básica aqui de ahã se essa equação
35:3435 minutos e 34 segundostoda der maior que maior ou igual a zero é chuva. Se não, ela vai ser sem chuva.
35:4335 minutos e 43 segundosVamos melhorar isso daqui pro nosso para algoritmos, né? Então é um, ou seja, chuva, se aquilo for maior ou igual a
35:5135 minutos e 51 segundoszero, ou zero, caso contrário, né? Então a gente vai pensar algoritmicamente dessa forma, né?
35:5935 minutos e 59 segundosAté porque ã, e notem que aqui eu tô fazendo uma uma regra muito básica para um um caso que são só duas classes, né?
36:1036 minutos e 10 segundosPoderia ter mais classes, poderia. E aí a gente ia ter que pensar numa regra bem mais complexa, né?
36:1736 minutos e 17 segundosBom, aqui vamos eh só dar algumas nomenclaturas, né? Então, a gente tem um vetor de pesos, né? Um array, uma lista,
36:2536 minutos e 25 segundoscomo vocês quiserem chamar. Então, temos o peso zero, o peso um e o peso dois, tá? E aí a gente tem um um vetor de
36:3436 minutos e 34 segundosentrada que é ã x1 e x2 e mais um um valor ali, um valor dame, né, pra gente
36:4336 minutos e 43 segundossimplesmente fazer a a assimilação ali com o w0, né? E aí notem como isso é
36:5036 minutos e 50 segundosimportante, porque agora a gente pode fazer o produto o o e é o produto dessas duas desses dois
36:5736 minutos e 57 segundosvetores, né? O dot. Ahã. E aí a gente chega naquela equação. Então vamos seguir.
37:0537 minutos e 5 segundosÃ, bom, aqui tem ah um outro conceito que se chama
37:1337 minutos e 13 segundosperceptum, tá? A gente já vai falar um pouquinho melhor o que que é o percepton, mas
37:1937 minutos e 19 segundosvamos pensar num percepton como essa função aqui de forma meio genérica primeiro pra gente só ir explorando com
37:2837 minutos e 28 segundoscom o andar do do do processo aí. Ah, e desenvolvendo essa ideia, tá?
37:3537 minutos e 35 segundosAhã. Eu trouxe aqui uma função aqui que parece meio meio diabólica aqui, mas eh
37:4237 minutos e 42 segundossó para explicar, eu vou vou mudar um pouquinho aqui só pra gente conseguir ver e não assustar tanto, tá? Ã, mas
37:5037 minutos e 50 segundosbasicamente aqui tá uma regra da gente como é que a gente atualiza esses pesos de um perceptor, tá? Então o wi, ou
37:5937 minutos e 59 segundosseja, o peso i, né? Então pode ser o o um, pode ser o zero, pode ser o dois ou
38:0538 minutos e 5 segundoso o se for mais, né? Eh, conforme for, ã, o peso I, eh, a gente vai atualizar
38:1438 minutos e 14 segundosele sendo ele mais um valor alfa ali, tá? Que eu já vou falar o que que seria
38:2138 minutos e 21 segundosesse valor alfa. E aí a gente vai fazer essa conta ali de valor observado menos a estimativa
38:2838 minutos e 28 segundosvezes o o valor eh o valor que a gente tem. Então, já vou dar um exemplo melhor
38:3738 minutos e 37 segundosali depois vai ficar mais claro, né? Mas basicamente o que a gente tá fazendo aqui é a gente pega ã um ponto,
38:4538 minutos e 45 segundosvê eh se o que a gente estimou e vê o valor que ele era para ser. Faz essa
38:5238 minutos e 52 segundossubtração, multiplica por esse esse valor A ali, né? E depois soma com os pesos pra gente ir atualizando. Então,
39:0039 minutosse eh pode ser que a gente vá diminuir esses pesos ou pode ser que a gente aumente esse peso, né? dependendo do do
39:0739 minutos e 7 segundosnosso problema, né? Se a gente estimou muito mais alto que o valor que deveria ser, a gente vai baixar esse peso ou vice-versa, certo?
39:1739 minutos e 17 segundosEsse a a gente chama basicamente de learning rate. Então é simplesmente um valor que a gente vai indicar pro nosso
39:2439 minutos e 24 segundosmodelo ah para mostrar para para indicar para ele qual o passo que a gente vai dar, se a gente vai dar um
39:3239 minutos e 32 segundospasso muito grande, ou seja, se qualquer variaçãozinha que eu der, ele vai multiplicar muito esse vai aumentar
39:4039 minutos e 40 segundosmuito, né? Vai mexer muito nesse peso ou se ele vai mexer pouco, né?
39:4639 minutos e 46 segundosEntão aqui, ã, só para mostrar aqui para vocês, a gente fez uma uma função degrau, né, que a gente chama. Ã, então
39:5539 minutos e 55 segundostem só duas situações, né? Ou é zero a saída ou é um, que é a indicação de chuva, né? Vamos voltar rapidamente pro
40:0340 minutos e 3 segundosnosso exemplo e olhar que a gente tem a separação aqui dos dos eh novamente aquela reta, né?
40:1240 minutos e 12 segundosE aí vão pegar esses dois caras aqui que eu vou mostrar de novo, eh, piscando.
40:1940 minutos e 19 segundosÃ, vamos olhar como é que ele, meu slide ficou errado aqui.
40:2740 minutos e 27 segundosEh, tá, vamos agora eu explico para vocês. Ã, pensem que a gente quer classificar esses dois caras aqui, né?
40:3740 minutos e 37 segundosSó que talvez a gente queira uma outra abordagem.
40:4340 minutos e 43 segundosÀs vezes a gente não quer só saber se ele é chuva ou não, mas que é o o limear rígido, né? Às vezes a gente quer só
40:5140 minutos e 51 segundossaber se ele é qual é a probabilidade daquilo ser chuva. Então aqui, deixa eu ver se tem uma outra reta aqui para
40:5840 minutos e 58 segundosmostrar. Eu acho que não, tá? Eh, aqui, na verdade, seria uma uma eh uma função
41:0841 minutos e 8 segundoseh não uma reta, né? Não um um degrau, mas uma função suave, aonde a gente consegue ter uma granularidade entre
41:1641 minutos e 16 segundoszero e um. Depois vou ver se eu se eu ajusto para vocês verem melhor, mas vamos seguindo, né? A ideia basicamente
41:2341 minutos e 23 segundosaqui que em vez da gente ter uma coisa eh binária, a gente tem uma certa eh
41:3041 minutos e 30 segundosuma certa tranquilidade, né? Uma uma um relaxamento dessa regra que a gente pode ter probabilidades. Então, ao invés de
41:3841 minutos e 38 segundosser um ou zero, a probabilidade, né, de ser chuva vai ser de 08 ou 04, né?
41:4641 minutos e 46 segundosEntão, a a gente relaxa um pouco esse esse processo. Hã, deixa eu ver o meu tempo aqui, tá?
41:5541 minutos e 55 segundosTô falando bastante, né, gente? Eh, vou apresentar rapidamente mais uma ideia aqui, que é a máquina de vetores, né?
42:0542 minutos e 5 segundosBom, vamos olhar esse exemplo aqui, tá?
42:0842 minutos e 8 segundosEh, digamos que a gente faça essa reta aqui e separe desse jeito, tá?
42:1542 minutos e 15 segundosTalvez vocês achem estranho, né? Porque bem, poderia ter uma outra abordagem pra gente fazer aqui, né? Quem sabe a gente
42:2442 minutos e 24 segundoscoloca uma reta diagonal para separar esses caras, né? Mas em que lado que eu coloco? Eu coloco muito mais próximo
42:3242 minutos e 32 segundoslados sem chuva ou eu coloco mais pro lado de cá, né, dos dos com chuva, né?
42:4042 minutos e 40 segundosH, então aqui é uma decisão aonde a gente tem um espaço que a gente não tem como saber, a gente não tem dados
42:4742 minutos e 47 segundossuficientes para saber qual é o limite entre os dois, né? Então a ideia, o que a gente gostaria é fazer uma reta que
42:5642 minutos e 56 segundossepare no máximo, né? E a a máxima distância entre os dois que a gente consiga separar e deixar uma margem ali
43:0443 minutos e 4 segundospara fazer isso, né? Ahã. Então, basicamente, ah, de forma bem simplória, tá? Eu vou tô passando bem rápido aqui.
43:1243 minutos e 12 segundosEh, essa é a ideia do SVM, tá? Então, a gente vai tentar maximizar essa margem
43:1943 minutos e 19 segundosentre os pontos para conseguir eh encontrar uma uma função que se assemelhe melhor aqueles aqueles pontos, né?
43:3043 minutos e 30 segundosMas bom, o que que vocês me diriam se a gente tivesse um caso assim?
43:3543 minutos e 35 segundosComo é que a gente separaria esse cara aqui? Não teria muito como separar, né?
43:4243 minutos e 42 segundosEsse cara aqui se torna bem mais, não sei se alguém tem dúvida, só
43:4743 minutos e 47 segundos[risadas]
43:4843 minutos e 48 segundosesboçou a ã, mas bom, esse cara aqui se torna bem difícil, né? A gente já não consegue
43:5743 minutos e 57 segundosmais traçar reta, quem sabe? Aí vocês podem argumentar comigo, tá? Mas se a gente tentar fazer
44:0344 minutos e 3 segundosuma, sei lá, uma função de segundo grau, um uma
44:1044 minutos e 10 segundose notem que é difícil, né, a gente pensar uma função que consiga separar isso daqui, né? Idealmente a gente queria alguma coisa que fosse assim, né?
44:2044 minutos e 20 segundosEntão, conseguir fazer essa separação de forma mais eh, opa, mais
44:2744 minutos e 27 segundoseh localizada, né? E basicamente esse é um dos problemas que o SVM consegue
44:3444 minutos e 34 segundosresolver, tá? Como eu falei, não vou entrar muito em detalhes porque a gente tá com tempo curto, mas é só para que vocês entendam o problema, entendam de
44:4444 minutos e 44 segundosforma intuitiva quais os algoritmos que a gente pode utilizar para chegar naquele problema e como é que a gente pensa essa conexão matemática com o a
44:5444 minutos e 54 segundosquestão, né? Hã, bom, só para dar um um breve resumo, né? O SVM ele vai lidar
45:0145 minutos e 1 segundotambém com eh mais dimensões, então ele vai conseguir eh lidar com coisas em
45:0845 minutos e 8 segundosmais dimensões. Aqui, no caso, ele eh tem um exemplo com papel, mas é como se esses azuis tivessem numa dimensão mais
45:1645 minutos e 16 segundosembaixo e os e os sem chuva, né, esses rosinhas, estariam numa dimensão mais alta. Então, a gente consegue separar
45:2545 minutos e 25 segundosdessa forma. A gente mudaria a perspectiva do jeito que a gente tá vendo. A gente tá vendo 2D, né? Assim, a
45:3145 minutos e 31 segundosgente teria que mudar dessa forma, mais ou menos assim, tá? Ah, mas bom, digamos que o problema, na verdade, que a gente
45:4045 minutos e 40 segundosquer não é só classificar, tá? Digamos que agora a gente quer prever um valor e esse valor sendo um valor contínuo, daí
45:4945 minutos e 49 segundoso nosso problema começa a mudar de de forma. E aí a gente chama um problema de regressão. Então, a gente tava falando de problema de classificação, agora a
45:5845 minutos e 58 segundosgente vai falar de um problema de regressão, né?
46:0246 minutos e 2 segundosAh, então o problema de regressão é exatamente isso. Ao invés de eu dizer se é eh uma classe ou outra, eu quero dizer
46:1046 minutos e 10 segundosqual é o valor daquele da dado aquele ponto, qual é o valor que que eu que eu chego na na eh levando em conta aquele
46:1846 minutos e 18 segundosponto, né? Eu já vou mostrar um exemplo que fica um pouco melhor, né?
46:2446 minutos e 24 segundosAh, então, digamos que ã eu tenho uma empresa e eu quero quantificar o quanto
46:3346 minutos e 33 segundosde lucro que eu vou ter dado o gasto em publicidade.
46:3846 minutos e 38 segundosÉ um, é uma forma muito ruim da gente conseguir quantificar isso, né? Ahã.
46:4446 minutos e 44 segundosDaqui a pouco a gente poderia mudar também um exemplo mais atual seria ã o quanto eu tô o meus funcionários estão
46:5246 minutos e 52 segundosusando IA pro meu lucro ou o meu sucesso da minha empresa, né? Ã, só um adendo
46:5946 minutos e 59 segundosaqui. Eh, hoje, infelizmente, ã, as empresas estão cada vez mais eh, com
47:0747 minutos e 7 segundosesse foco que, a meu ver, é incorreto, né? que é quanto mais os meus funcionários estão usando IA, melhor,
47:1547 minutos e 15 segundosné? Então, eh eh notem que não necessariamente isso é real, é verdade, né? Eu posso eh usar extensivamente IA e
47:2447 minutos e 24 segundosnão chegar num trabalho bom e ao mesmo tempo posso ter um funcionário que é muito bom, não quer usar IA, que que é mais meticuloso, que gosta de olhar
47:3347 minutos e 33 segundoscódigo, que gosta de de acompanhar o processo, né, e ser um bom funcionário, né? Então, infelizmente, a gente tá num
47:4147 minutos e 41 segundosmomento em que isso é uma métrica das empresas, né? Mas bom, vamos voltar ao nosso exemplo, né? Eh, digamos que eu
47:5147 minutos e 51 segundostenho uma função que dado o valor que eu gasto com publicidade, eu tenho o meu lucro. Então, eu trouxe alguns exemplos
47:5847 minutos e 58 segundosaqui, né? 1200 eu vou ter lucro de 5800, 2800, 13.400.
48:0648 minutos e 6 segundosE ali o último exemplo, né?
48:0948 minutos e 9 segundosAhã. O que a gente quer fazer aqui então é chegar numa função hipótese, né, que a
48:1648 minutos e 16 segundosgente chama de hipótese, que se aproxima daquela função original ali que tá originando os dados. Ã, vocês já devem
48:2448 minutos e 24 segundoster olhado esses dados, quem tá mais a a a mais concentrado e já deve ter percebido certo certo padrão, né?
48:3448 minutos e 34 segundosEh, a gente aumenta a publicidade, o o nosso ganho aumenta, né? Mas bom, vamos
48:4148 minutos e 41 segundosplotar aqui, né, a as nossas o nosso gráfico. Ã, aqui eu botei vendas, não botei lucro, mas vamos pensar em vendas.
48:5148 minutos e 51 segundosEntão, como que a gente consegue, dado um novo ponto nesse meio aqui, como é que a gente consegue prever qual vai ser o
49:0049 minutosvalor? Então, notem que aqui diferente, vou voltar aqui rapidamente para nosso exemplo. Notem que diferente do do
49:0849 minutos e 8 segundosexemplo anterior, agora, ao invés de eu dizer uma classe única, eu quero que
49:1549 minutos e 15 segundosdado um valor eu retorne um novo valor, uma predição, uma previsão, né? Ah, daquele valor. Como é que a gente
49:2449 minutos e 24 segundospoderia pensar aqui? Então, eh, dada essa essa essa configuração,
49:3149 minutos e 31 segundosné, dos nossos dados, bom, poderíamos pensar novamente traçar uma reta. Será
49:3949 minutos e 39 segundosque fica legal? Será que ela funciona bem, né? quais as diferentes eh rotações
49:4549 minutos e 45 segundose e ã que a gente pode fazer com essa reta para que a gente consiga mais ou menos
49:5349 minutos e 53 segundoseh organizar para esses para esses dados, né? Então, por exemplo, eh se eu pegasse qualquer dado de publicidade ali no
50:0150 minutos e 1 segundomeio, por exemplo, pense no meio da da da reta, né?
50:0550 minutos e 5 segundosAhã. E depois eu fizesse o correspondente dele usando a reta, eu chegaria num valor. Pode ser que ele esteja próximo desses valores que eu
50:1450 minutos e 14 segundostenho como referência, talvez estejam muito longe. [roncando] Notem que aqui é muito difícil eu conseguir fazer isso
50:2250 minutos e 22 segundoscom essa reta, né? Ah, ela vai ter um erro associado muito grande aqui, porque os dados estão muito espalhados, né?
50:3150 minutos e 31 segundosAhã. Mas bom, vamos eh explorar alguns conceitos importantes, tá? Então, o
50:3850 minutos e 38 segundosprimeiro conceito que a gente vai falar é a função de perda, né? Ã, a loss function que no inglês, eh,
50:4750 minutos e 47 segundosessa função basicamente vai quantificar eh o quanto a gente errou na nossa hipótese, né? O quanto o nosso modelo errou, né?
50:5750 minutos e 57 segundosEntão, eh, aqui eu trouxe mais ou menos ali, eh, a função loss, né? Ah,
51:0551 minutos e 5 segundosrecebendo o que a gente eh predizeu e o observado. Então, eh, zero se o observado for igual ao previsto e um,
51:1451 minutos e 14 segundoscaso contrário. Então, a gente tá tentando quantificar o quanto de erro eu fiz nessa minha previsão. Vamos voltar aqui no nosso exemplo, tá?
51:2451 minutos e 24 segundosH, naquele exemplo inicial lá, né? Ã, digamos que eu traço essa reta aí. E aí, bom, aqui eu tô mostrando o cálculo, né?
51:3651 minutos e 36 segundosEntão, aqueles dois caras lá de cima, eh, eu tô quantificando como um. Errei ali. E os dois de baixo aqui que estão
51:4351 minutos e 43 segundosfora também errei mais ahã dois, né? Então são quatro de erro e
51:5151 minutos e 51 segundosnão sei quantos eh eh quantas entradas aqui de acerto, né? Ahã.
51:5851 minutos e 58 segundosEssa função a gente pode fazer ela o quão complexo a gente precisar que ela seja, tá? Aqui eu fiz uma função bem
52:0652 minutos e 6 segundossimples, né? Bem bem básica, que é só olhar e dizer se sim ou não, né? Acertou ou errou. Mas talvez a gente precise de
52:1552 minutos e 15 segundosalguma coisa um pouco mais eh complexa, né? Então temos a L1 aqui, que é
52:2252 minutos e 22 segundosbasicamente o módulo, né? Eh, e aí eu vou pegar a previsão, eh, aliás, o observado menos a previsão,
52:3052 minutos e 30 segundostá? Então, eu vou ter um valor ali um pouco mais contínuo.
52:3452 minutos e 34 segundosEntão, voltando aquele nosso exemplo da publicidade, se eu pegar e quantificar, então vê o quanto eu errei ali, né?
52:4452 minutos e 44 segundosvai ser basicamente isso. Então, a gente pode pensar que é simplesmente a distância entre o ponto, né, e a e a
52:5252 minutos e 52 segundosminha previsão ali, no caso, a nossa reta, né?
52:5752 minutos e 57 segundosUma outra forma que a gente pode pensar é o que a gente chama de L2, né, e que é o erro quadrado médio, né? Então, a
53:0653 minutos e 6 segundosgente utiliza o observado menos o previsto ao quadrado. Basicamente isso, tá? Eh,
53:1553 minutos e 15 segundostem um outro conceito importante aqui que é o sobreajuste, o overfitting, que você já deve ter ouvido falar.
53:2253 minutos e 22 segundosNotem que vamos pegar esse, acho que eu deixei um exemplo aqui, tá?
53:2853 minutos e 28 segundosVamos explorar esse conceito de forma mais eh eh intuitiva.
53:3553 minutos e 35 segundosÃ, uma coisa importante que vocês vão ver é que ahã dependendo da onde vocês forem
53:4453 minutos e 44 segundostrabalhar, dependendo da onde do problema que vocês forem atacar, a gente tem uma quantidade de dados disponíveis.
53:5253 minutos e 52 segundosNem sempre a gente tem todas as possibilidades possíveis e e classificadas ali. Tem um exemplo muito
54:0054 minutosinteressante, eh, e um pouco triste, né? Mas bom, ã, quando surgiu o Face ID da Apple, né,
54:0954 minutos e 9 segundosaquele processo do iPhone conseguir eh eles con conseguir reconhecer as imag a a pessoa que tá acessando o celular, né?
54:2054 minutos e 20 segundosQuando a Apple época introduziu aquele conceito, funcionou muito bem lá nos Estados Unidos, todo mundo usou e tal, até
54:2854 minutos e 28 segundoscomeçar a ter os problemas. Então, o que que acontece? Ahã.
54:3454 minutos e 34 segundosEles treinaram, então eles foram lá, fotografaram várias pessoas, viram várias eh várias profundidades,
54:4354 minutos e 43 segundosdiferentes ã tipos de pessoas, né? Ã, e pegar aqueles dados, então, digamos,
54:5254 minutos e 52 segundosplotar esses dados da da forma que tá aqui, por exemplo, né? Tem uma quantidade de dados que eles eh capturaram
54:5954 minutos e 59 segundosquando chegou no mundo real. O que que aconteceu?
55:0355 minutos e 3 segundosEles pegaram muitas pessoas que eram brancas e, infelizmente, não pegaram uma quantidade eh considerável de pessoas
55:1155 minutos e 11 segundosque eram negras. E aí o que aconteceu foi que o algoritmo não conseguia capturar aquela pele negra, ah,
55:2055 minutos e 20 segundossimplesmente porque não foi apresentado o suficiente para ele. Então, o que que aconteceu?
55:2755 minutos e 27 segundoso algoritmo aprendeu, né, a reidentificar só aquele tipo específico de de pessoa, digamos, de de cor de pele, sei lá.
55:3655 minutos e 36 segundos[roncando]
55:3655 minutos e 36 segundosAhã. E aí na na época deu uma baita polêmica, depois eles eh eh expandiram,
55:4355 minutos e 43 segundosinclusive foram lá na lá na África, numa aldeia super eh separada lá, isolada e tiraram foto de
55:5255 minutos e 52 segundospessoas muito diferentes. E aí o a a a tecnologia começou a funcionar melhor, né?
55:5955 minutos e 59 segundosEntão isso é um exemplo de como ã é importante a questão de dados, é importante a variabilidade desses dados,
56:0656 minutos e 6 segundosné? Então vamos olhar para esse caso aqui, tá? Digamos que eu quero fazer uma função que separe esses dois casos.
56:1656 minutos e 16 segundosDigamos que eu trace uma uma reta aqui, né? Meu modelo, a minha hipótese e essa reta aqui. Aí vocês vão olhar e tá, mas
56:2456 minutos e 24 segundostem aquele pontinho ali que tá tá fora, né? Ahã. E se eu fizesse, caísse na tentação de fazer isso daqui?
56:3456 minutos e 34 segundosA gente às vezes tem muito essa tentação. Eh, aqui a gente tá vendo de uma maneira muito eh lúdica, né? Porque
56:4356 minutos e 43 segundosa gente tá vendo os pontinhos coloridinhos e tal, mas isso daqui é muito fácil de acontecer dentro da área
56:4956 minutos e 49 segundosde IA. Eh, já vi vários trabalhos que o pessoal eh overfita, né? Então, faz um
56:5856 minutos e 58 segundossobreajuste sobre aqueles dados. Então, tem uma quantidade de dados, algum dado ali tá um pouquinho mais eh complicado
57:0557 minutos e 5 segundosali e a pessoa ajusta certinho na tá aquele faz aquele recorte certinho, né?
57:1157 minutos e 11 segundosE aí quando vai eh o algoritmo vai funcionar no no dia a dia, né? Ã, aquilo
57:1857 minutos e 18 segundosali acaba sendo um problema, porque notem que a gente fez todo um recorte ali do lado da chuva. Se tudo fosse
57:2557 minutos e 25 segundoschuva aqui embaixo, só aquele ponto, digamos, que alguém anotou errado ou aquele dado realmente aconteceu alguma a
57:3357 minutos e 33 segundoseh aberração, digamos, ali naquele tempo, né? Notem que a gente vai errar muitos dados aqui, né? vai, vai, vai no
57:4157 minutos e 41 segundosinício, eh, quando a gente classificar esse modelo aqui, vai est tudo certo. Se a gente fazer o cálculo de, é, de erro, né, ele vai tá excelente, vai tá
57:4957 minutos e 49 segundosacertando 100%, mas depois conforme a gente for pegando mais dados e esses dados caírem naquela caixinha ali que eu
57:5757 minutos e 57 segundoscriei embaixo, ele vai acabar errando, vai errar muito inclusive, né?
58:0358 minutos e 3 segundosEntão, eh, um outro exemplo aqui da publicidade, eh, a gente poderia traçar a reta, como eu falei, eh, ela vai ter
58:1158 minutos e 11 segundosum erro associado, mas ela a gente pode tentar balancear, né? A gente pode tentar fazer com que ela erre menos possível.
58:2258 minutos e 22 segundosA tentação é fazer isso aqui.
58:2558 minutos e 25 segundosE aí, como eu falei, ah, eventualmente a gente vai ter pontos ali que não passem por esses por esses caminhos, né? Ahã.
58:3658 minutos e 36 segundosTá. Vamos passar aqui rapidinho toda uma conversa de regularização.
58:4258 minutos e 42 segundosEh, eu queria chegar na parte de eh um pouco de redes neurais para pra gente
58:5158 minutos e 51 segundoseh falar rapidamente, porque eu já falei bastante, né, Jerônimo, como é que estamos de de tempo? Será que o pessoal
59:0059 minutosfica mais um tempinho aí só pra gente falar rapidamente do Claro, cara. Pode ficar tranquilo aí, tá? Tá sossegado.
59:0759 minutos e 7 segundosToca ficha.
59:0959 minutos e 9 segundosGente, vamos passar rapidinho ali. Eu acho que esses conceitos aí, eu sei que talvez pode ter terem parecido um pouco básicos para vocês, mas eu queria que
59:1859 minutos e 18 segundosvocês pegassem essa intuição. A partir do que eu falei aqui, vocês vão começar a olhar de uma forma talvez diferente esses algoritmos, né?
59:2859 minutos e 28 segundosAqui rapidamente temos o aprendizado por reforço. Então a gente fez o supervisionado, que era simplesmente a gente dá o exemplo, um monte de exemplos
59:3759 minutos e 37 segundoscom o label, né? Então é Pokémon aqui é de luta, Pokémon esse é água, esse é
59:4459 minutos e 44 segundoságua e a gente desenvolve um algoritmo para predizer a partir dos dados. O aprendizado por reforço é diferente. O
59:5259 minutos e 52 segundosaprendizado por reforço a gente vai eh coloca o agente num eh num ambiente ali.
1:00:011 hora e 1 segundoPensem, por exemplo, eh não sei se vocês chegaram a pegar aquela época do Flapp Bird, mas eh talvez vocês não conheçamô
1:00:081 hora e 8 segundostô ficando velho já. Mas pensem um um num jogo, um personagem
1:00:161 hora e 16 segundosandando. Ã, a ideia é a gente colocar um um um agente, né, o computador ali para
1:00:251 hora e 25 segundoslidar com cada uma das etapas do personagem. Então, primeiro ele vai tentar só andar pra frente. Pensem Pensem no Mário, por exemplo, que é um
1:00:331 hora e 33 segundosum clássico, né? Primeiro ele vai tentar só andar pra frente e aí ele vai ver que não chegou no objetivo dele. Então a
1:00:411 hora e 41 segundosgente vai ter uma função lá que penaliza ele por ele não ter chegado no objetivo.
1:00:451 hora e 45 segundosDaí ele vai tentar andar e dar um pulo no início. Não deu, tenta de novo, tá?
1:00:501 hora e 50 segundosEle vai tentar andar e dar dois pulos, vai tentar andar e dar três pulos.
1:00:541 hora e 54 segundosEventualmente ele vai tentar andar de cabeça para baixo. Ele vai tentar andar eh se arrastando, engatinhando até encontrar uma forma que funcione, tá?
1:01:041 hora, 1 minuto e 4 segundosEntão essa grosseiramente é a forma como funciona o aprendizado por reforço, tá?
1:01:101 hora, 1 minuto e 10 segundosEh, eu trouxe bastante coisa que era legal, mas eh ficar muito extensa esse meu.
1:01:181 hora, 1 minuto e 18 segundosIsso daqui tinha que ter sido umas uns dois workshops, três workshop.
1:01:221 hora, 1 minuto e 22 segundosDeixa eu passar aqui rapidamente. Agora eu tenho que passar por todos os
1:01:261 hora, 1 minuto e 26 segundos[risadas]
1:01:271 hora, 1 minuto e 27 segundosã se eu consigo só Ah, não consigo pular pro
1:01:341 hora, 1 minuto e 34 segundoseh aqui eu tô mostrando mais ou menos o processo de reforço, né, por reforço. Ã,
1:01:421 hora, 1 minuto e 42 segundosentão ele vai testando várias eh possibilidades até chegar no caminho onde ele tem que chegar, né?
1:01:531 hora, 1 minuto e 53 segundosH, deixa eu ver se eu consigo só avançar aqui, senão eu vou ter que passar o tempo todo, né?
1:02:031 hora, 2 minutos e 3 segundosTá, vamos, vamos seguir aqui que eu consigo ter um controle melhor. Ah, aí agora eu consigo ver vocês também.
1:02:091 hora, 2 minutos e 9 segundosaprendizado não supervisionado. Então, a ideia diferente do supervisionado, eu vou dar eh Pensem nos Pokémons
1:02:161 hora, 2 minutos e 16 segundosnovamente. Eh, eu apresento todos eles, todos eles sem sem dizer nada, sem
1:02:231 hora, 2 minutos e 23 segundosqualquer label, sem qualquer coisa. O algoritmo vai simplesmente tentar encontrar padrões nos nos Pokémons, né?
1:02:331 hora, 2 minutos e 33 segundosAh, e ele mesmo vai tentar encontrar classes. Não é que ele vai dizer qual é a classe, tá? Mas ele vai dizer que tá,
1:02:401 hora, 2 minutos e 40 segundosesse Pokémon aqui, todos que são azul, talvez ele vai pensar por cor, né? Ele vai pegar característica mais fácil, né?
1:02:461 hora, 2 minutos e 46 segundosEntão ele vai olhar todas as cores azuis e vai dizer: "Tá, todos esses Pokémons estão meio parecidos aqui, estão numa classe. Esses todos aqui, eles estão
1:02:531 hora, 2 minutos e 53 segundosmeio na num numa posição de de luta, tão meio tão meio beliculosos. Ah, e talvez
1:03:001 hora e 3 minutoseles sejam um Pokémon diferente desses outros que são fofinhos e bonitinhos ali, né? Então, ah, mais ou menos esse é
1:03:081 hora, 3 minutos e 8 segundoso processo do aprendizado não supervisionado, tá?
1:03:121 hora, 3 minutos e 12 segundosÃ, aqui eu tô mostrando basicamente um dos algoritmos é o caminhos, né? Então, deixa eu fechar aqui esse aí, ó.
1:03:221 hora, 3 minutos e 22 segundosEsse o caminhos é basicamente isso, ó.
1:03:241 hora, 3 minutos e 24 segundosTem um monte de dados, né, que a gente não sabe que classe que é. E aí vocês, intuitivamente vocês já conseguem ver,
1:03:321 hora, 3 minutos e 32 segundostem eh um conjunto aqui embaixo, tem um conjunto aqui em cima, tem um aqui em cima. Então o algoritmo vai fazer
1:03:391 hora, 3 minutos e 39 segundossimplesmente isso de pegar eh e classificar esses ah pegar um ponto e tentar classificar e separar esses
1:03:471 hora, 3 minutos e 47 segundosdados, né? Então aqui ele tá, eu tô coloquei aqui as diferente diferentes
1:03:531 hora, 3 minutos e 53 segundosabordagens, né, desse centro eh de de decisão, digamos, né? Ahãsa é mais ou
1:04:021 hora, 4 minutos e 2 segundosmenos a ideia do aprendizado supervisionado, não supervisionado, desculpa. Então, mais ou menos não supervisionado, supervisionado e por reforço, né?
1:04:141 hora, 4 minutos e 14 segundosRapidamente, redes neurais aqui, eh, só pra gente finalizar.
1:04:181 hora, 4 minutos e 18 segundosVou ter que fazer uma ginástica muito grande aqui pra gente conseguir passar pelo pelo processo todo. Ã, mas bom,
1:04:281 hora, 4 minutos e 28 segundosredes neurais é a grande coisa do momento, é a grande área que todo mundo fala que trouxe a a área de inteligência
1:04:381 hora, 4 minutos e 38 segundosartificial mais ou menos de volta a aos holofotes, né? Ah, e bom, a ideia é
1:04:451 hora, 4 minutos e 45 segundosbasicamente a gente replicar mais ou menos o funcionamento de um neurônio, tá? Então, eh, de forma bem básica, a
1:04:521 hora, 4 minutos e 52 segundosgente tem um neurônio que tem conexões com outros neurônios. Então, é um mundo de neurônios, né? E aí, esses neurônios
1:04:591 hora, 4 minutos e 59 segundostêm conexões com esses outros eh ã neurônios.
1:05:051 hora, 5 minutos e 5 segundosE ah dependendo da força como eu eh colocar essa essa
1:05:151 hora, 5 minutos e 15 segundoseh dependendo da força que vem do de que são tudo eletricidade, né? Dependendo da força da eletricidade, ele vai disparar
1:05:231 hora, 5 minutos e 23 segundosã pro próximo neurônio ou não. Então basic é é um conceito eh um pouco mais é mais complexo que isso, mas eh basicamente esse é o processo, tá? Ahã.
1:05:371 hora, 5 minutos e 37 segundosVamos chegar no nossos nosso neurônio artificial. Então, eh, e assim, ele é
1:05:441 hora, 5 minutos e 44 segundosbem simples, tá? O o funcionamento dele é bem simples. Digamos que a gente tem aqui, eh, um neurônio, tá?
1:05:521 hora, 5 minutos e 52 segundosH, que tem uma conexão com outro neurônio. Então, vamos pensar em grafos, né, que é mais fácil paraa nossa área. E
1:05:581 hora, 5 minutos e 58 segundosa gente quer ã a partir desse de de bom, vamos vamos explorar um pouco melhor. Tô
1:06:061 hora, 6 minutos e 6 segundostentando simplificar coisas que vai ficar pior do que a gente explorar o problema, né? Mas tá, vamos pegar um um
1:06:131 hora, 6 minutos e 13 segundosexemplo aqui. Então, a gente tem dois pontos x1 e x2. Talvez pode ser aqueles eh aqueles mesmos argumentos que a gente
1:06:201 hora, 6 minutos e 20 segundosusou no início lá atrás, né, de eh umidade, pressão e se vai chover ou não.
1:06:261 hora, 6 minutos e 26 segundosE a gente quer predizer se vai chover ou não, tá? Então, como eu disse, a gente tem aquela formulazinha que a gente já
1:06:341 hora, 6 minutos e 34 segundosmais ou menos pensou lá atrás, que é uma fórmula que eu pensei, eu eu pensei ah em fazer assim, ela pode ser mais complexa ou pode ser menos complexa, tá?
1:06:461 hora, 6 minutos e 46 segundosEntão, a gente tem aqui a função degrau, né? Aqui tá a função que eu tinha mostrado lá, que é uma a função sigmoide, né? Que ao invés de ter só
1:06:561 hora, 6 minutos e 56 segundoszero e um, a gente vai ter probabilidades, né? Então, a coisa fica mais relaxada, né? Ali tá a fórmula da
1:07:031 hora, 7 minutos e 3 segundosfunção sigmoide. Tem também uma outra que se chama eh a função relu eh que é
1:07:101 hora, 7 minutos e 10 segundosbasicamente ela é constante ali em zero e depois de zero ela segue
1:07:181 hora, 7 minutos e 18 segundosaté então a gente usa o max entre zero e o valor que a gente quer. Se for zero é zero. Se for mais que zero vai ser mais que zero.
1:07:261 hora, 7 minutos e 26 segundosÃ, então o que que acontece? tá? Lá atrás, não sei se vocês lembram, mas a gente
1:07:331 hora, 7 minutos e 33 segundosbotou eh uma regra super simples, né, de como fazer essa classificação. Então, novamente, a mesma função eh hipótese
1:07:421 hora, 7 minutos e 42 segundosaqui que a gente tinha lá atrás, né, com os mesmos argumentos e a gente tem aquela nossa função que a gente desenvolveu.
1:07:511 hora, 7 minutos e 51 segundosÉ, notem que lá atrás a gente botou, se fosse maior que zero esse valor todo era
1:07:581 hora, 7 minutos e 58 segundoschuva ou um, né? True. Se fosse menor que zero, aquilo ali era false, era não
1:08:051 hora, 8 minutos e 5 segundoschuva ou enfim, a a classe negativa daquele problema que a gente tava fazendo.
1:08:111 hora, 8 minutos e 11 segundosIsso que a gente fez é chamado de eh função de ativação, tá?
1:08:171 hora, 8 minutos e 17 segundosEntão, é basicamente uma função que a gente vai colocar entre o nosso a nossa o nosso resultado que vai indicar se aquilo vai ser true ou false.
1:08:301 hora, 8 minutos e 30 segundosPensando em neurônios, vai ser basicamente o que vai definir se ele eventualmente você vai definir se ele vai seguir, né, o o quanto ele vai
1:08:371 hora, 8 minutos e 37 segundosmandar pro próximo neurônio ali, né? Ah, ou não, não é ausência ou ativação.
1:08:451 hora, 8 minutos e 45 segundosEntão aqui tem, eu trouxe os exemplozinhos, né? Então aqui seriam dois neurônios, então duas entradas x1,
1:08:531 hora, 8 minutos e 53 segundosx2, aquele nosso peso que a gente já conversou e a saída vai ser ah aquela classificação.
1:09:011 hora, 9 minutos e 1 segundoEntão notem, eh vamos só para retomar aqui, né? A gente tinha essa função aqui, né? Eh,
1:09:091 hora, 9 minutos e 9 segundosque a gente viu lá atrás que a gente pensou, a gente eh pegou uma função de ativação,
1:09:161 hora, 9 minutos e 16 segundosentão uma função para dizer se aquilo vai ser true ou false, tá? Para definir, para decidir pra gente, né? Ã, e aí pode
1:09:241 hora, 9 minutos e 24 segundosser aquela função simples, pode ser a relu, pode ser a SIGMO, tem várias funções que a gente pode utilizar aqui.
1:09:311 hora, 9 minutos e 31 segundosEntão, a gente vai fazer esse cálculo do jeito que tá aqui. X1 x W1, né? + x2 x
1:09:381 hora, 9 minutos e 38 segundosw2, a gente vai ter um resultado, passa pela função de ativação, a gente tem o nosso resultado decisório, true ou false, né?
1:09:481 hora, 9 minutos e 48 segundosNão esqueçam o bias que eu falei lá atrás, que é esse esse peso extra que parecia meio aleatório lá, mas
1:09:551 hora, 9 minutos e 55 segundosbasicamente esse bias vai nos eh vai nos dar uma certa margem paraa correção, digamos assim, né? Eh, como se a gente
1:10:041 hora, 10 minutos e 4 segundospensar, por exemplo, naquela função lá, naquela reta, né?
1:10:071 hora, 10 minutos e 7 segundosH, esse bias vai ser o que vai conseguir ajustar essa reta, né, né, na na nesse sentido, né? Então, é um valor extra que
1:10:151 hora, 10 minutos e 15 segundosa gente pode eh atrelar a a esse processo aqui, né?
1:10:211 hora, 10 minutos e 21 segundosEntão, eh vamos passar aqui rapidamente. Eu trouxe alguns alguns processos aqui para mostrar, né, fazendo paralelo com aquele
1:10:301 hora, 10 minutos e 30 segundosnossos exemplos, né? Mas gente, o funcionamento quase todo ele é sempre a mesma coisa, independente se a gente tem
1:10:381 hora, 10 minutos e 38 segundosdois, duas entradas, três entradas, 1 milhão de entradas. E aí a gente vai colocando o que a gente precisar de
1:10:451 hora, 10 minutos e 45 segundosentradas, né? Ahã. Então, cada uma das entradas com seus pesos, o nó de saída e uma função de ativação, somando tudo
1:10:531 hora, 10 minutos e 53 segundosaquilo e dando aquela decisão, tá? tem um algoritmo de descida de gradiente que, bom, eu não vou conseguir falar
1:11:021 hora, 11 minutos e 2 segundosmuito sobre eles, né? Depois acho que vocês podem dar uma olhada, mas é basicamente um processo de como a gente
1:11:091 hora, 11 minutos e 9 segundosaqui eu tô mostrando eh aqui é legal de ver, ó, eh digamos que o nossa decisão não fosse só binária, mas fosse com mais classes,
1:11:181 hora, 11 minutos e 18 segundosné? Então o que a gente precisa é ampliar essa nossa saída, né? os nós de saída. E aí a gente pode lidar com
1:11:251 hora, 11 minutos e 25 segundosprobabilidades, né? Então a gente vai passar a não ter uma decisão única, mas probabilidades, né? Então eu vou
1:11:341 hora, 11 minutos e 34 segundosalimentar essas esses meus nós da esquos nós de entrada, né? E com esses cálculos
1:11:411 hora, 11 minutos e 41 segundoseu vou gerar uma certa probabilidade de de ser alguma dessas coisas, né?
1:11:461 hora, 11 minutos e 46 segundosEntão aqui a probabilidade mais alta foi de 100 ensolarado que deu 0, mas os outros deu um valor mais baixo, né? Ah,
1:11:551 hora, 11 minutos e 55 segundosenfim, é o percept que a gente já mais ou menos falou que é essa ideia. A gente
1:12:021 hora, 12 minutos e 2 segundospode começar a eh deixar mais complexo essa nossa função, né? Colocando camadas
1:12:091 hora, 12 minutos e 9 segundose escondidas, né? os hidden layers, ã, que vão fazer, vão pegar essa entrada inicial, pensem que vão fazer como se
1:12:181 hora, 12 minutos e 18 segundosfosse um processamento, né? O que eu gosto de pensar é como se eles fossem, fizessem um filtro no meio do caminho, né? Então eles vão pegar aquela entrada
1:12:261 hora, 12 minutos e 26 segundosbruta ali no início da esquerda aqui, né? vão fazer um certo processamento, vão fazer aqueles mesmos eh cálculos que
1:12:331 hora, 12 minutos e 33 segundosa gente falou ali atrás e vai chegar no final com e ele mais ele já o dado já processado, né?
1:12:421 hora, 12 minutos e 42 segundosEntão eh tudo isso ah e aí tem as redes neuróis profundas que a gente consegue aumenta bastante essa quantidade de
1:12:501 hora, 12 minutos e 50 segundoshidden layers, né? Então, quanto mais hidden layers, mais a gente vai eh tendo capacidade de expressar o que a gente
1:12:581 hora, 12 minutos e 58 segundosquer. Aquele exemplo que a gente teve lá, que tinha todos aqueles pontos e tinha um círculo no meio. Aquele exemplo, por exemplo, a gente consegue
1:13:061 hora, 13 minutos e 6 segundosfacilmente aumentando e essas camadas, né? A gente consegue ter mais margem, porque até então a gente só tava usando
1:13:141 hora, 13 minutos e 14 segundosum processo de separação linear. Agora a gente tem uma função que a gente não sabe que é isso daqui vai ser uma coisa
1:13:211 hora, 13 minutos e 21 segundosabsurda, né? Ã, então essas são as redes neurais profundas, né? Ã,
1:13:291 hora, 13 minutos e 29 segundosúltima coisa, só para finalizar, eu prometo, tá, J? Não, não fica bravo comigo. Eh, e vocês também, gente. Eh, já só para pra gente passar rapidamente,
1:13:381 hora, 13 minutos e 38 segundosque talvez fosse o tópico mais legal dessa desse momento, né? visão computacional, que é especificamente a
1:13:461 hora, 13 minutos e 46 segundosárea que lida com dados de imagem, vídeo, enfim. Ah,
1:13:521 hora, 13 minutos e 52 segundosentão eh aqui eu mostrava esses é um dataset de eh escrita à mão, né? é que tá disponível, que é bastante clássico.
1:14:031 hora, 14 minutos e 3 segundosE a ideia é como que a gente consegue identificar esses esses dígitos só pelos
1:14:101 hora, 14 minutos e 10 segundospixels dessa imagem, né? Então, eh tem ali os pixels, né? A imagem tem um
1:14:181 hora, 14 minutos e 18 segundostamanho padrão, todos os pixels tm um tamanho padrão. Como é que eu consigo olhar para esse oito e e pensar um
1:14:251 hora, 14 minutos e 25 segundosalgoritmo que eh olha para esse esse monte de pixelzinhos, né? Não só os do oito, mas de toda a matriz ali. E diz:
1:14:341 hora, 14 minutos e 34 segundos"Tá, esse daqui, esse daqui é um oito, esse daqui é um dois, esse daqui é um cachorro, esse daqui é um gato, esse daqui é uma pessoa, esse daqui é o
1:14:421 hora, 14 minutos e 42 segundosCarlos e esse daqui é o Jerônimo." Difícil, né? Porque aqui ainda é mais simples porque só tem duas cores, né?
1:14:521 hora, 14 minutos e 52 segundosMas numa imagem que tem mais cores começa a se tornar bastante complicado, né, de fazer esse processo aqui. Ã, mas
1:15:011 hora, 15 minutos e 1 segundobom, aí a gente começa a ver a convolução, né, que é uma rede neural gigantesca,
1:15:081 hora, 15 minutos e 8 segundostá? Eh, aí eu fala de CNN, né, que é uma uma rede neural gigantesca, mas que
1:15:171 hora, 15 minutos e 17 segundostrabalha com convolução. Qual que é o a ideia básica da convolução? Tá, se já se encaminhando pro final aqui, gente. Eh,
1:15:261 hora, 15 minutos e 26 segundosa convolução é basicamente um filtro que a gente aplica na imagem original.
1:15:311 hora, 15 minutos e 31 segundosEntão, a gente tem, pensa aqui que a gente tem a imagem original e, digamos que esse daqui é os valores dos pixels, tá? Eh, eu simplifiquei aqui, tá? Vamos
1:15:401 hora, 15 minutos e 40 segundospensar só a intensidade de preto. É o branco e a intensidade de preto. Então aqui a intensidade é 10, 20, 30, 40 e assim por diante.
1:15:501 hora, 15 minutos e 50 segundosE aí eu penso num filtro e aí esse filtro a gente também vai treinar, né, para para chegar em um filtro que seja
1:15:591 hora, 15 minutos e 59 segundossuficientemente bom, né, para lidar com isso. E esse filtro vai passar por cada pixel dessa imagem e vai fazer essa esse processamento.
1:16:091 hora, 16 minutos e 9 segundosEntão, 0 x 10 - 1 x 20 0 x 30. E aí a gente soma tudo e a gente chega naquele
1:16:171 hora, 16 minutos e 17 segundosvalor final. Então, como eu falei, assim como os o o as camadas intermediárias
1:16:241 hora, 16 minutos e 24 segundosali, as hidayers, isso daqui é um filtro. O que que acontece? Talvez a gente possa ter um filtro especializado
1:16:321 hora, 16 minutos e 32 segundosem identificar bordas, tá? Então a gente pode ter aqui, ele trouxe um filtro que identifica bordas, ó. Então ele passou
1:16:401 hora, 16 minutos e 40 segundosaquele mesmo processo que eu mostrei para vocês e transformou a imagem dessa forma. Talvez a gente queira só saber
1:16:471 hora, 16 minutos e 47 segundosaonde tá a separação do céu pro resto da imagem.
1:16:511 hora, 16 minutos e 51 segundosTalvez seja uma um dos objetivos aqui, né?
1:16:551 hora, 16 minutos e 55 segundosEntão, tanto faz se aquele toda aquela parte azul do céu, né, pra gente, o importante é só aonde tá a borda disso
1:17:031 hora, 17 minutos e 3 segundosdaqui que consegue separar um do outro, né? E daí antes da gente entrar eh mandar imagem pra nossa rede neurógica,
1:17:111 hora, 17 minutos e 11 segundosvai mandar esse essa imagem filtrada pra nossa rede. E aí ela vai fazer o
1:17:181 hora, 17 minutos e 18 segundosprocesso, tá? Vai fazer todos os cálculos e tal. vou olhar cada um dos pixels e vai gerar um resultado lá no fim. O último conceito aqui que é
1:17:271 hora, 17 minutos e 27 segundosimportante é o de pulling, né? Pensem que ã a gente pega uma imagem gigantesca, né? Eh, uma imagem em 4K,
1:17:361 hora, 17 minutos e 36 segundospor exemplo, é eh 4800 e pouco vezes 4 3000 e alguma coisa, né? É muita coisa,
1:17:441 hora, 17 minutos e 44 segundosé muitos pixels. A gente botar uma rede neural grandiosa para conseguir pegar toda essa imagem é custoso, né? Então a
1:17:531 hora, 17 minutos e 53 segundosgente tem um processo de pulling que é basicamente a gente pegar um filtro novamente, só que a gente vai fazer um
1:18:011 hora, 18 minutos e 1 segundoum bem bolado desse desse nosso desse nosso desse nossos pixels, né? Então, a gente
1:18:101 hora, 18 minutos e 10 segundospode, e aí tem várias abordagens, a gente pode pegar o o pixel com maior eh intensidade, né? Então aqui é entre todos aqui 50, 110, aqui vai ser 20, né?
1:18:221 hora, 18 minutos e 22 segundosE aqui vai ser 40. Então a gente pegou aquela imagem grandona e eh encolheu
1:18:311 hora, 18 minutos e 31 segundosela, né? pegou o que era mais eh significativo pra gente. Talvez o mais significativo aqui seja uma uma outra
1:18:391 hora, 18 minutos e 39 segundosfunçãozinha que lide com faça uma média dos pontos, faça eh sei lá, pegue só os
1:18:461 hora, 18 minutos e 46 segundosos 10 melhores maiores, né? E aí a gente pode definir a o tamanho. Aqui eu tô mostrando de 2 por 2, mas pode ser um
1:18:551 hora, 18 minutos e 55 segundos4x4, 6x 6, enfim, cada abordagem é uma abordagem específica que a gente precisa
1:19:021 hora, 19 minutos e 2 segundoslidar, né? E a rede eh neural convolucional, a CNN, né? É basicamente isso. A gente passa por pega a imagem
1:19:111 hora, 19 minutos e 11 segundoscompleta, passa por uma convolução, então a gente filtra ela para eh e aqui pensem que filtro é sempre a gente pode
1:19:191 hora, 19 minutos e 19 segundospensar como características importantes daquela imagem, tá? Bordas, regiões de de fronteira, né? Então ele faz uma
1:19:281 hora, 19 minutos e 28 segundosconvolução, faz um pulling ali para baixar essa a dimensão dessa imagem, a gente achata e aí a gente coloca na
1:19:361 hora, 19 minutos e 36 segundosnossa rede neural, tá? Então mais ou menos é isso, gente. Eu ã aí todo o
1:19:431 hora, 19 minutos e 43 segundosprocesso de eh depois tem eh trabalho com LLMs, né, com com linguagem, tem
1:19:511 hora, 19 minutos e 51 segundostodo um processo aí de de redes neurais, né? Ahã. Mas bom, gente, eh, acho que a
1:19:591 hora, 19 minutos e 59 segundosconversa era essa. A minha ideia aqui era de fato fazer uma introdução eh de
1:20:061 hora, 20 minutos e 6 segundosforma intuitiva, tá? Eh, eu queria que vocês tivessem uma certa noção do que é a área, passasse de bem uma pincelada
1:20:151 hora, 20 minutos e 15 segundospor tudo, né? Eh, para que você tivesse essa noção, eh, peço desculpas para quem já tem um pouco mais de conhecimento aí,
1:20:231 hora, 20 minutos e 23 segundostalvez possa ter sido um pouco básica, né? Mas também tive que escolher qual ia ser o foco, né? Não tinha como colocar
1:20:321 hora, 20 minutos e 32 segundostudo aqui. Ã, mas é isso, gente. Muito obrigado aí pelo pelo tempo de vocês, pela paciência. Eh, e boa sorte aí no no
1:20:411 hora, 20 minutos e 41 segundosprocesso. Eh, aproveitem passar a palavra pro Geroni.
1:20:491 hora, 20 minutos e 49 segundosMuito bem, Carlos, muito obrigado aí pela pela tua ótima ótima palestra. foi
1:20:561 hora, 20 minutos e 56 segundosmuito bom, muito eh informativo. Acho que o pessoal vai, com esses conceitos que tu conseguiu trazer aí, vai
1:21:031 hora, 21 minutos e 3 segundosconseguir eh ter boas ideias para resolver o problema aí durante o o
1:21:101 hora, 21 minutos e 10 segundosHackaton. Eh, tu estavas um pouco preocupado com o tempo, então eu fui ter fazendo algumas alguns favores aqui, porque o pessoal tava fazendo bastante
1:21:191 hora, 21 minutos e 19 segundosperguntas no Ah, é, eh, no chat. E as que eu fui conseguindo aqui, eu fui eu fui respondendo, né?
1:21:271 hora, 21 minutos e 27 segundosEntão, por exemplo, né, o teve um aqui o colega, onde é que tá aqui? Desculpe. HH
1:21:351 hora, 21 minutos e 35 segundoseh, o a Eduarda perguntou sobre a gravação. Sim, Eduarda, a gente vai a gente vai disponibilizar junto com os
1:21:421 hora, 21 minutos e 42 segundosslides do Carlos. Eh, o Márcio perguntou se a gente vai conseguir eh, se a apresentação dos dados e do KGO será
1:21:511 hora, 21 minutos e 51 segundosapós a palestra. Sim. Então, agora na sequência, uma vez que a gente termina com as dúvidas aqui, eu vou apresentar
1:21:581 hora, 21 minutos e 58 segundostanto os dados quanto o Kegle. Eh, o João falou do que o SVM tem diferentes
1:22:051 hora, 22 minutos e 5 segundosativações que tratam não só de separação entre fronteiras. É mais um comentário, né?
1:22:111 hora, 22 minutos e 11 segundosEh, o Daniel perguntou se função de perda tem o mesmo o mesmo sentido de função de custo, não é?
1:22:201 hora, 22 minutos e 20 segundosCost function, né?
1:22:211 hora, 22 minutos e 21 segundosÉ, são são diferentes. É, quer dizer, é, a gente pode considerar, mas eh a princípio são
1:22:301 hora, 22 minutos e 30 segundosde problemas diferentes, né? O de custo é mais talvez eh orientado ali a à
1:22:371 hora, 22 minutos e 37 segundosbusca, eh, a otimização, né? que é uma outra área da da IA, mas a gente pode pensar também como se fosse, né, algo
1:22:451 hora, 22 minutos e 45 segundoscom um custo, né, mas a nota que custo é o quanto a gente e eh gasta para chegar aí um problema de de busca, né, só
1:22:531 hora, 22 minutos e 53 segundosrapidamente, né, problema de busca, a gente quer chegar de um lugar para um de um estado A para um estado B, né? Então, pensa Google Maps, um exemplo mais
1:23:031 hora, 23 minutos e 3 segundosprático ali, que é chegar de eh de Pelotas a Porto Alegre, vamos usar o exemplo aqui, né? Quais as
1:23:101 hora, 23 minutos e 10 segundospossibilidades, quais os caminhos que eu posso explorar, né? Tem vários, vários caminhos que eu posso explorar. Então, o
1:23:171 hora, 23 minutos e 17 segundoscusto aí seria, poderia ser a quilometragem, né? O quanto eu custa para mim chegar até Porto Alegre. Então,
1:23:241 hora, 23 minutos e 24 segundoseu posso ir pela costa da do Rio Grande do Sul e vai ter um custo X. Se eu ir pelo interior, mais pra esquerda e fazer
1:23:321 hora, 23 minutos e 32 segundostoda uma volta, né? Vai ter um custo 2 3x, por exemplo, né? Isso é custo. Ã, a
1:23:391 hora, 23 minutos e 39 segundosfunção de loss a gente tá eh tentando quantificar o nosso erro, né? Então, a gente faz uma previsão e vê quanto a
1:23:471 hora, 23 minutos e 47 segundosgente errou. Eh, são conceitos eh diferentes, tá?
1:23:531 hora, 23 minutos e 53 segundosPerfeito. Eh, beleza. Aí depois o o João também ele interagiu com o pessoal. Como aí, poxa, aí o rapaz complica um pouco.
1:24:061 hora, 24 minutos e 6 segundosEle botou um número no nome ali, se ele quiser [risadas] qual que é o nome dele no o 32. 33 ali.
1:24:131 hora, 24 minutos e 13 segundosÉ o 32. É, ele perguntou como saber se o erro é aceitável. Eu comentei ali para aí eu
1:24:211 hora, 24 minutos e 21 segundostive já puxei a a brasa pro nosso assado aqui falando, né, sobre os baselines que a gente geralmente treina, mas se tu quiser dar uma complementada, por favor.
1:24:311 hora, 24 minutos e 31 segundosNão sei se a ideia eu posso responder, mas é que pessoal, tá?
1:24:351 hora, 24 minutos e 35 segundosClaro, eh, gente, erro, né? Erro é uma coisa bastante complicada assim, porque eh
1:24:431 hora, 24 minutos e 43 segundosisso vai depender muito do problema que tu tá que tu tá resolvendo, né? Eh, tem uma parte eh específica, por exemplo, da
1:24:521 hora, 24 minutos e 52 segundosnão só da IA, mas a parte de eh de algoritmos mesmo, né? Toda uma área da computação que se preocupa com
1:25:001 hora e 25 minutosotimização, né? Então, assim, por exemplo, esse esse problema do Google Maps, né? Ã, digamos que eu quero sair
1:25:081 hora, 25 minutos e 8 segundosaqui de Pelotas, aqui do fim do Rio Grande do Sul, lá para Salvador, lá em cima. Pensem a quantidade de possibilidades que eu vou ter de
1:25:161 hora, 25 minutos e 16 segundoscaminhos para explorar. Pensa em um computador que tem que sair explorando caminhos. A gente consegue ver o mapa por cima, né? A gente sabe que que tem
1:25:241 hora, 25 minutos e 24 segundosesse caminho aqui parece ser o melhor, né? Ah, mas pro computador isso é uma tarefa bastante complicada. É uma
1:25:311 hora, 25 minutos e 31 segundosexplosão de de estados, né? Eh, e o faz isso em segundos, né? Como é que ele faz
1:25:381 hora, 25 minutos e 38 segundosisso? Ele faz uma estimativa, ele faz uma função que estima mais ou menos eh qual é a distância mais ótima.
1:25:481 hora, 25 minutos e 48 segundosEh, será que a distância mais a melhor distância vocês [limpando a garganta] já devem ter usado maps Uber? Vocês vão ver
1:25:541 hora, 25 minutos e 54 segundosque não. Eh, constantemente ele dá uma uma um caminho muito ruim, né? Mas por quê? Porque ele estimou um caminho, né?
1:26:031 hora, 26 minutos e 3 segundosEle ele fez um cálculo ali meio por cima assim. Eh, o que que seria melhor? Daí eu aí eu volto a pergunta que retorno a
1:26:101 hora, 26 minutos e 10 segundospergunta para ti, né? Para te refletir um pouco, né? Eh, o que que seria melhor? A gente esperar 10 anos para ter
1:26:181 hora, 26 minutos e 18 segundosa resposta do [risadas] caminho de Pelotas a Salvador ou ter a resposta em milissegundos, mas não ser a
1:26:271 hora, 26 minutos e 27 segundosresposta melhor? Vai ter um erro atrelado ali. Talvez não seja a melhor rota, mas é melhor do que nada, é melhor do que a a outra possibilidade, né?
1:26:381 hora, 26 minutos e 38 segundosEntão, infelizmente é sempre esse balanço, né? o quanto a gente de fato eh o quanto o nosso problema permite a
1:26:461 hora, 26 minutos e 46 segundoserrar. A gente tá fazendo um exame lá de, sei lá, acho que é é encontrar eh
1:26:521 hora, 26 minutos e 52 segundoscâncer num raio X, né? Ã, sei lá, será que a gente quer o máximo que o que que
1:26:591 hora, 26 minutos e 59 segundoso o modelo seja muito conservador e erre bastante, mas eventualmente pegue casos que de fato eram câncer? ou será que a
1:27:081 hora, 27 minutos e 8 segundosgente quer que ele não erre nunca, mas ele deixa passar alguns casos, né? Então é sempre esse balanço, gente. É sempre
1:27:161 hora, 27 minutos e 16 segundospor isso que por isso que precisa de gente que conhece e precisa dos dos dos
1:27:231 hora, 27 minutos e 23 segundospesquisadores e engenheiros de, né, de com conhecimento ali. Vamos ver.
1:27:301 hora, 27 minutos e 30 segundosPerfeito. Não, muito bom, Carlos.
1:27:331 hora, 27 minutos e 33 segundosEh, eu me permito completar eh complementar, aliás, a tua claro, a tua eh resposta com algo que a professora Marília falou pela manhã, né?
1:27:441 hora, 27 minutos e 44 segundosEh, por exemplo, no nosso caso específico aqui de previsão eh climática, por exemplo, né? um um baseline muito, né, que é algo, digamos
1:27:521 hora, 27 minutos e 52 segundosassim, óbvio, que a gente que a gente tenta sempre compara o nosso modelo, né, para saber se o modelo de fato é útil, é a climatologia, né? Então, a média do
1:28:011 hora, 28 minutos e 1 segundoque chove num mês, né? Pega 30 anos do que chove em janeiro e aquela é a tua previsão. Bom, será que o meu modelo faz
1:28:081 hora, 28 minutos e 8 segundosuma previsão melhor do que na do que essa média? Então, perfeito. Exatamente.
1:28:141 hora, 28 minutos e 14 segundosÉ algo são esses baselines, né, que o pessoal que que a gente vê bastante também nos artigos aí, né, Carlos?
1:28:211 hora, 28 minutos e 21 segundosSim, sim. Então, é é um é um bom exemplo, cara. É um, é exatamente isso.
1:28:281 hora, 28 minutos e 28 segundosA Karina falou que aceita os três três workshops.
1:28:321 hora, 28 minutos e 32 segundos[risadas] Aí já falamos ali do erro. Eh, [roncando] o José Carlos depois pergunta
1:28:391 hora, 28 minutos e 39 segundosnessa questão da função de ativação, se eu usar a Sigmoide, não vai dar um resultado diferente se eu for usar relu?
1:28:461 hora, 28 minutos e 46 segundosO que determina a função de ativação a ser usada? [limpando a garganta] Boa pergunta, excelente pergunta. Eh, nota que esse problema da Ele tá aí, T.
1:28:561 hora, 28 minutos e 56 segundosEh, nota que esse problema de qual função de de ativação usar, né? Isso,
1:29:031 hora, 29 minutos e 3 segundosnovamente, isso tudo vai depender do do problema, infelizmente. E esse o que torna a área de A tão eh complexa, né? E
1:29:131 hora, 29 minutos e 13 segundosporque a gente vê os ah GPT saiu, [roncando] saiu cloud, sempre coisa nova, né? Parece que a coisa é
1:29:201 hora, 29 minutos e 20 segundossuper simples, mas quem trabalha com o o o eh de fato ali com problema, eh a coisa
1:29:301 hora, 29 minutos e 30 segundosé muito mais embaixo. Às vezes às vezes a gente tem que tomar decisões eh muito complicadas ali, a gente tem que pesquisar muito, né? Por isso que é uma
1:29:381 hora, 29 minutos e 38 segundosárea que não é simplesmente eh ver um vídeo no YouTube e e sai e fazer, né? É toda uma um estudo, né?
1:29:471 hora, 29 minutos e 47 segundosEntão, por isso que é importante entender o que que cada uma, qual a característica de cada uma das funções, né? Ã, a Sigmoide, por exemplo, tem uma
1:29:571 hora, 29 minutos e 57 segundosuma curva mais suave, né? Então, talvez a probabilidade ali vai ficar um pouquinho mais tranquila. A relu já é
1:30:051 hora, 30 minutos e 5 segundoszero e qualquer valor, né? Então ela é é uma coisa mais talvez agressiva, né? Ah,
1:30:131 hora, 30 minutos e 13 segundosentão depende do do problema. Isso. Eh, cada problema vai ter uma uma indicação.
1:30:201 hora, 30 minutos e 20 segundosE aí é testando. Eh, tinha um professor nosso que é o Ricardo que falava muito que eh chega um momento que é meio no
1:30:291 hora, 30 minutos e 29 segundosfeeling. É, é ruim a gente falar isso, né? Porque parece uma coisa meio não ortodoxa, né? Mas às vezes a coisa é no
1:30:371 hora, 30 minutos e 37 segundosfeeling. Por que que eu uso, por exemplo, eh, ali a gente tava falando do tem alguns hiperparâmetros, né? alguns
1:30:441 hora, 30 minutos e 44 segundosmodelos que a gente define quais os hiperparâmetros.
1:30:471 hora, 30 minutos e 47 segundosPor exemplo, tem o o o camin ali, o o aliás, o KNN, que é o dos eh K ã
1:30:561 hora, 30 minutos e 56 segundosvizinhos mais próximos, né? Como é que a gente define esse K? A gente pega 10 vizinhos mais próximos, a gente pega só
1:31:031 hora, 31 minutos e 3 segundoso vizinho mais próximo, um pega 100, pega 1000. Não tem como saber, né? É
1:31:091 hora, 31 minutos e 9 segundosnovamente é testando, né? olhando paraos teus dados e um pouco tem esse feeling
1:31:161 hora, 31 minutos e 16 segundostambém de de eu vou chutar aqui, eu acho que vai dar certo sem testo, tá? Deu certo. Parece que funcionou, né?
1:31:251 hora, 31 minutos e 25 segundosMas é isso. Perfeito.
1:31:281 hora, 31 minutos e 28 segundosMuito bem. Ótimo. Muito obrigado. Eh, depois o José Carlos pergun agradece ali, né? E o Alisson tinha perguntado
1:31:351 hora, 31 minutos e 35 segundoscomo as gravações vão ser acessadas. A gente já processou a da manhã, depois vai processar. Tem um tempinho aqui que a que a plataforma processa a gravação e
1:31:451 hora, 31 minutos e 45 segundosdepois a gente vai disponibilizar no no SL no Slack. Isso mesmo, no Slack, pessoal. Então, eh, vocês fiquem
1:31:541 hora, 31 minutos e 54 segundostranquilos que, provavelmente até o final do dia, no máximo amanhã, vocês vão ter acesso a essas gravações.
1:32:011 hora, 32 minutos e 1 segundoBom, eh, pessoal, se ninguém tiver mais nenhuma pergunta pro Carlos, eu, em nome
1:32:081 hora, 32 minutos e 8 segundosde todos nós aqui, agradeço novamente a ele pela boa vontade, pelo tempo que ele dedicou aí para nos dar essa ótima palestra.
1:32:171 hora, 32 minutos e 17 segundosEh, Carlos, por favor, fique à vontade aí para ficar com a gente, se tu quiseres e puderes, e se não continuar nas tuas
1:32:261 hora, 32 minutos e 26 segundosatividades. Aí a gente vai seguir agora aqui. Perfeito.
1:32:291 hora, 32 minutos e 29 segundosAntes da gente da gente eh encerrar o dia de hoje, né, o primeiro dia, eu vou apresentar um pouquinho agora sobre os
1:32:371 hora, 32 minutos e 37 segundosdados, falar finalmente sobre o problema, né, e mostrar o Kego, que é onde o pessoal vai fazer a vai fazer as
1:32:441 hora, 32 minutos e 44 segundossubmissões do do das suas soluções aí no no decorrer dos próximos 10 dias. Então, te agradecemos de novo pela boa vontade
1:32:521 hora, 32 minutos e 52 segundose fique fique à vontade aí para para nos para seguir nos acompanhando, tá bom? Perfeito. Deixa eu só dar um a último.
1:33:011 hora, 33 minutos e 1 segundoEh, gente, eh, novamente, obrigado, obrigado pelo pelo vocês que que me convidaram aí. Ã, pessoal, aproveitem a
1:33:091 hora, 33 minutos e 9 segundosoportunidade, aproveitem para estudar eh a nossa, só dar uma algumas palavras aí
1:33:161 hora, 33 minutos e 16 segundosde encerramento, né? Mas, eh, a área tá bastante eh em alta, ao mesmo
1:33:231 hora, 33 minutos e 23 segundostempo tá bastante concorrida, né? Mas tem muita gente, eh, tem muita gente que
1:33:311 hora, 33 minutos e 31 segundosé desqualificada ali, que a gente tá num ritmo que às vezes ainda não tem gente suficiente com qualificação, né? E é
1:33:391 hora, 33 minutos e 39 segundosessa, esse pessoal que tá que tá indo atrás, que tá estudando de fato, como é que funciona ali a fundo aquele algoritmo, que entende, né, que faz as
1:33:481 hora, 33 minutos e 48 segundosperguntas certas, qual que é a diferença usar uma relu ou uma outra função de ativação, né? é esse pessoal que vai que eventualmente o mercado vai querer.
1:33:591 hora, 33 minutos e 59 segundosEntão, sigam aí nesse, nessa busca aí por aperfeiçoamento.
1:34:041 hora, 34 minutos e 4 segundosEh, que o que precisarem de mim podem podem mandar e-mail, podem me chamar. Eu tô no Slack ali também. Eh, talvez eu
1:34:131 hora, 34 minutos e 13 segundosnão veja, mas vocês podem me chamar ou no LinkedIn ali, que é um é um lugar também que eu eu olho e se vocês quiserem alguma ajuda ali, eu posso ajudo vocês e fico à disposição, tá bem?
1:34:261 hora, 34 minutos e 26 segundosMas é isso, gente. Valeu. Eu tenho que sair aqui já.
1:34:301 hora, 34 minutos e 30 segundosVale, beleza, cara. Muito obrigado aí. Um bom fim de tarde para ti e obrigado novamente.
1:34:381 hora, 34 minutos e 38 segundosValeu, gente. Boa sorte.
1:34:411 hora, 34 minutos e 41 segundosEntão tá, pessoal, eh, continuamos aqui na nossa vaca fria, digamos assim. Eu vou compartilhar agora eu, a minha tela.
1:34:491 hora, 34 minutos e 49 segundosÃ, por favor, Igor, só me coloca como apresentador para eu poder apresentar.
1:34:551 hora, 34 minutos e 55 segundosEntão, gente, acho que agora a gente vai para pro momento, acho que tava que tá todo mundo esperando, né, que é, enfim,
1:35:031 hora, 35 minutos e 3 segundospra gente conseguir falar sobre sobre o problema e como que a gente vai tentar
1:35:111 hora, 35 minutos e 11 segundosresolver eh essa questão de previsão climática com aprendizado de máquina. [roncando]
1:35:191 hora, 35 minutos e 19 segundosMuito bem. Então, vocês estão vendo a minha tela? Eu queria, eu também fiz um conjuntinho de, de slides aqui. Eh, eu
1:35:281 hora, 35 minutos e 28 segundosnão vou eu não vou tomar muito mais o tempo de vocês. Eu acho que é só eu apresentar e a gente discutir eventuais
1:35:361 hora, 35 minutos e 36 segundosdúvidas de vocês. Eu vou mostrar também o Kegle antes da gente concluir, tá bom?
1:35:411 hora, 35 minutos e 41 segundosEh, então, muito bem, né? Eh, nós vamos, o problema que a gente vai abordar é previsão climática. Então, previsão
1:35:491 hora, 35 minutos e 49 segundosclimática eh de precipitação, né? Então, como a professora Marília já falou mais cedo, né? Eu não quero também eh repetir
1:35:571 hora, 35 minutos e 57 segundosmuito que o pessoal já já comentou, mas acho que vocês conseguiram entender a ideia de do quão difícil é esse problema
1:36:051 hora, 36 minutos e 5 segundosde de eh de previsão de precipitação em escala mensal, né? E vai ser esse o vai
1:36:121 hora, 36 minutos e 12 segundosser esse o problema que a gente vai abordar aqui do lado. Vocês já podem ver, por exemplo, os mapinhas que vocês vão estar nos próximos 10 dias aí eh
1:36:221 hora, 36 minutos e 22 segundosplotando e e olhando, né? Esses são os dados do 5 de precipitação, né? Vocês lembram quando a professora Marília falou pela manhã sobre os dados de
1:36:311 hora, 36 minutos e 31 segundosreanálise? Então, são esses os dados que a gente vai utilizar para fazer eh para fazer os nossos experimentos. Eles não
1:36:391 hora, 36 minutos e 39 segundossão muito, eles não são necessariamente dados de observação, como dados de satélite. [roncando] Quem já conhece um pouco aí da área sabe que a gente tem,
1:36:481 hora, 36 minutos e 48 segundoseh, conjunto de dados eh de satélites, né, ou seja, de observações mesmo. A gente vai utilizar esse conjunto aqui
1:36:561 hora, 36 minutos e 56 segundosporque ele é um dado baseado em observações e a gente tem uma série histórica eh maior desses dados, né?
1:37:031 hora, 37 minutos e 3 segundosEntão, a gente vai trabalhar com a série histórica de 1940 até 2024, dados mensais, né? Então, os dados de precipitação mensal. Muito bem, né?
1:37:161 hora, 37 minutos e 16 segundosEntão, como eu falei para vocês, é a tarefa aqui, basicamente, tentando resumir em um slide, é dado dado o
1:37:251 hora, 37 minutos e 25 segundosestado atmosférico em um mês, né? eh, a gente vai tentar fazer uma estimativa da média de precipitação do próximo mês e a
1:37:341 hora, 37 minutos e 34 segundosgente vai utilizar então esses dados do 5 de reanálise para aquele domínio da da América do Sul. Eh, já havia surgido uma
1:37:431 hora, 37 minutos e 43 segundosdúvida durante a manhã ali sobre a questão da previsão em anomalia, em probabilidades aqui, né? Eu acho que
1:37:521 hora, 37 minutos e 52 segundosvocês já conseguiram ter uma ideia de que é um problema de fato bem complexo.
1:37:561 hora, 37 minutos e 56 segundosEntão, a gente vai dar uma, como é um exercício e muito mais uma um, né, um um
1:38:041 hora, 38 minutos e 4 segundoslugar de aprendizado, a gente vai eh simplificar um pouco esse esse problema,
1:38:111 hora, 38 minutos e 11 segundosné, e vai fazer a a previsão de absolutos, né? Então a gente vai ver, tentar prever a média em a precipitação
1:38:181 hora, 38 minutos e 18 segundosem milímetros por dia, eh, a média do mês, né? Então, eh, a, e a gente vai trabalhar com a previsão absoluta, né?
1:38:291 hora, 38 minutos e 29 segundosMuito bem. Eh, então aqui, eh, hoje a gente tá no dia um com essas apresentações e a gente vai ficar aí
1:38:361 hora, 38 minutos e 36 segundosaté, eh, a partir de hoje, já, na verdade, né, até o dia do workup, no dia 23, ou seja, vamos ter aí 10 dias para
1:38:461 hora, 38 minutos e 46 segundosfazer essa essa ã vocês eh conseguirem fazer as suas os seus desenvolvimentos.
1:38:541 hora, 38 minutos e 54 segundosa gente eh reconhece que é de fato um tempo um pouco curto, mas a gente precisa também, né, eh fazer, a gente
1:39:021 hora, 39 minutos e 2 segundostem essa data limite do nosso do nosso evento aqui da pós-graduação, que eu reforço para convidar todos, né? Então,
1:39:101 hora, 39 minutos e 10 segundoseh, vocês vão ter esse período aí de 10 dias a partir de hoje, né, para para fazer os desenvolvimentos até o dia 23.
1:39:181 hora, 39 minutos e 18 segundosEntão aqui, eh, como eu comentei, a gente tem, eh, os dados de 1940 até
1:39:241 hora, 39 minutos e 24 segundos2024. Esses dados de 1940 até 2022 vão ser os dados que vocês vão baixar lá no Kagle [roncando]
1:39:321 hora, 39 minutos e 32 segundospara fazer o treinamento do dos modelos de vocês, né, e desenvolver as soluções. E
1:39:391 hora, 39 minutos e 39 segundosa gente vai ter dois anos de conjunto de teste ali que vocês não vão receber.
1:39:441 hora, 39 minutos e 44 segundosEsses dados vão ser só utilizados para eh para vocês terem as
1:39:531 hora, 39 minutos e 53 segundosas métricas, né, pra gente calcular as métricas, que é o RMFE, né, o erro o a raiz do erro quadrado do do erro
1:40:011 hora, 40 minutos e 1 segundoquadrático. E a gente separou isso eh esse conjunto de teste em dois, né?
1:40:071 hora, 40 minutos e 7 segundosEntão, eh, o ano de 2023, ele vocês vão ter ali agora no Kego, na sequência, eu vou eu vou eh
1:40:161 hora, 40 minutos e 16 segundoseu vou falar com um pouco mais de detalhe quando eu mostrar a plataforma, mas vai ter um leaderboard ali, né? Ou
1:40:221 hora, 40 minutos e 22 segundosseja, um um ranking com as soluções. É esse esse ranking público, né? O ano de
1:40:301 hora, 40 minutos e 30 segundos2023 vai ser utilizado para calcular um ranking público. Ou seja, vocês vão ter já um para vocês irem tendo uma ideia de
1:40:371 hora, 40 minutos e 37 segundosquão boas eh o quão boas tá sendo já as soluções de vocês num conjunto independente, mas de
1:40:461 hora, 40 minutos e 46 segundosfato a a as métricas que vão decidir o ganhador da competição vão ser calculadas sobre o ano de 2024. Então,
1:40:551 hora, 40 minutos e 55 segundoseh, isso é pra gente não cair num pouco daquele problema que o Carlos tinha comentado agora na apresentação dele, né, sobre ajuste, sobre ajuste de
1:41:041 hora, 41 minutos e 4 segundosmodelos, né, a gente pode eh muito bem, seja por maldade ou por por erro de
1:41:121 hora, 41 minutos e 12 segundosdesenvolvimento mesmo, né, fazer um modelo que vai muito bem apenas num ano específico, mas na prática, nos outros anos ele vai muito mal. Então isso é uma
1:41:201 hora, 41 minutos e 20 segundosforma que a gente que a gente eh ajuda vocês inclusive a tentar mitigar esse risco, né, do do sobreajuste do modelo num conjunto de dados específico.
1:41:311 hora, 41 minutos e 31 segundosEh, e para vocês também irem tendo uma ideia de quão boa tá sendo a solução de vocês, né?
1:41:371 hora, 41 minutos e 37 segundosEh, aqui é uma coisa importante, tá? Eh, vocês vocês eh viram na palestra de
1:41:451 hora, 41 minutos e 45 segundosmanhã, né, que a previsão climática ela envolve uma série de questões, dado eh dados de atmosfera, dados de superfície
1:41:521 hora, 41 minutos e 52 segundosdo mar, eh uso cobertura da terra, várias coisas, né?
1:41:571 hora, 41 minutos e 57 segundosEh, como eu já tinha comentado com vocês em alguma em uma outra comunicação que que a gente que a gente teve, eh, o
1:42:051 hora, 42 minutos e 5 segundosvolume de dados, esses dados meteorológicos, mesmo eles na nas suas médias mensais, ele é muito grande, tá?
1:42:121 hora, 42 minutos e 12 segundosEh, então aqui como como uma escolha deliberada da gente que que tá montando a a competição, a gente escolheu um
1:42:211 hora, 42 minutos e 21 segundosconjunto aqui de 10 variáveis apenas atmosféricas, que é o conjunto de dados que a gente vai que a gente vai ã
1:42:291 hora, 42 minutos e 29 segundosapresentar para vocês no Kegle e vocês vão poder baixar. Nada impede de que vocês eh procurem e eventualmente façam
1:42:391 hora, 42 minutos e 39 segundoso download de outras de outras variáveis e tanto atmosferas quanto de temperatura
1:42:461 hora, 42 minutos e 46 segundosdo mar e e dados de eh de continente como evaporanspiração e essas coisas.
1:42:531 hora, 42 minutos e 53 segundosMas eh a avaliação dos dos das soluções de vocês, ela não vai ser
1:43:001 hora e 43 minutostotalmente automatizadas. Obviamente que vai ter o ranking ali que vai calculando as métricas, mas eh o a gente vai olhar,
1:43:091 hora, 43 minutos e 9 segundosvai fazer a verificação eh dos códigos também. Então, eh, se caso vocês façam o download de outras variáveis que não
1:43:181 hora, 43 minutos e 18 segundosestão nesse conjunto que a gente tá que a gente vai disponibilizar de vocês, a gente pede que vocês documentem muito bem essas coisas para que a gente possa ã de certa forma fazer alguma auditoria.
1:43:291 hora, 43 minutos e 29 segundosAuditoria é uma palavra forte, né, mas que a gente consiga conferir a a solução de vocês, tá? Então, a gente e a gente
1:43:371 hora, 43 minutos e 37 segundosnão quer restringir eh ninguém a esse tipo de coisa, né? tanto pelos conhecimentos que alguém que as pessoas já podem ter sobre o problema, né,
1:43:461 hora, 43 minutos e 46 segundosquanto capacidade de computação mesmo, né? Mas a princípio a gente tá dando aqui um conjunto eh um conjunto de eh de
1:43:551 hora, 43 minutos e 55 segundosvariáveis que vão aí cobertura cobertura de nuvens, umidade, componentes iv do vento, pressão de superfície,
1:44:021 hora, 44 minutos e 2 segundostemperatura, geopotencial, eh umidade.
1:44:061 hora, 44 minutos e 6 segundosA gente acredita que com essas eh com essas variáveis vocês já consigam chegar
1:44:141 hora, 44 minutos e 14 segundosnuma numa solução. Mas como eu comentei, vocês têm essa essa possibilidade também. Muito bem.
1:44:221 hora, 44 minutos e 22 segundosÉ, então falando um pouco aqui mais dos dados, né? Então a gente tá a gente vai dar essas variáveis para vocês junto com
1:44:291 hora, 44 minutos e 29 segundosa com a precipitação, né? Que é o dado, desculpem, que é o dado alvo, né? Numa
1:44:361 hora, 44 minutos e 36 segundosresolução de 0,25. Então a gente tem uma grade ali de quase 79.000 pontos, né?
1:44:421 hora, 44 minutos e 42 segundosEh, e nessa nessa série de 1940 até 2024.
1:44:461 hora, 44 minutos e 46 segundoseh com mais ou menos ali 1000 amostras eh nessa série completa, né? E aqui da onde é que eu tirei esse 78 por e quase
1:44:541 hora, 44 minutos e 54 segundos79.000 pontos, né? É que a gente tem 300 e 301 pontos de latitude contra 261
1:45:011 hora, 45 minutos e 1 segundopontos de longitude, né? Então se a gente fosse pensar que isso era uma que isso é uma imagem, né? Vamos pensar que seja uma imagem multiespectral aí que na
1:45:101 hora, 45 minutos e 10 segundosque são as nossas variáveis, né? a gente tem eh 301 pixels de largura contra 261
1:45:201 hora, 45 minutos e 20 segundosde altura, né? Então essa é a dimensão eh das eh das imagens. E vamos
1:45:271 hora, 45 minutos e 27 segundosusar um termo talvez não tão correto, né? Mas eh esses cubos cubos de dados, talvez seja o termo mais correto, ele tem essas dimensões, né? Muito bem.
1:45:401 hora, 45 minutos e 40 segundosEh, então, como eu falei para vocês, a gente vai submeter essas coisas no Kegle, né? A gente vai ter um agora na sequência, eu vou eu vou mostrar para
1:45:481 hora, 45 minutos e 48 segundosvocês. A gente tem um um arquivo ali eh padrão que vocês vão
1:45:551 hora, 45 minutos e 55 segundossubmeter as suas soluções naquele formato, né? A métrica que a gente vai utilizar, então, como a gente vai est trabalhando com a previsão absoluta, vai ser o RMSE.
1:46:061 hora, 46 minutos e 6 segundosE a gente vai ter esse leaderboard lá que vai tá sendo calculado sobre o ano de 2023. E vocês vão ver como é que tá o andamento, o andamento das soluções ali e dos times por esse leaderboard, né?
1:46:191 hora, 46 minutos e 19 segundosEh, como eh ali no Kegle, no Kegle, desculpem, no Slack já tem o pessoal
1:46:271 hora, 46 minutos e 27 segundosinteragindo para fazer as suas as suas próprias equipes, né? A gente estimula, quem não tem equipe formada ainda, que
1:46:341 hora, 46 minutos e 34 segundosmande mensagem ali, né? E caso queira fazer em equipe, né? A gente tá ã a gente tá permitindo quatro participantes
1:46:431 hora, 46 minutos e 43 segundospor equipes, né? As submissões, vocês vão ter um limite de submissões por dia, três envios por dia por cada equipe, né?
1:46:511 hora, 46 minutos e 51 segundosComo eu comentei para vocês, eh, vocês podem utilizar dados externos, outros outros, eh, conjuntos de reanálise,
1:47:001 hora e 47 minutosnovas variáveis, dados de superfície eh de temperatura do mar, o que vocês acharem eh interessante. Mas essas
1:47:081 hora, 47 minutos e 8 segundoscoisas, como eu comentei, como a gente vai verificar essas soluções de vocês além do do ranking ali, né, é bom que
1:47:161 hora, 47 minutos e 16 segundosessas coisas estejam eh estejam eh bem documentadas.
1:47:211 hora, 47 minutos e 21 segundospara pra gente poder verificar, né? E eh como a gente tem eh pessoas de vários backgrounds aqui de eh de formação, né,
1:47:291 hora, 47 minutos e 29 segundosa gente não tem nenhuma restrição com utilização de ferramentas de geração de código aí para para vocês
1:47:371 hora, 47 minutos e 37 segundos[limpando a garganta] eh utilizarem eh no desenvolvimento. Acho que a única coisa que o bom senso diz é que não vale
1:47:441 hora, 47 minutos e 44 segundoscopiar o código do outro, né? Ou seja, copiar eh soluções de outras equipes, né? Mas utilizar essas ferramentas, a
1:47:511 hora, 47 minutos e 51 segundosferramenta tá aí, a gente a gente utiliza se utiliza delas, né? Muito bem.
1:47:571 hora, 47 minutos e 57 segundosEh, aqui tá um formate. Eu eu vou passar esse esse arquivo para vocês depois ali, né? Mas hã mas o arquivo o arquivo final
1:48:071 hora, 48 minutos e 7 segundosque vocês vão submeter ali, que vão ter mais de 1 milhão de linhas ali, por causa que vai ser uma linha para cada
1:48:151 hora, 48 minutos e 15 segundospara cada ã ponto de latitude e longitude, né? pra gente poder calcular o erro. E ele vai ter esse formatinho aqui, né? Então ele vai ter um ID que
1:48:241 hora, 48 minutos e 24 segundosvai ter o ano, underline, o mês, underline, a latitude e longitude do ponto, separado por uma vírgula e a
1:48:331 hora, 48 minutos e 33 segundosprevisão do modelo para vocês naquele naquele naquele ponto, né? Então, e aí vocês vão ter cada isso [roncando] não
1:48:421 hora, 48 minutos e 42 segundosé, eu admito para vocês que não é a melhor forma de se fazer, mas é como a plataforma ali do Kegle eh, dá uma restringida, né? Então, foi a forma como
1:48:511 hora, 48 minutos e 51 segundosa gente como a gente eh conseguiu ali de de montar o arquivo, né, para vocês poderem para vocês poderem submeter.
1:49:011 hora, 49 minutos e 1 segundoEntão, é isso, né? é o identificador que tem a data e a coordenada do ponto separado por vírgula e o valor que de
1:49:101 hora, 49 minutos e 10 segundosprevisão do modelo de vocês para aquele ponto, né? E aí a gente tendo o dado o dado referência aqui, calcula as métricas e faz e faz aquele ranking.
1:49:221 hora, 49 minutos e 22 segundosEh, então agora eu vou mostrar para vocês o Kegle, né? Como eu falei, a gente vai ter essas submissões por arquivo, vai ter um um fórum de dúvidas
1:49:301 hora, 49 minutos e 30 segundoslá, mas que que vocês podem postar lá, mas a gente recomenda que vocês usem que
1:49:351 hora, 49 minutos e 35 segundosvocês utilizem o o Slack para tirar as dúvidas, né? A gente é mais fácil de
1:49:421 hora, 49 minutos e 42 segundosmonitorar e a gente recomenda que vocês façam o desenvolvimento de vocês pelo Kegle também, né? Então o Kegle ele tem
1:49:501 hora, 49 minutos e 50 segundosuma estrutura de Júpiter Notebook ali que vocês podem utilizar. Ele dá umas GPUs eh de graça para vocês usarem, ou
1:49:581 hora, 49 minutos e 58 segundosseja, tem 30 horas de de GPU eh por semana e vocês podem tem que fazer um
1:50:051 hora, 50 minutos e 5 segundoscadastro ali sobre sobre ã colocar o número de telefone, mas vocês conseguem utilizar aquelas as
1:50:131 hora, 50 minutos e 13 segundosGPUs do Kegle ali por 12 horas ininterruptas e 30 horas na semana no total. Vocês só me dão uma licencinha que eu preciso botar o notebook para carregar aqui. Só um segundo, gente.
1:50:421 hora, 50 minutos e 42 segundosAh, muito bem. Vocês vocês desculpem.
1:50:441 hora, 50 minutos e 44 segundosEh, bom, então, como eu falei, né, vocês conseguem fazendo, eh, esse cadastro no Kegle, vocês conseguem utilizar a as
1:50:531 hora, 50 minutos e 53 segundosGPUs da plataforma. Então, eu acho que é algo que é algo interessante também se fazer, né?
1:51:001 hora e 51 minutosAh, eh, qualquer dúvida que vocês tiverem durante esses 10 dias, vocês podem falar comigo. Eu sou o Jerônimo, né, o Igor, que participou aqui com a
1:51:081 hora, 51 minutos e 8 segundosgente. A Cind também, ela, infelizmente, não conseguiu participar com a gente hoje, mas ela tá ali no, ela é a nossa meteorologista aqui do time, né? Então,
1:51:161 hora, 51 minutos e 16 segundosqual eh qualquer coisa vocês podem eh conversar com ela, manda mensagem ali no
1:51:241 hora, 51 minutos e 24 segundosna parte de dúvidas do Slack, né, ou pelo Kegle também. Mas a gente recomenda
1:51:311 hora, 51 minutos e 31 segundosno eh fortemente pelo pelo Slack, porque a gente consegue monitorar melhor monitorar melhor a as dúvidas de vocês.
1:51:401 hora, 51 minutos e 40 segundosMuito bem, gente. Eh, eu acho que da parte dos slides era isso. Eu vou mostrar para vocês aqui rapidinho a plataforma. Ela ainda não tá pública,
1:51:491 hora, 51 minutos e 49 segundostá? Ela a gente vai a gente vai disponibilizar ela para vocês agora na sequência, mas deixa eu parar o meu compartilhamento aqui e mostrar para vocês o que tem ali também.
1:52:031 hora, 52 minutos e 3 segundosEntão aqui aqui
1:52:111 hora, 52 minutos e 11 segundoseu acredito que vocês tenham voltado a ver a minha a minha tela, né? Me ajuda qualquer coisa aíor.
1:52:181 hora, 52 minutos e 18 segundosHum. Eh, só antes de Prisle que talvez tenha uma dúvida no chat sobre, apesar que eu acho que você vai
1:52:261 hora, 52 minutos e 26 segundoslevela agora, mas eh a previsão, a do Márcio perguntou se a previsão é para mês seguinte e por dia também.
1:52:351 hora, 52 minutos e 35 segundosAh, tá bom. Eh, obrigado. Eh, obrigado, Igor. Obrigado pela pergunta, Márcio.
1:52:401 hora, 52 minutos e 40 segundosMárcio, a a previsão ela vai ser pro mês seguinte, ou seja, a gente vai prever ã a precipitação a média do próximo mês,
1:52:491 hora, 52 minutos e 49 segundosné? Então, não tem não envolve nada de previsão diária, né?
1:52:551 hora, 52 minutos e 55 segundosEntão, tu tem o estado, essas [roncando] variáveis que a gente vai dar para vocês ali, eh, são uma média, né, mensal daquelas variáveis atmosféricas. E a
1:53:031 hora, 53 minutos e 3 segundosgente vai tentar prever o a média do próximo mês.
1:53:101 hora, 53 minutos e 10 segundosEh, próximo mês, não, não, o próximo, quer dizer, outubro está nessas eh está nessas ã naquele conjunto ali,
1:53:201 hora, 53 minutos e 20 segundosou seja, tu vai o modelo vai receber receber como entrada os dados de janeiro e vai prever fevereiro. Depois vai
1:53:281 hora, 53 minutos e 28 segundosreceber os dados de fevereiro e vai prever março. E aí a gente, vocês vão fazer previsões aí para para o que vai
1:53:361 hora, 53 minutos e 36 segundoscontar ali pr pro pro vencimento da da competição vai ser o ano de 2024. Mas como eu falei, né, vocês vão ver o
1:53:441 hora, 53 minutos e 44 segundosleaderboard público ali para 2023, mas o que vai definir vai ser 2024,
1:53:521 hora, 53 minutos e 52 segundoscerto, gente? Eh, ficou ficou esclarecido. Vocês podem vocês podem mandar perguntas, outras perguntas aí no
1:54:011 hora, 54 minutos e 1 segundochat também, tá bom? Eh, então aqui no Kegle, tá? Eh, a gente você aqui tem algumas coisas que vocês não vão ver
1:54:091 hora, 54 minutos e 9 segundosporque eh a gente não quando tiver, né, público, essas coisas vão tá. Mas aqui
1:54:161 hora, 54 minutos e 16 segundostem toda uma descrição aqui, ó, da das avaliações, o exemplo, o exemplo de eh
1:54:241 hora, 54 minutos e 24 segundosde arquivo que vocês têm que submeter, o como a gente vai avaliar, eh, a descrição do problema, né? Os dados
1:54:311 hora, 54 minutos e 31 segundosestão aqui, então, a gente dá uma breve descrição dos dados, eh, como que vocês leem ele, né? O os dados. Então, eh,
1:54:411 hora, 54 minutos e 41 segundosaqui mais para baixo, como eu falei, a gente vai dar, ã, a gente vai dar nove variáveis atmosféricas para vocês e elas
1:54:491 hora, 54 minutos e 49 segundosestão salvos nesses formato ponto e netd. Ou seja, para cada uma,
1:54:571 hora, 54 minutos e 57 segundoscada uma variável dessas aqui, ela tá salva em um arquivo, vocês precisam, né, de alguma forma juntar essas coisas,
1:55:051 hora, 55 minutos e 5 segundosné, para para conseguir dar pro modelo de previsão de vocês, né? Então, ainda [roncando] tem uma um e vocês precisam,
1:55:151 hora, 55 minutos e 15 segundosné, ler esses dados e processar essas coisas, né, eh, e vocês podem entrar em contato com a gente, obviamente, para
1:55:241 hora, 55 minutos e 24 segundosfazer a para fazer a caso alguém tenha alguma dúvida, né? E a previsão de vocês vai ter essa cara aqui, né? Ou seja, então aqui tá o mapa, o nosso domínio.
1:55:331 hora, 55 minutos e 33 segundosEh, e aí aqui a gente vai ter a precipitação, né, em milímetros por dia, né, ou seja, a média de milímetros por
1:55:391 hora, 55 minutos e 39 segundosdia eh sobre o território da da América do Sul. Aqui tem essa parte de código
1:55:471 hora, 55 minutos e 47 segundosque vocês podem ir colocando o código de vocês. E ele tem um um sisteminha de versionamento que é muito simples, mas
1:55:541 hora, 55 minutos e 54 segundostem, né? Vocês podem ir guardando essas coisas.
1:55:571 hora, 55 minutos e 57 segundos[roncando]
1:55:571 hora, 55 minutos e 57 segundosCaso alguém queira você não poder salvar os próprios modelos. A aba de discussões que como eu falei, né, tem aqui também,
1:56:051 hora, 56 minutos e 5 segundosmas a gente a gente espera que vocês usem o Slack, o ranking público que vai que vai tá sobre o ano de 2023.
1:56:161 hora, 56 minutos e 16 segundosE aqui um pouco mais das regras que a gente que a gente comentou que eu acho que eh acho que tudo já foi.
1:56:231 hora, 56 minutos e 23 segundosJôimo, segundo. Eh, foi sim.
1:56:261 hora, 56 minutos e 26 segundosAh, a tela tá fixa no overview aí pra gente. Ah, [limpando a garganta] desculpe.
1:56:301 hora, 56 minutos e 30 segundosMuito bem. Eu tava passando aqui e vocês não estavam vendo. Deixa eu eh pensei que estava dando um panorama
1:56:391 hora, 56 minutos e 39 segundosgeral das aulas ali. Eu não, eu vou, não tem problema. Eu vou eu vou compartilhar a minha a minha tela
1:56:461 hora, 56 minutos e 46 segundosinteira aqui. Vocês podem e vocês podem eh desculpa, só um momentinho que o meu
1:56:541 hora, 56 minutos e 54 segundoscarregador desconectou de novo aqui. Só um segundo.
1:57:161 hora, 57 minutos e 16 segundosAí, certinho. Desculpem, pessoal. Eh, então, eh, bom, eu tava, eu tinha colocado aqui no overview, né? Eh, mas
1:57:251 hora, 57 minutos e 25 segundosaqui então tem os dados, né, como eu tinha falado para você, só voltando aqui tem um exemplinho de como vocês leem eles, né? Eh, como eu falei, cada uma
1:57:341 hora, 57 minutos e 34 segundosdaquelas nove variáveis que a gente que a gente vai disponibilizar, elas são salvos em arquivos separados aqui.
1:57:411 hora, 57 minutos e 41 segundosEntão, vocês podem podem eh ler elas desse jeito que tem um exemplo como faz, né? vocês precisam, enfim, juntar essas
1:57:491 hora, 57 minutos e 49 segundoscoisas e e, enfim, colocar no formato certo do
1:57:561 hora, 57 minutos e 56 segundosmodelo para vocês, né, de de vocês. E essa daqui é a cara da previsão que a gente vai que a gente vai fazer, né, ou seja, a precipitação em milímetros por
1:58:041 hora, 58 minutos e 4 segundosdia pro próximo mês, né? Então, é isso aqui que vocês são mapas desse tipo que vocês vão ficar vendo o resto da semana agora, né, gente?
1:58:151 hora, 58 minutos e 15 segundos[roncando]
1:58:151 hora, 58 minutos e 15 segundosEh, aqui eu tinha falado aba de códigos que vocês podem ir colocando Júpiter Notebooks do Kegle para vocês aqui, né?
1:58:231 hora, 58 minutos e 23 segundosEh, vocês podem ir fazendo, salvando os checkpoints dos modelos de vocês. Aa de discussão que eu comentei que a gente
1:58:301 hora, 58 minutos e 30 segundosprefere que vocês usem no Slack, mas se mandarem aqui, a gente vai responder também, não tem problema.
1:58:371 hora, 58 minutos e 37 segundoseh o ranking que vai ser calculado sobre o ano de 2023, como eu tinha comentado com vocês.
1:58:431 hora, 58 minutos e 43 segundosEh, aqui uma página de regras que já foram foram as coisas que basicamente eu falei agora na na apresentação, mas
1:58:531 hora, 58 minutos e 53 segundosvocês podem olhar, ler com um pouquinho mais com um pouquinho mais de calma. Tem algumas coisas específicas do Kegle aqui também que não nos interessam muito, tá?
1:59:021 hora, 59 minutos e 2 segundosMas vocês podem vocês podem acessar essa página também.
1:59:071 hora, 59 minutos e 7 segundosEh, e gente, eh, basicamente é isso, assim, a gente vai a gente vai disponibilizar para vocês essa página
1:59:161 hora, 59 minutos e 16 segundosaté o final do dia agora, né? Eh, e aí eu vou mandar o link para vocês ali no Slack e vocês já podem ir eh cadastrando
1:59:251 hora, 59 minutos e 25 segundosas equipes e a partir de hoje já ir pensando no desenvolvimento de vocês, tá
1:59:321 hora, 59 minutos e 32 segundosbom? Eh, então eu acho que assim, eu acho que é isso e a gente fica a disp à
1:59:401 hora, 59 minutos e 40 segundosdisposição de vocês aí para para tirar as dúvidas, caso alguém tenha aí. Eu acho que essa é a é agora a hora, né?
1:59:491 hora, 59 minutos e 49 segundosA Luise perguntou: "Podemos então submeter, avaliar com dado de 2023, melhorar e submeter de novo até o fim do prazo?" Sim, Luiz, vocês po, cada equipe
1:59:581 hora, 59 minutos e 58 segundospode fazer até o dia do até o dia de até o dia do do término da competição, três
2:00:052 horas e 5 segundossubmissões por dia, tá? Eh, é aquilo que a gente comentou, né? Às vezes, eh,
2:00:122 horas e 12 segundosmelhorar 2023 não significa que a gente vai hã melhorar 2024, né? Então, até por
2:00:192 horas e 19 segundosisso a gente dá uma a gente dá uma uma restrição ali de envios por dia, né?
2:00:242 horas e 24 segundosPorque a gente pode, vocês podem estar sub eh sobreajustando o modelo de vocês, aquilo que o Carlos havia comentado, né?
2:00:322 horas e 32 segundosMas sim, sim, vocês podem eh é justamente para isso, né? Para vocês terem tirando uma febre de como tá indo o modelo de vocês, né? O modelo bom, né?
2:00:412 horas e 41 segundosÉ aquele que vai ter um um desempenho bom em ambos os anos, né? Em todos os anos, né? De certa forma. Mas, eh,
2:00:502 horas e 50 segundosentão, eh, para resumir, sim, vocês podem fazer mais de uma submissão.
2:01:022 horas, 1 minuto e 2 segundosEh, mais alguma dúvida, gente? A gente tá à disposição de vocês aqui para vocês, eh,
2:01:092 horas, 1 minuto e 9 segundosclaro, né? a gente vai ter bastante interações no nos próximos dias aí até até o o término da competição, né?
2:01:212 horas, 1 minuto e 21 segundosAcho que no chat mais ninguém ali, né? O Igor,
2:01:332 horas, 1 minuto e 33 segundoso Márcio mandou mesmo. Ah, sim.
2:01:362 horas, 1 minuto e 36 segundosNão, reenviar não, Márcio, porque a gente ainda nem a gente ainda nem disponibilizou para vocês até o final do dia a gente vai
2:01:452 horas, 1 minuto e 45 segundoscompartilhar ali, tá? E e aí vocês vão poder ter acesso e já fazer a inscrição,
2:01:532 horas, 1 minuto e 53 segundosné? Todos todos têm que fazer a a sua inscrição ali no no do seu time, né?
2:02:002 horas e 2 minutosEntão, a gente ainda vai deixar um um tempinho para vocês indo para vocês eh
2:02:082 horas, 2 minutos e 8 segundosir ajustando os times de vocês, né? E mas a gente hoje já vai tá no ar e a gente recomenda fortemente que quem vai
2:02:172 horas, 2 minutos e 17 segundosentrar em time já entre hoje, né? E quem vai fazer sozinho que também já se inscreva. E aí para, né, como eu
2:02:252 horas, 2 minutos e 25 segundoscomentei, o o tempo é um pouco curto, então não é bom perder tempo muito com
2:02:322 horas, 2 minutos e 32 segundosessas coisas, não é bom para vocês poderem ter bastante tempo para desenvolver e testar
2:02:392 horas, 2 minutos e 39 segundosideias mais por isso, né? Nada nada além disso, né? para vocês terem o tempo de de de desenvolverem bem a solução.
2:02:542 horas, 2 minutos e 54 segundosEh, bom, gente, eu acho se ninguém tem mais, se alguém tiver mais alguma dúvida,
2:03:022 horas, 3 minutos e 2 segundosvocês podem perguntar, mas se ninguém eh se ninguém tiver mais nenhuma pergunta,
2:03:092 horas, 3 minutos e 9 segundoseh, por hora, eu acho que a gente libera vocês, né, Igor? Acho que agora é a gente a gente vai dar mais um tempinho
2:03:162 horas, 3 minutos e 16 segundospara vocês ali irem se combinando nos times até o final do dia aí. Eh, e aí eu vou marcar todo mundo ali naquele
2:03:252 horas, 3 minutos e 25 segundosgeneral do do Slack, né? Todo mundo vai receber a notificação. E aí é mão na
2:03:312 horas, 3 minutos e 31 segundosmassa, não tem mais não tem mais muito o que se falar. Tá bom? Eh, desejamos
2:03:412 horas, 3 minutos e 41 segundosboa sorte a todos e pedimos, eh, antes, só para terminar, né, pedimos encarecidamente que quem não se
2:03:472 horas, 3 minutos e 47 segundosinscreveu ainda no WordP, por favor, se inscreva. É o e essa esse esforço aqui
2:03:542 horas, 3 minutos e 54 segundosque a gente tá fazendo eh tá nesse contexto do workshop da nossa pós aqui, né? E
2:04:012 horas, 4 minutos e 1 segundotem tem dá para participar online, né? é baratinho, eh, e vocês ajudam a gente
2:04:092 horas, 4 minutos e 9 segundosmuito, muito mesmo, né, para para divulgar que o que a gente faz dentro do do IMP, do Instituto. Eu acho que para
2:04:182 horas, 4 minutos e 18 segundoseh é de interesse da sociedade toda, né, o que a gente faz aqui dentro. Então, eh, participar de eventos como esse, né,
2:04:262 horas, 4 minutos e 26 segundosde de competições como essa e de eventos como Workup ajudam a gente divulgar o que tá sendo feito aqui no no Instituto.
2:04:332 horas, 4 minutos e 33 segundosEntão, eh, a gente pede que quem puder, quem conseguir, por favor, se inscreva, tá bom, pessoal?
2:04:412 horas, 4 minutos e 41 segundosEntão eu acho que é isso. Acaba, quando fechamos 2 horas aqui de papo, a gente se despede. Eh, desejando uma boa sorte
2:04:502 horas, 4 minutos e 50 segundosa todos e espero que tenham gostado. A gente vem trabalhando nisso já há algum tempo. É a primeira vez que a gente tá fazendo, então a gente tá aprendendo a
