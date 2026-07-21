#Limpeza e tipagem (Raw → Silver) + colunas calculadas.

# ● Fase 2 - Transformação e camada Silver (2_transformar.py): copiar Raw para Silver convertendo os tipos (texto para DECIMAL e DATE), 
# respeitando a integridade referencial e calculando as colunas valor_total e duracao_dias.

from banco import obter_engine

engine = obter_engine()

def transformar_dados():
    try:
        print("\nIniciando a transformação dos dados (Camada Raw -> Silver)...")

        with engine.begin() as conn:
            
            # 1. SILVER VIAGEM
            print("Transformando silver_viagem...")
            conn.exec_driver_sql("TRUNCATE TABLE silver_viagem CASCADE;")
            conn.exec_driver_sql("""
                INSERT INTO silver_viagem (
                    id_viagem, num_proposta, situacao, viagem_urgente, justificativa_urgencia,
                    cod_orgao_superior, nome_orgao_superior, cod_orgao_solicitante, nome_orgao_solicitante,
                    cpf_viajante, nome_viajante, cargo, funcao, descricao_funcao,
                    data_inicio, data_fim, destinos, motivo,
                    valor_diarias, valor_passagens, valor_devolucao, valor_outros_gastos
                )
                SELECT 
                    id_viagem,
                    num_proposta,
                    situacao,
                    CASE WHEN LOWER(viagem_urgente) IN ('sim', 'true', '1') THEN TRUE ELSE FALSE END,
                    NULLIF(justificativa_urgencia, ''),
                    NULLIF(REPLACE(cod_orgao_superior, ',', '.'), '')::NUMERIC::INTEGER,
                    COALESCE(NULLIF(nome_orgao_superior, ''), 'Órgão Não Informado'),
                    NULLIF(REPLACE(cod_orgao_solicitante, ',', '.'), '')::NUMERIC::INTEGER,
                    NULLIF(nome_orgao_solicitante, ''),
                    NULLIF(cpf_viajante, ''),
                    NULLIF(nome_viajante, ''),
                    NULLIF(cargo, ''),
                    NULLIF(funcao, ''),
                    NULLIF(descricao_funcao, ''),
                    TO_DATE(NULLIF(data_inicio, ''), 'DD/MM/YYYY'),
                    TO_DATE(NULLIF(data_fim, ''), 'DD/MM/YYYY'),
                    NULLIF(destinos, ''),
                    NULLIF(motivo, ''),
                    COALESCE(NULLIF(REPLACE(valor_diarias, ',', '.'), ''), '0')::NUMERIC(12,2),
                    COALESCE(NULLIF(REPLACE(valor_passagens, ',', '.'), ''), '0')::NUMERIC(12,2),
                    COALESCE(NULLIF(REPLACE(valor_devolucao, ',', '.'), ''), '0')::NUMERIC(12,2),
                    COALESCE(NULLIF(REPLACE(valor_outros_gastos, ',', '.'), ''), '0')::NUMERIC(12,2)
                FROM raw_viagem
                WHERE id_viagem IS NOT NULL AND id_viagem != '';
            """)

            # 2. SILVER PAGAMENTO
            print("Transformando silver_pagamento...")
            conn.exec_driver_sql("TRUNCATE TABLE silver_pagamento CASCADE;")
            conn.exec_driver_sql("""
                INSERT INTO silver_pagamento (
                    id_viagem, num_proposta, cod_orgao_superior, nome_orgao_superior,
                    cod_orgao_pagador, nome_orgao_pagador, cod_ug_pagadora, nome_ug_pagadora,
                    tipo_pagamento, valor
                )
                SELECT 
                    p.id_viagem,
                    COALESCE(NULLIF(p.num_proposta, ''), 'SN'),
                    NULLIF(REPLACE(p.cod_orgao_superior, ',', '.'), '')::NUMERIC::INTEGER,
                    NULLIF(p.nome_orgao_superior, ''),
                    NULLIF(REPLACE(p.cod_orgao_pagador, ',', '.'), '')::NUMERIC::INTEGER,
                    NULLIF(p.nome_orgao_pagador, ''),
                    NULLIF(REPLACE(p.cod_ug_pagadora, ',', '.'), '')::NUMERIC::INTEGER,
                    NULLIF(p.nome_ug_pagadora, ''),
                    COALESCE(NULLIF(p.tipo_pagamento, ''), 'Não Informado'),
                    COALESCE(NULLIF(REPLACE(p.valor, ',', '.'), ''), '0')::NUMERIC(12,2)
                FROM raw_pagamento p
                JOIN silver_viagem v ON p.id_viagem = v.id_viagem;
            """)

            # 3. SILVER PASSAGEM
            print("Transformando silver_passagem...")
            conn.exec_driver_sql("TRUNCATE TABLE silver_passagem CASCADE;")
            conn.exec_driver_sql("""
                INSERT INTO silver_passagem (
                    id_viagem, num_proposta, meio_transporte,
                    pais_origem_ida, uf_origem_ida, cidade_origem_ida,
                    pais_destino_ida, uf_destino_ida, cidade_destino_ida,
                    valor_passagem, taxa_servico, data_emissao, hora_emissao
                )
                SELECT 
                    p.id_viagem,
                    NULLIF(p.num_proposta, ''),
                    COALESCE(NULLIF(p.meio_transporte, ''), 'Outros'),
                    NULLIF(p.pais_origem_ida, ''),
                    SUBSTRING(NULLIF(p.uf_origem_ida, ''), 1, 10),
                    NULLIF(p.cidade_origem_ida, ''),
                    NULLIF(p.pais_destino_ida, ''),
                    SUBSTRING(NULLIF(p.uf_destino_ida, ''), 1, 10),
                    NULLIF(p.cidade_destino_ida, ''),
                    COALESCE(NULLIF(REPLACE(p.valor_passagem, ',', '.'), ''), '0')::NUMERIC(12,2),
                    COALESCE(NULLIF(REPLACE(p.taxa_servico, ',', '.'), ''), '0')::NUMERIC(12,2),
                    TO_DATE(NULLIF(p.data_emissao, ''), 'DD/MM/YYYY'),
                    NULLIF(p.hora_emissao, '')::TIME
                FROM raw_passagem p
                JOIN silver_viagem v ON p.id_viagem = v.id_viagem;
            """)

            # 4. SILVER TRECHO
            print("Transformando silver_trecho...")
            conn.exec_driver_sql("TRUNCATE TABLE silver_trecho CASCADE;")
            conn.exec_driver_sql("""
                INSERT INTO silver_trecho (
                    id_viagem, num_proposta, sequencia_trecho,
                    origem_data, origem_pais, origem_uf, origem_cidade,
                    destino_data, destino_pais, destino_uf, destino_cidade,
                    meio_transporte, numero_diarias, missao
                )
                SELECT 
                    t.id_viagem,
                    NULLIF(t.num_proposta, ''),
                    COALESCE(NULLIF(REPLACE(t.sequencia_trecho, ',', '.'), '')::NUMERIC::INTEGER, 1),
                    TO_DATE(NULLIF(t.origem_data, ''), 'DD/MM/YYYY'),
                    NULLIF(t.origem_pais, ''),
                    SUBSTRING(NULLIF(t.origem_uf, ''), 1, 10),
                    NULLIF(t.origem_cidade, ''),
                    TO_DATE(NULLIF(t.destino_data, ''), 'DD/MM/YYYY'),
                    NULLIF(t.destino_pais, ''),
                    SUBSTRING(NULLIF(t.destino_uf, ''), 1, 10),
                    NULLIF(t.destino_cidade, ''),
                    NULLIF(t.meio_transporte, ''),
                    COALESCE(NULLIF(REPLACE(t.numero_diarias, ',', '.'), ''), '0')::NUMERIC(10,2),
                    CASE WHEN LOWER(t.missao) IN ('sim', 'true', '1') THEN TRUE ELSE FALSE END
                FROM raw_trecho t
                JOIN silver_viagem v ON t.id_viagem = v.id_viagem;
            """)

        print("\nSUCESSO! Camada Silver populada com sucesso.")

    except Exception as erro:
        print("\nERRO DURANTE A TRANSFORMAÇÃO:")
        print(erro)

if __name__ == "__main__":
    transformar_dados()