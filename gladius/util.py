__all__ = [
    'make_page',
]

from .element import Element
from .gladius import Gladius


def make_page(
    g: Gladius,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    favicon: str | tuple | list | dict | Element='/static/img/favicon.png',
    links: list[str | tuple | list | dict | Element]=[],
    scripts: list[str | tuple | list | dict | Element]=[],
) -> Element:
    el: Element

    with g.html(lang=lang) as el:
        with g.head() as head:
            g.meta(charset='utf-8')
            g.meta(name='viewport', content='width=device-width, initial-scale=1')
            g.title(title)
            g.meta(name='description', content=description)

            # favicon
            if isinstance(favicon, str):
                g.link(rel='icon', href=favicon, type='image/png')
            elif isinstance(favicon, (tuple, list)):
                assert 1 <= len(favicon) <= 2

                if len(favicon) == 1:
                    href = favicon[0]
                    g.link(rel='icon', href=href, type='image/png')
                elif len(favicon) == 2:
                    href, type_ = favicon
                    g.link(rel='icon', href=href, type=type_)
            elif isinstance(favicon, dict):
                g.link(**favicon)
            elif isinstance(favicon, Element):
                head.add(favicon)

            # links
            for n in links:
                if isinstance(n, str):
                    g.link(rel='stylesheet', href=n)
                elif isinstance(n, (tuple, list)):
                    assert 1 <= len(n) <= 2

                    if len(n) == 1:
                        href = n[0]
                        g.link(rel='stylesheet', href=href)
                    elif len(n) == 2:
                        rel, href = n
                        g.link(rel=rel, href=href)
                elif isinstance(n, dict):
                    g.link(**n)
                elif isinstance(n, Element):
                    head.add(n)

            # scripts
            for n in scripts:
                if isinstance(n, str):
                    g.script(src=n)
                elif isinstance(n, (tuple, list)):
                    assert 1 <= len(n) <= 2

                    if len(n) == 1:
                        src = n[0]
                        g.script(src=src)
                    elif len(n) == 2:
                        src, defer = n
                        g.script(src=src, defer=defer)
                elif isinstance(n, dict):
                    g.script(**n)
                elif isinstance(n, Element):
                    head.add(n)

    return el
