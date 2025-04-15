__all__ = ['h', 'render', 'define']

import json
import inspect
from contextlib import AbstractContextManager, contextmanager
from typing import Any, Optional, Union, Callable, TypedDict, Iterator

from .defs import SVG_TAGS, VOID_TAGS, CONTAINER_TAGS


class HNode(TypedDict):
    type: str | Callable[[dict[str, Any]], 'HNode']
    props: dict[str, Any] | None
    children: list[Union[str, 'HNode']]


class H:
    defined_elements: dict[str, Any]
    element_scopes: list[HNode]  # used for elements using `with` statement

    def __init__(self):
        self.defined_elements = {}
        self.element_scopes = []


    def __call__(self, type: str | Callable[[dict[str, Any]], HNode], props: dict[str, Any] | None, *children) -> HNode:
        node = HNode(
            type=type,
            props=props,
            children=list(children),
        )

        if self.element_scopes:
            scope: HNode = self.element_scopes[-1]
            scope['children'].append(node)

        return node


    def __getattr__(self, attr: str) -> Any:
        print(f'??? [0] {attr=}')

        @contextmanager
        def _code_fn(props: Optional[dict[str, Any]]=None, *children) -> Iterator[HNode]:
            print(f'??? [1] {attr=}')
            type: str | Callable[[dict[str, Any]], HNode]

            if attr in self.defined_elements:
                type = self.defined_elements[attr]
            else:
                type = attr

            node = HNode(
                type=type,
                props=props,
                children=list(children),
            )
            print(f'!!! {attr=} {node=}')

            if self.element_scopes:
                scope: HNode = self.element_scopes[-1]
                scope['children'].append(node)

            self.element_scopes.append(node)

            try:
                yield node
            finally:
                self.element_scopes.pop()

        return _code_fn


    def define(self, fn: Callable):
        self.defined_elements[fn.__name__] = fn
        return fn


h = H()
define = h.define


def render(node: str | HNode | AbstractContextManager, ident: int=0) -> str:
    type: str | Callable[[dict[str, Any]], HNode]
    props: dict[str, Any] | None
    children: list[Union[str, HNode]]
    rendered_props: list[str] | str
    rendered_node: str
    ident_str: str = " " * (ident * 2)
    text_ident_str: str = " " * ((ident + 1) * 2)

    if isinstance(node, str):
        return f'{text_ident_str}{node}'
    elif isinstance(node, AbstractContextManager):
        with node as n:
            type = n['type']
            props = n['props']
            children = n['children']
    else:
        type = node['type']
        props = node['props']
        children = node['children']

    print(f'{type}')
    print(f'{props}')
    print(f'{children}')

    if props:
        rendered_props = [f'{k}={json.dumps(v)}' for k, v in props.items()]
        rendered_props = ' '.join(rendered_props)
    else:
        rendered_props = ''

    if type in VOID_TAGS:
        rendered_node = f'{ident_str}<{type} {rendered_props}/>'
    elif type in SVG_TAGS or type in CONTAINER_TAGS:
        rendered_children: list[str] | str

        if children:
            rendered_children = [
                render(n, ident=ident + 1)
                for n in children
            ]

            rendered_children = '\n'.join(rendered_children)
            rendered_node = f'{ident_str}<{type} {rendered_props}>\n{rendered_children}\n{ident_str}</{type}>'
        else:
            rendered_node = f'{ident_str}<{type} {rendered_props}></{type}>'
    elif isinstance(node, AbstractContextManager):
        print('!' * 80)
        raise ValueError(node)
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
