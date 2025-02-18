# CHANGELOG

## v0.3.0a

Changed:
  - Replaced pyscript/micropython with Brython

## v0.2.9

Changed:
  - Updated all requirements

## v0.2.8

Changed:
  - `esbuild` disable `sourcemap`.

## v0.2.7

Changed:
  - Current working dir in `create_aiohttp_app`.
  - Print error in `install_npm_package`.

## v0.2.6

Changed:
  - For deployments, tolerate missing `nodejs` binaries.

## v0.2.5

Fixed:
  - Do not try to include: `os` and `time` packages/modules.

## v0.2.4

Added:
  - Demo 3: Reactive Notes example

Fixed:
  - Issue with `aaa` demo package.

## v0.2.3

Changed:
  - `starter.py` does not delete `TemporaryDirectory`

## v0.2.2

Added:
  - Demo 2: Alpine.js demo, looping messages, handling events.

Fixed:
  - PyPI project page.

## v0.2.1

Added:
  - Support for client side imports and modules.

Changed:
  - npm packages built and copied into `static/__npm__` dir
  - micropython stubs packages copied into `static/__mpy__` dir
  - user app modules/packages copied into `static/__app__` dir
  - Reimplemented simplified examples `demo_0` and `demo_1`.

## v0.2.0

Changed:
  - Redefined/reimplemented API and whole library.

## v0.1.13

Added:
* Component: `ComponentLibrary.__getattr__` method.
* Pico: `Page.__init__` got Modal JS script.
* Pico: `Page.__init__` got Checkbox indeterminate JS script.
* Pico: Module's `__all__` variable.
* Pico: Example `pico_1.py`, chat UI.
* Html5: `Section` component.
* Pico: `Section` component.

Fixed:
* Html5: Usage of `default_attrs` in `Component.__init__`.
* Html5: Properly implemented `Text` component.
* Pico: Removed conflicting `class Link(html5.A): pass`. Only use `p.A`.
* Html5: Void elements `Hr`, `Br`.

Removed:
* Pico: `SubmitInput`, `ButtonLink`, `SecondaryButtonLink`, `ContrastButtonLink` components.
* Pico: `OutlineButtonLink`, `SecondaryOutlineButtonLink`, `ContrastOutlineButtonLink` components.
* Html5: `Html5.__getattr__` method.
* DaisyUI: `DaisyUI.__getattr__` method.
* Pico: `Pico.__getattr__` method.
* Pico: `SecondaryLink`, `ContrastLink` components

## v0.1.12

Added:
* Html5: `Style`, `Svg`, `Aside` components.
* Html5: `Progress`, `Br`, `Hr` components.
* Pico: `A`, `Nav`, `Dialog` components.
* Pico: `Html`, `Head`, `Meta`, `Link`, `Title`, `Script`, `Style`, `Body`, `Svg`, `Aside` components.
* Pico: `Progress`, `Br`, `Hr` components.
* Pico: Renamed `hello_world_pico_0` to `pico_0`.
* Pico: `hello_world_pico_0` complete example with all components https://picocss.com.
* README: Updated examples section.
* Pico/Html5: Input checkbox, indeterminate=true, https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Input/checkbox#indeterminate

## v0.1.11

Added:
* Html5: Special case `Label` component `for_` attribute.
* Html5: `Form`, `Label`, `Select`, `Option`, `Fieldset`, `Legend` components.
* Pico: `Form`, `Label`, `Input`, `Select`, `Option`, `Fieldset`, `Legend`, `Text` components.
* Html5: `Figure`, `Table`, `THead`, `TR`, `TH`, `TBody`, `TD`, `TFoot` components.
* Pico: `Figure`, `Table` components.
* Html5: `Details`, `Summary` component.
* Html5: `Article` component.
* Pico: `Details`, `Summary`, `Ul`, `Li` component.
* Pico: `Article`, `Header`, `Footer` component.

Changed:
* Html5: Rename `content` prop/attr to be `data`. https://dom.spec.whatwg.org/#text

## v0.1.10

Added:
* Html5: `HGroup` component.
* Pico: `Grid`, `H1`, `H2`, `H3`, `H4`, `H5`, `H6` components.
* Pico: `HGroup`, `Headings` components.
* Pico: `Link`, `SecondaryLink`, `ContrastLink` components.
* Html5: `Abbr`, `B`, `I`, `Cite`, `Del`, `Ins`, `Kbd` components.
* Html5: `Mark`, `S`, `Small`, `Sub`, `Sup`, `U` components.
* Pico: `Abbr`, `Strong`, `B`, `I`, `Em`, `Cite`, `Del`, `Ins` components.
* Pico: `Mark`, `S`, `Small`, `Sub`, `Sup`, `U` components.
* Pico: `BlockQuote`, `Footer` components.
* Html5: `Input` component.
* Pico: `Button`, `SubmitInput` components.
* Pico: `ButtonLink`, `SecondaryButtonLink`, `ContrastButtonLink` components.
* Pico: `OutlineButtonLink`, `SecondaryOutlineButtonLink`, `ContrastOutlineButtonLink` components.

Changed:
* Component: `content` arg/attr is empty string `''` instead of `None`.
* Component: `render` method.

## v0.1.9

Added:
* Html5: `debug` extension for `htmx`.
* Html5: Added `Main` component.
* Pico: Added `Pico` component library.
* Pico: Added `Page`, `Main`, `Grid` components.
* Html5: Added `H5`, `H6` components.

## v0.1.8

Added:
* Gladius: `SF-Session-ID` header.
* Component: `sf-session-id` attr on `html` element.
* Html5: use `idiomorph` library as the swapping mechanism in `htmx`.

Changed:
* Gladius: Redefined `Event` to allow future definition of `Web Event`.
* DaisyUI: `Navbar` based on `html5.Div`, with custom `add` method.
* Html5: Swap only body on any event and optimize DOM update using `idiomorph`.
* Html5: Rename `sf_id` to `g_id`.
* Html5: Rename `sf_session_id` to `g_session_id`.
* Html5: Rename `SF-Session-ID` to `G-Session-ID`.
* HTML5, DaisyUI: Rename `default_tag` to `tag`.
* HTML5, DaisyUI: moved `htmx` scripts from DaisyUI to Html5.

Removed:
* consts: `_ontextchanged`, `_ontablechanged`.

## v0.1.7

Added:
* Component: `remove` child method.
* Component: `clone` method, with support for shallow and deep cloning.

Changed:
* DaisyUI: Upgraded from version `3.7.7` to `3.8.0`.
* Component: Simplified `Component.__init__` using `set_attr`.

Fixed:
* Component: `set_attr`, takes care of `class` and `id` attrs.
* CHANGELOG: fixed list markdown.

## v0.1.6

Added:
* HTML5: `set_attr`, `set_attr`, `del_attr`, `has_attr` methods.
* HTML5: High-level `Page` component.
* Example: `hello_world_2.py`.

Changed:
* DaisyUI: `Page` extends `html5.Page`.

Fixed:
* Component: do not attach `htmx` attributes for: html, head, meta, title, link, script, body, button, a, input, textarea
* DaisyUI: `NavbarButton` extends `html5.A`.
* DaisyUI: `Text` extends `html5.Span`.
* Html5: `hx-boots` on body.
* DaisyUI: `ht-target` attr added on `Navbar` and `Join` children.

## v0.1.5

Changed:
* Tailwind: Plugin `line-clamp` is included by default from Tailwind v3.3.
* Component: can be triggered now on custom event `_contentchange`.

Removed:
* Component: Removed need for `TextContentComponent`.

## v0.1.4

Added:
* Component: Added `TextContentComponent` for components that have text content in constructor.
* HTML5: H1, H2, H3, H4, P, BlockQuote, Figure, FigCaption, Strong, Em, Code.
* HTML5: Pre, Ol, Ul, Li, Table, THead, Tr, Th, Td, Img, Video, Source, Hr.
* HTML5: Button.
* DaisyUI: Hero, HeroContent.
* DaisyUI: Indicator, IndicatorItem.
* DaisyUI: Stack.
* DaisyUI: Toast, Alert.
* Examples: Layout.

Changed:
* Tailwind Plugins: forms, typography, aspect-ratio, line-clamp.
* DaisyUI: Button, support for text label in constructor.
* HTML5: Span is subclass of TextContentComponent.
* Component: `Component` go all features from `TextContentComponent`.

Removed:
* Examples: Artboard, Divider, Footer.

## v0.1.3

Added:
* Component: `add_class`, `remove_class`, `has_class` methods.
* DaisyUI: NavbarButton, Artboard, Divider, Footer, FooterTitle components.
* HTML5: A, Footer, Nav, Header.

Changed:
* Examples, rename `dui` to `d`.
* Rename `prop{s}` to `attr{s}` because of HTML convention.
* Rename attr `sf_id` to be `sf-id`.
* Renamed `EventRequest` to `Event`.
* Updated DaisyUI from `2.6.0` to `3.7.7`.
* DaisyUI: `Join` component adds default class `join-item` to its children.

Fixed:
* Component registration of ComponentLibrary's sub-classes.
* Read `event: Event` from HTTP headers, and pass to callback.

## v0.1.2

Added:
* HTML5 Components: Html, Head, Meta, Link, Title, Script, Body, Div, Span.
* Added example: hello_world_1.

Changed:
* Component uses `hx-target='[sf_id="ID"]'` instead of `hx-target="#ID"`.
* Moved Html5 Components into independent module `html5`.

Fixed:
* Cyclic reference imports.
* Fixed examples: multi_page_0, hello_world_0.

## v0.1.1

Fixed:
* Text got custom event `_ontextchange`, so it can detect changes.

## v0.1.0

Added:
* Initial version based on aiohttp, uvloop, htmx, TailwindCSS, DaisyUI.
