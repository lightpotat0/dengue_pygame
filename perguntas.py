import random
escolhida = 0

def reescolher_pergunta():
	global escolhida
	escolhida = random.randint(0, len(PERGUNTAS) - 1)

def get_pergunta():
	return PERGUNTAS[escolhida]

PERGUNTAS = [("O que é a dengue?",
"Uma infecção bacteriana transmitida pela água contaminada",
"Uma doença viral transmitida pelo mosquito Aedes aegypti",
"Uma doença causada por parasitas transmitidos pelo ar",
"Uma infecção viral transmitida pelo contato com pessoas infectadas", 1),
("Qual é o principal vetor de transmissão da dengue?",
"Mosquito Anopheles",
"Mosquito Aedes aegypti",
"Carrapato estrela",
"Mosca doméstica", 1),
("Quais são os principais sintomas da dengue?",
"Febre alta, dor no corpo, dor de cabeça e manchas vermelhas na pele",
"Dificuldade para respirar, tosse e dores nas articulações",
"Vômito, diarreia e dor de garganta",
"Febre baixa, coriza e espirros", 0),
("Qual é o tratamento mais indicado para casos de dengue?",
"Uso de antibióticos",
"Hidratação, repouso e controle da febre",
"Vacinação durante a doença",
"Cirurgia para remover o mosquito infectado", 1),
("Como é possível prevenir a proliferação do mosquito transmissor da dengue?",
"Deixando água parada em locais abertos",
"Utilizando redes de proteção e repelentes",
"Aplicando veneno nas plantas",
"Guardando lixo em locais fechados e sombreados", 1),
("Qual medida deve ser adotada para evitar criadouros do mosquito Aedes aegypti?",
"Manter garrafas e recipientes abertos",
"Armazenar água sem tampas",
"Eliminar a água parada de pneus, vasos e caixas d'água",
"Deixar piscinas descobertas", 2),
("Qual é a principal estratégia de combate ao mosquito transmissor da dengue?",
"Uso de inseticidas em áreas urbanas",
"Aplicação de fungicidas em plantas",
"Vacinação em massa contra o vírus da dengue",
"Uso de máscaras faciais em áreas afetadas", 0),
("Em qual das seguintes situações a pessoa deve procurar atendimento médico com urgência ao contrair dengue?",
"Quando apresenta apenas febre baixa",
"Quando sente dor de cabeça leve",
"Quando apresenta sinais de sangramento ou dificuldade para respirar",
"Quando há coceira leve nas pernas", 2),
("Qual é a forma mais eficaz de evitar a contaminação pela dengue?",
"Não se aproximar de pessoas contaminadas",
"Tomar antibióticos preventivos",
"Evitar a picada do mosquito através do uso de repelentes e roupas longas",
"Tomar vacinas disponíveis para todas as idades", 2),
("Quem corre mais risco de complicações graves ao contrair dengue?",
"Crianças pequenas, idosos e pessoas com doenças crônicas",
"Pessoas que moram em áreas rurais",
"Jovens saudáveis entre 18 e 25 anos",
"Pessoas que tomam vitaminas regularmente", 0),
("O que o mosquito Aedes aegypti precisa para se reproduzir?",
"Água corrente",
"Água parada",
"Alimentos contaminados",
"Folhas secas", 1),
("Em quais locais públicos o mosquito da dengue pode se reproduzir?",
"Lojas de roupas",
"Parques com água parada em fontes",
"Cinemas",
"Academias de ginástica", 1),
("Qual das opções abaixo ajuda a prevenir a dengue?",
"Deixar garrafas viradas para baixo",
"Colocar plantas dentro de casa",
"Usar perfumes fortes",
"Evitar sair ao sol", 0),
("O mosquito que transmite a dengue é mais ativo em qual período do dia?",
"Durante a noite",
"No amanhecer e entardecer",
"Ao meio-dia",
"Somente à tarde", 1),
("Qual desses itens pode se tornar um criadouro do mosquito da dengue?",
"Caixas de papelão",
"Pneu velho com água acumulada",
"Tapetes",
"Móveis de madeira", 1),
("Em áreas urbanas, quais locais são os principais focos de reprodução do Aedes aegypti?",
"Lagos naturais",
"Piscinas com cloro",
"Vasos de plantas, pneus e calhas",
"Fontes de água potável", 2),
("O mosquito Aedes aegypti também pode transmitir qual dessas doenças?",
"Tuberculose",
"Zika vírus",
"Gripe",
"Hepatite", 1),
("A transmissão da dengue pode ocorrer em qualquer estação do ano, mas é mais comum em qual período?",
"Inverno",
"Verão",
"Outono",
"Primavera", 1),
("Qual é o método mais eficaz para monitorar o índice de infestação de mosquitos em uma área?",
"Contagem de picadas nas pessoas",
"Testes de laboratório",
"Coleta de ovos e larvas em armadilhas",
"Pesquisa nas redes sociais", 2),
("O que deve ser feito com bebedouros de animais para evitar criadouros do mosquito da dengue?",
"Deixar sempre cheios de água",
"Trocar a água diariamente",
"Usar água clorada",
"Cobrir com tampas", 1),
("Por que é importante não usar medicamentos à base de ácido acetilsalicílico (AAS) no tratamento da dengue?",
"Porque aumentam a febre",
"Porque podem causar sangramentos",
"Porque não funcionam contra vírus",
"Porque causam alergias graves", 1),
("Como os mosquitos Aedes aegypti geralmente colocam seus ovos?",
"Apenas em água corrente",
"Somente em rios e lagos",
"Nas bordas de recipientes com água parada",
"Nas folhas das árvores", 2),
("Qual é o nome da fase larval do mosquito Aedes aegypti?",
"Ninfa",
"Lagarta",
"Pupa",
"Larva aquática", 3),
("Qual órgão do corpo humano é mais afetado pela dengue grave?",
"Coração",
"Fígado",
"Cérebro",
"Pulmões", 1),
("O que é a \"ação de bloqueio\" no combate à dengue?",
"Fechamento de áreas afetadas por mosquitos",
"Aplicação de inseticida em uma região específica após a identificação de casos de dengue",
"Bloqueio do trânsito para evitar a disseminação",
"Proibição do uso de água encanada", 1),
("Como os ovos do mosquito Aedes aegypti sobrevivem em períodos sem água?",
"Eles secam e morrem imediatamente",
"Eles ficam em estado de dormência e podem eclodir quando a água retorna",
"Eles se transformam em larvas no ar",
"Eles são levados pelo vento para outro local", 1),
("Qual o nome do teste que identifica rapidamente a presença do vírus da dengue no sangue?",
"Teste de glicose",
"Hemograma",
"Teste rápido NS1",
"Raio-X", 2),
("Qual é o principal fator de risco para uma pessoa desenvolver dengue grave (hemorrágica)?",
"Contato com o mosquito durante a noite",
"Ter tido dengue anteriormente",
"Viver em áreas rurais",
"Praticar atividades ao ar livre", 1),
("O que deve ser feito com pratos de vasos de plantas para evitar a proliferação do Aedes aegypti?",
"Deixar sempre cheios de água",
"Cobrir com areia",
"Trocar a água a cada dois dias",
"Colocar detergente no fundo", 1),
("Além da dengue, qual outra doença é transmitida pelo mosquito Aedes aegypti?",
"Febre amarela",
"Malária",
"Leishmaniose",
"Doença de Chagas", 0),
("O vírus da dengue pode ser transmitido de pessoa para pessoa?",
"Sim, pelo ar",
"Sim, pelo contato direto com a pele",
"Não, apenas pela picada do mosquito",
"Sim, através da água", 2),
("Qual das ações abaixo NÃO ajuda a combater a dengue?",
"Cobrir caixas d'água",
"Deixar pneus ao ar livre",
"Limpar calhas",
"Descartar lixo corretamente", 1),
("Qual o papel da vigilância epidemiológica no controle da dengue?",
"Espalhar larvas de mosquitos em áreas controladas",
"Monitorar e mapear os casos da doença",
"Aplicar vacinas obrigatórias",
"Capturar mosquitos para criar como animais de estimação", 1),
("Quantos dias depois da picada o mosquito infectado pode transmitir o vírus da dengue?",
"Imediatamente",
"Após 2 dias",
"Após 7 a 10 dias",
"Após 1 mês", 2),
("Qual é a principal maneira de o mosquito Aedes aegypti encontrar uma pessoa para picar?",
"Pelo cheiro do perfume",
"Pelo suor e pela respiração",
"Pela luz de lanternas",
"Pelo som da voz humana", 1)]