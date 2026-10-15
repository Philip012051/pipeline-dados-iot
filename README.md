# Pipeline de Dados com IoT e Docker

## 1. Sobre o projeto

Este projeto implementa um pipeline de dados para analisar leituras de temperatura provenientes de dispositivos IoT. Os dados são processados com Python e Pandas, armazenados em um banco PostgreSQL executado com Docker e apresentados em um dashboard interativo desenvolvido com Streamlit e Plotly.

## 2. Tecnologias utilizadas

- Python
- Pandas
- PostgreSQL
- Docker e Docker Compose
- SQLAlchemy
- psycopg2-binary
- Streamlit
- Plotly

## 3. Fonte dos dados

Dataset: Temperature Readings: IoT Devices

Fonte: Kaggle  
https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

O arquivo CSV utilizado pelo projeto é `IOT-temp.csv`.

## 4. Estrutura do projeto

- `data/`: arquivo CSV utilizado na importação.
- `sql/`: visualizações SQL do banco.
- `dashboard/`: aplicação do dashboard.
- `importar_dados.py`: processamento e importação dos dados.
- `requirements.txt`: dependências Python.
- `docker-compose.yml`: configuração do PostgreSQL.
- `README.md`: documentação do projeto.

## 5. Como executar

### Pré-requisitos

Instale Python e Docker Desktop.

### Iniciar o banco de dados

Na pasta do projeto, execute:

```bash
docker compose up -d
```

### Instalar as dependências

No terminal, execute:

```bash
python -m venv .venv
```

No Windows, ative o ambiente virtual:

```bash
.venv\Scripts\activate
```

Instale as bibliotecas:

```bash
python -m pip install -r requirements.txt
```

### Importar os dados

Execute:

```bash
python importar_dados.py
```

### Criar as visualizações SQL

Execute no terminal do Windows:

```cmd
docker exec -i postgres-iot psql -U postgres -d iot_db < sql\views.sql
```

### Iniciar o dashboard

Execute:

```bash
python -m streamlit run dashboard\dashboard.py
```

O dashboard ficará disponível normalmente em `http://localhost:8501`.

## 6. Visualizações SQL

O projeto utiliza três visualizações:

- `avg_temp_por_dispositivo`: calcula a temperatura média por dispositivo ou local registrado.
- `leituras_por_hora`: contabiliza as leituras por hora do dia.
- `temp_max_min_por_dia`: apresenta as temperaturas máxima e mínima de cada dia.

## 7. Dashboard

O dashboard apresenta indicadores gerais, gráficos de temperatura média, distribuição de leituras por hora e variação das temperaturas máxima e mínima por dia, além de uma tabela para consultar os registros importados.

## 8. Objetivo

O objetivo é demonstrar a integração entre processamento de dados, banco de dados relacional, Docker e visualização interativa para análise de dados de IoT.