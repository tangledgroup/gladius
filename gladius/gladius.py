from .types import BaseGladius
from .element import ElementType, Element, ContainerElement, Text


class Gladius(BaseGladius):
    element_types: dict[str, ElementType]
    element_scopes: list[ContainerElement]


    def __init__(self):
        ctx_Text: ElementType = ElementType('Text', (Text,), {'ctx': self})
        ctx_Text.ctx = self

        self.element_types = {'text': ctx_Text}
        self.element_scopes = []


    def __getattr__(self, tag: str) -> ElementType:
        element_type: ElementType

        if tag in self.element_types:
            element_type = self.element_types[tag]
        else:
            element_type = getattr(Element, tag)
            element_type.ctx = self
            element_type.tag = tag
            self.element_types[tag] = element_type

        return element_type
