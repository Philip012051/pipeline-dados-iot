
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import MetaData, Table

# ==========================================
# CONFIGURACAO DO BANCO DE DADOS
# ==========================================

DATABASE_URL = (
    "postgresql+psycopg2://postgres:iot12345@localhost:5432/iot_db"
)

CSV_PATH = "data/IOT-temp.csv"

engine = create_engine(DATABASE_URL)


# ==========================================
# IMPORTACAO DOS DADOS
# ==========================================

def importar_dados():
    print("Lendo o arquivo CSV...")

    # Le o arquivo original
    df = pd.read_csv(CSV_PATH)

    # Renomeia as colunas
    df = df.rename(columns={
        "id": "id_leitura",
        "room_id/id": "dispositivo_id",
        "noted_date": "data_leitura",
        "temp": "temperatura",
        "out/in": "local_tipo"
    })

    # Preserva os identificadores como texto
    df["id_leitura"] = df["id_leitura"].astype("string")
    df["dispositivo_id"] = df["dispositivo_id"].astype("string")

    # Converte as datas para o formato correto
    df["data_leitura"] = pd.to_datetime(
        df["data_leitura"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    # Converte a temperatura para numero
    df["temperatura"] = pd.to_numeric(
        df["temperatura"],
        errors="coerce"
    )

    # Remove registros invalidos
    df = df.dropna(subset=[
        "id_leitura",
        "dispositivo_id",
        "data_leitura",
        "temperatura"
    ])

    # Converte valores do pandas para tipos compativeis
    df["id_leitura"] = df["id_leitura"].astype(str)
    df["dispositivo_id"] = df["dispositivo_id"].astype(str)
    df["local_tipo"] = df["local_tipo"].fillna("Desconhecido").astype(str)

    print(f"Registros validos encontrados: {len(df)}")

    # Cria a tabela se ela ainda nao existir
    with engine.begin() as conexao:
        conexao.execute(text("""
            CREATE TABLE IF NOT EXISTS leituras_temperatura (
                id_leitura TEXT PRIMARY KEY,
                dispositivo_id TEXT,
                data_leitura TIMESTAMP,
                temperatura DOUBLE PRECISION,
                local_tipo VARCHAR(20)
            )
        """))

    # Confere se a tabela existente tem a estrutura esperada.
    # A primeira tentativa de importacao pode ter criado a coluna
    # id_leitura como BIGINT. Nesse caso, interrompe sem apagar dados.
    metadata = MetaData()
    tabela = Table(
        "leituras_temperatura",
        metadata,
        autoload_with=engine
    )

    tipo_id = str(tabela.c.id_leitura.type).upper()

    if tipo_id not in ("TEXT", "VARCHAR"):
        raise RuntimeError(
            "A tabela antiga tem id_leitura do tipo "
            f"{tipo_id}, mas precisamos de TEXT. "
            "Avise-me antes de alterar a tabela."
        )

    print("Inserindo dados no PostgreSQL...")

    # Insere em lotes pequenos para evitar excesso de parametros.
    # Identificadores que ja existem sao ignorados.
    colunas = [
        "id_leitura",
        "dispositivo_id",
        "data_leitura",
        "temperatura",
        "local_tipo"
    ]

    registros = df[colunas].to_dict(orient="records")
    total = len(registros)

    with engine.begin() as conexao:
        for inicio in range(0, total, 100):
            lote = registros[inicio:inicio + 100]

            comando = insert(tabela).values(lote)
            comando = comando.on_conflict_do_nothing(
                index_elements=["id_leitura"]
            )

            conexao.execute(comando)

            processados = min(inicio + len(lote), total)
            print(f"Processados {processados} de {total} registros...")

    # Verifica quantas linhas existem no banco
    with engine.connect() as conexao:
        quantidade = conexao.execute(
            text("SELECT COUNT(*) FROM leituras_temperatura")
        ).scalar_one()

    print("\nImportacao concluida!")
    print(f"Registros validos no CSV: {total}")
    print(f"Total de registros na tabela: {quantidade}")


# ==========================================
# EXECUCAO DO PROGRAMA
# ==========================================

if __name__ == "__main__":
    try:
        importar_dados()
    except Exception as erro:
        print("\nOcorreu um erro durante a importacao:")
        print(f"{type(erro).__name__}: {erro}")
        raise
    finally:
        engine.dispose()
