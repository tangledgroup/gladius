from .types import BaseGladius
from .element import Element, ElementType


class Gladius(BaseGladius):
    element_types: dict[str, ElementType]


    def __init__(self):
        self.element_types = {}


    def __getattr__(self, tag: str) -> ElementType:
        element_type: ElementType

        if tag in self.element_types:
            element_type = self.element_types[tag]
            return element_type

        element_type = getattr(Element, tag)
        element_type.ctx = self
        element_type.tag = tag
        self.element_types[tag] = element_type
        return element_type
