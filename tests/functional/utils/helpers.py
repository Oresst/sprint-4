def es_generate_actions(index_name: str, doc_data: list[dict], es_id_field: str = 'id'):
    for item in doc_data:
        doc = item
        doc['_id'] = item[es_id_field]
        doc['_index'] = index_name
        yield doc
