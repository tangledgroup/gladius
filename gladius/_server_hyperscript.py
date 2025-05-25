__all__ = ['h', 'render']

import json
import inspect
from dataclasses import dataclass
from typing import Any, Optional, Union, Callable


SVG_TAGS: set[str] = {
    'a', 'animate', 'animateMotion', 'animateTransform',
    'circle', 'clipPath',
    'defs', 'desc',
    'ellipse',
    'feBlend', 'feColorMatrix', 'feComponentTransfer', 'feComposite',
    'feConvolveMatrix', 'feDiffuseLighting', 'feDisplacementMap',
    'feDistantLight', 'feDropShadow', 'feFlood', 'feFuncA', 'feFuncB',
    'feFuncG', 'feFuncR', 'feGaussianBlur', 'feImage', 'feMerge', 'feMergeNode',
    'feMorphology', 'feOffset', 'fePointLight', 'feSpecularLighting',
    'feSpotLight', 'feTile', 'feTurbulence', 'filter', 'foreignObject',
    'g',
    'image',
    'line', 'linearGradient',
    'marker', 'mask', 'metadata', 'mpath',
    'path', 'pattern', 'polygon', 'polyline',
    'radialGradient', 'rect',
    'script', 'set', 'stop', 'style', 'svg', 'switch', 'symbol',
    'text', 'textPath', 'title', 'tspan',
    'use',
    'view',
}


VOID_TAGS: set[str] = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
    'meta', 'param', 'source', 'track', 'wbr',
}


CONTAINER_TAGS: set[str] = {
    'a', 'abbr', 'address', 'article', 'aside', 'audio', 'b', 'bdi', 'bdo',
    'blockquote', 'body', 'button', 'canvas', 'caption', 'cite', 'code',
    'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn',
    'dialog', 'div', 'dl', 'dt', 'em', 'fieldset', 'figcaption',
    'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'head', 'header', 'hgroup', 'html', 'i', 'iframe', 'ins', 'kbd',
    'label', 'legend', 'li', 'main', 'map', 'mark', 'menu', 'meter',
    'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output',
    'p', 'picture', 'pre', 'progress', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby',
    's', 'samp', 'script', 'section', 'select', 'slot', 'small', 'span',
    'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody',
    'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time',
    'title', 'tr', 'u', 'ul', 'var', 'video',

    *SVG_TAGS,
}

BOOLEAN_PROPERTIES: list[str] = [
    'allowfullscreen', 'async', 'autofocus', 'autoplay', 'checked',
    'controls', 'default', 'defer', 'disabled', 'formnovalidate',
    'hidden', 'ismap', 'loop', 'multiple', 'muted', 'nomodule',
    'novalidate', 'open', 'playsinline', 'readonly', 'required',
    'reversed', 'selected', 'sortable',
]


@dataclass(init=False)
class HNode:
    type: Union[str, Callable[[], 'HNode'], Callable[[dict[str, Any]], 'HNode']]
    props: Optional[dict[str, Any]]
    children: list[Union[str, 'HNode']]


    def __init__(self, type, props, children):
        self.type = type
        self.props = props
        self.children = children


    def __enter__(self) -> 'HNode':
        global h
        h.element_scopes.append(self)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        global h

        h.element_scopes.pop()

        if exc_val:
            raise exc_val


@dataclass(init=False)
class Text(HNode):
    def __init__(self, children):
        self.type = 'Text'
        self.props = None
        self.children = children


class H:
    element_scopes: list[HNode] # used for elements using `with` statement


    def __init__(self):
        self.element_scopes = []


    def __call__(self,
                 type: Union[str, Callable[[], HNode], Callable[[dict[str, Any]], HNode]],
                 props: dict[str, Any] | None,
                 *children) -> HNode:
        node = HNode(
            type=type,
            props=props,
            children=list(children),
        )

        if self.element_scopes:
            parent_node: HNode = self.element_scopes[-1]
            parent_node.children.append(node)

        return node


    def text(self, text: str) -> HNode:
        node = Text(text)

        if h.element_scopes:
            scope: HNode = h.element_scopes[-1]
            scope.children.append(node)

        return node


def render(node: str | HNode, ident: int=0) -> str:
    type: Union[str, Callable[[], HNode], Callable[[dict[str, Any]], HNode]]
    props: Optional[dict[str, Any]]
    children: list[Union[str, HNode]]
    rendered_props: Union[list[str], str]
    rendered_node: Union[list[str], str]
    ident_str: str = ' ' * (ident * 2)
    text_ident_str: str = ' ' * ((ident + 1) * 2)

    if isinstance(node, str):
        return f'{text_ident_str}{node}'
    elif isinstance(node, HNode) and node.type == 'Text':
        return f'{text_ident_str}{node.children}'
    else:
        type = node.type
        props = node.props
        children = node.children

    if props:
        rendered_props = [
            k if k in BOOLEAN_PROPERTIES and v is None else f'{k}={json.dumps(v)}'
            for k, v in props.items()
        ]

        rendered_props = ' '.join(rendered_props)
    else:
        rendered_props = ''

    if type in VOID_TAGS:
        rendered_node = f'{ident_str}<{type} {rendered_props}/>'
    elif type in SVG_TAGS or type in CONTAINER_TAGS:
        rendered_children: Union[list[str], str]

        if children:
            if type == 'script' and props and props.get('type') == 'text/python':
                assert all(isinstance(n, str) for n in children)
                rendered_children = children # type: ignore
            else:
                rendered_children = [
                    render(n, ident=ident + 1)
                    for n in children
                ]

            rendered_children = '\n'.join(rendered_children)

            if rendered_props:
                rendered_node = f'{ident_str}<{type} {rendered_props}>\n{rendered_children}\n{ident_str}</{type}>'
            else:
                rendered_node = f'{ident_str}<{type}>\n{rendered_children}\n{ident_str}</{type}>'
        else:
            if rendered_props:
                rendered_node = f'{ident_str}<{type} {rendered_props}></{type}>'
            else:
                rendered_node = f'{ident_str}<{type}></{type}>'

        rendered_node = ''.join(rendered_node)
    elif callable(type):
        # check if element expects props
        args_names: list[str] = inspect.getargs(type.__code__).args

        if len(args_names) == 0:
            type_node: HNode = type() # type: ignore
        elif len(args_names) == 1:
            type_node: HNode = type(props) # type: ignore
        else:
            raise ValueError(f'Unexpected number of parameters: {len(args_names)}')

        rendered_node = render(type_node, ident=ident)
    else:
        raise ValueError(f'Unsupported node type: {type!r}')

    if type == 'html':
        rendered_node = '<!DOCTYPE html>\n' + rendered_node

    return rendered_node


h = H()
