# MovieRatings

Pipeline de dados utilizando o dataset disponibilizado pela GroupLens: https://grouplens.org/datasets/movielens/latest/. 

O projeto foi implementado dentro da Google Cloud Platform com algumas limitações do período gratuito.

O streaming de dados ainda está em desenvolvimento. Por enquanto o Batch Job executa a partir de um DeltaLake criado a partir dos arquivos csv disponibilizados.

GCP Products:
- Cloud Dataproc (Apache Spark + Apache Zeppelin)
- Cloud Storage
- Cloud Marketplace (Apache Kafka)
- AppEngine (Apache Airflow)
- Cloud Functions (Geração de dados artificialmente)

Informações do dataset:
- movie.csv: Dados dos Filmes
- rating.csv: Dados de Avaliação dos Filmes

Job:
- Selecionar os TOP 1000 filmes com maiores números de Avaliação
- Depois selecionar os TOP 100 com melhores Avaliações

Batch Pipeline:
- Execução do Job diariamente
- Delta Lake -> Spark -> json (Datetime -> Result)
- Orquestrador: Apache Airflow

Streaming:
- Cloud Functions -> Apache Kafka -> Spark -> Delta Lake

Tech-Stack:
- Apache Spark: framework de processamento
- Apache Zeppelin: usado para testes e visualizações
- Apache Airflow: orquestrador dos Batch Jobs
- Apache Kakfa: usado como fila de mensagem de eventos
- GCP Storage: Data Lake
- Delta Lake: camada que provém transações ACID e validação de Schema para o Data Lake

Objetivos do projeto:
- Geração de dados artificialmente
- Ingestão desses dados no Kafka
- Ingestão no Spark
- Inserção desses dados no Delta Lake
- Leitura dos dados do Delta Lake no Batch Job diário
- Inserção dos dados processados no Data Lake no formato json (também poderia salvar num banco de dados relacional ou NoSQL)
