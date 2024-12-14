__all__ = ['ElementType', 'Element', 'VoidElement', 'ContainerElement']

from typing import Any

from .types import BaseGladius
from .defs import VOID_TAGS, CONTAINER_TAGS


class ElementType(type):
    def __getattr__(cls, tag: str) -> 'ElementType':
        assert tag in VOID_TAGS or tag in CONTAINER_TAGS, f'unsupported tag {tag!r}'

        et: ElementType = ElementType(
            tag,
            (VoidElement if tag in VOID_TAGS else ContainerElement,),
            {},
        )

        return et


class Element(metaclass=ElementType):
    ctx: BaseGladius
    tag: str | None
    attrs: dict[str, Any]

    # A void element is an element in HTML that cannot have any child nodes
    # (i.e., nested elements or text nodes).
    # Void elements only have a start tag;
    # end tags must not be specified for void elements.
    # https://developer.mozilla.org/en-US/docs/Glossary/Void_element
    void_element: bool = False


    def __init__(self, /, **kwargs):
        self.attrs = dict(kwargs)


class TextNode(Element):
    tag = None
    content: str


    def __init__(self, ctx: BaseGladius, content: str):
        super().__init__()
        self.ctx = ctx
        self.content = content


    def __repr2__(self, ident: int=0) -> str:
       text: list[str] | str = []
       text.append(' ' * ident)
       text.append('<')
       text.append(self.__class__.__name__)
       text.append(f' content={self.content!r}')
       text.append('>')
       text = ''.join(text)
       return text


    __repr__ = __repr2__


class VoidElement(Element):
    void_element: bool = True


    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)


    def __repr2__(self, ident: int=0) -> str:
        text: list[str] | str = []
        text.append(' ' * ident)
        text.append('<')
        text.append(self.__class__.__name__)

        for k, v in self.attrs.items():
            text.append(f' {k}={v!r}')

        text.append('>')
        text = ''.join(text)
        return text


    __repr__ = __repr2__



class ContainerElement(Element):
    void_element: bool = False
    children: list[Element | str]


    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)
        self.children = []


    def __repr2__(self, ident: int=0) -> str:
        text: list[str] | str = []
        text.append(' ' * ident)
        text.append('<')
        text.append(self.__class__.__name__)

        for k, v in self.attrs.items():
            text.append(f' {k}={v!r}')

        text.append(' children=[')

        if self.children:
            text.append('\n')

        for n in self.children:
            text.append(n.__repr2__(ident + 2))
            text.append(',\n')

        text.append(' '  * ident)
        text.append(']>')
        text = ''.join(text)
        return text


    __repr__ = __repr2__


    def add(self, *args) -> 'Element':
        assert all(isinstance(n, (Element, str)) for n in args)

        if self.children is None:
            self.children = []

        new_args: list[Element] = [TextNode(self, n) if isinstance(n, str) else n for n in args]
        self.children.extend(new_args)
        return self
