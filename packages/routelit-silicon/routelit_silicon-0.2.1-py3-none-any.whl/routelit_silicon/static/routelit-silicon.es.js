import { jsx as r, jsxs as c } from "react/jsx-runtime";
import { useState as m } from "react";
import { componentStore as o } from "routelit-client";
function d({ children: e, className: t = "" }) {
  return /* @__PURE__ */ r("div", { className: "root " + t, children: e });
}
function u({ isOpen: e, toggle: t }) {
  return /* @__PURE__ */ r("button", { className: "sidebar-toggle", onClick: t, children: e ? "x" : ">" });
}
function l({ defaultOpen: e, children: t, className: i, ...s }) {
  const [n, a] = m(e || !1);
  return /* @__PURE__ */ c("aside", { className: i, ...s, children: [
    /* @__PURE__ */ r("div", { className: `content ${n ? "" : "hidden"}`, children: t }),
    /* @__PURE__ */ r(u, { isOpen: n, toggle: () => a(!n) })
  ] });
}
function f({ children: e, ...t }) {
  return /* @__PURE__ */ r("main", { ...t, children: e });
}
o.register("root", d);
o.register("sidebar", l);
o.register("main", f);
o.forceUpdate();
export {
  f as Main,
  d as Root,
  l as Sidebar
};
