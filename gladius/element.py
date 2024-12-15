__all__ = ['ElementType', 'Element', 'VoidElement', 'ContainerElement']

from typing import Any

from .types import BaseGladius
from .defs import VOID_TAGS, CONTAINER_TAGS


class ElementType(type):
    ctx: BaseGladius
    tag: str | None
    void_element: bool


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
    void_element: bool


    def __init__(self, /, **kwargs):
        self.attrs = dict(kwargs)


    def __repr2__(self, indet: int=0):
        return super().__repr__()

    def __repr__(self):
        return self.__repr2__()

class TextNode(Element):
    tag = None
    void_element = False
    text_content: str

    def __init__(self, ctx: BaseGladius, text_content: str):
        super().__init__()
        self.ctx = ctx
        self.text_content = text_content


    def __repr2__(self, ident: int=0) -> str:
       text: list[str] | str = []
       text.append(' ' * ident)
       text.append('<')
       text.append(self.__class__.__name__)
       text.append(f' text_content={self.text_content!r}')
       text.append('>')
       text = ''.join(text)
       return text


    def __repr__(self):
        return self.__repr2__()


class VoidElement(Element):
    void_element = True


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


    def __repr__(self):
        return self.__repr2__()



class ContainerElement(Element):
    void_element = False
    children: list[Element]


    def __init__(self, text_content: str | None = None, /, **kwargs):
        super().__init__(**kwargs)
        self.children = []

        if text_content is not None:
            text_node: Element = TextNode(ctx=self.ctx, text_content=text_content)
            self.children.append(text_node)

        if self.ctx.element_scopes:
            parent_element: ContainerElement = self.ctx.element_scopes[-1]
            parent_element.add(self)


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


    def __repr__(self):
        return self.__repr2__()


    def __enter__(self):
        assert isinstance(self, ContainerElement), "only container elements can contain other elements"
        self.ctx.element_scopes.append(self)
        return self


    def __exit__(self, *exs):
        element: Element = self.ctx.element_scopes.pop()
        return element


    def add(self, *args) -> 'Element':
        assert all(isinstance(n, (Element, str)) for n in args)

        if self.children is None:
            self.children = []

        new_args: list[Element] = []

        for n in args:
            if isinstance(n, str):
                n = TextNode(ctx=self.ctx, text_content=n)

            new_args.append(n)

        self.children.extend(new_args)
        return self
