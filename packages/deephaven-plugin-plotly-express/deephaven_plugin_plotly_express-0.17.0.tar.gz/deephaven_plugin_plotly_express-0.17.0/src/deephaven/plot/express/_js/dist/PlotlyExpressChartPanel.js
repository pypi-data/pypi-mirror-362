var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
import { jsx as _jsx } from "react/jsx-runtime";
import { useCallback, useState } from 'react';
import Plotly from 'plotly.js-dist-min';
import { ChartPanel } from '@deephaven/dashboard-core-plugins';
import { useApi } from '@deephaven/jsapi-bootstrap';
import PlotlyExpressChartModel from './PlotlyExpressChartModel.js';
import { useHandleSceneTicks } from './useHandleSceneTicks.js';
export function PlotlyExpressChartPanel(props) {
    const dh = useApi();
    const { fetch, metadata = {} } = props, rest = __rest(props, ["fetch", "metadata"]);
    const [container, setContainer] = useState(null);
    const [model, setModel] = useState();
    const makeModel = useCallback(async () => {
        const widgetData = await fetch();
        const m = new PlotlyExpressChartModel(dh, widgetData, fetch);
        setModel(m);
        return m;
    }, [dh, fetch]);
    useHandleSceneTicks(model, container);
    return (_jsx(ChartPanel
    // eslint-disable-next-line react/jsx-props-no-spreading
    , Object.assign({}, rest, { containerRef: setContainer, makeModel: makeModel, Plotly: Plotly, metadata: metadata })));
}
export default PlotlyExpressChartPanel;
//# sourceMappingURL=PlotlyExpressChartPanel.js.map