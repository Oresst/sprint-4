from .genres_data import genres_data
from .genres_index import genres_index_attributes
from .movies_data import movies_data
from .movies_index import movies_index_attributes
from .persons_data import persons_data
from .persons_index import persons_index_attributes

index_data_map = {
    'movies': movies_data,
    'persons': persons_data,
    'genres': genres_data
}

index_attributes_map = {
    'movies': movies_index_attributes,
    'persons': persons_index_attributes,
    'genres': genres_index_attributes
}
