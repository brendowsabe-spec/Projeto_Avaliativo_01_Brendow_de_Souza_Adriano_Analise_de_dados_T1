#Download + leitura dos CSVs + carga na camada Raw.

#● Fase 1 - Extração e camada Raw (1_extrair.py): baixar o arquivo .zip do Google Drive, ler os 4 CSVs em blocos 
# e carregar nas tabelas Raw sem alterar o conteúdo. O processo deve ser idempotente (TRUNCATE antes de carregar) 
# e resiliente (try/except). Este zip já está transformado para trabalharmos com 6 meses do ano 2025.