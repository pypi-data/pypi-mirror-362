var Jn = Object.defineProperty;
var Qn = (e, t, n) => t in e ? Jn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var T = (e, t, n) => Qn(e, typeof t != "symbol" ? t + "" : t, n);
import * as Yn from "vue";
import { unref as M, watch as z, nextTick as Ne, isRef as Qt, ref as Y, shallowRef as H, watchEffect as Yt, computed as W, toRaw as Xt, customRef as ue, toValue as Ye, readonly as Xn, provide as le, inject as K, shallowReactive as Zn, defineComponent as D, reactive as er, h as x, getCurrentInstance as Zt, onUnmounted as tr, renderList as nr, TransitionGroup as en, cloneVNode as Ve, withDirectives as tn, withModifiers as rr, normalizeStyle as or, normalizeClass as Ce, toDisplayString as xe, vModelDynamic as sr, vShow as ir, resolveDynamicComponent as ar, normalizeProps as cr, onErrorCaptured as ur, openBlock as Q, createElementBlock as ne, createElementVNode as nn, createVNode as lr, createCommentVNode as Xe, createBlock as rn, Teleport as fr, renderSlot as dr, toRef as ie, useAttrs as hr, Fragment as on, mergeProps as pr, KeepAlive as gr } from "vue";
let sn;
function mr(e) {
  sn = e;
}
function Ze() {
  return sn;
}
function Ie() {
  const { queryPath: e, pathParams: t, queryParams: n } = Ze();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
const gt = /* @__PURE__ */ new Map();
function vr(e) {
  var t;
  (t = e.scopes) == null || t.forEach((n) => {
    gt.set(n.id, n);
  });
}
function Ge(e) {
  return gt.get(e);
}
function Pe(e) {
  return e && gt.has(e);
}
function ve(e) {
  return typeof e == "function" ? e() : M(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const et = () => {
};
function tt(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function nt(e, t = !1) {
  function n(i, { flush: f = "sync", deep: h = !1, timeout: g, throwOnTimeout: m } = {}) {
    let v = null;
    const b = [new Promise((R) => {
      v = z(
        e,
        (N) => {
          i(N) !== t && (v ? v() : Ne(() => v == null ? void 0 : v()), R(N));
        },
        {
          flush: f,
          deep: h,
          immediate: !0
        }
      );
    })];
    return g != null && b.push(
      tt(g, m).then(() => ve(e)).finally(() => v == null ? void 0 : v())
    ), Promise.race(b);
  }
  function r(i, f) {
    if (!Qt(i))
      return n((N) => N === i, f);
    const { flush: h = "sync", deep: g = !1, timeout: m, throwOnTimeout: v } = f ?? {};
    let w = null;
    const R = [new Promise((N) => {
      w = z(
        [e, i],
        ([A, B]) => {
          t !== (A === B) && (w ? w() : Ne(() => w == null ? void 0 : w()), N(A));
        },
        {
          flush: h,
          deep: g,
          immediate: !0
        }
      );
    })];
    return m != null && R.push(
      tt(m, v).then(() => ve(e)).finally(() => (w == null || w(), ve(e)))
    ), Promise.race(R);
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
      return g.includes(i) || g.includes(ve(i));
    }, f);
  }
  function d(i) {
    return c(1, i);
  }
  function c(i = 1, f) {
    let h = -1;
    return n(() => (h += 1, h >= i), f);
  }
  return Array.isArray(ve(e)) ? {
    toMatch: n,
    toContains: l,
    changed: d,
    changedTimes: c,
    get not() {
      return nt(e, !t);
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
      return nt(e, !t);
    }
  };
}
function yr(e) {
  return nt(e);
}
function _r(e, t, n) {
  let r;
  Qt(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: a = !0,
    onError: u = et
  } = r, l = Y(!o), d = a ? H(t) : Y(t);
  let c = 0;
  return Yt(async (i) => {
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
  }), o ? W(() => (l.value = !0, d.value)) : d;
}
function wr(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = et,
    onSuccess: a = et,
    resetOnExecute: u = !0,
    shallow: l = !0,
    throwError: d
  } = {}, c = l ? H(t) : Y(t), i = Y(!1), f = Y(!1), h = H(void 0);
  async function g(w = 0, ...b) {
    u && (c.value = t), h.value = void 0, i.value = !1, f.value = !0, w > 0 && await tt(w);
    const R = typeof e == "function" ? e(...b) : e;
    try {
      const N = await R;
      c.value = N, i.value = !0, a(N);
    } catch (N) {
      if (h.value = N, s(N), d)
        throw N;
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
    return new Promise((w, b) => {
      yr(f).toBe(!1).then(() => w(m)).catch(b);
    });
  }
  return {
    ...m,
    then(w, b) {
      return v().then(w, b);
    }
  };
}
function L(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Yn];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function Er(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return L(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function an(e) {
  return e.constructor.name === "AsyncFunction";
}
class br {
  toString() {
    return "";
  }
}
const be = new br();
function Re(e) {
  return Xt(e) === be;
}
function Rr(e) {
  return Array.isArray(e) && e[0] === "bind";
}
function Pr(e) {
  return e[1];
}
function cn(e, t, n) {
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
  const r = un(t, n);
  return e[r];
}
function un(e, t) {
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
function ln(e, t, n) {
  return t.reduce(
    (r, o) => cn(r, o, n),
    e
  );
}
function fn(e, t, n, r) {
  t.reduce((o, s, a) => {
    if (a === t.length - 1)
      o[un(s, r)] = n;
    else
      return cn(o, s, r);
  }, e);
}
function Sr(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: a } = t;
  return r === void 0 || r.length === 0 ? e : ue(() => ({
    get() {
      try {
        return ln(
          Ye(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(u) {
      fn(
        Ye(e),
        s || r,
        u,
        a
      );
    }
  }));
}
function mt(e) {
  return ue((t, n) => ({
    get() {
      return t(), e;
    },
    set(r) {
      !Re(e) && JSON.stringify(r) === JSON.stringify(e) || (e = r, n());
    }
  }));
}
function Or(e, t) {
  const { deepCompare: n = !1 } = e;
  return n ? mt(e.value) : Y(e.value);
}
function kr(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, a = Object.values(r).map((c, i) => s[i] === 1 ? c : t.getVueRefObject(c));
  if (an(new Function(o)))
    return _r(
      async () => {
        const c = Object.fromEntries(
          Object.keys(r).map((i, f) => [i, a[f]])
        );
        return await L(o, c)();
      },
      null,
      { lazy: !0 }
    );
  const u = Object.fromEntries(
    Object.keys(r).map((c, i) => [c, a[i]])
  ), l = L(o, u);
  return W(l);
}
function Nr(e) {
  const { init: t, deepEqOnInput: n } = e;
  return n === void 0 ? H(t ?? be) : mt(t ?? be);
}
function Vr(e, t, n) {
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
  const h = L(o), g = l === 0 ? H(be) : mt(be), m = { immediate: !0, deep: !0 };
  return an(h) ? (g.value = u, z(
    i,
    async () => {
      f().some(Re) || (g.value = await h(...f()));
    },
    m
  )) : z(
    i,
    () => {
      const v = f();
      v.some(Re) || (g.value = h(...v));
    },
    m
  ), Xn(g);
}
function Cr(e) {
  return e.tag === "vfor";
}
function Ir(e) {
  return e.tag === "vif";
}
function Ar(e) {
  return e.tag === "match";
}
function dn(e) {
  return !("type" in e);
}
function $r(e) {
  return "type" in e && e.type === "rp";
}
function vt(e) {
  return "sid" in e && "id" in e;
}
class xr extends Map {
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
function yt(e) {
  return new xr(e);
}
class Tr {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, a = Ze().webServerInfo, u = s !== void 0 ? { key: s } : {}, l = r === "sync" ? a.event_url : a.event_async_url;
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
        page: Ie(),
        ...d
      })
    });
    if (!c.ok)
      throw new Error(`HTTP error! status: ${c.status}`);
    return await c.json();
  }
  async watchSend(t) {
    const { fType: n, key: r } = t.watchConfig, o = Ze().webServerInfo, s = n === "sync" ? o.watch_url : o.watch_async_url, a = t.getServerInputs(), u = {
      key: r,
      input: a,
      page: Ie()
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
class Dr {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, a = s !== void 0 ? { key: s } : {};
    let u = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...a,
      page: Ie(),
      ...u
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { fType: n, key: r } = t.watchConfig, o = t.getServerInputs(), s = {
      key: r,
      input: o,
      fType: n,
      page: Ie()
    };
    return await window.pywebview.api.watch_call(s);
  }
}
let rt;
function jr(e) {
  switch (e) {
    case "web":
      rt = new Tr();
      break;
    case "webview":
      rt = new Dr();
      break;
  }
}
function hn() {
  return rt;
}
var G = /* @__PURE__ */ ((e) => (e[e.Ref = 0] = "Ref", e[e.EventContext = 1] = "EventContext", e[e.Data = 2] = "Data", e[e.JsFn = 3] = "JsFn", e))(G || {}), ot = /* @__PURE__ */ ((e) => (e.const = "c", e.ref = "r", e.range = "n", e))(ot || {}), ce = /* @__PURE__ */ ((e) => (e[e.Ref = 0] = "Ref", e[e.RouterAction = 1] = "RouterAction", e[e.ElementRefAction = 2] = "ElementRefAction", e[e.JsCode = 3] = "JsCode", e))(ce || {});
function Mr(e, t) {
  const r = {
    ref: {
      id: t.id,
      sid: e
    },
    type: ce.Ref
  };
  return {
    ...t,
    immediate: !0,
    outputs: [r, ...t.outputs || []]
  };
}
function pn(e) {
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
        const v = Wr(m, n);
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
function Wr(e, t) {
  const { inputs: n = [], code: r } = e, o = L(r), s = n.map((a) => t.getValue(a));
  return o(...s);
}
function kt(e) {
  return e == null;
}
function Te(e, t, n) {
  if (kt(t) || kt(e.values))
    return;
  t = t;
  const r = e.values, o = e.types ?? Array.from({ length: t.length }).fill(0);
  t.forEach((s, a) => {
    const u = o[a];
    if (u === 1)
      return;
    if (s.type === ce.Ref) {
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
    if (s.type === ce.RouterAction) {
      const d = r[a], c = n.getRouter()[d.fn];
      c(...d.args);
      return;
    }
    if (s.type === ce.ElementRefAction) {
      const d = s.ref, c = n.getVueRefObject(d).value, i = r[a], { method: f, args: h = [] } = i;
      c[f](...h);
      return;
    }
    if (s.type === ce.JsCode) {
      const d = r[a];
      if (!d)
        return;
      const c = L(d);
      Promise.resolve(c());
      return;
    }
    const l = n.getVueRefObject(
      s.ref
    );
    l.value = r[a];
  });
}
function Br(e) {
  const { watchConfigs: t, computedConfigs: n, varMapGetter: r, sid: o } = e;
  return new Lr(t, n, r, o);
}
class Lr {
  constructor(t, n, r, o) {
    T(this, "taskQueue", []);
    T(this, "id2TaskMap", /* @__PURE__ */ new Map());
    T(this, "input2TaskIdMap", yt(() => []));
    this.varMapGetter = r;
    const s = [], a = (u) => {
      var d;
      const l = new Fr(u, r);
      return this.id2TaskMap.set(l.id, l), (d = u.inputs) == null || d.forEach((c, i) => {
        var h, g;
        if (((h = u.data) == null ? void 0 : h[i]) === 0 && ((g = u.slient) == null ? void 0 : g[i]) === 0) {
          if (!dn(c))
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
        Mr(o, u)
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
      z(
        h,
        (g) => {
          g.some(Re) || (u.modify = !0, this.taskQueue.push(new Ur(u)), this._scheduleNextTick());
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
    Ne(() => this._runAllTasks());
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
      if (!vt(r.ref))
        throw new Error("Non-var output bindings are not supported.");
      const { sid: o, id: s } = r.ref, a = `${o}-${s}`;
      (this.input2TaskIdMap.get(a) || []).forEach((l) => n.add(l));
    }), n;
  }
}
class Fr {
  constructor(t, n) {
    T(this, "modify", !0);
    T(this, "_running", !1);
    T(this, "id");
    T(this, "_runningPromise", null);
    T(this, "_runningPromiseResolve", null);
    T(this, "_inputInfos");
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
class Ur {
  /**
   *
   */
  constructor(t) {
    T(this, "prevNodes", []);
    T(this, "nextNodes", []);
    T(this, "_runningPrev", !1);
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
        await Hr(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function Hr(e) {
  const { varMapGetter: t } = e, { outputs: n, preSetup: r } = e.watchConfig, o = pn({
    config: r,
    varGetter: t
  });
  try {
    o.run(), e.taskDone();
    const s = await hn().watchSend(e);
    if (!s)
      return;
    Te(s, n, t);
  } finally {
    o.tryReset();
  }
}
function Nt(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function De(e, t) {
  return gn(e, {
    valueFn: t
  });
}
function gn(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s], a) => [
      r ? r(o, s) : o,
      n(s, o, a)
    ])
  );
}
function Gr(e, t, n) {
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
  const r = zr(t);
  return e[r];
}
function zr(e, t) {
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
function Kr(e, t, n) {
  return t.reduce(
    (r, o) => Gr(r, o),
    e
  );
}
function qr(e, t) {
  return t ? t.reduce((n, r) => n[r], e) : e;
}
const Jr = window.structuredClone || ((e) => JSON.parse(JSON.stringify(e)));
function mn(e) {
  return typeof e == "function" ? e : Jr(Xt(e));
}
function Qr(e, t) {
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
  } = e, i = d || Array.from({ length: n.length }).fill(0), f = c || Array.from({ length: Object.keys(l).length }).fill(0), h = De(
    l,
    (v, w, b) => f[b] === 0 ? t.getVueRefObject(v) : v
  ), g = L(r, h), m = n.length === 1 ? Vt(i[0] === 1, n[0], t) : n.map(
    (v, w) => Vt(i[w] === 1, v, t)
  );
  return z(m, g, { immediate: o, deep: s, once: a, flush: u });
}
function Vt(e, t, n) {
  return e ? () => t : n.getVueRefObject(t);
}
function Yr(e, t) {
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
  } = e, i = o || Array.from({ length: n.length }).fill(0), f = s || Array.from({ length: n.length }).fill(0), h = L(a), g = n.filter((v, w) => i[w] === 0 && f[w] === 0).map((v) => t.getVueRefObject(v));
  function m() {
    return n.map((v, w) => f[w] === 0 ? mn(t.getValue(v)) : v);
  }
  z(
    g,
    () => {
      let v = h(...m());
      if (!r)
        return;
      const b = r.length === 1 ? [v] : v, R = b.map((N) => N === void 0 ? 1 : 0);
      Te(
        {
          values: b,
          types: R
        },
        r,
        t
      );
    },
    { immediate: u, deep: l, once: d, flush: c }
  );
}
const st = yt(() => Symbol());
function Xr(e, t) {
  const n = e.sid, r = st.getOrDefault(n);
  st.set(n, r), le(r, t);
}
function Zr(e) {
  const t = st.get(e);
  return K(t);
}
function eo() {
  return vn().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function vn() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const to = typeof Proxy == "function", no = "devtools-plugin:setup", ro = "plugin:settings:set";
let ae, it;
function oo() {
  var e;
  return ae !== void 0 || (typeof window < "u" && window.performance ? (ae = !0, it = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (ae = !0, it = globalThis.perf_hooks.performance) : ae = !1), ae;
}
function so() {
  return oo() ? it.now() : Date.now();
}
class io {
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
        return so();
      }
    }, n && n.on(ro, (a, u) => {
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
function ao(e, t) {
  const n = e, r = vn(), o = eo(), s = to && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(no, e, t);
  else {
    const a = s ? new io(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: a
    }), a && t(a.proxiedTarget);
  }
}
var P = {};
const J = typeof document < "u";
function yn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function co(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && yn(e.default);
}
const V = Object.assign;
function ze(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = F(o) ? o.map(e) : e(o);
  }
  return n;
}
const we = () => {
}, F = Array.isArray;
function S(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const _n = /#/g, uo = /&/g, lo = /\//g, fo = /=/g, ho = /\?/g, wn = /\+/g, po = /%5B/g, go = /%5D/g, En = /%5E/g, mo = /%60/g, bn = /%7B/g, vo = /%7C/g, Rn = /%7D/g, yo = /%20/g;
function _t(e) {
  return encodeURI("" + e).replace(vo, "|").replace(po, "[").replace(go, "]");
}
function _o(e) {
  return _t(e).replace(bn, "{").replace(Rn, "}").replace(En, "^");
}
function at(e) {
  return _t(e).replace(wn, "%2B").replace(yo, "+").replace(_n, "%23").replace(uo, "%26").replace(mo, "`").replace(bn, "{").replace(Rn, "}").replace(En, "^");
}
function wo(e) {
  return at(e).replace(fo, "%3D");
}
function Eo(e) {
  return _t(e).replace(_n, "%23").replace(ho, "%3F");
}
function bo(e) {
  return e == null ? "" : Eo(e).replace(lo, "%2F");
}
function fe(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    P.NODE_ENV !== "production" && S(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const Ro = /\/$/, Po = (e) => e.replace(Ro, "");
function Ke(e, t, n = "/") {
  let r, o = {}, s = "", a = "";
  const u = t.indexOf("#");
  let l = t.indexOf("?");
  return u < l && u >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, u > -1 ? u : t.length), o = e(s)), u > -1 && (r = r || t.slice(0, u), a = t.slice(u, t.length)), r = ko(r ?? t, n), {
    fullPath: r + (s && "?") + s + a,
    path: r,
    query: o,
    hash: fe(a)
  };
}
function So(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function Ct(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function It(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && ee(t.matched[r], n.matched[o]) && Pn(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function ee(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function Pn(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!Oo(e[n], t[n]))
      return !1;
  return !0;
}
function Oo(e, t) {
  return F(e) ? At(e, t) : F(t) ? At(t, e) : e === t;
}
function At(e, t) {
  return F(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function ko(e, t) {
  if (e.startsWith("/"))
    return e;
  if (P.NODE_ENV !== "production" && !t.startsWith("/"))
    return S(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
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
const X = {
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
var de;
(function(e) {
  e.pop = "pop", e.push = "push";
})(de || (de = {}));
var re;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(re || (re = {}));
const qe = "";
function Sn(e) {
  if (!e)
    if (J) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), Po(e);
}
const No = /^[^#]+#/;
function On(e, t) {
  return e.replace(No, "#") + t;
}
function Vo(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const je = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function Co(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (P.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          S(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        S(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      P.NODE_ENV !== "production" && S(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = Vo(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function $t(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const ct = /* @__PURE__ */ new Map();
function Io(e, t) {
  ct.set(e, t);
}
function Ao(e) {
  const t = ct.get(e);
  return ct.delete(e), t;
}
let $o = () => location.protocol + "//" + location.host;
function kn(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let u = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(u);
    return l[0] !== "/" && (l = "/" + l), Ct(l, "");
  }
  return Ct(n, e) + r + o;
}
function xo(e, t, n, r) {
  let o = [], s = [], a = null;
  const u = ({ state: f }) => {
    const h = kn(e, location), g = n.value, m = t.value;
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
        type: de.pop,
        direction: v ? v > 0 ? re.forward : re.back : re.unknown
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
    f.state && f.replaceState(V({}, f.state, { scroll: je() }), "");
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
function xt(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? je() : null
  };
}
function To(e) {
  const { history: t, location: n } = window, r = {
    value: kn(e, n)
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
    const i = e.indexOf("#"), f = i > -1 ? (n.host && document.querySelector("base") ? e : e.slice(i)) + l : $o() + e + l;
    try {
      t[c ? "replaceState" : "pushState"](d, "", f), o.value = d;
    } catch (h) {
      P.NODE_ENV !== "production" ? S("Error with push/replace State", h) : console.error(h), n[c ? "replace" : "assign"](f);
    }
  }
  function a(l, d) {
    const c = V({}, t.state, xt(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), d, { position: o.value.position });
    s(l, c, !0), r.value = l;
  }
  function u(l, d) {
    const c = V(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: je()
      }
    );
    P.NODE_ENV !== "production" && !t.state && S(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(c.current, c, !0);
    const i = V({}, xt(r.value, l, null), { position: c.position + 1 }, d);
    s(l, i, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: u,
    replace: a
  };
}
function Nn(e) {
  e = Sn(e);
  const t = To(e), n = xo(e, t.state, t.location, t.replace);
  function r(s, a = !0) {
    a || n.pauseListeners(), history.go(s);
  }
  const o = V({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: On.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function Do(e = "") {
  let t = [], n = [qe], r = 0;
  e = Sn(e);
  function o(u) {
    r++, r !== n.length && n.splice(r), n.push(u);
  }
  function s(u, l, { direction: d, delta: c }) {
    const i = {
      direction: d,
      delta: c,
      type: de.pop
    };
    for (const f of t)
      f(u, l, i);
  }
  const a = {
    // rewritten by Object.defineProperty
    location: qe,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: On.bind(null, e),
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
      t = [], n = [qe], r = 0;
    },
    go(u, l = !0) {
      const d = this.location, c = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        u < 0 ? re.back : re.forward
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
function jo(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), P.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && S(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), Nn(e);
}
function Ae(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function Vn(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const ut = Symbol(P.NODE_ENV !== "production" ? "navigation failure" : "");
var Tt;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(Tt || (Tt = {}));
const Mo = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${Bo(t)}" via a navigation guard.`;
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
function he(e, t) {
  return P.NODE_ENV !== "production" ? V(new Error(Mo[e](t)), {
    type: e,
    [ut]: !0
  }, t) : V(new Error(), {
    type: e,
    [ut]: !0
  }, t);
}
function q(e, t) {
  return e instanceof Error && ut in e && (t == null || !!(e.type & t));
}
const Wo = ["params", "query", "hash"];
function Bo(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of Wo)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const Dt = "[^/]+?", Lo = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, Fo = /[.+*?^${}()[\]/\\]/g;
function Uo(e, t) {
  const n = V({}, Lo, t), r = [];
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
        i || (o += "/"), o += f.value.replace(Fo, "\\$&"), h += 40;
      else if (f.type === 1) {
        const { value: g, repeatable: m, optional: v, regexp: w } = f;
        s.push({
          name: g,
          repeatable: m,
          optional: v
        });
        const b = w || Dt;
        if (b !== Dt) {
          h += 10;
          try {
            new RegExp(`(${b})`);
          } catch (N) {
            throw new Error(`Invalid custom RegExp for param "${g}" (${b}): ` + N.message);
          }
        }
        let R = m ? `((?:${b})(?:/(?:${b}))*)` : `(${b})`;
        i || (R = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        v && d.length < 2 ? `(?:/${R})` : "/" + R), v && (R += "?"), o += R, h += 20, v && (h += -8), m && (h += -20), b === ".*" && (h += -50);
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
          if (F(w) && !m)
            throw new Error(`Provided param "${g}" is an array but it is not repeatable (* or + modifiers)`);
          const b = F(w) ? w.join("/") : w;
          if (!b)
            if (v)
              f.length < 2 && (c.endsWith("/") ? c = c.slice(0, -1) : i = !0);
            else
              throw new Error(`Missing required param "${g}"`);
          c += b;
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
function Ho(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function Cn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = Ho(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (jt(r))
      return 1;
    if (jt(o))
      return -1;
  }
  return o.length - r.length;
}
function jt(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const Go = {
  type: 0,
  value: ""
}, zo = /[a-zA-Z0-9_]/;
function Ko(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[Go]];
  if (!e.startsWith("/"))
    throw new Error(P.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
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
        l === "(" ? n = 2 : zo.test(l) ? f() : (i(), n = 0, l !== "*" && l !== "?" && l !== "+" && u--);
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
function qo(e, t, n) {
  const r = Uo(Ko(e.path), n);
  if (P.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const a of r.keys)
      s.has(a.name) && S(`Found duplicated params with name "${a.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(a.name);
  }
  const o = V(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function Jo(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = Lt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(i) {
    return r.get(i);
  }
  function s(i, f, h) {
    const g = !h, m = Wt(i);
    P.NODE_ENV !== "production" && Zo(m, f), m.aliasOf = h && h.record;
    const v = Lt(t, i), w = [m];
    if ("alias" in i) {
      const N = typeof i.alias == "string" ? [i.alias] : i.alias;
      for (const A of N)
        w.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          Wt(V({}, m, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: h ? h.record.components : m.components,
            path: A,
            // we might be the child of an alias
            aliasOf: h ? h.record : m
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let b, R;
    for (const N of w) {
      const { path: A } = N;
      if (f && A[0] !== "/") {
        const B = f.record.path, U = B[B.length - 1] === "/" ? "" : "/";
        N.path = f.record.path + (A && U + A);
      }
      if (P.NODE_ENV !== "production" && N.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (b = qo(N, f, v), P.NODE_ENV !== "production" && f && A[0] === "/" && ts(b, f), h ? (h.alias.push(b), P.NODE_ENV !== "production" && Xo(h, b)) : (R = R || b, R !== b && R.alias.push(b), g && i.name && !Bt(b) && (P.NODE_ENV !== "production" && es(i, f), a(i.name))), In(b) && l(b), m.children) {
        const B = m.children;
        for (let U = 0; U < B.length; U++)
          s(B[U], b, h && h.children[U]);
      }
      h = h || b;
    }
    return R ? () => {
      a(R);
    } : we;
  }
  function a(i) {
    if (Vn(i)) {
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
    const f = ns(i, n);
    n.splice(f, 0, i), i.record.name && !Bt(i) && r.set(i.record.name, i);
  }
  function d(i, f) {
    let h, g = {}, m, v;
    if ("name" in i && i.name) {
      if (h = r.get(i.name), !h)
        throw he(1, {
          location: i
        });
      if (P.NODE_ENV !== "production") {
        const R = Object.keys(i.params || {}).filter((N) => !h.keys.find((A) => A.name === N));
        R.length && S(`Discarded invalid param(s) "${R.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      v = h.record.name, g = V(
        // paramsFromLocation is a new object
        Mt(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          h.keys.filter((R) => !R.optional).concat(h.parent ? h.parent.keys.filter((R) => R.optional) : []).map((R) => R.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        i.params && Mt(i.params, h.keys.map((R) => R.name))
      ), m = h.stringify(g);
    } else if (i.path != null)
      m = i.path, P.NODE_ENV !== "production" && !m.startsWith("/") && S(`The Matcher cannot resolve relative paths but received "${m}". Unless you directly called \`matcher.resolve("${m}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), h = n.find((R) => R.re.test(m)), h && (g = h.parse(m), v = h.record.name);
    else {
      if (h = f.name ? r.get(f.name) : n.find((R) => R.re.test(f.path)), !h)
        throw he(1, {
          location: i,
          currentLocation: f
        });
      v = h.record.name, g = V({}, f.params, i.params), m = h.stringify(g);
    }
    const w = [];
    let b = h;
    for (; b; )
      w.unshift(b.record), b = b.parent;
    return {
      name: v,
      path: m,
      params: g,
      matched: w,
      meta: Yo(w)
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
function Mt(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function Wt(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: Qo(e),
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
function Qo(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function Bt(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function Yo(e) {
  return e.reduce((t, n) => V(t, n.meta), {});
}
function Lt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function lt(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Xo(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(lt.bind(null, n)))
      return S(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(lt.bind(null, n)))
      return S(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function Zo(e, t) {
  t && t.record.name && !e.name && !e.path && S(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function es(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function ts(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(lt.bind(null, n)))
      return S(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function ns(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    Cn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = rs(e);
  return o && (r = t.lastIndexOf(o, r - 1), P.NODE_ENV !== "production" && r < 0 && S(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function rs(e) {
  let t = e;
  for (; t = t.parent; )
    if (In(t) && Cn(e, t) === 0)
      return t;
}
function In({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function os(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(wn, " "), a = s.indexOf("="), u = fe(a < 0 ? s : s.slice(0, a)), l = a < 0 ? null : fe(s.slice(a + 1));
    if (u in t) {
      let d = t[u];
      F(d) || (d = t[u] = [d]), d.push(l);
    } else
      t[u] = l;
  }
  return t;
}
function Ft(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = wo(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (F(r) ? r.map((s) => s && at(s)) : [r && at(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function ss(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = F(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const is = Symbol(P.NODE_ENV !== "production" ? "router view location matched" : ""), Ut = Symbol(P.NODE_ENV !== "production" ? "router view depth" : ""), Me = Symbol(P.NODE_ENV !== "production" ? "router" : ""), wt = Symbol(P.NODE_ENV !== "production" ? "route location" : ""), ft = Symbol(P.NODE_ENV !== "production" ? "router view location" : "");
function ye() {
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
function Z(e, t, n, r, o, s = (a) => a()) {
  const a = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((u, l) => {
    const d = (f) => {
      f === !1 ? l(he(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Ae(f) ? l(he(2, {
        from: t,
        to: f
      })) : (a && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === a && typeof f == "function" && a.push(f), u());
    }, c = s(() => e.call(r && r.instances[o], t, n, P.NODE_ENV !== "production" ? as(d, t, n) : d));
    let i = Promise.resolve(c);
    if (e.length < 3 && (i = i.then(d)), P.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof c == "object" && "then" in c)
        i = i.then((h) => d._called ? h : (S(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (c !== void 0 && !d._called) {
        S(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    i.catch((f) => l(f));
  });
}
function as(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && S(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function Je(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const a of e) {
    P.NODE_ENV !== "production" && !a.components && !a.children.length && S(`Record with path "${a.path}" is either missing a "component(s)" or "children" property.`);
    for (const u in a.components) {
      let l = a.components[u];
      if (P.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw S(`Component "${u}" in record with path "${a.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          S(`Component "${u}" in record with path "${a.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const d = l;
          l = () => d;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, S(`Component "${u}" in record with path "${a.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !a.instances[u]))
        if (yn(l)) {
          const c = (l.__vccOpts || l)[t];
          c && s.push(Z(c, n, r, a, u, o));
        } else {
          let d = l();
          P.NODE_ENV !== "production" && !("catch" in d) && (S(`Component "${u}" in record with path "${a.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), d = Promise.resolve(d)), s.push(() => d.then((c) => {
            if (!c)
              throw new Error(`Couldn't resolve component "${u}" at "${a.path}"`);
            const i = co(c) ? c.default : c;
            a.mods[u] = c, a.components[u] = i;
            const h = (i.__vccOpts || i)[t];
            return h && Z(h, n, r, a, u, o)();
          }));
        }
    }
  }
  return s;
}
function Ht(e) {
  const t = K(Me), n = K(wt);
  let r = !1, o = null;
  const s = W(() => {
    const c = M(e.to);
    return P.NODE_ENV !== "production" && (!r || c !== o) && (Ae(c) || (r ? S(`Invalid value for prop "to" in useLink()
- to:`, c, `
- previous to:`, o, `
- props:`, e) : S(`Invalid value for prop "to" in useLink()
- to:`, c, `
- props:`, e)), o = c, r = !0), t.resolve(c);
  }), a = W(() => {
    const { matched: c } = s.value, { length: i } = c, f = c[i - 1], h = n.matched;
    if (!f || !h.length)
      return -1;
    const g = h.findIndex(ee.bind(null, f));
    if (g > -1)
      return g;
    const m = Gt(c[i - 2]);
    return (
      // we are dealing with nested routes
      i > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Gt(f) === m && // avoid comparing the child with its parent
      h[h.length - 1].path !== m ? h.findIndex(ee.bind(null, c[i - 2])) : g
    );
  }), u = W(() => a.value > -1 && ds(n.params, s.value.params)), l = W(() => a.value > -1 && a.value === n.matched.length - 1 && Pn(n.params, s.value.params));
  function d(c = {}) {
    if (fs(c)) {
      const i = t[M(e.replace) ? "replace" : "push"](
        M(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(we);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => i), i;
    }
    return Promise.resolve();
  }
  if (P.NODE_ENV !== "production" && J) {
    const c = Zt();
    if (c) {
      const i = {
        route: s.value,
        isActive: u.value,
        isExactActive: l.value,
        error: null
      };
      c.__vrl_devtools = c.__vrl_devtools || [], c.__vrl_devtools.push(i), Yt(() => {
        i.route = s.value, i.isActive = u.value, i.isExactActive = l.value, i.error = Ae(M(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: W(() => s.value.href),
    isActive: u,
    isExactActive: l,
    navigate: d
  };
}
function cs(e) {
  return e.length === 1 ? e[0] : e;
}
const us = /* @__PURE__ */ D({
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
  useLink: Ht,
  setup(e, { slots: t }) {
    const n = er(Ht(e)), { options: r } = K(Me), o = W(() => ({
      [zt(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [zt(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && cs(t.default(n));
      return e.custom ? s : x("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, s);
    };
  }
}), ls = us;
function fs(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function ds(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!F(o) || o.length !== r.length || r.some((s, a) => s !== o[a]))
      return !1;
  }
  return !0;
}
function Gt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const zt = (e, t, n) => e ?? t ?? n, hs = /* @__PURE__ */ D({
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
    P.NODE_ENV !== "production" && gs();
    const r = K(ft), o = W(() => e.route || r.value), s = K(Ut, 0), a = W(() => {
      let d = M(s);
      const { matched: c } = o.value;
      let i;
      for (; (i = c[d]) && !i.components; )
        d++;
      return d;
    }), u = W(() => o.value.matched[a.value]);
    le(Ut, W(() => a.value + 1)), le(is, u), le(ft, o);
    const l = Y();
    return z(() => [l.value, u.value, e.name], ([d, c, i], [f, h, g]) => {
      c && (c.instances[i] = d, h && h !== c && d && d === f && (c.leaveGuards.size || (c.leaveGuards = h.leaveGuards), c.updateGuards.size || (c.updateGuards = h.updateGuards))), d && c && // if there is no instance but to and from are the same this might be
      // the first visit
      (!h || !ee(c, h) || !f) && (c.enterCallbacks[i] || []).forEach((m) => m(d));
    }, { flush: "post" }), () => {
      const d = o.value, c = e.name, i = u.value, f = i && i.components[c];
      if (!f)
        return Kt(n.default, { Component: f, route: d });
      const h = i.props[c], g = h ? h === !0 ? d.params : typeof h == "function" ? h(d) : h : null, v = x(f, V({}, g, t, {
        onVnodeUnmounted: (w) => {
          w.component.isUnmounted && (i.instances[c] = null);
        },
        ref: l
      }));
      if (P.NODE_ENV !== "production" && J && v.ref) {
        const w = {
          depth: a.value,
          name: i.name,
          path: i.path,
          meta: i.meta
        };
        (F(v.ref) ? v.ref.map((R) => R.i) : [v.ref.i]).forEach((R) => {
          R.__vrv_devtools = w;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Kt(n.default, { Component: v, route: d }) || v
      );
    };
  }
});
function Kt(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const ps = hs;
function gs() {
  const e = Zt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    S(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function _e(e, t) {
  const n = V({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => Os(r, ["instances", "children", "aliasOf"]))
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
function ke(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let ms = 0;
function vs(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = ms++;
  ao({
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
        value: _e(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: c, componentInstance: i }) => {
      if (i.__vrv_devtools) {
        const f = i.__vrv_devtools;
        c.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: An
        });
      }
      F(i.__vrl_devtools) && (i.__devtoolsApi = o, i.__vrl_devtools.forEach((f) => {
        let h = f.route.path, g = Tn, m = "", v = 0;
        f.error ? (h = f.error, g = bs, v = Rs) : f.isExactActive ? (g = xn, m = "This is exactly active") : f.isActive && (g = $n, m = "This link is active"), c.tags.push({
          label: h,
          textColor: v,
          tooltip: m,
          backgroundColor: g
        });
      }));
    }), z(t.currentRoute, () => {
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
        guard: ke("beforeEach"),
        from: _e(i, "Current Location during this navigation"),
        to: _e(c, "Target location")
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
        guard: ke("afterEach")
      };
      f ? (h.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, h.status = ke("❌")) : h.status = ke("✅"), h.from = _e(i, "Current Location during this navigation"), h.to = _e(c, "Target location"), o.addTimelineEvent({
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
      i.forEach(Mn), c.filter && (i = i.filter((f) => (
        // save matches state based on the payload
        dt(f, c.filter.toLowerCase())
      ))), i.forEach((f) => jn(f, t.currentRoute.value)), c.rootNodes = i.map(Dn);
    }
    let d;
    o.on.getInspectorTree((c) => {
      d = c, c.app === e && c.inspectorId === u && l();
    }), o.on.getInspectorState((c) => {
      if (c.app === e && c.inspectorId === u) {
        const f = n.getRoutes().find((h) => h.record.__vd_id === c.nodeId);
        f && (c.state = {
          options: _s(f)
        });
      }
    }), o.sendInspectorTree(u), o.sendInspectorState(u);
  });
}
function ys(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function _s(e) {
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
        display: e.keys.map((r) => `${r.name}${ys(r)}`).join(" "),
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
const An = 15485081, $n = 2450411, xn = 8702998, ws = 2282478, Tn = 16486972, Es = 6710886, bs = 16704226, Rs = 12131356;
function Dn(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: ws
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: Tn
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: An
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: xn
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: $n
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: Es
  });
  let r = n.__vd_id;
  return r == null && (r = String(Ps++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map(Dn)
  };
}
let Ps = 0;
const Ss = /^\/(.*)\/([a-z]*)$/;
function jn(e, t) {
  const n = t.matched.length && ee(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => ee(r, e.record))), e.children.forEach((r) => jn(r, t));
}
function Mn(e) {
  e.__vd_match = !1, e.children.forEach(Mn);
}
function dt(e, t) {
  const n = String(e.re).match(Ss);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((a) => dt(a, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = fe(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((a) => dt(a, t));
}
function Os(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function ks(e) {
  const t = Jo(e.routes, e), n = e.parseQuery || os, r = e.stringifyQuery || Ft, o = e.history;
  if (P.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = ye(), a = ye(), u = ye(), l = H(X);
  let d = X;
  J && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const c = ze.bind(null, (p) => "" + p), i = ze.bind(null, bo), f = (
    // @ts-expect-error: intentionally avoid the type check
    ze.bind(null, fe)
  );
  function h(p, _) {
    let y, E;
    return Vn(p) ? (y = t.getRecordMatcher(p), P.NODE_ENV !== "production" && !y && S(`Parent route "${String(p)}" not found when adding child route`, _), E = _) : E = p, t.addRoute(E, y);
  }
  function g(p) {
    const _ = t.getRecordMatcher(p);
    _ ? t.removeRoute(_) : P.NODE_ENV !== "production" && S(`Cannot remove non-existent route "${String(p)}"`);
  }
  function m() {
    return t.getRoutes().map((p) => p.record);
  }
  function v(p) {
    return !!t.getRecordMatcher(p);
  }
  function w(p, _) {
    if (_ = V({}, _ || l.value), typeof p == "string") {
      const O = Ke(n, p, _.path), I = t.resolve({ path: O.path }, _), te = o.createHref(O.fullPath);
      return P.NODE_ENV !== "production" && (te.startsWith("//") ? S(`Location "${p}" resolved to "${te}". A resolved location cannot start with multiple slashes.`) : I.matched.length || S(`No match found for location with path "${p}"`)), V(O, I, {
        params: f(I.params),
        hash: fe(O.hash),
        redirectedFrom: void 0,
        href: te
      });
    }
    if (P.NODE_ENV !== "production" && !Ae(p))
      return S(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, p), w({});
    let y;
    if (p.path != null)
      P.NODE_ENV !== "production" && "params" in p && !("name" in p) && // @ts-expect-error: the type is never
      Object.keys(p.params).length && S(`Path "${p.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), y = V({}, p, {
        path: Ke(n, p.path, _.path).path
      });
    else {
      const O = V({}, p.params);
      for (const I in O)
        O[I] == null && delete O[I];
      y = V({}, p, {
        params: i(O)
      }), _.params = i(_.params);
    }
    const E = t.resolve(y, _), C = p.hash || "";
    P.NODE_ENV !== "production" && C && !C.startsWith("#") && S(`A \`hash\` should always start with the character "#". Replace "${C}" with "#${C}".`), E.params = c(f(E.params));
    const $ = So(r, V({}, p, {
      hash: _o(C),
      path: E.path
    })), k = o.createHref($);
    return P.NODE_ENV !== "production" && (k.startsWith("//") ? S(`Location "${p}" resolved to "${k}". A resolved location cannot start with multiple slashes.`) : E.matched.length || S(`No match found for location with path "${p.path != null ? p.path : p}"`)), V({
      fullPath: $,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: C,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === Ft ? ss(p.query) : p.query || {}
      )
    }, E, {
      redirectedFrom: void 0,
      href: k
    });
  }
  function b(p) {
    return typeof p == "string" ? Ke(n, p, l.value.path) : V({}, p);
  }
  function R(p, _) {
    if (d !== p)
      return he(8, {
        from: _,
        to: p
      });
  }
  function N(p) {
    return U(p);
  }
  function A(p) {
    return N(V(b(p), { replace: !0 }));
  }
  function B(p) {
    const _ = p.matched[p.matched.length - 1];
    if (_ && _.redirect) {
      const { redirect: y } = _;
      let E = typeof y == "function" ? y(p) : y;
      if (typeof E == "string" && (E = E.includes("?") || E.includes("#") ? E = b(E) : (
        // force empty params
        { path: E }
      ), E.params = {}), P.NODE_ENV !== "production" && E.path == null && !("name" in E))
        throw S(`Invalid redirect found:
${JSON.stringify(E, null, 2)}
 when navigating to "${p.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return V({
        query: p.query,
        hash: p.hash,
        // avoid transferring params if the redirect has a path
        params: E.path != null ? {} : p.params
      }, E);
    }
  }
  function U(p, _) {
    const y = d = w(p), E = l.value, C = p.state, $ = p.force, k = p.replace === !0, O = B(y);
    if (O)
      return U(
        V(b(O), {
          state: typeof O == "object" ? V({}, C, O.state) : C,
          force: $,
          replace: k
        }),
        // keep original redirectedFrom if it exists
        _ || y
      );
    const I = y;
    I.redirectedFrom = _;
    let te;
    return !$ && It(r, E, y) && (te = he(16, { to: I, from: E }), St(
      E,
      E,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (te ? Promise.resolve(te) : Et(I, E)).catch((j) => q(j) ? (
      // navigation redirects still mark the router as ready
      q(
        j,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? j : Fe(j)
    ) : (
      // reject any unknown error
      Le(j, I, E)
    )).then((j) => {
      if (j) {
        if (q(
          j,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return P.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          It(r, w(j.to), I) && // and we have done it a couple of times
          _ && // @ts-expect-error: added only in dev
          (_._count = _._count ? (
            // @ts-expect-error
            _._count + 1
          ) : 1) > 30 ? (S(`Detected a possibly infinite redirection in a navigation guard when going from "${E.fullPath}" to "${I.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : U(
            // keep options
            V({
              // preserve an existing replacement but allow the redirect to override it
              replace: k
            }, b(j.to), {
              state: typeof j.to == "object" ? V({}, C, j.to.state) : C,
              force: $
            }),
            // preserve the original redirectedFrom if any
            _ || I
          );
      } else
        j = Rt(I, E, !0, k, C);
      return bt(I, E, j), j;
    });
  }
  function zn(p, _) {
    const y = R(p, _);
    return y ? Promise.reject(y) : Promise.resolve();
  }
  function We(p) {
    const _ = Oe.values().next().value;
    return _ && typeof _.runWithContext == "function" ? _.runWithContext(p) : p();
  }
  function Et(p, _) {
    let y;
    const [E, C, $] = Ns(p, _);
    y = Je(E.reverse(), "beforeRouteLeave", p, _);
    for (const O of E)
      O.leaveGuards.forEach((I) => {
        y.push(Z(I, p, _));
      });
    const k = zn.bind(null, p, _);
    return y.push(k), se(y).then(() => {
      y = [];
      for (const O of s.list())
        y.push(Z(O, p, _));
      return y.push(k), se(y);
    }).then(() => {
      y = Je(C, "beforeRouteUpdate", p, _);
      for (const O of C)
        O.updateGuards.forEach((I) => {
          y.push(Z(I, p, _));
        });
      return y.push(k), se(y);
    }).then(() => {
      y = [];
      for (const O of $)
        if (O.beforeEnter)
          if (F(O.beforeEnter))
            for (const I of O.beforeEnter)
              y.push(Z(I, p, _));
          else
            y.push(Z(O.beforeEnter, p, _));
      return y.push(k), se(y);
    }).then(() => (p.matched.forEach((O) => O.enterCallbacks = {}), y = Je($, "beforeRouteEnter", p, _, We), y.push(k), se(y))).then(() => {
      y = [];
      for (const O of a.list())
        y.push(Z(O, p, _));
      return y.push(k), se(y);
    }).catch((O) => q(
      O,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? O : Promise.reject(O));
  }
  function bt(p, _, y) {
    u.list().forEach((E) => We(() => E(p, _, y)));
  }
  function Rt(p, _, y, E, C) {
    const $ = R(p, _);
    if ($)
      return $;
    const k = _ === X, O = J ? history.state : {};
    y && (E || k ? o.replace(p.fullPath, V({
      scroll: k && O && O.scroll
    }, C)) : o.push(p.fullPath, C)), l.value = p, St(p, _, y, k), Fe();
  }
  let me;
  function Kn() {
    me || (me = o.listen((p, _, y) => {
      if (!Ot.listening)
        return;
      const E = w(p), C = B(E);
      if (C) {
        U(V(C, { replace: !0, force: !0 }), E).catch(we);
        return;
      }
      d = E;
      const $ = l.value;
      J && Io($t($.fullPath, y.delta), je()), Et(E, $).catch((k) => q(
        k,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? k : q(
        k,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (U(
        V(b(k.to), {
          force: !0
        }),
        E
        // avoid an uncaught rejection, let push call triggerError
      ).then((O) => {
        q(
          O,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !y.delta && y.type === de.pop && o.go(-1, !1);
      }).catch(we), Promise.reject()) : (y.delta && o.go(-y.delta, !1), Le(k, E, $))).then((k) => {
        k = k || Rt(
          // after navigation, all matched components are resolved
          E,
          $,
          !1
        ), k && (y.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !q(
          k,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-y.delta, !1) : y.type === de.pop && q(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), bt(E, $, k);
      }).catch(we);
    }));
  }
  let Be = ye(), Pt = ye(), Se;
  function Le(p, _, y) {
    Fe(p);
    const E = Pt.list();
    return E.length ? E.forEach((C) => C(p, _, y)) : (P.NODE_ENV !== "production" && S("uncaught error during route navigation:"), console.error(p)), Promise.reject(p);
  }
  function qn() {
    return Se && l.value !== X ? Promise.resolve() : new Promise((p, _) => {
      Be.add([p, _]);
    });
  }
  function Fe(p) {
    return Se || (Se = !p, Kn(), Be.list().forEach(([_, y]) => p ? y(p) : _()), Be.reset()), p;
  }
  function St(p, _, y, E) {
    const { scrollBehavior: C } = e;
    if (!J || !C)
      return Promise.resolve();
    const $ = !y && Ao($t(p.fullPath, 0)) || (E || !y) && history.state && history.state.scroll || null;
    return Ne().then(() => C(p, _, $)).then((k) => k && Co(k)).catch((k) => Le(k, p, _));
  }
  const Ue = (p) => o.go(p);
  let He;
  const Oe = /* @__PURE__ */ new Set(), Ot = {
    currentRoute: l,
    listening: !0,
    addRoute: h,
    removeRoute: g,
    clearRoutes: t.clearRoutes,
    hasRoute: v,
    getRoutes: m,
    resolve: w,
    options: e,
    push: N,
    replace: A,
    go: Ue,
    back: () => Ue(-1),
    forward: () => Ue(1),
    beforeEach: s.add,
    beforeResolve: a.add,
    afterEach: u.add,
    onError: Pt.add,
    isReady: qn,
    install(p) {
      const _ = this;
      p.component("RouterLink", ls), p.component("RouterView", ps), p.config.globalProperties.$router = _, Object.defineProperty(p.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => M(l)
      }), J && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !He && l.value === X && (He = !0, N(o.location).catch((C) => {
        P.NODE_ENV !== "production" && S("Unexpected error when starting the router:", C);
      }));
      const y = {};
      for (const C in X)
        Object.defineProperty(y, C, {
          get: () => l.value[C],
          enumerable: !0
        });
      p.provide(Me, _), p.provide(wt, Zn(y)), p.provide(ft, l);
      const E = p.unmount;
      Oe.add(p), p.unmount = function() {
        Oe.delete(p), Oe.size < 1 && (d = X, me && me(), me = null, l.value = X, He = !1, Se = !1), E();
      }, P.NODE_ENV !== "production" && J && vs(p, _, t);
    }
  };
  function se(p) {
    return p.reduce((_, y) => _.then(() => We(y)), Promise.resolve());
  }
  return Ot;
}
function Ns(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let a = 0; a < s; a++) {
    const u = t.matched[a];
    u && (e.matched.find((d) => ee(d, u)) ? r.push(u) : n.push(u));
    const l = e.matched[a];
    l && (t.matched.find((d) => ee(d, l)) || o.push(l));
  }
  return [n, r, o];
}
function Vs() {
  return K(Me);
}
function Cs(e) {
  return K(wt);
}
function Is(e) {
  const { immediately: t = !1, code: n } = e;
  let r = L(n);
  return t && (r = r()), r;
}
const Ee = /* @__PURE__ */ new Map();
function As(e) {
  if (!Ee.has(e)) {
    const t = Symbol();
    return Ee.set(e, t), t;
  }
  return Ee.get(e);
}
function ge(e, t) {
  var l, d;
  const n = Ge(e);
  if (!n)
    return {
      updateVforInfo: () => {
      },
      updateSlotPropValue: () => {
      }
    };
  const { varMap: r, vforRealIndexMap: o } = xs(n, t);
  if (r.size > 0) {
    const c = As(e);
    le(c, r);
  }
  tr(() => {
    r.clear(), o.clear();
  });
  const s = oe({ attached: { varMap: r, sid: e } });
  Br({
    watchConfigs: n.py_watch || [],
    computedConfigs: n.web_computed || [],
    varMapGetter: s,
    sid: e
  }), (l = n.js_watch) == null || l.forEach((c) => {
    Yr(c, s);
  }), (d = n.vue_watch) == null || d.forEach((c) => {
    Qr(c, s);
  });
  function a(c, i) {
    const f = Ge(c);
    if (!f.vfor)
      return;
    const { fi: h, fv: g } = f.vfor;
    h && (r.get(h.id).value = i.index), g && (o.get(g.id).value = i.index);
  }
  function u(c) {
    const { sid: i, value: f } = c;
    if (!i)
      return;
    const h = Ge(i), { id: g } = h.sp, m = r.get(g);
    m.value = f;
  }
  return {
    updateVforInfo: a,
    updateSlotPropValue: u
  };
}
function oe(e) {
  const { attached: t, sidCollector: n } = e || {}, [r, o, s] = Ts(n);
  t && r.set(t.sid, t.varMap);
  const a = o ? Cs() : null, u = s ? Vs() : null, l = o ? () => a : () => {
    throw new Error("Route params not found");
  }, d = s ? () => u : () => {
    throw new Error("Router not found");
  };
  function c(m) {
    const v = Ye(f(m));
    return ln(v, m.path ?? [], c);
  }
  function i(m) {
    const v = f(m);
    return Sr(v, {
      paths: m.path,
      getBindableValueFn: c
    });
  }
  function f(m) {
    return $r(m) ? () => l()[m.prop] : r.get(m.sid).get(m.id);
  }
  function h(m, v) {
    if (vt(m)) {
      const w = f(m);
      if (m.path) {
        fn(w.value, m.path, v, c);
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
function Wn(e) {
  const t = Ee.get(e);
  return K(t);
}
function $s(e) {
  const t = Wn(e);
  if (t === void 0)
    throw new Error(`Scope not found: ${e}`);
  return t;
}
function xs(e, t) {
  var s, a, u, l, d, c;
  const n = /* @__PURE__ */ new Map(), r = /* @__PURE__ */ new Map(), o = oe({
    attached: { varMap: n, sid: e.id }
  });
  if (e.data && e.data.forEach((i) => {
    n.set(i.id, i.value);
  }), e.jsFn && e.jsFn.forEach((i) => {
    const f = Is(i);
    n.set(i.id, () => f);
  }), e.vfor) {
    if (!t || !t.initVforInfo)
      throw new Error("Init vfor info not found");
    const { fv: i, fi: f, fk: h } = e.vfor, { index: g, keyValue: m, config: v } = t.initVforInfo;
    if (i) {
      const w = H(g);
      r.set(i.id, w);
      const { sid: b } = v, R = Zr(b), N = ue(() => ({
        get() {
          const A = R.value;
          return Array.isArray(A) ? A[w.value] : Object.values(A)[w.value];
        },
        set(A) {
          const B = R.value;
          if (!Array.isArray(B)) {
            B[m] = A;
            return;
          }
          B[w.value] = A;
        }
      }));
      n.set(i.id, N);
    }
    f && n.set(f.id, H(g)), h && n.set(h.id, H(m));
  }
  if (e.sp) {
    const { id: i } = e.sp, f = ((s = t == null ? void 0 : t.initSlotPropInfo) == null ? void 0 : s.value) || null;
    n.set(i, H(f));
  }
  return (a = e.eRefs) == null || a.forEach((i) => {
    n.set(i.id, H(null));
  }), (u = e.refs) == null || u.forEach((i) => {
    const f = Or(i);
    n.set(i.id, f);
  }), (l = e.web_computed) == null || l.forEach((i) => {
    const f = Nr(i);
    n.set(i.id, f);
  }), (d = e.js_computed) == null || d.forEach((i) => {
    const f = Vr(
      i,
      o
    );
    n.set(i.id, f);
  }), (c = e.vue_computed) == null || c.forEach((i) => {
    const f = kr(
      i,
      o
    );
    n.set(i.id, f);
  }), { varMap: n, vforRealIndexMap: r };
}
function Ts(e) {
  const t = /* @__PURE__ */ new Map();
  if (e) {
    const { sids: n, needRouteParams: r = !0, needRouter: o = !0 } = e;
    for (const s of n)
      t.set(s, $s(s));
    return [t, r, o];
  }
  for (const n of Ee.keys()) {
    const r = Wn(n);
    r !== void 0 && t.set(n, r);
  }
  return [t, !0, !0];
}
const Ds = D(js, {
  props: ["vforConfig", "vforIndex", "vforKeyValue"]
});
function js(e) {
  const { sid: t, items: n = [] } = e.vforConfig, { updateVforInfo: r } = ge(t, {
    initVforInfo: {
      config: e.vforConfig,
      index: e.vforIndex,
      keyValue: e.vforKeyValue
    }
  });
  return () => (r(t, {
    index: e.vforIndex,
    keyValue: e.vforKeyValue
  }), n.length === 1 ? pe(n[0]) : n.map((o) => pe(o)));
}
function qt(e) {
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
const Bn = D(Ms, {
  props: ["config"]
});
function Ms(e) {
  const { fkey: t, tsGroup: n = {} } = e.config, r = oe(), s = Ls(t ?? "index"), a = Fs(e.config, r);
  return Xr(e.config, a), () => {
    const u = nr(a.value, (...l) => {
      const d = l[0], c = l[2] !== void 0, i = c ? l[2] : l[1], f = c ? l[1] : i, h = s(d, i);
      return x(Ds, {
        key: h,
        vforIndex: i,
        vforKeyValue: f,
        vforConfig: e.config
      });
    });
    return n && Object.keys(n).length > 0 ? x(en, n, {
      default: () => u
    }) : u;
  };
}
const Ws = (e) => e, Bs = (e, t) => t;
function Ls(e) {
  const t = Er(e);
  return typeof t == "function" ? t : e === "item" ? Ws : Bs;
}
function Fs(e, t) {
  const { type: n, value: r } = e.array, o = n === ot.range;
  if (n === ot.const || o && typeof r == "number") {
    const a = o ? qt({
      end: Math.max(0, r)
    }) : r;
    return ue(() => ({
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
    return ue(() => ({
      get() {
        return qt({
          end: Math.max(0, u.value)
        });
      },
      set() {
        throw new Error("Cannot set value to range array");
      }
    }));
  }
  return ue(() => {
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
const Ln = D(Us, {
  props: ["config"]
});
function Us(e) {
  const { sid: t, items: n, on: r } = e.config;
  Pe(t) && ge(t);
  const o = oe();
  return () => (typeof r == "boolean" ? r : o.getValue(r)) ? n.map((a) => pe(a)) : void 0;
}
const Jt = D(Hs, {
  props: ["slotConfig"]
});
function Hs(e) {
  const { sid: t, items: n } = e.slotConfig;
  return Pe(t) && ge(t), () => n.map((r) => pe(r));
}
const Qe = ":default", Fn = D(Gs, {
  props: ["config"]
});
function Gs(e) {
  const { on: t, caseValues: n, slots: r, sid: o } = e.config;
  Pe(o) && ge(o);
  const s = oe();
  return () => {
    const a = s.getValue(t), u = n.map((l, d) => {
      const c = d.toString(), i = r[c];
      return l === a ? x(Jt, { slotConfig: i, key: c }) : null;
    }).filter(Boolean);
    return u.length === 0 && Qe in r ? x(Jt, {
      slotConfig: r[Qe],
      key: Qe
    }) : u;
  };
}
const zs = "on:mounted";
function Ks(e, t, n) {
  if (!t)
    return e;
  const r = yt(() => []);
  t.map(([u, l]) => {
    const d = qs(l, n), { eventName: c, handleEvent: i } = Zs({
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
  const { [zs]: s, ...a } = o;
  return e = Ve(e, a), s && (e = tn(e, [
    [
      {
        mounted(u) {
          s(u);
        }
      }
    ]
  ])), e;
}
function qs(e, t) {
  if (e.type === "web") {
    const n = Js(e, t);
    return Qs(e, n, t);
  } else {
    if (e.type === "vue")
      return Xs(e, t);
    if (e.type === "js")
      return Ys(e, t);
  }
  throw new Error(`unknown event type ${e}`);
}
function Js(e, t) {
  const { inputs: n = [] } = e;
  return (...r) => n.map(({ value: o, type: s }) => {
    if (s === G.EventContext) {
      const { path: a } = o;
      if (a.startsWith(":")) {
        const u = a.slice(1);
        return L(u)(...r);
      }
      return qr(r[0], a.split("."));
    }
    return s === G.Ref ? t.getValue(o) : o;
  });
}
function Qs(e, t, n) {
  async function r(...o) {
    const s = t(...o), a = pn({
      config: e.preSetup,
      varGetter: n
    });
    try {
      a.run();
      const u = await hn().eventSend(e, s);
      if (!u)
        return;
      Te(u, e.sets, n);
    } finally {
      a.tryReset();
    }
  }
  return r;
}
function Ys(e, t) {
  const { sets: n, code: r, inputs: o = [] } = e, s = L(r);
  function a(...u) {
    const l = o.map(({ value: c, type: i }) => {
      if (i === G.EventContext) {
        if (c.path.startsWith(":")) {
          const f = c.path.slice(1);
          return L(f)(...u);
        }
        return Kr(u[0], c.path.split("."));
      }
      if (i === G.Ref)
        return mn(t.getValue(c));
      if (i === G.Data)
        return c;
      if (i === G.JsFn)
        return t.getValue(c);
      throw new Error(`unknown input type ${i}`);
    }), d = s(...l);
    if (n !== void 0) {
      const i = n.length === 1 ? [d] : d, f = i.map((h) => h === void 0 ? 1 : 0);
      Te(
        { values: i, types: f },
        n,
        t
      );
    }
  }
  return a;
}
function Xs(e, t) {
  const { code: n, inputs: r = {} } = e, o = De(
    r,
    (u) => u.type !== G.Data ? t.getVueRefObject(u.value) : u.value
  ), s = L(n, o);
  function a(...u) {
    s(...u);
  }
  return a;
}
function Zs(e) {
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
  const l = a.length > 0 ? t + a.join("") : t, d = u.length > 0 ? rr(r, u) : r;
  return {
    eventName: l,
    handleEvent: d
  };
}
function ei(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((a) => t.getValue(a))
    ) : n.push(
      De(
        s,
        (a) => t.getValue(a)
      )
    );
  });
  const r = or([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function ti(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return Ce(n);
  const { str: r, map: o, bind: s } = n, a = [];
  return r && a.push(r), o && a.push(
    De(
      o,
      (u) => t.getValue(u)
    )
  ), s && a.push(...s.map((u) => t.getValue(u))), Ce(a);
}
function $e(e, t = !0) {
  if (!(typeof e != "object" || e === null)) {
    if (Array.isArray(e)) {
      t && e.forEach((n) => $e(n, !0));
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
        t && $e(r, !0);
  }
}
function ni(e, t) {
  const n = e.startsWith(":");
  return n && (e = e.slice(1), t = L(t)), { name: e, value: t, isFunc: n };
}
function ri(e, t, n) {
  var o;
  const r = {};
  return Nt(e.bProps || {}, (s, a) => {
    const u = n.getValue(s);
    Re(u) || ($e(u), r[a] = oi(u, a));
  }), (o = e.proxyProps) == null || o.forEach((s) => {
    const a = n.getValue(s);
    typeof a == "object" && Nt(a, (u, l) => {
      const { name: d, value: c } = ni(l, u);
      r[d] = c;
    });
  }), { ...t, ...r };
}
function oi(e, t) {
  return t === "innerText" ? xe(e) : e;
}
const si = D(ii, {
  props: ["slotPropValue", "config"]
});
function ii(e) {
  const { sid: t, items: n } = e.config, r = Pe(t) ? ge(t, {
    initSlotPropInfo: {
      value: e.slotPropValue
    }
  }).updateSlotPropValue : ai;
  return () => (r({ sid: t, value: e.slotPropValue }), n.map((o) => pe(o)));
}
function ai() {
}
function ci(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return t ? ht(n[":"]) : gn(n, { keyFn: (a) => a === ":" ? "default" : a, valueFn: (a) => (u) => a.use_prop ? ui(u, a) : ht(a) });
}
function ui(e, t) {
  return x(si, { config: t, slotPropValue: e });
}
function li(e, t, n) {
  const r = [], { dir: o = [] } = t;
  return o.forEach((s) => {
    const { sys: a, name: u, arg: l, value: d, mf: c } = s;
    if (u === "vmodel") {
      const i = n.getVueRefObject(d);
      if (e = Ve(e, {
        [`onUpdate:${l}`]: (f) => {
          i.value = f;
        }
      }), a === 1) {
        const f = c ? Object.fromEntries(c.map((h) => [h, !0])) : {};
        r.push([sr, i.value, void 0, f]);
      } else
        e = Ve(e, {
          [l]: i.value
        });
    } else if (u === "vshow") {
      const i = n.getVueRefObject(d);
      r.push([ir, i.value]);
    } else
      console.warn(`Directive ${u} is not supported yet`);
  }), tn(e, r);
}
function fi(e, t, n) {
  const { eRef: r } = t;
  return r ? Ve(e, { ref: n.getVueRefObject(r) }) : e;
}
const Un = Symbol();
function di(e) {
  le(Un, e);
}
function Hi() {
  return K(Un);
}
const hi = D(pi, {
  props: ["config"]
});
function pi(e) {
  const { config: t } = e, n = oe({
    sidCollector: new gi(t).getCollectInfo()
  });
  t.varGetterStrategy && di(n);
  const r = t.props ?? {};
  return $e(r, !0), () => {
    const { tag: o } = t, s = typeof o == "string" ? o : n.getValue(o), a = ar(s), u = typeof a == "string", l = ti(t, n), { styles: d, hasStyle: c } = ei(t, n), i = ci(t, u), f = ri(t, r, n), h = cr(f) || {};
    c && (h.style = d), l && (h.class = l);
    let g = x(a, { ...h }, i);
    return g = Ks(g, t.events, n), g = fi(g, t, n), li(g, t, n);
  };
}
class gi {
  constructor(t) {
    T(this, "sids", /* @__PURE__ */ new Set());
    T(this, "needRouteParams", !0);
    T(this, "needRouter", !0);
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
    dn(t) && this.sids.add(t.sid);
  }
  _handleEventInputs(t) {
    if (t.type === "js" || t.type === "web") {
      const { inputs: n } = t;
      n == null || n.forEach((r) => {
        if (r.type === G.Ref) {
          const o = r.value;
          this._tryExtractSidToCollection(o), this._extendWithPaths(o);
        }
      });
    } else if (t.type === "vue") {
      const { inputs: n } = t;
      if (n) {
        const r = Object.values(n);
        r == null || r.forEach((o) => {
          if (o.type === G.Ref) {
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
        vt(r.ref) && (this.sids.add(r.ref.sid), this._extendWithPaths(r.ref));
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
      if (Rr(r)) {
        const o = Pr(r);
        this._tryExtractSidToCollection(o), o.path && n.push(...o.path);
      }
    }
  }
}
function pe(e, t) {
  return Cr(e) ? x(Bn, { config: e, key: t }) : Ir(e) ? x(Ln, { config: e, key: t }) : Ar(e) ? x(Fn, { config: e, key: t }) : x(hi, { config: e, key: t });
}
function ht(e, t) {
  return x(Hn, { slotConfig: e, key: t });
}
const Hn = D(mi, {
  props: ["slotConfig"]
});
function mi(e) {
  const { sid: t, items: n } = e.slotConfig;
  return Pe(t) && ge(t), () => n.map((r) => pe(r));
}
function vi(e, t) {
  const { state: n, isReady: r, isLoading: o } = wr(async () => {
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
function yi(e) {
  const t = Y(!1), n = Y("");
  function r(o, s) {
    let a;
    return s.component ? a = `Error captured from component:tag: ${s.component.tag} ; id: ${s.component.id} ` : a = "Error captured from app init", console.group(a), console.error("Component:", s.component), console.error("Error:", o), console.groupEnd(), e && (t.value = !0, n.value = `${a} ${o.message}`), !1;
  }
  return ur(r), { hasError: t, errorMessage: n };
}
let pt;
function _i(e) {
  if (e === "web" || e === "webview") {
    pt = wi;
    return;
  }
  if (e === "zero") {
    pt = Ei;
    return;
  }
  throw new Error(`Unsupported mode: ${e}`);
}
function wi(e) {
  const { assetPath: t = "/assets/icons", icon: n = "" } = e, [r, o] = n.split(":");
  return {
    assetPath: t,
    svgName: `${r}.svg`
  };
}
function Ei() {
  return {
    assetPath: "",
    svgName: ""
  };
}
function bi(e, t) {
  const n = W(() => {
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
    return x("svg", r);
  };
}
const Ri = {
  class: "app-box insta-themes",
  "data-scaling": "100%"
}, Pi = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Si = {
  key: 0,
  style: { color: "red", "font-size": "1.2em", margin: "1rem", border: "1px dashed red", padding: "1rem" }
}, Oi = /* @__PURE__ */ D({
  __name: "App",
  props: {
    config: {},
    meta: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { debug: n = !1 } = t.meta, { config: r, isLoading: o } = vi(
      t.config,
      t.configUrl
    );
    z(r, (u) => {
      u.url && (mr({
        mode: t.meta.mode,
        version: t.meta.version,
        queryPath: u.url.path,
        pathParams: u.url.params,
        webServerInfo: u.webInfo
      }), jr(t.meta.mode)), _i(t.meta.mode), vr(u);
    });
    const { hasError: s, errorMessage: a } = yi(n);
    return (u, l) => (Q(), ne("div", Ri, [
      M(o) ? (Q(), ne("div", Pi, l[0] || (l[0] = [
        nn("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (Q(), ne("div", {
        key: 1,
        class: Ce(["insta-main", M(r).class])
      }, [
        lr(M(Hn), { "slot-config": M(r) }, null, 8, ["slot-config"]),
        M(s) ? (Q(), ne("div", Si, xe(M(a)), 1)) : Xe("", !0)
      ], 2))
    ]));
  }
});
function ki(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => x(
    en,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const Ni = D(ki, {
  props: ["name", "tag"]
});
function Vi(e) {
  const { content: t, r: n = 0 } = e, r = oe(), o = n === 1 ? () => r.getValue(t) : () => t;
  return () => xe(o());
}
const Ci = D(Vi, {
  props: ["content", "r"]
});
function Ii(e) {
  return `i-size-${e}`;
}
function Ai(e) {
  return e ? `i-weight-${e}` : "";
}
function $i(e) {
  return e ? `i-text-align-${e}` : "";
}
const xi = /* @__PURE__ */ D({
  __name: "Heading",
  props: {
    text: {},
    size: {},
    weight: {},
    align: {}
  },
  setup(e) {
    const t = e, n = W(() => [
      Ii(t.size ?? "6"),
      Ai(t.weight),
      $i(t.align)
    ]);
    return (r, o) => (Q(), ne("h1", {
      class: Ce(["insta-Heading", n.value])
    }, xe(r.text), 3));
  }
}), Ti = /* @__PURE__ */ D({
  __name: "_Teleport",
  props: {
    to: {},
    defer: { type: Boolean, default: !0 },
    disabled: { type: Boolean, default: !1 }
  },
  setup(e) {
    return (t, n) => (Q(), rn(fr, {
      to: t.to,
      defer: t.defer,
      disabled: t.disabled
    }, [
      dr(t.$slots, "default")
    ], 8, ["to", "defer", "disabled"]));
  }
}), Di = ["width", "height", "color"], ji = ["xlink:href"], Mi = /* @__PURE__ */ D({
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
    const t = e, { assetPath: n, svgName: r } = pt(t), o = ie(() => t.icon ? t.icon.split(":")[1] : ""), s = ie(() => t.size || "1em"), a = ie(() => t.color || "currentColor"), u = ie(() => t.rawSvg || null), l = W(() => `${n}/${r}/#${o.value}`), d = hr(), c = bi(u, {
      size: ie(() => t.size),
      color: ie(() => t.color),
      attrs: d
    });
    return (i, f) => (Q(), ne(on, null, [
      o.value ? (Q(), ne("svg", pr({
        key: 0,
        width: s.value,
        height: s.value,
        color: a.value
      }, M(d)), [
        nn("use", { "xlink:href": l.value }, null, 8, ji)
      ], 16, Di)) : Xe("", !0),
      u.value ? (Q(), rn(M(c), { key: 1 })) : Xe("", !0)
    ], 64));
  }
});
function Wi(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => Gn(o, n)
  );
}
function Gn(e, t) {
  var u;
  const { server: n = !1, vueItem: r } = e, o = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(Bi(e, t));
  }, s = (u = r.children) == null ? void 0 : u.map(
    (l) => Gn(l, t)
  ), a = {
    ...r,
    children: s,
    component: o
  };
  return r.component.length === 0 && delete a.component, s === void 0 && delete a.children, a;
}
function Bi(e, t) {
  const { sid: n, vueItem: r } = e, { path: o, component: s } = r, a = ht(
    {
      items: s,
      sid: n
    },
    o
  ), u = x(on, null, a);
  return t ? x(gr, null, () => a) : u;
}
function Li(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? jo() : n === "memory" ? Do() : Nn();
  e.use(
    ks({
      history: r,
      routes: Wi(t)
    })
  );
}
function Gi(e, t) {
  e.component("insta-ui", Oi), e.component("vif", Ln), e.component("vfor", Bn), e.component("match", Fn), e.component("teleport", Ti), e.component("icon", Mi), e.component("ts-group", Ni), e.component("content", Ci), e.component("heading", xi), t.router && Li(e, t);
}
export {
  $e as convertDynamicProperties,
  Gi as install,
  Hi as useVarGetter
};
//# sourceMappingURL=insta-ui.js.map
