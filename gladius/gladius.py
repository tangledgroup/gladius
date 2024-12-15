from .types import BaseGladius
from .element import ElementType, Element, ContainerElement


class Gladius(BaseGladius):
    element_types: dict[str, ElementType]
    element_scopes: list[ContainerElement]


    def __init__(self):
        self.element_types = {}
        self.element_scopes = []


    def __getattr__(self, tag: str) -> ElementType:
        element_type: ElementType

        if tag in self.element_types:
            element_type = self.element_types[tag]
            return element_type
        else:
            element_type = getattr(Element, tag)
            element_type.ctx = self
            element_type.tag = tag
            self.element_types[tag] = element_type

        return element_type
