from .state import state, _T


def session_storage(key: str, value: _T) -> _T:
    """
    Creates a reactive state object synchronized with the browser's session storage.

    This function initializes a reactive value tied to a given key in session storage.
    The value is preserved across page reloads during the same browser session, but
    will be cleared once the tab or window is closed.

    Args:
        key (str): The session storage key to associate with the value.
        value (_T): The default value to use if no value exists in session storage.

    Returns:
        _T: A reactive value linked to the specified session storage key.

    Example:
    .. code-block:: python

        from instaui import ui, html

        @ui.page('/')
        def index():
            name = ui.session_storage("username", "")
            html.input(name)
    """
    return state(value, storage="session", storage_key=key)
