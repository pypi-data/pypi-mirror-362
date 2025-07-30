# nsj-sql-utils-lib

Biblioteca de utilitários Python para facilitar a implementação de sistemas com acesso a banco de dados.
        
## Principais utilitários:
    
* **dao_util:** Módulo com utilitátios para implementação de classes DAO (exemplo: facilitar a criação da lista de fileds de um select, ou fields e values de um insert).
    * **dbadapter3:** Classe adapter para utilizar conexões de banco de dados (útil para conexões psycopg2).
    * **dbconection_psycopg2:** Classe para abertura de conexão com postgres, utilizando o drive psycopg2 (sem pool de conexões, nem uso do SQL Alchemy).
    * **db-updater:** Modulo para atualização de bancos pensado para ser em um formato parecido com o erp-3 
    * **create-script:** Modulo para criação de arquivos de scripts padronizados  
    
    ## Utilização do db-updater:
    * São duas as formas de utilizar o db-updater  uma seria instalando via pip em seu projeto e chamando o mesmo da seguinte forma 

    >python -m nsj_sql_utils_lib.updater.db_updater [parametros]
    
    Os parametros que podem ser passados são:
    
    | parâmetro       | valor default  | descrição
    | --------------- | ------------- |  ------------- |
    |--dbhost   DBHOST  |''|  Database host
    |--dbname   DBNAME  |'' |  Database name
    |--dbuser   DBUSER  |'' |  Database user
    |--dbpass   DBPASS  |''|   Database password
    |--dbport   DBPORT  |''|   Database port
    |--dbpath   DBPATH  |'./database'|   Database updatable files path
    |--version   VERSION  |''|  Version of database files


    Se não informar os parametros na chamada pode-se usar as variaveis de ambiente.

    | variavel        | valor default | descrição                              |
    | --------------- | ------------- | -------------------------------------- |
    | DATABASE_PATH   | /database      | Caminho para os arquivos de atualização |
    | DATABASE_HOST   | ''            | Database host                          |
    | DATABASE_NAME   | ''            | Database name                          |
    | DATABASE_PORT   | ''            | Database port                          |
    | DATABASE_USER   | ''        | Database user                          |
    | DATABASE_PASS   | ''            | Database password                      |
    | VERSION         | ''            | Version of database files   

    A variável Version serve somente para que o console printe a versão dos arquivos, para poder ter um log informando qual a versão que está sendo atualizada.
    

* O formato dos arquivos para a atualização precisarão serem como descrito na pasta skeleton_db:

         --database
           ├-- functions
           ├-- scripts
           └-- views
        
* Exemplo de uso: 
   > python -m nsj_sql_utils_lib.updater.db_updater [-h] [--dbhost DBHOST] [--dbname DBNAME] [--dbuser DBUSER] [--dbpass DBPASS] [--dbport DBPORT] [--dbpath DBPATH] [--version VERSION]

  * Também pode-se gerar uma imagem docker para chamar sem a necessidade de instalar via pip.
  * No momento deste documento a imagem ainda não se encontra no repositório do docker então seria necessário baixar este repositorio e executar o seguinte comando:

  > docker build -f ./dockerfiles/updater/Dockerfile -t db-updater .

  * E em seguida utilizar a imagem para chamar o atualizador

  > docker run -v "$PWD/database:/src/database" db-updater python -m nsj_sql_utils_lib.updater.db_updater  [-h] [--dbhost DBHOST] [--dbname DBNAME] [--dbuser DBUSER] [--dbpass DBPASS] [--dbport DBPORT] [--dbpath DBPATH] [--version VERSION]

        
    ## Utilização do create_script

*  Foi criado para padronizar a criação do arquivo script, pode ser instalado pelo mesmo pacote do db-updater:
  
    | parâmetro       | valor default  | descrição
    | --------------- | ------------- |  ------------- |
    |--filename   FILENAME  |''|  Database nome do arquivo a ser criado 
     |--scriptspath   SCRIPTSPATH  |'./database/scripts/' | Caminho da pasta de scripts  

 > python -m nsj_sql_utils_lib.updater.create_script[-h] [--filename FILENAME] [--scriptspath SCRIPTSPATH]
 
 
 
 * Pode ser usado a forma como imagem docker:
 *   > docker run -v "$PWD/database:/src/database" db-updater python -m nsj_sql_utils_lib.updater.create_script [-h] [--filename FILENAME] [--scriptspath SCRIPTSPATH]
