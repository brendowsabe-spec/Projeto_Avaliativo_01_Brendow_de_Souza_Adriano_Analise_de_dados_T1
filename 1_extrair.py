#Download + leitura dos CSVs + carga na camada Raw.

#● Fase 1 - Extração e camada Raw (1_extrair.py): baixar o arquivo .zip do Google Drive, ler os 4 CSVs em blocos 
# e carregar nas tabelas Raw sem alterar o conteúdo. O processo deve ser idempotente (TRUNCATE antes de carregar) 
# e resiliente (try/except). Este zip já está transformado para trabalharmos com 6 meses do ano 2025.

#import pandas as pd
#encoding="latin-1"

import pandas as pd

from banco import obter_engine

try:

    print("Conectando ao banco...")

    engine = obter_engine()

    print("Lendo CSV...")

    df = pd.read_csv(
        "2025_Viagem.csv",
        sep=";",
        encoding="latin-1"
    )
    #print(df.columns.tolist())
    
    df.columns = [
    "id_viagem",
    "num_proposta",
    "situacao",
    "viagem_urgente",
    "justificativa_urgencia",
    "cod_orgao_superior",
    "nome_orgao_superior",
    "cod_orgao_solicitante",
    "nome_orgao_solicitante",
    "cpf_viajante",
    "nome_viajante",
    "cargo",
    "funcao",
    "descricao_funcao",
    "data_inicio",
    "data_fim",
    "destinos",
    "motivo",
    "valor_diarias",
    "valor_passagens",
    "valor_devolucao",
    "valor_outros_gastos"
]
    #print(df.columns.tolist())

    print(f"Linhas encontradas: {len(df)}")

    print("Limpando tabela RAW...")

    with engine.begin() as conn:
        conn.exec_driver_sql(
            "TRUNCATE TABLE raw_viagem;"
        )

    print("Inserindo dados...")

    df.to_sql(
        "raw_viagem",
        engine,
        if_exists="append",
        index=False
    )

    print("Carga concluída com sucesso!")

except Exception as erro:

    print("Erro:")
    print(erro)