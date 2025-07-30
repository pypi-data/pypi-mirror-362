import { p as a, f as o } from "./flowDb-d35e309a-DSihZQIX.js";
import { f as e, g as t } from "./styles-7383a064-B6HgaSJ2.js";
import { t as s } from "./main-5nQ2LM6l.js";
import "./graph-CmXIkTsG.js";
import "./layout-ejG4WEgY.js";
const p = {
  parser: a,
  db: o,
  renderer: e,
  styles: t,
  init: (r) => {
    r.flowchart || (r.flowchart = {}), r.flowchart.arrowMarkerAbsolute = r.arrowMarkerAbsolute, s({ flowchart: { arrowMarkerAbsolute: r.arrowMarkerAbsolute } }), e.setConf(r.flowchart), o.clear(), o.setGen("gen-2");
  }
};
export {
  p as diagram
};
//# sourceMappingURL=flowDiagram-v2-49332944-DlVVUVkv.js.map
