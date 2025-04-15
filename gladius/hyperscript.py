__all__ = ['h', 'render', 'define']

import json
import inspect
from dataclasses import dataclass
from typing import Any, Optional, Union, Callable

from .defs import SVG_TAGS, VOID_TAGS, CONTAINER_TAGS


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
    defined_elements: dict[str, Any]
    element_scopes: list[HNode] # used for elements using `with` statement


    def __init__(self):
        self.defined_elements = {'del_': 'del', 'Text': Text}
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


    def __getattr__(self, attr: str) -> Any:
        def _node_fn(props: Optional[dict[str, Any]]=None, *children) -> HNode:
            global h
            type: Union[str, Callable[[], HNode], Callable[[dict[str, Any]], HNode]]

            if attr in self.defined_elements:
                type = self.defined_elements[attr]
            else:
                type = attr

            node = HNode(
                type=type,
                props=props,
                children=list(children),
            )

            if h.element_scopes:
                parent_node: HNode = h.element_scopes[-1]

                for child in children:
                    if child in list(parent_node.children):
                        parent_node.children.remove(child)

                parent_node.children.append(node)

            return node

        return _node_fn


    def define(self, fn: Callable):
        self.defined_elements[fn.__name__] = fn
        return fn


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
    rendered_node: str
    ident_str: str = " " * (ident * 2)
    text_ident_str: str = " " * ((ident + 1) * 2)

    print('!', node)
    if isinstance(node, str):
        return f'{text_ident_str}{node}'
    elif isinstance(node, HNode) and node.type == 'Text':
        return f'{text_ident_str}{node.children}'
    else:
        type = node.type
        props = node.props
        children = node.children

    if props:
        rendered_props = [f'{k}={json.dumps(v)}' for k, v in props.items()]
        rendered_props = ' '.join(rendered_props)
    else:
        rendered_props = ''

    if type in VOID_TAGS:
        rendered_node = f'{ident_str}<{type} {rendered_props}/>'
    elif type in SVG_TAGS or type in CONTAINER_TAGS:
        rendered_children: Union[list[str], str]

        if children:
            rendered_children = [
                render(n, ident=ident + 1)
                for n in children
            ]

            rendered_children = '\n'.join(rendered_children)
            rendered_node = f'{ident_str}<{type} {rendered_props}>\n{rendered_children}\n{ident_str}</{type}>'
        else:
            rendered_node = f'{ident_str}<{type} {rendered_props}></{type}>'

        if type == 'p':
            print('###', rendered_node)
    elif callable(type):
        # check if element expects props
        args_names: list[str] = inspect.getargs(type.__code__).args

        if len(args_names) == 0:
            type_node: HNode = type() # type: ignore
        elif len(args_names) == 1:
            type_node: HNode = type(props) # type: ignore
        else:
            raise ValueError(f'Unexpected number of paramaters: {len(args_names)}')

        rendered_node = render(type_node, ident=ident)
    else:
        raise ValueError(f'Unsupported node type: {type!r}')

    return rendered_node


h = H()
define = h.define
