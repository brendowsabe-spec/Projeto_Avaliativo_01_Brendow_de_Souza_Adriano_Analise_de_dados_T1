import pandas as pd

from banco import obter_engine

engine = obter_engine()

def carregar_csv(arquivo, tabela, colunas):

    try:

        print(f"\nLendo {arquivo}...")

        df = pd.read_csv(
            arquivo,
            sep=";",
            encoding="latin-1"
        )

        df.columns = colunas

        print(f"Linhas encontradas: {len(df)}")

        print(f"Limpando {tabela}...")

        with engine.begin() as conn:
            conn.exec_driver_sql(
                f"TRUNCATE TABLE {tabela};"
            )

        print(f"Inserindo em {tabela}...")

        df.to_sql(
            tabela,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )

        print(f"{tabela} carregada com sucesso!")

    except Exception as erro:

        print(f"Erro em {arquivo}")
        print(erro)


# ==========================
# VIAGEM
# ==========================

# carregar_csv(

#     "2025_Viagem.csv",

#     "raw_viagem",

#     [
#         "id_viagem",
#         "num_proposta",
#         "situacao",
#         "viagem_urgente",
#         "justificativa_urgencia",
#         "cod_orgao_superior",
#         "nome_orgao_superior",
#         "cod_orgao_solicitante",
#         "nome_orgao_solicitante",
#         "cpf_viajante",
#         "nome_viajante",
#         "cargo",
#         "funcao",
#         "descricao_funcao",
#         "data_inicio",
#         "data_fim",
#         "destinos",
#         "motivo",
#         "valor_diarias",
#         "valor_passagens",
#         "valor_devolucao",
#         "valor_outros_gastos"
#     ]
# )

# # ==========================
# # PAGAMENTO
# # ==========================

# carregar_csv(

#     "2025_Pagamento.csv",

#     "raw_pagamento",

#     [
#         "id_viagem",
#         "num_proposta",
#         "cod_orgao_superior",
#         "nome_orgao_superior",
#         "cod_orgao_pagador",
#         "nome_orgao_pagador",
#         "cod_ug_pagadora",
#         "nome_ug_pagadora",
#         "tipo_pagamento",
#         "valor"
#     ]
# )

# ==========================
# PASSAGEM
# ==========================

carregar_csv(

    "2025_Passagem.csv",

    "raw_passagem",

    [
        "id_viagem",
        "num_proposta",
        "meio_transporte",
        "pais_origem_ida",
        "uf_origem_ida",
        "cidade_origem_ida",
        "pais_destino_ida",
        "uf_destino_ida",
        "cidade_destino_ida",
        "pais_origem_volta",
        "uf_origem_volta",
        "cidade_origem_volta",
        "pais_destino_volta",
        "uf_destino_volta",
        "cidade_destino_volta",
        "valor_passagem",
        "taxa_servico",
        "data_emissao",
        "hora_emissao"
    ]
)

# ==========================
# TRECHO
# ==========================

carregar_csv(

    "2025_Trecho.csv",

    "raw_trecho",

    [
        "id_viagem",
        "num_proposta",
        "sequencia_trecho",
        "origem_data",
        "origem_pais",
        "origem_uf",
        "origem_cidade",
        "destino_data",
        "destino_pais",
        "destino_uf",
        "destino_cidade",
        "meio_transporte",
        "numero_diarias",
        "missao"
    ]
)

print("\nPROCESSO FINALIZADO!")