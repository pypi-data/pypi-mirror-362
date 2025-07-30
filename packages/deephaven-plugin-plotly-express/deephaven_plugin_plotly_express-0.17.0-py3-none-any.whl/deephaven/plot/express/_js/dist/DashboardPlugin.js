import { useCallback, useEffect } from 'react';
import { nanoid } from 'nanoid';
import { LayoutUtils, PanelEvent, useListener, } from '@deephaven/dashboard';
import PlotlyExpressChartPanel from './PlotlyExpressChartPanel.js';
export function DashboardPlugin(props) {
    const { id, layout, registerComponent } = props;
    const handlePanelOpen = useCallback(async ({ dragEvent, fetch, metadata = {}, panelId = nanoid(), widget, }) => {
        const { type, name } = widget;
        if (type !== 'deephaven.plot.express.DeephavenFigure') {
            return;
        }
        const config = {
            type: 'react-component',
            component: 'PlotlyPanel',
            props: {
                localDashboardId: id,
                id: panelId,
                metadata: Object.assign(Object.assign(Object.assign({}, metadata), widget), { figure: name }),
                fetch,
            },
            title: name !== null && name !== void 0 ? name : undefined,
            id: panelId,
        };
        const { root } = layout;
        LayoutUtils.openComponent({ root, config, dragEvent });
    }, [id, layout]);
    useEffect(function registerComponentsAndReturnCleanup() {
        const cleanups = [
            registerComponent('PlotlyPanel', PlotlyExpressChartPanel),
        ];
        return () => {
            cleanups.forEach(cleanup => cleanup());
        };
    }, [registerComponent]);
    useListener(layout.eventHub, PanelEvent.OPEN, handlePanelOpen);
    return null;
}
export default DashboardPlugin;
//# sourceMappingURL=DashboardPlugin.js.map