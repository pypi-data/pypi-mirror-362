from urllib.parse import urlparse
from instaui.vars.mixin_types.element_binding import ElementBindingMixin
from instaui.vars.js_computed import JsComputed
from instaui.js.fn import JsFn

_complete_src_js_fn: JsFn = None  # type: ignore


def complete_src_computed(src: ElementBindingMixin):
    global _complete_src_js_fn

    if _complete_src_js_fn is None:
        _complete_src_js_fn = JsFn(
            code=r"""src=>{
            try {
                new URL(src);
                return src;
            } catch {
                if (!src.startsWith('/assets')) {
                src = src.startsWith('/')
                    ? '/assets' + src
                    : '/assets/' + src;
                }
                return src;
            }                   
            }""",
            global_scope=True,
        )

    return JsComputed(
        inputs=[src, _complete_src_js_fn],
        code=r"""(src,fn)=> fn(src)""",
    )


def complete_src(src: str) -> str:
    parsed = urlparse(src)

    if not parsed.scheme:
        if not src.startswith("/assets"):
            src = "/assets" + src if src.startswith("/") else "/assets/" + src
    return src
