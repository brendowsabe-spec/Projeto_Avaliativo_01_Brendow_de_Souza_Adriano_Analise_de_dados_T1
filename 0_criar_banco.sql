-- Criar as 8 tabelas (4 Raw + 4 Silver) com PK, FK e constraints

--  Fase 0 - Banco e tabelas (0_criar_banco.sql): criar o database e as 8 tabelas. As 4 tabelas Raw têm todas 
-- as colunas VARCHAR e sem constraints; as 4 tabelas Silver são tipadas e têm PRIMARY KEY, FOREIGN KEY 
-- e mais 2 constraints por tabela (NOT NULL, CHECK e UNIQUE), declaradas dentro do CREATE TABLE.


CREATE TABLE raw_viagem (

    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    situacao VARCHAR(100),
    viagem_urgente VARCHAR(20),
    justificativa_urgencia VARCHAR(500),
    cod_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    cod_orgao_solicitante VARCHAR(50),
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(20),
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    funcao VARCHAR(255),
    descricao_funcao VARCHAR(255),
    data_inicio VARCHAR(20),
    data_fim VARCHAR(20),
    destinos VARCHAR(1000),
    motivo VARCHAR(4000),
    valor_diarias VARCHAR(50),
    valor_passagens VARCHAR(50),
    valor_devolucao VARCHAR(50),
    valor_outros_gastos VARCHAR(50)

);

CREATE TABLE raw_pagamento (

    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    cod_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    cod_orgao_pagador VARCHAR(50),
    nome_orgao_pagador VARCHAR(255),
    cod_ug_pagadora VARCHAR(50),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(100),
    valor VARCHAR(50)

);

CREATE TABLE raw_passagem (

    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    meio_transporte VARCHAR(100),

    pais_origem_ida VARCHAR(100),
    uf_origem_ida VARCHAR(50),
    cidade_origem_ida VARCHAR(100),

    pais_destino_ida VARCHAR(100),
    uf_destino_ida VARCHAR(50),
    cidade_destino_ida VARCHAR(100),

    pais_origem_volta VARCHAR(100),
    uf_origem_volta VARCHAR(50),
    cidade_origem_volta VARCHAR(100),

    pais_destino_volta VARCHAR(100),
    uf_destino_volta VARCHAR(50),
    cidade_destino_volta VARCHAR(100),

    valor_passagem VARCHAR(50),
    taxa_servico VARCHAR(50),
    data_emissao VARCHAR(50),
    hora_emissao VARCHAR(50)

);

CREATE TABLE raw_trecho (

    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    sequencia_trecho VARCHAR(20),

    origem_data VARCHAR(50),
    origem_pais VARCHAR(100),
    origem_uf VARCHAR(50),
    origem_cidade VARCHAR(100),

    destino_data VARCHAR(50),
    destino_pais VARCHAR(100),
    destino_uf VARCHAR(50),
    destino_cidade VARCHAR(100),

    meio_transporte VARCHAR(100),
    numero_diarias VARCHAR(50),
    missao VARCHAR(20)

);


CREATE TABLE silver_viagem (

    id_viagem VARCHAR(50) PRIMARY KEY,

    num_proposta VARCHAR(50) UNIQUE NOT NULL,

    situacao VARCHAR(100) NOT NULL,

    viagem_urgente BOOLEAN,

    justificativa_urgencia TEXT,

    cod_orgao_superior INTEGER,

    nome_orgao_superior VARCHAR(255) NOT NULL,

    cod_orgao_solicitante INTEGER,

    nome_orgao_solicitante VARCHAR(255),

    cpf_viajante VARCHAR(20),

    nome_viajante VARCHAR(255),

    cargo VARCHAR(255),

    funcao VARCHAR(255),

    descricao_funcao VARCHAR(255),

    data_inicio DATE NOT NULL,

    data_fim DATE NOT NULL,

    destinos TEXT,

    motivo TEXT,

    valor_diarias NUMERIC(12,2) CHECK (valor_diarias >= 0),

    valor_passagens NUMERIC(12,2) CHECK (valor_passagens >= 0),

    valor_devolucao NUMERIC(12,2) CHECK (valor_devolucao >= 0),

    valor_outros_gastos NUMERIC(12,2) CHECK (valor_outros_gastos >= 0)

);

CREATE TABLE silver_pagamento (

    id_pagamento SERIAL PRIMARY KEY,

    id_viagem VARCHAR(50) NOT NULL,

    num_proposta VARCHAR(50) NOT NULL,

    cod_orgao_superior INTEGER,

    nome_orgao_superior VARCHAR(255),

    cod_orgao_pagador INTEGER,

    nome_orgao_pagador VARCHAR(255),

    cod_ug_pagadora INTEGER,

    nome_ug_pagadora VARCHAR(255),

    tipo_pagamento VARCHAR(100) NOT NULL,

    valor NUMERIC(12,2) NOT NULL CHECK (valor >= 0),

    FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem)

);

CREATE TABLE silver_passagem (

    id_passagem SERIAL PRIMARY KEY,

    id_viagem VARCHAR(50) NOT NULL,

    num_proposta VARCHAR(50),

    meio_transporte VARCHAR(100) NOT NULL,

    pais_origem_ida VARCHAR(100),

    uf_origem_ida VARCHAR(10),

    cidade_origem_ida VARCHAR(100),

    pais_destino_ida VARCHAR(100),

    uf_destino_ida VARCHAR(10),

    cidade_destino_ida VARCHAR(100),

    valor_passagem NUMERIC(12,2) CHECK (valor_passagem >= 0),

    taxa_servico NUMERIC(12,2) CHECK (taxa_servico >= 0),

    data_emissao DATE,

    hora_emissao TIME,

    FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem)

);

CREATE TABLE silver_trecho (

    id_trecho SERIAL PRIMARY KEY,

    id_viagem VARCHAR(50) NOT NULL,

    num_proposta VARCHAR(50),

    sequencia_trecho INTEGER NOT NULL,

    origem_data DATE,

    origem_pais VARCHAR(100),

    origem_uf VARCHAR(10),

    origem_cidade VARCHAR(100),

    destino_data DATE,

    destino_pais VARCHAR(100),

    destino_uf VARCHAR(10),

    destino_cidade VARCHAR(100),

    meio_transporte VARCHAR(100),

    numero_diarias NUMERIC(10,2)
        CHECK (numero_diarias >= 0),

    missao BOOLEAN,

    UNIQUE (id_viagem, sequencia_trecho),

    FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem)

);