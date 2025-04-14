__all__ = ['h', 'render', 'register']

import json
import inspect
from typing import Any, Union, Callable, TypedDict

from .defs import SVG_TAGS, VOID_TAGS, CONTAINER_TAGS


class HNode(TypedDict):
    type: str | Callable[[dict[str, Any]], 'HNode']
    props: dict[str, Any] | None
    children: list[Union[str, 'HNode']]


'''
def h(type: str | Callable[[dict[str, Any]], HNode], props: dict[str, Any] | None, *children) -> HNode:
    return HNode(
        type=type,
        props=props,
        children=children, # type: ignore
    )
'''
class H:
    registered_elements: dict[str, Any]


    def __init__(self):
        self.registered_elements = {}


    def __call__(self, type: str | Callable[[dict[str, Any]], HNode], props: dict[str, Any] | None, *children) -> HNode:
        return HNode(
            type=type,
            props=props,
            children=children, # type: ignore
        )


    def __getattr__(self, attr: str) -> Callable[[dict[str, Any] | None], HNode]:
        def _code_fn(props: dict[str, Any] | None=None, *children) -> HNode:
            type: str | Callable[[dict[str, Any]], HNode]

            if attr in self.registered_elements:
                type = self.registered_elements[attr]
            else:
                type = attr

            return HNode(
                type=type,
                props=props,
                children=children, # type: ignore
            )

        return _code_fn


    def register(self, fn: Callable):
        self.registered_elements[fn.__name__] = fn
        return fn


h = H()
register = h.register


def render(node: HNode, ident: int=0) -> str:
    type: str | Callable[[dict[str, Any]], HNode] = node['type']
    props: dict[str, Any] | None = node['props']
    rendered_props: list[str] | str
    rendered_node: str
    ident_str: str = " " * (ident * 2)

    if props:
        rendered_props = [f'{k}={json.dumps(v)}' for k, v in props.items()]
        rendered_props = ' '.join(rendered_props)
    else:
        rendered_props = ''

    if type in VOID_TAGS:
        rendered_node = f'{ident_str}<{type} {rendered_props}/>'
    elif type in SVG_TAGS or type in CONTAINER_TAGS:
        children: list[Union[str, HNode]] = node['children']
        rendered_children: list[str] | str
        text_ident_str: str = " " * ((ident + 1) * 2)

        if children:
            rendered_children = [
                render(n, ident=ident + 1) if isinstance(n, dict) else f'{text_ident_str}{n}'
                for n in children
            ]

            rendered_children = '\n'.join(rendered_children)
            rendered_node = f'{ident_str}<{type} {rendered_props}>\n{rendered_children}\n{ident_str}</{type}>'
        else:
            rendered_node = f'{ident_str}<{type} {rendered_props}></{type}>'
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
