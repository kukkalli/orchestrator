import logging
from typing import List, TypeVar

LOG = logging.getLogger(__name__)


T = TypeVar('T')


def add_elements(list_features: List[T], features):
    for feature in features:
        list_features.append(feature)


def add_elements_with_type(list_features: List[T], features, class_type):
    for feature in features:
        list_features.append(class_type(feature))
