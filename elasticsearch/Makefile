HOST_DIR ?= './dumps'
ELASTIC_URL ?= 'http://localhost:9200'
INDEX_NAME ?= 'movies'


backup:
	# Copy an index from ES to files:
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump/elasticsearch-dump \
	  --input=${ELASTIC_URL}/${INDEX_NAME} \
	  --output=/tmp/${INDEX_NAME}_analizer.json \
	  --overwrite \
	  --type=analyzer
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump/elasticsearch-dump \
	  --input=${ELASTIC_URL}/${INDEX_NAME} \
	  --output=/tmp/${INDEX_NAME}_mapping.json \
	  --overwrite \
	  --type=mapping
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump/elasticsearch-dump \
	  --input=${ELASTIC_URL}/${INDEX_NAME} \
	  --output=/tmp/${INDEX_NAME}_data.json \
	  --overwrite \
	  --type=data

restore:
	# Copy an index from files to ES:
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump/elasticsearch-dump \
	  --input=/tmp/${INDEX_NAME}_analizer.json \
	  --output=${ELASTIC_URL}/${INDEX_NAME} \
	  --type=analyzer
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump/elasticsearch-dump \
	  --input=/tmp/${INDEX_NAME}_mapping.json \
	  --output=${ELASTIC_URL}/${INDEX_NAME} \
	  --type=mapping
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump/elasticsearch-dump \
	  --input=/tmp/${INDEX_NAME}_data.json \
	  --output=${ELASTIC_URL}/${INDEX_NAME} \
	  --type=data

backup-index:
	# Backup index data to a JSON file:
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump/elasticsearch-dump \
		--input=${ELASTIC_URL}/${INDEX_NAME} \
		--output=/tmp/${FILENAME} \
		--type=data

restore-index:
	# Import data from JSON file into ES
	docker run --net=host --rm -ti -v ${HOST_DIR}:/tmp elasticdump \
	  --input "json:///tmp/${FILENAME}" \
	  --output=${ELASTIC_URL}/${INDEX_NAME}
