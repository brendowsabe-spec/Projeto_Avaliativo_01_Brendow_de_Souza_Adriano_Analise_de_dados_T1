Olá!

Seja bem-vindo(a) à minha atividade para o curso de análise de dados do SCTEC.

Me chamo brendow e estou iniciando nesta área, ainda tenho muito a aprender, o que eu pude inclui nesta atividade para demonstrar um pouco do que aprendi e também coisas que ainda preciso melhorar!

Sobre o Projeto: Pipeline de dados ETL utilizando Arquitetura Medallion (Raw, Silver, Gold) para o Portal da Transparência (Ano 2025).

documentar a sua solução
- Solução iniciada com a criação de todos os arquivos necessários para iniciar, python, postgreSQL, arquivos como .env, e todas as modulações necessárias que se encontram no requirements.txt.
demonstrar as técnicas e linguagens utilizadas
- Muito utilizado Python e PostgreSQL para resolução
escopo do projeto
- Projeto dedicado a encontrar dados em arquivos CSV de viagens aéreas, que demonstra quantidade total de voos de uma rede de linhas aéreas e seus respectivos balanços, quantitativos, dados das pessoas que frequentam
como o usuário pode executar o seu sistema.
- Pode ser executado via VSCode com Python e SQL

Algumas dicas interessantes para utilizar na criação do seu portfólio são:
● Descrever qual o problema ele resolve;
- Organização e tratamento de dados de viagens do Portal da Transparência de 2025 para apoio à tomada de decisão.
● Descrever quais técnicas e tecnologias utilizadas. Aqui você também pode inserir alguma imagem ou diagrama para melhor entendimento;
- Desenvolvi técnicas aprendidas em aula sobre Análise de dados com python e SQL, colocando em foco encontrar os dados sujos e os guardar em um banco, depois os limpar para chegar mais proximo dos dados reais (silver) e por ultimo fazer analise mais aprofundada de cada dado (gold)
* Portanto utilizado ao fim: Python (Pandas, SQLAlchemy), PostgreSQL e Jupyter Notebook.
● Descrever como executar;
Pode ser executado pelo terminal do VS Code com python, executando na ordem: 0_criar_banco.sql, depois 1_extrair.py, em seguida 2_transformar.py, e por fim explorar o 3_analise.ipynb.
● Descrever quais melhorias podem ser aplicadas;
- Durante o carregamento dos dados para a camada Raw, foram identificadas colunas com textos superiores ao tamanho definido inicialmente. Para evitar perda de informação, alguns campos foram alterados para o tipo TEXT, permitindo armazenar os dados originais sem truncamento.
● Descrever as conclusões e os insights a partir dos gráfi cos e análise de base.