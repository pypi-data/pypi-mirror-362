from .state import state, _T


def local_storage(key: str, value: _T) -> _T:
    """
    Creates a reactive state object synchronized with the browser's local storage.

    This function initializes a reactive value tied to a given key in local storage.
    The state persists across page reloads and retains its value between sessions
    on the same browser and device.

    Args:
        key (str): The local storage key to associate with the value.
        value (_T): The default value to use if no value exists in local storage.

    Returns:
        _T: A reactive value linked to the specified local storage key.

    Example:
    .. code-block:: python

        from instaui import ui, html

        @ui.page('/')
        def index():
            name = ui.local_storage("username", "")
            html.input(name)
    """

    return state(value, storage="local", storage_key=key)
