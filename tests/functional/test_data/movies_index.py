movies_mapping = {
    "dynamic": "strict",
    "properties": {
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {"id": {"type": "keyword"}, "name": {"type": "text", "analyzer": "ru_en"}},
        },
        "actors_names": {"type": "text", "analyzer": "ru_en"},
        "description": {"type": "text", "analyzer": "ru_en"},
        "director": {"type": "text", "analyzer": "ru_en"},
        "genre": {
            "type": "text",
            "fields": {"raw": {"type": "keyword"}},
            "analyzer": "genres_analyzer",
            "fielddata": True,
        },
        "id": {"type": "keyword"},
        "imdb_rating": {"type": "float"},
        "title": {"type": "text", "fields": {"raw": {"type": "keyword"}}, "analyzer": "ru_en"},
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {"id": {"type": "keyword"}, "name": {"type": "text", "analyzer": "ru_en"}},
        },
        "writers_names": {"type": "text", "analyzer": "ru_en"},
    },
}

movies_settings = {
    "index": {
        "routing": {"allocation": {"include": {"_tier_preference": "data_content"}}},
        "number_of_shards": "1",
        "analysis": {
            "filter": {
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "english_stop": {"type": "stop", "stopwords": "_english_"},
            },
            "analyzer": {
                "ru_en": {
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                    "tokenizer": "standard",
                },
                "genres_analyzer": {"tokenizer": "genres_tokenizer"},
            },
            "tokenizer": {"genres_tokenizer": {"pattern": ",", "type": "simple_pattern_split"}},
        },
        "number_of_replicas": "1",
    }
}