from testdata.es_models_data import index_data_mapper


def es_index_rows_generator(index_name: str, n: int = 1) -> list[dict]:
    if index_name in index_data_mapper:
        return index_data_mapper[index_name](n)
    else:
        raise ValueError('index_name does not defined')


def es_generate_actions(index_name: str, doc_data: list[dict], es_id_field: str = 'id'):
    for item in doc_data:
        doc = item
        doc['_id'] = item[es_id_field]
        doc['_index'] = index_name
        yield doc
