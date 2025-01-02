__all__ = ['ElementType', 'Element', 'Text', 'VoidElement', 'ContainerElement']

import json
from typing import Any, Optional

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


    def __init__(self, /, inline: bool=False, extra_attrs: Optional[dict]=None, **kwargs):
        self.attrs = dict(kwargs)

        if extra_attrs:
            self.attrs.update(extra_attrs)

        # print(self.attrs)

        if not inline and self.ctx.element_scopes:
            parent_element: ContainerElement = self.ctx.element_scopes[-1]
            parent_element.add(self)


    def __repr2__(self, indet: int=0):
        return super().__repr__()


    def __repr__(self) -> str:
        return self.__repr2__()


    def __len__(self) -> int:
        return 0


    def render(self, indent: int=0) -> str:
        raise NotImplementedError('override render method')


    def render_attr_key(self, key: str) -> str:
        if key == 'class_':
            return 'class'
        elif key == 'for_':
            return 'for'

        return key.replace('_', '-')


    def render_attr_value(self, value: Any) -> str:
        return json.dumps(str(value))


class Text(Element):
    tag = None
    void_element = True
    text_content: str


    def __init__(self, text_content: str, inline: bool=False):
        super().__init__(inline=inline)
        self.text_content = text_content


    def __repr2__(self, indent: int=0) -> str:
       text: list[str] | str = []
       text.append(' ' * indent)
       text.append('<')
       text.append(self.__class__.__name__)
       text.append(f' text_content={self.text_content!r}')
       text.append('>')
       text = ''.join(text)
       return text


    def __repr__(self) -> str:
        return self.__repr2__()


    def __len__(self) -> int:
        return len(self.text_content)


    def __getitem__(self, index: int) -> str:
        return self.text_content[index]


    def render(self, indent : int=0) -> str:
        return (' ' * indent) + self.text_content


class VoidElement(Element):
    void_element = True


    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)


    def __repr2__(self, indent: int=0) -> str:
        text: list[str] | str = []
        text.append(' ' * indent)
        text.append('<')
        text.append(self.__class__.__name__)

        for k, v in self.attrs.items():
            # text.append(f' {k}={v!r}')
            text.append(f' {self.render_attr_key(k)}={self.render_attr_value(v)}')

        text.append('>')
        text = ''.join(text)
        return text


    def __repr__(self):
        return self.__repr2__()


    def __len__(self) -> int:
        return 0


    def render(self, indent : int=0) -> str:
        text: list[str] | str = []
        text.append(' ' * indent)
        text.append('<')
        text.append(self.__class__.__name__)

        for k, v in self.attrs.items():
            # text.append(f' {k}={v!r}')
            text.append(f' {self.render_attr_key(k)}={self.render_attr_value(v)}')

        text.append('/>')
        text = ''.join(text)
        return text



class ContainerElement(Element):
    void_element = False
    children: list[Element]


    def __init__(self, text_content: str | None=None, /, **kwargs):
        super().__init__(**kwargs)
        self.children = []

        # print('!!! [0] self', self, text_content, type(text_content), kwargs)
        # if text_content is not None:
        # if not (text_content is None or isinstance(text_content, str)):
        #     raise ValueError(text_content)

        if text_content:
            # print('----')
            # text_node: Element = Text(ctx=self.ctx, text_content=text_content)
            text_node: Element = self.ctx.text(text_content, inline=True) # type: ignore
            # print('!!! [1] self', self, text_content, kwargs, text_node)
            self.children.append(text_node)


    def __repr2__(self, indent: int=0) -> str:
        text: list[str] | str = []
        text.append(' ' * indent)
        text.append(f'<{self.__class__.__name__}')

        for k, v in self.attrs.items():
            # text.append(f' {k}={v!r}')
            text.append(f' {self.render_attr_key(k)}={self.render_attr_value(v)}')

        text.append(' children=[')

        if self.children:
            text.append('\n')

        for n in self.children:
            text.append(n.__repr2__(indent + 2))
            text.append(',\n')

        if self.children:
            text.append(' ' * indent)

        text.append(']>')
        text = ''.join(text)
        return text


    def __repr__(self):
        return self.__repr2__()


    def __len__(self) -> int:
        return len(self.children)


    def __getitem__(self, index: int) -> Element:
        return self.children[index]


    def __enter__(self):
        assert isinstance(self, ContainerElement), "only container elements can contain other elements"
        self.ctx.element_scopes.append(self)
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise exc_value.with_traceback(traceback)

        element: Element = self.ctx.element_scopes.pop()
        return element


    def add(self, *args) -> 'Element':
        assert all(isinstance(n, (Element, str)) for n in args)

        if self.children is None:
            self.children = []

        new_args: list[Element] = []

        for n in args:
            if isinstance(n, str):
                n = self.ctx.text(n, inline=True) # type: ignore

            new_args.append(n)

        self.children.extend(new_args)
        return self


    def render(self, indent : int=0) -> str:
        text: list[str] | str = []

        if self.tag == 'html':
            text.append('<!DOCTYPE html>\n')

        text.append(' ' * indent)
        text.append(f'<{self.__class__.__name__}')

        for k, v in self.attrs.items():
            # text.append(f' {k}={v!r}')
            text.append(f' {self.render_attr_key(k)}={self.render_attr_value(v)}')

        text.append('>')

        if self.children:
            text.append('\n')

        for n in self.children:
            text.append(n.render(indent + 2))
            text.append('\n')

        if self.children:
            text.append(' ' * indent)

        text.append(f'</{self.__class__.__name__}>')
        text = ''.join(text)
        return text
