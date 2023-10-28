## ElasticSearch dump

### Install Elasticdump
https://hub.docker.com/r/elasticdump/elasticsearch-dump/

`docker pull elasticdump/elasticsearch-dump`

### Using makefile 
*make backup INDEX_NAME = <index_name>* - Копирование данных из Elastic в файл.<br>
*make restore INDEX_NAME = <index_name>* - Копирование данных из файла в Elastic.<br>


#### Backup data
- `make backup INDEX_NAME=movies`
- `make backup INDEX_NAME=persons`
- `make backup INDEX_NAME=genres`    

#### Restore data
- `make restore INDEX_NAME=movies`
- `make restore INDEX_NAME=persons`
- `make restore INDEX_NAME=genres`

