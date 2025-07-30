import { jsx as _jsx } from "react/jsx-runtime";
import { useEffect, useRef, useState } from 'react';
import { useSelector } from 'react-redux';
import Plotly from 'plotly.js-dist-min';
import { Chart } from '@deephaven/chart';
import { useApi } from '@deephaven/jsapi-bootstrap';
import { getSettings } from '@deephaven/redux';
import PlotlyExpressChartModel from './PlotlyExpressChartModel.js';
import { useHandleSceneTicks } from './useHandleSceneTicks.js';
export function PlotlyExpressChart(props) {
    const dh = useApi();
    const { fetch } = props;
    const containerRef = useRef(null);
    const [model, setModel] = useState();
    const settings = useSelector((getSettings));
    const [widgetRevision, setWidgetRevision] = useState(0); // Used to force a clean chart state on widget change
    useEffect(() => {
        let cancelled = false;
        async function init() {
            const widgetData = await fetch();
            if (!cancelled) {
                setModel(new PlotlyExpressChartModel(dh, widgetData, fetch));
                setWidgetRevision(r => r + 1);
            }
        }
        init();
        return () => {
            cancelled = true;
        };
    }, [dh, fetch]);
    useHandleSceneTicks(model, containerRef.current);
    return model ? (_jsx(Chart
    // eslint-disable-next-line react/jsx-props-no-spreading, @typescript-eslint/ban-ts-comment
    // @ts-ignore
    , { containerRef: containerRef, model: model, settings: settings, Plotly: Plotly }, widgetRevision)) : null;
}
export default PlotlyExpressChart;
//# sourceMappingURL=PlotlyExpressChart.js.map