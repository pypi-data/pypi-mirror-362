from typing import Any

import air

from . import styles
from .utils import stringify


def Button(
    *content: Any,
    class_: str | list[str] | None = styles.buttons.primary,
    **kwargs: Any,
) -> air.Tag:
    """
    Args:
        content: The content of the button.
        class_: The class of the button.
        **kwargs: Additional keyword arguments passed to the button tag.

    Returns:
        air.Tag: The button tag.

    Example:
        Button("Click me", class_=styles.buttons.primary)
    """
    return air.Button(*content, class_=stringify(styles.buttons.base, class_), **kwargs)


def H1(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """
    Args:
        content: The content of the h1 tag.
        class_: The class of the h1 tag.
        **kwargs: Additional keyword arguments passed to the h1 tag.

    Returns:
        air.Tag: The h1 tag.

    Example:
        H1("Hello, world!")
    """
    return air.H1(*content, class_=stringify(styles.typography.h1, class_), **kwargs)


def H2(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """
    Args:
        content: The content of the h2 tag.
        class_: The class of the h2 tag.
        **kwargs: Additional keyword arguments passed to the h2 tag.

    Returns:
        air.Tag: The h2 tag.

    Example:
        H2("Hello, world!")
    """
    return air.H2(*content, class_=stringify(styles.typography.h2, class_), **kwargs)


def H3(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """
    Args:
        content: The content of the h3 tag.
        class_: The class of the h3 tag.
        **kwargs: Additional keyword arguments passed to the h3 tag.

    Returns:
        air.Tag: The h3 tag.

    Example:
        H3("Hello, world!")
    """
    return air.H3(*content, class_=stringify(styles.typography.h3, class_), **kwargs)


def H4(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.H4(*content, class_=stringify(styles.typography.h4, class_), **kwargs)


def H5(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.H5(*content, class_=stringify(styles.typography.h5, class_), **kwargs)


def H6(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.H6(*content, class_=stringify(styles.typography.h6, class_), **kwargs)


def Body(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Body(*content, class_=stringify(styles.Theme.body, class_), **kwargs)


# Semantic HTML Elements


def Strong(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Strong(*content, class_=stringify(styles.typography.strong, class_), **kwargs)


def I(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.I(*content, class_=stringify(styles.typography.i, class_), **kwargs)


def Small(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Small(*content, class_=stringify(styles.typography.small, class_), **kwargs)


def Del(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Del(*content, class_=stringify(styles.typography.del_, class_), **kwargs)


def Abbr(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """
    Args:
        content: The content of the abbr tag.
        class_: The class of the abbr tag.
        **kwargs: Additional keyword arguments passed to the abbr tag.

    Returns:
        air.Tag: The abbr tag.

    Example:
        Abbr("HTML", title="Hyper Text Markup Language")
    """
    return air.Abbr(*content, class_=stringify(styles.typography.abbr, class_), **kwargs)


def Var(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Var(*content, class_=stringify(styles.typography.var, class_), **kwargs)


def Mark(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Mark(*content, class_=stringify(styles.typography.mark, class_), **kwargs)


def Time(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Time(*content, class_=stringify(styles.typography.time, class_), **kwargs)


def Code(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Code(*content, class_=stringify(styles.typography.code, class_), **kwargs)


def Pre(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Pre(*content, class_=stringify(styles.typography.pre, class_), **kwargs)


def Kbd(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Kbd(*content, class_=stringify(styles.typography.kbd, class_), **kwargs)


def Samp(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Samp(*content, class_=stringify(styles.typography.samp, class_), **kwargs)


def Blockquote(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Blockquote(*content, class_=stringify(styles.typography.blockquote, class_), **kwargs)


def Cite(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Cite(*content, class_=stringify(styles.typography.cite, class_), **kwargs)


def Address(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Address(*content, class_=stringify(styles.typography.address, class_), **kwargs)


def Hr(class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Hr(class_=stringify(styles.typography.hr, class_), **kwargs)


def Details(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Details(*content, class_=stringify(styles.typography.details, class_), **kwargs)


def Summary(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Summary(*content, class_=stringify(styles.typography.summary, class_), **kwargs)


def Dl(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Dl(*content, class_=stringify(styles.typography.dl, class_), **kwargs)


def Dt(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Dt(*content, class_=stringify(styles.typography.dt, class_), **kwargs)


def Dd(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Dd(*content, class_=stringify(styles.typography.dd, class_), **kwargs)


def Figure(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Figure(*content, class_=stringify(styles.typography.figure, class_), **kwargs)


def Figcaption(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Figcaption(*content, class_=stringify(styles.typography.figcaption, class_), **kwargs)


# Table elements with styling


def Table(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """Styled table element."""
    return air.Table(*content, class_=stringify(styles.tables.table, class_), **kwargs)


def Thead(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """Styled table head element."""
    return air.Thead(*content, class_=stringify(styles.tables.thead, class_), **kwargs)


def Tbody(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """Styled table body element."""
    return air.Tbody(*content, class_=stringify(styles.tables.tbody, class_), **kwargs)


def Tfoot(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """Styled table footer element."""
    return air.Tfoot(*content, class_=stringify(styles.tables.tfoot, class_), **kwargs)


def Tr(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """Styled table row element."""
    return air.Tr(*content, class_=stringify(styles.tables.tr, class_), **kwargs)


def Th(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """Styled table header cell element."""
    return air.Th(*content, class_=stringify(styles.tables.th, class_), **kwargs)


def Td(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    """Styled table data cell element."""
    return air.Td(*content, class_=stringify(styles.tables.td, class_), **kwargs)


def Ul(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Ul(*content, class_=stringify(styles.lists.ul, class_), **kwargs)


def Ol(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Ol(*content, class_=stringify(styles.lists.ol, class_), **kwargs)


def Li(*content: Any, class_: str | list[str] | None = None, **kwargs: Any) -> air.Tag:
    return air.Li(*content, class_=stringify(styles.lists.li, class_), **kwargs)



# Pass-through tags from air.tags
# Import all standard HTML tags that don't have custom styling
