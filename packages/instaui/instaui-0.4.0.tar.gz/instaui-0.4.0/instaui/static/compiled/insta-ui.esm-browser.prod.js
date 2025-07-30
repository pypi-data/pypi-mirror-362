var or = Object.defineProperty;
var sr = (e, t, n) => t in e ? or(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var M = (e, t, n) => sr(e, typeof t != "symbol" ? t + "" : t, n);
import * as ir from "vue";
import { unref as L, onMounted as ar, nextTick as me, ref as J, readonly as an, getCurrentInstance as bt, watch as q, getCurrentScope as cr, onScopeDispose as ur, isRef as St, shallowRef as K, watchEffect as cn, computed as B, toRaw as un, customRef as ae, toValue as ke, provide as ge, inject as Y, shallowReactive as lr, defineComponent as W, reactive as fr, h as D, onUnmounted as dr, renderList as hr, TransitionGroup as ln, cloneVNode as je, withDirectives as fn, withModifiers as pr, normalizeStyle as gr, normalizeClass as Me, toDisplayString as Ue, vModelDynamic as mr, vShow as vr, resolveDynamicComponent as yr, normalizeProps as wr, onErrorCaptured as Er, openBlock as ee, createElementBlock as ie, createElementVNode as dn, createVNode as _r, createCommentVNode as st, createBlock as hn, Teleport as br, renderSlot as Sr, toRef as de, useAttrs as Rr, Fragment as pn, mergeProps as Pr, KeepAlive as Or } from "vue";
let gn;
function Nr(e) {
  gn = e;
}
function it() {
  return gn;
}
function We() {
  const { queryPath: e, pathParams: t, queryParams: n } = it();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
const Rt = /* @__PURE__ */ new Map();
function kr(e) {
  var t;
  (t = e.scopes) == null || t.forEach((n) => {
    Rt.set(n.id, n);
  });
}
function Ze(e) {
  return Rt.get(e);
}
function Ae(e) {
  return e && Rt.has(e);
}
function Cr(e) {
  return cr() ? (ur(e), !0) : !1;
}
function re(e) {
  return typeof e == "function" ? e() : L(e);
}
const Vr = typeof window < "u" && typeof document < "u";
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const Ar = Object.prototype.toString, Ir = (e) => Ar.call(e) === "[object Object]", Fe = () => {
};
function $r(e, t) {
  function n(...r) {
    return new Promise((o, s) => {
      Promise.resolve(e(() => t.apply(this, r), { fn: t, thisArg: this, args: r })).then(o).catch(s);
    });
  }
  return n;
}
const mn = (e) => e();
function xr(e = mn) {
  const t = J(!0);
  function n() {
    t.value = !1;
  }
  function r() {
    t.value = !0;
  }
  const o = (...s) => {
    t.value && e(...s);
  };
  return { isActive: an(t), pause: n, resume: r, eventFilter: o };
}
function at(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function Tr(e) {
  return bt();
}
function Dr(e, t, n = {}) {
  const {
    eventFilter: r = mn,
    ...o
  } = n;
  return q(
    e,
    $r(
      r,
      t
    ),
    o
  );
}
function jr(e, t, n = {}) {
  const {
    eventFilter: r,
    ...o
  } = n, { eventFilter: s, pause: a, resume: u, isActive: l } = xr(r);
  return { stop: Dr(
    e,
    t,
    {
      ...o,
      eventFilter: s
    }
  ), pause: a, resume: u, isActive: l };
}
function Mr(e, t = !0, n) {
  Tr() ? ar(e, n) : t ? e() : me(e);
}
function ct(e, t = !1) {
  function n(i, { flush: f = "sync", deep: h = !1, timeout: g, throwOnTimeout: m } = {}) {
    let v = null;
    const _ = [new Promise((S) => {
      v = q(
        e,
        (k) => {
          i(k) !== t && (v ? v() : me(() => v == null ? void 0 : v()), S(k));
        },
        {
          flush: f,
          deep: h,
          immediate: !0
        }
      );
    })];
    return g != null && _.push(
      at(g, m).then(() => re(e)).finally(() => v == null ? void 0 : v())
    ), Promise.race(_);
  }
  function r(i, f) {
    if (!St(i))
      return n((k) => k === i, f);
    const { flush: h = "sync", deep: g = !1, timeout: m, throwOnTimeout: v } = f ?? {};
    let w = null;
    const S = [new Promise((k) => {
      w = q(
        [e, i],
        ([I, j]) => {
          t !== (I === j) && (w ? w() : me(() => w == null ? void 0 : w()), k(I));
        },
        {
          flush: h,
          deep: g,
          immediate: !0
        }
      );
    })];
    return m != null && S.push(
      at(m, v).then(() => re(e)).finally(() => (w == null || w(), re(e)))
    ), Promise.race(S);
  }
  function o(i) {
    return n((f) => !!f, i);
  }
  function s(i) {
    return r(null, i);
  }
  function a(i) {
    return r(void 0, i);
  }
  function u(i) {
    return n(Number.isNaN, i);
  }
  function l(i, f) {
    return n((h) => {
      const g = Array.from(h);
      return g.includes(i) || g.includes(re(i));
    }, f);
  }
  function d(i) {
    return c(1, i);
  }
  function c(i = 1, f) {
    let h = -1;
    return n(() => (h += 1, h >= i), f);
  }
  return Array.isArray(re(e)) ? {
    toMatch: n,
    toContains: l,
    changed: d,
    changedTimes: c,
    get not() {
      return ct(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: s,
    toBeNaN: u,
    toBeUndefined: a,
    changed: d,
    changedTimes: c,
    get not() {
      return ct(e, !t);
    }
  };
}
function Wr(e) {
  return ct(e);
}
function Fr(e, t, n) {
  let r;
  St(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: a = !0,
    onError: u = Fe
  } = r, l = J(!o), d = a ? K(t) : J(t);
  let c = 0;
  return cn(async (i) => {
    if (!l.value)
      return;
    c++;
    const f = c;
    let h = !1;
    s && Promise.resolve().then(() => {
      s.value = !0;
    });
    try {
      const g = await e((m) => {
        i(() => {
          s && (s.value = !1), h || m();
        });
      });
      f === c && (d.value = g);
    } catch (g) {
      u(g);
    } finally {
      s && f === c && (s.value = !1), h = !0;
    }
  }), o ? B(() => (l.value = !0, d.value)) : d;
}
const ut = Vr ? window : void 0;
function Lr(e) {
  var t;
  const n = re(e);
  return (t = n == null ? void 0 : n.$el) != null ? t : n;
}
function $t(...e) {
  let t, n, r, o;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([n, r, o] = e, t = ut) : [t, n, r, o] = e, !t)
    return Fe;
  Array.isArray(n) || (n = [n]), Array.isArray(r) || (r = [r]);
  const s = [], a = () => {
    s.forEach((c) => c()), s.length = 0;
  }, u = (c, i, f, h) => (c.addEventListener(i, f, h), () => c.removeEventListener(i, f, h)), l = q(
    () => [Lr(t), re(o)],
    ([c, i]) => {
      if (a(), !c)
        return;
      const f = Ir(i) ? { ...i } : i;
      s.push(
        ...n.flatMap((h) => r.map((g) => u(c, h, g, f)))
      );
    },
    { immediate: !0, flush: "post" }
  ), d = () => {
    l(), a();
  };
  return Cr(d), d;
}
function Br(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = Fe,
    onSuccess: a = Fe,
    resetOnExecute: u = !0,
    shallow: l = !0,
    throwError: d
  } = {}, c = l ? K(t) : J(t), i = J(!1), f = J(!1), h = K(void 0);
  async function g(w = 0, ..._) {
    u && (c.value = t), h.value = void 0, i.value = !1, f.value = !0, w > 0 && await at(w);
    const S = typeof e == "function" ? e(..._) : e;
    try {
      const k = await S;
      c.value = k, i.value = !0, a(k);
    } catch (k) {
      if (h.value = k, s(k), d)
        throw k;
    } finally {
      f.value = !1;
    }
    return c.value;
  }
  r && g(o);
  const m = {
    state: c,
    isReady: i,
    isLoading: f,
    error: h,
    execute: g
  };
  function v() {
    return new Promise((w, _) => {
      Wr(f).toBe(!1).then(() => w(m)).catch(_);
    });
  }
  return {
    ...m,
    then(w, _) {
      return v().then(w, _);
    }
  };
}
const xe = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof global < "u" ? global : typeof self < "u" ? self : {}, Te = "__vueuse_ssr_handlers__", Ur = /* @__PURE__ */ Hr();
function Hr() {
  return Te in xe || (xe[Te] = xe[Te] || {}), xe[Te];
}
function zr(e, t) {
  return Ur[e] || t;
}
function Gr(e) {
  return e == null ? "any" : e instanceof Set ? "set" : e instanceof Map ? "map" : e instanceof Date ? "date" : typeof e == "boolean" ? "boolean" : typeof e == "string" ? "string" : typeof e == "object" ? "object" : Number.isNaN(e) ? "any" : "number";
}
const Kr = {
  boolean: {
    read: (e) => e === "true",
    write: (e) => String(e)
  },
  object: {
    read: (e) => JSON.parse(e),
    write: (e) => JSON.stringify(e)
  },
  number: {
    read: (e) => Number.parseFloat(e),
    write: (e) => String(e)
  },
  any: {
    read: (e) => e,
    write: (e) => String(e)
  },
  string: {
    read: (e) => e,
    write: (e) => String(e)
  },
  map: {
    read: (e) => new Map(JSON.parse(e)),
    write: (e) => JSON.stringify(Array.from(e.entries()))
  },
  set: {
    read: (e) => new Set(JSON.parse(e)),
    write: (e) => JSON.stringify(Array.from(e))
  },
  date: {
    read: (e) => new Date(e),
    write: (e) => e.toISOString()
  }
}, xt = "vueuse-storage";
function Tt(e, t, n, r = {}) {
  var o;
  const {
    flush: s = "pre",
    deep: a = !0,
    listenToStorageChanges: u = !0,
    writeDefaults: l = !0,
    mergeDefaults: d = !1,
    shallow: c,
    window: i = ut,
    eventFilter: f,
    onError: h = (V) => {
      console.error(V);
    },
    initOnMounted: g
  } = r, m = (c ? K : J)(typeof t == "function" ? t() : t);
  if (!n)
    try {
      n = zr("getDefaultStorage", () => {
        var V;
        return (V = ut) == null ? void 0 : V.localStorage;
      })();
    } catch (V) {
      h(V);
    }
  if (!n)
    return m;
  const v = re(t), w = Gr(v), _ = (o = r.serializer) != null ? o : Kr[w], { pause: S, resume: k } = jr(
    m,
    () => j(m.value),
    { flush: s, deep: a, eventFilter: f }
  );
  i && u && Mr(() => {
    n instanceof Storage ? $t(i, "storage", le) : $t(i, xt, be), g && le();
  }), g || le();
  function I(V, T) {
    if (i) {
      const H = {
        key: e,
        oldValue: V,
        newValue: T,
        storageArea: n
      };
      i.dispatchEvent(n instanceof Storage ? new StorageEvent("storage", H) : new CustomEvent(xt, {
        detail: H
      }));
    }
  }
  function j(V) {
    try {
      const T = n.getItem(e);
      if (V == null)
        I(T, null), n.removeItem(e);
      else {
        const H = _.write(V);
        T !== H && (n.setItem(e, H), I(T, H));
      }
    } catch (T) {
      h(T);
    }
  }
  function U(V) {
    const T = V ? V.newValue : n.getItem(e);
    if (T == null)
      return l && v != null && n.setItem(e, _.write(v)), v;
    if (!V && d) {
      const H = _.read(T);
      return typeof d == "function" ? d(H, v) : w === "object" && !Array.isArray(H) ? { ...v, ...H } : H;
    } else return typeof T != "string" ? T : _.read(T);
  }
  function le(V) {
    if (!(V && V.storageArea !== n)) {
      if (V && V.key == null) {
        m.value = v;
        return;
      }
      if (!(V && V.key !== e)) {
        S();
        try {
          (V == null ? void 0 : V.newValue) !== _.write(m.value) && (m.value = U(V));
        } catch (T) {
          h(T);
        } finally {
          V ? me(k) : k();
        }
      }
    }
  }
  function be(V) {
    le(V.detail);
  }
  return m;
}
function z(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), ir];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function qr(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return z(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function vn(e) {
  return e.constructor.name === "AsyncFunction";
}
class Jr {
  toString() {
    return "";
  }
}
const Ce = new Jr();
function Ve(e) {
  return un(e) === Ce;
}
function Qr(e) {
  return Array.isArray(e) && e[0] === "bind";
}
function Yr(e) {
  return e[1];
}
function yn(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...s] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + s[0];
      case "~+":
        return s[0] + e;
    }
  }
  const r = wn(t, n);
  return e[r];
}
function wn(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      if (!t)
        throw new Error("No bindable function provided");
      return t(r[0]);
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function En(e, t, n) {
  return t.reduce(
    (r, o) => yn(r, o, n),
    e
  );
}
function _n(e, t, n, r) {
  t.reduce((o, s, a) => {
    if (a === t.length - 1)
      o[wn(s, r)] = n;
    else
      return yn(o, s, r);
  }, e);
}
function Xr(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: a } = t;
  return r === void 0 || r.length === 0 ? e : ae(() => ({
    get() {
      try {
        return En(
          ke(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(u) {
      _n(
        ke(e),
        s || r,
        u,
        a
      );
    }
  }));
}
function Dt(e, t) {
  return !Ve(e) && JSON.stringify(t) === JSON.stringify(e);
}
function Pt(e) {
  if (St(e)) {
    const t = e;
    return ae(() => ({
      get() {
        return ke(t);
      },
      set(n) {
        const r = ke(t);
        Dt(r, n) || (t.value = n);
      }
    }));
  }
  return ae((t, n) => ({
    get() {
      return t(), e;
    },
    set(r) {
      Dt(e, r) || (e = r, n());
    }
  }));
}
function Zr(e, t) {
  const { deepCompare: n = !1, storage: r } = e, o = r ? eo(r, e.value) : e.value;
  return n ? Pt(o) : J(o);
}
function eo(e, t) {
  const { type: n, key: r } = e;
  return n === "local" ? Tt(r, t) : Tt(r, t, sessionStorage);
}
function to(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, a = Object.values(r).map((c, i) => s[i] === 1 ? c : t.getVueRefObject(c));
  if (vn(new Function(o)))
    return Fr(
      async () => {
        const c = Object.fromEntries(
          Object.keys(r).map((i, f) => [i, a[f]])
        );
        return await z(o, c)();
      },
      null,
      { lazy: !0 }
    );
  const u = Object.fromEntries(
    Object.keys(r).map((c, i) => [c, a[i]])
  ), l = z(o, u);
  return B(l);
}
function no(e) {
  const { init: t, deepEqOnInput: n } = e;
  return n === void 0 ? K(t ?? Ce) : Pt(t ?? Ce);
}
function ro(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: s,
    data: a,
    asyncInit: u = null,
    deepEqOnInput: l = 0
  } = e, d = s || Array(r.length).fill(0), c = a || Array(r.length).fill(0), i = r.filter((v, w) => d[w] === 0 && c[w] === 0).map((v) => t.getVueRefObject(v));
  function f() {
    return r.map(
      (v, w) => c[w] === 1 ? v : t.getValue(v)
    );
  }
  const h = z(o), g = l === 0 ? K(Ce) : Pt(Ce), m = { immediate: !0, deep: !0 };
  return vn(h) ? (g.value = u, q(
    i,
    async () => {
      f().some(Ve) || (g.value = await h(...f()));
    },
    m
  )) : q(
    i,
    () => {
      const v = f();
      v.some(Ve) || (g.value = h(...v));
    },
    m
  ), an(g);
}
function oo(e) {
  return e.tag === "vfor";
}
function so(e) {
  return e.tag === "vif";
}
function io(e) {
  return e.tag === "match";
}
function bn(e) {
  return !("type" in e);
}
function ao(e) {
  return "type" in e && e.type === "rp";
}
function Ot(e) {
  return "sid" in e && "id" in e;
}
class co extends Map {
  constructor(t) {
    super(), this.factory = t;
  }
  getOrDefault(t) {
    if (!this.has(t)) {
      const n = this.factory();
      return this.set(t, n), n;
    }
    return super.get(t);
  }
}
function Nt(e) {
  return new co(e);
}
class uo {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, a = it().webServerInfo, u = s !== void 0 ? { key: s } : {}, l = r === "sync" ? a.event_url : a.event_async_url;
    let d = {};
    const c = await fetch(l, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: n,
        hKey: o,
        ...u,
        page: We(),
        ...d
      })
    });
    if (!c.ok)
      throw new Error(`HTTP error! status: ${c.status}`);
    return await c.json();
  }
  async watchSend(t) {
    const { fType: n, key: r } = t.watchConfig, o = it().webServerInfo, s = n === "sync" ? o.watch_url : o.watch_async_url, a = t.getServerInputs(), u = {
      key: r,
      input: a,
      page: We()
    };
    return await (await fetch(s, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(u)
    })).json();
  }
}
class lo {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, a = s !== void 0 ? { key: s } : {};
    let u = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...a,
      page: We(),
      ...u
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { fType: n, key: r } = t.watchConfig, o = t.getServerInputs(), s = {
      key: r,
      input: o,
      fType: n,
      page: We()
    };
    return await window.pywebview.api.watch_call(s);
  }
}
let lt;
function fo(e) {
  switch (e) {
    case "web":
      lt = new uo();
      break;
    case "webview":
      lt = new lo();
      break;
  }
}
function Sn() {
  return lt;
}
var Q = /* @__PURE__ */ ((e) => (e[e.Ref = 0] = "Ref", e[e.EventContext = 1] = "EventContext", e[e.Data = 2] = "Data", e[e.JsFn = 3] = "JsFn", e))(Q || {}), ft = /* @__PURE__ */ ((e) => (e.const = "c", e.ref = "r", e.range = "n", e))(ft || {}), pe = /* @__PURE__ */ ((e) => (e[e.Ref = 0] = "Ref", e[e.RouterAction = 1] = "RouterAction", e[e.ElementRefAction = 2] = "ElementRefAction", e[e.JsCode = 3] = "JsCode", e))(pe || {});
function ho(e, t) {
  const r = {
    ref: {
      id: t.id,
      sid: e
    },
    type: pe.Ref
  };
  return {
    ...t,
    immediate: !0,
    outputs: [r, ...t.outputs || []]
  };
}
function Rn(e) {
  const { config: t, varGetter: n } = e;
  if (!t)
    return {
      run: () => {
      },
      tryReset: () => {
      }
    };
  const r = t.map((a) => {
    const [u, l, d] = a, c = n.getVueRefObject(u);
    function i(f, h) {
      const { type: g, value: m } = h;
      if (g === "const") {
        f.value = m;
        return;
      }
      if (g === "action") {
        const v = po(m, n);
        f.value = v;
        return;
      }
    }
    return {
      run: () => i(c, l),
      reset: () => i(c, d)
    };
  });
  return {
    run: () => {
      r.forEach((a) => a.run());
    },
    tryReset: () => {
      r.forEach((a) => a.reset());
    }
  };
}
function po(e, t) {
  const { inputs: n = [], code: r } = e, o = z(r), s = n.map((a) => t.getValue(a));
  return o(...s);
}
function jt(e) {
  return e == null;
}
function He(e, t, n) {
  if (jt(t) || jt(e.values))
    return;
  t = t;
  const r = e.values, o = e.types ?? Array.from({ length: t.length }).fill(0);
  t.forEach((s, a) => {
    const u = o[a];
    if (u === 1)
      return;
    if (s.type === pe.Ref) {
      if (u === 2) {
        r[a].forEach(([c, i]) => {
          const f = s.ref, h = {
            ...f,
            path: [...f.path ?? [], ...c]
          };
          n.updateValue(h, i);
        });
        return;
      }
      n.updateValue(s.ref, r[a]);
      return;
    }
    if (s.type === pe.RouterAction) {
      const d = r[a], c = n.getRouter()[d.fn];
      c(...d.args);
      return;
    }
    if (s.type === pe.ElementRefAction) {
      const d = s.ref, c = n.getVueRefObject(d).value, i = r[a], { method: f, args: h = [] } = i;
      c[f](...h);
      return;
    }
    if (s.type === pe.JsCode) {
      const d = r[a];
      if (!d)
        return;
      const c = z(d);
      Promise.resolve(c());
      return;
    }
    const l = n.getVueRefObject(
      s.ref
    );
    l.value = r[a];
  });
}
function go(e) {
  const { watchConfigs: t, computedConfigs: n, varMapGetter: r, sid: o } = e;
  return new mo(t, n, r, o);
}
class mo {
  constructor(t, n, r, o) {
    M(this, "taskQueue", []);
    M(this, "id2TaskMap", /* @__PURE__ */ new Map());
    M(this, "input2TaskIdMap", Nt(() => []));
    this.varMapGetter = r;
    const s = [], a = (u) => {
      var d;
      const l = new vo(u, r);
      return this.id2TaskMap.set(l.id, l), (d = u.inputs) == null || d.forEach((c, i) => {
        var h, g;
        if (((h = u.data) == null ? void 0 : h[i]) === 0 && ((g = u.slient) == null ? void 0 : g[i]) === 0) {
          if (!bn(c))
            throw new Error("Non-var input bindings are not supported.");
          const m = `${c.sid}-${c.id}`;
          this.input2TaskIdMap.getOrDefault(m).push(l.id);
        }
      }), l;
    };
    t == null || t.forEach((u) => {
      const l = a(u);
      s.push(l);
    }), n == null || n.forEach((u) => {
      const l = a(
        ho(o, u)
      );
      s.push(l);
    }), s.forEach((u) => {
      const {
        deep: l = !0,
        once: d,
        flush: c,
        immediate: i = !0
      } = u.watchConfig, f = {
        immediate: i,
        deep: l,
        once: d,
        flush: c
      }, h = this._getWatchTargets(u);
      q(
        h,
        (g) => {
          g.some(Ve) || (u.modify = !0, this.taskQueue.push(new yo(u)), this._scheduleNextTick());
        },
        f
      );
    });
  }
  _getWatchTargets(t) {
    if (!t.watchConfig.inputs)
      return [];
    const n = t.slientInputs, r = t.constDataInputs;
    return t.watchConfig.inputs.filter(
      (s, a) => !r[a] && !n[a]
    ).map((s) => this.varMapGetter.getVueRefObject(s));
  }
  _scheduleNextTick() {
    me(() => this._runAllTasks());
  }
  _runAllTasks() {
    const t = this.taskQueue.slice();
    this.taskQueue.length = 0, this._setTaskNodeRelations(t), t.forEach((n) => {
      n.run();
    });
  }
  _setTaskNodeRelations(t) {
    t.forEach((n) => {
      const r = this._findNextNodes(n, t);
      n.appendNextNodes(...r), r.forEach((o) => {
        o.appendPrevNodes(n);
      });
    });
  }
  _findNextNodes(t, n) {
    const r = t.watchTask.watchConfig.outputs;
    if (r && r.length <= 0)
      return [];
    const o = this._getCalculatorTasksByOutput(
      t.watchTask.watchConfig.outputs
    );
    return n.filter(
      (s) => o.has(s.watchTask.id) && s.watchTask.id !== t.watchTask.id
    );
  }
  _getCalculatorTasksByOutput(t) {
    const n = /* @__PURE__ */ new Set();
    return t == null || t.forEach((r) => {
      if (!Ot(r.ref))
        throw new Error("Non-var output bindings are not supported.");
      const { sid: o, id: s } = r.ref, a = `${o}-${s}`;
      (this.input2TaskIdMap.get(a) || []).forEach((l) => n.add(l));
    }), n;
  }
}
class vo {
  constructor(t, n) {
    M(this, "modify", !0);
    M(this, "_running", !1);
    M(this, "id");
    M(this, "_runningPromise", null);
    M(this, "_runningPromiseResolve", null);
    M(this, "_inputInfos");
    this.watchConfig = t, this.varMapGetter = n, this.id = Symbol(t.debug), this._inputInfos = this.createInputInfos();
  }
  createInputInfos() {
    const { inputs: t = [] } = this.watchConfig, n = this.watchConfig.data || Array.from({ length: t.length }).fill(0), r = this.watchConfig.slient || Array.from({ length: t.length }).fill(0);
    return {
      const_data: n,
      slients: r
    };
  }
  get slientInputs() {
    return this._inputInfos.slients;
  }
  get constDataInputs() {
    return this._inputInfos.const_data;
  }
  getServerInputs() {
    const { const_data: t } = this._inputInfos;
    return this.watchConfig.inputs ? this.watchConfig.inputs.map((n, r) => t[r] === 0 ? this.varMapGetter.getValue(n) : n) : [];
  }
  get running() {
    return this._running;
  }
  get runningPromise() {
    return this._runningPromise;
  }
  /**
   * setRunning
   */
  setRunning() {
    this._running = !0, this._runningPromise = new Promise((t) => {
      this._runningPromiseResolve = t;
    });
  }
  /**
   * taskDone
   */
  taskDone() {
    this._running = !1, this._runningPromiseResolve && (this._runningPromiseResolve(), this._runningPromiseResolve = null);
  }
}
class yo {
  /**
   *
   */
  constructor(t) {
    M(this, "prevNodes", []);
    M(this, "nextNodes", []);
    M(this, "_runningPrev", !1);
    this.watchTask = t;
  }
  /**
   * appendPrevNodes
   */
  appendPrevNodes(...t) {
    this.prevNodes.push(...t);
  }
  /**
   *
   */
  appendNextNodes(...t) {
    this.nextNodes.push(...t);
  }
  /**
   * hasNextNodes
   */
  hasNextNodes() {
    return this.nextNodes.length > 0;
  }
  /**
   * run
   */
  async run() {
    if (this.prevNodes.length > 0 && !this._runningPrev)
      try {
        this._runningPrev = !0, await Promise.all(this.prevNodes.map((t) => t.run()));
      } finally {
        this._runningPrev = !1;
      }
    if (this.watchTask.running) {
      await this.watchTask.runningPromise;
      return;
    }
    if (this.watchTask.modify) {
      this.watchTask.modify = !1, this.watchTask.setRunning();
      try {
        await wo(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function wo(e) {
  const { varMapGetter: t } = e, { outputs: n, preSetup: r } = e.watchConfig, o = Rn({
    config: r,
    varGetter: t
  });
  try {
    o.run(), e.taskDone();
    const s = await Sn().watchSend(e);
    if (!s)
      return;
    He(s, n, t);
  } finally {
    o.tryReset();
  }
}
function Mt(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function ze(e, t) {
  return Pn(e, {
    valueFn: t
  });
}
function Pn(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s], a) => [
      r ? r(o, s) : o,
      n(s, o, a)
    ])
  );
}
function Eo(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...s] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + s[0];
      case "~+":
        return s[0] + e;
    }
  }
  const r = _o(t);
  return e[r];
}
function _o(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      throw new Error("No bindable function provided");
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function bo(e, t, n) {
  return t.reduce(
    (r, o) => Eo(r, o),
    e
  );
}
function So(e, t) {
  return t ? t.reduce((n, r) => n[r], e) : e;
}
const Ro = window.structuredClone || ((e) => JSON.parse(JSON.stringify(e)));
function On(e) {
  return typeof e == "function" ? e : Ro(un(e));
}
function Po(e, t) {
  const {
    on: n,
    code: r,
    immediate: o,
    deep: s,
    once: a,
    flush: u,
    bind: l = {},
    onData: d,
    bindData: c
  } = e, i = d || Array.from({ length: n.length }).fill(0), f = c || Array.from({ length: Object.keys(l).length }).fill(0), h = ze(
    l,
    (v, w, _) => f[_] === 0 ? t.getVueRefObject(v) : v
  ), g = z(r, h), m = n.length === 1 ? Wt(i[0] === 1, n[0], t) : n.map(
    (v, w) => Wt(i[w] === 1, v, t)
  );
  return q(m, g, { immediate: o, deep: s, once: a, flush: u });
}
function Wt(e, t, n) {
  return e ? () => t : n.getVueRefObject(t);
}
function Oo(e, t) {
  const {
    inputs: n = [],
    outputs: r,
    slient: o,
    data: s,
    code: a,
    immediate: u = !0,
    deep: l,
    once: d,
    flush: c
  } = e, i = o || Array.from({ length: n.length }).fill(0), f = s || Array.from({ length: n.length }).fill(0), h = z(a), g = n.filter((v, w) => i[w] === 0 && f[w] === 0).map((v) => t.getVueRefObject(v));
  function m() {
    return n.map((v, w) => f[w] === 0 ? On(t.getValue(v)) : v);
  }
  q(
    g,
    () => {
      let v = h(...m());
      if (!r)
        return;
      const _ = r.length === 1 ? [v] : v, S = _.map((k) => k === void 0 ? 1 : 0);
      He(
        {
          values: _,
          types: S
        },
        r,
        t
      );
    },
    { immediate: u, deep: l, once: d, flush: c }
  );
}
const dt = Nt(() => Symbol());
function No(e, t) {
  const n = e.sid, r = dt.getOrDefault(n);
  dt.set(n, r), ge(r, t);
}
function ko(e) {
  const t = dt.get(e);
  return Y(t);
}
function Co() {
  return Nn().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function Nn() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const Vo = typeof Proxy == "function", Ao = "devtools-plugin:setup", Io = "plugin:settings:set";
let he, ht;
function $o() {
  var e;
  return he !== void 0 || (typeof window < "u" && window.performance ? (he = !0, ht = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (he = !0, ht = globalThis.perf_hooks.performance) : he = !1), he;
}
function xo() {
  return $o() ? ht.now() : Date.now();
}
class To {
  constructor(t, n) {
    this.target = null, this.targetQueue = [], this.onQueue = [], this.plugin = t, this.hook = n;
    const r = {};
    if (t.settings)
      for (const a in t.settings) {
        const u = t.settings[a];
        r[a] = u.defaultValue;
      }
    const o = `__vue-devtools-plugin-settings__${t.id}`;
    let s = Object.assign({}, r);
    try {
      const a = localStorage.getItem(o), u = JSON.parse(a);
      Object.assign(s, u);
    } catch {
    }
    this.fallbacks = {
      getSettings() {
        return s;
      },
      setSettings(a) {
        try {
          localStorage.setItem(o, JSON.stringify(a));
        } catch {
        }
        s = a;
      },
      now() {
        return xo();
      }
    }, n && n.on(Io, (a, u) => {
      a === this.plugin.id && this.fallbacks.setSettings(u);
    }), this.proxiedOn = new Proxy({}, {
      get: (a, u) => this.target ? this.target.on[u] : (...l) => {
        this.onQueue.push({
          method: u,
          args: l
        });
      }
    }), this.proxiedTarget = new Proxy({}, {
      get: (a, u) => this.target ? this.target[u] : u === "on" ? this.proxiedOn : Object.keys(this.fallbacks).includes(u) ? (...l) => (this.targetQueue.push({
        method: u,
        args: l,
        resolve: () => {
        }
      }), this.fallbacks[u](...l)) : (...l) => new Promise((d) => {
        this.targetQueue.push({
          method: u,
          args: l,
          resolve: d
        });
      })
    });
  }
  async setRealTarget(t) {
    this.target = t;
    for (const n of this.onQueue)
      this.target.on[n.method](...n.args);
    for (const n of this.targetQueue)
      n.resolve(await this.target[n.method](...n.args));
  }
}
function Do(e, t) {
  const n = e, r = Nn(), o = Co(), s = Vo && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(Ao, e, t);
  else {
    const a = s ? new To(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: a
    }), a && t(a.proxiedTarget);
  }
}
var R = {};
const Z = typeof document < "u";
function kn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function jo(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && kn(e.default);
}
const C = Object.assign;
function et(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = G(o) ? o.map(e) : e(o);
  }
  return n;
}
const Oe = () => {
}, G = Array.isArray;
function P(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const Cn = /#/g, Mo = /&/g, Wo = /\//g, Fo = /=/g, Lo = /\?/g, Vn = /\+/g, Bo = /%5B/g, Uo = /%5D/g, An = /%5E/g, Ho = /%60/g, In = /%7B/g, zo = /%7C/g, $n = /%7D/g, Go = /%20/g;
function kt(e) {
  return encodeURI("" + e).replace(zo, "|").replace(Bo, "[").replace(Uo, "]");
}
function Ko(e) {
  return kt(e).replace(In, "{").replace($n, "}").replace(An, "^");
}
function pt(e) {
  return kt(e).replace(Vn, "%2B").replace(Go, "+").replace(Cn, "%23").replace(Mo, "%26").replace(Ho, "`").replace(In, "{").replace($n, "}").replace(An, "^");
}
function qo(e) {
  return pt(e).replace(Fo, "%3D");
}
function Jo(e) {
  return kt(e).replace(Cn, "%23").replace(Lo, "%3F");
}
function Qo(e) {
  return e == null ? "" : Jo(e).replace(Wo, "%2F");
}
function ve(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    R.NODE_ENV !== "production" && P(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const Yo = /\/$/, Xo = (e) => e.replace(Yo, "");
function tt(e, t, n = "/") {
  let r, o = {}, s = "", a = "";
  const u = t.indexOf("#");
  let l = t.indexOf("?");
  return u < l && u >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, u > -1 ? u : t.length), o = e(s)), u > -1 && (r = r || t.slice(0, u), a = t.slice(u, t.length)), r = ts(r ?? t, n), {
    fullPath: r + (s && "?") + s + a,
    path: r,
    query: o,
    hash: ve(a)
  };
}
function Zo(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function Ft(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function Lt(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && oe(t.matched[r], n.matched[o]) && xn(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function oe(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function xn(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!es(e[n], t[n]))
      return !1;
  return !0;
}
function es(e, t) {
  return G(e) ? Bt(e, t) : G(t) ? Bt(t, e) : e === t;
}
function Bt(e, t) {
  return G(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function ts(e, t) {
  if (e.startsWith("/"))
    return e;
  if (R.NODE_ENV !== "production" && !t.startsWith("/"))
    return P(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
  if (!e)
    return t;
  const n = t.split("/"), r = e.split("/"), o = r[r.length - 1];
  (o === ".." || o === ".") && r.push("");
  let s = n.length - 1, a, u;
  for (a = 0; a < r.length; a++)
    if (u = r[a], u !== ".")
      if (u === "..")
        s > 1 && s--;
      else
        break;
  return n.slice(0, s).join("/") + "/" + r.slice(a).join("/");
}
const te = {
  path: "/",
  // TODO: could we use a symbol in the future?
  name: void 0,
  params: {},
  query: {},
  hash: "",
  fullPath: "/",
  matched: [],
  meta: {},
  redirectedFrom: void 0
};
var ye;
(function(e) {
  e.pop = "pop", e.push = "push";
})(ye || (ye = {}));
var ce;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(ce || (ce = {}));
const nt = "";
function Tn(e) {
  if (!e)
    if (Z) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), Xo(e);
}
const ns = /^[^#]+#/;
function Dn(e, t) {
  return e.replace(ns, "#") + t;
}
function rs(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const Ge = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function os(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (R.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          P(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        P(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      R.NODE_ENV !== "production" && P(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = rs(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function Ut(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const gt = /* @__PURE__ */ new Map();
function ss(e, t) {
  gt.set(e, t);
}
function is(e) {
  const t = gt.get(e);
  return gt.delete(e), t;
}
let as = () => location.protocol + "//" + location.host;
function jn(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let u = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(u);
    return l[0] !== "/" && (l = "/" + l), Ft(l, "");
  }
  return Ft(n, e) + r + o;
}
function cs(e, t, n, r) {
  let o = [], s = [], a = null;
  const u = ({ state: f }) => {
    const h = jn(e, location), g = n.value, m = t.value;
    let v = 0;
    if (f) {
      if (n.value = h, t.value = f, a && a === g) {
        a = null;
        return;
      }
      v = m ? f.position - m.position : 0;
    } else
      r(h);
    o.forEach((w) => {
      w(n.value, g, {
        delta: v,
        type: ye.pop,
        direction: v ? v > 0 ? ce.forward : ce.back : ce.unknown
      });
    });
  };
  function l() {
    a = n.value;
  }
  function d(f) {
    o.push(f);
    const h = () => {
      const g = o.indexOf(f);
      g > -1 && o.splice(g, 1);
    };
    return s.push(h), h;
  }
  function c() {
    const { history: f } = window;
    f.state && f.replaceState(C({}, f.state, { scroll: Ge() }), "");
  }
  function i() {
    for (const f of s)
      f();
    s = [], window.removeEventListener("popstate", u), window.removeEventListener("beforeunload", c);
  }
  return window.addEventListener("popstate", u), window.addEventListener("beforeunload", c, {
    passive: !0
  }), {
    pauseListeners: l,
    listen: d,
    destroy: i
  };
}
function Ht(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? Ge() : null
  };
}
function us(e) {
  const { history: t, location: n } = window, r = {
    value: jn(e, n)
  }, o = { value: t.state };
  o.value || s(r.value, {
    back: null,
    current: r.value,
    forward: null,
    // the length is off by one, we need to decrease it
    position: t.length - 1,
    replaced: !0,
    // don't add a scroll as the user may have an anchor, and we want
    // scrollBehavior to be triggered without a saved position
    scroll: null
  }, !0);
  function s(l, d, c) {
    const i = e.indexOf("#"), f = i > -1 ? (n.host && document.querySelector("base") ? e : e.slice(i)) + l : as() + e + l;
    try {
      t[c ? "replaceState" : "pushState"](d, "", f), o.value = d;
    } catch (h) {
      R.NODE_ENV !== "production" ? P("Error with push/replace State", h) : console.error(h), n[c ? "replace" : "assign"](f);
    }
  }
  function a(l, d) {
    const c = C({}, t.state, Ht(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), d, { position: o.value.position });
    s(l, c, !0), r.value = l;
  }
  function u(l, d) {
    const c = C(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: Ge()
      }
    );
    R.NODE_ENV !== "production" && !t.state && P(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(c.current, c, !0);
    const i = C({}, Ht(r.value, l, null), { position: c.position + 1 }, d);
    s(l, i, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: u,
    replace: a
  };
}
function Mn(e) {
  e = Tn(e);
  const t = us(e), n = cs(e, t.state, t.location, t.replace);
  function r(s, a = !0) {
    a || n.pauseListeners(), history.go(s);
  }
  const o = C({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: Dn.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function ls(e = "") {
  let t = [], n = [nt], r = 0;
  e = Tn(e);
  function o(u) {
    r++, r !== n.length && n.splice(r), n.push(u);
  }
  function s(u, l, { direction: d, delta: c }) {
    const i = {
      direction: d,
      delta: c,
      type: ye.pop
    };
    for (const f of t)
      f(u, l, i);
  }
  const a = {
    // rewritten by Object.defineProperty
    location: nt,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: Dn.bind(null, e),
    replace(u) {
      n.splice(r--, 1), o(u);
    },
    push(u, l) {
      o(u);
    },
    listen(u) {
      return t.push(u), () => {
        const l = t.indexOf(u);
        l > -1 && t.splice(l, 1);
      };
    },
    destroy() {
      t = [], n = [nt], r = 0;
    },
    go(u, l = !0) {
      const d = this.location, c = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        u < 0 ? ce.back : ce.forward
      );
      r = Math.max(0, Math.min(r + u, n.length - 1)), l && s(this.location, d, {
        direction: c,
        delta: u
      });
    }
  };
  return Object.defineProperty(a, "location", {
    enumerable: !0,
    get: () => n[r]
  }), a;
}
function fs(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), R.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && P(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), Mn(e);
}
function Le(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function Wn(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const mt = Symbol(R.NODE_ENV !== "production" ? "navigation failure" : "");
var zt;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(zt || (zt = {}));
const ds = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${ps(t)}" via a navigation guard.`;
  },
  4({ from: e, to: t }) {
    return `Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`;
  },
  8({ from: e, to: t }) {
    return `Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`;
  },
  16({ from: e, to: t }) {
    return `Avoided redundant navigation to current location: "${e.fullPath}".`;
  }
};
function we(e, t) {
  return R.NODE_ENV !== "production" ? C(new Error(ds[e](t)), {
    type: e,
    [mt]: !0
  }, t) : C(new Error(), {
    type: e,
    [mt]: !0
  }, t);
}
function X(e, t) {
  return e instanceof Error && mt in e && (t == null || !!(e.type & t));
}
const hs = ["params", "query", "hash"];
function ps(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of hs)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const Gt = "[^/]+?", gs = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, ms = /[.+*?^${}()[\]/\\]/g;
function vs(e, t) {
  const n = C({}, gs, t), r = [];
  let o = n.start ? "^" : "";
  const s = [];
  for (const d of e) {
    const c = d.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !d.length && (o += "/");
    for (let i = 0; i < d.length; i++) {
      const f = d[i];
      let h = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        i || (o += "/"), o += f.value.replace(ms, "\\$&"), h += 40;
      else if (f.type === 1) {
        const { value: g, repeatable: m, optional: v, regexp: w } = f;
        s.push({
          name: g,
          repeatable: m,
          optional: v
        });
        const _ = w || Gt;
        if (_ !== Gt) {
          h += 10;
          try {
            new RegExp(`(${_})`);
          } catch (k) {
            throw new Error(`Invalid custom RegExp for param "${g}" (${_}): ` + k.message);
          }
        }
        let S = m ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        i || (S = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        v && d.length < 2 ? `(?:/${S})` : "/" + S), v && (S += "?"), o += S, h += 20, v && (h += -8), m && (h += -20), _ === ".*" && (h += -50);
      }
      c.push(h);
    }
    r.push(c);
  }
  if (n.strict && n.end) {
    const d = r.length - 1;
    r[d][r[d].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const a = new RegExp(o, n.sensitive ? "" : "i");
  function u(d) {
    const c = d.match(a), i = {};
    if (!c)
      return null;
    for (let f = 1; f < c.length; f++) {
      const h = c[f] || "", g = s[f - 1];
      i[g.name] = h && g.repeatable ? h.split("/") : h;
    }
    return i;
  }
  function l(d) {
    let c = "", i = !1;
    for (const f of e) {
      (!i || !c.endsWith("/")) && (c += "/"), i = !1;
      for (const h of f)
        if (h.type === 0)
          c += h.value;
        else if (h.type === 1) {
          const { value: g, repeatable: m, optional: v } = h, w = g in d ? d[g] : "";
          if (G(w) && !m)
            throw new Error(`Provided param "${g}" is an array but it is not repeatable (* or + modifiers)`);
          const _ = G(w) ? w.join("/") : w;
          if (!_)
            if (v)
              f.length < 2 && (c.endsWith("/") ? c = c.slice(0, -1) : i = !0);
            else
              throw new Error(`Missing required param "${g}"`);
          c += _;
        }
    }
    return c || "/";
  }
  return {
    re: a,
    score: r,
    keys: s,
    parse: u,
    stringify: l
  };
}
function ys(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function Fn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = ys(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (Kt(r))
      return 1;
    if (Kt(o))
      return -1;
  }
  return o.length - r.length;
}
function Kt(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const ws = {
  type: 0,
  value: ""
}, Es = /[a-zA-Z0-9_]/;
function _s(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[ws]];
  if (!e.startsWith("/"))
    throw new Error(R.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(h) {
    throw new Error(`ERR (${n})/"${d}": ${h}`);
  }
  let n = 0, r = n;
  const o = [];
  let s;
  function a() {
    s && o.push(s), s = [];
  }
  let u = 0, l, d = "", c = "";
  function i() {
    d && (n === 0 ? s.push({
      type: 0,
      value: d
    }) : n === 1 || n === 2 || n === 3 ? (s.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${d}) must be alone in its segment. eg: '/:ids+.`), s.push({
      type: 1,
      value: d,
      regexp: c,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), d = "");
  }
  function f() {
    d += l;
  }
  for (; u < e.length; ) {
    if (l = e[u++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (d && i(), a()) : l === ":" ? (i(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : Es.test(l) ? f() : (i(), n = 0, l !== "*" && l !== "?" && l !== "+" && u--);
        break;
      case 2:
        l === ")" ? c[c.length - 1] == "\\" ? c = c.slice(0, -1) + l : n = 3 : c += l;
        break;
      case 3:
        i(), n = 0, l !== "*" && l !== "?" && l !== "+" && u--, c = "";
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${d}"`), i(), a(), o;
}
function bs(e, t, n) {
  const r = vs(_s(e.path), n);
  if (R.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const a of r.keys)
      s.has(a.name) && P(`Found duplicated params with name "${a.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(a.name);
  }
  const o = C(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function Ss(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = Yt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(i) {
    return r.get(i);
  }
  function s(i, f, h) {
    const g = !h, m = Jt(i);
    R.NODE_ENV !== "production" && Ns(m, f), m.aliasOf = h && h.record;
    const v = Yt(t, i), w = [m];
    if ("alias" in i) {
      const k = typeof i.alias == "string" ? [i.alias] : i.alias;
      for (const I of k)
        w.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          Jt(C({}, m, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: h ? h.record.components : m.components,
            path: I,
            // we might be the child of an alias
            aliasOf: h ? h.record : m
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, S;
    for (const k of w) {
      const { path: I } = k;
      if (f && I[0] !== "/") {
        const j = f.record.path, U = j[j.length - 1] === "/" ? "" : "/";
        k.path = f.record.path + (I && U + I);
      }
      if (R.NODE_ENV !== "production" && k.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = bs(k, f, v), R.NODE_ENV !== "production" && f && I[0] === "/" && Cs(_, f), h ? (h.alias.push(_), R.NODE_ENV !== "production" && Os(h, _)) : (S = S || _, S !== _ && S.alias.push(_), g && i.name && !Qt(_) && (R.NODE_ENV !== "production" && ks(i, f), a(i.name))), Ln(_) && l(_), m.children) {
        const j = m.children;
        for (let U = 0; U < j.length; U++)
          s(j[U], _, h && h.children[U]);
      }
      h = h || _;
    }
    return S ? () => {
      a(S);
    } : Oe;
  }
  function a(i) {
    if (Wn(i)) {
      const f = r.get(i);
      f && (r.delete(i), n.splice(n.indexOf(f), 1), f.children.forEach(a), f.alias.forEach(a));
    } else {
      const f = n.indexOf(i);
      f > -1 && (n.splice(f, 1), i.record.name && r.delete(i.record.name), i.children.forEach(a), i.alias.forEach(a));
    }
  }
  function u() {
    return n;
  }
  function l(i) {
    const f = Vs(i, n);
    n.splice(f, 0, i), i.record.name && !Qt(i) && r.set(i.record.name, i);
  }
  function d(i, f) {
    let h, g = {}, m, v;
    if ("name" in i && i.name) {
      if (h = r.get(i.name), !h)
        throw we(1, {
          location: i
        });
      if (R.NODE_ENV !== "production") {
        const S = Object.keys(i.params || {}).filter((k) => !h.keys.find((I) => I.name === k));
        S.length && P(`Discarded invalid param(s) "${S.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      v = h.record.name, g = C(
        // paramsFromLocation is a new object
        qt(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          h.keys.filter((S) => !S.optional).concat(h.parent ? h.parent.keys.filter((S) => S.optional) : []).map((S) => S.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        i.params && qt(i.params, h.keys.map((S) => S.name))
      ), m = h.stringify(g);
    } else if (i.path != null)
      m = i.path, R.NODE_ENV !== "production" && !m.startsWith("/") && P(`The Matcher cannot resolve relative paths but received "${m}". Unless you directly called \`matcher.resolve("${m}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), h = n.find((S) => S.re.test(m)), h && (g = h.parse(m), v = h.record.name);
    else {
      if (h = f.name ? r.get(f.name) : n.find((S) => S.re.test(f.path)), !h)
        throw we(1, {
          location: i,
          currentLocation: f
        });
      v = h.record.name, g = C({}, f.params, i.params), m = h.stringify(g);
    }
    const w = [];
    let _ = h;
    for (; _; )
      w.unshift(_.record), _ = _.parent;
    return {
      name: v,
      path: m,
      params: g,
      matched: w,
      meta: Ps(w)
    };
  }
  e.forEach((i) => s(i));
  function c() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: s,
    resolve: d,
    removeRoute: a,
    clearRoutes: c,
    getRoutes: u,
    getRecordMatcher: o
  };
}
function qt(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function Jt(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: Rs(e),
    children: e.children || [],
    instances: {},
    leaveGuards: /* @__PURE__ */ new Set(),
    updateGuards: /* @__PURE__ */ new Set(),
    enterCallbacks: {},
    // must be declared afterwards
    // mods: {},
    components: "components" in e ? e.components || null : e.component && { default: e.component }
  };
  return Object.defineProperty(t, "mods", {
    value: {}
  }), t;
}
function Rs(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function Qt(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function Ps(e) {
  return e.reduce((t, n) => C(t, n.meta), {});
}
function Yt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function vt(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Os(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(vt.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(vt.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function Ns(e, t) {
  t && t.record.name && !e.name && !e.path && P(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function ks(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function Cs(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(vt.bind(null, n)))
      return P(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function Vs(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    Fn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = As(e);
  return o && (r = t.lastIndexOf(o, r - 1), R.NODE_ENV !== "production" && r < 0 && P(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function As(e) {
  let t = e;
  for (; t = t.parent; )
    if (Ln(t) && Fn(e, t) === 0)
      return t;
}
function Ln({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Is(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(Vn, " "), a = s.indexOf("="), u = ve(a < 0 ? s : s.slice(0, a)), l = a < 0 ? null : ve(s.slice(a + 1));
    if (u in t) {
      let d = t[u];
      G(d) || (d = t[u] = [d]), d.push(l);
    } else
      t[u] = l;
  }
  return t;
}
function Xt(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = qo(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (G(r) ? r.map((s) => s && pt(s)) : [r && pt(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function $s(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = G(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const xs = Symbol(R.NODE_ENV !== "production" ? "router view location matched" : ""), Zt = Symbol(R.NODE_ENV !== "production" ? "router view depth" : ""), Ke = Symbol(R.NODE_ENV !== "production" ? "router" : ""), Ct = Symbol(R.NODE_ENV !== "production" ? "route location" : ""), yt = Symbol(R.NODE_ENV !== "production" ? "router view location" : "");
function Re() {
  let e = [];
  function t(r) {
    return e.push(r), () => {
      const o = e.indexOf(r);
      o > -1 && e.splice(o, 1);
    };
  }
  function n() {
    e = [];
  }
  return {
    add: t,
    list: () => e.slice(),
    reset: n
  };
}
function ne(e, t, n, r, o, s = (a) => a()) {
  const a = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((u, l) => {
    const d = (f) => {
      f === !1 ? l(we(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Le(f) ? l(we(2, {
        from: t,
        to: f
      })) : (a && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === a && typeof f == "function" && a.push(f), u());
    }, c = s(() => e.call(r && r.instances[o], t, n, R.NODE_ENV !== "production" ? Ts(d, t, n) : d));
    let i = Promise.resolve(c);
    if (e.length < 3 && (i = i.then(d)), R.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof c == "object" && "then" in c)
        i = i.then((h) => d._called ? h : (P(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (c !== void 0 && !d._called) {
        P(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    i.catch((f) => l(f));
  });
}
function Ts(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && P(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function rt(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const a of e) {
    R.NODE_ENV !== "production" && !a.components && !a.children.length && P(`Record with path "${a.path}" is either missing a "component(s)" or "children" property.`);
    for (const u in a.components) {
      let l = a.components[u];
      if (R.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw P(`Component "${u}" in record with path "${a.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          P(`Component "${u}" in record with path "${a.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const d = l;
          l = () => d;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, P(`Component "${u}" in record with path "${a.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !a.instances[u]))
        if (kn(l)) {
          const c = (l.__vccOpts || l)[t];
          c && s.push(ne(c, n, r, a, u, o));
        } else {
          let d = l();
          R.NODE_ENV !== "production" && !("catch" in d) && (P(`Component "${u}" in record with path "${a.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), d = Promise.resolve(d)), s.push(() => d.then((c) => {
            if (!c)
              throw new Error(`Couldn't resolve component "${u}" at "${a.path}"`);
            const i = jo(c) ? c.default : c;
            a.mods[u] = c, a.components[u] = i;
            const h = (i.__vccOpts || i)[t];
            return h && ne(h, n, r, a, u, o)();
          }));
        }
    }
  }
  return s;
}
function en(e) {
  const t = Y(Ke), n = Y(Ct);
  let r = !1, o = null;
  const s = B(() => {
    const c = L(e.to);
    return R.NODE_ENV !== "production" && (!r || c !== o) && (Le(c) || (r ? P(`Invalid value for prop "to" in useLink()
- to:`, c, `
- previous to:`, o, `
- props:`, e) : P(`Invalid value for prop "to" in useLink()
- to:`, c, `
- props:`, e)), o = c, r = !0), t.resolve(c);
  }), a = B(() => {
    const { matched: c } = s.value, { length: i } = c, f = c[i - 1], h = n.matched;
    if (!f || !h.length)
      return -1;
    const g = h.findIndex(oe.bind(null, f));
    if (g > -1)
      return g;
    const m = tn(c[i - 2]);
    return (
      // we are dealing with nested routes
      i > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      tn(f) === m && // avoid comparing the child with its parent
      h[h.length - 1].path !== m ? h.findIndex(oe.bind(null, c[i - 2])) : g
    );
  }), u = B(() => a.value > -1 && Fs(n.params, s.value.params)), l = B(() => a.value > -1 && a.value === n.matched.length - 1 && xn(n.params, s.value.params));
  function d(c = {}) {
    if (Ws(c)) {
      const i = t[L(e.replace) ? "replace" : "push"](
        L(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(Oe);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => i), i;
    }
    return Promise.resolve();
  }
  if (R.NODE_ENV !== "production" && Z) {
    const c = bt();
    if (c) {
      const i = {
        route: s.value,
        isActive: u.value,
        isExactActive: l.value,
        error: null
      };
      c.__vrl_devtools = c.__vrl_devtools || [], c.__vrl_devtools.push(i), cn(() => {
        i.route = s.value, i.isActive = u.value, i.isExactActive = l.value, i.error = Le(L(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: B(() => s.value.href),
    isActive: u,
    isExactActive: l,
    navigate: d
  };
}
function Ds(e) {
  return e.length === 1 ? e[0] : e;
}
const js = /* @__PURE__ */ W({
  name: "RouterLink",
  compatConfig: { MODE: 3 },
  props: {
    to: {
      type: [String, Object],
      required: !0
    },
    replace: Boolean,
    activeClass: String,
    // inactiveClass: String,
    exactActiveClass: String,
    custom: Boolean,
    ariaCurrentValue: {
      type: String,
      default: "page"
    }
  },
  useLink: en,
  setup(e, { slots: t }) {
    const n = fr(en(e)), { options: r } = Y(Ke), o = B(() => ({
      [nn(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [nn(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && Ds(t.default(n));
      return e.custom ? s : D("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, s);
    };
  }
}), Ms = js;
function Ws(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function Fs(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!G(o) || o.length !== r.length || r.some((s, a) => s !== o[a]))
      return !1;
  }
  return !0;
}
function tn(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const nn = (e, t, n) => e ?? t ?? n, Ls = /* @__PURE__ */ W({
  name: "RouterView",
  // #674 we manually inherit them
  inheritAttrs: !1,
  props: {
    name: {
      type: String,
      default: "default"
    },
    route: Object
  },
  // Better compat for @vue/compat users
  // https://github.com/vuejs/router/issues/1315
  compatConfig: { MODE: 3 },
  setup(e, { attrs: t, slots: n }) {
    R.NODE_ENV !== "production" && Us();
    const r = Y(yt), o = B(() => e.route || r.value), s = Y(Zt, 0), a = B(() => {
      let d = L(s);
      const { matched: c } = o.value;
      let i;
      for (; (i = c[d]) && !i.components; )
        d++;
      return d;
    }), u = B(() => o.value.matched[a.value]);
    ge(Zt, B(() => a.value + 1)), ge(xs, u), ge(yt, o);
    const l = J();
    return q(() => [l.value, u.value, e.name], ([d, c, i], [f, h, g]) => {
      c && (c.instances[i] = d, h && h !== c && d && d === f && (c.leaveGuards.size || (c.leaveGuards = h.leaveGuards), c.updateGuards.size || (c.updateGuards = h.updateGuards))), d && c && // if there is no instance but to and from are the same this might be
      // the first visit
      (!h || !oe(c, h) || !f) && (c.enterCallbacks[i] || []).forEach((m) => m(d));
    }, { flush: "post" }), () => {
      const d = o.value, c = e.name, i = u.value, f = i && i.components[c];
      if (!f)
        return rn(n.default, { Component: f, route: d });
      const h = i.props[c], g = h ? h === !0 ? d.params : typeof h == "function" ? h(d) : h : null, v = D(f, C({}, g, t, {
        onVnodeUnmounted: (w) => {
          w.component.isUnmounted && (i.instances[c] = null);
        },
        ref: l
      }));
      if (R.NODE_ENV !== "production" && Z && v.ref) {
        const w = {
          depth: a.value,
          name: i.name,
          path: i.path,
          meta: i.meta
        };
        (G(v.ref) ? v.ref.map((S) => S.i) : [v.ref.i]).forEach((S) => {
          S.__vrv_devtools = w;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        rn(n.default, { Component: v, route: d }) || v
      );
    };
  }
});
function rn(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const Bs = Ls;
function Us() {
  const e = bt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    P(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function Pe(e, t) {
  const n = C({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => ei(r, ["instances", "children", "aliasOf"]))
  });
  return {
    _custom: {
      type: null,
      readOnly: !0,
      display: e.fullPath,
      tooltip: t,
      value: n
    }
  };
}
function De(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let Hs = 0;
function zs(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = Hs++;
  Do({
    id: "org.vuejs.router" + (r ? "." + r : ""),
    label: "Vue Router",
    packageName: "vue-router",
    homepage: "https://router.vuejs.org",
    logo: "https://router.vuejs.org/logo.png",
    componentStateTypes: ["Routing"],
    app: e
  }, (o) => {
    typeof o.now != "function" && console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."), o.on.inspectComponent((c, i) => {
      c.instanceData && c.instanceData.state.push({
        type: "Routing",
        key: "$route",
        editable: !1,
        value: Pe(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: c, componentInstance: i }) => {
      if (i.__vrv_devtools) {
        const f = i.__vrv_devtools;
        c.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: Bn
        });
      }
      G(i.__vrl_devtools) && (i.__devtoolsApi = o, i.__vrl_devtools.forEach((f) => {
        let h = f.route.path, g = zn, m = "", v = 0;
        f.error ? (h = f.error, g = Qs, v = Ys) : f.isExactActive ? (g = Hn, m = "This is exactly active") : f.isActive && (g = Un, m = "This link is active"), c.tags.push({
          label: h,
          textColor: v,
          tooltip: m,
          backgroundColor: g
        });
      }));
    }), q(t.currentRoute, () => {
      l(), o.notifyComponentUpdate(), o.sendInspectorTree(u), o.sendInspectorState(u);
    });
    const s = "router:navigations:" + r;
    o.addTimelineLayer({
      id: s,
      label: `Router${r ? " " + r : ""} Navigations`,
      color: 4237508
    }), t.onError((c, i) => {
      o.addTimelineEvent({
        layerId: s,
        event: {
          title: "Error during Navigation",
          subtitle: i.fullPath,
          logType: "error",
          time: o.now(),
          data: { error: c },
          groupId: i.meta.__navigationId
        }
      });
    });
    let a = 0;
    t.beforeEach((c, i) => {
      const f = {
        guard: De("beforeEach"),
        from: Pe(i, "Current Location during this navigation"),
        to: Pe(c, "Target location")
      };
      Object.defineProperty(c.meta, "__navigationId", {
        value: a++
      }), o.addTimelineEvent({
        layerId: s,
        event: {
          time: o.now(),
          title: "Start of navigation",
          subtitle: c.fullPath,
          data: f,
          groupId: c.meta.__navigationId
        }
      });
    }), t.afterEach((c, i, f) => {
      const h = {
        guard: De("afterEach")
      };
      f ? (h.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, h.status = De("❌")) : h.status = De("✅"), h.from = Pe(i, "Current Location during this navigation"), h.to = Pe(c, "Target location"), o.addTimelineEvent({
        layerId: s,
        event: {
          title: "End of navigation",
          subtitle: c.fullPath,
          time: o.now(),
          data: h,
          logType: f ? "warning" : "default",
          groupId: c.meta.__navigationId
        }
      });
    });
    const u = "router-inspector:" + r;
    o.addInspector({
      id: u,
      label: "Routes" + (r ? " " + r : ""),
      icon: "book",
      treeFilterPlaceholder: "Search routes"
    });
    function l() {
      if (!d)
        return;
      const c = d;
      let i = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      i.forEach(qn), c.filter && (i = i.filter((f) => (
        // save matches state based on the payload
        wt(f, c.filter.toLowerCase())
      ))), i.forEach((f) => Kn(f, t.currentRoute.value)), c.rootNodes = i.map(Gn);
    }
    let d;
    o.on.getInspectorTree((c) => {
      d = c, c.app === e && c.inspectorId === u && l();
    }), o.on.getInspectorState((c) => {
      if (c.app === e && c.inspectorId === u) {
        const f = n.getRoutes().find((h) => h.record.__vd_id === c.nodeId);
        f && (c.state = {
          options: Ks(f)
        });
      }
    }), o.sendInspectorTree(u), o.sendInspectorState(u);
  });
}
function Gs(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function Ks(e) {
  const { record: t } = e, n = [
    { editable: !1, key: "path", value: t.path }
  ];
  return t.name != null && n.push({
    editable: !1,
    key: "name",
    value: t.name
  }), n.push({ editable: !1, key: "regexp", value: e.re }), e.keys.length && n.push({
    editable: !1,
    key: "keys",
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.keys.map((r) => `${r.name}${Gs(r)}`).join(" "),
        tooltip: "Param keys",
        value: e.keys
      }
    }
  }), t.redirect != null && n.push({
    editable: !1,
    key: "redirect",
    value: t.redirect
  }), e.alias.length && n.push({
    editable: !1,
    key: "aliases",
    value: e.alias.map((r) => r.record.path)
  }), Object.keys(e.record.meta).length && n.push({
    editable: !1,
    key: "meta",
    value: e.record.meta
  }), n.push({
    key: "score",
    editable: !1,
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.score.map((r) => r.join(", ")).join(" | "),
        tooltip: "Score used to sort routes",
        value: e.score
      }
    }
  }), n;
}
const Bn = 15485081, Un = 2450411, Hn = 8702998, qs = 2282478, zn = 16486972, Js = 6710886, Qs = 16704226, Ys = 12131356;
function Gn(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: qs
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: zn
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: Bn
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: Hn
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: Un
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: Js
  });
  let r = n.__vd_id;
  return r == null && (r = String(Xs++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map(Gn)
  };
}
let Xs = 0;
const Zs = /^\/(.*)\/([a-z]*)$/;
function Kn(e, t) {
  const n = t.matched.length && oe(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => oe(r, e.record))), e.children.forEach((r) => Kn(r, t));
}
function qn(e) {
  e.__vd_match = !1, e.children.forEach(qn);
}
function wt(e, t) {
  const n = String(e.re).match(Zs);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((a) => wt(a, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = ve(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((a) => wt(a, t));
}
function ei(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function ti(e) {
  const t = Ss(e.routes, e), n = e.parseQuery || Is, r = e.stringifyQuery || Xt, o = e.history;
  if (R.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = Re(), a = Re(), u = Re(), l = K(te);
  let d = te;
  Z && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const c = et.bind(null, (p) => "" + p), i = et.bind(null, Qo), f = (
    // @ts-expect-error: intentionally avoid the type check
    et.bind(null, ve)
  );
  function h(p, E) {
    let y, b;
    return Wn(p) ? (y = t.getRecordMatcher(p), R.NODE_ENV !== "production" && !y && P(`Parent route "${String(p)}" not found when adding child route`, E), b = E) : b = p, t.addRoute(b, y);
  }
  function g(p) {
    const E = t.getRecordMatcher(p);
    E ? t.removeRoute(E) : R.NODE_ENV !== "production" && P(`Cannot remove non-existent route "${String(p)}"`);
  }
  function m() {
    return t.getRoutes().map((p) => p.record);
  }
  function v(p) {
    return !!t.getRecordMatcher(p);
  }
  function w(p, E) {
    if (E = C({}, E || l.value), typeof p == "string") {
      const O = tt(n, p, E.path), $ = t.resolve({ path: O.path }, E), se = o.createHref(O.fullPath);
      return R.NODE_ENV !== "production" && (se.startsWith("//") ? P(`Location "${p}" resolved to "${se}". A resolved location cannot start with multiple slashes.`) : $.matched.length || P(`No match found for location with path "${p}"`)), C(O, $, {
        params: f($.params),
        hash: ve(O.hash),
        redirectedFrom: void 0,
        href: se
      });
    }
    if (R.NODE_ENV !== "production" && !Le(p))
      return P(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, p), w({});
    let y;
    if (p.path != null)
      R.NODE_ENV !== "production" && "params" in p && !("name" in p) && // @ts-expect-error: the type is never
      Object.keys(p.params).length && P(`Path "${p.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), y = C({}, p, {
        path: tt(n, p.path, E.path).path
      });
    else {
      const O = C({}, p.params);
      for (const $ in O)
        O[$] == null && delete O[$];
      y = C({}, p, {
        params: i(O)
      }), E.params = i(E.params);
    }
    const b = t.resolve(y, E), A = p.hash || "";
    R.NODE_ENV !== "production" && A && !A.startsWith("#") && P(`A \`hash\` should always start with the character "#". Replace "${A}" with "#${A}".`), b.params = c(f(b.params));
    const x = Zo(r, C({}, p, {
      hash: Ko(A),
      path: b.path
    })), N = o.createHref(x);
    return R.NODE_ENV !== "production" && (N.startsWith("//") ? P(`Location "${p}" resolved to "${N}". A resolved location cannot start with multiple slashes.`) : b.matched.length || P(`No match found for location with path "${p.path != null ? p.path : p}"`)), C({
      fullPath: x,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: A,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === Xt ? $s(p.query) : p.query || {}
      )
    }, b, {
      redirectedFrom: void 0,
      href: N
    });
  }
  function _(p) {
    return typeof p == "string" ? tt(n, p, l.value.path) : C({}, p);
  }
  function S(p, E) {
    if (d !== p)
      return we(8, {
        from: E,
        to: p
      });
  }
  function k(p) {
    return U(p);
  }
  function I(p) {
    return k(C(_(p), { replace: !0 }));
  }
  function j(p) {
    const E = p.matched[p.matched.length - 1];
    if (E && E.redirect) {
      const { redirect: y } = E;
      let b = typeof y == "function" ? y(p) : y;
      if (typeof b == "string" && (b = b.includes("?") || b.includes("#") ? b = _(b) : (
        // force empty params
        { path: b }
      ), b.params = {}), R.NODE_ENV !== "production" && b.path == null && !("name" in b))
        throw P(`Invalid redirect found:
${JSON.stringify(b, null, 2)}
 when navigating to "${p.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return C({
        query: p.query,
        hash: p.hash,
        // avoid transferring params if the redirect has a path
        params: b.path != null ? {} : p.params
      }, b);
    }
  }
  function U(p, E) {
    const y = d = w(p), b = l.value, A = p.state, x = p.force, N = p.replace === !0, O = j(y);
    if (O)
      return U(
        C(_(O), {
          state: typeof O == "object" ? C({}, A, O.state) : A,
          force: x,
          replace: N
        }),
        // keep original redirectedFrom if it exists
        E || y
      );
    const $ = y;
    $.redirectedFrom = E;
    let se;
    return !x && Lt(r, b, y) && (se = we(16, { to: $, from: b }), At(
      b,
      b,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (se ? Promise.resolve(se) : V($, b)).catch((F) => X(F) ? (
      // navigation redirects still mark the router as ready
      X(
        F,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? F : Qe(F)
    ) : (
      // reject any unknown error
      Je(F, $, b)
    )).then((F) => {
      if (F) {
        if (X(
          F,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return R.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          Lt(r, w(F.to), $) && // and we have done it a couple of times
          E && // @ts-expect-error: added only in dev
          (E._count = E._count ? (
            // @ts-expect-error
            E._count + 1
          ) : 1) > 30 ? (P(`Detected a possibly infinite redirection in a navigation guard when going from "${b.fullPath}" to "${$.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : U(
            // keep options
            C({
              // preserve an existing replacement but allow the redirect to override it
              replace: N
            }, _(F.to), {
              state: typeof F.to == "object" ? C({}, A, F.to.state) : A,
              force: x
            }),
            // preserve the original redirectedFrom if any
            E || $
          );
      } else
        F = H($, b, !0, N, A);
      return T($, b, F), F;
    });
  }
  function le(p, E) {
    const y = S(p, E);
    return y ? Promise.reject(y) : Promise.resolve();
  }
  function be(p) {
    const E = $e.values().next().value;
    return E && typeof E.runWithContext == "function" ? E.runWithContext(p) : p();
  }
  function V(p, E) {
    let y;
    const [b, A, x] = ni(p, E);
    y = rt(b.reverse(), "beforeRouteLeave", p, E);
    for (const O of b)
      O.leaveGuards.forEach(($) => {
        y.push(ne($, p, E));
      });
    const N = le.bind(null, p, E);
    return y.push(N), fe(y).then(() => {
      y = [];
      for (const O of s.list())
        y.push(ne(O, p, E));
      return y.push(N), fe(y);
    }).then(() => {
      y = rt(A, "beforeRouteUpdate", p, E);
      for (const O of A)
        O.updateGuards.forEach(($) => {
          y.push(ne($, p, E));
        });
      return y.push(N), fe(y);
    }).then(() => {
      y = [];
      for (const O of x)
        if (O.beforeEnter)
          if (G(O.beforeEnter))
            for (const $ of O.beforeEnter)
              y.push(ne($, p, E));
          else
            y.push(ne(O.beforeEnter, p, E));
      return y.push(N), fe(y);
    }).then(() => (p.matched.forEach((O) => O.enterCallbacks = {}), y = rt(x, "beforeRouteEnter", p, E, be), y.push(N), fe(y))).then(() => {
      y = [];
      for (const O of a.list())
        y.push(ne(O, p, E));
      return y.push(N), fe(y);
    }).catch((O) => X(
      O,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? O : Promise.reject(O));
  }
  function T(p, E, y) {
    u.list().forEach((b) => be(() => b(p, E, y)));
  }
  function H(p, E, y, b, A) {
    const x = S(p, E);
    if (x)
      return x;
    const N = E === te, O = Z ? history.state : {};
    y && (b || N ? o.replace(p.fullPath, C({
      scroll: N && O && O.scroll
    }, A)) : o.push(p.fullPath, A)), l.value = p, At(p, E, y, N), Qe();
  }
  let Se;
  function nr() {
    Se || (Se = o.listen((p, E, y) => {
      if (!It.listening)
        return;
      const b = w(p), A = j(b);
      if (A) {
        U(C(A, { replace: !0, force: !0 }), b).catch(Oe);
        return;
      }
      d = b;
      const x = l.value;
      Z && ss(Ut(x.fullPath, y.delta), Ge()), V(b, x).catch((N) => X(
        N,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? N : X(
        N,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (U(
        C(_(N.to), {
          force: !0
        }),
        b
        // avoid an uncaught rejection, let push call triggerError
      ).then((O) => {
        X(
          O,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !y.delta && y.type === ye.pop && o.go(-1, !1);
      }).catch(Oe), Promise.reject()) : (y.delta && o.go(-y.delta, !1), Je(N, b, x))).then((N) => {
        N = N || H(
          // after navigation, all matched components are resolved
          b,
          x,
          !1
        ), N && (y.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !X(
          N,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-y.delta, !1) : y.type === ye.pop && X(
          N,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), T(b, x, N);
      }).catch(Oe);
    }));
  }
  let qe = Re(), Vt = Re(), Ie;
  function Je(p, E, y) {
    Qe(p);
    const b = Vt.list();
    return b.length ? b.forEach((A) => A(p, E, y)) : (R.NODE_ENV !== "production" && P("uncaught error during route navigation:"), console.error(p)), Promise.reject(p);
  }
  function rr() {
    return Ie && l.value !== te ? Promise.resolve() : new Promise((p, E) => {
      qe.add([p, E]);
    });
  }
  function Qe(p) {
    return Ie || (Ie = !p, nr(), qe.list().forEach(([E, y]) => p ? y(p) : E()), qe.reset()), p;
  }
  function At(p, E, y, b) {
    const { scrollBehavior: A } = e;
    if (!Z || !A)
      return Promise.resolve();
    const x = !y && is(Ut(p.fullPath, 0)) || (b || !y) && history.state && history.state.scroll || null;
    return me().then(() => A(p, E, x)).then((N) => N && os(N)).catch((N) => Je(N, p, E));
  }
  const Ye = (p) => o.go(p);
  let Xe;
  const $e = /* @__PURE__ */ new Set(), It = {
    currentRoute: l,
    listening: !0,
    addRoute: h,
    removeRoute: g,
    clearRoutes: t.clearRoutes,
    hasRoute: v,
    getRoutes: m,
    resolve: w,
    options: e,
    push: k,
    replace: I,
    go: Ye,
    back: () => Ye(-1),
    forward: () => Ye(1),
    beforeEach: s.add,
    beforeResolve: a.add,
    afterEach: u.add,
    onError: Vt.add,
    isReady: rr,
    install(p) {
      const E = this;
      p.component("RouterLink", Ms), p.component("RouterView", Bs), p.config.globalProperties.$router = E, Object.defineProperty(p.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => L(l)
      }), Z && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !Xe && l.value === te && (Xe = !0, k(o.location).catch((A) => {
        R.NODE_ENV !== "production" && P("Unexpected error when starting the router:", A);
      }));
      const y = {};
      for (const A in te)
        Object.defineProperty(y, A, {
          get: () => l.value[A],
          enumerable: !0
        });
      p.provide(Ke, E), p.provide(Ct, lr(y)), p.provide(yt, l);
      const b = p.unmount;
      $e.add(p), p.unmount = function() {
        $e.delete(p), $e.size < 1 && (d = te, Se && Se(), Se = null, l.value = te, Xe = !1, Ie = !1), b();
      }, R.NODE_ENV !== "production" && Z && zs(p, E, t);
    }
  };
  function fe(p) {
    return p.reduce((E, y) => E.then(() => be(y)), Promise.resolve());
  }
  return It;
}
function ni(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let a = 0; a < s; a++) {
    const u = t.matched[a];
    u && (e.matched.find((d) => oe(d, u)) ? r.push(u) : n.push(u));
    const l = e.matched[a];
    l && (t.matched.find((d) => oe(d, l)) || o.push(l));
  }
  return [n, r, o];
}
function ri() {
  return Y(Ke);
}
function oi(e) {
  return Y(Ct);
}
function si(e) {
  const { immediately: t = !1, code: n } = e;
  let r = z(n);
  return t && (r = r()), r;
}
const Ne = /* @__PURE__ */ new Map();
function ii(e) {
  if (!Ne.has(e)) {
    const t = Symbol();
    return Ne.set(e, t), t;
  }
  return Ne.get(e);
}
function _e(e, t) {
  var l, d;
  const n = Ze(e);
  if (!n)
    return {
      updateVforInfo: () => {
      },
      updateSlotPropValue: () => {
      }
    };
  const { varMap: r, vforRealIndexMap: o } = ci(n, t);
  if (r.size > 0) {
    const c = ii(e);
    ge(c, r);
  }
  dr(() => {
    r.clear(), o.clear();
  });
  const s = ue({ attached: { varMap: r, sid: e } });
  go({
    watchConfigs: n.py_watch || [],
    computedConfigs: n.web_computed || [],
    varMapGetter: s,
    sid: e
  }), (l = n.js_watch) == null || l.forEach((c) => {
    Oo(c, s);
  }), (d = n.vue_watch) == null || d.forEach((c) => {
    Po(c, s);
  });
  function a(c, i) {
    const f = Ze(c);
    if (!f.vfor)
      return;
    const { fi: h, fv: g } = f.vfor;
    h && (r.get(h.id).value = i.index), g && (o.get(g.id).value = i.index);
  }
  function u(c) {
    const { sid: i, value: f } = c;
    if (!i)
      return;
    const h = Ze(i), { id: g } = h.sp, m = r.get(g);
    m.value = f;
  }
  return {
    updateVforInfo: a,
    updateSlotPropValue: u
  };
}
function ue(e) {
  const { attached: t, sidCollector: n } = e || {}, [r, o, s] = ui(n);
  t && r.set(t.sid, t.varMap);
  const a = o ? oi() : null, u = s ? ri() : null, l = o ? () => a : () => {
    throw new Error("Route params not found");
  }, d = s ? () => u : () => {
    throw new Error("Router not found");
  };
  function c(m) {
    const v = ke(f(m));
    return En(v, m.path ?? [], c);
  }
  function i(m) {
    const v = f(m);
    return Xr(v, {
      paths: m.path,
      getBindableValueFn: c
    });
  }
  function f(m) {
    return ao(m) ? () => l()[m.prop] : r.get(m.sid).get(m.id);
  }
  function h(m, v) {
    if (Ot(m)) {
      const w = f(m);
      if (m.path) {
        _n(w.value, m.path, v, c);
        return;
      }
      w.value = v;
      return;
    }
    throw new Error(`Unsupported output binding: ${m}`);
  }
  function g() {
    return d();
  }
  return {
    getValue: c,
    getRouter: g,
    getVueRefObject: i,
    updateValue: h,
    getVueRefObjectWithoutPath: f
  };
}
function Jn(e) {
  const t = Ne.get(e);
  return Y(t);
}
function ai(e) {
  const t = Jn(e);
  if (t === void 0)
    throw new Error(`Scope not found: ${e}`);
  return t;
}
function ci(e, t) {
  var s, a, u, l, d, c;
  const n = /* @__PURE__ */ new Map(), r = /* @__PURE__ */ new Map(), o = ue({
    attached: { varMap: n, sid: e.id }
  });
  if (e.data && e.data.forEach((i) => {
    n.set(i.id, i.value);
  }), e.jsFn && e.jsFn.forEach((i) => {
    const f = si(i);
    n.set(i.id, () => f);
  }), e.vfor) {
    if (!t || !t.initVforInfo)
      throw new Error("Init vfor info not found");
    const { fv: i, fi: f, fk: h } = e.vfor, { index: g, keyValue: m, config: v } = t.initVforInfo;
    if (i) {
      const w = K(g);
      r.set(i.id, w);
      const { sid: _ } = v, S = ko(_), k = ae(() => ({
        get() {
          const I = S.value;
          return Array.isArray(I) ? I[w.value] : Object.values(I)[w.value];
        },
        set(I) {
          const j = S.value;
          if (!Array.isArray(j)) {
            j[m] = I;
            return;
          }
          j[w.value] = I;
        }
      }));
      n.set(i.id, k);
    }
    f && n.set(f.id, K(g)), h && n.set(h.id, K(m));
  }
  if (e.sp) {
    const { id: i } = e.sp, f = ((s = t == null ? void 0 : t.initSlotPropInfo) == null ? void 0 : s.value) || null;
    n.set(i, K(f));
  }
  return (a = e.eRefs) == null || a.forEach((i) => {
    n.set(i.id, K(null));
  }), (u = e.refs) == null || u.forEach((i) => {
    const f = Zr(i);
    n.set(i.id, f);
  }), (l = e.web_computed) == null || l.forEach((i) => {
    const f = no(i);
    n.set(i.id, f);
  }), (d = e.js_computed) == null || d.forEach((i) => {
    const f = ro(
      i,
      o
    );
    n.set(i.id, f);
  }), (c = e.vue_computed) == null || c.forEach((i) => {
    const f = to(
      i,
      o
    );
    n.set(i.id, f);
  }), { varMap: n, vforRealIndexMap: r };
}
function ui(e) {
  const t = /* @__PURE__ */ new Map();
  if (e) {
    const { sids: n, needRouteParams: r = !0, needRouter: o = !0 } = e;
    for (const s of n)
      t.set(s, ai(s));
    return [t, r, o];
  }
  for (const n of Ne.keys()) {
    const r = Jn(n);
    r !== void 0 && t.set(n, r);
  }
  return [t, !0, !0];
}
const li = W(fi, {
  props: ["vforConfig", "vforIndex", "vforKeyValue"]
});
function fi(e) {
  const { sid: t, items: n = [] } = e.vforConfig, { updateVforInfo: r } = _e(t, {
    initVforInfo: {
      config: e.vforConfig,
      index: e.vforIndex,
      keyValue: e.vforKeyValue
    }
  });
  return () => (r(t, {
    index: e.vforIndex,
    keyValue: e.vforKeyValue
  }), n.length === 1 ? Ee(n[0]) : n.map((o) => Ee(o)));
}
function on(e) {
  const { start: t = 0, end: n, step: r = 1 } = e;
  let o = [];
  if (r > 0)
    for (let s = t; s < n; s += r)
      o.push(s);
  else
    for (let s = t; s > n; s += r)
      o.push(s);
  return o;
}
const Qn = W(di, {
  props: ["config"]
});
function di(e) {
  const { fkey: t, tsGroup: n = {} } = e.config, r = ue(), s = gi(t ?? "index"), a = mi(e.config, r);
  return No(e.config, a), () => {
    const u = hr(a.value, (...l) => {
      const d = l[0], c = l[2] !== void 0, i = c ? l[2] : l[1], f = c ? l[1] : i, h = s(d, i);
      return D(li, {
        key: h,
        vforIndex: i,
        vforKeyValue: f,
        vforConfig: e.config
      });
    });
    return n && Object.keys(n).length > 0 ? D(ln, n, {
      default: () => u
    }) : u;
  };
}
const hi = (e) => e, pi = (e, t) => t;
function gi(e) {
  const t = qr(e);
  return typeof t == "function" ? t : e === "item" ? hi : pi;
}
function mi(e, t) {
  const { type: n, value: r } = e.array, o = n === ft.range;
  if (n === ft.const || o && typeof r == "number") {
    const a = o ? on({
      end: Math.max(0, r)
    }) : r;
    return ae(() => ({
      get() {
        return a;
      },
      set() {
        throw new Error("Cannot set value to constant array");
      }
    }));
  }
  if (o) {
    const a = r, u = t.getVueRefObject(a);
    return ae(() => ({
      get() {
        return on({
          end: Math.max(0, u.value)
        });
      },
      set() {
        throw new Error("Cannot set value to range array");
      }
    }));
  }
  return ae(() => {
    const a = t.getVueRefObject(
      r
    );
    return {
      get() {
        return a.value;
      },
      set(u) {
        a.value = u;
      }
    };
  });
}
const Yn = W(vi, {
  props: ["config"]
});
function vi(e) {
  const { sid: t, items: n, on: r } = e.config;
  Ae(t) && _e(t);
  const o = ue();
  return () => (typeof r == "boolean" ? r : o.getValue(r)) ? n.map((a) => Ee(a)) : void 0;
}
const sn = W(yi, {
  props: ["slotConfig"]
});
function yi(e) {
  const { sid: t, items: n } = e.slotConfig;
  return Ae(t) && _e(t), () => n.map((r) => Ee(r));
}
const ot = ":default", Xn = W(wi, {
  props: ["config"]
});
function wi(e) {
  const { on: t, caseValues: n, slots: r, sid: o } = e.config;
  Ae(o) && _e(o);
  const s = ue();
  return () => {
    const a = s.getValue(t), u = n.map((l, d) => {
      const c = d.toString(), i = r[c];
      return l === a ? D(sn, { slotConfig: i, key: c }) : null;
    }).filter(Boolean);
    return u.length === 0 && ot in r ? D(sn, {
      slotConfig: r[ot],
      key: ot
    }) : u;
  };
}
const Ei = "on:mounted";
function _i(e, t, n) {
  if (!t)
    return e;
  const r = Nt(() => []);
  t.map(([u, l]) => {
    const d = bi(l, n), { eventName: c, handleEvent: i } = Ni({
      eventName: u,
      info: l,
      handleEvent: d
    });
    r.getOrDefault(c).push(i);
  });
  const o = {};
  for (const [u, l] of r) {
    const d = l.length === 1 ? l[0] : (...c) => l.forEach((i) => Promise.resolve().then(() => i(...c)));
    o[u] = d;
  }
  const { [Ei]: s, ...a } = o;
  return e = je(e, a), s && (e = fn(e, [
    [
      {
        mounted(u) {
          s(u);
        }
      }
    ]
  ])), e;
}
function bi(e, t) {
  if (e.type === "web") {
    const n = Si(e, t);
    return Ri(e, n, t);
  } else {
    if (e.type === "vue")
      return Oi(e, t);
    if (e.type === "js")
      return Pi(e, t);
  }
  throw new Error(`unknown event type ${e}`);
}
function Si(e, t) {
  const { inputs: n = [] } = e;
  return (...r) => n.map(({ value: o, type: s }) => {
    if (s === Q.EventContext) {
      const { path: a } = o;
      if (a.startsWith(":")) {
        const u = a.slice(1);
        return z(u)(...r);
      }
      return So(r[0], a.split("."));
    }
    return s === Q.Ref ? t.getValue(o) : o;
  });
}
function Ri(e, t, n) {
  async function r(...o) {
    const s = t(...o), a = Rn({
      config: e.preSetup,
      varGetter: n
    });
    try {
      a.run();
      const u = await Sn().eventSend(e, s);
      if (!u)
        return;
      He(u, e.sets, n);
    } finally {
      a.tryReset();
    }
  }
  return r;
}
function Pi(e, t) {
  const { sets: n, code: r, inputs: o = [] } = e, s = z(r);
  function a(...u) {
    const l = o.map(({ value: c, type: i }) => {
      if (i === Q.EventContext) {
        if (c.path.startsWith(":")) {
          const f = c.path.slice(1);
          return z(f)(...u);
        }
        return bo(u[0], c.path.split("."));
      }
      if (i === Q.Ref)
        return On(t.getValue(c));
      if (i === Q.Data)
        return c;
      if (i === Q.JsFn)
        return t.getValue(c);
      throw new Error(`unknown input type ${i}`);
    }), d = s(...l);
    if (n !== void 0) {
      const i = n.length === 1 ? [d] : d, f = i.map((h) => h === void 0 ? 1 : 0);
      He(
        { values: i, types: f },
        n,
        t
      );
    }
  }
  return a;
}
function Oi(e, t) {
  const { code: n, inputs: r = {} } = e, o = ze(
    r,
    (u) => u.type !== Q.Data ? t.getVueRefObject(u.value) : u.value
  ), s = z(n, o);
  function a(...u) {
    s(...u);
  }
  return a;
}
function Ni(e) {
  const { eventName: t, info: n, handleEvent: r } = e;
  if (n.type === "vue")
    return {
      eventName: t,
      handleEvent: r
    };
  const { modifier: o = [] } = n;
  if (o.length === 0)
    return {
      eventName: t,
      handleEvent: r
    };
  const s = ["passive", "capture", "once"], a = [], u = [];
  for (const c of o)
    s.includes(c) ? a.push(c[0].toUpperCase() + c.slice(1)) : u.push(c);
  const l = a.length > 0 ? t + a.join("") : t, d = u.length > 0 ? pr(r, u) : r;
  return {
    eventName: l,
    handleEvent: d
  };
}
function ki(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((a) => t.getValue(a))
    ) : n.push(
      ze(
        s,
        (a) => t.getValue(a)
      )
    );
  });
  const r = gr([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function Ci(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return Me(n);
  const { str: r, map: o, bind: s } = n, a = [];
  return r && a.push(r), o && a.push(
    ze(
      o,
      (u) => t.getValue(u)
    )
  ), s && a.push(...s.map((u) => t.getValue(u))), Me(a);
}
function Be(e, t = !0) {
  if (!(typeof e != "object" || e === null)) {
    if (Array.isArray(e)) {
      t && e.forEach((n) => Be(n, !0));
      return;
    }
    for (const [n, r] of Object.entries(e))
      if (n.startsWith(":"))
        try {
          e[n.slice(1)] = new Function(`return (${r})`)(), delete e[n];
        } catch (o) {
          console.error(
            `Error while converting ${n} attribute to function:`,
            o
          );
        }
      else
        t && Be(r, !0);
  }
}
function Vi(e, t) {
  const n = e.startsWith(":");
  return n && (e = e.slice(1), t = z(t)), { name: e, value: t, isFunc: n };
}
function Ai(e, t, n) {
  var o;
  const r = {};
  return Mt(e.bProps || {}, (s, a) => {
    const u = n.getValue(s);
    Ve(u) || (Be(u), r[a] = Ii(u, a));
  }), (o = e.proxyProps) == null || o.forEach((s) => {
    const a = n.getValue(s);
    typeof a == "object" && Mt(a, (u, l) => {
      const { name: d, value: c } = Vi(l, u);
      r[d] = c;
    });
  }), { ...t, ...r };
}
function Ii(e, t) {
  return t === "innerText" ? Ue(e) : e;
}
const $i = W(xi, {
  props: ["slotPropValue", "config"]
});
function xi(e) {
  const { sid: t, items: n } = e.config, r = Ae(t) ? _e(t, {
    initSlotPropInfo: {
      value: e.slotPropValue
    }
  }).updateSlotPropValue : Ti;
  return () => (r({ sid: t, value: e.slotPropValue }), n.map((o) => Ee(o)));
}
function Ti() {
}
function Di(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return t ? Et(n[":"]) : Pn(n, { keyFn: (a) => a === ":" ? "default" : a, valueFn: (a) => (u) => a.use_prop ? ji(u, a) : Et(a) });
}
function ji(e, t) {
  return D($i, { config: t, slotPropValue: e });
}
function Mi(e, t, n) {
  const r = [], { dir: o = [] } = t;
  return o.forEach((s) => {
    const { sys: a, name: u, arg: l, value: d, mf: c } = s;
    if (u === "vmodel") {
      const i = n.getVueRefObject(d);
      if (e = je(e, {
        [`onUpdate:${l}`]: (f) => {
          i.value = f;
        }
      }), a === 1) {
        const f = c ? Object.fromEntries(c.map((h) => [h, !0])) : {};
        r.push([mr, i.value, void 0, f]);
      } else
        e = je(e, {
          [l]: i.value
        });
    } else if (u === "vshow") {
      const i = n.getVueRefObject(d);
      r.push([vr, i.value]);
    } else
      console.warn(`Directive ${u} is not supported yet`);
  }), fn(e, r);
}
function Wi(e, t, n) {
  const { eRef: r } = t;
  return r ? je(e, { ref: n.getVueRefObject(r) }) : e;
}
const Zn = Symbol();
function Fi(e) {
  ge(Zn, e);
}
function ya() {
  return Y(Zn);
}
const Li = W(Bi, {
  props: ["config"]
});
function Bi(e) {
  const { config: t } = e, n = ue({
    sidCollector: new Ui(t).getCollectInfo()
  });
  t.varGetterStrategy && Fi(n);
  const r = t.props ?? {};
  return Be(r, !0), () => {
    const { tag: o } = t, s = typeof o == "string" ? o : n.getValue(o), a = yr(s), u = typeof a == "string", l = Ci(t, n), { styles: d, hasStyle: c } = ki(t, n), i = Di(t, u), f = Ai(t, r, n), h = wr(f) || {};
    c && (h.style = d), l && (h.class = l);
    let g = D(a, { ...h }, i);
    return g = _i(g, t.events, n), g = Wi(g, t, n), Mi(g, t, n);
  };
}
class Ui {
  constructor(t) {
    M(this, "sids", /* @__PURE__ */ new Set());
    M(this, "needRouteParams", !0);
    M(this, "needRouter", !0);
    this.config = t;
  }
  /**
   * getCollectFn
   */
  getCollectInfo() {
    const {
      eRef: t,
      dir: n,
      classes: r,
      bProps: o,
      proxyProps: s,
      bStyle: a,
      events: u,
      varGetterStrategy: l
    } = this.config;
    if (l !== "all") {
      if (t && this._tryExtractSidToCollection(t), n && n.forEach((d) => {
        this._tryExtractSidToCollection(d.value), this._extendWithPaths(d.value);
      }), r && typeof r != "string") {
        const { map: d, bind: c } = r;
        d && Object.values(d).forEach((i) => {
          this._tryExtractSidToCollection(i), this._extendWithPaths(i);
        }), c && c.forEach((i) => {
          this._tryExtractSidToCollection(i), this._extendWithPaths(i);
        });
      }
      return o && Object.values(o).forEach((d) => {
        this._tryExtractSidToCollection(d), this._extendWithPaths(d);
      }), s && s.forEach((d) => {
        this._tryExtractSidToCollection(d), this._extendWithPaths(d);
      }), a && a.forEach((d) => {
        Array.isArray(d) ? d.forEach((c) => {
          this._tryExtractSidToCollection(c), this._extendWithPaths(c);
        }) : Object.values(d).forEach((c) => {
          this._tryExtractSidToCollection(c), this._extendWithPaths(c);
        });
      }), u && u.forEach(([d, c]) => {
        this._handleEventInputs(c), this._handleEventSets(c);
      }), Array.isArray(l) && l.forEach((d) => {
        this.sids.add(d.sid);
      }), {
        sids: this.sids,
        needRouteParams: this.needRouteParams,
        needRouter: this.needRouter
      };
    }
  }
  _tryExtractSidToCollection(t) {
    bn(t) && this.sids.add(t.sid);
  }
  _handleEventInputs(t) {
    if (t.type === "js" || t.type === "web") {
      const { inputs: n } = t;
      n == null || n.forEach((r) => {
        if (r.type === Q.Ref) {
          const o = r.value;
          this._tryExtractSidToCollection(o), this._extendWithPaths(o);
        }
      });
    } else if (t.type === "vue") {
      const { inputs: n } = t;
      if (n) {
        const r = Object.values(n);
        r == null || r.forEach((o) => {
          if (o.type === Q.Ref) {
            const s = o.value;
            this._tryExtractSidToCollection(s), this._extendWithPaths(s);
          }
        });
      }
    }
  }
  _handleEventSets(t) {
    if (t.type === "js" || t.type === "web") {
      const { sets: n } = t;
      n == null || n.forEach((r) => {
        Ot(r.ref) && (this.sids.add(r.ref.sid), this._extendWithPaths(r.ref));
      });
    }
  }
  _extendWithPaths(t) {
    if (!t.path)
      return;
    const n = [];
    for (n.push(...t.path); n.length > 0; ) {
      const r = n.pop();
      if (r === void 0)
        break;
      if (Qr(r)) {
        const o = Yr(r);
        this._tryExtractSidToCollection(o), o.path && n.push(...o.path);
      }
    }
  }
}
function Ee(e, t) {
  return oo(e) ? D(Qn, { config: e, key: t }) : so(e) ? D(Yn, { config: e, key: t }) : io(e) ? D(Xn, { config: e, key: t }) : D(Li, { config: e, key: t });
}
function Et(e, t) {
  return D(er, { slotConfig: e, key: t });
}
const er = W(Hi, {
  props: ["slotConfig"]
});
function Hi(e) {
  const { sid: t, items: n } = e.slotConfig;
  return Ae(t) && _e(t), () => n.map((r) => Ee(r));
}
function zi(e, t) {
  const { state: n, isReady: r, isLoading: o } = Br(async () => {
    let s = e;
    const a = t;
    if (!s && !a)
      throw new Error("Either config or configUrl must be provided");
    if (!s && a && (s = await (await fetch(a)).json()), !s)
      throw new Error("Failed to load config");
    return s;
  }, {});
  return { config: n, isReady: r, isLoading: o };
}
function Gi(e) {
  const t = J(!1), n = J("");
  function r(o, s) {
    let a;
    return s.component ? a = `Error captured from component:tag: ${s.component.tag} ; id: ${s.component.id} ` : a = "Error captured from app init", console.group(a), console.error("Component:", s.component), console.error("Error:", o), console.groupEnd(), e && (t.value = !0, n.value = `${a} ${o.message}`), !1;
  }
  return Er(r), { hasError: t, errorMessage: n };
}
let _t;
function Ki(e) {
  if (e === "web" || e === "webview") {
    _t = qi;
    return;
  }
  if (e === "zero") {
    _t = Ji;
    return;
  }
  throw new Error(`Unsupported mode: ${e}`);
}
function qi(e) {
  const { assetPath: t = "/assets/icons", icon: n = "" } = e, [r, o] = n.split(":");
  return {
    assetPath: t,
    svgName: `${r}.svg`
  };
}
function Ji() {
  return {
    assetPath: "",
    svgName: ""
  };
}
function Qi(e, t) {
  const n = B(() => {
    const r = e.value;
    if (!r)
      return null;
    const a = new DOMParser().parseFromString(r, "image/svg+xml").querySelector("svg");
    if (!a)
      throw new Error("Invalid svg string");
    const u = {};
    for (const f of a.attributes)
      u[f.name] = f.value;
    const { size: l, color: d, attrs: c } = t;
    d.value !== null && d.value !== void 0 && (a.removeAttribute("fill"), a.querySelectorAll("*").forEach((h) => {
      h.hasAttribute("fill") && h.setAttribute("fill", "currentColor");
    }), u.color = d.value), l.value !== null && l.value !== void 0 && (u.width = l.value.toString(), u.height = l.value.toString());
    const i = a.innerHTML;
    return {
      ...u,
      ...c,
      innerHTML: i
    };
  });
  return () => {
    if (!n.value)
      return null;
    const r = n.value;
    return D("svg", r);
  };
}
const Yi = {
  class: "app-box insta-themes",
  "data-scaling": "100%"
}, Xi = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Zi = {
  key: 0,
  style: { color: "red", "font-size": "1.2em", margin: "1rem", border: "1px dashed red", padding: "1rem" }
}, ea = /* @__PURE__ */ W({
  __name: "App",
  props: {
    config: {},
    meta: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { debug: n = !1 } = t.meta, { config: r, isLoading: o } = zi(
      t.config,
      t.configUrl
    );
    q(r, (u) => {
      u.url && (Nr({
        mode: t.meta.mode,
        version: t.meta.version,
        queryPath: u.url.path,
        pathParams: u.url.params,
        webServerInfo: u.webInfo
      }), fo(t.meta.mode)), Ki(t.meta.mode), kr(u);
    });
    const { hasError: s, errorMessage: a } = Gi(n);
    return (u, l) => (ee(), ie("div", Yi, [
      L(o) ? (ee(), ie("div", Xi, l[0] || (l[0] = [
        dn("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (ee(), ie("div", {
        key: 1,
        class: Me(["insta-main", L(r).class])
      }, [
        _r(L(er), { "slot-config": L(r) }, null, 8, ["slot-config"]),
        L(s) ? (ee(), ie("div", Zi, Ue(L(a)), 1)) : st("", !0)
      ], 2))
    ]));
  }
});
function ta(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => D(
    ln,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const na = W(ta, {
  props: ["name", "tag"]
});
function ra(e) {
  const { content: t, r: n = 0 } = e, r = ue(), o = n === 1 ? () => r.getValue(t) : () => t;
  return () => Ue(o());
}
const oa = W(ra, {
  props: ["content", "r"]
});
function sa(e) {
  return `i-size-${e}`;
}
function ia(e) {
  return e ? `i-weight-${e}` : "";
}
function aa(e) {
  return e ? `i-text-align-${e}` : "";
}
const ca = /* @__PURE__ */ W({
  __name: "Heading",
  props: {
    text: {},
    size: {},
    weight: {},
    align: {}
  },
  setup(e) {
    const t = e, n = B(() => [
      sa(t.size ?? "6"),
      ia(t.weight),
      aa(t.align)
    ]);
    return (r, o) => (ee(), ie("h1", {
      class: Me(["insta-Heading", n.value])
    }, Ue(r.text), 3));
  }
}), ua = /* @__PURE__ */ W({
  __name: "_Teleport",
  props: {
    to: {},
    defer: { type: Boolean, default: !0 },
    disabled: { type: Boolean, default: !1 }
  },
  setup(e) {
    return (t, n) => (ee(), hn(br, {
      to: t.to,
      defer: t.defer,
      disabled: t.disabled
    }, [
      Sr(t.$slots, "default")
    ], 8, ["to", "defer", "disabled"]));
  }
}), la = ["width", "height", "color"], fa = ["xlink:href"], da = /* @__PURE__ */ W({
  __name: "Icon",
  props: {
    size: {},
    icon: {},
    color: {},
    assetPath: {},
    svgName: {},
    rawSvg: {}
  },
  setup(e) {
    const t = e, { assetPath: n, svgName: r } = _t(t), o = de(() => t.icon ? t.icon.split(":")[1] : ""), s = de(() => t.size || "1em"), a = de(() => t.color || "currentColor"), u = de(() => t.rawSvg || null), l = B(() => `${n}/${r}/#${o.value}`), d = Rr(), c = Qi(u, {
      size: de(() => t.size),
      color: de(() => t.color),
      attrs: d
    });
    return (i, f) => (ee(), ie(pn, null, [
      o.value ? (ee(), ie("svg", Pr({
        key: 0,
        width: s.value,
        height: s.value,
        color: a.value
      }, L(d)), [
        dn("use", { "xlink:href": l.value }, null, 8, fa)
      ], 16, la)) : st("", !0),
      u.value ? (ee(), hn(L(c), { key: 1 })) : st("", !0)
    ], 64));
  }
});
function ha(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => tr(o, n)
  );
}
function tr(e, t) {
  var u;
  const { server: n = !1, vueItem: r } = e, o = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(pa(e, t));
  }, s = (u = r.children) == null ? void 0 : u.map(
    (l) => tr(l, t)
  ), a = {
    ...r,
    children: s,
    component: o
  };
  return r.component.length === 0 && delete a.component, s === void 0 && delete a.children, a;
}
function pa(e, t) {
  const { sid: n, vueItem: r } = e, { path: o, component: s } = r, a = Et(
    {
      items: s,
      sid: n
    },
    o
  ), u = D(pn, null, a);
  return t ? D(Or, null, () => a) : u;
}
function ga(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? fs() : n === "memory" ? ls() : Mn();
  e.use(
    ti({
      history: r,
      routes: ha(t)
    })
  );
}
function wa(e, t) {
  e.component("insta-ui", ea), e.component("vif", Yn), e.component("vfor", Qn), e.component("match", Xn), e.component("teleport", ua), e.component("icon", da), e.component("ts-group", na), e.component("content", oa), e.component("heading", ca), t.router && ga(e, t);
}
export {
  Be as convertDynamicProperties,
  wa as install,
  ya as useVarGetter
};
//# sourceMappingURL=insta-ui.js.map
