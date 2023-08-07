# Projeto de ETL orquestrado com Apache Airflow  

O projeto roda em Linux e algumas configurações e criações de diretório são necessárias para que utiliza-lo.
Antes de tudo é necessário ter instalado o pipenv.  
Junto com os arquivos Pipfile e Pipfile.lock é necessário criar um arquivo **.env** com as variáveis de ambiente utilizadas no projeto.  
No arquivo em inclua as duas variáveis de ambiente, substitua o user pelo caminho da máquina utilizada:  
AIRFLOW_HOME=/home/{user}/projeto/.venv/airflow  
KAGGLE_CONFIG_DIR=/home/{user}/projeto/.venv/.kaggle

Outros arquivos que precisam ter os caminhos de diretório alterado são:  
/.kaggle/kaggle.json  
/airflow/dags/pipeline.py  
/src/testes/consultas.py  
/src/util/unzip_dataset.py  

Feita a configuração baixe as dependencias com o seguinte comando:  
pipenv install

Instaladas as dependências é necessário executar o comando **pipenv shell** para utilizar as variáveis de ambientes declaradas no projeto  
Após isso, é hora de iniciar o airflow, execute os seguintes comandos:  
airflow db init  

Você pode criar um usuário com o seguinte comando:  
airflow users create \  
    --username user \  
    --firstname name \  
    --lastname lastname \  
    --role Admin \  
    --password admin \  
    --email user.mail@mail.com  
    
Em seguida executar airflow webserver --port 8080 e airflow scheduler

